import pytest

from unit_test.unit_test_case import UnitTestCase
from dependency_injection import DependencyContainer


class TestRegisterInstance(UnitTestCase):
    def test_register_instance_succeeds_when_not_previously_registered(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        instance = Car()

        # act
        dependency_container.register_instance(Vehicle, instance)

        # assert
        # (no exception thrown)

    def test_register_instance_fails_when_already_registered(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        instance = Car()
        dependency_container.register_instance(Vehicle, instance)

        # act + assert
        with pytest.raises(ValueError, match="is already registered"):
            dependency_container.register_instance(Vehicle, instance)
