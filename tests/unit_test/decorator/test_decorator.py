import pytest

from dependency_injection import DependencyContainer, inject
from unit_test.unit_test_case import UnitTestCase


class TestDecorator(UnitTestCase):
    def test_decoration_on_class_method(self):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle
        implementation = Car

        dependency_container.register_transient(service, implementation)

        class Garage:
            vehicle: Vehicle

            @classmethod
            @inject()
            def park(cls, vehicle: Vehicle):
                cls.vehicle = vehicle

        # act
        Garage.park()

        # assert
        self.assertIsNotNone(Garage.vehicle)

    def test_decoration_on_static_method(self):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle
        implementation = Car

        dependency_container.register_transient(service, implementation)

        class Garage:
            vehicle: Vehicle

            @staticmethod
            @inject()
            def park(vehicle: Vehicle):
                Garage.vehicle = vehicle

        # act
        Garage.park()

        # assert
        self.assertIsNotNone(Garage.vehicle)

    def test_decoration_on_instance_method_raises(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        dependency_container = DependencyContainer.get_instance()
        service = Vehicle
        implementation = Car

        dependency_container.register_transient(service, implementation)

        with pytest.raises(
            TypeError,
            match="@inject decorator can only be applied to "
            "class methods or static methods.",
        ):

            class Garage:
                @inject()
                def park(self, vehicle: Vehicle):
                    pass

    def test_class_method_decorator_container_name_is_honoured(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        service = Vehicle
        implementation = Car

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_singleton(service, implementation)

        second_container = DependencyContainer.get_instance("second")
        second_container.register_singleton(service, implementation)

        second_container_vehicle = second_container.resolve(service)

        class Garage:
            vehicle: Vehicle

            @classmethod
            @inject(container_name="second")
            def park(cls, vehicle: Vehicle):
                cls.vehicle = vehicle

        # act
        Garage.park()

        # assert
        self.assertEqual(second_container_vehicle, Garage.vehicle)

    def test_class_method_decorator_scope_name_is_honoured(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        service = Vehicle
        implementation = Car

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_scoped(service, implementation)

        first_scope_vehicle = dependency_container.resolve(
            service, scope_name="first_scope"
        )
        second_scope_vehicle = dependency_container.resolve(
            service, scope_name="second_scope"
        )

        class Garage:
            first_vehicle: Vehicle
            second_vehicle: Vehicle

            @classmethod
            @inject(scope_name="first_scope")
            def park_first(cls, vehicle: Vehicle):
                cls.first_vehicle = vehicle

            @classmethod
            @inject(scope_name="second_scope")
            def park_second(cls, vehicle: Vehicle):
                cls.second_vehicle = vehicle

        # act
        Garage.park_first()
        Garage.park_second()

        # assert
        self.assertEqual(first_scope_vehicle, Garage.first_vehicle)
        self.assertEqual(second_scope_vehicle, Garage.second_vehicle)
        self.assertNotEqual(Garage.first_vehicle, Garage.second_vehicle)

    def test_static_method_decorator_container_name_is_honoured(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        service = Vehicle
        implementation = Car

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_singleton(service, implementation)

        second_container = DependencyContainer.get_instance("second")
        second_container.register_singleton(service, implementation)

        second_container_vehicle = second_container.resolve(service)

        class Garage:
            vehicle: Vehicle

            @staticmethod
            @inject(container_name="second")
            def park(vehicle: Vehicle):
                Garage.vehicle = vehicle

        # act
        Garage.park()

        # assert
        self.assertEqual(second_container_vehicle, Garage.vehicle)

    def test_static_method_decorator_scope_name_is_honoured(
        self,
    ):
        # arrange
        class Vehicle:
            pass

        class Car(Vehicle):
            pass

        service = Vehicle
        implementation = Car

        dependency_container = DependencyContainer.get_instance()
        dependency_container.register_scoped(service, implementation)

        first_scope_vehicle = dependency_container.resolve(
            service, scope_name="first_scope"
        )
        second_scope_vehicle = dependency_container.resolve(
            service, scope_name="second_scope"
        )

        class Garage:
            first_vehicle: Vehicle
            second_vehicle: Vehicle

            @staticmethod
            @inject(scope_name="first_scope")
            def park_first(vehicle: Vehicle):
                Garage.first_vehicle = vehicle

            @staticmethod
            @inject(scope_name="second_scope")
            def park_second(vehicle: Vehicle):
                Garage.second_vehicle = vehicle

        # act
        Garage.park_first()
        Garage.park_second()

        # assert
        self.assertEqual(first_scope_vehicle, Garage.first_vehicle)
        self.assertEqual(second_scope_vehicle, Garage.second_vehicle)
        self.assertNotEqual(Garage.first_vehicle, Garage.second_vehicle)
