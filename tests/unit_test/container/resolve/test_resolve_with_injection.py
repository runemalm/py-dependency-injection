from dataclasses import dataclass

from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveWithInjection(UnitTestCase):
    def test_resolve_injects_dependencies_in_constructor(
        self,
    ):
        # arrange
        class Engine:
            pass

        class Car:
            def __init__(self, engine: Engine):
                self.engine = engine

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Engine)
        dependency_container.register_transient(Car)

        # act
        resolved_dependency = dependency_container.resolve(Car)

        # assert
        self.assertIsInstance(resolved_dependency, Car)
        self.assertIsNotNone(resolved_dependency.engine)
        self.assertIsInstance(resolved_dependency.engine, Engine)

    def test_resolve_skips_constructor_injection_for_dataclass(self):
        # arrange
        class Engine:
            pass

        @dataclass
        class Car:
            engine: Engine = None

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Engine)
        dependency_container.register_transient(Car)

        # act
        resolved_dependency = dependency_container.resolve(Car)

        # assert
        self.assertIsInstance(resolved_dependency, Car)
        self.assertIsNone(
            resolved_dependency.engine
        )  # Should be None since injection is skipped
