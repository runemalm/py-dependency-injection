import inspect
from typing import Any, Dict, Type

from dependency_injection.registration import Registration
from dependency_injection.scope import DEFAULT_SCOPE_NAME, Scope
from dependency_injection.utils.singleton_meta import SingletonMeta


DEFAULT_CONTAINER_NAME = "default_container"

class DependencyContainer(metaclass=SingletonMeta):

    def __init__(self, name=None):
        self.name = name if name is not None else DEFAULT_CONTAINER_NAME
        self._registrations = {}
        self._singleton_instances = {}
        self._scoped_instances = {}

    @classmethod
    def get_instance(cls, name=None):
        if name is None:
            name = DEFAULT_CONTAINER_NAME

        if (cls, name) not in cls._instances:
            cls._instances[(cls, name)] = cls(name)

        return cls._instances[(cls, name)]

    def register_transient(self, interface, class_, constructor_args=None):
        if interface in self._registrations:
            raise ValueError(f"Dependency {interface} is already registered.")
        self._registrations[interface] = Registration(interface, class_, Scope.TRANSIENT, constructor_args)

    def register_scoped(self, interface, class_, constructor_args=None):
        if interface in self._registrations:
            raise ValueError(f"Dependency {interface} is already registered.")
        self._registrations[interface] = Registration(interface, class_, Scope.SCOPED, constructor_args)

    def register_singleton(self, interface, class_, constructor_args=None):
        if interface in self._registrations:
            raise ValueError(f"Dependency {interface} is already registered.")
        self._registrations[interface] = Registration(interface, class_, Scope.SINGLETON, constructor_args)

    def resolve(self, interface, scope_name=DEFAULT_SCOPE_NAME):
        if scope_name not in self._scoped_instances:
            self._scoped_instances[scope_name] = {}

        if interface not in self._registrations:
            raise KeyError(f"Dependency {interface.__name__} is not registered.")

        registration = self._registrations[interface]
        dependency_scope = registration.scope
        dependency_class = registration.class_
        constructor_args = registration.constructor_args

        self._validate_constructor_args(constructor_args=constructor_args, class_=dependency_class)

        if dependency_scope == Scope.TRANSIENT:
            return self._inject_dependencies(
                class_=dependency_class,
                constructor_args=constructor_args
            )
        elif dependency_scope == Scope.SCOPED:
            if interface not in self._scoped_instances[scope_name]:
                self._scoped_instances[scope_name][interface] = (
                    self._inject_dependencies(
                        class_=dependency_class,
                        scope_name=scope_name,
                        constructor_args=constructor_args,
                    ))
            return self._scoped_instances[scope_name][interface]
        elif dependency_scope == Scope.SINGLETON:
            if interface not in self._singleton_instances:
                self._singleton_instances[interface] = (
                    self._inject_dependencies(
                        class_=dependency_class,
                        constructor_args=constructor_args
                    )
                )
            return self._singleton_instances[interface]

        raise ValueError(f"Invalid dependency scope: {dependency_scope}")

    def _validate_constructor_args(self, constructor_args: Dict[str, Any], class_: Type) -> None:
        class_constructor = inspect.signature(class_.__init__).parameters

        # Check if any required parameter is missing
        missing_params = [param for param in class_constructor.keys() if
                          param not in ["self", "cls", "args", "kwargs"] and
                          param not in constructor_args]
        if missing_params:
            raise ValueError(
                f"Missing required constructor arguments: "
                f"{', '.join(missing_params)} for class '{class_.__name__}'.")

        for arg_name, arg_value in constructor_args.items():
            if arg_name not in class_constructor:
                raise ValueError(
                    f"Invalid constructor argument '{arg_name}' for class '{class_.__name__}'. "
                    f"The class does not have a constructor parameter with this name.")

            expected_type = class_constructor[arg_name].annotation
            if expected_type != inspect.Parameter.empty:
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Constructor argument '{arg_name}' has an incompatible type. "
                        f"Expected type: {expected_type}, provided type: {type(arg_value)}.")

    def _inject_dependencies(self, class_, scope_name=None, constructor_args=None):
        constructor = inspect.signature(class_.__init__)
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

        return class_(**dependencies)
