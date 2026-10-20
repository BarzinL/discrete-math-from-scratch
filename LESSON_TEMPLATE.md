# Lesson Template

Use this template when creating a new lesson. Copy the folder structure and fill in
the content. Every code block in the lesson must run standalone with Python 3.10+
standard library only.

## Folder Structure

```
NN-lesson-name/
├── docs/
│   └── en.md              (lesson documentation)
├── code/
│   ├── main.py            (computational verification script)
│   └── exercises.py       (self-grading exercises — TODO stubs + checker)
└── quiz.json              (pre/check/post question pools)
```

## Documentation Format (docs/en.md)

Sections appear in this exact order — Pre-Lesson Check and Test Your Understanding
are REQUIRED because the build inserts interactive quiz mounts under those exact
headings (`Pre-Lesson Check`, `Test Your Understanding`):

```markdown
---
title: Lesson Title
type: Build | Learn
prerequisites: []
time: 45
---

# Lesson Title

> One-line motto — the core idea that sticks.

## Learning Objectives

4 bullets: concrete capabilities the learner gains. "Explain…", "Implement…",
"Prove…", "Decide when…".

## Pre-Lesson Check

Answer before reading — the explanations point at the section covering each idea.

*(Questions render below — three drawn at random from a larger pool each visit.)*

## The Problem

2-3 paragraphs. A concrete scenario where not knowing this hurts.

## The Concept

Definitions, intuition, ASCII diagrams, small worked examples.

## Build It

Computational verification. Enumerate small cases, check identities, simulate.

## Prove It

A guided proof of the central theorem, plus one proof left as an exercise.

## Connect It

Ties the topic to CS, AI/ML engineering, and systems practice — concrete named
mechanisms (one-hot encoding, boolean masks, NOT EXISTS, train/test splits), not
vague gestures.

## Test Your Understanding

Answer after working through the lesson.

*(Questions render below — four drawn at random from a larger pool each visit.)*

## Exercises

Completed AT THE COMPUTER in code/exercises.py. List each TODO function with its
difficulty and what the self-grader checks. No pen-and-paper-only exercises.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
```

## Exercises File Guidelines (code/exercises.py)

- Same style as main.py: stdlib only, runs with `python3 exercises.py`
- Each exercise is a function stub raising `NotImplementedError`, with a docstring
  stating the task and hint
- A `main()` self-grader prints PASS/FAIL per exercise and a final
  `ALL EXERCISES COMPLETE` banner ONLY when every check passes
- Checks compare the learner's function against brute force or a property, never
  against a hardcoded single answer
- Difficulty ladder: easy (reinforce), medium (apply), hard (prove or build a tool)

## Quiz File Format (quiz.json)

```json
{
  "lesson": "NN-lesson-slug",
  "title": "Lesson Title",
  "questions": [
    {
      "stage": "pre",
      "question": "…",
      "options": ["…", "…", "…", "…"],
      "correct": 1,
      "explanation": "1-2 sentences; name the lesson section to re-read."
    }
  ]
}
```

Authoring rules:

- **Pools, not fixed sets:** at least 5 `"pre"` questions and 6 `"post"` questions.
  The site shows 3 pre / 4 post, drawn and shuffled at random per page load —
  larger pools are what defeat memorization. Add `"check"`-stage questions only if
  a mid-lesson checkpoint is wanted.
- Exactly 4 options, exactly one correct (`correct` is the 0-based option index).
- Questions grounded in THIS lesson's text — definitions, proofs, and code from it,
  not general knowledge.
- Distractors plausible but clearly wrong to someone who studied; no joke answers.
- Question text 1–2 sentences. Explanations 1–2 sentences and reference the section
  (or the code file) to re-read.
- Pre-questions test prerequisites and intuition; post-questions test the lesson's
  actual content, including results proven in Prove It and verified in code.

## Front-Matter Reference

| Field | Meaning |
|---|---|
| `title` | Lesson title, shown in the catalog |
| `type` | `Build` (hands-on) or `Learn` (reading-focused) |
| `prerequisites` | list of lesson folder names, e.g. `[03-propositional-logic]` |
| `time` | estimated minutes to complete |
