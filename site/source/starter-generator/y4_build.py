import random, sys, re
sys.path.insert(0, '/home/claude/work')
from y4c import *
from docbuild import *
CORE = [y_arith, y_tables, y_missing, y_pv, y_round, y_negroman, y_fractions, y_decimals, y_money, y_units, y_time, y_perim, y_seq, y_chart]
STRETCH = [y_asn, y_bounds, y_share, y_ages, y_count, y_machine, y_digits]
def _sigs(q):
    out = [p['text'] for p in q['parts'] if re.search(r'\d{2}', p['text'])] + [l for l in q['intro'] if re.search(r'\d{2}', l)]
    return out or [' '.join(p['text'] for p in q['parts'])]
def uniq(gen, used, slot, tries=120):
    best = None
    for t in range(tries):
        q = gen(t); sg = [(slot, x) for x in _sigs(q)]
        if not any(x in used for x in sg):
            used.update(sg); return q
        if best is None: best = q
    used.update(sg); return q
def make_y4(i, used=None):
    used = used if used is not None else set()
    S = lambda k, t=0: random.Random(5000 * (i + 1) + k + 7919 * t)
    qs = []
    for n, f in enumerate(CORE, 1): qs.append(uniq(lambda t: f(S(n, t), i, f'y4_p{i+1:02d}_q{n}'), used, n))
    start = (i * 2) % 7
    idx = sorted({(start + k) % 7 for k in range(4)}) if False else sorted([(start + k * 2) % 7 for k in range(4)])
    for k, j in enumerate(idx): qs.append(uniq(lambda t: STRETCH[j](S(100 + k, t), i // 2 + k, f'y4_p{i+1:02d}_s{k}'), used, 100 + j))
    return qs, [STRETCH[j].__name__ for j in idx]
if __name__ == '__main__':
    u_ = set()
    for i in range(10):
        qs, st = make_y4(i, u_); print(i + 1, len(qs), sum(len(q['parts']) for q in qs), st)
