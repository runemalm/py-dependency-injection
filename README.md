[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Master workflow](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml)

# py-dependency-injection

A dependency injection library for Python.

## Features

- **Dependency Container:** Manage and resolve object dependencies with a flexible and easy-to-use container.
- **Dependency Scopes:** Define different scopes for dependencies, allowing for fine-grained control over their lifecycle.
- **Constructor Injection:** Inject dependencies into constructors, promoting cleaner and more modular code.
- **Method Injection:** Inject dependencies into methods, enabling more flexible dependency management within class instances.
- **Tags:** Register and resolve dependencies using tags, facilitating flexible and dynamic dependency management.
- **Factory Registration:** Register dependencies using factory functions for dynamic instantiation.
- **Instance Registration:** Register existing instances as dependencies, providing more control over object creation.
- **Python Compatibility:** Compatible with Python versions 3.7 to 3.12, ensuring broad compatibility with existing and future Python projects.

## Compatibility

This library is compatible with the following Python versions:

- 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

## Installation

```bash
$ pip install py-dependency-injection
```

## Basic Usage

The following examples demonstrates how to use the library.

### Creating a Dependency Container

```python
# Get the default dependency container
dependency_container = DependencyContainer.get_instance()

# Create additional named containers if needed
another_container = DependencyContainer.get_instance(name="another_container")
```

### Registering Dependencies with Scopes

```python
# Register a transient dependency (a new instance every time)
dependency_container.register_transient(Connection, PostgresConnection)

# Register a scoped dependency (a new instance per scope)
dependency_container.register_scoped(Connection, PostgresConnection, scope_name="http_request")

# Register a singleton dependency (a single instance for the container's lifetime)
dependency_container.register_singleton(Connection, PostgresConnection)
```

### Using Constructor Arguments

```python
# Register a dependency with constructor arguments
dependency_container.register_transient(
    Connection,
    PostgresConnection,
    constructor_args={"host": "localhost", "port": 5432}
)
```

### Using Factory Functions

```python
# Define a factory function
def create_connection(host: str, port: int) -> Connection:
    return PostgresConnection(host=host, port=port)

# Register the factory function
dependency_container.register_factory(Connection, create_connection, factory_args={"host": "localhost", "port": 5432})
```

Besides functions, you can also use lambdas and class functions. Read more in the [documentation](https://py-dependency-injection.readthedocs.io/en/latest/).

### Registering and Using Instances

```python
# Create an instance
my_connection = PostgresConnection(host="localhost", port=5432)

# Register the instance
dependency_container.register_instance(Connection, my_connection)

# Resolve the instance
resolved_connection = dependency_container.resolve(Connection)
print(resolved_connection.host)  # Output: localhost
```

### Registering and Resolving with Tags

```python
# Register dependencies with tags
dependency_container.register_transient(Connection, PostgresConnection, tags={"Querying", "Startable"})
dependency_container.register_scoped(BusConnection, KafkaBusConnection, tags={"Publishing", "Startable"})

# Resolve dependencies by tags
startable_dependencies = dependency_container.resolve_all(tags={"Startable"})
for dependency in startable_dependencies:
    dependency.start()
```

### Using Constructor Injection

```python
class OrderRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

# Register dependencies
dependency_container.register_transient(OrderRepository)
dependency_container.register_singleton(Connection, PostgresConnection)

# Resolve the OrderRepository with injected dependencies
repository = dependency_container.resolve(OrderRepository)
print(repository.connection.__class__.__name__)  # Output: PostgresConnection
```

### Using Method Injection

```python
class OrderController:
    @staticmethod
    @inject()
    def place_order(order: Order, repository: OrderRepository):
        order.status = "placed"
        repository.save(order)

# Register the dependency
dependency_container.register_transient(OrderRepository)
dependency_container.register_singleton(Connection, PostgresConnection)

# Use method injection to inject the dependency
my_order = Order.create()
OrderController.place_order(order=my_order)  # The repository instance will be automatically injected
```

You can also specify container- and scope names in the decorator arguments. Read more in the [documentation](https://py-dependency-injection.readthedocs.io/en/latest/).

## Documentation

For the latest documentation, visit [readthedocs](https://py-dependency-injection.readthedocs.io/en/latest/).

## Contribution

To contribute, create a pull request on the develop branch following the [git flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.

## Release Notes

### [1.0.0-alpha.6](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.6) (2024-03-23)

- Factory Registration: Added support for registering dependencies using factory functions for dynamic instantiation.
- Instance Registration: Enabled registering existing instances as dependencies.
- Tag-based Registration and Resolution: Introduced the ability to register and resolve dependencies using tags for flexible dependency management.

### [1.0.0-alpha.5](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.5) (2024-03-03)

- **Critical Package Integrity Fix**: This release addresses a critical issue that affected the packaging of the Python library in all previous alpha releases (1.0.0-alpha.1 to 1.0.0-alpha.4). The problem involved missing source files in the distribution, rendering the library incomplete and non-functional. Users are strongly advised to upgrade to version 1.0.0-alpha.5 to ensure the correct functioning of the library. All previous alpha releases are affected by this issue.

### [1.0.0-alpha.4](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.4) (2024-03-02)

- Constructor Arguments: Support for constructor arguments added to dependency registration.

### [1.0.0-alpha.3](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.3) (2024-03-02)

- **Breaking Change**: Starting from this version, the `@inject` decorator can only be used on static class methods and class methods. It can't be used on instance methods anymore.
- Documentation Update: The documentation has been updated to reflect the new restriction on the usage of the decorator.

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
