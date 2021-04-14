import unittest

from janggi.utils import algebraic_to_numeric, numeric_to_algebraic


class TestBoard(unittest.TestCase):
    def test_algebraic_to_numeric(self):
        alg1 = "a1"
        alg2 = "e5"
        alg3 = "d10"
        self.assertEqual((0, 0), algebraic_to_numeric(alg1))
        self.assertEqual((4, 4), algebraic_to_numeric(alg2))
        self.assertEqual((9, 3), algebraic_to_numeric(alg3))

    def test_numeric_to_algebraic(self):
        num1 = (0, 0)
        num2 = (4, 4)
        num3 = (9, 3)
        self.assertEqual("a1", numeric_to_algebraic(num1))
        self.assertEqual("e5", numeric_to_algebraic(num2))
        self.assertEqual("d10", numeric_to_algebraic(num3))
