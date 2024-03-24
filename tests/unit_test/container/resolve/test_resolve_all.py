from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveAll(UnitTestCase):
    def test_returns_dependency_with_tag(
        self,
    ):
        # arrange
        class Driveable:
            pass

        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Vehicle, Car, tags={Driveable})

        # act
        resolved_dependencies = dependency_container.resolve_all(tags={Driveable})

        # assert
        self.assertEqual(len(resolved_dependencies), 1)
        self.assertIsInstance(resolved_dependencies[0], Car)

    def test_returns_all_dependencies_with_tag(
        self,
    ):
        # arrange
        class Driveable:
            pass

        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        class Innovation:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Vehicle, tags={Driveable})
        dependency_container.register_transient(Car, tags={Driveable})
        dependency_container.register_transient(Innovation, tags={Driveable})

        # act
        resolved_dependencies = dependency_container.resolve_all(tags={Driveable})

        # assert
        self.assertEqual(len(resolved_dependencies), 3)
        self.assertTrue(
            any(isinstance(dependency, Vehicle) for dependency in resolved_dependencies)
        )
        self.assertTrue(
            any(isinstance(dependency, Car) for dependency in resolved_dependencies)
        )
        self.assertTrue(
            any(
                isinstance(dependency, Innovation)
                for dependency in resolved_dependencies
            )
        )

    def test_does_not_return_dependency_without_tag(
        self,
    ):
        # arrange
        class Driveable:
            pass

        class Refuelable:
            pass

        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        class Innovation:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Vehicle, tags={Driveable, Refuelable})
        dependency_container.register_transient(Car, tags={Driveable, Refuelable})
        dependency_container.register_transient(Innovation, tags={Driveable})

        # act
        resolved_dependencies = dependency_container.resolve_all(tags={Refuelable})

        # assert
        self.assertEqual(len(resolved_dependencies), 2)
        self.assertTrue(
            any(isinstance(dependency, Vehicle) for dependency in resolved_dependencies)
        )
        self.assertTrue(
            any(isinstance(dependency, Car) for dependency in resolved_dependencies)
        )

    def test_returns_all_dependencies_when_no_tag_specified(
        self,
    ):
        # arrange
        class Driveable:
            pass

        class Refuelable:
            pass

        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        class Innovation:
            pass

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_transient(Vehicle, tags={Driveable, Refuelable})
        dependency_container.register_transient(Car, tags={Driveable, Refuelable})
        dependency_container.register_transient(Innovation, tags={Driveable})

        # act
        resolved_dependencies = dependency_container.resolve_all()

        # assert
        self.assertEqual(len(resolved_dependencies), 3)
        self.assertTrue(
            any(isinstance(dependency, Vehicle) for dependency in resolved_dependencies)
        )
        self.assertTrue(
            any(isinstance(dependency, Car) for dependency in resolved_dependencies)
        )
        self.assertTrue(
            any(
                isinstance(dependency, Innovation)
                for dependency in resolved_dependencies
            )
        )
