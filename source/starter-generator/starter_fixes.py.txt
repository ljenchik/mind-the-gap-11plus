"""Hand fixes for the Starter exam papers, applied after build_starter.py.
Run:  python3 starter_fixes.py   (rewrites starter-data.json in place; safe to run more than once)
1. 'value of the digit' and 'Write N in Roman numerals' and 'Write N in words' -> tap one of four answers
2. fractions written as a/b (shown stacked in the app) instead of unicode fraction characters
3. sequences put on their own line
4. no near-identical question in sitting A and B of the same set (Jess's outfits)
5. a labelled rectangle picture for the perimeter questions
"""
import json, re, random, base64

UNI = {'½': '1/2', '⅓': '1/3', '⅔': '2/3', '¼': '1/4', '¾': '3/4', '⅕': '1/5', '⅖': '2/5', '⅗': '3/5', '⅘': '4/5',
       '⅙': '1/6', '⅚': '5/6', '⅛': '1/8', '⅜': '3/8', '⅝': '5/8', '⅞': '7/8', '⅐': '1/7', '⅑': '1/9', '⅒': '1/10'}
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789'); SUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')

def plain_fractions(s):
    if not isinstance(s, str): return s
    s = re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹]+)⁄([₀₁₂₃₄₅₆₇₈₉]+)', lambda m: m.group(1).translate(SUP) + '/' + m.group(2).translate(SUB), s)
    for k, v in UNI.items(): s = s.replace(k, v)
    return s

def fix_mixed(s, before):
    # '2⅔' (digit followed directly by a unicode fraction) must become '2 2/3', not '22/3'
    if not isinstance(s, str): return s
    for k, v in UNI.items(): s = re.sub(r'(\d)' + k, r'\1 ' + v, s)
    s = re.sub(r'(\d)([⁰¹²³⁴⁵⁶⁷⁸⁹]+⁄)', r'\1 \2', s)
    s = re.sub(r'\s*⁄\s*', '/', s)
    return plain_fractions(s)

