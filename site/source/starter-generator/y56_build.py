import random, sys, os, copy, re
sys.path.insert(0, '/home/claude/work')
from common import *
from y56a import *; from y56b import *; from y56c import *; from y56d import *
from docbuild import *

def trim(q, keep):
    q = copy.deepcopy(q); q['parts'] = [q['parts'][i] for i in keep if i < len(q['parts'])]; return q

MID = [t_count, t_digits, t_cost]; LATE = [t_relations, t_puzzle, t_ages]
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
def make_y56(i, used=None):
    used = used if used is not None else set()
    S = lambda k, t=0: random.Random(1000 * (i + 1) + k + 7919 * t)
    tg = lambda n: f'y56_p{i+1:02d}_q{n}'
    v = i  # variant driver
    mid = MID[i % 3]; late = LATE[(i + i // 3) % 3]
    slots = [
        (t_arith, v, None), (t_fractions, v, None), (t_powers, v, None), (t_order, v, None), (t_units, v, None), (t_dec, v + 1, [0, 1]),
        (t_money, v, None), (t_ratio, v, None), (mid, v // 3 + i % 2, None), (t_seq, v, None), (t_machine, v, None), (t_angles, v, [0, 2]),
        (t_coords, v, None), (t_round, v, None), (t_charts, v, None), (t_time, v, [0, 1, 2]) , (t_mean, v, None), (t_asn, v, None), (t_rect, v, None), (late, v // 3 + i % 2, None)]
    qs = []
    for n, (f, vv, keep) in enumerate(slots, 1):
        q = uniq(lambda t: f(S(n, t), vv, tg(n)), used, n)
        if f is t_time and vv % 3 != 0: keep = None
        if f is t_count and q['parts'] and len(q['parts']) == 4: keep = [0, 1, 2]
        if keep: q = trim(q, keep)
        qs.append(q)
    return qs
if __name__ == '__main__':
    u_ = set()
    for i in range(10):
        qs = make_y56(i, u_); print(i + 1, len(qs), sum(len(q['parts']) for q in qs), [f.__name__ for f in (MID[i % 3], LATE[(i + i // 3) % 3])])
