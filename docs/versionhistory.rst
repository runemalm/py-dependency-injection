###############
Version history
###############

**1.0.0-alpha.2 (2024-02-27)**

- Python Version Support: Added support for Python versions 3.7, 3.9, 3.10, 3.11, and 3.12.
- New Feature: Method Injection with Decorator: Introduced a new feature allowing method injection using the @inject decorator. Dependencies can now be injected into an instance method, providing more flexibility in managing dependencies within class instance methods.
- New Feature: Multiple Containers: Enhanced the library to support multiple containers. Users can now create and manage multiple dependency containers, enabling better organization and separation of dependencies for different components or modules.
- Documentation Update: Expanded and improved the documentation to include details about the newly added method injection feature and additional usage examples. Users can refer to the latest documentation at readthedocs for comprehensive guidance.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.2>`_

**1.0.0-alpha.1 (2024-02-25)**

- Initial alpha release.
- Added Dependency Container: The library includes a simple dependency container for managing object dependencies.
- Added Constructor Injection: Users can leverage constructor injection for cleaner and more modular code.
- Added Dependency Scopes: Define and manage the lifecycle of dependencies with support for different scopes.
- Basic Documentation: An initial set of documentation is provided, giving users an introduction to the library.
- License: Released under the GPL 3 license.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.1>`_
