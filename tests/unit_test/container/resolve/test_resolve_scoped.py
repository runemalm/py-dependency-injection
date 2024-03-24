from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveScoped(UnitTestCase):
    def test_returns_same_instance_when_registered_with_same_scope(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_scoped(Vehicle, Car)

        # act
        resolved_dependency_in_scope_1 = dependency_container.resolve(
            Vehicle, scope_name="test-scope"
        )
        resolved_dependency_in_scope_2 = dependency_container.resolve(
            Vehicle, scope_name="test-scope"
        )

        # assert
        self.assertEqual(resolved_dependency_in_scope_1, resolved_dependency_in_scope_2)

    def test_returns_different_instances_when_registered_in_different_scopes(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_scoped(Vehicle, Car)

        # act
        resolved_dependency_in_scope_1 = dependency_container.resolve(
            Vehicle, scope_name="scope_1"
        )
        resolved_dependency_in_scope_2 = dependency_container.resolve(
            Vehicle, scope_name="scope_2"
        )

        # assert
        self.assertNotEqual(
            resolved_dependency_in_scope_1, resolved_dependency_in_scope_2
        )

    def test_returns_an_instance_when_registered_without_implementation_arg(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_scoped(Vehicle)

        # act
        resolved_dependency = dependency_container.resolve(Vehicle)

        # assert
        self.assertIsInstance(resolved_dependency, Vehicle)
