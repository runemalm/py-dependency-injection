from dependency_injection.container import DEFAULT_CONTAINER_NAME, DependencyContainer
from unit_test.unit_test_case import UnitTestCase


class TestObtainInstance(UnitTestCase):
    def test_obtain_instance_without_name_returns_default_container(
        self,
    ):
        # act
        dependency_container = DependencyContainer.get_instance()

        # assert
        self.assertIsNotNone(dependency_container)
        self.assertIsInstance(dependency_container, DependencyContainer)
        self.assertEqual(DEFAULT_CONTAINER_NAME, dependency_container.name)

    def test_obtain_instance_with_name_creates_and_returns_container(
        self,
    ):
        # act
        dependency_container = DependencyContainer.get_instance(name="second_container")

        # assert
        self.assertIsNotNone(dependency_container)
        self.assertIsInstance(dependency_container, DependencyContainer)
        self.assertEqual("second_container", dependency_container.name)

    def test_obtain_instance_with_name_second_time_returns_same_container(
        self,
    ):
        # act
        dependency_container = DependencyContainer.get_instance(name="second_container")
        dependency_container_in_second_call = DependencyContainer.get_instance(
            name="second_container"
        )

        # assert
        self.assertEqual(dependency_container, dependency_container_in_second_call)

    def test_obtain_using_two_different_names_return_two_different_instances(
        self,
    ):
        # act
        dependency_container_with_first_name = DependencyContainer.get_instance(
            name="first_container"
        )
        dependency_container_with_second_name = DependencyContainer.get_instance(
            name="second-container"
        )

        # assert
        self.assertNotEqual(
            dependency_container_with_first_name, dependency_container_with_second_name
        )
