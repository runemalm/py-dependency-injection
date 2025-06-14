from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveTransient(UnitTestCase):
    def test_resolve_transient_returns_an_instance(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        implementation = Car
        dependency_container.register_transient(dependency, implementation)

        # act
        resolved_dependency = dependency_container.resolve(dependency)

        # assert
        self.assertIsInstance(resolved_dependency, Car)

    def test_resolve_transient_twice_returns_different_instances(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        implementation = Car
        dependency_container.register_transient(dependency, implementation)

        # act
        resolved_dependency_1 = dependency_container.resolve(dependency)
        resolved_dependency_2 = dependency_container.resolve(dependency)

        # assert
        self.assertNotEqual(resolved_dependency_1, resolved_dependency_2)

    def test_returns_an_instance_when_registered_without_implementation_arg(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency = Vehicle
        dependency_container.register_transient(dependency)

        # act
        resolved_dependency = dependency_container.resolve(dependency)

        # assert
        self.assertIsInstance(resolved_dependency, Vehicle)
