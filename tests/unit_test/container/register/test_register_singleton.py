import pytest

from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestRegisterSingleton(UnitTestCase):
    def test_register_singleton_succeeds_when_not_previously_registered(
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
        dependency_container.register_singleton(service, implementation)

        # assert
        # (no exception thrown)

    def test_register_singleton_fails_when_already_registered(
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
        dependency_container.register_singleton(service, implementation)

        # act + assert
        with pytest.raises(ValueError, match="is already registered"):
            dependency_container.register_singleton(service, implementation)

    def test_register_singleton_when_dependency_and_implementation_being_the_same(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle

        # act
        dependency_container.register_singleton(service)

        # assert (no exception thrown)
