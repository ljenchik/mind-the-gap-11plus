from common import *

def isprime(n):
    if n < 2: return False
    return all(n % k for k in range(2, int(n ** .5) + 1))
def rnd10(x, u=10): return int(math.floor(x / u + 0.5)) * u   # halves round up

# ---------- Q1 arithmetic ----------
def t_arith(r, v, tag):
    if v % 2 == 0:
        while True:
            a = r.randint(1100, 5999); b = r.randint(55, 99)
            if a % 100 + b >= 100 and a % 10 + b % 10 >= 10: break
        while True:
            c = r.randint(2000, 6999); d = r.randint(250, 899)
            if c % 10 < d % 10 and (c // 10) % 10 < (d // 10) % 10: break
        dv = r.choice([6, 6, 7, 7, 8, 9]); qq = r.choice([k for k in range(45, 200) if k % 10])
        return Q(None, [(f'Calculate {a} + {b}.', a + b), (f'Calculate {c} − {d}.', c - d), (f'Calculate {dv*qq} ÷ {dv}.', qq)])
    a = r.randint(1000, 5999); b = r.choice([996, 997, 998, 999])
    c = r.randint(2000, 4999); d = r.choice([597, 698, 797, 896, 997])
    x = r.randint(21, 48); y = r.randint(21, 59)
    return Q(None, [(f'Calculate {a} + {b}.', a + b), (f'Calculate {c} − {d}.', c - d), (f'Work out {x} × {y}.', x * y)])

# ---------- Q2 fractions (4 parts) ----------
def t_fractions(r, v, tag):
    dp = r.choice([(3, 4), (3, 5), (4, 5), (5, 6), (3, 8), (5, 4), (2, 5), (3, 6)])
    w1, w2 = r.randint(1, 4), r.randint(1, 3)
    n1 = r.randint(1, dp[0] - 1); n2 = r.randint(1, dp[1] - 1)
    x = F(w1) + F(n1, dp[0]); y = F(w2) + F(n2, dp[1])
    pa = [(f'Calculate the value of {frac(x)} + {frac(y)}.', x + y)]
    if v % 2: pa = [(f'Calculate the value of {frac(x + y)} − {frac(y)}.', x)] if False else [(f'Calculate the value of {frac(max(x,y)+1)} − {frac(min(x,y))}.', max(x,y)+1-min(x,y))]
    while True:
        d1, d2 = r.choice([(8, 5), (9, 4), (7, 6), (8, 3), (6, 5), (9, 2), (7, 3), (10, 3)])
        a = F(r.randint(1, d1 - 1), d1); b = F(r.randint(1, d2 - 1), d2)
        if a > b and a - b != 0: break
    pb = (f'Calculate the value of {frac(a)} − {frac(b)}.', a - b)
    c = v % 3
    if c == 0:
        d = r.choice([3, 4, 5, 6, 8]); k = r.choice([5, 7, 9, 10, 12, 15]); pc = (f'Fill in the box to make the calculation work.   □ ÷ {frac(F(1, d))} = {k}', F(k, d))
    elif c == 1:
        b_, a_ = r.choice([(3, 2), (4, 3), (5, 4), (5, 2), (3, 1)]); m = r.randint(3, 9); res = m * F(a_, b_)
        pc = (f'Fill in the box to make the calculation work.   □ × {frac(F(a_, b_))} = {frac(res)}', m)
    else:
        k = r.choice([3, 4, 6, 7, 9]); xx = F(r.randint(1, 4), r.choice([3, 4, 5]))
        pc = (f'Fill in the box to make the calculation work.   {k} × □ = {frac(k*xx)}', xx)
    e = (v + 1) % 3
    if e == 0:
        B = F(r.randint(1, 2)) + F(r.randint(1, 4), 5); xx = F(r.choice([3, 7, 9, 11, 13, 17]), 20); A = B + xx
        pd = (f'Fill in the box to make the subtraction work.   {frac(A)} − □ = {frac(B)}', xx)
    elif e == 1:
        while True:
            p, q, s, t = r.randint(1, 4), r.randint(2, 7), r.randint(1, 5), r.randint(2, 8)
            a_, b_ = F(p, q), F(s, t)
            if a_ < 1 and b_ < 1 and (a_ * b_).denominator < a_.denominator * b_.denominator: break
        pd = (f'Work out {frac(a_)} × {frac(b_)}. Give your answer in its simplest form.', a_ * b_)
    else:
        d = r.choice([3, 4, 5]); w = r.randint(1, 4); n = r.randint(1, d - 1); mm = w + F(n, d)
        pd = (f'Work out {frac(mm)} ÷ {frac(F(1, d))}.', mm * d)
    parts = [pa[0], pb, pc, pd]
    return Q(None, [(t, frac(a) if isinstance(a, F) else a) for t, a in parts])

# ---------- Q3 powers ----------
def t_powers(r, v, tag):
    b, e = r.choice([(3, 5), (2, 7), (5, 3), (4, 3), (6, 3), (7, 3), (2, 8), (3, 4), (5, 4), (2, 6), (3, 6)])
    b0, e0 = r.choice([(7, 5), (4, 5), (6, 4), (8, 3), (9, 3), (5, 5)])
    intro = f'{b0}{sup(e0)} means {" × ".join([str(b0)]*e0)}.   Fill in the boxes to make these statements correct.'
    pa = (f'{b} raised to the power □ = {b**e}', e)
    if v % 2 == 0:
        x = r.choice([2, 3, 4, 5]); pb = (f'□{sup(4)} = {x**4}', x)
    else:
        bb, ee = r.choice([(3, 5), (2, 8), (5, 4), (4, 4)]); k = r.choice([1, 2])
        pb = (f'{bb} raised to the power □ ÷ {bb**k} = {bb**(ee-k)}', ee)
    parts = [pa, pb]
    if v % 3 == 2:
        a, c = r.choice([(3, 4), (2, 5), (2, 6), (3, 5), (2, 7)])
        big = max(a ** c, c ** a); lo = min(a ** c, c ** a)
        who = f'{a}{sup(c)}' if a ** c > c ** a else f'{c}{sup(a)}'
        parts.append((f'Which is bigger, {a}{sup(c)} or {c}{sup(a)}? Work out the difference between them.', f'{who} is bigger; difference {big-lo}'))
    return Q(intro, parts)

# ---------- Q4 ordering ----------
FRPOOL = [F(1, 3), F(2, 5), F(3, 8), F(3, 4), F(5, 8), F(4, 5), F(2, 3), F(5, 6), F(7, 8), F(1, 4), F(1, 5), F(3, 5), F(7, 10), F(9, 20), F(1, 2), F(11, 15)]
def t_order(r, v, tag):
    while True:
        frs = r.sample(FRPOOL, 3)
        decs = [F(r.randint(21, 89), 100) if r.random() < .7 else F(r.randint(2, 8), 10) for _ in range(2)]
        vals = frs + decs
        if len(set(vals)) < 5: continue
        shown = [frac(x) if x in frs else dec(x) for x in vals]
        r.shuffle(vals) if False else None
        t = F(r.randint(25, 85), 100)
        diffs = sorted((abs(x - t), x) for x in vals)
        if diffs[0][0] > 0 and diffs[1][0] - diffs[0][0] >= F(2, 100) and t not in vals: break
    order = list(range(5)); r.shuffle(order)
    lst = [shown[i] for i in order]; vv = [vals[i] for i in order]
    fmt = lambda x: frac(x) if x in frs else dec(x)
    p1 = ('Which is the smallest number?', fmt(min(vv))) if v % 2 == 0 else ('Which is the largest number?', fmt(max(vv)))
    p2 = (f'Which number is closest in value to {dec(t)}?', fmt(diffs[0][1]))
    return Q(['This question is about the following numbers.', '     ' + '        '.join(lst)], [p1, p2])

# ---------- Q5 decimals ----------
def t_dec(r, v, tag):
    nz = lambda lo, hi, dn: F(r.choice([k for k in range(lo, hi + 1) if k % 10]), dn)
    a = nz(21, 89, 10); b = nz(105, 899, 100)
    c = nz(21, 49, 10); d = nz(105, 899, 100)
    if c <= d: c = d + F(r.randint(11, 29), 10)
    x = nz(21, 59, 10); y = F(r.choice([12, 15, 16, 24, 11, 13]), 10)
    qd = r.choice([F(12, 10), F(15, 10), F(25, 10), F(8, 10), F(6, 10)]); qq = r.randint(8, 30) 
    dividend = qd * qq
    opts = [(f'Calculate {dec(a)} + {dec(b)}.', a + b), (f'Calculate {dec(c)} − {dec(d)}.', c - d),
            (f'Calculate {dec(x)} × {dec(y)}.', x * y), (f'Calculate {dec(dividend)} ÷ {dec(qd)}.', qq),
            (f'Calculate ({dec(F(r.randint(21,59),10))} × 1000) + ({dec(F(r.randint(105,399),100))} × 100).', None)]
    # last option: compute properly
    m1 = F(r.randint(21, 59), 10); m2 = F(r.randint(105, 399), 100)
    opts[4] = (f'Calculate ({dec(m1)} × 1000) + ({dec(m2)} × 100).', m1 * 1000 + m2 * 100)
    idx = [(0, 1, 2), (1, 2, 3), (0, 2, 3), (1, 3, 4), (0, 2, 4), (2, 3, 4)][v % 6]
    return Q(None, [(opts[i][0], dec(opts[i][1])) for i in idx])

# ---------- Q6 units ----------
def t_units(r, v, tag):
    def u1():
        x = F(r.choice(['4.721', '2.358', '6.043', '3.906', '5.206', '7.84', '12.37'])); return (f'How many cm are there in {dec(x)} m?', dec(x * 100))
    def u2():
        x = F(r.choice(['7.08', '2.35', '4.6', '12.045', '0.85', '3.2'])); return (f'How many metres are there in {dec(x)} km?', dec(x * 1000))
    def u3():
        x = F(r.choice(['2.075', '1.8', '0.64', '3.025', '5.5'])); return (f'How many grams are there in {dec(x)} kg?', dec(x * 1000))
    def u4():
        k = F(r.randint(101, 199), 10000); return (f'Convert {dec(k)} kg into mg. (1000 mg = 1 g and 1000 g = 1 kg.)', dec(k * 10**6))
    def u5():
        mg = r.randint(150, 450) * 100; return (f'Convert {mg} mg into kg. (1000 mg = 1 g and 1000 g = 1 kg.)', dec(F(mg, 10**6)))
    def u6():
        w = r.choice([20, 30, 40, 50, 60, 80]); L = r.randint(5, 16); A = F(L * w, 10)
        return (f'A rectangle has width {w} mm and area {dec(A)} cm². What is its length in cm?', L)
    def u7():
        n = r.choice([13, 15, 17, 19, 21]); return (f'There are 12 inches in 1 foot and 3 feet in 1 yard. How many inches are there in {n} yards?', 36 * n)
    def u8():
        m = r.choice([F(3, 2), F(5, 2), F(7, 2), F(9, 2)]); return (f'A mile is 1760 yards. How many feet are there in {frac(m)} miles?', dec(m * 1760 * 3))
    def u9():
        a, b = r.randint(3, 9), r.randint(4, 12); return (f'A rectangle measures {a} m by {b} m. What is its area in cm²?', a * b * 10000)
    def u10():
        x = F(r.choice(['0.35', '0.8', '1.25', '2.4', '3.5'])); return (f'A jug holds {dec(x)} litres. How many 50 ml cups can be filled from it?', dec(x * 1000 / 50))
    def u11():
        mm = r.choice([540, 4007, 380, 1250, 905]); return (f'Write {mm} mm in cm.', dec(F(mm, 10)))
    def u12():
        mins = r.choice([385, 205, 470, 530, 245]); return (f'Write {mins} minutes in hours and minutes.', f'{mins//60} hours {mins%60} minutes')
    pool = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12]
    sets = [(0, 5, 6), (1, 8, 3), (2, 10, 7), (3, 5, 8), (0, 4, 6), (1, 9, 11), (2, 8, 5), (10, 4, 6), (0, 3, 7), (1, 5, 11), (2, 9, 6), (4, 5, 7)]
    s = sets[v % len(sets)]
    return Q(None, [pool[i]() for i in s])

