"""Self-grading exercises for lesson 02. Implement each TODO, then run this file."""


def power_set(u):
    """Exercise 1 (easy): return ALL subsets of `u` as a list of frozensets.

    No itertools. Build up from the empty set: for each element, double the
    collection by adding copies that include it.
    """
    raise NotImplementedError


def symdiff(a, b):
    """Exercise 2 (medium): symmetric difference using ONLY membership tests.

    Allowed: `in`, loops, building result sets element by element.
    Forbidden: -, ^, |, &, symmetric_difference.
    Return a plain set.
    """
    raise NotImplementedError


def is_subset(a, b):
    """Exercise 3a (hard): return True iff every member of `a` is a member of `b`.

    Membership tests only — no <= or issubset.
    """
    raise NotImplementedError


def set_eq(a, b):
    """Exercise 3b (hard): decide equality by DOUBLE INCLUSION, using your is_subset.

    This is the proof technique from the lesson, executed as code.
    """
    raise NotImplementedError


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"{status}  {name}{(' — ' + detail) if detail and not condition else ''}")
    return condition


def all_subsets(u):
    result = [frozenset()]
    for size in range(1, len(u) + 1):
        from itertools import combinations
        result.extend(frozenset(c) for c in combinations(u, size))
    return result


def main():
    ok = True
    u = frozenset(range(4))
    subs = all_subsets(sorted(u))

    try:
        got = power_set([1, 2, 3, 4])
        got_norm = sorted(map(frozenset, map(set, got)))
        want_norm = sorted(subs)
        ok &= check("ex1 power_set count == 16", len(got) == 16, f"got {len(got)}")
        ok &= check("ex1 power_set contents match brute force",
                    got_norm == want_norm and len(got_norm) == len(set(got_norm)))
    except NotImplementedError:
        ok = False
        print("FAIL  ex1 power_set — not implemented yet")

    try:
        mismatch = None
        for a in subs:
            for b in subs:
                if set(symdiff(a, b)) != (a ^ b):
                    mismatch = (a, b, symdiff(a, b), a ^ b)
                    break
        ok &= check("ex2 symdiff matches ^ over all 256 subset pairs", mismatch is None,
                    f"mismatch at {mismatch}")
    except NotImplementedError:
        ok = False
        print("FAIL  ex2 symdiff — not implemented yet")

    try:
        cases = [
            (frozenset({1, 2}), frozenset({1, 2, 3}), True),
            (frozenset(), frozenset({1}), True),
            (frozenset({1, 2, 3}), frozenset({1, 2}), False),
            (frozenset({1, 2}), frozenset({3, 4}), False),
        ]
        wrong = [c for c in cases if is_subset(c[0], c[1]) != c[2]]
        ok &= check("ex3a is_subset on tricky pairs", not wrong, f"wrong on {wrong}")
    except NotImplementedError:
        ok = False
        print("FAIL  ex3a is_subset — not implemented yet")

    try:
        pairs = [
            (frozenset({1, 2, 3}), frozenset({3, 2, 1}), True),
            (frozenset({1}), frozenset({1, 2}), False),
            (frozenset(), frozenset(), True),
            (frozenset({5}), frozenset({6}), False),
        ]
        wrong = [p for p in pairs if set_eq(p[0], p[1]) != p[2]]
        ok &= check("ex3b set_eq via double inclusion", not wrong, f"wrong on {wrong}")
    except NotImplementedError:
        ok = False
        print("FAIL  ex3b set_eq — not implemented yet")

    print()
    if ok:
        print("ALL EXERCISES COMPLETE — your membership-only ops match Python's set algebra.")
    else:
        print("Not done yet — fix the FAIL lines above and re-run.")


if __name__ == "__main__":
    main()
