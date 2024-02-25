[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Push on master](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml)

## py-dependency-injection

This is a dependency injection library for python. It provides a simple and flexible way to manage dependencies in your Python applications, promoting modularity, testability, and code maintainability.

### Features:

- Dependency Container
- Constructor Injection
- Support Dependency Scopes

### Python Compatibility

This library is compatible with the following Python versions:

- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
  
### Installation:
  
```bash
$ pip install py-dependency-injection
```
  
### Example:

```python
from dependency_injection.container import DependencyContainer


container = DependencyContainer.get_instance()

# Register dependencies
container.register_transient(SomeInterface, SomeClass)
container.register_scoped(AnotherInterface, AnotherClass)
container.register_singleton(ThirdInterface, ThirdClass)

# Resolve dependencies
transient_instance = container.resolve(SomeInterface)
scoped_instance = container.resolve(AnotherInterface, scope_name="http_request_scope_123")
singleton_instance = container.resolve(ThirdInterface)

# Use dependencies
transient_instance.do_something()
scoped_instance.do_something()
singleton_instance.do_something()

```

### Documentation:
  
You can find the latest [documentation](https://py-dependency-injection.readthedocs.io/en/latest/) at readthedocs.

### Contribution:
  
If you want to contribute to the code base, create a pull request on the develop branch.

We follow the git flow model, documentation can be found here:
- [Official documentation](https://nvie.com/posts/a-successful-git-branching-model/)
- [Atlassian guide](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
  
### Release Notes

#### [1.0.0-alpha.1](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.1) (2024-02-25)

- Initial alpha release.
- Added Dependency Container: The library includes a dependency container for managing object dependencies.
- Added Constructor Injection: Users can leverage constructor injection for cleaner and more modular code.
- Added Dependency Scopes: Define and manage the lifecycle of dependencies with support for different scopes.
- Basic Documentation: An initial set of documentation is provided, giving users an introduction to the library.
- License: Released under the GPL 3 license.

#### [1.0.0-alpha.2](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.2) (2024-03-xx)

- Python Version Support: Added support for Python versions 3.7, 3.9, 3.10, 3.11, and 3.12.
