from unittest import TestCase as TestCaseBase

from dependency_injection.container.container import DependencyContainer


class TestCase(TestCaseBase):

    def tearDown(self):
        super().tearDown()
        if DependencyContainer in DependencyContainer._instances:
            del DependencyContainer._instances[DependencyContainer]
