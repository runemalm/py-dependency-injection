import inspect

from typing import Any, Dict, Optional, TypeVar, Type

from dependency_injection.registration import Registration
from dependency_injection.scope import DEFAULT_SCOPE_NAME, Scope
from dependency_injection.utils.singleton_meta import SingletonMeta

Self = TypeVar('Self', bound='DependencyContainer')


DEFAULT_CONTAINER_NAME = "default_container"

class DependencyContainer(metaclass=SingletonMeta):

    def __init__(self, name: str=None):
        self.name = name if name is not None else DEFAULT_CONTAINER_NAME
        self._registrations = {}
        self._singleton_instances = {}
        self._scoped_instances = {}

    @classmethod
    def get_instance(cls, name: str=None) -> Self:
        if name is None:
            name = DEFAULT_CONTAINER_NAME

        if (cls, name) not in cls._instances:
            cls._instances[(cls, name)] = cls(name)

        return cls._instances[(cls, name)]

    def register_transient(self, dependency: Type, implementation: Optional[Type] = None, constructor_args: Optional[Dict[str, Any]] = None) -> None:
        if implementation is None:
            implementation = dependency
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")
        self._registrations[dependency] = Registration(dependency, implementation, Scope.TRANSIENT, constructor_args)

    def register_scoped(self, dependency: Type, implementation: Optional[Type] = None, constructor_args: Optional[Dict[str, Any]] = None) -> None:
        if implementation is None:
            implementation = dependency
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")
        self._registrations[dependency] = Registration(dependency, implementation, Scope.SCOPED, constructor_args)

    def register_singleton(self, dependency: Type, implementation: Optional[Type] = None, constructor_args: Optional[Dict[str, Any]] = None) -> None:
        if implementation is None:
            implementation = dependency
        if dependency in self._registrations:
            raise ValueError(f"Dependency {dependency} is already registered.")
        self._registrations[dependency] = Registration(dependency, implementation, Scope.SINGLETON, constructor_args)

    def resolve(self, dependency: Type, scope_name: str = DEFAULT_SCOPE_NAME) -> Type:
        if scope_name not in self._scoped_instances:
            self._scoped_instances[scope_name] = {}

        if dependency not in self._registrations:
            raise KeyError(f"Dependency {dependency.__name__} is not registered.")

        registration = self._registrations[dependency]
        scope = registration.scope
        implementation = registration.implementation
        constructor_args = registration.constructor_args

        self._validate_constructor_args(constructor_args=constructor_args, implementation=implementation)

        if scope == Scope.TRANSIENT:
            return self._inject_dependencies(
                implementation=implementation,
                constructor_args=constructor_args
            )
        elif scope == Scope.SCOPED:
            if dependency not in self._scoped_instances[scope_name]:
                self._scoped_instances[scope_name][dependency] = (
                    self._inject_dependencies(
                        implementation=implementation,
                        scope_name=scope_name,
                        constructor_args=constructor_args,
                    ))
            return self._scoped_instances[scope_name][dependency]
        elif scope == Scope.SINGLETON:
            if dependency not in self._singleton_instances:
                self._singleton_instances[dependency] = (
                    self._inject_dependencies(
                        implementation=implementation,
                        constructor_args=constructor_args
                    )
                )
            return self._singleton_instances[dependency]

        raise ValueError(f"Invalid dependency scope: {scope}")

    def _validate_constructor_args(self, constructor_args: Dict[str, Any], implementation: Type) -> None:
        constructor = inspect.signature(implementation.__init__).parameters

        # Check if any required parameter is missing
        missing_params = [param for param in constructor.keys() if
                          param not in ["self", "cls", "args", "kwargs"] and
                          param not in constructor_args]
        if missing_params:
            raise ValueError(
                f"Missing required constructor arguments: "
                f"{', '.join(missing_params)} for class '{implementation.__name__}'.")

        for arg_name, arg_value in constructor_args.items():
            if arg_name not in constructor:
                raise ValueError(
                    f"Invalid constructor argument '{arg_name}' for class '{implementation.__name__}'. "
                    f"The class does not have a constructor parameter with this name.")

            expected_type = constructor[arg_name].annotation
            if expected_type != inspect.Parameter.empty:
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Constructor argument '{arg_name}' has an incompatible type. "
                        f"Expected type: {expected_type}, provided type: {type(arg_value)}.")

    def _inject_dependencies(self, implementation: Type, scope_name: str = None, constructor_args: Optional[Dict[str, Any]] = None) -> Type:
        constructor = inspect.signature(implementation.__init__)
        params = constructor.parameters

        dependencies = {}
        for param_name, param_info in params.items():
            if param_name != 'self':
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
                        dependencies[param_name] = self.resolve(param_info.annotation, scope_name=scope_name)

        return implementation(**dependencies)
