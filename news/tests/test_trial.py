# news/tests/test_trial.py
import unittest
from django.test import TestCase


class Test(TestCase):

    def test_example_success(self):
        self.assertTrue(True)  # Этот тест всегда будет проходить успешно.


class YetAnotherTest(TestCase):

    def test_example_fails(self):
        self.assertTrue(False)  # Этот тест всегда будет проваливаться.


unittest.main()
