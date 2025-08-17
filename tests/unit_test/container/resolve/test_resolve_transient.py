from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveTransient(UnitTestCase):
    def test_resolve_transient_returns_an_instance(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle
        implementation = Car
        dependency_container.register_transient(service, implementation)

        # act
        resolved = dependency_container.resolve(service)

        # assert
        self.assertIsInstance(resolved, Car)

    def test_resolve_transient_twice_returns_different_instances(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle
        implementation = Car
        dependency_container.register_transient(service, implementation)

        # act
        resolved_1 = dependency_container.resolve(service)
        resolved_2 = dependency_container.resolve(service)

        # assert
        self.assertNotEqual(resolved_1, resolved_2)

    def test_returns_an_instance_when_registered_without_implementation_arg(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle
        dependency_container.register_transient(service)

        # act
        resolved = dependency_container.resolve(service)

        # assert
        self.assertIsInstance(resolved, Vehicle)
