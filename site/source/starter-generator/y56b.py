from common import *
from y56a import isprime, rnd10

NAMES = ['Katie', 'Temmy', 'Arjun', 'Priya', 'Joel', 'Dylan', 'Sasha', 'Jordan', 'Mia', 'Omar', 'Leah', 'Ravi', 'Zara', 'Ben', 'Isla', 'Kofi']

# ---------- ratio / sharing ----------
def t_ratio(r, v, tag):
    m = v % 4
    nm = r.sample(NAMES, 3)
    if m == 0:
        k = r.randint(5, 17); mult = r.choice([2, 2, 3]); T = k * (1 + mult + mult * mult)
        intro = f'£{T} is shared between {nm[0]}, {nm[1]} and {nm[2]} so that {nm[0]} gets {"twice" if mult==2 else "three times"} as much as {nm[1]}, and {nm[1]} gets {"twice" if mult==2 else "three times"} as much as {nm[2]}.'
        return Q(intro, [(f'How much does {nm[2]} get?', f'£{k}'), (f'How much does {nm[0]} get?', f'£{k*mult*mult}')])
    if m == 1:
        d = r.choice([8, 12, 14, 16, 20, 24]); Y = r.randint(11, 45); T = 2 * Y + d
        intro = f'£{T} is shared between {nm[0]} and {nm[1]} so that {nm[0]} gets £{d} more than {nm[1]}.'
        return Q(intro, [(f'How much does {nm[1]} get?', f'£{Y}'), (f'What fraction of the £{T} does {nm[0]} get? Give your answer in its simplest form.', frac(F(Y + d, T)))])
    if m == 2:
        d = r.choice([4, 6, 8, 10]); D = r.randint(7, 30); S = D + d; J = 2 * S; T = D + S + J
        intro = f'£{T} is shared between {nm[0]}, {nm[1]} and {nm[2]}. {nm[1]} gets £{d} more than {nm[0]}, and {nm[2]} gets twice as much as {nm[1]}.'
        return Q(intro, [(f'How much does {nm[0]} get?', f'£{D}'), (f'How much does {nm[2]} get?', f'£{J}')])
    rec = r.choice([(200, 150, 100, 150), (250, 150, 100, 100), (300, 200, 100, 150), (200, 100, 100, 100), (250, 200, 50, 100)])
    G = sum(rec); kg = r.choice([2, 3, 4, 5]); target = kg * 1000
    if (target * rec[1]) % G: kg = 3; target = 3000
    while (target * rec[1]) % G: kg += 1; target = kg * 1000
    ch = r.choice([450, 600, 750, 900, 1050]); 
    while (ch * rec[3]) % rec[2]: ch += 50
    intro = (f'A recipe for scones uses {rec[0]} g of flour, {rec[1]} g of butter, {rec[2]} g of cheese and {rec[3]} g of milk.')
    return Q(intro, [(f'Sam keeps to the same proportions and wants {kg} kg of dough altogether. How much butter does he need?', f'{target*rec[1]//G} g'),
                     (f'Jo has {ch} g of cheese and wants to use all of it. How much milk does she need?', f'{ch*rec[3]//rec[2]} g')])

# ---------- formula machine ----------
MACH = [(3, 8, 2), (5, 9, 2), (4, 6, 2), (3, 10, 2), (5, 8, 3), (7, 12, 4), (4, 7, 3), (5, 6, 2), (3, 6, 2), (6, 10, 4)]
def t_machine(r, v, tag):
    m, c, d = MACH[v % len(MACH)]
    f = lambda x: F(m * x + c, d)
    ex = next(x for x in range(10, 30) if f(x).denominator == 1)
    x0 = next(x for x in range(r.randint(20, 55), 90) if f(x).denominator == 1)
    x1 = next(x for x in range(r.randint(15, 70), 130) if f(x).denominator == 1 and x != x0)
    fp = F(c, d - m); assert f(fp) == fp and fp < 0 and fp.denominator == 1
    dn = {2: 'Halve', 3: 'Divide by 3', 4: 'Divide by 4'}[d]
    intro = [f'A formula machine works as follows.', f'Number in  →  × {m}  →  + {c}  →  {dn}  →  Output',
             f'For example, if you put in {ex} the machine gives:  {ex} → {m*ex} → {m*ex+c} → {int(f(ex))}.  The output is {int(f(ex))}.']
    return Q(intro, [(f'Find the output if {x0} is the number put in.', int(f(x0))), (f'Find the number put in if {int(f(x1))} is the output.', x1),
                     ('Find a negative number to put in so that the output is the same as the number put in.', int(fp))])

