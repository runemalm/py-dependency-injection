import pytest

from dependency_injection.container import DependencyContainer
from unit_test.car import Car
from unit_test.unit_test_case import UnitTestCase
from unit_test.vehicle import Vehicle


class TestRegisterSingleton(UnitTestCase):

    def test_register_singleton_succeeds_when_not_previously_registered(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car

        # act
        dependency_container.register_singleton(interface, dependency_class)

        # assert
        # (no exception thrown)

    def test_register_singleton_fails_when_already_registered(
        self,
    ):
        # arrange
        dependency_container = DependencyContainer.get_instance()
        interface = Vehicle
        dependency_class = Car
        dependency_container.register_singleton(interface, dependency_class)

        # act + assert
        with pytest.raises(ValueError, match="is already registered"):
            dependency_container.register_singleton(interface, dependency_class)
