from dependency_injection.container import DependencyContainer
from dependency_injection.decorator import inject
from unit_test.car import Car
from unit_test.unit_test_case import UnitTestCase
from unit_test.vehicle import Vehicle


class TestDecorator(UnitTestCase):

    def test_injects_dependencies_into_method_signature(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car

        dependency_container.register_transient(interface, dependency_class)

        # act
        foo = Foo()
        foo.bar_1()

        # assert
        self.assertIsNotNone(foo.vehicle_1)
        self.assertIsInstance(foo.vehicle_1, Vehicle)

    def test_injects_dependencies_from_different_scopes_correctly(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car

        dependency_container.register_scoped(interface, dependency_class)

        # act
        foo = Foo()
        foo.bar_1()
        foo.bar_2()

        # assert
        self.assertIsNotNone(foo.vehicle_1)
        self.assertIsNotNone(foo.vehicle_2)
        self.assertNotEqual(foo.vehicle_1, foo.vehicle_2)

class Foo:
    def __init__(self):
        self.vehicle_1 = None
        self.vehicle_2 = None

    @inject(container=DependencyContainer.get_instance(), scope_name="test-scope-1")
    def bar_1(self, vehicle: Vehicle):
        self.vehicle_1 = vehicle

    @inject(container=DependencyContainer.get_instance(), scope_name="test-scope-2")
    def bar_2(self, vehicle: Vehicle):
        self.vehicle_2 = vehicle
