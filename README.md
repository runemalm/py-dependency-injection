[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Master workflow](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml)

# py-dependency-injection

A dependency injection library for Python.

## Features

- **Scoped Registrations:** Define the lifetime of your dependencies as transient, scoped, or singleton.
- **Constructor Injection:** Automatically resolve and inject dependencies when creating instances.
- **Method Injection:** Inject dependencies into methods using a simple decorator.
- **Factory Functions:** Register factory functions, classes, or lambdas to create dependencies.
- **Instance Registration:** Register existing instances as dependencies.
- **Tag-Based Registration and Resolution:** Organize and resolve dependencies based on tags.
- **Multiple Containers:** Support for using multiple dependency containers.

## Compatibility

The library is compatible with the following Python versions:

- 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

## Installation

```bash
$ pip install py-dependency-injection
```

## Quick Start

Here's a quick example to get you started:

```python
from dependency_injection.container import DependencyContainer

# Define an abstract Connection
class Connection:
    pass

# Define a specific implementation of the Connection
class PostgresConnection(Connection):
    def connect(self):
        print("Connecting to PostgreSQL database...")

# Define a repository that depends on some type of Connection
class UserRepository:
    def __init__(self, connection: Connection):
        self._connection = connection

    def fetch_users(self):
        self._connection.connect()
        print("Fetching users from the database...")

# Get an instance of the (default) DependencyContainer
container = DependencyContainer.get_instance()

# Register the specific connection type as a singleton instance
container.register_singleton(Connection, PostgresConnection)

# Register UserRepository as a transient (new instance every time)
container.register_transient(UserRepository)

# Resolve an instance of UserRepository, automatically injecting the required Connection
user_repository = container.resolve(UserRepository)

# Use the resolved user_repository to perform an operation
user_repository.find_all()
```

## Documentation

For more advanced usage and examples, please visit our [readthedocs](https://py-dependency-injection.readthedocs.io/en/latest/) page.

## License

`py-dependency-injection` is released under the GPL 3 license. See [LICENSE](LICENSE) for more details.

## Source Code

You can find the source code for `py-dependency-injection` on [GitHub](https://github.com/runemalm/py-dependency-injection).

## Release Notes

### [1.0.0-alpha.9](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.9) (2024-08-08)

- **Breaking Change**: Removed constructor injection when resolving dataclasses.
- **Enhancement**: Added dependency container getter and setter for registrations. Also added new `RegistrationSerializer` class for for serializing and deserializing them. These additions provide a more flexible way to interact with the container's registrations.

### [1.0.0-alpha.8](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.8) (2024-06-07)

- **Bug Fix**: Fixed an issue in the dependency resolution logic where registered constructor arguments were not properly merged with automatically injected dependencies. This ensures that constructor arguments specified during registration are correctly combined with dependencies resolved by the container.
- **Documentation Update**: The documentation structure has been updated for better organization and ease of understanding.

### [1.0.0-alpha.7](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.7) (2024-03-24)

- **Documentation Update**: Updated the documentation to provide clearer instructions and more comprehensive examples.
- **Preparing for Beta Release**: Made necessary adjustments and refinements in preparation for the upcoming first beta release.

### [1.0.0-alpha.6](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.6) (2024-03-23)

- **Factory Registration**: Added support for registering dependencies using factory functions for dynamic instantiation.
- **Instance Registration**: Enabled registering existing instances as dependencies.
- **Tag-based Registration and Resolution**: Introduced the ability to register and resolve dependencies using tags for flexible dependency management.

### [1.0.0-alpha.5](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.5) (2024-03-03)

- **Critical Package Integrity Fix**: This release addresses a critical issue that affected the packaging of the Python library in all previous alpha releases (1.0.0-alpha.1 to 1.0.0-alpha.4). The problem involved missing source files in the distribution, rendering the library incomplete and non-functional. Users are strongly advised to upgrade to version 1.0.0-alpha.5 to ensure the correct functioning of the library. All previous alpha releases are affected by this issue.

### [1.0.0-alpha.4](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.4) (2024-03-02)

- **Constructor Arguments**: Support for constructor arguments added to dependency registration.

### [1.0.0-alpha.3](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.3) (2024-03-02)

- **Breaking Change**: Starting from this version, the `@inject` decorator can only be used on static class methods and class methods. It can't be used on instance methods anymore.
- **Documentation Update**: The documentation has been updated to reflect the new restriction on the usage of the decorator.

### [1.0.0-alpha.2](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.2) (2024-02-27)

- **Python Version Support**: Added support for Python versions 3.7, 3.9, 3.10, 3.11, and 3.12.
- **New Feature**: Method Injection with Decorator: Introduced a new feature allowing method injection using the @inject decorator. Dependencies can now be injected into an instance method, providing more flexibility in managing dependencies within class instance methods.
- **New Feature**: Multiple Containers: Enhanced the library to support multiple containers. Users can now create and manage multiple dependency containers, enabling better organization and separation of dependencies for different components or modules.
- **Documentation Update**: Expanded and improved the documentation to include details about the newly added method injection feature and additional usage examples. Users can refer to the latest documentation at readthedocs for comprehensive guidance.

### [1.0.0-alpha.1](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.1) (2024-02-25)

- **Initial alpha release**.
- **Added Dependency Container**: The library includes a dependency container for managing object dependencies.
- **Added Constructor Injection**: Users can leverage constructor injection for cleaner and more modular code.
- **Added Dependency Scopes**: Define and manage the lifecycle of dependencies with support for different scopes.
- **Basic Documentation**: An initial set of documentation is provided, giving users an introduction to the library.
- **License**: Released under the GPL 3 license.
