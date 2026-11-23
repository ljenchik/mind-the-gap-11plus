import sys, re, json, base64, io, random
sys.path.insert(0, '/home/claude/work')
from fractions import Fraction as F
from y56_build import *            # makers, MID, LATE, trim, _sigs, uniq
import y4_build
from y4c import *
from PIL import Image

def sig_all(q): return ' | '.join(q['intro']) + ' || ' + ' | '.join(p['text'] + '=' + str(p['ans']) for p in q['parts'])
def uq(gen, used, tries=200):
    for t in range(tries):
        q = gen(t)
        if sig_all(q) not in used:
            used.add(sig_all(q)); return q
    raise RuntimeError('could not make a distinct question')
# ---------- generation (own seed range, so Starter papers are never the printed practice papers) ----------
SK56 = [('arith', 'Written arithmetic', 'Add and subtract'), ('frac', 'Fractions', 'Fractions'), ('pow', 'Powers', 'Number'), ('order', 'Ordering numbers', 'Number'),
        ('units', 'Units and measures', 'Money & Time'), ('dec', 'Decimals', 'Decimals'), ('money', 'Money and percentages', 'Money & Time'), ('ratio', 'Ratio and sharing', 'Multiply and divide'),
        ('puz1', 'Number puzzles', 'Number'), ('seq', 'Sequences and formulas', 'Number'), ('mach', 'Formula machines', 'Number'), ('ang', 'Angles', 'Number'),
        ('coord', 'Coordinates and shapes', 'Number'), ('round', 'Rounding and limits', 'Number'), ('chart', 'Charts and graphs', 'Number'), ('time', 'Time and timetables', 'Money & Time'),
        ('mean', 'Averages', 'Multiply and divide'), ('asn', 'Always, sometimes, never', 'Number'), ('rect', 'Rectangles', 'Multiply and divide'), ('puz2', 'Logic puzzles', 'Number')]
SK4 = [('arith', 'Written arithmetic', 'Add and subtract'), ('tables', 'Times tables and division', 'Multiply and divide'), ('missing', 'Missing numbers', 'Add and subtract'),
       ('pv', 'Place value', 'Number'), ('round', 'Rounding', 'Number'), ('negroman', 'Negative numbers and Roman numerals', 'Number'), ('frac', 'Fractions', 'Fractions'),
       ('dec', 'Decimals', 'Decimals'), ('money', 'Money', 'Money & Time'), ('units', 'Units and measures', 'Money & Time'), ('time', 'Time', 'Money & Time'),
       ('perim', 'Perimeter and area', 'Multiply and divide'), ('seq', 'Sequences', 'Number'), ('chart', 'Charts', 'Number'), ('chal', 'Challenge puzzles', 'Number')]

