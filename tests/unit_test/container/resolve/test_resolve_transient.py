from dependency_injection.container.container import DependencyContainer
from unit_test.car import Car
from unit_test.unit_test_case import UnitTestCase
from unit_test.vehicle import Vehicle


class TestResolveTransient(UnitTestCase):

    def test_resolve_transient_returns_an_instance(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car
        dependency_container.register_transient(interface, dependency_class)

        # act
        resolved_dependency = dependency_container.resolve(interface)

        # assert
        self.assertIsInstance(resolved_dependency, Car)

    def test_resolve_transient_twice_returns_different_instances(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer()
        interface = Vehicle
        dependency_class = Car
        dependency_container.register_transient(interface, dependency_class)

        # act
        resolved_dependency_1 = dependency_container.resolve(interface)
        resolved_dependency_2 = dependency_container.resolve(interface)

        # assert
        self.assertNotEquals(resolved_dependency_1, resolved_dependency_2)

