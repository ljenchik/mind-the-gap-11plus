# Mind the Gap 11+

Maths practice for the Essex (CSSE) 11+ exam, for Year 5 children and their parents.
Not connected with or endorsed by CSSE.

## Folders (Netlify publishes the whole repository: `publish = "."`)
- `index.html` – the website's front page; `privacy.html`, `style.css`
- `app/` – the app: `index.html`, `config.js` (database and payment settings), `sw.js` (offline), `manifest.webmanifest`, icons,
  and `app/source/questions-cem.js` + `app/source/figures-more.js` (the papers 1–60 and extra topic questions, and their pictures)
- `netlify/functions/stripe-webhook.js` records payments; `supabase/schema.sql` the database. See `SETUP.md`.
- `source/` – what `app/index.html` is built from: `app-template.html.txt`, `questions.json`, `help.json`, `starter-data.json`,
  `questions-cem.js`, and the scripts that write and check questions.
- `site/` is a copy of the website (front page, privacy page and `app/`). Netlify is set to publish this folder, so it must always match the top-level files.

## Rebuilding the app
In a folder with `app-template.html.txt` (renamed `template.html`), `questions.json`, `help.json`, `starter-data.json`: run `build.py`.
Copy `index.html` to `app/`, and `questions-cem.js`, `figures-more.js` to `app/source/`. Change `VERSION` in `app/sw.js`.

## Wording (26 Nov)
`wording-fix.py.txt` (run in a folder with `questions.json` and `cem.json`, the CEM questions as JSON) keeps the wording plain:
"Work out" not "Calculate", no topic labels at the start of questions, no semicolons in worked answers, pictures instead of
written-out diagrams (L-shapes, Venn diagrams), tables instead of long lists, plain "moving objects" puzzles, fractions instead of
probability, and no median, range or rotational symmetry. Safe to run more than once.
