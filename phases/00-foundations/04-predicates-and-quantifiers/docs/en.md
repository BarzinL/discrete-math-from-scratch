---
title: Predicates and Quantifiers
type: Build
prerequisites:
  - 03-propositional-logic
time: 50
---

# Predicates and Quantifiers

> ∀ and ∃ are just `all()` and `any()` — written the way mathematicians write them.

## Learning Objectives

By the end of this lesson you will be able to:

- Translate English claims into predicates with quantifiers over a stated domain
- Negate quantified statements correctly (flip the quantifier, negate the predicate)
- Explain why quantifier order changes meaning, with a concrete example
- Build a counterexample finder that produces witnesses for failed universal claims

## Pre-Lesson Check

Answer before reading — the explanations point at the section covering each idea.

*(Questions render below — three drawn at random from a larger pool each visit.)*

## The Problem

"This function never returns negative values." "Every user in the export has a valid
email." "Some request in the log was retried more than three times." Each of these is a
claim about *many* individual facts, and none of them is a single proposition — they
are proposition-*templates* waiting for an input. Propositional logic from the last
lesson cannot even write them down; it has no way to say "for all x".

Python programmers already own the machinery. `all(x > 0 for x in xs)` and
`any(x > 0 for x in xs)` are exactly ∀ and ∃ over a finite domain. The lesson's job is
to make that correspondence explicit and precise, and then to teach the one part that
is genuinely subtle: *negation*. Getting "not everyone" vs "everyone not" backwards in
a validation rule ships bugs; getting ∀/∃ negation backwards in a proof stalls every
later chapter.

## The Concept

A **predicate** is a proposition with holes: P(x) = "x is prime", Q(x, y) = "x < y".
Fill in the hole with an element of the **domain** and you get a proposition with a
truth value. Q(2, 5) is true; Q(5, 2) is false. Predicates become interesting when we
bind their holes with **quantifiers**:

| Statement | Reads as | True when… | Python over finite domain |
|---|---|---|---|
| ∀x P(x) | "for all x, P(x)" | every domain element satisfies P | `all(P(x) for x in domain)` |
| ∃x P(x) | "there exists x, P(x)" | at least one element satisfies P | `any(P(x) for x in domain)` |
| ∃!x P(x) | "exactly one x" | one and only one satisfies P | `sum(map(P, domain)) == 1` |

Two conventions matter. The quantifier's *domain* is always part of the statement —
"∀x" is incomplete until you say x ranges over what. And the order of quantifiers is
part of the statement: ∀x ∃y (y < x) is true over the integers (take y = x − 1), but
∃y ∀x (y < x) is false (no single y is below *every* integer). Mixed quantifiers do
not commute — ∀∃ means "for each, a helper may be chosen", ∃∀ means "one helper serves
everyone".

**Negation rules** — the heart of the lesson. To deny a universal claim you need only
one counterexample; to deny an existential claim you must rule out all of them:

| Statement | Negation |
|---|---|
| ¬∀x P(x) | ∃x ¬P(x) |
| ¬∃x P(x) | ∀x ¬P(x) |
| ¬∀x ∃y P(x, y) | ∃x ∀y ¬P(x, y) |

Read the first row aloud: "not everyone passed" = "someone failed". The quantifier
*flips* and the predicate *negates*. This is the discrete-math twin of De Morgan, and
it drives the counterexample-finder in this lesson's code.

**Bounded quantifiers** appear constantly in practice: ∀ prime p, ∃ k ≤ 10, … — the
domain is restricted by a condition. In code that is a filtered `all()`/`any()`; in
proofs it is a hypothesis on what you may assume about x.

## Build It

We model predicates over finite domains and implement quantifiers from scratch, then
build a *counterexample finder* — the tool that makes negation rules feel real.

### Step 1: Quantifiers from scratch

```python
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
```

`for_all` returns False the moment one element fails — that failing element *is* the
witness for ¬∀x P(x) ⇒ ∃x ¬P(x). `exists` returns True at the first success — that
element is the *witness* whose existence ∃ asserts. The short-circuiting behavior of
everyday Python is the negation rules in miniature.

### Step 2: The counterexample finder

To check that ¬∀x P(x) really equals ∃x ¬P(x) — not just believe it — we evaluate
both sides over many random domains and predicates, and when a claim fails, we *name
the witness*:

```python
def counterexample(domain, predicate):
    for x in domain:
        if not predicate(x):
            return x
    return None

def universal_negation_agrees(domain, predicate):
    left = not for_all(domain, predicate)
    right = exists(domain, lambda x: not predicate(x))
    if left != right:
        return False
    if left:
        witness = counterexample(domain, predicate)
        assert witness is not None
        assert not predicate(witness)
    return True
```

The assert in the middle is the punchline: whenever "not all" is true, the finder
hands back a concrete x that fails P — the counterexample exists, as promised. Run the
full script: it sweeps domains of sizes 0 through 8 with dozens of generated predicates
and verifies the agreement every time, including the empty domain.

