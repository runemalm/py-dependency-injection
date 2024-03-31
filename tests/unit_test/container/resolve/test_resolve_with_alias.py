from dependency_injection.container import DependencyContainer

from unit_test.unit_test_case import UnitTestCase

from unit_test.container.resolve.vehicle import Vehicle
from unit_test.container.resolve.vehicle import Vehicle as VehicleAlias


class TestResolveWithAlias(UnitTestCase):
    def test_register_with_alias_and_resolve_with_original_name(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(VehicleAlias)

        # act
        resolved_dependency = dependency_container.resolve(Vehicle)

        # assert
        self.assertIsNotNone(resolved_dependency)
        self.assertIsInstance(resolved_dependency, Vehicle)
