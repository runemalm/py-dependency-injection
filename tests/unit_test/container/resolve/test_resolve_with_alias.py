from unit_test.unit_test_case import UnitTestCase
from unit_test.container.resolve.test_data.vehicle import Vehicle
from unit_test.container.resolve.test_data.vehicle import Vehicle as VehicleAlias

from dependency_injection import DependencyContainer


class TestResolveWithAlias(UnitTestCase):
    def test_register_with_alias_and_resolve_with_original_name(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(VehicleAlias)

        # act
        resolved = dependency_container.resolve(Vehicle)

        # assert
        self.assertIsNotNone(resolved)
        self.assertIsInstance(resolved, Vehicle)
