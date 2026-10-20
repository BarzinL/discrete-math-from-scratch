import random


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


def counterexample(domain, predicate):
    for x in domain:
        if not predicate(x):
            return x
    return None


def witness(domain, predicate):
    for x in domain:
        if predicate(x):
            return x
    return None


def universal_negation_agrees(domain, predicate):
    left = not for_all(domain, predicate)
    right = exists(domain, lambda x: not predicate(x))
    assert left == right, f"negation rules disagree on domain={domain}"
    if left:
        w = counterexample(domain, predicate)
        assert w is not None, "no counterexample found though not-all held"
        assert not predicate(w), f"counterexample {w} does not actually fail the predicate"
    print(f"PASS  neg(not-all) == exists-not over domain size {len(domain)}")


def existential_negation_agrees(domain, predicate):
    left = not exists(domain, predicate)
    right = for_all(domain, lambda x: not predicate(x))
    assert left == right, f"negation rules disagree on domain={domain}"
    if left:
        assert witness(domain, predicate) is None, "found a P-witness though none should exist"
    print(f"PASS  neg(none) == all-not over domain size {len(domain)}")


def check_empty_domain():
    assert for_all([], lambda x: x > 0) is True
    assert exists([], lambda x: x > 0) is False
    print("PASS  empty domain: for-all vacuously true, exists false")


def check_quantifier_order():
    Z = list(range(-3, 4))
    assert for_all(Z, lambda x: exists(Z, lambda y: y != x)) is True
    assert exists(Z, lambda y: for_all(Z, lambda x: y != x)) is False
    print("PASS  forall-exists vs exists-forall over Z: opposite verdicts")


def check_boundary_trap():
    Z = list(range(-3, 4))
    assert for_all(Z, lambda x: exists(Z, lambda y: y < x)) is False
    print("PASS  boundary trap: forall-exists (y < x) FALSE on finite slice, true over all of Z")


def random_predicate(rng):
    threshold = rng.randint(-3, 3)
    mod = rng.randint(1, 3)
    mode = rng.choice(["gt", "mod", "or", "and"])
    if mode == "gt":
        return lambda x: x > threshold
    if mode == "mod":
        return lambda x: x % mod == 0
    if mode == "or":
        return lambda x: x > threshold or x % mod == 0
    return lambda x: x > threshold and x % mod == 0


def sweep_negation_rules(trials=40, seed=2026):
    rng = random.Random(seed)
    for _ in range(trials):
        size = rng.randint(0, 8)
        domain = [rng.randint(-5, 5) for _ in range(size)]
        predicate = random_predicate(rng)
        universal_negation_agrees(domain, predicate)
        existential_negation_agrees(domain, predicate)


def exists_unique(domain, predicate):
    hits = [x for x in domain if predicate(x)]
    return len(hits) == 1


def check_exists_unique():
    domain = list(range(10))
    assert exists_unique(domain, lambda x: x * x == 49) is True
    assert exists_unique(domain, lambda x: x % 5 == 0) is False
    assert exists_unique(domain, lambda x: x > 100) is False
    print("PASS  exists_unique: exactly-one semantics (true / zero / two cases)")


if __name__ == "__main__":
    check_empty_domain()
    sweep_negation_rules()
    check_quantifier_order()
    check_boundary_trap()
    check_exists_unique()
