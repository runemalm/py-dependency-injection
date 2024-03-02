from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestRegisterWithArgs(UnitTestCase):

    def test_register_with_constructor_args(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car

        # act + assert (no exception)
        dependency_container.register_transient(interface, dependency_class, constructor_args={"color": "red", "mileage": 3800})
