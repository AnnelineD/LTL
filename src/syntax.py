from dataclasses import dataclass
from typing import Any
"""
This code is inspired by https://github.com/Adam-Vandervorst/Logics
"""


class LTLFormula:
    def show(self) -> str:
        match self:
            case Top():
                return "True"
            case Bottom():
                return "False"
            case Var(s):
                return f"\"{s}\""
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
            case Finally(p):
                return f"F({p.show()})"
            case Globally(p):
                return f"G({p.show()})"
            case Weak(p, q):
                return f"({p.show()} WU {q.show()})"
            case Strong(p, q):
                return f"({p.show()} SU {q.show()})"

    def get_atoms(self) -> set[Any]:
        match self:
            case Top():
                return set()
            case Bottom():
                return set()
            case Var(s):
                return {s}
            case Not(p):
                return p.get_atoms()
            case And(p, q):
                return p.get_atoms() | q.get_atoms()
            case Or(p, q):
                return p.get_atoms() | q.get_atoms()
            case Next(p):
                return p.get_atoms()
            case Until(p, q):
                return p.get_atoms() | q.get_atoms()
            case Release(p, q):
                return p.get_atoms() | q.get_atoms()
            case Then(p, q):
                return p.get_atoms() | q.get_atoms()
            case Iff(p, q):
                return p.get_atoms() | q.get_atoms()
            case Finally(p):
                return p.get_atoms()
            case Globally(p):
                return p.get_atoms()
            case Weak(p, q):
                return p.get_atoms() | q.get_atoms()
            case Strong(p, q):
                return p.get_atoms() | q.get_atoms()

    def replace_var(self, to_replace, replace_with):
        match self:
            case Var(s) if Var(s) == to_replace: return replace_with
            case Var(s): return Var(s)
            case Top() | Bottom() as op: return op
            case Not(p): return Not(p.replace_var(to_replace, replace_with))
            case And(p, q): return And(p.replace_var(to_replace, replace_with), q.replace_var(to_replace, replace_with))
            case Or(p, q): return Or(p.replace_var(to_replace, replace_with), q.replace_var(to_replace, replace_with))
            case Next(p): return Next(p.replace_var(to_replace, replace_with))
            case Until(p, q): return Until(p.replace_var(to_replace, replace_with), q.replace_var(to_replace, replace_with))
            case Release(p, q): return Release(p.replace_var(to_replace, replace_with), q.replace_var(to_replace, replace_with))
            case Then(p, q): return Then(p.replace_var(to_replace, replace_with), q.replace_var(to_replace, replace_with))
            case Iff(p, q): return Iff(p.replace_var(to_replace, replace_with), q.replace_var(to_replace, replace_with))
            case Finally(p): return Finally(p.replace_var(to_replace, replace_with))
            case Globally(p): return Globally(p.replace_var(to_replace, replace_with))
            case Weak(p, q): return Weak(p.replace_var(to_replace, replace_with), q.replace_var(to_replace, replace_with))
            case Strong(p, q): return Strong(p.replace_var(to_replace, replace_with), q.replace_var(to_replace, replace_with))


@dataclass
class Top(LTLFormula):
    pass


@dataclass
class Bottom(LTLFormula):
    pass


@dataclass
class Var(LTLFormula):
    data: Any


@dataclass
class Not(LTLFormula):
    p: LTLFormula


@dataclass
class And(LTLFormula):
    l: LTLFormula
    r: LTLFormula


@dataclass
class Or(LTLFormula):
    l: LTLFormula
    r: LTLFormula


@dataclass
class Next(LTLFormula):
    p: LTLFormula


@dataclass
class Until(LTLFormula):
    l: LTLFormula
    r: LTLFormula


@dataclass
class Release(LTLFormula):
    l: LTLFormula
    r: LTLFormula


@dataclass
class Finally(LTLFormula):  # = Until(True, p)
    p: LTLFormula


@dataclass
class Globally(LTLFormula):  # = Not(Finally(Not(p)))
    p: LTLFormula


@dataclass
class Weak(LTLFormula):  # = Release(q, Or(p, q))
    l: LTLFormula
    r: LTLFormula


@dataclass
class Strong(LTLFormula):  # = Until(q, And(p, q))
    l: LTLFormula
    r: LTLFormula


@dataclass
class Then(LTLFormula):  # = Or(Not(p), q)
    l: LTLFormula
    r: LTLFormula


@dataclass
class Iff(LTLFormula):  # = And(Then(p, q), Then(q, p))
    l: LTLFormula
    r: LTLFormula


def test():
    print(Or(Not(Var('a')), Top()).show())
    print(Or(Not(Var('a')), Top()).replace_var(Var('a'), And(Var('a'), Var('b'))).show())


if __name__ == '__main__':
    test()

