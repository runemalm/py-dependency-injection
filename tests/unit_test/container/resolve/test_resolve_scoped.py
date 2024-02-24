from dependency_injection.container import DependencyContainer
from unit_test.car import Car
from unit_test.unit_test_case import UnitTestCase
from unit_test.vehicle import Vehicle


class TestResolveScoped(UnitTestCase):

    def test_resolve_singleton_in_same_scope_returns_same_instance(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car
        dependency_container.register_scoped(interface, dependency_class)

        # act
        resolved_dependency_in_scope_1 = dependency_container.resolve(interface, scope_name="test-scope")
        resolved_dependency_in_scope_2 = dependency_container.resolve(interface, scope_name="test-scope")

        # assert
        self.assertEqual(resolved_dependency_in_scope_1, resolved_dependency_in_scope_2)

    def test_resolve_singleton_in_different_scopes_returns_different_instances(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car
        dependency_container.register_scoped(interface, dependency_class)

        # act
        resolved_dependency_in_scope_1 = dependency_container.resolve(interface, scope_name="scope_1")
        resolved_dependency_in_scope_2 = dependency_container.resolve(interface, scope_name="scope_2")

        # assert
        self.assertNotEqual(resolved_dependency_in_scope_1, resolved_dependency_in_scope_2)
