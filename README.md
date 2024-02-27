[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Push on master](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml)

# py-dependency-injection

A dependency injection library for Python.

## Features:

- Dependency Container
- Dependency Scopes
- Constructor Injection
- Method Injection

## Python Compatibility

This library is compatible with the following Python versions:

- 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
  
## Installation:
  
```bash
$ pip install py-dependency-injection
```

## Usage:

The following examples demonstrates how to use the library.

#### Example: Obtaining the Default Dependency Container

```python
# Retrieve the default container, typically recommended for a single-application setup.

from dependency_injection.container import DependencyContainer


dependency_container = DependencyContainer.get_instance()
```

#### Example: Obtaining a Second Dependency Container

```python
# Create additional containers if needed, especially for multi-application scenarios.

from dependency_injection.container import DependencyContainer


a_second_dependency_container = DependencyContainer.get_instance(name="a_second_dependency_container")
```

#### Example: Registering Dependencies

```python
# Register dependencies with three available scopes: transient, scoped, or singleton.

dependency_container.register_transient(SomeInterface, SomeClass)
dependency_container.register_scoped(AnotherInterface, AnotherClass)
dependency_container.register_singleton(ThirdInterface, ThirdClass)
```

#### Example: Resolving Dependencies

```python
# Resolve transient instance (created anew for each call).
transient_instance = dependency_container.resolve(SomeInterface)

# Resolve scoped instance (consistent within a specific scope, e.g. a scope for the application action being run).
scoped_instance = dependency_container.resolve(AnotherInterface, scope_name="application_action_scope")

# Resolve singleton instance (consistent across the entire application).
singleton_instance = dependency_container.resolve(ThirdInterface)
```

#### Example: Constructor Injection

```python
# Class instances resolved through the container have dependencies injected into their constructors.

class Foo:

    def __init__(self, transient_instance: SomeInterface, scoped_instance: AnotherInterface, singleton_instance: ThirdInterface):
        self._transient_instance = transient_instance
        self._scoped_instance = scoped_instance
        self._singleton_instance = singleton_instance
```

#### Example: Method Injection

```python
# Inject dependencies into instance methods using the `@inject` decorator.
# You may pass 'container_name' and 'scope_name' as decorator arguments.

from dependency_injection.decorator import inject


class Foo:

    @inject()
    def bar(self, transient_instance: SomeInterface, scoped_instance: AnotherInterface, singleton_instance: ThirdInterface):
        transient_instance.do_something()
        scoped_instance.do_something()
        singleton_instance.do_something()
```

## Documentation:
  
For the latest documentation, visit [readthedocs](https://py-dependency-injection.readthedocs.io/en/latest/).

## Contribution:

To contribute, create a pull request on the develop branch following the [git flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.
  
## Release Notes

### [1.0.0-alpha.2](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.2) (2024-02-27)

- Python Version Support: Added support for Python versions 3.7, 3.9, 3.10, 3.11, and 3.12.
- New Feature: Method Injection with Decorator: Introduced a new feature allowing method injection using the @inject decorator. Dependencies can now be injected into an instance method, providing more flexibility in managing dependencies within class instance methods.
- New Feature: Multiple Containers: Enhanced the library to support multiple containers. Users can now create and manage multiple dependency containers, enabling better organization and separation of dependencies for different components or modules.
- Documentation Update: Expanded and improved the documentation to include details about the newly added method injection feature and additional usage examples. Users can refer to the latest documentation at readthedocs for comprehensive guidance.

### [1.0.0-alpha.1](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.1) (2024-02-25)

- Initial alpha release.
- Added Dependency Container: The library includes a dependency container for managing object dependencies.
- Added Constructor Injection: Users can leverage constructor injection for cleaner and more modular code.
- Added Dependency Scopes: Define and manage the lifecycle of dependencies with support for different scopes.
- Basic Documentation: An initial set of documentation is provided, giving users an introduction to the library.
- License: Released under the GPL 3 license.
