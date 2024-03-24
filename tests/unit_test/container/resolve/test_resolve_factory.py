from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveTransient(UnitTestCase):
    def test_resolve_factory_returns_an_instance(
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
        dependency_container.register_factory(Vehicle, factory=CarFactory.create)

        # act
        resolved_dependency = dependency_container.resolve(Vehicle)

        # assert
        self.assertIsInstance(resolved_dependency, Car)

    def test_resolve_factory_twice_returns_different_instances(
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
        dependency_container.register_factory(Vehicle, factory=CarFactory.create)

        # act
        resolved_dependency_1 = dependency_container.resolve(Vehicle)
        resolved_dependency_2 = dependency_container.resolve(Vehicle)

        # assert
        self.assertNotEqual(resolved_dependency_1, resolved_dependency_2)

    def test_resolve_factory_with_args_passes_args(
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
        dependency_container.register_factory(
            Vehicle,
            factory=CarFactory.create,
            factory_args={"color": "red", "mileage": 6327},
        )

        # act
        resolved_dependency = dependency_container.resolve(Vehicle)

        # assert
        self.assertIsInstance(resolved_dependency, Car)
        self.assertEqual("red", resolved_dependency.color)
        self.assertEqual(6327, resolved_dependency.mileage)

    def test_resolve_factory_registered_with_lambda(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            def __init__(self, color: str):
                self.color = color

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_factory(Vehicle, factory=lambda: Car(color="red"))

        # act
        resolved_dependency = dependency_container.resolve(Vehicle)

        # assert
        self.assertIsInstance(resolved_dependency, Car)
        self.assertEqual(resolved_dependency.color, "red")
