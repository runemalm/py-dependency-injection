import pytest

from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestRegisterTransient(UnitTestCase):
    def test_succeeds_when_not_previously_registered(
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

        # act
        dependency_container.register_transient(service, implementation)

        # assert (no exception thrown)

    def test_fails_when_already_registered(
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
        dependency_container.register_transient(service, implementation)

        # act + assert
        with pytest.raises(ValueError, match="is already registered"):
            dependency_container.register_transient(service, implementation)

    def test_success_when_dependency_and_implementation_same(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle

        # act
        dependency_container.register_transient(service)

        # assert (no exception thrown)

    def test_fails_when_already_registered_and_dependency_and_implementation_same(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Vehicle, Car)

        # act + assert
        with pytest.raises(ValueError, match="is already registered"):
            dependency_container.register_transient(Vehicle)

    def test_success_when_other_dependency_registered_of_implementation_ancestor_class(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Vehicle, Car)

        # act
        dependency_container.register_transient(Car)

        # assert (no exception thrown)
