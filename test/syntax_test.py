import unittest
from ltl.syntax import *


class SyntaxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.f1 = Or(Finally(Var('a')), Top())
        self.f2 = Then(Var(1), Until(Var("b"), Or(Var("b"), Var(1))))
        self.f3 = Next(And(Bottom(), Var('a')))

    def test_show(self):
        self.assertEqual('"a"', Var('a').show())
        self.assertEqual('(F("a") | True)', self.f1.show())
        assert self.f2.show() == '("1" -> ("b" U ("b" | "1")))'

    def test_get_atoms(self):
        assert self.f1.get_atoms() == {'a'}
        assert self.f2.get_atoms() == {1, 'b'}

    def test_get_vars(self):
        self.assertEqual({Var('a')}, self.f1.get_vars())
        self.assertEqual({Var(1), Var('b')}, self.f2.get_vars())

        @dataclass(frozen=True, eq=True)
        class IntVar(Var):
            data: int

        self.assertEqual({IntVar(5)}, IntVar(5).get_vars())

    def test_typed_variables(self):
        @dataclass(frozen=True, eq=True)
        class IntVar(Var):
            data: int

        i1 = Or(IntVar(1), IntVar(2))
        # print(Or(IntVar('a'), IntVar(2)).show())

    def test_replace(self):
        assert Var('a').replace(Var('a'), Var(1)) == Var(1)
        assert Not(Var('a')).replace(Var('a'), Var(1)) == Not(Var(1))
        assert self.f1.replace(Finally(Var('a')), Var(['a', 'b'])) == Or(Var(['a', 'b']), Top())
        assert And(Var('a'), Var('a')).replace(Var('a'), Top()) == And(Top(), Top())

    def test_dsl(self):
        assert Or(Not(Var('a')), Top()) == ~Var('a') | Top()
        assert self.f1 == Finally(Var('a')) | Top()
        assert self.f2 == (Var(1) > Until(Var("b"), Var("b") | Var(1)))
        assert self.f3 == Next(Bottom() & Var('a'))


if __name__ == '__main__':
    unittest.main()
