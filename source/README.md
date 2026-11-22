# 11+ Maths Practice – source code

| File | What it is |
|---|---|
| `app-template.html.txt` (rename to .html) | The whole app: page layout, styles and JavaScript. The question bank goes where it says `__DATA__`. |
| `questions.json` | The built-in question bank (id, question, answer, worked solution, level, marks, type, topic tab, picture). |
| `build.py.txt` (rename to .py) | Puts `questions.json` into the template and writes `index.html` (the published app). |
| `starter-data.json` | The Starter exam: 8 fixed papers (Year 4 and Year 5–6, set 1 and 2, sittings A and B) with answers and marking rules. Built by `starter-generator/`. |
| `marker.js.txt` (rename to .js) | Auto-marking of typed answers (numbers, fractions, money, times, durations, coordinates, lists, choices). Put into the app at `/*__MARKER__*/`. `node test-marker.js.txt` style checks are in `starter-generator/test_marker.js.txt`. |
| `starter-generator/starter_fixes.py.txt` | Hand fixes applied after `build_starter.py` (tap-to-answer for place value, Roman numerals and numbers in words; plain a/b fractions shown stacked; sequences on their own line; rectangle pictures; no repeated question across sittings). Run it after every rebuild of `starter-data.json`. |
| `starter-generator/` | Python that makes and checks the Starter papers: `build_starter.py` (run it in a folder with the `y*.py` and `common.py` files), `test_marker.js`. |
| `print-tasks.js.txt` (rename to .js) | Makes the printable PDF of the Number questions (needs Node and Chrome). |

Build: `python3 build.py` (needs `app-template.html`, `questions.json`, `help.json`, `starter-data.json`, `marker.js` in one folder).

Inside the app's JavaScript:
- `STARTER` – the Starter exam papers. `ST*` / `st*` functions – exam screens, saving, marking, skill map (section "starter exam"). Progress is saved on the device (`starter:*` keys) and in the progress document when signed in.
- `TREE` – topics and subtopics, and which question types belong to each.
- `GEN` – generators that make new questions without AI (times tables, clocks, comparing calculations, number lines…).
- `buildQuestion` / `wrongAnswersFor` – choose typed answer or multiple choice and make the wrong options.
- `drawPic` – clocks, number lines, bar charts, times tables and other pictures (SVG).
- Parent area – PIN, progress, question editor (edits saved to the Claude account `edits` collection, or on the device), set test.

Edits parents make in the app are stored separately from `questions.json` and laid over it when the app loads.


## Credits
Some word problems (IDs WP-Y4-001 to WP-Y4-019) are adapted from Oak National Academy resources, © Oak National Academy Limited, licensed under the Open Government Licence v3.0: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
Questions with IDs Y4S-, Y5- and Y6- are reworded from the DfE "Mathematics guidance: key stages 1 and 2" (reference DfE-00100-2020) and the Standards and Testing Agency 2024 key stage 2 mathematics tests, both licensed under the Open Government Licence v3.0. The source of each is in the question's "src" field.
