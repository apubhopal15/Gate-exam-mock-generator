# GATE 2026 ECE — Mock Test (Web App)

A subject-wise GATE-level mock test for Electronics & Communication Engineering, built as a static web app. Questions and answer keys are kept in **separate files** so the quiz app can grade without exposing answers in the same file as the questions.

## What's inside

```
gate2026-mock/
├── docs/
│   └── index.html              <- the quiz app (this is what gets "served")
├── data/
│   ├── questions_*.json        <- 9 subject files, questions only (no answers)
│   └── answers_*.json          <- 9 matching answer-key files (answer + explanation)
└── README.md
```

Current content: **280 questions** across all 9 GATE ECE subjects (Engineering Mathematics, Networks/Signals/Systems, Electronic Devices, Analog Circuits, Digital Circuits, Control Systems, Communications, Electromagnetics, General Aptitude). More questions can be added later — just drop a new `questions_<subject>.json` / `answers_<subject>.json` pair into `data/` and add the subject name to the `SUBJECTS` array in `docs/index.html`.

## How to upload this to GitHub

1. **Create a new repository** on github.com (e.g. `gate2026-mock-test`). Don't initialize it with a README (we already have one).

2. On your computer, open a terminal in the `gate2026-mock` folder and run:

```bash
git init
git add .
git commit -m "Initial GATE 2026 ECE mock test"
git branch -M main
git remote add origin https://github.com/<your-username>/gate2026-mock-test.git
git push -u origin main
```

3. That's it — your code is now on GitHub.

## How to "run it as a server" (GitHub Pages — no backend needed)

Since this is a static quiz app (HTML + JSON, no database), GitHub Pages can serve it directly for free:

1. In your GitHub repo, go to **Settings → Pages**.
2. Under "Source", choose **Deploy from a branch**.
3. Select branch `main` and folder `/docs`, then click **Save**.
4. After a minute, GitHub will give you a live URL like:
   `https://<your-username>.github.io/gate2026-mock-test/`

Open that link — the quiz app will load `questions_*.json`, let you attempt each question, and grade you against `answers_*.json` when you click **Submit Test**.

## Notes

- All content here is original, written specifically for this project — safe to make public.
- If you want a real backend later (user login, saved scores across devices, leaderboard), that would need a small server (Node/Express + a database) rather than GitHub Pages — let me know if you want that built out.
