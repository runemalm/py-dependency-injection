###############
Version history
###############

**1.0.0-alpha.6 (2024-03-23)**

- **Factory Registration:** Added support for registering dependencies using factory functions for dynamic instantiation.

- **Instance Registration:** Enabled registering existing instances as dependencies.

- **Tag-based Registration and Resolution:** Introduced the ability to register and resolve dependencies using tags for flexible dependency management.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.6>`_

**1.0.0-alpha.5 (2024-03-03)**

- **Critical Package Integrity Fix**: This release addresses a critical issue that affected the packaging of the Python library in all previous alpha releases (1.0.0-alpha.1 to 1.0.0-alpha.4). The problem involved missing source files in the distribution, rendering the library incomplete and non-functional.

**Action Required:** Users are strongly advised to upgrade to version 1.0.0-alpha.5 to ensure the correct functioning of the library. All previous alpha releases are affected by this issue.

**Note:** No functional changes or new features have been introduced in this release, and its primary purpose is to rectify the consistent packaging problem.

For installation and upgrade instructions, please refer to the Installation section in the README.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.5>`_

**1.0.0-alpha.4 (2024-03-02)**

- **New Feature**: Support for constructor arguments in dependency registration: In this release, we introduce the ability to specify constructor arguments when registering dependencies with the container. This feature provides more flexibility when configuring dependencies, allowing users to customize the instantiation of classes during registration.

    **Usage Example:**::
    
        # Registering a dependency with constructor arguments
        dependency_container.register_transient(
            SomeInterface, SomeClass,
            constructor_args={"arg1": value1, "arg2": value2}
        )

    Users can now pass specific arguments to be used during the instantiation of the dependency. This is particularly useful when a class requires dynamic or configuration-dependent parameters.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.4>`_

**1.0.0-alpha.3 (2024-03-02)**

- **Breaking Change**: Restriction on `@inject` Decorator: Starting from this version, the `@inject` decorator can now only be used on static class methods and class methods. This change is introduced due to potential pitfalls associated with resolving and injecting dependencies directly into class instance methods using the dependency container.

    **Reasoning:**
  
    Resolving and injecting dependencies into instance methods can lead to unexpected behaviors and may violate the principles of dependency injection. Instance methods often rely on the state of the object, and injecting dependencies from the container directly can obscure the dependencies required for a method. Additionally, it may introduce difficulties in testing and make the code harder to reason about.

    By restricting the usage of the `@inject` decorator to static and class methods, we aim to encourage a cleaner separation of concerns, making it more explicit when dependencies are injected and providing better clarity on the dependencies required by a method.

    **Before:**::

        class Foo:
        
            @inject()
            def instance_method(self, transient_instance: SomeInterface, scoped_instance: AnotherInterface, singleton_instance: ThirdInterface):
                # ...

    **After:**::

        class Foo:
        
            @classmethod
            @inject()
            def class_method(cls, transient_instance: SomeInterface, scoped_instance: AnotherInterface, singleton_instance: ThirdInterface):
                # ...

            @staticmethod
            @inject()
            def static_method(transient_instance: SomeInterface, scoped_instance: AnotherInterface, singleton_instance: ThirdInterface):
                # ...

- Documentation Update: The documentation has been updated to reflect the new restriction on the usage of the `@inject` decorator. Users are advised to review the documentation for updated examples and guidelines regarding method injection.

`View release on GitHub <https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.3>`_

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
