# discrete-math-from-scratch

Learn discrete mathematics. Prove it. Build it. Verify it.

A free, open-source curriculum where every lesson teaches a concept, walks through a
proof, and *verifies the math computationally* with small Python programs you can run
yourself. Inspired by [ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch)
(MIT) — same lesson-folder model, adapted for mathematics.

## How it works

- Every lesson is a folder under `phases/NN-phase-name/NN-lesson-name/` containing:
  - `docs/en.md` — the lesson itself (problem → concept → build → prove → connect)
  - `code/main.py` — a runnable, stdlib-only script that brute-forces small cases
    so you can *see* the theorem is true before reading the proof
- `python3 tools/build.py` walks the tree and generates a static site in `site/` —
  a catalog plus one page per lesson. No dependencies, no JavaScript framework.
- Preview locally: `python3 -m http.server 8000 --directory site` → http://localhost:8000

## Curriculum

| Phase | Topic | Lessons |
|---|---|---|
| 00 | Foundations (sets, logic) | 4 |
| 01 | Proof Techniques | 6 |
| 02 | Relations and Functions | 6 |
| 03 | Combinatorics | 8 |
| 04 | Number Theory | 7 |
| 05 | Graph Theory | 8 |
| 06 | Boolean Algebra and Circuits | 4 |
| 07 | Discrete Probability | 5 |
| 08 | Algorithms and Complexity bridge | 4 |

## License

MIT — see [LICENSE](LICENSE). The lesson model and site architecture are inspired by
[rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch),
which is MIT licensed. All lesson content here is original.
