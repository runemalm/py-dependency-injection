##############################
Creating dependency containers
##############################

.. code-block:: python

    # Get the default dependency container
    dependency_container = DependencyContainer.get_instance()

    # Get an additional container if necessary
    another_container = DependencyContainer.get_instance(
        name="another_container"
    )


####################################
Registering dependencies with scopes
####################################

.. code-block:: python

    # Register a transient dependency
    dependency_container.register_transient(
        Connection,
        PostgresConnection
    )

    # Register a scoped dependency
    dependency_container.register_scoped(
        Connection,
        PostgresConnection,
        scope_name="http_request"
    )

    # Register a singleton dependency
    dependency_container.register_singleton(
        Connection,
        PostgresConnection
    )


######################################
Registering with constructor arguments
######################################

.. code-block:: python

    # Register with constructor arguments
    dependency_container.register_transient(
        Connection,
        PostgresConnection,
        constructor_args={
            "host": "localhost",
            "port": 5432
        }
    )


################################
Resolving with factory functions
################################

.. note::
    Any `callable <https://docs.python.org/3/glossary.html#term-callable>`_ can be used as factory function.

.. code-block:: python

    # Define factory function
    def factory_function(host: str, port: int) -> Connection:
        return PostgresConnection(
            host=host,
            port=port
        )

    # Register with factory function
    dependency_container.register_factory(
        Connection,
        factory_function,
        factory_args={
            "host": "localhost",
            "port": 5432
        }
    )

.. code-block:: python

    # Define factory class
    class FactoryClass:
        @staticmethod
        def create(host: str, port: int) -> Connection:
            return PostgresConnection(
                host=host,
                port=port
            )

    # Register with factory class
    dependency_container.register_factory(
        Connection,
        FactoryClass.create,
        factory_args={
            "host": "localhost",
            "port": 5432
        }
    )

.. code-block:: python

    # Register with lambda factory function
    dependency_container.register_factory(
        Connection,
        lambda host, port: PostgresConnection(
            host=host,
            port=port
        ),
        factory_args={
            "host": "localhost",
            "port": 5432
        }
    )


###############################
Registering and using instances
###############################

.. code-block:: python

    # Create instance
    instance = PostgresConnection(
        host="localhost",
        port=5432
    )

    # Register instance
    dependency_container.register_instance(
        Connection,
        instance
    )

    # Resolve instance
    resolved_instance = dependency_container.resolve(Connection)
    print(resolved_instance.host)  # Output: localhost


###################################
Registering and resolving with tags
###################################

.. code-block:: python

    # Register with tags
    dependency_container.register_scoped(
        Connection,
        PostgresConnection,
        tags={
            Querying,
            Startable
        }
    )

    # Register another dependency with tags
    dependency_container.register_scoped(
        BusConnection,
        KafkaBusConnection,
        tags={
            Publishing,
            Startable
        }
    )

    # Resolve all dependencies with a specific tag
    resolved_dependencies = dependency_container.resolve_all(
        tags={
            Startable
        }
    )

    # Use resolved dependencies
    for dependency in resolved_dependencies:
        dependency.start()


###########################
Using constructor injection
###########################

.. code-block:: python

    class OrderRepository:
        def __init__(self, connection: Connection):
            self.connection = connection

    # Register dependencies
    dependency_container.register_transient(
        OrderRepository
    )

    dependency_container.register_singleton(
        Connection,
        PostgresConnection
    )

    # Resolve with injected dependencies
    repository = dependency_container.resolve(
        OrderRepository
    )

    # Use injected dependency
    print(repository.connection.__class__.__name__)  # Output: PostgresConnection


######################
Using method injection
######################

.. code-block:: python

    class OrderController:
        @staticmethod
        @inject()
        def place_order(order: Order, repository: OrderRepository):
            order.set_status("placed")
            repository.save(order)

    # Register dependencies
    dependency_container.register_transient(
        OrderRepository
    )

    dependency_container.register_singleton(
        Connection,
        PostgresConnection
    )

    # Call decorated method (missing argument will be injected)
    OrderController.place_order(
        order=Order.create()
    )

.. note::
    You can pass ``container_name`` and ``scope_name`` arguments to the ``@inject`` decorator to specify container and/or scope. If none of the arguments are passed, the `default container` and the `default scope` will be used.
