from dataclasses import dataclass, replace
from typing import Any, Tuple
"""
This code is inspired by https://github.com/Adam-Vandervorst/Logics
"""


class LTLFormula:
    def __and__(self, other): return And(self, other)
    def __or__(self, other): return Or(self, other)
    def __invert__(self): return Not(self)
    def __gt__(self, other): return Then(self, other)

    def show(self) -> str:
        match self:
            case Top():
                return "True"
            case Bottom():
                return "False"
            case Var(s) as v:
                return f'\"{v.var_show()}\"'
            case Not(p):
                return f"!{p.show()}"
            case And(p, q):
                return f"({p.show()} & {q.show()})"
            case Or(p, q):
                return f"({p.show()} | {q.show()})"
            case Next(p):
                return f"X({p.show()})"
            case Until(p, q):
                return f"({p.show()} U {q.show()})"
            case Release(p, q):
                return f"({p.show()} R {q.show()})"
            case Then(p, q):
                return f"({p.show()} -> {q.show()})"
            case Iff(p, q):
                return f"({p.show()} <-> {q.show()})"
            case Finally(p, b):
                if not b: return f"F({p.show()})"
                else: return f"F[{b}]({p.show()})"
            case Globally(p):
                return f"G({p.show()})"
            case Weak(p, q):
                return f"({p.show()} WU {q.show()})"
            case Strong(p, q):
                return f"({p.show()} SU {q.show()})"
            case Previous(p):
                return f"Y({p.show()})"
            case Once(p, b):
                if not b: return f"O({p.show()})"
                else: return f"O[{b}]({p.show()})"

    def get_atoms(self) -> set[Any]:
        match self:
            case Var(s):
                return {s}
            case Nullary():
                return set()
            case Unary(p):
                return p.get_atoms()
            case Binary(p, q):
                return p.get_atoms() | q.get_atoms()

    def get_vars(self) -> set[Any]:
        match self:
            case Var(s) as v:
                return {v}
            case Nullary():
                return set()
            case Unary(p):
                return p.get_vars()
            case Binary(p, q):
                return p.get_vars() | q.get_vars()

    def replace(self, to_replace, replace_with):
        match self:
            case x if x == to_replace: return replace_with
            case Var(s) as v: return v  # return instance instead of constructing a new one, in case it is overridden
            case Nullary() as n: return n
            case Unary(p) as u: return replace(u, p=p.replace(to_replace, replace_with))
            case Binary(p, q) as b: return replace(b, l=p.replace(to_replace, replace_with), r=q.replace(to_replace, replace_with))


@dataclass
class Nullary(LTLFormula):
    pass


@dataclass
class Unary(LTLFormula):
    p: LTLFormula


@dataclass
class Binary(LTLFormula):
    l: LTLFormula
    r: LTLFormula


@dataclass(frozen=True, eq=True)
class Var(LTLFormula):
    data: Any

    def var_show(self) -> str:
        return f'{self.data}'


@dataclass
class Top(Nullary):
    pass


@dataclass
class Bottom(Nullary):
    pass


@dataclass
class Not(Unary):
    p: LTLFormula


@dataclass
class And(Binary):
    l: LTLFormula
    r: LTLFormula


@dataclass
class Or(Binary):
    l: LTLFormula
    r: LTLFormula


@dataclass
class Next(Unary):
    p: LTLFormula


@dataclass
class Until(Binary):
    l: LTLFormula
    r: LTLFormula


@dataclass
class Release(Binary):
    l: LTLFormula
    r: LTLFormula


@dataclass
class Finally(Unary):  # = Until(True, p)
    p: LTLFormula
    bound: Tuple[int, int] = None


@dataclass
class Globally(Unary):  # = Not(Finally(Not(p)))
    p: LTLFormula


@dataclass
class Weak(Binary):  # = Release(q, Or(p, q))
    l: LTLFormula
    r: LTLFormula


@dataclass
class Strong(Binary):  # = Until(q, And(p, q))
    l: LTLFormula
    r: LTLFormula


@dataclass
class Then(Binary):  # = Or(Not(p), q)
    l: LTLFormula
    r: LTLFormula


@dataclass
class Iff(Binary):  # = And(Then(p, q), Then(q, p))
    l: LTLFormula
    r: LTLFormula


@dataclass
class Previous(Unary):
    p: LTLFormula


@dataclass
class Once(Unary):
    p: LTLFormula
    bound: Tuple[int, int] = None


def test():
    print(Or(Not(Var('a')), Top()).show())
    print((~Var('a') | Top()).show())
    print(Or(Not(Var('a')), Top()).replace(Not(Var('a')), And(Var('a'), Var('b'))).show())
    print(Finally(Var('a'), (5, 5)).show())


if __name__ == '__main__':
    test()

