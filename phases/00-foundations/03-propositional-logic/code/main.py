from itertools import product


def variables(formula):
    return sorted(formula.__code__.co_varnames)


def assignments(vars_):
    for bits in product([False, True], repeat=len(vars_)):
        yield dict(zip(vars_, bits))


def truth_table(formula):
    rows = []
    for a in assignments(variables(formula)):
        rows.append((tuple(sorted(a.items())), formula(**a)))
    rows.sort()
    return rows


def equivalent(f, g):
    return truth_table(f) == truth_table(g)


def check(name, f, g):
    assert equivalent(f, g), f"NOT equivalent: {name}"
    print(f"PASS  {name}")


def check_distinct(name, f, g):
    assert not equivalent(f, g), f"unexpectedly equivalent: {name}"
    print(f"PASS  {name} (correctly distinct)")


def check_de_morgan_or():
    check("De Morgan: not(P or Q) == (not P) and (not Q)", lambda P, Q: not (P or Q),
          lambda P, Q: (not P) and (not Q))


def check_de_morgan_and():
    check("De Morgan: not(P and Q) == (not P) or (not Q)", lambda P, Q: not (P and Q),
          lambda P, Q: (not P) or (not Q))


def implies(p, q):
    return (not p) or q


def check_implication_rewrites():
    check("P -> Q == (not P) or Q", implies, lambda P, Q: (not P) or Q)
    check("contrapositive: P -> Q == (not Q) -> (not P)", implies,
          lambda P, Q: Q or (not P))


def check_converse_is_not_equivalent():
    check_distinct("converse: P -> Q  vs  Q -> P", implies, lambda P, Q: (not Q) or P)


def check_billing_condition():
    check("billing: not (expired or unpaid) == not expired and not unpaid",
          lambda expired, unpaid: not (expired or unpaid),
          lambda expired, unpaid: (not expired) and (not unpaid))


def count_binary_connectives():
    outputs = set()
    for bits in product([False, True], repeat=4):
        table = frozenset({(p, q): r for (p, q), r in zip(product([False, True], repeat=2), bits)}.items())
        outputs.add(table)
    assert len(outputs) == 16, f"expected 16 distinct connectives, got {len(outputs)}"
    print(f"PASS  exactly {len(outputs)} distinct binary connectives exist")


if __name__ == "__main__":
    check_de_morgan_or()
    check_de_morgan_and()
    check_implication_rewrites()
    check_converse_is_not_equivalent()
    check_billing_condition()
    count_binary_connectives()
