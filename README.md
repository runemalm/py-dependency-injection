[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)

## py-dependency-injection

This is a simple and lightweight dependency injection library for python.

### Features:

- Dependency Container
- Dependency Scopes
- Constructor Injection
- Method Injection

### Python Compatibility

This library is compatible and tested with the following Python versions:

- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

[![Push on master](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml)
  
### Installation:
  
```bash
$ pip install py-dependency-injection
```
  
### Example - Getting a dependency container:

```python
# While you can create multiple containers, it's typically recommended to use one per application.
# For this purpose, you can easily obtain the default container.

from dependency_injection.container import DependencyContainer


dependency_container = DependencyContainer.get_instance()
```

### Example - Registering dependencies:

```python
# You can register using one of three scopes - transient, scoped or singleton.

dependency_container.register_transient(SomeInterface, SomeClass)
dependency_container.register_scoped(AnotherInterface, AnotherClass)
dependency_container.register_singleton(ThirdInterface, ThirdClass)
```

### Example - Resolving dependencies:

```python
# When resolving scoped dependencies, specify the scope explicitly if needed.
# The scope, often associated with an application service action invocation, can be provided for scoped instances.
# Default resolution is applied for non-scoped instances.

transient_instance = dependency_container.resolve(SomeInterface)
scoped_instance = dependency_container.resolve(AnotherInterface, scope_name="some-action-id") # application service action invocation ID
singleton_instance = dependency_container.resolve(ThirdInterface)

```

### Example - Constructor injection:

```python
# As long as the class is resolved using the dependency container, 
# dependencies are injected into it's constructor at resolution time.

class Foo:

    def __init__(self, transient_instance: SomeInterface, scoped_instance: AnotherInterface, singleton_instance: ThirdInterface):
        self._transient_instance = transient_instance
        self._scoped_instance = scoped_instance
        self._singleton_instance = singleton_instance
```

### Example - Method injection:

```python
# Dependencies can be injected into an instance method using the `@inject` decorator.
# The dependency container and scope name can be provided as arguments to the decorator.
# If none are provided, the default container and scope are applied.
from dependency_injection.decorator import inject


class Foo:

    @inject()
    def bar(self, transient_instance: SomeInterface, scoped_instance: AnotherInterface, singleton_instance: ThirdInterface):
        transient_instance.do_something()
        scoped_instance.do_something()
        singleton_instance.do_something()
```

### Documentation:
  
You can find the latest documentation at [readthedocs](https://py-dependency-injection.readthedocs.io/en/latest/).

### Contribution:
  
If you want to contribute to the code base, create a pull request on the develop branch.

We follow the [git flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.
  
### Release Notes

#### [1.0.0-alpha.2](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.2) (2024-02-xx)

- Python Version Support: Added support for Python versions 3.7, 3.9, 3.10, 3.11, and 3.12.
- New Feature: Method Injection with Decorator: Introduced a new feature allowing method injection using the @inject decorator. Dependencies can now be injected into an instance method, providing more flexibility in managing dependencies within class instance methods.
- Documentation Update: Expanded and improved the documentation to include details about the newly added method injection feature and additional usage examples. Users can refer to the latest documentation at readthedocs for comprehensive guidance.

#### [1.0.0-alpha.1](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.1) (2024-02-25)

- Initial alpha release.
- Added Dependency Container: The library includes a dependency container for managing object dependencies.
- Added Constructor Injection: Users can leverage constructor injection for cleaner and more modular code.
- Added Dependency Scopes: Define and manage the lifecycle of dependencies with support for different scopes.
- Basic Documentation: An initial set of documentation is provided, giving users an introduction to the library.
- License: Released under the GPL 3 license.
