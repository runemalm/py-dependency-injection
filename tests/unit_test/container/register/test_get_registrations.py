from dependency_injection.container import DependencyContainer
from dependency_injection.scope import Scope
from unit_test.unit_test_case import UnitTestCase


class TestGetRegistrations(UnitTestCase):
    def test_get_registrations_returns_empty_dict_initially(self):
        # arrange
        dependency_container = DependencyContainer.get_instance()

        # act
        registrations = dependency_container.get_registrations()

        # assert
        self.assertEqual(registrations, {})

    def test_get_registrations_returns_correct_registrations(self):
        # arrange
        class Vehicle:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Vehicle)

        # act
        registrations = dependency_container.get_registrations()

        # assert
        self.assertIn(Vehicle, registrations)
        self.assertEqual(registrations[Vehicle].dependency, Vehicle)
        self.assertEqual(registrations[Vehicle].implementation, Vehicle)
        self.assertEqual(registrations[Vehicle].scope, Scope.TRANSIENT)
