"""Self-grading exercises for lesson 03. Implement each TODO, then run this file."""

from itertools import product


def truth_table(formula):
    """Exercise 1 (easy): return the truth table of a 2-variable formula.

    `formula` is a callable taking keyword args P and Q. Return a list of
    (P, Q, result) tuples for all four assignments, in this order:
    (F,F), (F,T), (T,F), (T,T).
    """
    raise NotImplementedError


def is_tautology(formula):
    """Exercise 2a (medium): True iff the formula is true under EVERY assignment."""
    raise NotImplementedError


def is_contradiction(formula):
    """Exercise 2b (medium): True iff the formula is false under EVERY assignment."""
    raise NotImplementedError


def satisfiable(formula):
    """Exercise 2c (medium): True iff SOME assignment makes the formula true."""
    raise NotImplementedError


def equivalent(f, g):
    """Exercise 3 (hard): True iff f and g have identical truth tables.

    Build both tables with your truth_table and compare. This is the lesson's
    equivalence checker — implemented, not imported.
    """
    raise NotImplementedError


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"{status}  {name}{(' — ' + detail) if detail and not condition else ''}")
    return condition


def implies(p, q):
    return (not p) or q


def xor(p, q):
    return p != q


def main():
    ok = True

    try:
        rows = truth_table(lambda P, Q: P and Q)
        want = [(False, False, False), (False, True, False),
                (True, False, False), (True, True, True)]
        ok &= check("ex1 truth_table(P and Q) rows", rows == want, f"got {rows}")
        rows_or = truth_table(lambda P, Q: P or Q)
        ok &= check("ex1 truth_table(P or Q) last row True",
                    rows_or[-1] == (True, True, True), f"got {rows_or[-1]}")
    except NotImplementedError:
        ok = False
        print("FAIL  ex1 truth_table — not implemented yet")

    try:
        ok &= check("ex2a P or (not P) is a tautology",
                    is_tautology(lambda P, Q: P or (not P)) is True)
        ok &= check("ex2a P and Q is NOT a tautology",
                    is_tautology(lambda P, Q: P and Q) is False)
        ok &= check("ex2b P and (not P) is a contradiction",
                    is_contradiction(lambda P, Q: P and (not P)) is True)
        ok &= check("ex2c xor is satisfiable",
                    satisfiable(xor) is True)
        ok &= check("ex2c P and (not P) is not satisfiable",
                    satisfiable(lambda P, Q: P and (not P)) is False)
    except NotImplementedError:
        ok = False
        print("FAIL  ex2 tautology/contradiction/satisfiable — not implemented yet")

    try:
        ok &= check("ex3 De Morgan: not(P or Q) == not P and not Q",
                    equivalent(lambda P, Q: not (P or Q),
                               lambda P, Q: (not P) and (not Q)) is True)
        ok &= check("ex3 P -> Q == (not P) or Q",
                    equivalent(implies, lambda P, Q: (not P) or Q) is True)
        ok &= check("ex3 contrapositive: P -> Q == not Q -> not P",
                    equivalent(implies, lambda P, Q: (not Q) or P) is True)
        ok &= check("ex3 converse correctly NOT equivalent",
                    equivalent(implies, lambda P, Q: (not P) or Q) is False)
    except NotImplementedError:
        ok = False
        print("FAIL  ex3 equivalent — not implemented yet")

    print()
    if ok:
        print("ALL EXERCISES COMPLETE — you have built and used a complete proof checker.")
    else:
        print("Not done yet — fix the FAIL lines above and re-run.")


if __name__ == "__main__":
    main()
