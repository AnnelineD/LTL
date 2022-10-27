import unittest
from syntax import *


class SyntaxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.f1 = Or(Finally(Var('a')), Top())
        self.f2 = Then(Var(1), Until(Var("b"), Or(Var("b"), Var(1))))

    def test_show(self):
        assert self.f1.show() == '(F("a") | True)'
        assert self.f2.show() == '("1" -> ("b" U ("b" | "1")))'

    def test_get_atoms(self):
        assert self.f1.get_atoms() == {'a'}
        assert self.f2.get_atoms() == {1, 'b'}


if __name__ == '__main__':
    unittest.main()
