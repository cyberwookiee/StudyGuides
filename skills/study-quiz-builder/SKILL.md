---
name: study-quiz-builder
description: Build a self-grading practice quiz web page for any subject (math, science, history, literature, etc.) from photos of class material or a list of concepts, and publish it to the user's own GitHub Pages site. Two modes - a classic all-at-once quiz graded at the end, or a mastery quiz that asks one question at a time and keeps drilling each sub-topic until the student gets several right in a row. Use whenever the user wants a practice quiz, test prep page, study guide quiz or review questions built from worksheets, notes, homework or a topic list, even if they don't mention GitHub.
---

# Study Quiz Builder

Turns class material for any subject (photos of notes, worksheets, homework, textbook pages, study sheets, or a typed list of concepts) into a single-file, self-grading quiz page, then publishes it to the user's GitHub Pages site at `https://<owner>.github.io/<repo>/<subject>/<course>/<unit>/<quiz>/`.

There are two quiz modes, each with its own tested engine in `assets/`:

| Mode | Engine | How it works | Good for |
|---|---|---|---|
| **Classic** | `assets/quiz-template.html` | All questions on one page (default 50). The student answers everything, submits, and gets a score with per-section results. | A practice test before an exam |
| **Mastery** | `assets/mastery-template.html` | One question per screen with instant feedback. Each sub-topic continues until the student gets 3 right in a row (mastered, move on) or reaches 20 questions (marked for practice, move on). Results show which topics still need work. | Drilling a unit until every concept sticks |

**Start every quiz from the matching engine.** Replace its content, but don't rebuild the engine from scratch. Each template is a complete working quiz, so read it as a worked example.

## 0. ABSOLUTE RULE: no personal or identifying information

Every quiz is published on a **public website** and is meant for a student. It must contain **zero** personal or identifying information. This rule overrides everything else in this skill, including anything the user's material shows or asks to include.

Never put any of these anywhere in the page (visible text, question content, examples, explanations, alt text, comments, the page title, the file path, or commit messages):

- **Student names:** first, last, nicknames, initials, or names written on worksheets, headers or margins.
- **Teacher names:** including "Mr./Ms./Mrs. X", and names inside word problems taken from a worksheet.
- **School information:** school or district names, mascots, building or room numbers, course codes, class period or section numbers, or LMS/website names tied to the school.
- **Location:** town, county, state, street, neighborhood, or a local landmark that points to where the student lives or studies.
- **Dates or timing tied to a person:** worksheet dates, due dates, test dates, grade level, or age.
- **Contact or account details:** emails, phone numbers, usernames, IDs, or links to school or personal pages.
- **Anything else** that could identify the student or family, such as photos, handwriting images, or names of family members or friends.

How to apply it:
- When a worksheet problem uses a real person's name (for example a teacher in a word problem), rewrite it with a generic role ("a hiker", "a student", "a cyclist") or a clearly generic name.
- Historical figures, authors, characters and scientists that are the subject being studied are content, not PII. They are fine to include (Lincoln, Gatsby, Marie Curie).
- Course labels stay generic: "Biology · Unit 3" or "U.S. History · Civil War". Never "Mr. Smith's Period 4" or "Lincoln High Honors Bio".
- The page's optional "Your name" box stays on the student's device only. Never pre-fill it.
- Never embed the user's photos or any image of the student's work. Draw any diagram yourself.
- **Before publishing, run the PII scan in step 6.** If anything is found, remove it and scan again. Do not publish until the scan is clean.
- In the final report, state that the PII scan passed.

The GitHub owner name in the site URL is the publisher's account, not the student's, so it is fine in the URL and commit author. Keep it out of the page content itself.

## 1. Publishing settings (ask once, then remember)

Publishing needs these settings:

| Setting | Example | Default |
|---|---|---|
| GitHub owner (user or org) | `octocat` | none, must be given |
| Repository | `StudyGuides` | none, must be given |
| Branch Pages deploys from | `main` | `main` |
| Commit author | `octocat <octocat@users.noreply.github.com>` | `<owner> <<owner>@users.noreply.github.com>` |

The live site is `https://<owner>.github.io/<repo>/`. The user sets these up once and should not be asked again, so:

