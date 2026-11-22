# Mind the Gap 11+

Maths practice for the Essex (CSSE) 11+ exam, for Year 5 children and their parents.
Not connected with or endorsed by CSSE.

## Folders
- `site/` – the live website (a single `index.html`). Netlify publishes this folder.
- `source/` – what `index.html` is built from: the app template, the question bank (`questions.json`),
  the Initial assessment (`starter-data.json`), and the scripts that write and check questions.

## Updating
1. Change files in `source/` (or ask Claude to).
2. Rebuild `site/index.html` from `source/` with `build.py`.
3. Commit and push. Netlify republishes in about a minute; each branch or pull request gets its own preview link.

Progress is kept on each device for now (browser storage). Parent accounts, payments (Stripe) and free-access codes come next.
