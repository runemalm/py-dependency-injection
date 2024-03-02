import functools
import inspect

from dependency_injection.container import DEFAULT_CONTAINER_NAME, \
    DependencyContainer
from dependency_injection.scope import DEFAULT_SCOPE_NAME


def inject(container_name=DEFAULT_CONTAINER_NAME, scope_name=DEFAULT_SCOPE_NAME):

    def is_instance_method(func):
        parameters = inspect.signature(func).parameters
        is_instance_method = len(parameters) > 0 and list(parameters.values())[0].name == 'self'
        return is_instance_method

    def decorator_inject(func):

        @functools.wraps(func)
        def wrapper_inject(*args, **kwargs):

            # Get the parameter names from the function signature
            sig = inspect.signature(func)
            parameter_names = [param.name for param in sig.parameters.values()]

            # Iterate over the parameter names and inject dependencies into kwargs
            for parameter_name in parameter_names:
                if parameter_name != 'cls' and parameter_name not in kwargs:
                    # get container
                    container = DependencyContainer.get_instance(container_name)
                    # Resolve the dependency based on the parameter name
                    dependency_type = sig.parameters[parameter_name].annotation
                    kwargs[parameter_name] = container.resolve(dependency_type, scope_name=scope_name)

            # Call the original function with the injected dependencies
            return func(*args, **kwargs)

        # Not allowed on instance methods
        if is_instance_method(func):
            raise TypeError(
                "@inject decorator can only be applied to class methods or static methods.")

        return wrapper_inject

    return decorator_inject
