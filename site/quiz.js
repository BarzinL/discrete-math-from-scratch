/* Interactive lesson quizzes: draws a random subset from an embedded pool,
   shuffles question and option order, grades inline with explanations. */
(function () {
  "use strict";

  function shuffle(arr) {
    const out = arr.slice();
    for (let i = out.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [out[i], out[j]] = [out[j], out[i]];
    }
    return out;
  }

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  const LETTERS = ["A", "B", "C", "D"];

  function renderQuestion(container, q, index, total, onAnswered) {
    const perm = shuffle(q.options.map((text, i) => ({ text, original: i })));
    const box = el("div", "quiz-question");
    box.appendChild(el("p", "quiz-qnum", "Question " + (index + 1) + " of " + total));
    box.appendChild(el("p", "quiz-qtext", q.question));

    const feedback = el("div", "quiz-feedback");
    let answered = false;

    perm.forEach(function (opt, position) {
      const btn = el("button", "quiz-option");
      btn.type = "button";
      btn.appendChild(el("span", "quiz-option-letter", LETTERS[position]));
      btn.appendChild(el("span", "quiz-option-text", opt.text));
      btn.addEventListener("click", function () {
        if (answered) return;
        answered = true;
        const correct = opt.original === q.correct;
        btn.classList.add(correct ? "is-correct" : "is-wrong");
        if (!correct) {
          const buttons = box.querySelectorAll(".quiz-option");
          buttons.forEach(function (b, pos) {
            if (perm[pos].original === q.correct) b.classList.add("is-correct");
          });
        }
        box.querySelectorAll(".quiz-option").forEach(function (b) {
          b.disabled = true;
        });
        feedback.appendChild(el("p", "quiz-verdict " + (correct ? "ok" : "no"),
          correct ? "Correct." : "Not quite."));
        feedback.appendChild(el("p", "quiz-explain", q.explanation));
        box.classList.add("is-answered");
        onAnswered(correct);
      });
      box.appendChild(btn);
    });

    box.appendChild(feedback);
    container.appendChild(box);
  }

  function mountQuiz(mount, pool, shown, title, results) {
    const section = el("section", "quiz");
    const heading = el("h2", "quiz-title", title);
    section.appendChild(heading);
    const picked = shuffle(pool).slice(0, shown);
    let correctCount = 0;
    let answeredCount = 0;

    picked.forEach(function (q, i) {
      renderQuestion(section, q, i, picked.length, function (correct) {
        correctCount += correct ? 1 : 0;
        answeredCount += 1;
        if (answeredCount === picked.length) {
          const summary = el("p", "quiz-summary",
            "You answered " + correctCount + " of " + picked.length + " correctly.");
          if (correctCount === picked.length) {
            summary.textContent += " Full marks — reload for a fresh set.";
          } else {
            summary.textContent += " Re-read the sections referenced above, " +
              "then reload for a fresh set of questions.";
          }
          section.appendChild(summary);
          results.push({ title: title, score: correctCount, total: picked.length });
        }
      });
    });

    mount.replaceWith(section);
  }

  function init() {
    const dataTag = document.getElementById("quiz-data");
    if (!dataTag) return;
    let data;
    try {
      data = JSON.parse(dataTag.textContent);
    } catch (err) {
      return;
    }
    const results = [];

    document.querySelectorAll(".quiz-mount").forEach(function (mount) {
      const kind = mount.getAttribute("data-quiz");
      if (kind === "pre" && data.pre && data.pre.pool.length) {
        mountQuiz(mount, data.pre.pool, Math.min(data.pre.shown, data.pre.pool.length),
          mount.getAttribute("data-title") || "Pre-Lesson Check", results);
      } else if (kind === "post" && data.post && data.post.pool.length) {
        mountQuiz(mount, data.post.pool, Math.min(data.post.shown, data.post.pool.length),
          mount.getAttribute("data-title") || "Test Your Understanding", results);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
