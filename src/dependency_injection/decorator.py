import functools
import inspect

from dependency_injection.container import DependencyContainer
from dependency_injection.scope import DEFAULT_SCOPE_NAME


def inject(container=DependencyContainer.get_instance(), scope_name=DEFAULT_SCOPE_NAME):

    def decorator_inject(func):
        @functools.wraps(func)
        def wrapper_inject(self, *args, **kwargs):
            # Get the parameter names from the function signature
            param_names = list(inspect.signature(func).parameters.keys())

            # Iterate over the parameter names and inject dependencies into kwargs
            for param_name in param_names:
                if param_name != 'self' and param_name not in kwargs:
                    # Resolve the dependency based on the parameter name
                    dependency_type = inspect.signature(func).parameters[param_name].annotation
                    kwargs[param_name] = container.resolve(dependency_type, scope_name=scope_name)

            # Call the original function with the injected dependencies
            return func(self, *args, **kwargs)

        return wrapper_inject

    return decorator_inject
