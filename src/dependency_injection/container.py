import inspect
from dataclasses import is_dataclass

from typing import Any, Callable, Dict, List, Optional, TypeVar, Type, Union

try:
    from typing import get_origin, get_args
except ImportError:
    # Fallback if on Python <= 3.8
    def get_origin(tp):
        return getattr(tp, "__origin__", None)

    def get_args(tp):
        return getattr(tp, "__args__", ())


from dependency_injection.tags.all_tagged import AllTagged
from dependency_injection.tags.any_tagged import AnyTagged
from dependency_injection.tags.tagged import Tagged
from dependency_injection.registration import Registration
from dependency_injection.scope import DEFAULT_SCOPE_NAME, Scope
from dependency_injection.utils.singleton_meta import SingletonMeta

Self = TypeVar("Self", bound="DependencyContainer")
NoneType = type(None)


DEFAULT_CONTAINER_NAME = "default_container"


class DependencyContainer(metaclass=SingletonMeta):
    _default_scope_name: Union[str, Callable[[], str]] = DEFAULT_SCOPE_NAME
    _default_container_name: Union[str, Callable[[], str]] = DEFAULT_CONTAINER_NAME

    def __init__(self, name: str):
        self.name = name
        self._registrations = {}
        self._singleton_instances = {}
        self._scoped_instances = {}
        self._has_resolved = False

    @classmethod
    def configure_default_container_name(
        cls, name_or_callable: Union[str, Callable[[], str]]
    ) -> None:
        """Override the default container name, which can be string or callable."""
        cls._default_container_name = name_or_callable

    @classmethod
    def configure_default_scope_name(
        cls, default_scope_name: Union[str, Callable[[], str]]
    ) -> None:
        """Configure the global default scope name, which can be string or callable."""
        cls._default_scope_name = default_scope_name

    @classmethod
    def get_default_scope_name(cls) -> str:
        """Return the default scope name. If it's callable, call it to get the value."""
        if callable(cls._default_scope_name):
            return cls._default_scope_name()
        return cls._default_scope_name

    @classmethod
    def get_instance(cls, name: str = None) -> Self:
        if name is None:
            name = (
                cls._default_container_name()
                if callable(cls._default_container_name)
                else cls._default_container_name
            )

        if (cls, name) not in cls._instances:
            cls._instances[(cls, name)] = cls(name)

        return cls._instances[(cls, name)]

    def register_transient(
        self,
        dependency: Type,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._register(
            dependency, implementation, Scope.TRANSIENT, tags, constructor_args
        )

    def register_scoped(
        self,
        dependency: Type,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._register(dependency, implementation, Scope.SCOPED, tags, constructor_args)

    def register_singleton(
        self,
        dependency: Type,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._register(
            dependency, implementation, Scope.SINGLETON, tags, constructor_args
        )

    def register_factory(
        self,
        dependency: Type,
        factory: Callable[[Any], Any],
        factory_args: Optional[Dict[str, Any]] = None,
        tags: Optional[set] = None,
    ) -> None:
        self._validate_registration(dependency)
        self._registrations[dependency] = Registration(
            dependency, None, Scope.FACTORY, tags, None, factory, factory_args
        )

    def register_instance(
        self, dependency: Type, instance: Any, tags: Optional[set] = None
    ) -> None:
        self._validate_registration(dependency)
        self._registrations[dependency] = Registration(
            dependency, type(instance), Scope.SINGLETON, tags=tags
        )
        self._singleton_instances[dependency] = instance

    def _register(
        self,
        dependency: Type,
        implementation: Optional[Type],
        scope: Scope,
        tags: Optional[set],
        constructor_args: Optional[Dict[str, Any]],
    ) -> None:
        implementation = implementation or dependency
        self._validate_registration(dependency)
        self._registrations[dependency] = Registration(
            dependency, implementation, scope, tags, constructor_args
        )

    def resolve(self, dependency: Type, scope_name: Optional[str] = None) -> Any:
        self._has_resolved = True
        scope_name = scope_name or self.get_default_scope_name()

        if scope_name not in self._scoped_instances:
            self._scoped_instances[scope_name] = {}

        registration = self._registrations.get(dependency)
        if not registration:
            raise KeyError(f"Dependency {dependency.__name__} is not registered.")

        constructor_args = registration.constructor_args or {}
        self._validate_constructor_args(constructor_args, registration.implementation)

        return self._resolve_by_scope(registration, scope_name)

    def _resolve_by_scope(
        self, registration: Registration, scope_name: Optional[str] = None
    ) -> Any:
        scope = registration.scope
        scope_name = scope_name or self.get_default_scope_name()

        if scope == Scope.TRANSIENT:
            return self._inject_dependencies(
                registration.implementation,
                constructor_args=registration.constructor_args,
            )
        elif scope == Scope.SCOPED:
            instances = self._scoped_instances[scope_name]
            if registration.dependency not in instances:
                instances[registration.dependency] = self._inject_dependencies(
                    registration.implementation,
                    scope_name,
                    registration.constructor_args,
                )
            return instances[registration.dependency]
        elif scope == Scope.SINGLETON:
            if registration.dependency not in self._singleton_instances:
                self._singleton_instances[
                    registration.dependency
                ] = self._inject_dependencies(
                    registration.implementation,
                    constructor_args=registration.constructor_args,
                )
            return self._singleton_instances[registration.dependency]
        elif scope == Scope.FACTORY:
            return registration.factory(**(registration.factory_args or {}))

        raise ValueError(f"Invalid dependency scope: {scope}")

    def resolve_all(
        self, tags: Optional[set] = None, match_all_tags: bool = False
    ) -> List[Any]:
        tags = tags or set()
        resolved_dependencies = []

        for registration in self._registrations.values():
            if not tags:
                # If no tags are provided, resolve all dependencies
                resolved_dependencies.append(self.resolve(registration.dependency))
            else:
                if match_all_tags:
                    # Match dependencies that have all the specified tags
                    if registration.tags and tags.issubset(registration.tags):
                        resolved_dependencies.append(
                            self.resolve(registration.dependency)
                        )
                else:
                    # Match dependencies that have any of the specified tags
                    if registration.tags and tags.intersection(registration.tags):
                        resolved_dependencies.append(
                            self.resolve(registration.dependency)
                        )

        return resolved_dependencies

    def _validate_constructor_args(
        self, constructor_args: Dict[str, Any], implementation: Type
    ) -> None:
        constructor = inspect.signature(implementation.__init__).parameters

        for arg_name, arg_value in constructor_args.items():
            if arg_name not in constructor:
                raise ValueError(
                    f"Invalid constructor argument '{arg_name}' for class "
                    f"'{implementation.__name__}'. The class does not have a "
                    f"constructor parameter with this name."
                )

            expected_type = constructor[arg_name].annotation
            if expected_type != inspect.Parameter.empty:
                if self._is_optional_type(expected_type):
                    real_type = self._unwrap_optional_type(expected_type)
                    if not isinstance(arg_value, real_type) and arg_value is not None:
                        raise TypeError(
                            f"Constructor argument '{arg_name}' "
                            f"has an incompatible type. "
                            f"Expected type: {expected_type}, "
                            f"provided type: {type(arg_value)}."
                        )
                else:
                    if not isinstance(arg_value, expected_type):
                        raise TypeError(
                            f"Constructor argument '{arg_name}' "
                            f"has an incompatible type. "
                            f"Expected type: {expected_type}, "
                            f"provided type: {type(arg_value)}."
                        )

    def _validate_registration(self, dependency: Type) -> None:
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")

    def _inject_dependencies(
        self,
        implementation: Type,
        scope_name: Optional[str] = None,
        constructor_args: Optional[Dict[str, Any]] = None,
    ) -> Type:
        scope_name = scope_name or self.get_default_scope_name()

        if is_dataclass(implementation):
            return implementation()  # Do not inject into dataclasses

        dependencies = self._resolve_constructor_args(
            implementation, scope_name, constructor_args
        )
        return implementation(**dependencies)

    def _resolve_constructor_args(
        self,
        implementation: Type,
        scope_name: str,
        constructor_args: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        constructor = inspect.signature(implementation.__init__)
        dependencies = {}

        for name, param in constructor.parameters.items():
            if name == "self":
                continue
            if param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue

            if constructor_args and name in constructor_args:
                dependencies[name] = constructor_args[name]
            else:
                try:
                    dependencies[name] = self._resolve_param_value(param, scope_name)
                except KeyError:
                    if self._should_use_default(param):
                        continue
                    raise ValueError(
                        f"Cannot resolve dependency for parameter '{name}' "
                        f"of type '{param.annotation}' in class "
                        f"'{implementation.__name__}'."
                    )

        return dependencies

    def _resolve_param_value(self, param: inspect.Parameter, scope_name: str) -> Any:
        annotation = param.annotation

        if get_origin(annotation) is list:
            return self._resolve_list_dependency(annotation)

        if self._is_optional_type(annotation):
            inner = self._unwrap_optional_type(annotation)
            try:
                return self.resolve(inner, scope_name)
            except KeyError:
                if self._should_use_default(param):
                    raise KeyError  # signal to fallback to default
                return None

        return self.resolve(annotation, scope_name)

    def _resolve_list_dependency(self, annotation: Any) -> List[Any]:
        inner = get_args(annotation)[0]
        if isinstance(inner, type) and issubclass(inner, Tagged):
            return self.resolve_all(tags={inner.tag})
        elif isinstance(inner, type) and issubclass(inner, AnyTagged):
            return self.resolve_all(tags=inner.tags, match_all_tags=False)
        elif isinstance(inner, type) and issubclass(inner, AllTagged):
            return self.resolve_all(tags=inner.tags, match_all_tags=True)
        else:
            raise ValueError(f"Unsupported list injection type: {annotation}")

    def _is_optional_type(self, annotation: Any) -> bool:
        return get_origin(annotation) is Union and type(None) in get_args(annotation)

    def _unwrap_optional_type(self, annotation: Any) -> Any:
        return next(arg for arg in get_args(annotation) if arg is not NoneType)

    def _should_use_default(self, param_info: inspect.Parameter) -> bool:
        return param_info.default is not inspect.Parameter.empty

    @classmethod
    def clear_instances(cls) -> None:
        """Clear all container instances. Useful for test teardown."""
        cls._instances.clear()
