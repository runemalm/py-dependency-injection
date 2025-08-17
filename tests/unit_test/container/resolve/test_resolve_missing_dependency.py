import pytest
from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestResolveMissingDependency(UnitTestCase):
    def test_required_dependency_not_registered_raises(self):
        # arrange
        class Engine:
            pass

        class Car:
            def __init__(self, engine: Engine):
                self.engine = engine

        dependency_container = DependencyContainer.get_instance()
        # Register Car only; Engine is NOT registered
        dependency_container.register_transient(Car, Car)

        # act
        with pytest.raises(ValueError) as e:
            dependency_container.resolve(Car)

        # assert
        msg = str(e.value)
        self.assertIn("Cannot resolve service for parameter 'engine'", msg)
        self.assertIn("in class 'Car'", msg)
