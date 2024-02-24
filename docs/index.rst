py-dependency-injection
=======================

Welcome to the py-dependency-injection library documentation.

Whether you are new to dependency injection or an experienced developer, this guide will help you get started and make the most out of the features offered by the library.

Below is an example of the library in use.

Check out the :doc:`user guide<gettingstarted>` to get started using the library.
  

Example
=======

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
