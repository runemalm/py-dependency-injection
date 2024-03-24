##############
Basic Concepts
##############


Dependency Injection
--------------------

Dependency Injection (DI) is a design pattern that enables the inversion of control in software applications by allowing the injection of dependencies from external sources. In the context of `py-dependency-injection`, it simplifies the management of object dependencies and promotes modular and testable code.


Dependency Container
--------------------

The Dependency Container is a central component that manages the registration and resolution of dependencies. It acts as a repository for holding instances of classes and their dependencies, facilitating the inversion of control provided by dependency injection.


Constructor Injection
---------------------

Constructor Injection is a form of dependency injection where dependencies are provided through a class's constructor. This pattern enhances code readability, maintainability, and testability by explicitly declaring and injecting dependencies when creating an object.


Method Injection
----------------

Method Injection is another form of dependency injection where dependencies are injected into an object's method rather than its constructor. This allows for more flexible and dynamic dependency management, as dependencies can be provided at the time of method invocation.


Factory Registration
--------------------

Factory Registration is a technique where a factory function or class is used to create instances of a dependency. This allows for more complex instantiation logic, such as conditional creation based on runtime parameters or integration with external resources.


Instance Registration
---------------------

Instance Registration involves registering an already created instance of an object as a dependency. This is useful when you want to use a specific instance with a predefined state or when integrating with third-party libraries that provide instances of their classes.


Tags
----

Tags are used to categorize and identify dependencies within the container. By registering and resolving dependencies with tags, you can group related dependencies and retrieve them collectively. This is particularly useful in scenarios where you need to apply the same operation to multiple dependencies or when you want to resolve dependencies based on certain criteria.


Scoped Dependencies
-------------------

Scoped Dependencies refer to instances of objects that have a limited scope during their lifecycle. In `py-dependency-injection`, you can register dependencies with three different scopes, which are transient, scoped, or singleton, allowing control over how instances are created and managed.


Dependency Scopes
-----------------

Dependency Scopes define the lifecycle and visibility of a dependency within the application. The `py-dependency-injection` library supports three scopes:

- **Transient**: A new instance is created each time the dependency is resolved.
- **Scoped**: A single instance is created within a specific scope (e.g., a request in a web application) and reused across that scope.
- **Singleton**: A single instance is created and shared throughout the application's lifetime.


Dependency Resolution
---------------------

Dependency Resolution is the process of retrieving an instance of a required dependency from the container. The `py-dependency-injection` library provides various methods for resolving dependencies, including direct resolution by type, resolution by tag, and resolution with constructor or method injection.
