## py-dependency-injection

This is a simple dependency injection library for python. It provides a simple and flexible way to manage dependencies in your Python applications, promoting modularity, testability, and code maintainability.

### Features:

- Dependency Container
- Constructor Injection
- Support Dependency Scopes

### Python Compatibility

This library is compatible with the following Python versions:

- Python 3.8
  
### Installation:
  
```bash
$ pip install py-dependency-injection
```
  
### Example:

```python
from dependency_injection.container.container import DependencyContainer


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
- Added Dependency Container: The library includes a simple dependency container for managing object dependencies.
- Added Constructor Injection: Users can leverage constructor injection for cleaner and more modular code.
- Added Dependency Scopes: Define and manage the lifecycle of dependencies with support for different scopes.
- Basic Documentation: An initial set of documentation is provided, giving users an introduction to the library.
- License: Released under the GPL 3 license.
