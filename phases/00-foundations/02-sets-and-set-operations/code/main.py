from itertools import combinations


def all_subsets(u):
    result = [frozenset()]
    for size in range(1, len(u) + 1):
        result.extend(frozenset(c) for c in combinations(u, size))
    return result


def union(a, b):
    return {x for x in a} | {x for x in b}


def intersection(a, b):
    return {x for x in a if x in b}


def difference(a, b):
    return {x for x in a if x not in b}


def symmetric_difference(a, b):
    return difference(a, b) | difference(b, a)


def check_against_builtin(u):
    subs = all_subsets(u)
    for a in subs:
        for b in subs:
            assert union(a, b) == (a | b)
            assert intersection(a, b) == (a & b)
            assert difference(a, b) == (a - b)
            assert symmetric_difference(a, b) == (a ^ b)
    print(f"PASS  membership-defined operations match Python set ops over {len(subs)}^2 pairs")


def de_morgan_holds(u):
    subs = all_subsets(u)
    for a in subs:
        for b in subs:
            left = u - (a | b)
            right = (u - a) & (u - b)
            assert left == right, f"De Morgan counterexample: A={a} B={b}"
    print(f"PASS  De Morgan: complement of union == intersection of complements ({len(subs)}^2 pairs)")


def distributive_holds(u):
    subs = all_subsets(u)
    for a in subs:
        for b in subs:
            for c in subs:
                assert (a & (b | c)) == ((a & b) | (a & c)), f"counterexample: {a} {b} {c}"
                assert (a | (b & c)) == ((a | b) & (a | c)), f"dual counterexample: {a} {b} {c}"
    print(f"PASS  distributive law + dual over universe of size {len(u)}")


def complement_universe_trap():
    users = {"ada", "bo", "cy", "dee"}
    admins = {"ada", "bo"}
    banned = {"cy"}
    active_non_admins = users - admins - banned
    assert active_non_admins == {"dee"}
    print("PASS  complement is relative to the universe given (active non-admins == {dee})")


if __name__ == "__main__":
    u = frozenset(range(4))
    check_against_builtin(u)
    de_morgan_holds(u)
    distributive_holds(u)
    complement_universe_trap()
