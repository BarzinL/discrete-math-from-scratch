# UX Notes — translating ai-engineering-from-scratch

Scratch notes on how the upstream site
(https://github.com/rohitg00/ai-engineering-from-scratch) actually works, gathered
from its source (`site/style.css`, `site/app.js`, `api/lesson.js`, lesson
front-matter, `quiz.json` files, and the `.claude/skills/` authoring guides).
Purpose: decide what we translate, what we adapt, and what we deliberately skip.
MIT-licensed, so copying tokens and patterns is fine with attribution (in LICENSE).

## 1. Design tokens (from site/style.css `:root`)

- Fonts: `VT323` (pixel display, all headings, weight 400, uppercase),
  `Source Serif 4` (body, 18px/1.62), `JetBrains Mono` (labels, code).
- Palette: paper bg `#fafaf5`, surface `#f3f1e8`, ink `#1a1a1a` (soft `#4a4a4a`,
  mute `#7a7a78`), blueprint `#3553ff` + tint alphas 0.08/0.18.
- Hard offset shadows: `3px 3px 0 var(--ink)` (lg: `5px 5px 0`) — the signature
  brutalist-print look. Borders are 1px solid ink or `--rule-soft`.
- Dot-grid page background: `radial-gradient(paper-rule 1px, transparent 1px)`
  at 16px grid, `background-attachment: fixed`.
- `.ascii-rule`: two-layer repeating-linear-gradient divider (4px blue dashes
  over 6px tint dashes) — used as section break.
- Dark theme = full token swap under `[data-theme="dark"]` (bg `#0a0d1a`,
  blueprint `#6b8eff`); no component restyles.
- Motion grammar tokens: `--motion-press: 160ms`, `--motion-enter: 220ms`,
  `--ease-out: cubic-bezier(0.23,1,0.32,1)`; everything respects
  `prefers-reduced-motion`.

## 2. Lesson page anatomy (from api/lesson.js + a rendered lesson)

Order on a lesson page:
1. Fixed header (64px): logo (blue square icon + pixel-font wordmark), mono
   uppercase nav, GitHub stars chip, search + theme toggles.
2. Left sidebar: "FULL COURSE CATALOG", phase groups, lesson list; current
   lesson highlighted (blue text + tint bg); completed lessons get a checkbox.
3. Hero: phase number label, pixel-font title, then an **"Act on this lesson"
   checkpoint panel** — 5 cells: READ / BUILD / RUN / PROVE / CONTINUE. The
   active cell is solid blue; cells flip as the learner marks progress. Progress
   is separate from quiz correctness ("Each checkpoint is yours to mark").
4. Meta chips row: LOCAL PROGRESS · phase tag · PATH 730 MIN · LESSON 45 MIN.
5. "RUN FROM THE REPOSITORY" card: exact copyable command + COPY COMMAND button.
6. Motto blockquote, then content sections, each deep-linkable; right rail =
   "ON THIS PAGE" TOC with the active section highlighted.
7. Quiz section(s) rendered from `quiz.json` (see §3).
8. Exercises with **Hints** subsections (per-exercise, full walkthrough hints).

## 3. Quiz system (from quiz.json + .claude/skills/check-understanding)

- Location: `<lesson-dir>/quiz.json`, one per lesson.
- Schema: `{lesson, title, questions: [{stage, question, options[4], correct,
  explanation}]}`. `stage` ∈ `"pre"` | `"check"` | `"post"`.
  `correct` is the option index.
- Authoring rules from their skill (we adopt these verbatim as our standards):
  questions grounded in the lesson text, not general knowledge; 4 options,
  exactly one correct; distractors plausible but clearly wrong to a studier;
  no joke answers; explanation 1–2 sentences; keep question text 1–2 sentences.
- Their runtime presents questions one at a time, hides the answer until
  response, tracks a tally, grades with bands (7-8 Mastered / 5-6 Almost /
  3-4 Developing / 0-2 Start Over), shows per-wrong-answer breakdown with the
  lesson section to re-read, and offers retake with fresh questions.

## 4. What we adopt NOW (done in this pass)

- quiz.json per lesson with pre/check/post stages — same schema.
- Pre-Lesson Check + Test Your Understanding sections in every lesson doc.
- **Our upgrade over upstream: randomization.** Pools are larger than shown
  (pre: pool of 5 → 3 shown; post: pool of 6 → 4 shown); both question order
  and option order shuffle per page load, so retakes don't reward memorizing
  positions.
- Learning Objectives section (their front-matter has it; ours now too).
- Code Connections section — ours, not theirs: ties each topic to CS/AI/ML
  practice (sets→one-hot encodings, logic→boolean masks, quantifiers→data
  validation, etc.).
- Interactive exercises: `code/exercises.py` per lesson, TODO stubs +
  self-grading main printing PASS/FAIL — no pen and paper required.
- Design tokens + hard shadows + dot grid + ascii-rule (in tools/style.css).

## 5. Adopt LATER (queued, not built)

- Checkpoint panel (Read/Build/Run/Prove/Continue) — needs localStorage + a
  bit of JS; natural second JS component after quiz.js.
- Copy-command card under the lesson title.
- Dark theme — pure token swap in our stylesheet, add a toggle when we add
  localStorage.
- "On this page" scroll-spy highlighting (we have the static TOC already).
- Command palette (Cmd+K) — their `site/cmdpalette.js` is 30KB; only worth it
  past ~20 lessons.
- Score bands + wrong-answer breakdown with "re-read section X" links —
  quiz.js v2.
- Hints subsections in exercises (progressive disclosure via `<details>`).
- TTS "read aloud" bar — low priority.

## 6. Skip deliberately

- i18n (32 languages), sponsors, blogs, certifications, command-palette JS
  complexity, 30+ figure helper files, Vercel serverless API — out of scope
  for a lean static site.
