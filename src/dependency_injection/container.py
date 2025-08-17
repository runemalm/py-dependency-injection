import inspect
import warnings
from dataclasses import is_dataclass

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
    Type,
    Union,
    get_args,
    get_origin,
)

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

    # -------------
    # Registrations
    # -------------

    def register_transient(
        self,
        service: Type = None,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_kwargs: Optional[Dict[str, Any]] = None,
        **aliases: Any,
    ) -> None:
        # when we remove deprecated aliases in next major make service non-optional arg
        if "dependency" in aliases:
            warnings.warn(
                "`dependency` is deprecated; use `service`.",
                DeprecationWarning,
                stacklevel=2,
            )
            service = aliases.pop("dependency")
        if "constructor_args" in aliases:
            warnings.warn(
                "`constructor_args` is deprecated; use `constructor_kwargs`.",
                DeprecationWarning,
                stacklevel=2,
            )
            constructor_kwargs = aliases.pop("constructor_args")
        if aliases:
            raise TypeError(f"Unexpected keyword(s): {', '.join(aliases)}")
        if service is None:
            raise TypeError("`service` is required (or use deprecated `dependency=`).")

        self._register(
            service, implementation, Scope.TRANSIENT, tags, constructor_kwargs
        )

    def register_scoped(
        self,
        service: Type = None,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_kwargs: Optional[Dict[str, Any]] = None,
        **aliases: Any,
    ) -> None:
        # when we remove deprecated aliases in next major make service non-optional arg
        if "dependency" in aliases:
            warnings.warn(
                "`dependency` is deprecated; use `service`.",
                DeprecationWarning,
                stacklevel=2,
            )
            service = aliases.pop("dependency")
        if "constructor_args" in aliases:
            warnings.warn(
                "`constructor_args` is deprecated; use `constructor_kwargs`.",
                DeprecationWarning,
                stacklevel=2,
            )
            constructor_kwargs = aliases.pop("constructor_args")
        if aliases:
            raise TypeError(f"Unexpected keyword(s): {', '.join(aliases)}")
        if service is None:
            raise TypeError("`service` is required (or use deprecated `dependency=`).")

        self._register(service, implementation, Scope.SCOPED, tags, constructor_kwargs)

    def register_singleton(
        self,
        service: Type = None,
        implementation: Optional[Type] = None,
        tags: Optional[set] = None,
        constructor_kwargs: Optional[Dict[str, Any]] = None,
        **aliases: Any,
    ) -> None:
        # when we remove deprecated aliases in next major make service non-optional arg
        if "dependency" in aliases:
            warnings.warn(
                "`dependency` is deprecated; use `service`.",
                DeprecationWarning,
                stacklevel=2,
            )
            service = aliases.pop("dependency")
        if "constructor_args" in aliases:
            warnings.warn(
                "`constructor_args` is deprecated; use `constructor_kwargs`.",
                DeprecationWarning,
                stacklevel=2,
            )
            constructor_kwargs = aliases.pop("constructor_args")
        if aliases:
            raise TypeError(f"Unexpected keyword(s): {', '.join(aliases)}")
        if service is None:
            raise TypeError("`service` is required (or use deprecated `dependency=`).")

        self._register(
            service, implementation, Scope.SINGLETON, tags, constructor_kwargs
        )

    def register_factory(
        self,
        service: Type = None,
        factory: Callable[[Any], Any] = None,
        factory_kwargs: Optional[Dict[str, Any]] = None,
        tags: Optional[set] = None,
        **aliases: Any,
    ) -> None:
        # when we remove deprecated aliases in next major make service and
        # factory non-optional args
        if "dependency" in aliases:
            warnings.warn(
                "`dependency` is deprecated; use `service`.",
                DeprecationWarning,
                stacklevel=2,
            )
            service = aliases.pop("dependency")
        if "factory_args" in aliases:
            warnings.warn(
                "`factory_args` is deprecated; use `factory_kwargs`.",
                DeprecationWarning,
                stacklevel=2,
            )
            factory_kwargs = aliases.pop("factory_args")
        if aliases:
            raise TypeError(f"Unexpected keyword(s): {', '.join(aliases)}")
        if service is None:
            raise TypeError("`service` is required (or use deprecated `dependency=`).")
        if factory is None:
            raise TypeError("`factory` is required.")

        self._validate_registration(service)
        self._registrations[service] = Registration(
            service=service,
            implementation=None,
            scope=Scope.FACTORY,
            tags=tags,
            constructor_kwargs=None,
            factory=factory,
            factory_kwargs=factory_kwargs,
        )

    def register_instance(
        self,
        service: Type = None,
        instance: Any = None,
        tags: Optional[set] = None,
        **aliases: Any,
    ) -> None:
        # when we remove deprecated aliases in next major make service non-optional arg
        if "dependency" in aliases:
            warnings.warn(
                "`dependency` is deprecated; use `service`.",
                DeprecationWarning,
                stacklevel=2,
            )
            service = aliases.pop("dependency")
        if aliases:
            raise TypeError(f"Unexpected keyword(s): {', '.join(aliases)}")
        if service is None:
            raise TypeError("`service` is required (or use deprecated `dependency=`).")
        if instance is None:
            raise TypeError("`instance` is required.")

        self._validate_registration(service)
        self._registrations[service] = Registration(
            service=service,
            implementation=type(instance),
            scope=Scope.SINGLETON,
            tags=tags,
        )
        self._singleton_instances[service] = instance

    def _register(
        self,
        service: Type,
        implementation: Optional[Type],
        scope: Scope,
        tags: Optional[set],
        constructor_kwargs: Optional[Dict[str, Any]],
    ) -> None:
        implementation = implementation or service
        self._validate_registration(service)
        self._registrations[service] = Registration(
            service=service,
            implementation=implementation,
            scope=scope,
            tags=tags,
            constructor_kwargs=constructor_kwargs,
        )

    # --------
    # Resolve
    # --------

    def resolve(
        self, service: Type = None, scope_name: Optional[str] = None, **aliases: Any
    ) -> Any:
        if "dependency" in aliases:
            warnings.warn(
                "`dependency` is deprecated; use `service`.",
                DeprecationWarning,
                stacklevel=2,
            )
            service = aliases.pop("dependency")
        if aliases:
            raise TypeError(f"Unexpected keyword(s): {', '.join(aliases)}")

        self._has_resolved = True
        scope_name = scope_name or self.get_default_scope_name()

        if scope_name not in self._scoped_instances:
            self._scoped_instances[scope_name] = {}

        registration = self._registrations.get(service)
        if not registration:
            raise KeyError(
                f"Service {getattr(service, '__name__', service)!r} is not registered."
            )

        constructor_kwargs = registration.constructor_kwargs or {}
        self._validate_constructor_kwargs(
            constructor_kwargs, registration.implementation
        )

        return self._resolve_by_scope(registration, scope_name)

    def _resolve_by_scope(
        self, registration: Registration, scope_name: Optional[str] = None
    ) -> Any:
        scope = registration.scope
        scope_name = scope_name or self.get_default_scope_name()

        if scope == Scope.TRANSIENT:
            return self._inject_dependencies(
                registration.implementation,
                constructor_kwargs=registration.constructor_kwargs,
            )
        elif scope == Scope.SCOPED:
            instances = self._scoped_instances[scope_name]
            if registration.service not in instances:
                instances[registration.service] = self._inject_dependencies(
                    registration.implementation,
                    scope_name,
                    registration.constructor_kwargs,
                )
            return instances[registration.service]
        elif scope == Scope.SINGLETON:
            if registration.service not in self._singleton_instances:
                self._singleton_instances[
                    registration.service
                ] = self._inject_dependencies(
                    registration.implementation,
                    constructor_kwargs=registration.constructor_kwargs,
                )
            return self._singleton_instances[registration.service]
        elif scope == Scope.FACTORY:
            return registration.factory(**(registration.factory_kwargs or {}))

        raise ValueError(f"Invalid service scope: {scope}")

    def resolve_all(
        self, tags: Optional[set] = None, match_all_tags: bool = False
    ) -> List[Any]:
        tags = tags or set()
        resolved = []

        for registration in self._registrations.values():
            if not tags:
                # If no tags are provided, resolve all services
                resolved.append(self.resolve(registration.service))
            else:
                if match_all_tags:
                    # Match registrations that have all specified tags
                    if registration.tags and tags.issubset(registration.tags):
                        resolved.append(self.resolve(registration.service))
                else:
                    # Match registrations that have any of the specified tags
                    if registration.tags and tags.intersection(registration.tags):
                        resolved.append(self.resolve(registration.service))

        return resolved

    # -------------------
    # Validation & utils
    # -------------------

    def _validate_constructor_kwargs(
        self, constructor_kwargs: Dict[str, Any], implementation: Type
    ) -> None:
        constructor = inspect.signature(implementation.__init__).parameters

        for arg_name, arg_value in constructor_kwargs.items():
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
                            f"Constructor argument '{arg_name}' has an "
                            f"incompatible type. "
                            f"Expected: {expected_type}, provided: {type(arg_value)}."
                        )
                else:
                    if not isinstance(arg_value, expected_type):
                        raise TypeError(
                            f"Constructor argument '{arg_name}' has an "
                            f"incompatible type. "
                            f"Expected: {expected_type}, provided: {type(arg_value)}."
                        )

    def _validate_registration(self, service: Type) -> None:
        if service in self._registrations:
            raise ValueError(f"Service {service} is already registered.")

    def _inject_dependencies(
        self,
        implementation: Type,
        scope_name: Optional[str] = None,
        constructor_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        scope_name = scope_name or self.get_default_scope_name()

        if is_dataclass(implementation):
            return implementation()  # Do not inject into dataclasses

        dependencies = self._resolve_constructor_args(
            implementation, scope_name, constructor_kwargs
        )
        return implementation(**dependencies)

    def _resolve_constructor_args(
        self,
        implementation: Type,
        scope_name: str,
        constructor_kwargs: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        constructor = inspect.signature(implementation.__init__)
        resolved: Dict[str, Any] = {}

        for name, param in constructor.parameters.items():
            if name == "self":
                continue
            if param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue

            if constructor_kwargs and name in constructor_kwargs:
                resolved[name] = constructor_kwargs[name]
            else:
                try:
                    resolved[name] = self._resolve_param_value(param, scope_name)
                except KeyError:
                    if self._should_use_default(param):
                        continue
                    raise ValueError(
                        f"Cannot resolve service for parameter '{name}' "
                        f"of type '{param.annotation}' in class "
                        f"'{implementation.__name__}'."
                    )

        return resolved

    def _resolve_param_value(self, param: inspect.Parameter, scope_name: str) -> Any:
        annotation = param.annotation

        if get_origin(annotation) is list:
            return self._resolve_param_value_of_list_type(annotation)

        if self._is_optional_type(annotation):
            inner = self._unwrap_optional_type(annotation)

            if get_origin(inner) is list:
                return self._resolve_param_value_of_list_type(inner)

            try:
                return self.resolve(inner, scope_name)
            except KeyError:
                if self._should_use_default(param):
                    raise KeyError  # signal to fallback to default
                return None

        return self.resolve(annotation, scope_name)

    def _resolve_param_value_of_list_type(self, annotation: Any) -> List[Any]:
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
