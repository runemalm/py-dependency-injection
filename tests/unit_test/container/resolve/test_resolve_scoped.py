from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveScoped(UnitTestCase):

    def test_resolve_scoped_in_same_scope_returns_same_instance(
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
        dependency_container.register_scoped(dependency, implementation)

        # act
        resolved_dependency_in_scope_1 = dependency_container.resolve(dependency, scope_name="test-scope")
        resolved_dependency_in_scope_2 = dependency_container.resolve(dependency, scope_name="test-scope")

        # assert
        self.assertEqual(resolved_dependency_in_scope_1, resolved_dependency_in_scope_2)

    def test_resolve_scoped_in_different_scopes_returns_different_instances(
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
        dependency_container.register_scoped(dependency, implementation)

        # act
        resolved_dependency_in_scope_1 = dependency_container.resolve(dependency, scope_name="scope_1")
        resolved_dependency_in_scope_2 = dependency_container.resolve(dependency, scope_name="scope_2")

        # assert
        self.assertNotEqual(resolved_dependency_in_scope_1, resolved_dependency_in_scope_2)

    def test_resolve_scoped_when_registered_with_dependency_and_implementation_being_the_same_returns_an_instance(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        dependency_container.register_scoped(dependency)

        # act
        resolved_dependency = dependency_container.resolve(dependency)

        # assert
        self.assertIsInstance(resolved_dependency, Vehicle)

