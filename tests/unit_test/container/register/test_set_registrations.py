from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestSetRegistrations(UnitTestCase):
    def test_set_registrations_before_first_resolution(self):
        # arrange
        class Vehicle:
            pass

        dummy_container = DependencyContainer.get_instance("dummy_container")
        dummy_container.register_transient(Vehicle)
        new_registrations = dummy_container.get_registrations()

        container = DependencyContainer.get_instance()

        # act
        container.set_registrations(new_registrations)  # no exception

    def test_not_allowed_to_set_registrations_after_first_resolution(self):
        # arrange
        class Vehicle:
            pass

        class Fruit:
            pass

        dummy_container = DependencyContainer.get_instance("dummy_container")
        dummy_container.register_transient(Vehicle)
        new_registrations = dummy_container.get_registrations()

        container = DependencyContainer.get_instance()
        container.register_transient(Fruit)
        container.resolve(Fruit)

        # act & assert
        with self.assertRaises(Exception) as context:
            container.set_registrations(new_registrations)

        self.assertIn(
            "You can't set registrations after a dependency has been resolved.",
            str(context.exception),
        )
