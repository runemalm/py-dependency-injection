.. note::

    This library is currently in the release candidate stage.
    The public API is considered stable and is undergoing final validation before the 1.0.0 release.

###############
Version History
###############

**1.0.0-rc.2 (2025-08-07)**

- **License Change**: Switched from GPL-3.0 to MIT to support broader adoption and commercial use.
- **Toolchange**: Migrated from `pipenv` to `Poetry`.
- **Dropped Python 3.7 & 3.8 support** – Both versions are EOL and increasingly unsupported by modern tooling.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-rc.2>`_

**1.0.0-rc.1 (2025-06-22)**

- **Transition to Release Candidate**: This marks the first release candidate. The public API is now considered stable and ready for final validation before 1.0.0.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-rc.1>`_

**1.0.0-beta.3 (2025-06-14)**

- **Enhancement**: Added `DependencyContainer.configure_default_container_name(...)` to support container isolation in parallel tests, even when application code uses a single shared container via `DependencyContainer.get_instance()`.
- **Enhancement**: Added `DependencyContainer.clear_instances()` as a clean alternative to manually resetting `_instances` during test teardown.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-beta.3>`_

**1.0.0-beta.2 (2025-06-09)**

- **Enhancement**: Constructor parameters with default values or `Optional[...]` are now supported without requiring explicit registration.
- **Python Version Support**: Added support for Python version 3.13.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-beta.2>`_

**1.0.0-beta.1 (2025-01-06)**

- **Transition to Beta**: Transitioned from alpha to beta. Features have been stabilized and are ready for broader testing.
- **Removal**: We have removed the dependency container getter and setter functions, as well as the RegistrationSerializer class, which were first introduced in v1.0.0-alpha.9. This decision reflects our focus on maintaining a streamlined library that emphasizes core functionality. These features, which would not be widely used, added unnecessary complexity without offering significant value. By removing them, we are reinforcing our commitment to our design principles.
- **Enhancement**: Added suppprt for configuring default scope name. Either a static string value, or a callable that returns the name.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-beta.1>`_

**1.0.0-alpha.10 (2024-08-11)**

- **Tagged Constructor Injection**: Introduced support for constructor injection using the `Tagged`, `AnyTagged`, and `AllTagged` classes. This allows for seamless injection of dependencies that have been registered with specific tags, enhancing flexibility and control in managing your application's dependencies.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.10>`_

**1.0.0-alpha.9 (2024-08-08)**

- **Breaking Change**: Removed constructor injection when resolving dataclasses.
- **Enhancement**: Added dependency container getter and setter for registrations. Also added new `RegistrationSerializer` class for for serializing and deserializing them. These additions provide a more flexible way to interact with the container's registrations.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.9>`_

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
