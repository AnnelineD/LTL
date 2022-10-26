from dataclasses import dataclass
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


@dataclass
class Top(LTLFormula):
    pass


class Bottom(LTLFormula):
    pass


@dataclass
class Var(LTLFormula):
    name: str  #TODO this can be any type


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
    print(And(Finally(Var('a')), Top()).show())


if __name__ == '__main__':
    test()

