---
title: Sets and Set Operations
type: Build
prerequisites: []
time: 45
---

# Sets and Set Operations

> A set has no order and no repeats. Everything else — lists, databases, filters — is
> built on top of that.

## Learning Objectives

By the end of this lesson you will be able to:

- Define sets by membership and predict the result of ∪, ∩, −, △, and complement
- Implement each set operation from membership tests alone
- Verify De Morgan and distributive laws by exhaustive brute force over a universe
- Prove a set identity by double inclusion

## Pre-Lesson Check

Answer before reading — the explanations point at the section covering each idea.

*(Questions render below — three drawn at random from a larger pool each visit.)*

## The Problem

You have two access-control lists at work: `admins` and `contractors`. Who is both?
Who is one but not the other? Who is in neither? You could write three nested loops
with flags and edge cases — or you could recognize these as intersection, difference,
and complement and be done. Nearly every "find the overlap between two collections"
question in software is a set operation wearing a costume.

Sets also solve a subtler problem: *talking precisely*. When you write "all users with
an active subscription AND a verified email," you have defined a set. When the marketing
team disagrees with you about who that includes, you can settle it by checking one
membership question per user — because a set is exactly determined by what belongs to
it. No order, no duplicates, no ambiguity.

## The Concept

A **set** is a collection of distinct objects. `2 ∈ {1, 2, 3}` means 2 *is a member*;
`4 ∉ {1, 2, 3}` means it is not. Two sets are **equal** when they have exactly the same
members — so `{1, 2} = {2, 1} = {1, 1, 2}`. Repetition and order simply do not exist
in a set. If you need order, use a tuple or a list; a set is the tool for *membership*
questions.

Sets can contain other sets. `{1, 2}` is a set; `{{1}, {2}, {1, 2}}` is a different
set whose members happen to be sets. The **power set** of S, written P(S), is the set
of *all* subsets of S — we proved |P(S)| = 2ⁿ in the previous lesson.

The operations, all defined purely by membership:

| Operation | Notation | x is in the result when… |
|---|---|---|
| union | A ∪ B | x ∈ A **or** x ∈ B |
| intersection | A ∩ B | x ∈ A **and** x ∈ B |
| difference | A − B | x ∈ A and x ∉ B |
| symmetric difference | A △ B | x is in exactly one of A, B |
| complement | Ā | x ∉ A (relative to some universe U) |
| subset | A ⊆ B | every member of A is also a member of B |

The last row is the important conceptual shift: A ⊆ B is itself a *claim*, true or
false, that quantifies over all members. Operations produce sets; ⊆, ∈, and = produce
truth values. Keeping "which expressions denote sets, which denote booleans" straight
is half of set fluency.

Two laws tie the operations together and will be our proof targets:

- **De Morgan:** A ∪ B Ā = Ā ∩ B̄ — "not (in A or in B)" equals "not in A and not in B"
- **Distributive:** A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)

## Build It

Python's built-in `set` type implements all of this. But the point of this lesson is
to see that the operations are *nothing more than the membership conditions in the
table* — so we build them from `in` checks alone, then check them against Python's
versions.

### Step 1: Operations from membership tests

```python
def union(a, b):
    return {x for x in a | b}

def intersection(a, b):
    return {x for x in a if x in b}

def difference(a, b):
    return {x for x in a if x not in b}

def symmetric_difference(a, b):
    return {x for x in a if x not in b} | {x for x in b if x not in a}
```

Each one is a direct transcription of the rightmost table column: "or" becomes
combining both scans, "and" becomes a filter, "not in" becomes a negative filter.
That is the whole implementation.

### Step 2: Brute-force check the laws

A set law over a universe of size n can be checked by trying every combination of
"member / not member" for each element. With a universe of 4 elements that is 2⁴ = 16
worlds per set variable — cheap, and it either finds a counterexample or fails to
find one in every possible world.

```python
def all_subsets(u):
    result = [frozenset()]
    for size in range(1, len(u) + 1):
        result.extend(frozenset(c) for c in combinations(u, size))
    return result

def de_morgan_holds(u):
    for a in all_subsets(u):
        for b in all_subsets(u):
            if (u - (a | b)) != ((u - a) & (u - b)):
                return (False, a, b)
    return (True,)
```

The full script below does this properly for every pair (and triple) of subsets of a
4-element universe, asserting both sides of each law are equal as sets. If any
assignment of elements differed, the assert would fire with the offending sets
printed.

