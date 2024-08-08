.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

###############
Version History
###############

**1.0.0-alpha.8 (2024-06-07)**

- **Bug Fix**: Fixed an issue in the dependency resolution logic where registered constructor arguments were not properly merged with automatically injected dependencies. This ensures that constructor arguments specified during registration are correctly combined with dependencies resolved by the container.
- **Documentation Update**: The documentation structure has been updated for better organization and ease of understanding.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.8>`_

**1.0.0-alpha.7 (2024-03-24)**

- **Documentation Update**: Updated the documentation to provide clearer instructions and more comprehensive examples.
- **Preparing for Beta Release**: Made necessary adjustments and refinements in preparation for the upcoming first beta release.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.7>`_

**1.0.0-alpha.6 (2024-03-23)**

- **Factory Registration**: Added support for registering dependencies using factory functions for dynamic instantiation.
- **Instance Registration**: Enabled registering existing instances as dependencies.
- **Tag-based Registration and Resolution**: Introduced the ability to register and resolve dependencies using tags for flexible dependency management.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.6>`_

**1.0.0-alpha.5 (2024-03-03)**

- **Critical Package Integrity Fix**: This release addresses a critical issue that affected the packaging of the Python library in all previous alpha releases (1.0.0-alpha.1 to 1.0.0-alpha.4). The problem involved missing source files in the distribution, rendering the library incomplete and non-functional. Users are strongly advised to upgrade to version 1.0.0-alpha.5 to ensure the correct functioning of the library. All previous alpha releases are affected by this issue.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.5>`_

**1.0.0-alpha.4 (2024-03-02)**

- **Constructor Arguments**: Support for constructor arguments added to dependency registration.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.4>`_

**1.0.0-alpha.3 (2024-03-02)**

- **Breaking Change**: Starting from this version, the `@inject` decorator can only be used on static class methods and class methods. It can't be used on instance methods anymore.
- **Documentation Update**: The documentation has been updated to reflect the new restriction on the usage of the decorator.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.3>`_

**1.0.0-alpha.2 (2024-02-27)**

- **Python Version Support**: Added support for Python versions 3.7, 3.9, 3.10, 3.11, and 3.12.
- **New Feature**: Method Injection with Decorator: Introduced a new feature allowing method injection using the @inject decorator. Dependencies can now be injected into an instance method, providing more flexibility in managing dependencies within class instance methods.
- **New Feature**: Multiple Containers: Enhanced the library to support multiple containers. Users can now create and manage multiple dependency containers, enabling better organization and separation of dependencies for different components or modules.
- **Documentation Update**: Expanded and improved the documentation to include details about the newly added method injection feature and additional usage examples. Users can refer to the latest documentation at readthedocs for comprehensive guidance.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.2>`_

**1.0.0-alpha.1 (2024-02-25)**

- **Initial alpha release**.
- **Added Dependency Container**: The library includes a dependency container for managing object dependencies.
- **Added Constructor Injection**: Users can leverage constructor injection for cleaner and more modular code.
- **Added Dependency Scopes**: Define and manage the lifecycle of dependencies with support for different scopes.
- **Basic Documentation**: An initial set of documentation is provided, giving users an introduction to the library.
- **License**: Released under the GPL 3 license.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.1>`_
