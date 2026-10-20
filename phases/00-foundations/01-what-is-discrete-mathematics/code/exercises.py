"""Self-grading exercises for lesson 01. Implement each TODO, then run this file.

Every exercise is checked automatically: a PASS/FAIL line prints per exercise,
and the final banner appears only when all checks pass.
"""

from itertools import combinations


def subsets_of(elements):
    """Exercise 1 (easy): return ALL subsets of `elements` as a list of frozensets.

    Do NOT use itertools. Use the bit-string idea from the lesson: for each of
    the 2**n bit strings, include exactly the elements whose bit is 1.
    """
    raise NotImplementedError


def subsets_containing(elements, target):
    """Exercise 2a (medium): return the number of subsets of `elements` that contain `target`.

    Hint: fix target's membership — how many choices remain for the other elements?
    Return an int.
    """
    raise NotImplementedError


def pairs_subset(n):
    """Exercise 2b (medium): return the number of pairs (A, B) of subsets of an
    n-element set with A subset of B (A == B allowed).

    Hint: for each element there are three states: in neither, in B only, in both.
    """
    raise NotImplementedError


def encode_subset(elements, subset):
    """Exercise 3 (hard): return the bit string for `subset` over `elements`.

    Bit i is 1 exactly when elements[i] is in subset. Return a string of '0'/'1'.
    """
    raise NotImplementedError


def decode_bits(elements, bits):
    """Exercise 3 (hard): invert encode_subset — rebuild the frozenset from its bits."""
    raise NotImplementedError


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"{status}  {name}{(' — ' + detail) if detail and not condition else ''}")
    return condition


def main():
    ok = True

    elements = ["a", "b", "c"]
    try:
        got = sorted(map(sorted, map(set, subsets_of(elements))))
        want = sorted([list(c) for k in range(4) for c in combinations(elements, k)])
        ok &= check("ex1 subsets_of({a,b,c}) == 8 subsets", got == want, f"got {got}")
        ok &= check("ex1 count is 2**n", len(subsets_of(list(range(5)))) == 32)
    except NotImplementedError:
        ok = False
        print("FAIL  ex1 subsets_of — not implemented yet")

    try:
        n = 6
        brute = sum(1 for k in range(n + 1) for c in combinations(range(n), k) if 3 in c)
        got = subsets_containing(list(range(n)), 3)
        ok &= check("ex2a subsets containing a fixed element", got == brute,
                    f"got {got}, expected {brute}")
    except NotImplementedError:
        ok = False
        print("FAIL  ex2a subsets_containing — not implemented yet")

    try:
        brute = sum(1 for mask_a in range(16) for mask_b in range(16)
                    if mask_a & mask_b == mask_a)
        got = pairs_subset(4)
        ok &= check("ex2b pairs (A,B) with A subset of B, n=4", got == brute,
                    f"got {got}, expected {brute}")
        ok &= check("ex2b matches 3**n", pairs_subset(5) == 3 ** 5)
    except NotImplementedError:
        ok = False
        print("FAIL  ex2b pairs_subset — not implemented yet")

    try:
        universe = ["p", "q", "r", "s", "t", "u"]
        all_subsets = [frozenset(c) for k in range(7) for c in combinations(universe, k)]
        roundtrip_ok = all(
            decode_bits(universe, encode_subset(universe, s)) == s for s in all_subsets)
        distinct = len({encode_subset(universe, s) for s in all_subsets})
        ok &= check("ex3 bit-string roundtrip preserves every subset", roundtrip_ok)
        ok &= check("ex3 encoding is injective (64 distinct strings)",
                    distinct == 2 ** 6, f"got {distinct}")
    except NotImplementedError:
        ok = False
        print("FAIL  ex3 encode/decode — not implemented yet")

    print()
    if ok:
        print("ALL EXERCISES COMPLETE — the 2**n and 3**n laws are now yours.")
    else:
        print("Not done yet — fix the FAIL lines above and re-run.")


if __name__ == "__main__":
    main()
