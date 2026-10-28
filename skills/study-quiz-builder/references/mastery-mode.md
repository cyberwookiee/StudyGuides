# Mastery mode

Read this when building a mastery quiz. The page shows one question at a time. The student checks each answer and sees right or wrong with an explanation right away. Each sub-topic keeps going until the student gets `RULES.streak` right in a row (mastered, move to the next topic) or reaches `RULES.max` questions (marked for more practice, move on). A student who knows everything finishes in `topics × streak` questions; one who struggles can see up to `topics × max`. The results screen lists each topic's status and offers to practice only the topics that need work.

The engine is `assets/mastery-template.html`. It is a complete, tested quiz on Algebra 2 Unit 1 (five topics), so read its `TOPICS` array as the worked example.

## What to change in the template

Change only these parts, and leave the engine code below the `---------- grading ----------` comment alone:

- `<title>`, header eyebrow, `<h1>`, intro paragraph. Keep the `data-rule` spans in the intro so it always states the real rules.
- `const KEY`: a unique storage key, `<repo>-<subject>-<course>-<unit>-<quiz>-v1`.
- `const RULES={streak:3,max:20,retryGap:3}`: keep the defaults unless the user asks otherwise. Streak 3 is the default because two lucky guesses on true/false happen 25% of the time, three only 12.5%; use 2 only if the user wants shorter sessions.
- `TOPICS`: replace the sample topics with the unit's sub-topics.
- The sample's helpers for its own figures (`gx`, `gG`, `drGraph`, `ineq`): delete them if the new quiz doesn't use them. Keep `G`, `P`, `M`, `n`, `lin`, `sh`, `pk`, `coef`, `OPH`, `mcOpts` and `rng`; generators use them.
- The typing guide (`<details class="guide">`): drop entries for answer types the quiz doesn't use; add a short-answer entry if it uses `text`.

## Topics

Use 4 to 8 sub-topics, each a single skill or idea a student can be "done" with: "Solving absolute value equations", "Causes of the Civil War", "Parts of the cell". Order them the way the class learned them, because students work through them in order. A topic that mixes two skills makes the streak meaningless, so split it.

Each topic is `{name, qs:[...], gen:[...]}` and needs enough distinct questions that a struggling student doesn't see the same one again and again:

- `qs`: fixed questions, written exactly like classic-mode questions but without `s`. A missed fixed question can return after `retryGap` other questions, so it gets a second chance after the student has seen the explanation.
- `gen`: generator functions `r => question`, producing a fresh variant each time. Use them for any skill with a computable answer (math, unit conversions, chemistry stoichiometry, physics formulas, dates arithmetic). One generator per question style; 2 to 4 per topic gives good variety.

Aim for at least one generator per computational topic, and at least 10 fixed questions per topic that has no generator (vocabulary, history, literature). Mix question types within a topic and avoid a topic made only of true/false, which is easy to guess through.

## Question types

Same as classic mode (`mc`, `tf`, `num`, `nums`, `interval`, `expr`), plus a built-in `text` type for short answers: `acc` (array of accepted answers, including alternate spellings), `ans` (display). The `text` grader ignores capitals, punctuation, extra spaces and a leading "the/a/an", reads number words as digits, and forgives one typo in answers longer than 6 characters.

Multiple-choice options are shuffled every time a question is shown, so explanations must not refer to option letters. Set `keep:true` on a question to stop shuffling. Graph-option questions (`go:true`) are never shuffled.

## Writing generators

A generator receives a seeded random source `r` and returns one question object. The seed is saved, so after a reload the same question comes back identically. Never use `Math.random()` inside a generator.

- `r.int(lo, hi)` inclusive integer, `r.nz(lo, hi)` non-zero integer, `r.pick(array)`, `r.shuffle(array)`, `r.next()` in [0, 1).
- `mcOpts(r, correct, [wrong, ...])` returns `{o, a}`: drops duplicates of the correct answer, keeps up to three wrong options, shuffles. Pass 4 or 5 candidates so duplicates still leave 3 wrong ones.
- Formatting: `n(v)` prints negatives with a real minus sign; `lin(a, b)` prints `3x − 5`, `x`, `−x + 2` without "1x" or "+ −"; `sh(h)` prints `x − h` or `x + |h|`; `pk(k)` prints ` + k`, ` − |k|` or nothing; `coef(a)` prints a coefficient, empty for 1 and `−` for −1.

Design rules that keep generators correct:

1. **Build from the answer backwards.** Pick the answer first, then construct the problem so the answer is exact. For `|ax + b| = c` with integer solutions, pick the center `m` and distance `d`, then set `b = −a·m` and `c = a·d`. This avoids fractions and impossible cases.
2. **Keep numbers in a friendly range** that matches the class material (usually −10 to 10), and avoid degenerate cases with `r.nz` (a zero coefficient, a shift of 0 that makes the question trivial).
3. **Wrong options come from real mistakes**: wrong sign, forgot to distribute, flipped direction, forgot to flip the inequality, used the wrong piece.
4. **Explanations compute with the same numbers** the question shows, step by step, and name the mistake to avoid.
5. **Keep figures inside their window.** When a generator draws a graph with `G`, choose the domain so the curve stays on the grid.

Worked example from the sample (absolute value equations):

```js
r=>{const a=r.int(1,3),m=r.int(-5,5),d=r.int(1,6),b=-a*m,c=a*d;
  return{t:'nums',q:`Solve ${M(`|${lin(a,b)}| = ${c}`)}.`,a:[m+d,m-d],ans:`${n(m+d)}, ${n(m-d)}`,
    ex:`Split into two cases. ${M(`${lin(a,b)} = ${c}`)} gives ${M(`x = ${n(m+d)}`)}, and ${M(`${lin(a,b)} = −${c}`)} gives ${M(`x = ${n(m-d)}`)}.`};}
```

For non-computational subjects, generators can still add variety by combining facts: for example, pick two events from a list of dated events and ask which came first, or pick a term from a vocabulary table and build multiple choice from its definition and three other definitions. Keep the table of facts in the topic and check every fact against the class material.

## Verifying

Run `python3 scripts/check_mastery.py <path>/index.html` from the skill folder. It:

- builds every fixed question and 400 variants of every generator and confirms each answer key grades correct, an obvious wrong answer grades wrong, multiple choice has 3+ distinct options, and no text shows `undefined`, `NaN`, "1x" or "+ −";
- plays the quiz as a student who is always right (expects `topics × streak` questions), always wrong (expects every topic to stop at `max` and be marked for practice), then practices the missed topics;
- checks that a draft answer and a checked answer survive a reload, that the page never scrolls sideways at phone widths, and that there are no script errors.

It must print `RESULT: PASS`. Fix every failure and rerun. Also read a printed sample of each generator's output (question, answer, explanation) for a few seeds to check the wording and the math make sense; the script proves the key matches the grader, not that the question is good.
