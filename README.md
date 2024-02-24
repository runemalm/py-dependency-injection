## py-dependency-injection

A simple dependency injection implementation for python.

### Features:

- Dependency Container
- Constructor Injection
- Scopes
    - Transient
    - Scoped
    - Singleton

### Design Pattern Resources: 
  
You can read about the dependency injection pattern here:
  
- [Wikipedia](https://en.wikipedia.org/wiki/Dependency_injection)

### Supported Python Versions:

- Tested with python 3.8.5.
- Should work with any version >= 3.8.0.
  
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
scoped_instance = container.resolve(AnotherInterface, scope_name="some_scope")
singleton_instance = container.resolve(ThirdInterface)

# Use dependencies
transient_instance.do_something()
scoped_instance.do_something()
singleton_instance.do_something()

```

### ..constructor injection:

```python
class SomeClass(SomeInterface):

    def __init__(self, scoped_instance: AnotherInterface)
        self.scoped_instance = scoped_instance

transient_instance = container.resolve(SomeInterface)

```

### ..method injection:

```python
from dependency_injection.decorator.inject import inject

class SomeService:
    
    @inject()
    def do_something_1(self, transient_instance: SomeInterface):
        transient_instance.do_something()

    @inject(scope_name="some-scope")
    def do_something_2(self, scoped_instance: AnotherInterface):
        scoped_instance.do_something()

    @inject(container=DependencyContainer.get_instance())
    def do_something_3(self, singleton_instance: ThirdInterface):
        singleton_instance.do_something()

```

### Documentation:
  
You can find the latest [documentation](https://py-dependency-injection.readthedocs.io/en/latest/) at readthedocs.

### Contribution:
  
If you want to contribute to the code base, create a pull request on the develop branch.

We follow the git flow model, documentation can be found here:
- [Vincent Driessen at nvie (official)](https://nvie.com/posts/a-successful-git-branching-model/)
- [Atlassian (atlernative)](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
  
### Release Notes:

**1.0.0-alpha.1** - 2024-03-03
- Initial release.
