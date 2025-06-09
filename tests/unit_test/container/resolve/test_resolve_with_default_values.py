from typing import Optional
from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveWithDefaultValues(UnitTestCase):
    def test_resolve_optional_dependency_uses_default_value_when_not_registered(self):
        # arrange
        class Engine:
            pass

        class Car:
            def __init__(self, engine: Optional[Engine] = "default_engine"):
                self.engine = engine

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Car)

        # act
        resolved_car = dependency_container.resolve(Car)

        # assert
        self.assertEqual(resolved_car.engine, "default_engine")

    def test_resolve_uses_default_value_for_non_optional_when_not_registered(self):
        # arrange
        class Car:
            def __init__(self, color: str = "blue"):
                self.color = color

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Car)

        # act
        resolved_car = dependency_container.resolve(Car)

        # assert
        self.assertEqual(resolved_car.color, "blue")

    def test_resolve_with_mixed_default_and_optional_values(self):
        # arrange
        class Engine:
            pass

        class Car:
            def __init__(self, color: str = "blue", engine: Optional[Engine] = None):
                self.color = color
                self.engine = engine

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Car)

        # act
        resolved_car = dependency_container.resolve(Car)

        # assert
        self.assertEqual(resolved_car.color, "blue")
        self.assertIsNone(resolved_car.engine)
