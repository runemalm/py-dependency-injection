from typing import List, Optional
from unit_test.unit_test_case import UnitTestCase
from dependency_injection import DependencyContainer, AllTagged, AnyTagged, Tagged


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

    def test_resolve_optional_tagged_dependency_with_empty_list_when_no_matches(self):
        # arrange
        class PrimaryPort:
            pass

        class App:
            def __init__(self, ports: Optional[List[Tagged[PrimaryPort]]]):
                self.ports = ports

        c = DependencyContainer.get_instance()
        c.register_transient(App)

        # act
        app = c.resolve(App)

        # assert
        self.assertIsInstance(app, App)
        self.assertEqual(app.ports, [])

    def test_resolve_optional_tagged_dependency_with_items_when_matches(self):
        # arrange
        class PrimaryPort:
            pass

        class Http:
            pass

        class Cli:
            pass

        class App:
            def __init__(self, ports: Optional[List[Tagged[PrimaryPort]]]):
                self.ports = ports

        c = DependencyContainer.get_instance()
        c.register_transient(Http, tags={PrimaryPort})
        c.register_transient(Cli, tags={PrimaryPort})
        c.register_transient(App)

        # act
        app = c.resolve(App)

        # assert
        self.assertEqual(len(app.ports), 2)
        self.assertTrue(any(isinstance(p, Http) for p in app.ports))
        self.assertTrue(any(isinstance(p, Cli) for p in app.ports))

    def test_resolve_optional_anytagged_dependency_with_empty_list_when_no_matches(
        self,
    ):
        # arrange
        class A:
            pass

        class B:
            pass

        class App:
            def __init__(self, items: Optional[List[AnyTagged[A, B]]]):
                self.items = items

        c = DependencyContainer.get_instance()
        c.register_transient(App)

        # act
        app = c.resolve(App)

        # assert
        self.assertEqual(app.items, [])

    def test_resolve_optional_anytagged_dependency_with_items_when_matches(self):
        # arrange
        class A:
            pass

        class B:
            pass

        class X:
            pass

        class Y:
            pass

        class App:
            def __init__(self, items: Optional[List[AnyTagged[A, B]]]):
                self.items = items

        c = DependencyContainer.get_instance()
        c.register_transient(X, tags={A})
        c.register_transient(Y, tags={B})
        c.register_transient(App)

        # act
        app = c.resolve(App)

        # assert
        self.assertEqual(len(app.items), 2)
        self.assertTrue(any(isinstance(i, X) for i in app.items))
        self.assertTrue(any(isinstance(i, Y) for i in app.items))

    def test_resolve_optional_alltagged_dependency_with_empty_list_when_no_matches(
        self,
    ):
        # arrange
        class Red:
            pass

        class Green:
            pass

        class App:
            def __init__(self, items: Optional[List[AllTagged[Red, Green]]]):
                self.items = items

        c = DependencyContainer.get_instance()
        c.register_transient(App)

        # act
        app = c.resolve(App)

        # assert
        self.assertIsInstance(app, App)
        self.assertEqual(app.items, [])

    def test_resolve_optional_alltagged_dependency_with_items_when_matches(self):
        # arrange
        class Red:
            pass

        class Green:
            pass

        class Blue:
            pass

        class A:
            pass

        class B:
            pass

        class C:
            pass

        class App:
            def __init__(self, items: Optional[List[AllTagged[Red, Green]]]):
                self.items = items

        c = DependencyContainer.get_instance()
        c.register_transient(A, tags={Red, Green})
        c.register_transient(B, tags={Red, Green, Blue})
        c.register_transient(C, tags={Red})  # missing Green
        c.register_transient(App)

        # act
        app = c.resolve(App)

        # assert
        self.assertEqual(len(app.items), 2)
        self.assertTrue(any(isinstance(i, A) for i in app.items))
        self.assertTrue(any(isinstance(i, B) for i in app.items))
        self.assertFalse(any(isinstance(i, C) for i in app.items))
