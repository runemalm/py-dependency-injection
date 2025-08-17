from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestRegisterWithArgs(UnitTestCase):
    def test_register_with_constructor_kwargs(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle
        implementation = Car

        # act + assert (no exception)
        dependency_container.register_transient(
            service,
            implementation,
            constructor_kwargs={"color": "red", "mileage": 3800},
        )