def roman(n):
    out = ''
    for v, r in [(100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]:
        while n >= v: out += r; n -= v
    return out

ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'zero ten twenty thirty forty fifty sixty seventy eighty ninety'.split()
def words(n):
    def u100(n): return ONES[n] if n < 20 else TENS[n // 10] + ('-' + ONES[n % 10] if n % 10 else '')
    def u1000(n):
        h, r = divmod(n, 100)
        return (ONES[h] + ' hundred' + (' and ' + u100(r) if r else '')) if h else u100(r)
    th, r = divmod(n, 1000)
    if not th: return u1000(r)
    if not r: return u1000(th) + ' thousand'
    return u1000(th) + ' thousand' + (', ' if r >= 100 else ' and ') + u1000(r)

def opts(right, wrong, seed):
    o = [right] + [w for w in dict.fromkeys(wrong) if w != right][:3]
    random.Random(seed).shuffle(o); return o

def rect_svg(L, W, lab_l, lab_w):
    w = 240; h = max(70, min(170, round(240 * W / L)))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 {h + 70}" width="340" height="{h + 70}" font-family="Arial,sans-serif" font-size="17">'
           f'<rect x="40" y="20" width="{w}" height="{h}" fill="#eaf4fb" stroke="#1d3a4a" stroke-width="2.5"/>'
           f'<text x="{40 + w / 2}" y="{h + 48}" text-anchor="middle" fill="#1d3a4a" font-weight="700">{lab_l}</text>'
           f'<text x="{40 + w + 14}" y="{20 + h / 2 + 6}" fill="#1d3a4a" font-weight="700">{lab_w}</text>'
           f'<text x="{40 + w / 2}" y="14" text-anchor="middle" fill="#6b7c85" font-size="13">not drawn to scale</text></svg>')
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()

def main(path='starter-data.json'):
    S = json.load(open(path))
    for p in S['papers']:
        for q in p['qs']:
            q['intro'] = [fix_mixed(l, None) for l in q['intro']]
            if q.get('table'): q['table'] = [[fix_mixed(c, None) for c in r] for r in q['table']]
            for i, x in enumerate(q['parts']):
                x['t'] = fix_mixed(x['t'], None); x['a'] = fix_mixed(x['a'], None)
                if x['s'].get('k') == 'ch': x['s']['o'] = [fix_mixed(o, None) for o in x['s']['o']]; x['s']['v'] = fix_mixed(x['s']['v'], None)
                seed = q['id'] + str(i)
                m = re.match(r'What is the value of the digit (\d) in the number (\d+)\?', x['t'])
                if m and x['s'].get('k') == 'n':
                    d = m.group(1); v = x['s']['v']
                    x['s'] = {'k': 'ch', 'v': v, 'o': opts(v, [d, d + '0', d + '00', d + '000'], seed)}
                    x['t'] = x['t'].replace('?', '? Choose one.')
                m = re.match(r'Write (\d+) in Roman numerals\.', x['t'])
                if m:
                    n = int(m.group(1)); r = roman(n)
                    x['s'] = {'k': 'ch', 'v': r, 'o': opts(r, [roman(n - 10), roman(n + 1), roman(n - 1), roman(n + 10)], seed)}
                    x['t'] = f'Which of these is {n} in Roman numerals?'
                m = re.match(r'Write (\d+) in words\.', x['t'])
                if m:
                    n = int(m.group(1)); s = str(n)
                    alt = [int(s[0] + s[2] + s[1] + s[3]) if len(s) == 4 else n + 10, n * 10 + 0 if n < 1000 else int(s[:2] + '0' + s[2:]), n + 36 if n % 100 < 50 else n - 36]
                    alt = [a for a in alt if a != n]
                    w = words(n); x['s'] = {'k': 'ch', 'v': w, 'o': opts(w, [words(a) for a in alt], seed)}; x['a'] = w
                    x['t'] = f'Which of these is {n} written in words?'
                if q['sk'] == 'seq':
                    t = x['t']
                    m = re.match(r'(.*?):\s+((?:-?\d+|___)(?:,\s*(?:-?\d+|___))+)\.\s*(.+)$', t)
                    if m: t = f"{m.group(1)}. {m.group(3).rstrip('.')}:\n{m.group(2)}"
                    t = re.sub(r':\s{2,}', ':\n', t)
                    x['t'] = t
            if q['sk'] == 'perim':
                m = re.search(r'A rectangle is (\d+) cm long and (\d+) cm wide', ' '.join(q['intro']))
                if m: L, W = int(m.group(1)), int(m.group(2)); q['fig'] = rect_svg(L, W, f'{L} cm', f'{W} cm')
                else:
                    m = re.search(r'perimeter of (\d+) cm\. Its length is (\d+) cm', q['parts'][0]['t'])
                    if m:
                        P_, L = int(m.group(1)), int(m.group(2)); q['fig'] = rect_svg(L, P_ / 2 - L, f'{L} cm', '? cm')
    # 4. sitting B of set 1 (Year 4) had Jess's outfits again with tops and skirts swapped
    for p in S['papers']:
        if p['id'] != 'y4-F1-B': continue
        for q in p['qs']:
            if q['intro'] and q['intro'][0].startswith('Jess has'):
                q['intro'] = ['A café sells 3 kinds of sandwich, 4 kinds of drink and 2 kinds of cake.']
                q['parts'] = [
                    {'t': 'How many different meals of one sandwich and one drink can you choose?', 'a': '12', 's': {'k': 'n', 'v': '12'}},
                    {'t': 'How many different meals of one sandwich, one drink and one cake can you choose?', 'a': '24', 's': {'k': 'n', 'v': '24'}},
                    {'t': 'The café adds one more kind of drink. How many different meals of one sandwich, one drink and one cake are there now?', 'a': '30', 's': {'k': 'n', 'v': '30'}}]
    json.dump(S, open(path, 'w'), ensure_ascii=False)

if __name__ == '__main__':
    main()
