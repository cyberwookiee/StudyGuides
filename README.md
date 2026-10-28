# StudyGuides

Self-grading practice quizzes, published with GitHub Pages at **https://cyberwookiee.github.io/StudyGuides/**.

Each quiz is a single web page that runs in any browser, including on a phone. It grades answers instantly and saves progress on the device. Nothing is sent anywhere, and no account is needed.

## Quizzes

| Course | Unit | Quiz | Type |
|---|---|---|---|
| Algebra 1 | Sequences and patterns | [Quiz 1](https://cyberwookiee.github.io/StudyGuides/math/algebra-1/sequences-and-patterns/quiz-1/) | Practice test |
| Algebra 2 | Unit 1 | [Quiz 1](https://cyberwookiee.github.io/StudyGuides/math/algebra-2/unit-1/quiz-1/) | Practice test |
| Algebra 2 | Unit 1 | [Quiz 2](https://cyberwookiee.github.io/StudyGuides/math/algebra-2/unit-1/quiz-2/) | Practice test |
| Algebra 2 | Unit 1 | [Quiz 3](https://cyberwookiee.github.io/StudyGuides/math/algebra-2/unit-1/quiz-3/) | Practice test |

There are two kinds of quiz:

- **Practice test:** all the questions on one page. Answer everything, submit, and see a score with results by section.
- **Mastery drill:** one question at a time with instant feedback. Each topic keeps going until 3 answers in a row are right, up to 20 questions per topic. [Try a sample](https://cyberwookiee.github.io/StudyGuides/skills/study-quiz-builder/assets/mastery-template.html).

## How the repo is organized

Every quiz lives at `<subject>/<course>/<unit>/<quiz>/index.html`:

```
math/
  algebra-1/sequences-and-patterns/quiz-1/
  algebra-2/unit-1/quiz-1/
skills/
  study-quiz-builder/
```

- `<subject>`: broad subject, such as `math`, `science` or `history`
- `<course>`: course name, such as `algebra-2` or `biology`
- `<unit>`: `unit-<number>` when the class numbers its units, otherwise the unit's name
- `<quiz>`: `quiz-<number>`, counting up within the unit

## How the quizzes are made

The quizzes are built by the **Study Quiz Builder** skill for Claude, which lives in [`skills/study-quiz-builder`](skills/study-quiz-builder). It turns photos of class material or a list of topics into a quiz, checks every answer key, and publishes it here.

- [Skill page and download](https://cyberwookiee.github.io/StudyGuides/skills/study-quiz-builder/)
- To use it, download `study-quiz-builder.skill` and upload it in Claude under **Settings → Capabilities → Skills**.

## Privacy

Everything here is public. Quizzes never include names, schools, teachers, locations or other personal details, and each one is scanned for them before it's published.

## Contributions

This is a personal repo, and only the owner publishes to it. Issues with corrections, such as a wrong answer key, are welcome.
