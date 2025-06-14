import uuid
from dependency_injection.container import DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestConfigureDefaultContainer(UnitTestCase):
    def tearDown(self):
        # Reset after each test to avoid side effects
        DependencyContainer.clear_instances()
        DependencyContainer.configure_default_container_name("default_container")

    def test_configure_default_container_name_with_static_string(self):
        # arrange
        DependencyContainer.configure_default_container_name("custom_default")

        # act
        container = DependencyContainer.get_instance()

        # assert
        self.assertEqual(container.name, "custom_default")

    def test_configure_default_container_name_with_callable(self):
        # arrange
        container_name = f"test_{uuid.uuid4()}"
        DependencyContainer.configure_default_container_name(lambda: container_name)

        # act
        container = DependencyContainer.get_instance()

        # assert
        self.assertEqual(container.name, container_name)

    def test_get_instance_returns_different_container_when_default_is_changed(self):
        # arrange
        default_container = DependencyContainer.get_instance()
        DependencyContainer.configure_default_container_name("isolated")
        isolated_container = DependencyContainer.get_instance()

        # assert
        self.assertNotEqual(default_container, isolated_container)
        self.assertEqual(isolated_container.name, "isolated")

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