# ---------- Q7 money & percentages ----------
def t_money(r, v, tag):
    m = v % 3
    if m == 0:
        p = r.choice([15, 35, 12.5, 30, 45]); amt = r.choice([240, 320, 160, 480, 640, 200, 120]) 
        if p == 12.5: amt = r.choice([96, 160, 240, 320])
        q = r.choice([10, 20, 25, 30]); price = r.choice([20, 45, 60, 85, 120, 150]) 
        q2 = r.choice([20, 25, 40]); orig = r.choice([40, 60, 80, 90, 120, 150, 200]); C = F(orig) * (1 + F(q2, 100))
        verb = r.choice(['increased', 'reduced'])
        newp = F(price) * (1 + F(q, 100)) if verb == 'increased' else F(price) * (1 - F(q, 100))
        # reverse
        if verb == 'increased':
            after = F(orig) * (1 + F(q2, 100)); pc = (f'The price of a jacket was increased by {q2}%. After the increase it costs {gbp(after*100)}. What did it cost before the increase?', gbp(orig * 100))
        else:
            after = F(orig) * (1 - F(q2, 100)); pc = (f'In a sale the price of a jacket is reduced by {q2}%. The sale price is {gbp(after*100)}. What was the price before the sale?', gbp(orig * 100))
        return Q(None, [(f'Find {dec(F(str(p)))}% of £{amt}.', gbp(F(str(p)) * amt)),
                        (f'A coat costs £{price}. Its price is {verb} by {q}%. What is the new price?', gbp(newp * 100)), pc])
    if m == 1:
        P = r.choice([48, 64, 80, 120, 160, 200, 72]); p1 = r.choice([10, 15, 20, 25, 30]); p2 = r.choice([10, 20, 5])
        exp_ = F(P) * (1 - F(p1 + p2, 100)); act = F(P) * (1 - F(p1, 100)) * (1 - F(p2, 100))
        intro = f'Mr Brown buys a coat. The original price of the coat is £{P}. In the sale it has {p1}% off. Mr Brown also has a loyalty card which gives {p2}% off, so he expects to get {p1+p2}% off.'
        return Q(intro, [('What did Mr Brown expect to pay?', gbp(exp_ * 100)),
                         (f'In fact the shop gives him {p2}% off the sale price, not off the original price. What did Mr Brown actually pay?', gbp(act * 100)),
                         ('How much more did he pay than he expected?', gbp((act - exp_) * 100))])
    B = r.choice([60, 80, 120, 160, 200, 240]); k = r.choice([10, 15, 20, 25, 30, 35, 40]); R = F(B * k, 100)
    return Q(None, [(f'Calculate a quarter of £{B}.', gbp(F(B, 4) * 100)), (f'Calculate 11% of £{B}.', gbp(F(11 * B, 100) * 100)),
                    (f'A coat costing £{B} is reduced in a sale by {gbp(R*100)}. What percentage discount is this?', f'{k}%')])
