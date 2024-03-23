import pytest

from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestRegisterFactory(UnitTestCase):

    def test_register_with_factory_class_method_when_not_previously_registered(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        class CarFactory:
            @classmethod
            def create(cls) -> Car:
                return Car()

        dependency_container = DependencyContainer.get_instance()

        # act
        dependency_container.register_factory(Vehicle, factory=CarFactory.create)

        # assert
        # (no exception thrown)

    def test_register_with_factory_args(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            def __init__(self, color: str, mileage: int):
                self.color = color
                self.mileage = mileage

        class CarFactory:
            @classmethod
            def create(cls, color: str, mileage: int) -> Car:
                return Car(color=color, mileage=mileage)

        dependency_container = DependencyContainer.get_instance()

        # act + assert (no exception)
        dependency_container.register_factory(Vehicle, factory=CarFactory.create, factory_args={"color": "red", "mileage": 3800})

    def test_register_with_lambda_method(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()

        # act
        dependency_container.register_factory(Vehicle, factory=lambda: Car())

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

        class CarFactory:
            @classmethod
            def create(cls) -> Car:
                return Car()

        dependency_container = DependencyContainer.get_instance()

        # act
        dependency_container.register_factory(Vehicle, factory=CarFactory.create)

        # act + assert
        with pytest.raises(ValueError, match="is already registered"):
            dependency_container.register_factory(Vehicle, factory=CarFactory.create)
