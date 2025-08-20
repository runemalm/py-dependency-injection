###############
Getting Started
###############

.. note::
    This library is currently in the release candidate stage.
    The public API is considered stable and is undergoing final validation before the 1.0.0 release.

############
Introduction
############

`py-dependency-injection` is a lightweight and extensible dependency injection library for Python — inspired by the built-in DI system in **ASP.NET Core**. It promotes constructor injection, supports scoped lifetimes, and encourages clean, testable application architecture.

This guide provides an overview of the key concepts and demonstrates how to start using the library effectively. For detailed examples, see the `Examples` section.

###########
Terminology
###########

In this guide:

- **Service** — an abstract type or protocol you depend on.
- **Implementation** — a concrete class that fulfills the service.

############
Installation
############

Choose your preferred installer:

.. tab:: pip

   .. code-block:: bash

      python -m pip install py-dependency-injection

.. tab:: Poetry

   .. code-block:: bash

      poetry add py-dependency-injection

.. tab:: uv (fast)

   .. code-block:: bash

      uv add py-dependency-injection

The library supports Python versions 3.9 through 3.13.

##########################
Core Concepts and Features
##########################

`py-dependency-injection` offers:

- **Scoped Service Management**: Define lifetimes for your services (transient, scoped, singleton).
- **Flexible Registrations**: Use constructors, factories, or predefined instances for service registration.
- **Tag-Based Organization**: Categorize and resolve services using tags.
- **Multiple Containers**: Isolate services for different parts of your application.

Refer to the `Examples` section for detailed usage scenarios.

####################
Quick Start Overview
####################

1. **Create a Dependency Container**:
   - The `DependencyContainer` is the core object for registering and resolving services.

2. **Register Services**:
   - Services can be registered with different lifetimes: transient, scoped, or singleton.

3. **Resolve Services**:
   - Use the container to resolve services where needed.

Basic workflow:

.. code-block:: python

    from dependency_injection import DependencyContainer

    class Connection:
        pass

    class PostgresConnection(Connection):
        pass

    # Create a container
    container = DependencyContainer.get_instance()

    # Register and resolve services
    container.register_singleton(Connection, PostgresConnection)
    connection = container.resolve(Connection)
    print(type(connection).__name__)  # Output: PostgresConnection

##############
Best Practices
##############

- **Prefer Constructor Injection**: It promotes clear interfaces and testable components.
- **Use the Right Lifetime**: Choose between transient, scoped, and singleton based on your component's role.
- **Organize with Tags**: Use tag-based registration and resolution to group related services.
- **Avoid Container Coupling**: Inject services via constructors rather than accessing the container directly.
- **Use Multiple Containers When Needed**: For modular apps or test isolation, create dedicated containers.

#################
Where to Go Next?
#################

- **Examples**:
  Explore detailed examples of how to register, resolve, and manage services effectively in the `Examples` section.

- **Community and Support**:
  Join our community on GitHub to ask questions, report issues, or contribute to the project.
