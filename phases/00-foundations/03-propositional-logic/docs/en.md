---
title: Propositional Logic
type: Build
prerequisites:
  - 02-sets-and-set-operations
time: 50
---

# Propositional Logic

> A truth table is a tiny universe: every possible world, enumerated, with your claim
> evaluated in each.

## Learning Objectives

By the end of this lesson you will be able to:

- Build a truth-table engine and use it as a complete equivalence checker
- State when an implication is false, and why F → anything is true
- Distinguish contrapositive (always equivalent) from converse (never free)
- Apply De Morgan's laws to refactor boolean conditions in real code

## Pre-Lesson Check

Answer before reading — the explanations point at the section covering each idea.

*(Questions render below — three drawn at random from a larger pool each visit.)*

## The Problem

A billing condition in your codebase reads: `if not (expired or unpaid):`. Three months
later someone adds a second check nearby: `if not expired and not unpaid:`. Are these
the same? A wrong guess means either charging active customers or billing lapsed ones.
You can test a few users and *hope*, or you can settle it in four lines: enumerate
every combination of expired/unpaid and compare the results. This is propositional
logic used exactly as intended — not as philosophy, but as the cheapest possible
correctness tool for yes/no conditions.

The deeper payoff is vocabulary. "This function returns wrong results *when* the input
is a list but *not* when it is empty" is an implication with a negation, and being
able to write claims like that precisely is what makes the proofs in every later phase
writable at all.

## The Concept

A **proposition** is a sentence that is definitely true or definitely false — "7 is
prime" (true), "all birds fly" (false). Sentences with free variables like "x > 5" are
not propositions yet; they become them once x is fixed (that upgrade is the next
lesson's topic).

Propositions combine with **connectives**:

| Name | Notation | Python | True when… |
|---|---|---|---|
| negation | ¬P | `not P` | P is false |
| conjunction | P ∧ Q | `P and Q` | both true |
| disjunction | P ∨ Q | `P or Q` | at least one true |
| implication | P → Q | — | P is false, or Q is true |
| biconditional | P ↔ Q | `P == Q` | both the same |

The only genuinely strange row is implication. P → Q is a *promise*: "if P holds, then
Q holds." A promise is only broken when P holds and Q fails. If P never held, the
promise was kept vacuously — so F → anything is **true**. Two consequences students
find surprising, both worth memorizing:

- F → T is *true*. "If 2 is odd then 5 is prime" is a kept promise about nothing.
- P → Q has **no** relationship to the *converse* Q → P. "If it rains, the ground is
  wet" does not let you conclude the ground is wet ⇒ it rained (a sprinkler runs
  counterexample). Confusing a statement with its converse is the single most common
  reasoning error in code review and in mathematics.

Two compound statements are **logically equivalent** when they have the same truth
value under every possible assignment — i.e., their truth tables are identical
column-by-column. Equivalence is the engine of this lesson: every refactor of a
boolean condition is justified by an equivalence, and the two De Morgan identities
below are the workhorses.

## Build It

We build a truth-table engine from scratch: formulas as small Python functions over
an assignment dict, and a generator of every assignment over the formula's variables.

### Step 1: Formulas as functions

```python
def variables(formula):
    names = formula.__code__.co_varnames
    return sorted(names)

def assignments(vars_):
    n = len(vars_)
    for bits in product([False, True], repeat=n):
        yield dict(zip(vars_, bits))

def truth_table(formula):
    vars_ = variables(formula)
    rows = []
    for a in assignments(vars_):
        rows.append((a, formula(**a)))
    return rows
```

A formula is just a Python function whose parameters are the proposition letters.
`variables` reads them back out of the function signature, `assignments` produces all
2ⁿ worlds, and `truth_table` evaluates the formula in each. The whole engine is three
functions — because "check under every assignment" *is* the definition.

### Step 2: Equivalence checking

```python
def equivalent(f, g):
    return truth_table(f) == truth_table(g)
```

Since truth tables are sorted by assignment, two formulas are equivalent exactly when
their tables are equal. Note what this checker gives you that testing specific cases
never can: with n variables it has examined *every possible world*. For propositional
logic, brute force over the finite truth table is a complete decision procedure —
here, exhaustive verification actually *is* proof.

