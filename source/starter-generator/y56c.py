from common import *
from y56a import isprime, rnd10
from y56b import NAMES

# ---------- charts ----------
def t_charts(r, v, tag):
    path = make_fig_path(tag); m = v % 4
    if m == 0:
        while True:
            fr = [r.randint(1, 9) for _ in range(6)]
            games = sum(fr); goals = sum(i * f for i, f in enumerate(fr)); mean = F(goals, games)
            x = mean * 10 
            if abs((x - math.floor(x)) - F(1, 2)) > F(1, 10) and 30 <= games <= 40: break
        bar_chart(path, [str(i) for i in range(6)], fr, 'Goals scored in a game', 'Number of games', ymax=max(fr) + 1)
        return Q('Stefan recorded the number of goals scored in each game of a football league over four weekends. The bar chart shows his results. For example, the first bar shows that there were ' + f'{fr[0]} games in which no goals were scored.',
                 [('What was the total number of games over the four weekends?', games), ('What was the total number of goals scored over the four weekends?', goals),
                  ('What was the average (mean) number of goals scored per game? Give your answer to one decimal place.', f'{float(mean):.1f}')], fig=(path, 4.8))
    if m == 1:
        while True:
            t = [r.randint(-2, 6)]
            for e in [r.randint(1, 6) for _ in range(5)] + [r.randint(-3, 1)]: t.append(t[-1] + e)
            inc = [t[i + 1] - t[i] for i in range(6)]
            if max(inc) == sorted(inc)[-1] and inc.count(max(inc)) == 1 and max(t) <= 28 and any(x % 5 == 0 and x not in (0,) for x in t[1:]): break
        times = [5, 7, 9, 11, 13, 15, 17]; lab = [f'{h:02d}:00' for h in times]
        line_chart(path, times, t, lab, 'Time of day', 'Temperature (°C)', min(0, min(t) - 1) // 2 * 2, max(t) + 2, 2)
        ti = r.choice([i for i in range(1, 7) if t[i] % 5 == 0 and t[i] > 0]); fi = int(t[ti] * F(9, 5) + 32)
        a = r.choice([1, 2, 3]); b = r.choice([4, 5, 6])
        fast = inc.index(max(inc))
        return Q('The chart shows the temperature in degrees Celsius at different times of one day in Birmingham.',
                 [(f'What is the temperature at {lab[a]}?', f'{t[a]}°C'), (f'By how much has the temperature risen between {lab[0]} and {lab[b]}?', f'{t[b]-t[0]}°C'),
                  ('Between which two of the times shown is the temperature rising fastest?', f'{lab[fast]} and {lab[fast+1]}'),
                  (f'To change a temperature in °C to °F, multiply by 1.8 and then add 32. What is the temperature at {lab[ti]} in °F?', f'{fi}°F')], fig=(path, 5.0))
    if m == 2:
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        while True:
            rates = [F(r.choice([120, 125, 130, 135, 140, 150, 160]), 100) for _ in range(5)]
            inc = [rates[i + 1] - rates[i] for i in range(4)]
            if inc.count(max(inc)) == 1 and max(inc) > 0 and all((40 * x).denominator == 1 for x in rates) and 3 < len(set(rates)): break
        di = r.randrange(5); d2 = r.randrange(5)
        pounds = r.choice([50, 100, 200]); usd = rates[d2] * pounds
        assert usd.denominator == 1
        fig, ax = plt.subplots(figsize=(5.2, 3.0), dpi=160)
        ax.plot(range(5), [float(x) for x in rates], 'ko-', ms=4); ax.set_xticks(range(5)); ax.set_xticklabels(days)
        ax.set_ylim(1.1, 1.7); ax.set_yticks([1.1 + 0.1 * i for i in range(7)]); ax.set_yticklabels([f'{1.1+0.1*i:.2f}' for i in range(7)])
        ax.grid(True, color='#ccc', lw=.6); ax.set_ylabel('Dollars for £1'); ax.set_xlabel('Day of the week'); ax.spines[['top', 'right']].set_visible(False)
        fig.tight_layout(); fig.savefig(path); plt.close(fig)
        fi = inc.index(max(inc))
        return Q('The graph shows how many US dollars could be bought for £1 at a bank on each day of one week.',
                 [(f'On {days[di]}, how many dollars could be bought with £40?', f'${dec(rates[di]*40)}'),
                  (f'On {days[d2]}, how many pounds would be needed to buy ${int(usd)}?', f'£{pounds}'),
                  ('Between which two consecutive days was the greatest increase in the number of dollars that could be bought for £1?', f'{days[fi]} and {days[fi+1]}')], fig=(path, 4.6))
    while True:
        N = r.choice([60, 72, 80, 90, 120, 144]); k = [r.randint(2, 6) for _ in range(4)]
        tot = sum(k); cnt = [F(N * x, tot) for x in k]
        if all(c.denominator == 1 for c in cnt) and all((360 * c / N).denominator == 1 for c in cnt) and len(set(cnt)) == 4: break
    cnt = [int(c) for c in cnt]; ang = [int(360 * c / N) for c in cnt]
    labs = ['Cycling', 'Swimming', 'Tennis', 'Athletics']; r.shuffle(labs)
    pie_chart(path, [f'{l}\n({a}°)' if i == 0 else l for i, (l, a) in enumerate(zip(labs, ang))], cnt)
    j = 1; k2 = 2
    return Q(f'{N} people were asked to choose their favourite summer sport. The pie chart shows the results (not drawn accurately). The angle for {labs[0]} is {ang[0]}°.',
             [(f'How many people chose {labs[0]}?', cnt[0]), (f'{cnt[j]} people chose {labs[j]}. What fraction of the people chose {labs[j]}? Give your answer in its simplest form.', frac(F(cnt[j], N))),
              (f'{cnt[k2]} people chose {labs[k2]}. What angle is needed for {labs[k2]} on the pie chart?', f'{ang[k2]}°')], fig=(path, 3.0))

# ---------- always / sometimes / never ----------
R = range(1, 61)
ODD = [x for x in range(1, 80) if x % 2]; EVEN = [x for x in range(2, 80, 2)]
PR = [p for p in range(2, 80) if isprime(p)]; SQ = [k * k for k in range(1, 12)]
M3 = [x for x in range(3, 100, 3)]; M6 = [x for x in range(6, 100, 6)]; M4 = [x for x in range(4, 100, 4)]
def pairs(d1, d2=None): return [(a, b) for a in d1 for b in (d2 or d1)]
STAT = [
    ('When you add two odd numbers, you get an even number.', pairs(ODD), lambda a, b: (a + b) % 2 == 0),
    ('When you multiply two odd numbers, you get an odd number.', pairs(ODD), lambda a, b: (a * b) % 2 == 1),
    ('The difference between two prime numbers is even.', pairs(PR), lambda a, b: (a - b) % 2 == 0),
    ('A multiple of 4 is also a multiple of 8.', [(x,) for x in M4], lambda a: a % 8 == 0),
    ('When you add a multiple of 6 to a multiple of 3, you get a multiple of 9.', pairs(M6, M3), lambda a, b: (a + b) % 9 == 0),
    ('When you multiply two different prime numbers together, the answer is divisible by 9.', [(a, b) for a in PR for b in PR if a != b], lambda a, b: (a * b) % 9 == 0),
    ('When you add two square numbers, you get a square number.', pairs(SQ), lambda a, b: round((a + b) ** .5) ** 2 == a + b),
    ('When you multiply two square numbers, you get a square number.', pairs(SQ), lambda a, b: round((a * b) ** .5) ** 2 == a * b),
    ('When you find the average of two prime numbers, you get a prime number.', [(a, b) for a in PR for b in PR if (a + b) % 2 == 0], lambda a, b: isprime((a + b) // 2)),
    ('A number that ends in 5 is divisible by 10.', [(x,) for x in range(5, 200, 10)], lambda a: a % 10 == 0),
    ('The sum of three consecutive whole numbers is a multiple of 3.', [(x,) for x in R], lambda a: (3 * a + 3) % 3 == 0),
    ('When you square a whole number, the answer is bigger than the number you started with.', [(x,) for x in R], lambda a: a * a > a),
    ('The sum of two prime numbers is even.', pairs(PR), lambda a, b: (a + b) % 2 == 0),
    ('A factor of 12 is also a factor of 24.', [(x,) for x in range(1, 13) if 12 % x == 0], lambda a: 24 % a == 0),
    ('The product of two even numbers is a multiple of 4.', pairs(EVEN), lambda a, b: (a * b) % 4 == 0),
    ('A number that is divisible by both 4 and 6 is divisible by 24.', [(x,) for x in range(12, 200, 12)], lambda a: a % 24 == 0),
    ('The square of an odd number is odd.', [(x,) for x in ODD], lambda a: (a * a) % 2 == 1),
    ('The difference between two square numbers is even.', pairs(SQ), lambda a, b: (a - b) % 2 == 0),
    ('A multiple of 5 ends in 5.', [(x,) for x in range(5, 200, 5)], lambda a: a % 10 == 5),
    ('A prime number is odd.', [(x,) for x in PR], lambda a: a % 2 == 1),
    ('A square number has an even number of factors.', [(x,) for x in SQ], lambda a: sum(1 for d in range(1, a + 1) if a % d == 0) % 2 == 0),
    ('The sum of two multiples of 3 is a multiple of 6.', pairs(M3), lambda a, b: (a + b) % 6 == 0),
    ('A number that is divisible by 9 is also divisible by 3.', [(x,) for x in range(9, 200, 9)], lambda a: a % 3 == 0),
    ('When you add 1 to a multiple of 6, you get a prime number.', [(x,) for x in M6], lambda a: isprime(a + 1)),
    ('When you add two consecutive whole numbers, the answer is odd.', [(x,) for x in R], lambda a: (2 * a + 1) % 2 == 1),
    ('A number with exactly two factors is odd.', [(x,) for x in PR], lambda a: a % 2 == 1),
    ('When you add two odd numbers, you get an odd number.', pairs(ODD), lambda a, b: (a + b) % 2 == 1),
    ('A prime number greater than 2 is even.', [(x,) for x in PR if x > 2], lambda a: a % 2 == 0),
    ('When you multiply two odd numbers, the answer is even.', pairs(ODD), lambda a, b: (a * b) % 2 == 0),
    ('A multiple of 4 is an odd number.', [(x,) for x in M4], lambda a: a % 2 == 1),
    ('The difference between two even numbers is odd.', [(a, b) for a in EVEN for b in EVEN], lambda a, b: (a - b) % 2 == 1),
    ('A square number ends in 7.', [(x,) for x in SQ + [k * k for k in range(12, 40)]], lambda a: a % 10 == 7),
    ('A number that is a multiple of 9 is a prime number.', [(x,) for x in range(9, 200, 9)], lambda a: isprime(a)),
    ('The sum of two multiples of 5 is a multiple of 10.', [(a, b) for a in range(5, 100, 5) for b in range(5, 100, 5)], lambda a, b: (a + b) % 10 == 0),
    ('When you multiply a number by 4, the answer is a multiple of 8.', [(x,) for x in R], lambda a: (4 * a) % 8 == 0),
    ('When you add three consecutive whole numbers, the answer is even.', [(x,) for x in R], lambda a: (3 * a + 3) % 2 == 0),
    ('When you divide an even number by 2, the answer is a whole number.', [(x,) for x in EVEN], lambda a: (a / 2) % 1 == 0),
    ('A number with 3 factors is a square number.', [(x,) for x in range(2, 400) if sum(1 for d in range(1, x + 1) if x % d == 0) == 3], lambda a: round(a ** .5) ** 2 == a),

]
def classify(i):
    t, dom, f = STAT[i]; res = [bool(f(*d)) for d in dom]
    return 'always' if all(res) else ('never' if not any(res) else 'sometimes')
CLS = [classify(i) for i in range(len(STAT))]
def t_asn(r, v, tag):
    byc = {c: [i for i in range(len(STAT)) if CLS[i] == c] for c in ('always', 'sometimes', 'never')}
    pat = [['always', 'sometimes', 'never', 'sometimes'], ['sometimes', 'always', 'sometimes', 'never'], ['never', 'sometimes', 'always', 'always'],
           ['sometimes', 'sometimes', 'always', 'never'], ['always', 'never', 'sometimes', 'sometimes']][v % 5]
    chosen = []
    for c in pat:
        opts = [i for i in byc[c] if i not in chosen]; chosen.append(r.choice(opts))
    return Q('For each of these statements, say whether it is always true, sometimes true or never true.',
             [(STAT[i][0], CLS[i].capitalize() + ' true' if CLS[i] != 'sometimes' else 'Sometimes true') for i in chosen])

# ---------- sequences ----------
def fmt_lin(a, b, var='n'):
    s = f'{a if a != 1 else ""}{var}'
    return s + (f' + {b}' if b > 0 else (f' − {-b}' if b < 0 else ''))
def t_seq(r, v, tag):
    m = v % 4
    if m == 0:
        b0 = r.randint(2, 9); g = r.randint(2, 4); e = r.randint(1, 2)
        t = [b0]
        for k in range(12): t.append(t[-1] + g + k * e)
        shown = ', '.join(map(str, t[:5]))
        # reducing gaps
        g2 = r.choice([2, 3]); s0 = r.randint(10, 20); gaps = [8 + 2 * g2 - 2 * g2 + 0, 0, 0]
        gp = [6 + 2 * g2 * 0 + g2 * 2, 6 + g2, 6]  # three reducing gaps
        gp = [6 + 2 * g2, 6 + g2, 6, 6 - g2]  # 4 gaps reducing by g2
        seq = [s0]
        for gg in gp: seq.append(seq[-1] + gg)
        c_e = r.choice([2, 3]); c_g = r.randint(4, 9); c_b = r.randint(2, 12)
        cs = [c_b]
        for k in range(4): cs.append(cs[-1] + c_g + k * c_e)
        return Q(None, [(f'The gaps in this sequence increase by {e} each time: {shown}, … What is the 8th number in the sequence?', t[7]),
                        (f'The gaps in this sequence reduce by {g2} each time: {seq[0]}, □, {seq[2]}, {seq[3]}, {seq[4]}. Fill in the missing number.', seq[1]),
                        (f'The gaps in this sequence increase by {c_e} each time: b, c, d, {cs[3]}, {cs[4]}. Find the value of b, and the value of c − b.', f'b = {cs[0]}; c − b = {c_g}')])
    if m == 1:
        a1 = r.randint(3, 9); da = r.randint(2, 6); db = r.randint(1, 4); n0 = r.randint(8, 24)
        b1 = a1 + (da + db) * (n0 - 1); k = r.randint(25, 45); target = a1 + da * (k - 1)
        tbl = [['', 'Rule', '1st term', '2nd term', '3rd term'], ['Sequence A', f'Add {da} each term', str(a1), str(a1 + da), str(a1 + 2 * da)], ['Sequence B', f'Subtract {db} each term', str(b1), str(b1 - db), str(b1 - 2 * db)]]
        return Q('Two sequences are written out as follows.',
                 [('What would be the 10th term in sequence A?', a1 + 9 * da), (f'Which term in sequence A is equal to {target}?', f'term {k}'), ('At which term does sequence A equal sequence B?', f'term {n0}')],
                 table=dict(rows=tbl, widths=[1500, 2400, 1300, 1300, 1300]))
    if m == 2:
        a, b = r.choice([(3, -7), (4, -3), (5, -4), (3, -2), (6, -5)]); c = r.choice([2, 1, 2]); 
        while c >= a: c -= 1
        n0 = r.randint(6, 15); d = b + (a - c) * n0; 
        n1 = r.randint(5, 9); n2 = r.randint(17, 30)
        f = lambda n: a * n + b; g = lambda n: c * n + d
        nm = r.sample(['Tom', 'Jon', 'Mia', 'Sara', 'Dev'], 2)
        return Q(f'{nm[0]} is making a table of values for the formula {fmt_lin(a,b)}. {nm[1]} is making a table of values for the formula {fmt_lin(c,d)}.',
                 [(f'What value does {nm[0]} get when n = {n1}?', f(n1)), (f'Which formula gives the bigger value when n = {n2}? Give your answer as {fmt_lin(a,b)} or {fmt_lin(c,d)}.', fmt_lin(a, b) if f(n2) > g(n2) else fmt_lin(c, d)),
                  ('For which value of n do the two formulas give the same value?', n0)])
    d = r.randint(3, 8); c0 = r.randint(1, 6); sh = r.randint(2, 5)
    seq = [d * n + c0 for n in range(1, 6)]; seq2 = [x - sh for x in seq]
    return Q(f'Look at this sequence: {", ".join(map(str,seq))}, …  The formula for term n is {fmt_lin(d,c0)}.',
             [('What is the 20th term of the sequence?', d * 20 + c0), ('How much bigger is the 167th term than the 164th term?', 3 * d),
              (f'What is the formula for term n of the related sequence {", ".join(map(str,seq2))}, … ?', fmt_lin(d, c0 - sh))])

# ---------- rectangles with equal perimeter / area ----------
def t_rect(r, v, tag):
    path = make_fig_path(tag)
    cands = []
    for a in range(3, 30):
        for b in range(2, 30):
            if a == b or a <= 2 * b: continue
            num = 2 * b * (a - b); den = a - 2 * b
            if den > 0 and num % den == 0:
                x = num // den; y = x + a - b
                if x > 0 and y > 0 and x != a and y != b and x < 80: cands.append((a, b, x, y))
    a, b, xc, yc = r.choice(cands)
    # (a) same perimeter: y = x + a - b with chosen x0
    x0 = r.randint(6, 20) 
    while x0 + a - b <= 0: x0 += 1
    ya = x0 + a - b
    # (b) same area: x*a = b*y -> choose y1 multiple
    from math import gcd
    step = a // gcd(a, b); y1 = step * r.randint(2, 6); xb = F(b * y1, a)
    assert xc * a == 2 * b * yc and xc + a == b + yc
    rect_pair(path, dict(top='x cm', side=f'{a} cm'), dict(top=f'{b} cm', side='y cm'))
    return Q('The two rectangles below are not drawn to scale.',
             [(f'The two rectangles have the same perimeter. If x = {x0}, find y.', ya), (f'The two rectangles have the same area. If y = {y1}, find x.', dec(xb)),
              ('Now the two rectangles have the same perimeter, but the left-hand rectangle has double the area of the right-hand rectangle. Find x.', xc)], fig=(path, 5.2))
