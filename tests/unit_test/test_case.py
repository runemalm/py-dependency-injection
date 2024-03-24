from unittest import TestCase as TestCaseBase

from dependency_injection.container import DependencyContainer


class TestCase(TestCaseBase):
    def tearDown(self):
        super().tearDown()

        # Delete all singleton instances
        DependencyContainer._instances = {}
