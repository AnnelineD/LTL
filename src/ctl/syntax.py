from dataclasses import dataclass, replace
from typing import Any, Tuple

class CTLFormula:
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
            case AX(p):
                return f"AX({p.show()})"
            case EX(p):
                return f"EX({p.show()})"
            case Then(p, q):
                return f"({p.show()} -> {q.show()})"
            case Iff(p, q):
                return f"({p.show()} <-> {q.show()})"
            case AF(p, b):
                if not b: return f"AF({p.show()})"
                else: return f"AF[{b}]({p.show()})"
            case EF(p, b):
                if not b: return f"EF({p.show()})"
                else: return f"EF[{b}]({p.show()})"
            case AG(p):
                return f"AG({p.show()})"
            case EG(p):
                return f"EG({p.show()})"


    def get_atoms(self) -> set[any]:
        match self:
            case Var(s):
                return {s}
            case Nullary():
                return set()
            case Unary(p):
                return p.get_atoms()
            case Binary(p, q):
                return p.get_atoms() | q.get_atoms()

    def get_vars(self) -> set[any]:
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
class Nullary(CTLFormula):
    pass


@dataclass
class Unary(CTLFormula):
    p: CTLFormula


@dataclass
class Binary(CTLFormula):
    l: CTLFormula
    r: CTLFormula


@dataclass(frozen=True, eq=True)
class Var(CTLFormula):
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
    p: CTLFormula


@dataclass
class And(Binary):
    l: CTLFormula
    r: CTLFormula


@dataclass
class Or(Binary):
    l: CTLFormula
    r: CTLFormula


@dataclass
class AX(Unary):
    p: CTLFormula


@dataclass
class EX(Unary):
    p: CTLFormula


@dataclass
class AF(Unary):  # = Until(True, p)
    p: CTLFormula
    bound: Tuple[int, int] = None

@dataclass
class EF(Unary):  # = Until(True, p)
    p: CTLFormula
    bound: Tuple[int, int] = None


@dataclass
class AG(Unary):
    p: CTLFormula


@dataclass
class EG(Unary):
    p: CTLFormula


@dataclass
class Then(Binary):  # = Or(Not(p), q)
    l: CTLFormula
    r: CTLFormula


@dataclass
class Iff(Binary):  # = And(Then(p, q), Then(q, p))
    l: CTLFormula
    r: CTLFormula


def test():
    print(Or(Not(Var('a')), Top()).show())
    print((~Var('a') | Top()).show())
    print(Or(Not(Var('a')), Top()).replace(Not(Var('a')), And(Var('a'), Var('b'))).show())
    print(EF(Var('a'), (5, 5)).show())


if __name__ == '__main__':
    test()