The full script applies the checker to the pairs you will actually use, including the
billing condition from the opening problem, and prints PASS per law.

## Prove It

**Claim: ¬(P ∨ Q) ≡ ¬P ∧ ¬Q (De Morgan).**

Proof: take any assignment of truth values to P and Q.

- If ¬(P ∨ Q) is true: then P ∨ Q is false, so neither P nor Q is true (disjunction is
  true when at least one disjunct is true, so if either were true the disjunction
  would be). Hence ¬P and ¬Q are both true, so ¬P ∧ ¬Q is true.
- If ¬(P ∨ Q) is false: then P ∨ Q is true, so at least one of P, Q is true. Then at
  least one of ¬P, ¬Q is false, so the conjunction ¬P ∧ ¬Q is false.

The two sides agree on every assignment — true-together, false-together — which is
exactly the definition of logical equivalence. ∎

Now notice the split between this lesson's two halves. The truth-table checker proves
the law by *exhausting 4 worlds*; the prose proof proves it by *reasoning about an
arbitrary world once*. Both are legitimate, and the reason brute force is fully
legitimate here — unlike in the previous lesson, where no finite check could cover all
universes — is that a formula over n variables has *only* 2ⁿ worlds. Finite subject
matter makes enumeration a proof. When a later phase hands you infinitely many cases
(natural numbers, graphs of any size), enumeration loses that power and the proof
techniques of Phase 01 take over.

**Your turn:** write out the truth table for P → Q and for ¬Q → ¬P (the *contrapositive*)
and verify all four rows match. Then do the same for P → Q and Q → P (the converse)
and see the mismatch. That mismatch is the proof that a statement and its converse are
different claims.

## Connect It

**In AI/ML engineering.** Every filter on a dataset is a propositional formula —
`df[(df.age > 30) & ~(df.city.isin(["NYC", "LA"]))]` is a negated disjunction wearing
pandas syntax. Short-circuit evaluation (`and`/`or` bailing early) is exactly why the
truth table's "F ∧ anything is F" row saves work in guards like
`if user is not None and user.active`. In model evaluation, precision/recall
thresholds combine into compound conditions whose simplification is De Morgan;
in LLM tool-calling, permission rules ("allow if (read-only and safe) or approved")
are propositional formulas whose equivalence class you should reason about before
shipping a rewrite.

**In hardware.** A digital circuit *is* a propositional formula in silicon — Phase 06
makes that literal, and minimizing the formula minimizes the chip.

## Test Your Understanding

Answer after working through the lesson — including running `main.py` and starting
`exercises.py`.

*(Questions render below — four drawn at random from a larger pool each visit.)*

## Exercises

All exercises are completed **at the computer**. Open `code/exercises.py`, implement
each `TODO` function, and run `python3 exercises.py` — the script self-grades and
prints the completion banner only when every check passes.

1. Easy — `truth_table`: build the full table for any 2-variable formula as a list of
   (P, Q, result) rows. The checker compares yours against all 4 rows for several
   formulas.
2. Medium — `is_tautology` and `is_contradiction`: classify a formula by its table.
   Then `satisfiable`: does ANY assignment make it true? (The checker uses formulas
   where the answer differs formula to formula.)
3. Hard — `simplify_de_morgan`: given a lambda for ¬(P ∨ Q), produce and *verify* the
   equivalent ¬P ∧ ¬Q by showing the two tables match; then `implies_via_or`: prove
   P → Q ≡ ¬P ∨ Q the same way. Your function must return True from the checker's
   comparison — equivalence demonstrated, not asserted.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| proposition | "a statement" | a sentence with a definite truth value, no free variables |
| implication | "if-then" | a promise: false only when premise true and conclusion false; vacuously true when premise is false |
| converse | "the reverse" | Q → P — a *different claim* from P → Q, often falsely treated as equivalent |
| contrapositive | "flipped and negated" | ¬Q → ¬P — *always* equivalent to P → Q |
| logical equivalence | "same thing" | identical truth value under every assignment — same truth table |
| truth table | "the little grid" | enumeration of all 2ⁿ assignments; a complete decision procedure over finite variables |
