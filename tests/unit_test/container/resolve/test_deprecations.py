import pytest
import warnings
from unit_test.unit_test_case import UnitTestCase
from dependency_injection import DependencyContainer


class TestResolveDeprecations(UnitTestCase):
    def test_resolve_dependency_alias_warns_and_works(self):
        # arrange
        class Foo:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Foo)

        # act
        with pytest.warns(DeprecationWarning):
            obj = dependency_container.resolve(dependency=Foo)

        # assert
        self.assertIsInstance(obj, Foo)

    def test_resolve_new_name_no_warning(self):
        # arrange
        class Foo:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Foo)

        # act
        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always", DeprecationWarning)
            obj = dependency_container.resolve(service=Foo)

        # assert
        dep_warnings = [w for w in rec if issubclass(w.category, DeprecationWarning)]
        self.assertEqual([], dep_warnings)
        self.assertIsInstance(obj, Foo)
