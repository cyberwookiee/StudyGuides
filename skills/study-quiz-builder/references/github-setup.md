# One-time GitHub setup for quiz publishing

Read this when the user has no GitHub account or repo for quizzes yet, or isn't sure what owner, repo or Pages mean. Walk them through it in plain language, one part at a time, and wait for them to finish each part before moving on. They do the clicking; you explain. GitHub's menus change occasionally, so if a label doesn't match what they see, help them find the closest equivalent rather than insisting.

## What they're setting up (say this first, briefly)

GitHub is a free site for storing files. GitHub Pages turns a folder of files into a public website for free. Each quiz becomes one page on that site, at an address like `https://their-username.github.io/StudyGuides/biology/cells/`. Anyone with the link can open it, so quizzes never contain names or school details.

## Part 1: Create a GitHub account (skip if they have one)

1. Go to github.com and choose **Sign up**.
2. Pick a username. It appears in every quiz link, so suggest something they're comfortable sharing and that isn't the student's name.
3. Verify the email address GitHub sends.

## Part 2: Create the repository

A repository ("repo") is a folder on GitHub.

1. Signed in, click **+** in the top-right corner, then **New repository**.
2. Name it something like `StudyGuides`.
3. Choose **Public**. Free GitHub accounts can only publish Pages sites from public repos.
4. Check **Add a README file**, so the repo starts with a `main` branch.
5. Click **Create repository**.

## Part 3: Turn on GitHub Pages

1. In the new repo, open **Settings** (the tab along the top of the repo).
2. In the left sidebar, choose **Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Set **Branch** to `main` and the folder to `/ (root)`, then **Save**.
5. After a minute or two, the page shows the site address. The first quiz will appear underneath it.

## Part 4: Let Claude publish to the repo

Claude needs permission to add files to the repo.

- **In the Claude app (claude.ai):** connect GitHub from the app's settings under Connectors, and give it access to this repo. If Claude later reports that access was refused, the message names what to change; follow that.
- **In Claude Code or another setup:** the GitHub access configured there (for example the `gh` CLI being signed in) needs push access to the repo.

## Part 5: Commit author (optional)

Each published change is labeled with an author. To keep a personal email address off the public history, use GitHub's private "noreply" address:

1. On GitHub, open the profile menu → **Settings** → **Emails**.
2. Turn on **Keep my email addresses private**. GitHub then shows the noreply address, which looks like `12345678+username@users.noreply.github.com`.
3. Give Claude that address along with the username. If they skip this, Claude uses `username@users.noreply.github.com`.

## When they're done

Collect the owner (their username, or an organization name if the repo lives under one), the repo name, the branch (`main` unless they chose otherwise) and the commit author, save them as described in the skill's step 1, and continue building the quiz.
