"""Self-grading exercises for lesson 04. Implement each TODO, then run this file."""

import random


def negate_universal(domain, predicate):
    """Exercise 1a (easy): compute NOT(for_all(domain, predicate)) WITHOUT calling for_all.

    Use the negation rule: flip the quantifier and negate the predicate.
    Return a bool.
    """
    raise NotImplementedError


def negate_existential(domain, predicate):
    """Exercise 1b (easy): compute NOT(exists(domain, predicate)) WITHOUT calling exists.

    Negation rule: all elements must fail the predicate. Return a bool.
    """
    raise NotImplementedError


def exists_unique(domain, predicate):
    """Exercise 2 (medium): True iff EXACTLY ONE element of `domain` satisfies `predicate`."""
    raise NotImplementedError


def exists_unique_formula(domain, predicate):
    """Exercise 2 (medium): the SAME claim written as the formula
    exists x. (P(x) and for all y. (P(y) -> y == x)).

    Implement it directly from the formula — do not call exists_unique.
    """
    raise NotImplementedError


def validate_rows(rows, rule, rule_name):
    """Exercise 3 (hard): return the list of rows FAILING `rule` — the witnesses.

    `rule` takes a row dict and returns True when the row is VALID.
    Return failing rows in their original order.
    """
    raise NotImplementedError


def for_all(domain, predicate):
    for x in domain:
        if not predicate(x):
            return False
    return True


def exists(domain, predicate):
    for x in domain:
        if predicate(x):
            return True
    return False


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"{status}  {name}{(' — ' + detail) if detail and not condition else ''}")
    return condition


def random_predicate(rng):
    threshold = rng.randint(-3, 3)
    mod = rng.randint(1, 3)
    mode = rng.choice(["gt", "mod", "and"])
    if mode == "gt":
        return lambda x: x > threshold
    if mode == "mod":
        return lambda x: x % mod == 0
    return lambda x: x > threshold and x % mod == 0


def main():
    ok = True
    rng = random.Random(2026)

    try:
        sweep_ok = True
        for _ in range(30):
            domain = [rng.randint(-5, 5) for _ in range(rng.randint(0, 7))]
            p = random_predicate(rng)
            if negate_universal(domain, p) != (not for_all(domain, p)):
                sweep_ok = False
            if negate_existential(domain, p) != (not exists(domain, p)):
                sweep_ok = False
        ok &= check("ex1 negation rules agree with direct negation (30 random sweeps)",
                    sweep_ok)
    except NotImplementedError:
        ok = False
        print("FAIL  ex1 negate_universal / negate_existential — not implemented yet")

    try:
        domain = list(range(10))
        ok &= check("ex2 exists_unique: x*x == 49 has exactly one solution",
                    exists_unique(domain, lambda x: x * x == 49) is True)
        ok &= check("ex2 exists_unique: x % 5 == 0 has two solutions",
                    exists_unique(domain, lambda x: x % 5 == 0) is False)
        formula_agrees = all(
            exists_unique(domain, p) == exists_unique_formula(domain, p)
            for p in [lambda x: x * x == 49, lambda x: x % 5 == 0,
                      lambda x: x > 100, lambda x: x < 3]
        )
        ok &= check("ex2 implementation matches the formula version", formula_agrees)
    except NotImplementedError:
        ok = False
        print("FAIL  ex2 exists_unique — not implemented yet")

    try:
        rows = [
            {"id": 1, "email": "a@x.com", "age": 34},
            {"id": 2, "email": "", "age": 29},
            {"id": 3, "email": "c@x.com", "age": None},
            {"id": 4, "email": "d@x.com", "age": 41},
            {"id": 5, "email": None, "age": 25},
        ]
        rule = lambda row: bool(row.get("email")) and row.get("age") is not None
        expected = [row for row in rows if not rule(row)]
        got = validate_rows(rows, rule, "valid email and age")
        ok &= check("ex3 validate_rows finds exactly the failing rows",
                    got == expected, f"got {got}, expected {expected}")
        ok &= check("ex3 witness count matches the lesson's claim",
                    len(got) == 2, f"got {len(got)}")
    except NotImplementedError:
        ok = False
        print("FAIL  ex3 validate_rows — not implemented yet")

    print()
    if ok:
        print("ALL EXERCISES COMPLETE — quantifiers are now working tools in your toolkit.")
    else:
        print("Not done yet — fix the FAIL lines above and re-run.")


if __name__ == "__main__":
    main()
