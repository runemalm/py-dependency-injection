import inspect
from dataclasses import is_dataclass

from typing import Any, Callable, Dict, List, Optional, TypeVar, Type

from dependency_injection.registration import Registration
from dependency_injection.scope import DEFAULT_SCOPE_NAME, Scope
from dependency_injection.utils.singleton_meta import SingletonMeta

Self = TypeVar("Self", bound="DependencyContainer")


DEFAULT_CONTAINER_NAME = "default_container"


class DependencyContainer(metaclass=SingletonMeta):
    def __init__(self, name: str = None):
        self.name = name if name is not None else DEFAULT_CONTAINER_NAME
        self._registrations = {}
        self._singleton_instances = {}
        self._scoped_instances = {}
        self._has_resolved = False

    @classmethod
    def get_instance(cls, name: str = None) -> Self:
        if name is None:
            name = DEFAULT_CONTAINER_NAME

        if (cls, name) not in cls._instances:
            cls._instances[(cls, name)] = cls(name)

        return cls._instances[(cls, name)]

    def get_registrations(self) -> Dict[Type, Registration]:
        return self._registrations

    def set_registrations(self, registrations) -> None:
        if self._has_resolved:
            raise Exception(
                "You can't set registrations after a dependency has been resolved."
            )
        self._registrations = registrations

    def register_transient(
        self,
        dependency: Type,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        if implementation is None:
            implementation = dependency
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")
        self._registrations[dependency] = Registration(
            dependency, implementation, Scope.TRANSIENT, tags, constructor_args
        )

    def register_scoped(
        self,
        dependency: Type,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        if implementation is None:
            implementation = dependency
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")
        self._registrations[dependency] = Registration(
            dependency, implementation, Scope.SCOPED, tags, constructor_args
        )

    def register_singleton(
        self,
        dependency: Type,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        if implementation is None:
            implementation = dependency
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")
        self._registrations[dependency] = Registration(
            dependency, implementation, Scope.SINGLETON, tags, constructor_args
        )

    def register_factory(
        self,
        dependency: Type,
        factory: Callable[[Any], Any],
        factory_args: Optional[Dict[str, Any]] = None,
        tags: Optional[set] = None,
    ) -> None:
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")
        self._registrations[dependency] = Registration(
            dependency, None, Scope.FACTORY, None, tags, factory, factory_args
        )

    def register_instance(
        self, dependency: Type, instance: Any, tags: Optional[set] = None
    ) -> None:
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")
        self._registrations[dependency] = Registration(
            dependency, type(instance), Scope.SINGLETON, constructor_args={}, tags=tags
        )
        self._singleton_instances[dependency] = instance

    def resolve(self, dependency: Type, scope_name: str = DEFAULT_SCOPE_NAME) -> Type:
        self._has_resolved = True

        if scope_name not in self._scoped_instances:
            self._scoped_instances[scope_name] = {}

        if dependency not in self._registrations:
            raise KeyError(f"Dependency {dependency.__name__} is not registered.")

        registration = self._registrations[dependency]
        scope = registration.scope
        implementation = registration.implementation
        constructor_args = registration.constructor_args

        self._validate_constructor_args(
            constructor_args=constructor_args, implementation=implementation
        )

        if scope == Scope.TRANSIENT:
            return self._inject_dependencies(
                implementation=implementation, constructor_args=constructor_args
            )
        elif scope == Scope.SCOPED:
            if dependency not in self._scoped_instances[scope_name]:
                self._scoped_instances[scope_name][
                    dependency
                ] = self._inject_dependencies(
                    implementation=implementation,
                    scope_name=scope_name,
                    constructor_args=constructor_args,
                )
            return self._scoped_instances[scope_name][dependency]
        elif scope == Scope.SINGLETON:
            if dependency not in self._singleton_instances:
                self._singleton_instances[dependency] = self._inject_dependencies(
                    implementation=implementation, constructor_args=constructor_args
                )
            return self._singleton_instances[dependency]
        elif scope == Scope.FACTORY:
            factory = registration.factory
            factory_args = registration.factory_args or {}
            return factory(**factory_args)

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
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Constructor argument '{arg_name}' has an incompatible type. "
                        f"Expected type: {expected_type}, "
                        f"provided type: {type(arg_value)}."
                    )

    def _inject_dependencies(
        self,
        implementation: Type,
        scope_name: str = None,
        constructor_args: Optional[Dict[str, Any]] = None,
    ) -> Type:
        if is_dataclass(implementation):
            return implementation()  # Do not inject into dataclasses

        constructor = inspect.signature(implementation.__init__)
        params = constructor.parameters

        dependencies = {}
        for param_name, param_info in params.items():
            if param_name != "self":
                # Check for *args and **kwargs
                if param_info.kind == inspect.Parameter.VAR_POSITIONAL:
                    # *args parameter
                    pass
                elif param_info.kind == inspect.Parameter.VAR_KEYWORD:
                    # **kwargs parameter
                    pass
                else:
                    # Check if constructor_args has an argument with the same name
                    if constructor_args and param_name in constructor_args:
                        dependencies[param_name] = constructor_args[param_name]
                    else:
                        dependencies[param_name] = self.resolve(
                            param_info.annotation, scope_name=scope_name
                        )

        return implementation(**dependencies)