```python
from itertools import combinations

def all_subsets(u):
    result = [frozenset()]
    for size in range(1, len(u) + 1):
        result.extend(frozenset(c) for c in combinations(u, size))
    return result

def de_morgan_holds(u):
    subs = all_subsets(u)
    for a in subs:
        for b in subs:
            left = u - (a | b)
            right = (u - a) & (u - b)
            if left != right:
                return (False, a, b, left, right)
    return (True,)

def distributive_holds(u):
    subs = all_subsets(u)
    for a in subs:
        for b in subs:
            for c in subs:
                if (a & (b | c)) != ((a & b) | (a & c)):
                    return (False, a, b, c)
    return (True,)
```

Running `main.py` prints a PASS line for De Morgan and for distributivity over a
4-element universe — 256 and 4096 set comparisons respectively, all agreeing.

## Prove It

**Claim: Ā ∩ B̄ = complement of (A ∪ B), relative to universe U.**

Proof: we show each side is a subset of the other, which forces equality.

(⊆) Take any x ∈ Ā ∩ B̄. Then x ∈ Ā, so x ∉ A; and x ∈ B̄, so x ∉ B. Since x is in
neither A nor B, x is not in their union: x ∉ A ∪ B. So x is in the complement of
A ∪ B.

(⊇) Take any x in the complement of A ∪ B, so x ∉ A ∪ B. If x were in A, then x would
be in A ∪ B — contradiction. So x ∉ A, i.e. x ∈ Ā. Identically x ∉ B, so x ∈ B̄.
Therefore x ∈ Ā ∩ B̄.

Both subset directions hold for every x, so the two sets are equal. ∎

This proof technique — show A ⊆ B and B ⊆ A, conclude A = B — is called **double
inclusion** and is the standard way to prove two sets equal. Note also what the proof
used: only the meanings of ∩, ∪, and complement. Nothing about numbers, sizes, or
what the elements are. That is why the brute-force check over an arbitrary 4-element
universe finding no counterexample is *evidence*, and this proof is *the reason* —
the proof works over every universe, of any size, containing anything.

**Your turn:** prove A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C) by double inclusion. The structure
of the proof above repeats almost word for word.

## Connect It

**In AI/ML engineering.** A one-hot encoder maps each category to the set of features
it activates; a label space is literally a set, and `model.classes_` is its enumeration.
Train/test splits are set differences (the holdout is `all_data − train`), dedup before
splitting is set equality, and feature-overlap analysis between datasets is
intersection. In evaluation, "which errors do both models make?" is A ∩ B of their
error sets — if that intersection is large, the models fail the same way and an
ensemble won't help.

**In systems code.** Permission checks are intersections and complements; cache
invalidation is set difference; De Morgan read backwards is the difference between
"deny if not (admin or owner)" and "allow if not-admin and not-owner" — get it
backwards and you ship an authorization hole.

## Test Your Understanding

Answer after working through the lesson — including running `main.py` and starting
`exercises.py`.

*(Questions render below — four drawn at random from a larger pool each visit.)*

## Exercises

All exercises are completed **at the computer**. Open `code/exercises.py`, implement
each `TODO` function, and run `python3 exercises.py` — the script self-grades and
prints the completion banner only when every check passes.

1. Easy — `power_set`: build P(S) for a 4-element set without `itertools`. The checker
   verifies both the count (2ⁿ) and that your result matches the brute-force
   enumeration.
2. Medium — `symdiff`: implement symmetric difference using ONLY membership tests
   (`in`, loops, set-builder style) — no `-`, `^`, `|`, or `&`. The checker compares
   you against Python's `^` over all subset pairs of a 4-element universe.
3. Hard — `is_subset`, then `set_eq` via double inclusion: prove A = B by checking
   A ⊆ B and B ⊆ A through your own `is_subset`. The checker tries your functions
   against tricky pairs (equal sets, empty set, same-size non-equal sets).

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| set | "a list" | a collection with no order and no duplicates; only membership matters |
| power set | "all the lists" | the set of every subset; has exactly 2ⁿ members for n-element S |
| subset | "smaller than" | every member of A is a member of B — equal sets are subsets of each other |
| symmetric difference | "XOR of sets" | members of exactly one of the two sets |
| universe | "the world" | the fixed collection the complement is taken relative to |
| double inclusion | "check both ways" | A = B iff A ⊆ B and B ⊆ A — the standard set-equality proof |
