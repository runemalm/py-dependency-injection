###############
Getting Started
###############

.. note::
    `py-dependency-injection` has transitioned to beta! Features are now stable and ready for broader testing. Feedback is encouraged to help refine the library for its final release.

############
Introduction
############

`py-dependency-injection` is a lightweight and flexible dependency injection library for Python. It simplifies managing dependencies in your applications, promoting cleaner and more testable code.

This guide will help you understand the key concepts and how to start using the library. For detailed examples, see the `Examples` section.

############
Installation
############

Install the library using pip:

.. code-block:: bash

    $ pip install py-dependency-injection

The library supports Python versions 3.7 through 3.13.

##########################
Core Concepts and Features
##########################

`py-dependency-injection` offers:

- **Scoped Dependency Management**: Define lifetimes for your dependencies (e.g., transient, scoped, singleton).
- **Flexible Registrations**: Use constructors, factories, or predefined instances for dependency registration.
- **Tag-Based Organization**: Categorize and resolve dependencies using tags.
- **Multiple Containers**: Isolate dependencies for different parts of your application.

Refer to the `Examples` section for detailed usage scenarios.

####################
Quick Start Overview
####################

1. **Create a Dependency Container**:
   - The `DependencyContainer` is the core object for managing dependencies.

2. **Register Dependencies**:
   - Dependencies can be registered with different lifetimes: transient, scoped, or singleton.

3. **Resolve Dependencies**:
   - Use the container to resolve dependencies where needed.

Basic workflow:

.. code-block:: python

    from dependency_injection.container import DependencyContainer

    class Connection:
        pass

    class PostgresConnection(Connection):
        pass

    # Create a container
    container = DependencyContainer.get_instance()

    # Register and resolve dependencies
    container.register_singleton(Connection, PostgresConnection)
    connection = container.resolve(Connection)
    print(type(connection).__name__)  # Output: PostgresConnection

##############
Best Practices
##############

- **Use Constructor Injection**: Preferred for most cases as it promotes clear and testable designs.
- **Leverage Tags for Organization**: Group dependencies logically using tags.
- **Choose the Right Scope**: Use scoped or singleton lifetimes to optimize performance and resource usage.
- **Keep Dependencies Decoupled**: Avoid tightly coupling your components to the container.
- **Isolate Contexts with Containers**: Use multiple containers to manage dependencies for separate modules or contexts.

#################
Where to Go Next?
#################

- **Examples**:
  Explore detailed examples of how to register, resolve, and manage dependencies effectively in the `Examples` section.

- **Community and Support**:
  Join our community on GitHub to ask questions, report issues, or contribute to the project.
