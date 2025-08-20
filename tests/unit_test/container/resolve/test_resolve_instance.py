from dependency_injection import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveInstance(UnitTestCase):
    def test_resolve_instance_returns_instance(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        instance = Car()
        dependency_container.register_instance(Vehicle, instance)

        # act
        resolved = dependency_container.resolve(Vehicle)

        # assert
        self.assertEqual(resolved, instance)

    def test_resolve_instance_twice_returns_same_instance(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        instance = Car()
        dependency_container.register_instance(Vehicle, instance)

        # act
        resolved_1 = dependency_container.resolve(Vehicle)
        resolved_2 = dependency_container.resolve(Vehicle)

        # assert
        self.assertEqual(resolved_1, resolved_2)
