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

## Topic bank and Set B papers (added 23 Nov 2026)
`topic-bank/` holds the question makers for 30 topics (about 215 question types) and for the Set B papers (Practice tests 31–50).
- `topics1.py`, `topics2.py`, `topics3.py` – the topic question makers; `papers.py` – the 20-question paper makers; `common.py` – helpers and diagrams.
- `ondemand.py` – fresh questions for one topic: `python3 ondemand.py RAT 20 7` (topic code, how many, seed). Run it with no arguments to list the codes and question types.
- `build.py` – builds the printable Word files; `verify.py` – re-does the sums in every worked solution.
- `integrate.py` – converts the bank into `questions.json` records (ids `SK-<skill>-B001a…`, papers `PT31`–`PT50`). Safe to re-run.


## 10-topic main page (23 Nov)
The Year 5 page has 10 main topics with 34 parts (see `MAIN` in `app-template.html.txt` and `sk56` in `starter-data.json`).
After any script that writes questions, run in this order:
1. `new-parts.py.txt questions.json` – tops up the newer parts to at least 30 sets each.
2. `retopic.py.txt questions.json starter-data.json` – sorts every Year 5 question into its part
   (topic-bank questions by the topic and type in their source note, the others by their wording) and renames the parts.
3. `pct-update.py.txt questions.json starter-data.json` – the part "Percentages and word problems": adds 150 sets of percentage
   word problems (increase, decrease, reverse, percentage change, offers) and gives every paper (Papers 1–50) its percentage question
   from `pct-families.py.txt`. Topic labels such as "Decimals and order of operations." are never shown in questions.
4. `bond-topup.py.txt questions.json starter-data.json` – tops up Roman numerals, formula machines, sequences, add and subtract,
   number puzzles, logic puzzles and always/sometimes/never with Bond-style question types (`bond-families.py.txt`, ids SK-<part>-Ynn).
Magic squares are drawn with the picture `magic a,b,c;d,e,f;g,h,i` (`_` for an empty box).
