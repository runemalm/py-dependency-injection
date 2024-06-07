import pytest

from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveWithArgs(UnitTestCase):
    def test_resolve_passes_constructor_args(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            def __init__(self, color, make):
                self.color = color
                self.make = make

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        implementation = Car
        dependency_container.register_transient(
            dependency=dependency,
            implementation=implementation,
            constructor_args={"color": "red", "make": "Volvo"},
        )

        # act
        resolved_dependency = dependency_container.resolve(dependency)

        # assert
        self.assertEqual("red", resolved_dependency.color)
        self.assertEqual("Volvo", resolved_dependency.make)

    def test_resolve_with_extra_constructor_arg_raises(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            def __init__(self, color: str, make: str):
                self.color = color
                self.make = make

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        implementation = Car
        dependency_container.register_transient(
            dependency=dependency,
            implementation=implementation,
            constructor_args={"color": "red", "make": "Volvo", "extra": "argument"},
        )

        # act
        with pytest.raises(
            ValueError,
            match="Invalid constructor argument 'extra' for class 'Car'. "
            "The class does not have a constructor parameter with this name.",
        ):
            dependency_container.resolve(dependency)

    def test_resolve_with_wrong_constructor_arg_type_raises(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            def __init__(self, color: str, make: str):
                self.color = color
                self.make = make

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        implementation = Car
        dependency_container.register_transient(
            dependency=dependency,
            implementation=implementation,
            constructor_args={"color": "red", "make": -1},
        )

        # act
        with pytest.raises(
            TypeError,
            match="Constructor argument 'make' has an incompatible type. "
            "Expected type: <class 'str'>, provided type: <class 'int'>.",
        ):
            dependency_container.resolve(dependency)

    def test_resolve_when_no_constructor_arg_type_is_ok(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            def __init__(self, color: str, make):
                self.color = color
                self.make = make

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        implementation = Car
        dependency_container.register_transient(
            dependency=dependency,
            implementation=implementation,
            constructor_args={"color": "red", "make": -1},
        )

        # act + assert (no exception)
        dependency_container.resolve(dependency)

    def test_resolve_merges_registered_constructor_args_with_auto_injected_dependencies(
        self,
    ):
        # arrange
        class Engine:
            pass

        class Vehicle:
            pass

        class Car(Vehicle):
            def __init__(self, color: str, engine: Engine):
                self.color = color
                self.engine = engine

        class CarFactory:
            @classmethod
            def create(cls, color: str, engine: Engine) -> Car:
                return Car(color=color, engine=engine)

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Engine)
        dependency_container.register_transient(
            Vehicle,
            Car,
            constructor_args={"color": "red"},
        )

        # act
        resolved_dependency = dependency_container.resolve(Vehicle)

        # assert
        self.assertIsInstance(resolved_dependency, Car)
        self.assertEqual("red", resolved_dependency.color)
        self.assertIsInstance(resolved_dependency.engine, Engine)
