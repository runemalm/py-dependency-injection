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

    def test_injects_using_default_container_and_scope_if_omitted_in_decorator_arguments(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car

        dependency_container.register_scoped(interface, dependency_class)

        # act
        foo = Foo()
        foo.bar_3()

        # assert
        self.assertIsNotNone(foo.vehicle_3)
        self.assertIsInstance(foo.vehicle_3, Vehicle)

    def test_injects_same_scoped_dependency_when_no_container_or_scope_name_in_decorator_arguments(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car

        dependency_container.register_scoped(interface, dependency_class)

        # act
        foo = Foo()
        foo.bar_3()
        foo.bar_4()

        # assert
        self.assertIsNotNone(foo.vehicle_3)
        self.assertIsNotNone(foo.vehicle_4)
        self.assertEqual(foo.vehicle_3, foo.vehicle_4)

    def test_injects_different_scoped_dependencies_when_no_container_but_different_scope_names_in_decorator_arguments(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car

        dependency_container.register_scoped(interface, dependency_class)

        # act
        foo = Foo()
        foo.bar_5()
        foo.bar_6()

        # assert
        self.assertIsNotNone(foo.vehicle_5)
        self.assertIsNotNone(foo.vehicle_6)
        self.assertNotEqual(foo.vehicle_5, foo.vehicle_6)

class Foo:
    def __init__(self):
        self.vehicle_1 = None
        self.vehicle_2 = None
        self.vehicle_3 = None
        self.vehicle_4 = None
        self.vehicle_5 = None
        self.vehicle_6 = None

    @inject(container=DependencyContainer.get_instance(), scope_name="test-scope-1")
    def bar_1(self, vehicle: Vehicle):
        self.vehicle_1 = vehicle

    @inject(container=DependencyContainer.get_instance(), scope_name="test-scope-2")
    def bar_2(self, vehicle: Vehicle):
        self.vehicle_2 = vehicle

    @inject()
    def bar_3(self, vehicle: Vehicle):
        self.vehicle_3 = vehicle

    @inject()
    def bar_4(self, vehicle: Vehicle):
        self.vehicle_4 = vehicle

    @inject(scope_name="scope-5")
    def bar_5(self, vehicle: Vehicle):
        self.vehicle_5 = vehicle

    @inject(scope_name="scope-6")
    def bar_6(self, vehicle: Vehicle):
        self.vehicle_6 = vehicle
