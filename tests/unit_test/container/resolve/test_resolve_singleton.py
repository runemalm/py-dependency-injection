from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveSingleton(UnitTestCase):
    def test_returns_instance_when_resolved(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        implementation = Car
        dependency_container.register_singleton(dependency, implementation)

        # act
        resolved_dependency = dependency_container.resolve(dependency)

        # assert
        self.assertIsInstance(resolved_dependency, Car)

    def test_returns_same_instance_when_resolving_twice(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        implementation = Car
        dependency_container.register_singleton(dependency, implementation)

        # act
        resolved_dependency_1 = dependency_container.resolve(dependency)
        resolved_dependency_2 = dependency_container.resolve(dependency)

        # assert
        self.assertEqual(resolved_dependency_1, resolved_dependency_2)

    def test_returns_an_instance_when_registered_without_implementation_arg(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        dependency_container.register_singleton(dependency)

        # act
        resolved_dependency = dependency_container.resolve(dependency)

        # assert
        self.assertIsInstance(resolved_dependency, Vehicle)
