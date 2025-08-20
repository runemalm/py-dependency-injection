from dependency_injection import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestConfigureDefaultScopeName(UnitTestCase):
    def test_scoped_same_within_configured_default_scope_string(self):
        # arrange
        DependencyContainer.configure_default_scope_name("alpha")

        class Svc:
            pass

        c = DependencyContainer.get_instance()
        c.register_scoped(Svc, Svc)

        # act
        a1 = c.resolve(Svc)
        a2 = c.resolve(Svc)

        # assert
        self.assertIs(a1, a2)

    def test_scoped_new_instance_after_default_scope_string_changes(self):
        # arrange
        DependencyContainer.configure_default_scope_name("alpha")

        class Svc:
            pass

        c = DependencyContainer.get_instance()
        c.register_scoped(Svc, Svc)
        a1 = c.resolve(Svc)
        DependencyContainer.configure_default_scope_name("beta")

        # act
        b1 = c.resolve(Svc)

        # assert
        self.assertIsNot(b1, a1)

    def test_scoped_old_instance_still_resolvable_via_explicit_old_scope(self):
        # arrange
        DependencyContainer.configure_default_scope_name("alpha")

        class Svc:
            pass

        c = DependencyContainer.get_instance()
        c.register_scoped(Svc, Svc)
        a1 = c.resolve(Svc)
        DependencyContainer.configure_default_scope_name("beta")  # switch default

        # act
        a2 = c.resolve(Svc, scope_name="alpha")

        # assert
        self.assertIs(a2, a1)

    def test_scoped_same_when_default_scope_callable_returns_same_value(self):
        # arrange
        def scope_a():
            return "scope-a"

        DependencyContainer.configure_default_scope_name(scope_a)

        class Repo:
            pass

        c = DependencyContainer.get_instance()
        c.register_scoped(Repo, Repo)

        # act
        r1 = c.resolve(Repo)
        r2 = c.resolve(Repo)

        # assert
        self.assertIs(r1, r2)

    def test_scoped_new_instance_after_switching_default_scope_callable(self):
        # arrange
        def scope_a():
            return "scope-a"

        def scope_b():
            return "scope-b"

        DependencyContainer.configure_default_scope_name(scope_a)

        class Repo:
            pass

        c = DependencyContainer.get_instance()
        c.register_scoped(Repo, Repo)
        r_a = c.resolve(Repo)
        DependencyContainer.configure_default_scope_name(scope_b)

        # act
        r_b = c.resolve(Repo)

        # assert
        self.assertIsNot(r_b, r_a)
