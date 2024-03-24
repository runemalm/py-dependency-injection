############
Installation
############

Install using `pip <http://pypi.python.org/pypi/pip/>`_::

    $ pip install py-dependency-injection


#######
Example
#######

The following example demonstrates how to set up a dependency injection container and utilize it for registering and resolving dependencies::

    from dependency_injection.container import DependencyContainer


    container = DependencyContainer.get_instance()

    # Register dependencies
    container.register_transient(SomeInterface, SomeClass)
    container.register_scoped(AnotherInterface, AnotherClass)
    container.register_singleton(ThirdInterface, ThirdClass)

    # Resolve dependencies
    transient_instance = container.resolve(SomeInterface)
    scoped_instance = container.resolve(AnotherInterface, scope_name="http_request_scope_123")
    singleton_instance = container.resolve(ThirdInterface)

    # Use dependencies
    transient_instance.do_something()
    scoped_instance.do_something()
    singleton_instance.do_something()

Depending on the application framework, you may perform these steps in different parts of the code, but the essence remains the same.


##############
Basic Concepts
##############

These are the fundamental concepts of the library:

* :ref:`Dependency Injection`
* :ref:`Dependency Container`
* :ref:`Constructor Injection`
* :ref:`Scoped Dependencies`

See below for a brief explanation of each concept.


Dependency Injection
--------------------

Dependency Injection (DI) is a design pattern that enables the inversion of control in software applications by allowing the injection of dependencies from external sources. In the context of `py-dependency-injection`, it simplifies the management of object dependencies and promotes modular and testable code.


Dependency Container
--------------------

The Dependency Container is a central component that manages the registration and resolution of dependencies. It acts as a repository for holding instances of classes and their dependencies, facilitating the inversion of control provided by dependency injection.


Constructor Injection
---------------------

Constructor Injection is a form of dependency injection where dependencies are provided through a class's constructor. This pattern enhances code readability, maintainability, and testability by explicitly declaring and injecting dependencies when creating an object.


Scoped Dependencies
-------------------

Scoped Dependencies refer to instances of objects that have a limited scope during their lifecycle. In `py-dependency-injection`, you can register dependencies with three different scopes, which are transient, scoped, or singleton, allowing control over how instances are created and managed.


###############
Troubleshooting
###############

If you encounter unexpected behavior in the `py-dependency-injection` package, it can be helpful to increase the logging level of the logger to the ``DEBUG`` level. If logging is not enabled, you can set it up as follows::

    import logging

    logging.basicConfig()
    logging.getLogger('py-dependency-injection').setLevel(logging.DEBUG)

This configuration will provide detailed information about the internal workings of the `py-dependency-injection` library.