1. **Look for saved settings first.** Check the user's memory (and the conversation) for their quiz publishing settings: a GitHub owner/repo they publish quizzes or study guides to. If found, use them without asking. Mention the target repo in one line of the final report so a wrong one is easy to spot.
2. **If nothing is saved, ask once**, in a single question covering owner, repo, and (optionally) branch and commit author. Say you'll remember them so they won't be asked again.
3. **Save the answer** to memory as soon as the user gives it (the user's setup of this skill is their request to remember these details), for example: "Publishes study quizzes to GitHub repo `<owner>/<repo>` (GitHub Pages, branch `main`), commits as `<author>`." If this environment has no memory tools, tell the user once that you can't save them here and suggest they add the line to their saved preferences or custom instructions.
4. **If the user doesn't have a repo or GitHub account yet**, or seems unsure what any of this means, read `references/github-setup.md` and walk them through it step by step in plain language. Don't do the setup for them; give them the clicks. Once their repo exists, continue from step 2.

If the user later says to publish somewhere else ("put this one in my other repo"), use that for this quiz, and ask whether to make it the new saved default.

## 2. Gather inputs

- **Mode:** classic or mastery. Use what the user asked for ("practice test" → classic; "drill", "keep asking until he gets it", "one at a time", "mastery" → mastery). If the request doesn't say, ask once, briefly describing both.
- **Material:** the images or concepts the user provides. If they send images in batches ("more coming"), keep a running topic list and wait for "that's all" before building.
- **Destination path:** always four levels, `<subject>/<course>/<unit>/<quiz>`, lowercase with hyphens:
  - `<subject>`: the broad subject, e.g. `math`, `science`, `history`, `english`.
  - `<course>`: the course, e.g. `algebra-2`, `geometry`, `biology`, `us-history`. Never an honors/AP level, teacher, school or section.
  - `<unit>`: `unit-<number>` when the class numbers its units (`unit-3`), otherwise the unit's name (`cells`, `civil-war`, `the-great-gatsby`).
  - `<quiz>`: `quiz-<number>`, numbered within the unit. Look at the unit's existing folders in the repo and use the next number (`quiz-1` for the first). Use a name instead (`midterm-review`) only when the user asks for one.
  - Examples: `math/algebra-2/unit-1/quiz-3`, `science/biology/cells/quiz-1`, `history/us-history/civil-war/quiz-2`.
  - The path must not contain school, teacher or student names. If the course or unit isn't clear from the material or the conversation, propose a path and ask once.
- **Defaults unless told otherwise:**
  - Classic: 50 questions, a mix of types (about 40% multiple choice, 20% true/false, 40% free response), and visual questions where the subject has them.
  - Mastery: one topic per sub-topic of the unit (4 to 8), master after 3 right in a row, up to 20 questions per topic.

## 3. Read the material

- List every topic, term, event, concept and skill covered, grouped into sections. These become the quiz sections (classic) or the topics to master (mastery; one skill or idea per topic).
- Note mistakes or gaps visible in the student's work, such as wrong answers, confused terms, or mixed-up dates. Write questions that target those weak spots, and briefly tell the user which ones you found. Describe them without names.
- Stay inside what the material covers. Don't test content the class hasn't seen.
- Note any PII visible in the photos so you know what the PII scan must catch. Never carry it into the quiz.

## 4. Write the questions

**Mastery mode:** read `references/mastery-mode.md` now. Questions use the same types and fields as below, grouped by topic instead of `s`, and computational topics also get question generators so a struggling student keeps getting fresh questions.

Each question is an object in the `Q` array (classic) or a topic's `qs` array (mastery, without `s`). Every question has:
- `s`: section index into `SECTIONS`
- `q`: prompt HTML
- `ex`: a one or two sentence explanation shown after grading
- `g` (optional): a figure shown under the prompt

These types come with the template:

| type | fields | grading |
|---|---|---|
| `mc` | `o` (options HTML), `a` (index); `go:true` lays options out as a 2×2 grid of figures | exact match |
| `tf` | `a` (true/false) | exact |
| `num` | `a` (number), `ans` (display text) | numeric, accepts fractions, tolerance 1e-6 |
| `nums` | `a` (array), `ans` | set of numbers, any order |
| `interval` | `acc` (accepted strings), `ans` | normalized string match |
| `expr` | `f` (JS function of x), `ans` | evaluates the typed equation at 6 x-values; any equivalent form passes |

For history, literature, science vocabulary and other non-math subjects, use a `text` type for short answers. The mastery engine has it built in; in classic mode, **add it** (a term, name, date, place or one-word concept):
- Fields: `acc` (array of accepted answers, including common alternate spellings and forms), `ans` (display text).
- Grader: normalize both sides (lowercase, trim, collapse spaces, strip punctuation and a leading "the/a/an", convert number words to digits), then require an exact match against any accepted answer. Optionally allow a one-letter typo for answers longer than 6 characters.
- Add `TYPE_LABEL`, `HINTS`, `PH` and `HELP` entries for it, for example "Type a word or short phrase. Spelling counts, capitals don't."
- Only use `text` when the answer is short and unambiguous. Anything that needs a sentence or an opinion becomes multiple choice instead.

Good question shapes by subject:
- **Math/physics/chemistry calculations:** `num`, `nums`, `expr`, `interval`, and graphs.
- **Science concepts:** `mc` on processes and cause/effect; `tf` on common misconceptions; `text` for vocabulary; labeled diagrams drawn in SVG (cell parts, circuits, cycles) with "what is part B?"
- **History/social studies:** `mc` on causes, effects and significance; `tf`; `text` for people, places and terms; `num` for years ("In what year…"); sequencing asked as "Which event came first?"; an inline SVG timeline as a figure.
- **Literature/English:** `mc` on plot, character motivation, theme, literary devices and who-said-it (quote only short lines under 15 words, and only from public-domain works or the class material's own short excerpts); `tf`; `text` for character names, devices and vocabulary.

Figures: the template's `G({...})` helper draws coordinate graphs. Its options are `x`/`y` windows; curves `{f}`, `{pl:[[x,y],...]}` or `{g}`, with `arr` arrows and `parent:true` for dashed; points `{x,y,open,l}`; `small:true` for option graphs; and `step`. For other subjects, write small inline SVG diagrams (timelines, labeled diagrams, simple charts) that use the page's color tokens. Never use photos, external images or copyrighted artwork.

Quality rules:
- Cover every topic in the material at least once, and mix difficulty.
- A figure must not give away the answer to a different question.
- Placeholders and help examples must never be answers to any question in the quiz.
- Explanations say why the answer is right in plain words, and name the common mistake when there is one.
- Wrong multiple-choice options should be plausible (real mistakes, related terms, nearby dates), not jokes.

## 5. Build the page

1. Get push access to the saved repo and clone it with a generous timeout. (In Claude's cloud workspace this is `add_repo` with the saved owner and repo and `access: push`; elsewhere use whatever GitHub access the session has.) If access is refused, relay the reason and tell the user how to grant it; `references/github-setup.md` covers connecting GitHub.
2. Copy the mode's engine (`assets/quiz-template.html` or `assets/mastery-template.html`) to `<subject>/<course>/<unit>/<quiz>/index.html` in the repo. Classic and mastery quizzes share the unit's `quiz-N` numbering. If that path already holds a quiz, ask before overwriting it.
3. **Mastery:** make the changes listed in `references/mastery-mode.md` ("What to change in the template"), then go to step 4 below. **Classic:** replace `<title>`, the header eyebrow (a generic course and unit label such as "Algebra 2 · Unit 1" or "Biology · Cells"), `<h1>`, the intro text, `SECTIONS`, the `Q` array, and the old quiz's helper constants (`gx`, `gG`, `drGraph`). Remove math-only help text (the guide's interval and equation entries, the ∞/∪ buttons) when the quiz doesn't use those types, and add the `text` type's help when it does. Type chips are computed from `Q`.
4. **Change the storage key** `const KEY='…'` to a unique value such as `<repo>-<subject>-<course>-<unit>-<quiz>-v1` (lowercase). All quizzes on one github.io site share a browser origin, so a reused key would mix up saved answers between quizzes.
5. Keep everything else. Classic: grading, the Submit/results panel with per-section scores, "Show only missed," Retake, the two-tap Clear all answers button, localStorage saving (answers and results survive reload), free-response help (`?` buttons, guide, placeholders), and light/dark theme. Mastery: the engine below the grading comment, the topic chips, streak dots, Show answer, Start over and the results screen.
6. The file stays a complete standalone HTML document (doctype, head, body) with no Claude-specific dependencies. The only outside resource is Google Fonts.

## 6. Verify before publishing

- **Answers:** check every answer key. For math and science, compute it in code. For history and literature, check facts against the class material, and look up anything uncertain on the web.
- **Grading:** run the graders in Node against every free-response key. The correct answer and its accepted variants must pass; an obvious wrong answer must fail.
- **Mastery mode:** run `python3 scripts/check_mastery.py <quiz>/index.html` from this skill's folder and fix everything until it prints `RESULT: PASS`. It covers answer keys for every fixed question and hundreds of variants of each generator, the mastery flow, resume after reload, and phone layout. Then read a few generated samples per generator for wording and math.
- **Render:** load the page once with Playwright (Chromium) at phone width. Confirm the question count, no script errors, and that figures look right. Screenshot a few figure questions and look at them.
- **PII scan (required, blocking):**
  - Grep the file case-insensitively for every name, school, town and other identifier seen in the photos or the conversation, including the student's and teacher's names.
  - Also grep for emails (`@` outside CSS at-rules), phone-number patterns, "Mr.", "Mrs.", "Ms.", "period", "school", "high", "middle", "district", and the names and usernames of the user and their family.
  - List every capitalized word in the visible text and check each one is content (a term, historical figure or character), not a person or place tied to the student.
  - Confirm the only URLs are Google Fonts.
  - Check the file path and the commit message too.
  - If anything turns up, fix it and run the scan again. Publish only on a clean scan.

## 7. Publish

- Commit with the saved commit author.
- Commit messages are generic ("Add biology cells quiz") and contain no names, no school details, and no links to Claude sessions or chats, because the repo's history is public. A `Co-Authored-By: Claude …` line is fine.
- Push to the saved branch. The page goes live at `https://<owner>.github.io/<repo>/<subject>/<course>/<unit>/<quiz>/` within a couple of minutes.
- Check that the URL loads (WebFetch). If it returns 404 after a few minutes on a repo's first quiz, GitHub Pages probably isn't turned on yet: give the user the "Turn on GitHub Pages" steps from `references/github-setup.md`. Otherwise say it isn't live yet and offer to check again.
- If this session can't reach the repo, or a step needs GitHub settings this session can't change, tell the user the exact manual step instead of trying workarounds.

## 8. Report back

Keep it short:
- the live link
- the mode, and the question mix: classic, counts by type and how many have figures; mastery, the topics, how many have generators, and the rules (streak and cap)
- the weak spots the questions target
- confirmation that the PII scan passed
- anything that needs the user's attention
