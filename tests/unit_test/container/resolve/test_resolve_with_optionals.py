from typing import Optional
from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveWithOptionals(UnitTestCase):
    def test_resolve_optional_dependency_with_none_when_not_registered(self):
        # arrange
        class Engine:
            pass

        class Car:
            def __init__(self, engine: Optional[Engine] = None):
                self.engine = engine

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Car)

        # act
        resolved_car = dependency_container.resolve(Car)

        # assert
        self.assertIsNone(resolved_car.engine)

    def test_resolve_optional_dependency_when_registered(self):
        # arrange
        class Engine:
            pass

        class Car:
            def __init__(self, engine: Optional[Engine] = None):
                self.engine = engine

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Engine)
        dependency_container.register_transient(Car)

        # act
        resolved_car = dependency_container.resolve(Car)

        # assert
        self.assertIsInstance(resolved_car.engine, Engine)
