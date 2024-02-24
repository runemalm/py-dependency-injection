import inspect

from dependency_injection.container.registration import Registration
from dependency_injection.container.scope import Scope
from dependency_injection.utils.singleton_meta import SingletonMeta


class DependencyContainer(metaclass=SingletonMeta):

    def __init__(self):
        self._registrations = {}
        self._singleton_instances = {}
        self._scoped_instances = {}

    @classmethod
    def get_instance(cls):
        return cls()

    def register_transient(self, interface, class_):
        if interface in self._registrations:
            raise ValueError(f"Dependency {interface} is already registered.")
        self._registrations[interface] = Registration(interface, class_, Scope.TRANSIENT)

    def register_scoped(self, interface, class_):
        if interface in self._registrations:
            raise ValueError(f"Dependency {interface} is already registered.")
        self._registrations[interface] = Registration(interface, class_, Scope.SCOPED)

    def register_singleton(self, interface, class_):
        if interface in self._registrations:
            raise ValueError(f"Dependency {interface} is already registered.")
        self._registrations[interface] = Registration(interface, class_, Scope.SINGLETON)

    def resolve(self, interface, scope_name=None):
        if scope_name not in self._scoped_instances:
            self._scoped_instances[scope_name] = {}

        if interface not in self._registrations:
            raise KeyError(f"Dependency {interface.__name__} is not registered.")

        registration = self._registrations[interface]
        dependency_scope = registration.scope
        dependency_class = registration.class_

        if dependency_scope == Scope.TRANSIENT:
            return self._inject_dependencies(dependency_class)
        elif dependency_scope == Scope.SCOPED:
            if interface not in self._scoped_instances[scope_name]:
                self._scoped_instances[scope_name][interface] = (
                    self._inject_dependencies(
                        class_=dependency_class,
                        scope_name=scope_name,))
            return self._scoped_instances[scope_name][interface]
        elif dependency_scope == Scope.SINGLETON:
            if interface not in self._singleton_instances:
                self._singleton_instances[interface] = self._inject_dependencies(dependency_class)
            return self._singleton_instances[interface]

        raise ValueError(f"Invalid dependency scope: {dependency_scope}")

    def _inject_dependencies(self, class_, scope_name=None):
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
                    dependencies[param_name] = self.resolve(param_info.annotation, scope_name=scope_name)

        return class_(**dependencies)