### Step 3: Quantifier order can matter

```python
Z = list(range(-3, 4))

forall_exists = for_all(Z, lambda x: exists(Z, lambda y: y != x))
exists_forall = exists(Z, lambda y: for_all(Z, lambda x: y != x))
assert forall_exists and not exists_forall
```

Over any finite domain, ∀x ∃y (y ≠ x) holds (every element has *some other* element —
pick anyone else) while ∃y ∀x (y ≠ x) fails (the candidate y would have to differ from
itself). Same predicate, same domain, opposite verdicts — order is meaning. The script
also checks the boundary trap: ∀x ∃y (y < x) is true over all the integers but FALSE on
any finite slice, because the smallest element has nothing below it. A claim that is
true over an infinite domain can fail at the edge of a finite one — always ask what
happens at the boundary.

## Prove It

**Claim: ¬∀x P(x) ≡ ∃x ¬P(x).**

Proof: we show each side implies the other.

(⇒) Suppose ¬∀x P(x) holds, and suppose — for contradiction — that ∃x ¬P(x) does not.
Then every x satisfies P(x), which is exactly ∀x P(x), contradicting our supposition.
So ∃x ¬P(x) holds. (This "suppose not, derive a contradiction" move is Phase 01's
proof-by-contradiction; it earns its keep already.)

(⇐) Suppose ∃x ¬P(x) holds, and let w be the witnessing element with ¬P(w). Since
P fails at w, it cannot be that P holds at every x — so ¬∀x P(x).

Both directions hold, so the statements are equivalent. ∎

The companion rule ¬∃x P(x) ≡ ∀x ¬P(x) is this same proof with "and/or" swapped for
"all/some" — or, more elegantly, obtained by substituting ¬P into the rule just proven
and negating both sides. Notice also the empty domain: over an empty domain ∀x P(x) is
vacuously true (no x can fail it) while ∃x P(x) is false (no witness exists) — which
the script checks explicitly, and which matches the "kept promise about nothing"
intuition from the previous lesson.

**Your turn:** prove the order-sensitivity result — that ∃y ∀x P(x, y) implies
∀x ∃y P(x, y), and find a concrete P over a small domain where the reverse fails. The
witnessing structure of the proof above is all you need: the single serving y works
for everyone, so in particular it works for each.

## Connect It

**In AI/ML engineering.** Data validation is quantifier checking: "every row has a
non-null label" is ∀x P(x) over the dataset, and the rows failing it are exactly the
counterexamples your finder should name. Hypothesis testing in property-based testing
(Hypothesis, fuzzing) is automated ∃-hunting — the framework searches for one input
that breaks your invariant. Model cards make quantified claims ("for all demographic
subgroups, error rate < 2× the mean"); auditing is hunting the ∃x that falsifies it.
And the order lesson — ∀∃ vs ∃∀ — is the P vs NP distinction in miniature: "every
problem has a solution someone can find" versus "one method finds them all".

**In databases.** "Users with no orders" is ¬∃ order; the negation table turns it
into `NOT EXISTS`, the form that indexes. Every `WHERE NOT IN (subquery)` trap with
NULLs is a botched quantifier negation.

## Test Your Understanding

Answer after working through the lesson — including running `main.py` and starting
`exercises.py`.

*(Questions render below — four drawn at random from a larger pool each visit.)*

## Exercises

All exercises are completed **at the computer**. Open `code/exercises.py`, implement
each `TODO` function, and run `python3 exercises.py` — the script self-grades and
prints the completion banner only when every check passes.

1. Easy — `negate_universal` and `negate_existential`: implement both negation rules
   as functions over (domain, predicate) and verify they agree with the direct
   definitions over randomized domains — the lesson's sweep, now yours.
2. Medium — `exists_unique`: implement "exactly one x satisfies P" and prove by testing
   that it matches the formula ∃x (P(x) ∧ ∀y (P(y) → y = x)) implemented separately.
3. Hard — `counterexample` + `validate_rows`: given a list of row dicts and a rule
   predicate, return the failing rows (the witnesses). The checker hands you a small
   dirty dataset and asserts your function finds exactly the rows a brute-force scan
   finds — quantifier negation as a working data-quality tool.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| predicate | "a condition" | a proposition with variable holes; becomes true/false once the holes are filled |
| domain | "the range" | the fixed set a quantifier ranges over — always part of the statement |
| ∀ (universal) | "for all" | true when every domain element satisfies P; vacuously true over an empty domain |
| ∃ (existential) | "there exists" | true when at least one element satisfies P; false over an empty domain |
| witness | "an example" | the concrete element whose existence an ∃-statement asserts |
| quantifier order | "word order" | ∀∃ ≠ ∃∀: per-element helpers vs one helper for all |
| negation rule | "flip it" | negating a quantifier flips ∀↔∃ and negates the predicate |
