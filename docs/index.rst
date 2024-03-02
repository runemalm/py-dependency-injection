py-dependency-injection
=======================

Welcome to the documentation for the `py-dependency-injection` library.

Introduction
============

The `py-dependency-injection` library simplifies and enhances the management of dependencies in your Python projects. Whether you're new to the concept of dependency injection or an experienced developer seeking an efficient solution, this guide is designed to help you grasp the fundamentals and leverage the features offered by the library.

Key Features
============

- **Flexible Dependency Management:** The library provides a flexible and intuitive way to manage dependencies within your Python applications, promoting modular and maintainable code.

- **Scoped, Transient, and Singleton Dependencies:** `py-dependency-injection` supports various dependency lifetimes, allowing you to choose between scoped, transient, and singleton instances based on your application's requirements.

- **Effortless Dependency Resolution:** With a straightforward API, resolving dependencies is a breeze. The library ensures that instances are created and managed seamlessly, allowing you to focus on building robust and scalable applications.

Example
=======

To get started quickly, take a look at the following example showcasing the basic usage of the library:

.. code-block:: python

    from dependency_injection.container.container import DependencyContainer


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

Explore the :doc:`user guide<gettingstarted>` to dive deeper into using the library effectively.

.. gettingstarted-docs:
.. toctree::
  :maxdepth: 1
  :caption: User guide

  gettingstarted

.. versionhistory-docs:
.. toctree::
  :maxdepth: 1
  :caption: Releases

  versionhistory

.. community-docs:
.. toctree::
  :maxdepth: 1
  :caption: Community

  community

.. apireference-docs:
.. toctree::
  :maxdepth: 1
  :caption: API Reference

  py-modindex