def form56(v, sb, used):
    S = lambda k, t=0: random.Random(1000 * (sb + 1) + k + 7919 * t)
    tg = lambda n: f'st56_{sb}_q{n}'
    mid = MID[v % 3]; late = LATE[(v + v // 3) % 3]
    slots = [(t_arith, v, None), (t_fractions, v, None), (t_powers, v, None), (t_order, v, None), (t_units, v, None), (t_dec, v + 1, [0, 1]),
             (t_money, v, None), (t_ratio, v, None), (mid, v // 3 + v % 2, None), (t_seq, v, None), (t_machine, v, None), (t_angles, v, [0, 2]),
             (t_coords, v, None), (t_round, v, None), (t_charts, v, None), (t_time, v, [0, 1, 2]), (t_mean, v, None), (t_asn, v, None), (t_rect, v, None), (late, v // 3 + v % 2, None)]
    qs = []
    for n, (f, vv, keep) in enumerate(slots, 1):
        q = uq(lambda t: f(S(n, t), vv, tg(n)), used)
        if f is t_time and vv % 3 != 0: keep = None
        if f is t_count and q['parts'] and len(q['parts']) == 4: keep = [0, 1, 2]
        if keep: q = trim(q, keep)
        qs.append((SK56[n - 1][0], q))
    return qs

def form4(v, sb, used):
    S = lambda k, t=0: random.Random(5000 * (sb + 1) + k + 7919 * t)
    CORE = y4_build.CORE; STRETCH = y4_build.STRETCH
    qs = []
    for n, f in enumerate(CORE, 1):
        q = uq(lambda t: f(S(n, t), v, f'st4_{sb}_q{n}'), used); qs.append((SK4[n - 1][0], q))
    start = (v * 2) % 7; idx = sorted([(start + k * 2) % 7 for k in range(4)])
    for k, j in enumerate(idx):
        q = uq(lambda t: STRETCH[j](S(100 + k, t), v // 2 + k, f'st4_{sb}_s{k}'), used); qs.append(('chal', q))
    return qs

# ---------- answer specs ----------
VUL = {'½': (1, 2), '⅓': (1, 3), '⅔': (2, 3), '¼': (1, 4), '¾': (3, 4), '⅕': (1, 5), '⅖': (2, 5), '⅗': (3, 5), '⅘': (4, 5), '⅙': (1, 6), '⅚': (5, 6), '⅛': (1, 8), '⅜': (3, 8), '⅝': (5, 8), '⅞': (7, 8)}
SUPS = '⁰¹²³⁴⁵⁶⁷⁸⁹'; SUBS = '₀₁₂₃₄₅₆₇₈₉'
def unfrac(s):
    """unicode fraction string -> Fraction, or None"""
    s = s.strip().replace('−', '-'); neg = s.startswith('-'); s = s.lstrip('-')
    m = re.fullmatch(r'(\d+)?\s*([' + ''.join(VUL) + '])', s)
    if m: w = int(m.group(1) or 0); n, d = VUL[m.group(2)]; r = F(w) + F(n, d); return -r if neg else r
    m = re.fullmatch(r'(\d+)?\s*([' + SUPS + r']+)⁄([' + SUBS + r']+)', s)
    if m:
        w = int(m.group(1) or 0); n = int(''.join(str(SUPS.index(c)) for c in m.group(2))); d = int(''.join(str(SUBS.index(c)) for c in m.group(3)))
        r = F(w) + F(n, d); return -r if neg else r
    return None
def fs(x): x = F(x); return f'{x.numerator}/{x.denominator}' if x.denominator != 1 else str(x.numerator)
def dnorm(x):
    """numeric string -> canonical plain string (no trailing zeros)"""
    x = F(x); s = f'{float(x):.10f}'.rstrip('0').rstrip('.') if x.denominator != 1 else str(x.numerator)
    return s
def mm(a): return a.replace('−', '-')
ALWAYS = ['Always true', 'Sometimes true', 'Never true']
DAYS = {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}
UNITS = r'(?:°C|°F|°|%| cm²| cm| mm| km| m| kg| g| ml| years| degrees| goals| points)?'

def conv_part(text, ans, q):
    """returns dict(t, s, a, [labels], [ph], [pre], [suf]) ; raises if unknown"""
    ans = str(ans).strip(); intro = ' '.join(q['intro'])
    text = re.sub(r'^Calculate  ', 'Calculate ', text)
    text = re.sub(r'^(\d+) raised to the power □ ÷ (\d+) = (\d+)$', r'(\1 raised to the power □) ÷ \2 = \3', text)
    text = re.sub(r'(?<=[.?:])\s{3,}', '\n', text)
    P = dict(t=text, a=ans)
    def done(s, **kw): P['s'] = s; P.update(kw); return P
    # --- special, multi-box and open parts
    if 'Fill in the boxes to show one way' in text:
        a, T = map(int, re.search(r'(\d+) × \(□□ \+ □\) = (\d+)', text).groups())
        return done(dict(k='dig', a=a, T=T), ph='the three digits, e.g. 3 1 7')
    if (m := re.fullmatch(r'b = (-?\d+); c − b = (-?\d+)', ans)):
        return done(dict(k='multi', parts=[dict(k='n', v=m.group(1)), dict(k='n', v=m.group(2))]), labels=['b =', 'c − b ='])
    if (m := re.match(r'(\d+) goals and (\d+) penalties', ans)):
        a, b = map(int, re.search(r'scores (\d+) points and a penalty scores (\d+) points', intro).groups()); N = int(re.search(r'A score of (\d+)', text).group(1))
        excl = [[N // a, 0], [0, N // b]]; alts = [tuple(map(int, x)) for x in re.findall(r'(\d+) goals and (\d+) penalties', ans)]
        assert alts and all(a * g + b * p == N for g, p in alts), (text, ans)
        return done(dict(k='lin', a=a, b=b, N=N, excl=excl), labels=['goals', 'penalties'], a=' or '.join(f'{g} goals and {p} penalties' for g, p in alts))
    if (m := re.fullmatch(r'(\S+) is bigger; difference (\d+)', ans)):
        o = re.search(r'bigger, (\S+) or (\S+)\?', text).groups()
        return done(dict(k='multi', parts=[dict(k='ch', v=m.group(1), o=list(o)), dict(k='n', v=m.group(2))]), labels=['Which is bigger?', 'Difference'])
    if (m := re.match(r'(False|True)\b', ans)) and 'true or false' in text:
        dd = int(re.search(r'(\d+) apart', text).group(1))
        pr = [[2, dd + 2]] if m.group(1) == 'False' else []
        if m.group(1) == 'False': assert all(isprime(x) for x in pr[0]), ans
        T = text.replace('Is this true or false?', 'Is this true or false? If it is false, give two prime numbers that show it.')
        P['t'] = T
        return done(dict(k='multi', parts=[dict(k='ch', v=m.group(1), o=['True', 'False']), dict(k='pairs', v=pr, optional=(m.group(1) == 'True'))]), labels=['True or false?', 'Two prime numbers (if false)'])
    if (m := re.fullmatch(r'(\w+), by (\d+) degrees', ans)):
        towns = re.search(r'in (\w+) and [−-]\d+°C in (\w+)\.', text).groups()
        return done(dict(k='multi', parts=[dict(k='ch', v=m.group(1), o=list(towns)), dict(k='n', v=m.group(2))]), labels=['Colder town', 'Degrees colder'])
    if (m := re.fullmatch(r'The pack of (\d+) \((\d+)p each, compared with (\d+)p each\)', ans)):
        n1, c1, n2, c2 = re.search(r'A pack of (\d+) stickers costs £([\d.]+)\. A pack of (\d+) stickers costs £([\d.]+)', text).groups()
        n1, n2 = int(n1), int(n2); p1 = F(c1) * 100 / n1; p2 = F(c2) * 100 / n2; assert p1.denominator == 1 and p2.denominator == 1
        win = int(m.group(1)); o = [f'Pack of {n1}', f'Pack of {n2}']
        return done(dict(k='multi', parts=[dict(k='ch', v=f'Pack of {win}', o=o), dict(k='n', v=str(int(p1)), alt=[dnorm(p1 / 100)]), dict(k='n', v=str(int(p2)), alt=[dnorm(p2 / 100)])]),
                    labels=['Cheaper pack', f'Pence for one sticker in the pack of {n1}', f'Pence for one sticker in the pack of {n2}'])
    if re.fullmatch(r'(Always|Sometimes|Never) true', ans): return done(dict(k='ch', v=ans, o=ALWAYS))
    if ans in ('Yes', 'No'): return done(dict(k='ch', v=ans, o=['Yes', 'No']))
    if (m := re.search(r'Give your answer as (.+) or (.+)\.$', text)) and not re.search(r'[a-z]\)', ans):
        o = [m.group(1), m.group(2)]; assert ans in o, (text, ans); return done(dict(k='ch', v=ans, o=o))
    if re.fullmatch(r'\d+ and \d+( or \d+ and \d+)*', ans) and 'missing numbers' not in text:
        pairs = [list(map(str, x)) for x in re.findall(r'(\d+) and (\d+)', ans)]
        return done(dict(k='pairs', v=pairs), ph='two numbers, e.g. 5 and 29')
    if 'missing numbers' in text and (m := re.fullmatch(r'(-?\d+) and (-?\d+)', ans)):
        return done(dict(k='list', v=[m.group(1), m.group(2)]), ph='two numbers, with a comma between')
    if (m := re.fullmatch(r'(\w+) and (\w+)', ans)) and m.group(1) in DAYS:
        return done(dict(k='set', v=[x.lower() for x in m.groups()]), ph='e.g. Mon and Tue')
    if (m := re.fullmatch(r'(\d\d:\d\d) and (\d\d:\d\d)', ans)): return done(dict(k='set', v=list(m.groups())), ph='e.g. 09:00 and 11:00')
    if (m := re.fullmatch(r'term (\d+)', ans)): return done(dict(k='n', v=m.group(1)), pre='term')
    # --- times and durations
    if (m := re.fullmatch(r'(\d\d):(\d\d)( the next day| two days later)?', ans)): return done(dict(k='t', v=int(m.group(1)) * 60 + int(m.group(2))), ph='e.g. 14:35')
    if (m := re.fullmatch(r'(\d{1,2}):(\d\d)(am|pm)', ans)):
        h = int(m.group(1)) % 12 + (12 if m.group(3) == 'pm' else 0); return done(dict(k='t', v=h * 60 + int(m.group(2)), h12=True), ph='e.g. 3:30pm')
    if (m := re.fullmatch(r'(\d+) hours?(?: (\d+) minutes)?', ans)):
        v = int(m.group(1)) * 60 + int(m.group(2) or 0); return done(dict(k='d', v=v, **({'u': 'h'} if m.group(2) is None else {})), ph='e.g. 2 hours 5 minutes')
    if (m := re.fullmatch(r'\((-?\d+), (-?\d+)\)', mm(ans))): return done(dict(k='c', v=[int(m.group(1)), int(m.group(2))]), ph='(x, y)')
    # --- lists of numbers
    a2 = mm(ans)
    if re.fullmatch(r'-?\d+(\.\d+)?(,\s+-?\d+(\.\d+)?)+', a2):
        return done(dict(k='list', v=[x.strip() for x in a2.split(',')]), ph='numbers with commas between')
    # --- fractions
    fr = unfrac(ans)
    if fr is not None:
        strict = 'simplest form' in text; dm = re.search(r'denominator (\d+)', text)
        sp = dict(k='f', v=fs(fr)); 
        if strict: sp['strict'] = True
        if dm: sp['den'] = int(dm.group(1))
        return done(sp, ph=('e.g. 65/100' if dm else 'e.g. 3/4 or 1 1/2'))
    # --- numbers with money / units
    if (m := re.fullmatch(r'£(\d+(?:\.\d+)?)', ans)): return done(dict(k='n', v=m.group(1)), pre='£')
    if (m := re.fullmatch(r'\$(\d+(?:\.\d+)?)', ans)): return done(dict(k='n', v=m.group(1)), pre='$')
    if (m := re.fullmatch(r'(-?\d+(?:\.\d+)?)\s*(' + UNITS[3:-2].lstrip('?:') + r')?', a2)) or (m := re.fullmatch(r'(-?\d+(?:\.\d+)?)\s*(°C|°F|°|%|cm²|cm|km|g|years|degrees)?', a2)):
        u = (m.group(2) or '').strip(); sp = dict(k='n', v=m.group(1))
        if 'as a decimal' in text: sp['dec'] = True
        if u == 'g' and F(m.group(1)) % 100 == 0: sp['au'] = [[dnorm(F(m.group(1)) / 1000), 'kg']]
        return done(sp, **({'suf': u} if u else {}))
    # --- words, Roman numerals, formulas
    if re.fullmatch(r'[A-Za-z ,\-]+', ans): return done(dict(k='x', v=[ans]))
    if re.fullmatch(r'\d*n [+−-] \d+', ans): return done(dict(k='x', v=[ans], nospace=True), ph='e.g. 5n + 3')
    raise ValueError(f'no spec for: {text!r} -> {ans!r}')

PNGS = {}
def fig_uri(path):
    im = Image.open(path).convert('L'); w, h = im.size
    if w > 760: im = im.resize((760, int(h * 760 / w)), Image.LANCZOS)
    im = im.quantize(16, method=Image.MEDIANCUT) if False else im.convert('P', palette=Image.ADAPTIVE, colors=24)
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def conv_q(skill, q, n, qid):
    out = dict(id=qid, n=n, sk=skill, intro=[re.sub(r'(?<=[.?:])\s{3,}', '\n', l) for l in q['intro']], parts=[], fig=None, table=None)
    if q.get('fig'): out['fig'] = fig_uri(q['fig'][0])
    if q.get('table'): out['table'] = q['table']['rows']
    for p in q['parts']: out['parts'].append(conv_part(p['text'], p['ans'], q))
    return out

def paper(level, form, sit, qs):
    qq = [conv_q(sk, q, i + 1, f'{level}{form}{sit}-{i+1:02d}') for i, (sk, q) in enumerate(qs)]
    return dict(id=f'{level}-F{form}-{sit}', level=level, form=form, sit=sit, qs=qq, marks=sum(len(q['parts']) for q in qq))

if __name__ == '__main__':
    out = dict(sk56=[dict(id=a, name=b, topic=c) for a, b, c in SK56], sk4=[dict(id=a, name=b, topic=c) for a, b, c in SK4], papers=[])
    u56, u4 = set(), set()
    for form, (vA, vB) in enumerate([(0, 1), (2, 3)], 1):
        for sit, v in (('A', vA), ('B', vB)):
            out['papers'].append(paper('y56', form, sit, form56(v, 100 + 2 * (form - 1) + (sit == 'B'), u56)))
    for form, (vA, vB) in enumerate([(0, 1), (2, 3)], 1):
        for sit, v in (('A', vA), ('B', vB)):
            out['papers'].append(paper('y4', form, sit, form4(v, 200 + 2 * (form - 1) + (sit == 'B'), u4)))
    json.dump(out, open('starter-data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    for p in out['papers']: print(p['id'], len(p['qs']), p['marks'])
    import os; print(os.path.getsize('starter-data.json'))
