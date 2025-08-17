from dataclasses import dataclass
from typing import List

from dependency_injection.container import DependencyContainer
from dependency_injection.tags.all_tagged import AllTagged
from dependency_injection.tags.any_tagged import AnyTagged
from dependency_injection.tags.tagged import Tagged
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
        resolved = dependency_container.resolve(Car)

        # assert
        self.assertIsInstance(resolved, Car)
        self.assertIsNotNone(resolved.engine)
        self.assertIsInstance(resolved.engine, Engine)

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
        resolved = dependency_container.resolve(Car)

        # assert
        self.assertIsInstance(resolved, Car)
        self.assertIsNone(resolved.engine)  # Should be None since injection is skipped

    def test_resolve_injects_tagged_dependencies(self):
        # arrange
        class HttpAdapter:
            pass

        class CliAdapter:
            pass

        class PrimaryPort:
            pass

        class PostgresCarRepository:
            pass

        class SecondaryPort:
            pass

        class Application:
            def __init__(self, primary_ports: List[Tagged[PrimaryPort]]):
                self.primary_ports = primary_ports

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(HttpAdapter, tags={PrimaryPort})
        dependency_container.register_transient(CliAdapter, tags={PrimaryPort})
        dependency_container.register_transient(
            PostgresCarRepository, tags={SecondaryPort}
        )
        dependency_container.register_transient(Application)

        # act
        resolved = dependency_container.resolve(Application)

        # assert
        self.assertIsInstance(resolved, Application)
        self.assertEqual(len(resolved.primary_ports), 2)
        self.assertTrue(any(isinstance(t, HttpAdapter) for t in resolved.primary_ports))
        self.assertTrue(any(isinstance(t, CliAdapter) for t in resolved.primary_ports))
        self.assertFalse(
            any(isinstance(t, PostgresCarRepository) for t in resolved.primary_ports)
        )

    def test_resolve_injects_any_tagged_dependencies(self):
        # arrange
        class Volvo:
            pass

        class Scania:
            pass

        class Car:
            pass

        class Truck:
            pass

        class Fruit:
            pass

        class Banana:
            pass

        class Trip:
            def __init__(self, transportations: List[AnyTagged[Car, Truck]]):
                self.transportations = transportations

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Volvo, tags={Car})
        dependency_container.register_transient(Scania, tags={Truck})
        dependency_container.register_transient(Banana, tags={Fruit})
        dependency_container.register_transient(Trip)

        # act
        resolved = dependency_container.resolve(Trip)

        # assert
        self.assertIsInstance(resolved, Trip)
        self.assertIsInstance(resolved, Trip)
        self.assertEqual(len(resolved.transportations), 2)
        self.assertTrue(any(isinstance(t, Volvo) for t in resolved.transportations))
        self.assertTrue(any(isinstance(t, Scania) for t in resolved.transportations))
        self.assertFalse(any(isinstance(t, Banana) for t in resolved.transportations))

    def test_resolve_injects_any_tagged_dependencies_when_single_tag(self):
        class PrimaryPort:
            pass

        class Http:
            pass

        class Cli:
            pass

        class App:
            def __init__(self, ports: List[AnyTagged[PrimaryPort]]):
                self.ports = ports

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Http, tags={PrimaryPort})
        dependency_container.register_transient(Cli, tags={PrimaryPort})
        dependency_container.register_transient(App)

        app = dependency_container.resolve(App)

        self.assertEqual(len(app.ports), 2)
        self.assertTrue(any(isinstance(p, Http) for p in app.ports))
        self.assertTrue(any(isinstance(p, Cli) for p in app.ports))

    def test_resolve_injects_all_tagged_dependencies(self):
        # arrange
        class Red:
            pass

        class Green:
            pass

        class Blue:
            pass

        class White:
            pass

        class NonWhite:
            pass

        class Palette:
            def __init__(self, white_colors: List[AllTagged[Red, Green, Blue]]):
                self.white_colors = white_colors

        # Register instances with various tags
        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(
            White, tags={Red, Green, Blue}
        )  # Should be included
        dependency_container.register_transient(
            NonWhite, tags={Red, Green}
        )  # Should NOT be included
        dependency_container.register_transient(Palette)

        # act
        resolved = dependency_container.resolve(Palette)

        # assert
        self.assertIsInstance(resolved, Palette)
        self.assertEqual(len(resolved.white_colors), 1)
        self.assertIsInstance(resolved.white_colors[0], White)
        self.assertNotIsInstance(resolved.white_colors[0], NonWhite)

    def test_resolve_injects_all_tagged_dependencies_when_single_tag(self):
        class PrimaryPort:
            pass

        class Http:
            pass

        class Cli:
            pass

        class App:
            def __init__(self, ports: List[AllTagged[PrimaryPort]]):
                self.ports = ports

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Http, tags={PrimaryPort})
        dependency_container.register_transient(Cli, tags={PrimaryPort})
        dependency_container.register_transient(App)

        app = dependency_container.resolve(App)

        self.assertEqual(len(app.ports), 2)
        self.assertTrue(any(isinstance(p, Http) for p in app.ports))
        self.assertTrue(any(isinstance(p, Cli) for p in app.ports))

    def test_resolve_injects_empty_list_if_no_tags_match(self):
        # arrange
        class PrimaryPort:
            pass

        class Application:
            def __init__(self, primary_ports: List[Tagged[PrimaryPort]]):
                self.primary_ports = primary_ports

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Application)

        # act
        resolved = dependency_container.resolve(Application)

        # assert
        self.assertIsInstance(resolved, Application)
        self.assertEqual(len(resolved.primary_ports), 0)
