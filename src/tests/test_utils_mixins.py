from unittest import TestCase

from utils.mixins import SingletonMixin


class SingletonTestClass(SingletonMixin):
    def __init__(self, val):
        self.val = val


class SingletonTestClassChild(SingletonTestClass):
    pass


class TestSingletonMixin(TestCase):
    def test_instances_equal(self):
        instance1 = SingletonTestClass(5)
        instance2 = SingletonTestClass(7)

        self.assertEqual(instance1, instance2)
        self.assertEqual(instance2.val, 5)

    def test_child_instances_equal(self):
        child_instance1 = SingletonTestClassChild(3)
        child_instance2 = SingletonTestClassChild(8)

        self.assertEqual(child_instance1, child_instance2)
        self.assertEqual(child_instance2.val, 3)
