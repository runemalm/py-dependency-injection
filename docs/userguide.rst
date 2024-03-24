###############
Getting Started
###############


Installation
------------

Install using `pip <http://pypi.python.org/pypi/pip/>`_::

    $ pip install py-dependency-injection


Creating a Dependency Container
-------------------------------

.. code-block:: python

    # Get the default dependency container
    dependency_container = DependencyContainer.get_instance()

    # Create additional named containers if needed
    another_container = DependencyContainer.get_instance(name="another_container")


Registering Dependencies with Scopes
------------------------------------

.. code-block:: python

    # Register a transient dependency (a new instance every time)
    dependency_container.register_transient(Connection, PostgresConnection)

    # Register a scoped dependency (a new instance per scope)
    dependency_container.register_scoped(Connection, PostgresConnection, scope_name="http_request")

    # Register a singleton dependency (a single instance for the container's lifetime)
    dependency_container.register_singleton(Connection, PostgresConnection)


Using Constructor Arguments
---------------------------

.. code-block:: python

    # Register a dependency with constructor arguments
    dependency_container.register_transient(
        Connection,
        PostgresConnection,
        constructor_args={"host": "localhost", "port": 5432}
    )


Using Factory Functions
-----------------------

.. code-block:: python

    # Define a factory function
    def create_connection(host: str, port: int) -> Connection:
        return PostgresConnection(host=host, port=port)

    # Register dependency with the factory function
    dependency_container.register_factory(Connection, create_connection, factory_args={"host": "localhost", "port": 5432})

.. code-block:: python

    # Register dependency with a lambda factory function
    dependency_container.register_factory(
        Connection,
        lambda host, port: PostgresConnection(host=host, port=port),
        factory_args={"host": "localhost", "port": 5432}
    )

.. code-block:: python

    # Register dependency with a factory class function
    class ConnectionFactory:
        @staticmethod
        def create_connection(host: str, port: int) -> Connection:
            return PostgresConnection(host=host, port=port)

    # Register the factory method
    dependency_container.register_factory(
        Connection,
        connection_factory.create_connection,
        factory_args={"host": "localhost", "port": 5432}
    )


Registering and Using Instances
-------------------------------

.. code-block:: python

    # Create an instance
    my_connection = PostgresConnection(host="localhost", port=5432)

    # Register the instance
    dependency_container.register_instance(Connection, my_connection)

    # Resolve the instance
    resolved_connection = dependency_container.resolve(Connection)
    print(resolved_connection.host)  # Output: localhost


Registering and Resolving with Tags
-----------------------------------

.. code-block:: python

    # Register dependencies with tags
    dependency_container.register_transient(Connection, PostgresConnection, tags={"Querying", "Startable"})
    dependency_container.register_scoped(BusConnection, KafkaBusConnection, tags={"Publishing", "Startable"})

    # Resolve dependencies by tags
    startable_dependencies = dependency_container.resolve_all(tags={"Startable"})
    for dependency in startable_dependencies:
        dependency.start()


Using Constructor Injection
---------------------------

.. code-block:: python

    class OrderRepository:
        def __init__(self, connection: Connection):
            self.connection = connection

    # Register dependencies
    dependency_container.register_transient(OrderRepository)
    dependency_container.register_singleton(Connection, PostgresConnection)

    # Resolve the OrderRepository with injected dependencies
    repository = dependency_container.resolve(OrderRepository)
    print(repository.connection.__class__.__name__)  # Output: PostgresConnection


Using Method Injection
----------------------

.. code-block:: python

    class OrderController:
        @staticmethod
        @inject()
        def place_order(order: Order, repository: OrderRepository):
            order.status = "placed"
            repository.save(order)

    # Register the dependency
    dependency_container.register_transient(OrderRepository)
    dependency_container.register_singleton(Connection, PostgresConnection)

    # Use method injection to inject the dependency
    my_order = Order.create()
    OrderController.place_order(order=my_order)  # The repository instance will be automatically injected

You can also specify container and scope using the decorator arguments ``container_name`` and ``scope_name``.
