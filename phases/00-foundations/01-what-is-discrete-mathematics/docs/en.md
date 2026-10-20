---
title: What Is Discrete Mathematics?
type: Learn
prerequisites: []
time: 30
---

# What Is Discrete Mathematics?

> Study what you can count, one step at a time — because computers can too.

## Learning Objectives

By the end of this lesson you will be able to:

- Distinguish discrete from continuous quantities in concrete CS scenarios
- Explain why a computer is inherently a discrete machine
- State how many subsets an n-element set has and outline the bijection proof
- Decide when testing suffices for a claim and when a proof is required

## Pre-Lesson Check

Answer these before reading — they calibrate what to skim. If you miss one, the
explanation points at the section that covers it.

*(Questions render below — three drawn at random from a larger pool each visit.)*

## The Problem

You want to write a program that schedules final exams: 40 courses, 12 rooms, no two
exams in the same room at the same time, students must not have two exams at once.
Nothing here involves calculus. There is no curve to optimize, no rate of change.
There are *objects* (courses, rooms, time slots) and *relationships* between them
(conflicts, assignments). The mathematics that handles objects and relationships —
as opposed to quantities that vary smoothly — is discrete mathematics.

The word *discrete* is the opposite of *continuous*. A continuous quantity, like
temperature, can take any value in a range: 20.1°, 20.13°, 20.1300007°. A discrete
quantity is separated into individual pieces: a course either conflicts with another
or it does not — there is no "0.7 conflicts". Between any two courses there is no
third course "in between". Discrete mathematics is the mathematics of such separate,
countable structures.

This matters for computer science because a computer is a discrete machine. It stores
a finite number of bits, performs a finite number of operations per second, and every
data structure you will ever use — arrays, trees, graphs, hash tables — is a discrete
object. Continuous mathematics (calculus) explains how a neural network *trains*;
discrete mathematics explains everything about the *machine* doing the training: how
much memory, how many steps, whether the protocol is correct, whether the graph of
connections is connected.

## The Concept

The subject is a toolbox of linked topics, each giving a language for a different kind
of discrete structure:

| Topic | The structure it studies | Where you meet it in CS |
|---|---|---|
| Logic and proofs | sentences that are true or false | program correctness, verification |
| Sets | collections without order or repeats | relational databases, types |
| Functions and relations | pairings between collections | hashing, sorting, permissions |
| Combinatorics | counting without listing | algorithm analysis, probability |
| Number theory | integers and divisibility | cryptography, hashing |
| Graph theory | objects and connections | networks, dependencies, maps |
| Discrete probability | chance over finite outcomes | randomized algorithms, ML |

Two ideas run through everything and are worth naming now.

**Counting is hard to do correctly.** Given enough pieces, naive answers overcount or
undercount. Much of this curriculum is training a very specific skill: counting a set
of possibilities exactly once each.

**Verification is cheaper than proof sometimes, and proof is cheaper than verification
other times.** If you claim "every even number greater than 2 can be written as a sum
of two primes," testing the first few million cases is instant and proves nothing about
the rest. If you claim "this algorithm never loops forever," testing tells you almost
nothing and a proof settles it forever. Knowing which tool fits which claim is a
central skill — the next lessons alternate between the two deliberately.

A first concrete example: think of the people you follow on social media as dots, with
a line between two dots when one follows the other. Questions like "does a message from
A reach B within three forwards?" or "what is the smallest group of accounts whose
removal disconnects the network?" are graph-theory questions. The dots-and-lines model
throws away everything except the structure — and it turns out structure is the thing
that answers the question.

## Prove It

Even this orientation lesson has a first honest proof. Claim:

**There are exactly 2ⁿ subsets of a set with n elements.**

Why should anyone believe 2ⁿ? Here is the proof, called a *proof by bijection* —
counting the same collection two ways.

Every subset of a set with n elements corresponds, one-to-one, to a string of n bits:
bit i is 1 exactly when element i is in the subset, and 0 otherwise. The subset and the
bit string determine each other completely — nothing is lost going either direction.
So there are exactly as many subsets as there are n-bit strings. An n-bit string has 2
choices per position, and the positions are independent, so by the product rule
(properly proven in the counting phase) there are 2 × 2 × … × 2 = 2ⁿ strings. Hence 2ⁿ
subsets. ∎

Notice the shape of that argument: a bijection (the correspondence), plus a product
rule (the choices per bit). Nearly every counting proof in this curriculum has that
same skeleton with different bones.

## Connect It

**In AI/ML engineering.** Training sets, batches, and epochs are discrete counts; a
model's vocabulary is a finite set of tokens; a classifier's output space is a set of
labels whose size you set with one argument. The 2ⁿ subsets result is not a curiosity:
feature selection over n candidate features searches exactly 2ⁿ candidate feature sets
(exhaustive search dies near n = 30 — this is why heuristics exist), and a "power set"
of interventions sits underneath do-calculus in causal ML.

**In everyday code.** Every `frozenset` you use as a dict key, every `GROUP BY`, every
feature-engineering step that asks "which combination of columns identifies a row?"
is this lesson's machinery.

- **Scheduling exam conflicts**, from the opening problem, is graph coloring — Phase 05.
- **Cryptography** rests entirely on number theory — Phase 04.
- **Proofs of program correctness** are logic — Phases 00 and 01.
- **Big-O analysis** of every algorithm you will ever write is a counting argument — Phase 08.

## Test Your Understanding

Answer these after working through the lesson — including running `main.py` and
starting `exercises.py`.

*(Questions render below — four drawn at random from a larger pool each visit.)*

## Exercises

All exercises are completed **at the computer**. Open
`code/exercises.py`, implement each `TODO` function, and run
`python3 exercises.py` — the script self-grades every exercise with a PASS/FAIL line
and will not print the final `ALL EXERCISES COMPLETE` banner until every check passes.

1. Easy — `subsets_of`: generate all subsets of a list without `itertools`, using the
   bit-string encoding from the proof. The checker compares you against 2ⁿ.
2. Medium — `subsets_containing`: count subsets containing a given element, and
   `pairs_subset`: count pairs (A, B) with A ⊆ B. Both answers fall out of per-element
   choice arguments — the checker verifies your formula for n up to 12.
3. Hard — `bijection_roundtrip`: prove the bit-string encoding is a bijection by
   implementing `encode_subset` and `decode_bits` so that every subset survives the
   round trip. If your pair of functions is a genuine bijection, the exhaustive check
   passes for every subset of a 6-element set.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| discrete | "small" | made of separate, individually listable pieces; opposite of continuous |
| continuous | "big" | varies smoothly over a range, like real numbers on an interval |
| bijection | "they match up" | a pairing between two collections where every element is used exactly once on each side |
| combinatorics | "hard counting" | the exact counting of finite structures |
| structure | "the stuff" | which elements exist and how they relate — the only thing these models keep |
