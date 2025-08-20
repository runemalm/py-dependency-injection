import pytest
import warnings

from unit_test.unit_test_case import UnitTestCase
from dependency_injection import DependencyContainer


class TestRegisterDeprecations(UnitTestCase):
    def test_register_transient_dependency_alias_warns_and_works(self):
        # arrange
        class IFoo:
            pass

        class Foo(IFoo):
            pass

        dependency_container = DependencyContainer.get_instance()

        # act
        with pytest.warns(DeprecationWarning):
            dependency_container.register_transient(dependency=IFoo, implementation=Foo)
        resolved = dependency_container.resolve(IFoo)

        # assert
        self.assertIsInstance(resolved, Foo)

    def test_register_transient_constructor_args_alias_warns_and_works(self):
        # arrange
        class Foo:
            def __init__(self, x: int):
                self.x = x

        dependency_container = DependencyContainer.get_instance()

        # act
        with pytest.warns(DeprecationWarning):
            dependency_container.register_transient(Foo, constructor_args={"x": 123})
        obj = dependency_container.resolve(Foo)

        # assert
        self.assertEqual(123, obj.x)

    def test_register_transient_new_names_no_warning(self):
        # arrange
        class Foo:
            def __init__(self, x: int):
                self.x = x

        dependency_container = DependencyContainer.get_instance()

        # act
        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always", DeprecationWarning)
            dependency_container.register_transient(Foo, constructor_kwargs={"x": 1})

        obj = dependency_container.resolve(Foo)

        # assert
        dep_warnings = [w for w in rec if issubclass(w.category, DeprecationWarning)]
        self.assertEqual([], dep_warnings)
        self.assertEqual(1, obj.x)

    def test_register_scoped_dependency_alias_warns_and_works(self):
        # arrange
        class IService:
            pass

        class Service(IService):
            pass

        dependency_container = DependencyContainer.get_instance()

        # act
        with pytest.warns(DeprecationWarning):
            dependency_container.register_scoped(
                dependency=IService, implementation=Service
            )
        a1 = dependency_container.resolve(IService, scope_name="req-A")
        a2 = dependency_container.resolve(IService, scope_name="req-A")
        b1 = dependency_container.resolve(IService, scope_name="req-B")

        # assert
        self.assertIsInstance(a1, Service)
        self.assertIs(a1, a2)  # same scope -> same instance
        self.assertIsNot(a1, b1)  # different scope -> different instance

    def test_register_singleton_dependency_alias_warns_and_works(self):
        # arrange
        class IService:
            pass

        class Service(IService):
            pass

        dependency_container = DependencyContainer.get_instance()

        # act
        with pytest.warns(DeprecationWarning):
            dependency_container.register_singleton(
                dependency=IService, implementation=Service
            )
        s1 = dependency_container.resolve(IService)
        s2 = dependency_container.resolve(IService)

        # assert
        self.assertIs(s1, s2)

    def test_register_factory_factory_args_alias_warns_and_works(self):
        # arrange
        def build_cfg(*, env="prod"):
            return {"env": env}

        dependency_container = DependencyContainer.get_instance()

        # act
        with pytest.warns(DeprecationWarning):
            dependency_container.register_factory(
                dependency=dict, factory=build_cfg, factory_args={"env": "dev"}
            )
        cfg = dependency_container.resolve(dict)

        # assert
        self.assertEqual("dev", cfg["env"])

    def test_register_instance_dependency_alias_warns_and_works(self):
        # arrange
        class Foo:
            pass

        foo = Foo()
        dependency_container = DependencyContainer.get_instance()

        # act
        with pytest.warns(DeprecationWarning):
            dependency_container.register_instance(dependency=Foo, instance=foo)
        resolved = dependency_container.resolve(Foo)

        # assert
        self.assertIs(foo, resolved)

    def test_register_transient_unexpected_kw_raises_type_error(self):
        # arrange
        class Foo:
            pass

        dependency_container = DependencyContainer.get_instance()

        # act + assert
        with pytest.raises(TypeError):
            dependency_container.register_transient(Foo, unexpected_kw=1)
