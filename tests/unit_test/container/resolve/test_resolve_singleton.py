from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveSingleton(UnitTestCase):

    def test_resolve_singleton_returns_instance(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car
        dependency_container.register_singleton(interface, dependency_class)

        # act
        resolved_dependency = dependency_container.resolve(interface)

        # assert
        self.assertIsInstance(resolved_dependency, Car)

    def test_resolve_singleton_twice_returns_same_instance(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer()
        interface = Vehicle
        dependency_class = Car
        dependency_container.register_singleton(interface, dependency_class)

        # act
        resolved_dependency_1 = dependency_container.resolve(interface)
        resolved_dependency_2 = dependency_container.resolve(interface)

        # assert
        self.assertEqual(resolved_dependency_1, resolved_dependency_2)
