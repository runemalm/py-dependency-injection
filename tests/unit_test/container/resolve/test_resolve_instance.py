from dependency_injection.container import DependencyContainer
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
        resolved_dependency = dependency_container.resolve(Vehicle)

        # assert
        self.assertEqual(resolved_dependency, instance)

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
        resolved_dependency_1 = dependency_container.resolve(Vehicle)
        resolved_dependency_2 = dependency_container.resolve(Vehicle)

        # assert
        self.assertEqual(resolved_dependency_1, resolved_dependency_2)
