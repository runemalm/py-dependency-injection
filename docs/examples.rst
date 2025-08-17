##############################
Creating dependency containers
##############################

In this example, we demonstrate how to create and retrieve dependency containers using the `DependencyContainer` class. This is useful when you want to manage services in different contexts or areas of your application.

.. code-block:: python

    from dependency_injection.container import DependencyContainer

    # Get the default dependency container
    dependency_container = DependencyContainer.get_instance()

    # Get an additional container if necessary
    another_container = DependencyContainer.get_instance(
        name="another_container"
    )


################################
Registering services with scopes
################################

This example shows how to register services with different scopes (transient, scoped, and singleton). This is important for controlling the lifecycle and reuse of your services.

.. code-block:: python

    # Register a transient service
    dependency_container.register_transient(
        Connection,
        PostgresConnection
    )

    # Register a scoped service
    dependency_container.register_scoped(
        Connection,
        PostgresConnection,
        scope_name="http_request"
    )

    # Register a singleton service
    dependency_container.register_singleton(
        Connection,
        PostgresConnection
    )


###################################
Registering with constructor kwargs
###################################

Here, we illustrate how to register a service with constructor keyword arguments. This allows you to provide specific values or configurations to your services when they are instantiated.

.. code-block:: python

    # Register with constructor kwargs
    dependency_container.register_transient(
        Connection,
        PostgresConnection,
        constructor_kwargs={
            "host": "localhost",
            "port": 5432
        }
    )


################################
Resolving with factory functions
################################

In this section, we demonstrate how to register and resolve services using the factory pattern. This provides flexibility in how your services are created and configured. You can use factory functions, factory classes and factory lambdas.

.. note::
    Any `callable <https://docs.python.org/3/glossary.html#term-callable>`_ can be used as factory.

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
        factory_kwargs={
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
        factory_kwargs={
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
        factory_kwargs={
            "host": "localhost",
            "port": 5432
        }
    )


###############################
Registering and using instances
###############################

This example demonstrates how to register and use instances of your services. This is useful when you want to provide a specific instance of a service for use throughout your application.

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
    resolved = dependency_container.resolve(Connection)
    print(resolved.host)  # Output: localhost


###################################
Registering and resolving with tags
###################################

In this example, we show how to register and resolve services using tags. This allows you to categorize and retrieve specific groups of services based on their tags.

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

    # Register another service with tags
    dependency_container.register_scoped(
        BusConnection,
        KafkaBusConnection,
        tags={
            Publishing,
            Startable
        }
    )

    # Resolve all services with the 'Startable' tag
    resolved = dependency_container.resolve_all(
        tags={
            Startable
        }
    )

    # Use resolved services
    for service in resolved:
        service.start()


###########################
Using constructor injection
###########################

This example illustrates how to use constructor injection to automatically inject services into your classes. This is a common pattern for managing dependencies in object-oriented programming. This is probably how you'll want to resolve 99% of the services in your software application.

.. code-block:: python

    class OrderRepository:
        def __init__(self, connection: Connection):
            self.connection = connection

    # Register services
    dependency_container.register_transient(
        OrderRepository
    )

    dependency_container.register_singleton(
        Connection,
        PostgresConnection
    )

    # Resolve with injected services
    repository = dependency_container.resolve(
        OrderRepository
    )

    # Use injected service
    print(repository.connection.__class__.__name__)  # Output: PostgresConnection


################################################
Using constructor injection with tagged services
################################################

This example demonstrates how to use constructor injection to automatically inject tagged services into your classes. By leveraging tags, you can group and categorize services, enabling automatic injection based on specific criteria.

.. code-block:: python

    class PrimaryPort:
        pass

    class SecondaryPort:
        pass

    class HttpAdapter(PrimaryPort):
        pass

    class PostgresCarRepository(SecondaryPort):
        pass

    class Application:
        def __init__(self, primary_ports: List[Tagged[PrimaryPort]], secondary_ports: List[Tagged[SecondaryPort]]):
            self.primary_ports = primary_ports
            self.secondary_ports = secondary_ports

    # Register services with tags
    dependency_container.register_transient(HttpAdapter, tags={PrimaryPort})
    dependency_container.register_transient(PostgresCarRepository, tags={SecondaryPort})

    # Register the Application class to have its services injected
    dependency_container.register_transient(Application)

    # Resolve the Application class, with tagged services automatically injected
    application = dependency_container.resolve(Application)

    # Use the injected services
    print(f"Primary ports: {len(application.primary_ports)}")  # Output: Primary ports: 1
    print(f"Secondary ports: {len(application.secondary_ports)}")  # Output: Secondary ports: 1
    print(f"Primary port instance: {type(application.primary_ports[0]).__name__}")  # Output: HttpAdapter
    print(f"Secondary port instance: {type(application.secondary_ports[0]).__name__}")  # Output: PostgresCarRepository


In this example, the `Application` class expects lists of instances tagged with `PrimaryPort` and `SecondaryPort`. By tagging and registering these services, the container automatically injects the correct instances into the `Application` class when it is resolved.

Tags offer a powerful way to manage services, ensuring that the right instances are injected based on your application's needs.

.. note::
    You can also use the ``AnyTagged`` and ``AllTagged`` classes to inject services based on more complex tagging logic. ``AnyTagged`` allows injection of any service matching one or more specified tags, while ``AllTagged`` requires the service to match all specified tags before injection. This provides additional flexibility in managing and resolving services in your application.


######################
Using method injection
######################

This example demonstrates how to use method injection to inject services into methods at runtime. This is useful for dynamically providing services to class- or static methods, without affecting the entire class.

.. note::
    You can pass the arguments ``container_name`` and ``scope_name`` to ``@inject``.

.. note::
    The ``@inject`` has to be applied to the function after the ``@classmethod`` or ``@staticmethod``.

.. code-block:: python

    class OrderController:
        @staticmethod
        @inject()
        def place_order(order: Order, repository: OrderRepository):
            order.set_status("placed")
            repository.save(order)

    # Register services
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