# ---------- rounding bounds ----------
def t_round(r, v, tag):
    m = v % 3
    if m == 0:
        N1 = r.randint(30, 80) * 10; N2 = r.randint(30, 80) * 10
        while N2 == N1: N2 = r.randint(30, 80) * 10
        xs = [x for x in range(N1 - 20, N1 + 20) if rnd10(x) == N1]; ys = [y for y in range(N2 - 20, N2 + 20) if rnd10(y) == N2]
        ans = [max(xs), min(ys), max(xs) + max(ys), min(xs) - max(ys)]
        return Q(f'X and Y are whole numbers. X rounded to the nearest 10 gives {N1}. Y rounded to the nearest 10 gives {N2}.',
                 [('What is the largest possible value of X?', ans[0]), ('What is the smallest possible value of Y?', ans[1]),
                  ('What is the largest possible value of X + Y?', ans[2]), ('What is the smallest possible value of X − Y?', ans[3])])
    if m == 1:
        B = r.randint(40, 95) * 10; C = r.randint(8, 40) * 100
        bs = [x for x in range(B - 20, B + 20) if rnd10(x) == B]; cs = [x for x in range(C - 80, C + 80) if rnd10(x, 100) == C]
        return Q(f'A whole number B is rounded to the nearest 10 to give {B}. A whole number C is rounded to the nearest 100 to give {C}.',
                 [('What is the largest possible value of C?', max(cs)), ('What is the smallest possible value of B + C?', min(bs) + min(cs)),
                  ('What is the smallest possible value of C − B?', min(cs) - max(bs))])
    mult = r.choice([3, 4, 6]); N = r.choice([290, 190, 340, 250, 410]); N = rnd10(mult * (N // mult)) if False else N
    xs = [x for x in range(0, 400) if rnd10(mult * x) == N]
    N2 = r.choice([30, 50, 70, 90]); k = r.choice([4, 6, 8]); ds = [(D + k, D) for D in range(0, 200) if rnd10(2 * D + k) == N2]
    dec_ = F(r.randint(1500, 2999), 10)
    return Q(None, [(f'Round {dec(dec_)} to the nearest 10.', rnd10(int(dec_ + F(1, 2)) if False else math.floor(dec_ / 10 + F(1, 2)) * 10)),
                    (f'A whole number X is multiplied by {mult} and then rounded to the nearest 10 to give {N}. What is the largest possible value of X?', max(xs)),
                    (f'C and D are whole numbers and C is {k} larger than D. C and D are added and the result is rounded to the nearest 10 to give {N2}. What is the smallest possible value of C?', min(ds)[0])])

# ---------- mean ----------
def t_mean(r, v, tag):
    m = v % 3
    if m == 0:
        while True:
            marks = [r.randint(3, 10) for _ in range(7)]
            if sum(marks) % 7 == 0: break
        a = r.randint(4, 9); 
        while True:
            b = r.randint(8, 14)
            if (a + 2 * b) % 3 == 0 and a != b: break
        n = r.choice([10, 12, 20]); mm = r.choice([22, 24, 25, 18]); wr = r.randint(8, 14); rt = wr + r.choice([4, 6, 8])
        while F(n * mm + rt - wr, n).denominator not in (1, 2, 4, 5, 10, 20): rt += 2
        return Q(None, [(f'In a test out of 10 a group of pupils scored these marks: {", ".join(map(str, marks))}. What was the average (mean) mark?', sum(marks) // 7),
                        (f'In another test five boys averaged a score of {a} and ten girls averaged a score of {b}. Find the average (mean) for all fifteen children.', (a + 2 * b) // 3),
                        (f'In a third test a teacher found that {n} pupils had an average of {mm} marks. One pupil\'s test had been marked wrongly, giving {wr} marks when it should have been {rt}. What should the correct average be?', dec(F(n * mm + rt - wr, n)))])
    if m == 1:
        n = r.choice([6, 7, 8, 9]); avg = r.randint(11, 18)
        s = next(s for s in range(avg + 2, avg + 20) if (n * avg + s) % (n + 1) == 0)
        newavg = F(n * avg + s, n + 1); tgt = newavg + 1; ninth = tgt * (n + 2) - (n * avg + s)
        return Q(f'Jenna plays a computer game. After {n} attempts her average (mean) score is {avg}.',
                 [(f'What is the total of all her scores from the {n} attempts?', n * avg), (f'On her next attempt she scores {s}. What is her new average score?', dec(newavg)),
                  (f'What would she need to score on the attempt after that, to raise her average to exactly {dec(tgt)}?', dec(ninth))])
    while True:
        k = r.choice([2, 3, 4]); a = r.randint(4, 8); b = a + r.choice([2, 4, 6]); c = F(a + b, 2) if False else None
        g = r.choice([2, 3, 4, 5, 6, 8]); tot = F(k * a + g * b, k + g)
        if tot.denominator == 1 and a < tot < b: break
    sixlist = None
    while True:
        sixlist = [r.randint(2, 12) for _ in range(6)]
        if sum(sixlist) % 6 == 0: break
    return Q(None, [(f'The scores of six children in a test were {", ".join(map(str, sixlist))}. Find the average (mean) score.', sum(sixlist) // 6),
                    (f'A different test was sat by {k} boys and a number of girls. Altogether the children achieved an average of {int(tot)}. The average for the {k} boys was {a} and the average for the girls was {b}. How many girls were there?', g),
                    ('How many children sat that test altogether?', k + g)])

# ---------- time ----------
STN = [['London', 'Reading', 'Swindon', 'Bristol', 'Cardiff'], ['Leeds', 'Wakefield', 'Doncaster', 'Newark', 'Peterborough'], ['Exeter', 'Taunton', 'Bath', 'Swindon', 'Oxford'],
       ['Norwich', 'Ipswich', 'Colchester', 'Chelmsford', 'Stratford'], ['Carlisle', 'Penrith', 'Oxenholme', 'Preston', 'Wigan']]
def t_time(r, v, tag):
    m = v % 3
    if m == 0:
        names = STN[(v // 3) % len(STN)]
        T = r.choice([200, 250, 300, 350, 400]); off3 = T * 2 // 5
        while True:
            o1 = r.randrange(15, off3 - 30, 5); o2 = r.randrange(o1 + 15, off3 - 10, 5)
            if o2 < off3 - 5: break
        t0 = r.randrange(13 * 60, 18 * 60, 5)
        rows = [['Station', 'Time'], [names[0], hm(t0)], [names[1], hm(t0 + o1)], [names[2], hm(t0 + o2)], [names[3], hm(t0 + off3)]]
        a = (t0 + o2) - (t0 + o1)
        x = r.randrange(t0 + o1 + 10, t0 + o1 + 60, 5)
        z = r.randrange(t0 + 2 * o2 + 60, t0 + 2 * o2 + 160, 5)
        intro = [f'This is part of the train timetable between {names[0]} and a final station, {names[4]}.']
        parts = [(f'How long, in minutes, does the train take to travel from {names[1]} to {names[2]}?', a),
                 (f'The journey from {names[0]} to {names[3]} is 40% of the total journey time from {names[0]} to {names[4]}. At what time does the train reach {names[4]}?', hm(t0 + T)),
                 (f'When there are speed restrictions all journey times are doubled. A train leaves {names[1]} at {hm(x)} and travels under a speed restriction. At what time does it reach {names[3]}?', hm(x + 2 * (off3 - o1))),
                 (f'What is the latest time a train can leave {names[0]} and still reach {names[2]} by {hm(z)}, if it travels under a speed restriction?', hm(z - 2 * o2))]
        return Q(intro, parts, table=dict(rows=rows, widths=[2600, 1600]))
    if m == 1:
        H = r.choice([10, 12, 14, 18]); p = r.choice([30, 40, 50, 20]); leg = F(H * p, 100)
        d1 = r.choice([3, 4, 5]); d2 = r.choice([7, 8, 9]); stop = r.choice([1, 2, 3]); dep = r.randrange(9 * 60, 22 * 60, 10)
        arr1 = dep + leg * 60 + d1 * 60
        arr2 = dep + H * 60 + stop * 60 + d2 * 60
        def lt(mins):
            mins = int(mins); day = mins // 1440; t = hm(mins)
            return t + (' the next day' if day == 1 else (' two days later' if day == 2 else ''))
        intro = f'The total flying time from London to Singapore, stopping in Dubai, is {H} hours. The flight from London to Dubai takes {p}% of the total flying time. The plane leaves London at {hm(dep)}.'
        return Q(intro, [('How long does the flight from London to Dubai take, in hours and minutes?', dur(leg * 60)),
                         (f'Dubai is {d1} hours ahead of London time. Find the local time in Dubai when the plane arrives.', lt(arr1)),
                         (f'The plane stays in Dubai for {stop} hour{"s" if stop>1 else ""}. Singapore is {d2} hours ahead of London time. Find the local time in Singapore when the plane arrives.', lt(arr2))])
    pb = r.choice([3 * 60 + 44, 4 * 60 + 8, 3 * 60 + 52, 4 * 60 + 20, 3 * 60 + 36]); st = r.randrange(9 * 60 + 30, 12 * 60, 5); ex = r.choice([9, 12, 16, 21, 27])
    return Q(f'Anna is running a marathon. Her personal best is {pb//60} hours {pb%60} minutes. She starts the race at {clock12(st)}.',
             [('At what time does she need to finish to equal her personal best?', clock12(st + pb)),
              ('There are checkpoints a quarter, half and three quarters of the way round. At what time should she reach the three-quarter checkpoint if she runs at a steady pace and equals her personal best?', clock12(st + pb * 3 // 4)),
              (f'In fact she finishes at {clock12(st+pb+ex)}. How many minutes slower than her personal best is that?', ex)])

# ---------- angles ----------
def t_angles(r, v, tag):
    if v % 2 == 0:
        a, b, c = r.choice([(2, 3, 4), (1, 2, 6), (2, 3, 5), (3, 4, 5), (2, 5, 5), (3, 5, 7), (1, 3, 5), (1, 4, 5)])
        x = F(180, a + b + c); apex = r.choice([30, 40, 50, 64, 80, 100, 110])
        co = lambda k: '' if k == 1 else str(k)
        return Q(None,
                 [(f'The three angles of a triangle are {co(a)}x°, {co(b)}x° and {co(c)}x°. Find x.', dec(x)), ('Find the size of the largest angle in that triangle.', f'{dec(max(a,b,c)*x)}°'),
                  (f'An isosceles triangle has an angle of {apex}° between its two equal sides. Find the size of each of the other two angles.', f'{dec(F(180-apex,2))}°')])
    while True:
        p, q, s = r.choice([(2, 3, 4), (1, 2, 3), (2, 3, 5), (3, 4, 5), (1, 3, 5), (2, 5, 5)])
        if 180 % (p + q + s) == 0 or True: break
    sl = r.choice([(2, 3, 4), (1, 3, 5), (2, 3, 5), (1, 2, 6), (3, 4, 5), (1, 4, 4)])
    pt = r.choice([(3, 4, 5), (2, 3, 4), (2, 5, 5), (3, 4, 5)])
    n = r.choice([5, 6, 8, 9, 10, 12])
    co = lambda k: '' if k == 1 else str(k)
    return Q(None,
             [(f'Three angles on a straight line are {co(sl[0])}a°, {co(sl[1])}a° and {co(sl[2])}a°. Find a.', dec(F(180, sum(sl)))),
              (f'Three angles at a point are {co(pt[0])}b°, {co(pt[1])}b° and {co(pt[2])}b°. Find the size of the largest angle.', f'{dec(F(360, sum(pt)) * max(pt))}°'),
              (f'Find the size of one interior angle of a regular polygon with {n} sides.', f'{dec(F((n-2)*180, n))}°')])

# ---------- coordinates ----------
def t_coords(r, v, tag):
    path = make_fig_path(tag)
    if v % 2 == 0:
        while True:
            pts = [(r.randint(-5, 5), r.randint(-5, 5)) for _ in range(3)]
            area2 = abs((pts[1][0]-pts[0][0])*(pts[2][1]-pts[0][1]) - (pts[2][0]-pts[0][0])*(pts[1][1]-pts[0][1]))
            if len(set(pts)) == 3 and area2 >= 6 and all(x != 0 and y != 0 for x, y in pts) and len({x for x, _ in pts}) == 3: break
        grid_fig(path, [dict(pts=pts, names=['A', 'B', 'C'])])
        A, B, C = pts
        ops = [('reflected in the y-axis', lambda p: (-p[0], p[1])), ('reflected in the x-axis', lambda p: (p[0], -p[1])),
               ('rotated 90° clockwise about the origin (0, 0)', lambda p: (p[1], -p[0])), ('rotated 180° about the origin (0, 0)', lambda p: (-p[0], -p[1])),
               ('rotated 90° anticlockwise about the origin (0, 0)', lambda p: (-p[1], p[0]))]
        order = r.sample(range(5), 3); verts = r.sample(range(3), 3)
        parts = []
        for oi, vi in zip(order, verts):
            nm = 'ABC'[vi]; res = ops[oi][1](pts[vi])
            parts.append((f'Triangle ABC is {ops[oi][0]}. Give the coordinates of the new position of point {nm}.', f'({res[0]}, {res[1]})'))
        return Q('The diagram shows triangle ABC on a coordinate grid.', parts, fig=(path, 3.0))
    while True:
        B = (r.randint(-4, 2), r.randint(-4, 2)); w = r.randint(2, 5); h = r.randint(2, 4)
        A = (B[0], B[1] + h); C = (B[0] + w, B[1]); D = (C[0], A[1])
        if all(-6 <= c <= 6 for p in (A, B, C, D) for c in p): break
    pts3 = [A, B, C]
    grid_fig(path, [dict(pts=pts3, names=['A', 'B', 'C'])] if False else [dict(pts=[A], names=['A']), dict(pts=[B], names=['B']), dict(pts=[C], names=['C'])])
    return Q('The diagram shows three corners, A, B and C, of a rectangle ABCD.',
             [('Give the coordinates of the fourth corner, D.', f'({D[0]}, {D[1]})'), ('Find the area of the rectangle in square units.', w * h),
              ('The rectangle is reflected in the y-axis. Give the new coordinates of D.', f'({-D[0]}, {D[1]})')], fig=(path, 3.0))
