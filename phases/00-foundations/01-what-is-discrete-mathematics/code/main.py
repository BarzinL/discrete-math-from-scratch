from itertools import combinations, product


def subsets_brute_force(elements):
    result = []
    for size in range(len(elements) + 1):
        result.extend(combinations(elements, size))
    return [frozenset(s) for s in result]


def subsets_via_bits(elements):
    n = len(elements)
    result = []
    for bits in product([0, 1], repeat=n):
        result.append(frozenset(e for e, b in zip(elements, bits) if b))
    return result


def verify_subset_count(n=6):
    elements = list(range(n))
    counted = len(subsets_brute_force(elements))
    predicted = 2 ** n
    assert counted == predicted, f"{counted} != {predicted}"
    assert subsets_brute_force(elements) == subsets_via_bits(elements)
    print(f"PASS  |S| = {n}: {counted} subsets == 2^{n}")


def verify_pair_encoding(n=6):
    elements = list(range(n))
    pairs = {(a, b) for a in subsets_brute_force(elements) for b in subsets_brute_force(elements) if a <= b}
    positions = list(product([0, 1, 2], repeat=n))
    predicted = len(positions)
    assert len(pairs) == predicted, f"{len(pairs)} != {predicted}"
    print(f"PASS  ordered pairs (A, B) with A subset of B: {len(pairs)} == 3^{n}")


if __name__ == "__main__":
    verify_subset_count()
    verify_pair_encoding()
