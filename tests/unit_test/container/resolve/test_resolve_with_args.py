import pytest

from typing import Optional
from unit_test.unit_test_case import UnitTestCase
from dependency_injection import DependencyContainer


class TestResolveWithArgs(UnitTestCase):
    def test_resolve_passes_constructor_kwargs(
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
        service = Vehicle
        implementation = Car
        dependency_container.register_transient(
            service=service,
            implementation=implementation,
            constructor_kwargs={"color": "red", "make": "Volvo"},
        )

        # act
        resolved = dependency_container.resolve(service)

        # assert
        self.assertEqual("red", resolved.color)
        self.assertEqual("Volvo", resolved.make)

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
        service = Vehicle
        implementation = Car
        dependency_container.register_transient(
            service=service,
            implementation=implementation,
            constructor_kwargs={"color": "red", "make": "Volvo", "extra": "argument"},
        )

        # act
        with pytest.raises(
            ValueError,
            match="Invalid constructor argument 'extra' for class 'Car'. "
            "The class does not have a constructor parameter with this name.",
        ):
            dependency_container.resolve(service)

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
        service = Vehicle
        implementation = Car
        dependency_container.register_transient(
            service=service,
            implementation=implementation,
            constructor_kwargs={"color": "red", "make": -1},
        )

        # act
        with pytest.raises(
            TypeError,
            match="Constructor argument 'make' has an incompatible type. "
            "Expected: <class 'str'>, provided: <class 'int'>.",
        ):
            dependency_container.resolve(service)

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
        service = Vehicle
        implementation = Car
        dependency_container.register_transient(
            service=service,
            implementation=implementation,
            constructor_kwargs={"color": "red", "make": -1},
        )

        # act + assert (no exception)
        dependency_container.resolve(service)

    def test_resolve_merges_registered_constructor_kwargs_with_auto_injected_deps(
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
            constructor_kwargs={"color": "red"},
        )

        # act
        resolved = dependency_container.resolve(Vehicle)

        # assert
        self.assertIsInstance(resolved, Car)
        self.assertEqual("red", resolved.color)
        self.assertIsInstance(resolved.engine, Engine)

    def test_optional_dependency_overridden_by_constructor_kwargs(self):
        # arrange
        class Engine:
            def __init__(self, name: str):
                self.name = name

        class Car:
            def __init__(self, engine: Optional[Engine] = None):
                self.engine = engine

        engine_instance = Engine("Manual")

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(
            Car, constructor_kwargs={"engine": engine_instance}
        )

        # act
        resolved_car = dependency_container.resolve(Car)

        # assert
        self.assertEqual(resolved_car.engine.name, "Manual")

    def test_optional_dependency_not_registered_but_constructor_arg_provided(self):
        # arrange
        class Engine:
            def __init__(self, name: str):
                self.name = name

        class Car:
            def __init__(self, engine: Optional[Engine] = None):
                self.engine = engine

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(
            Car, constructor_kwargs={"engine": Engine("Fallback")}
        )

        # act
        resolved_car = dependency_container.resolve(Car)

        # assert
        self.assertEqual(resolved_car.engine.name, "Fallback")

    def test_optional_dependency_registered_but_constructor_arg_still_takes_precedence(
        self,
    ):
        # arrange
        class Engine:
            def __init__(self, name: str):
                self.name = name

        class Car:
            def __init__(self, engine: Optional[Engine] = None):
                self.engine = engine

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(
            Engine, constructor_kwargs={"name": "Auto"}
        )
        dependency_container.register_transient(
            Car, constructor_kwargs={"engine": Engine("Manual")}
        )

        # act
        resolved_car = dependency_container.resolve(Car)

        # assert
        self.assertEqual(resolved_car.engine.name, "Manual")  # not Auto
