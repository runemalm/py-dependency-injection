from dependency_injection import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestClearInstances(UnitTestCase):
    def tearDown(self):
        DependencyContainer.clear_instances()

    def test_clear_instances_removes_all_containers(self):
        # arrange
        c1 = DependencyContainer.get_instance("a")
        c2 = DependencyContainer.get_instance("b")

        # act
        DependencyContainer.clear_instances()

        # assert
        c1_new = DependencyContainer.get_instance("a")
        c2_new = DependencyContainer.get_instance("b")

        self.assertNotEqual(c1, c1_new)
        self.assertNotEqual(c2, c2_new)
