from common import *
from y56a import isprime, rnd10
from y56b import NAMES
from y4a import *

def y_money(r, v, tag):
    if v % 2 == 0:
        note = r.choice([5, 10, 20]); price = r.randint(1, note - 1) * 100 + r.choice([35, 45, 65, 85, 15, 75])
        p1, p2, p3 = r.randint(45, 299), r.randint(45, 299), r.randint(45, 299)
        ad, ch = r.choice([(18, 12), (15, 9), (14, 8), (12, 7)]); na, nc = r.choice([(2, 3), (1, 4), (2, 2), (3, 2)])
        return Q(None, [(f'Ravi pays with a £{note} note for something that costs {gbp(price)}. How much change does he get?', gbp(note * 100 - price)),
                        (f'A pencil costs {p1}p, a rubber costs {p2}p and a ruler costs {p3}p. What is the total cost of all three? Give your answer in pounds.', gbp(p1 + p2 + p3)),
                        (f'Zoo tickets cost £{ad} for an adult and £{ch} for a child. How much do {na} adult{"s" if na>1 else ""} and {nc} child{"ren" if nc>1 else ""} pay altogether?', gbp((na * ad + nc * ch) * 100))])
    each = r.choice([28, 35, 45, 60]); n_ = r.choice([6, 8, 9, 12])
    pens = r.choice([3, 4]); pp = r.choice([120, 140, 150, 160, 220, 240])
    n1 = r.choice([4, 5]); u = r.choice([25, 30, 35, 40]); n2 = r.choice([8, 10]); delta = r.choice([-5, 5]); u2 = u + delta
    return Q(None, [(f'Apples cost {each}p each. How much do {n_} apples cost? Give your answer in pounds.', gbp(each * n_)),
                    (f'Mia has £10. She buys {pens} pens at {gbp(pp)} each. How much money does she have left?', gbp(1000 - pens * pp)),
                    (f'A pack of {n1} stickers costs {gbp(n1*u)}. A pack of {n2} stickers costs {gbp(n2*u2)}. Which pack is cheaper for each sticker?',
                     f'The pack of {n2} ({u2}p each, compared with {u}p each)' if u2 < u else f'The pack of {n1} ({u}p each, compared with {u2}p each)')])

def y_units(r, v, tag):
    def u1(): x = r.choice([2, 3, 4, 6, 7, 8, 9]) + r.choice([0, 0.5, 0.25, 0.75]) ; x = F(str(x)); return (f'How many cm are there in {dec(x)} m?', dec(x * 100))
    def u2(): x = F(r.choice(['1.5', '2.5', '3.25', '4.5', '0.75'])); return (f'How many grams are there in {dec(x)} kg?', dec(x * 1000))
    def u3(): x = F(r.choice(['2', '3', '1.5', '0.5', '4.5'])); return (f'How many millilitres are there in {dec(x)} litres?', dec(x * 1000))
    def u4(): h = r.randint(1, 4); m = r.choice([15, 20, 25, 40, 45]); return (f'How many minutes are there in {h} hour{"s" if h>1 else ""} {m} minutes?', h * 60 + m)
    def u5(): mins = r.choice([75, 95, 110, 135, 150, 205]); return (f'Write {mins} minutes in hours and minutes.', f'{mins//60} hour{"s" if mins//60>1 else ""} {mins%60} minutes')
    def u6(): x = r.choice([54, 72, 36, 128, 245, 460]); return (f'Write {x} mm in cm.', dec(F(x, 10)))
    def u7(): x = r.choice([1450, 2300, 3250, 4075, 1900]); return (f'Write {x} g in kg.', dec(F(x, 1000)))
    def u8(): x = r.choice([2, 3, 4, 5]); y = r.choice([150, 250, 125, 300]); return (f'A jug holds {x} litres. How many {y} ml cups can be filled from it?', None)
    def u9(): x = r.choice([2, 3, 5, 6, 8]); return (f'How many metres are there in {x} km?', x * 1000)
    pool = [u1, u2, u3, u4, u5, u6, u7, u9]
    sets = [(0, 1, 3), (2, 5, 4), (7, 6, 0), (1, 4, 2), (3, 5, 6), (7, 2, 4), (0, 6, 3), (1, 5, 4), (2, 7, 3), (6, 0, 4)]
    return Q(None, [pool[i]() for i in sets[v % len(sets)]])

def y_time(r, v, tag):
    m = v % 3
    if m == 0:
        s = r.randrange(9 * 60 + 5, 14 * 60, 5); d = r.choice([95, 105, 130, 150, 85, 140])
        while s % 60 + d % 60 < 60 and False: pass
        return Q(f'A film starts at {hm(s)} and lasts {dur(d)}.', [('At what time does the film end?', hm(s + d)), (f'A second film ends at {hm(s+d+30)} and also lasts {dur(d)}. At what time did it start?', hm(s + 30)),
                                                                   ('How many minutes does the first film last?', d)])
    if m == 1:
        h1 = r.randint(13, 21); m1 = r.choice([15, 20, 35, 40, 45, 50]); h2 = h1 + 1; m2 = r.choice([5, 10, 20, 25])
        return Q(None, [(f'Write {hm(h1*60+m1)} using the 12-hour clock with am or pm.', clock12(h1 * 60 + m1)),
                        (f'How many minutes are there from {hm(h1*60+m1)} to {hm(h2*60+m2)}?', (h2 * 60 + m2) - (h1 * 60 + m1)),
                        (f'A bus journey takes 1 hour 25 minutes and ends at {hm(h2*60+m2)}. At what time did the journey start?', hm(h2 * 60 + m2 - 85))])
    w = r.choice([20, 25, 35, 40]); end = r.randrange(10 * 60 + 5, 16 * 60, 5)
    return Q(f'Priya walks to school. The walk takes {w} minutes and she arrives at {hm(end)}.',
             [('At what time did she leave home?', hm(end - w)), (f'One day she leaves 8 minutes later. At what time does she arrive?', hm(end + 8)),
              ('How many walks of this length would take 2 hours altogether?'.replace('How many walks of this length would take 2 hours altogether?', f'She walks to school and back each day. How many minutes does she walk in 5 days?'), w * 2 * 5)])

def y_perim(r, v, tag):
    L = r.randint(8, 16); W = r.randint(4, L - 2); sq = r.choice([5, 6, 7, 8, 9, 10, 12])
    m = v % 2
    if m == 0:
        return Q(f'A rectangle is {L} cm long and {W} cm wide.', [('Find the perimeter of the rectangle.', f'{2*(L+W)} cm'), ('Find the area of the rectangle.', f'{L*W} cm²'),
                                                              (f'A square has a perimeter of {4*sq} cm. How long is one side of the square?', f'{sq} cm')])
    P = 2 * (L + W)
    return Q(None, [(f'A rectangle has a perimeter of {P} cm. Its length is {L} cm. What is its width?', f'{W} cm'), (f'Find the area of the rectangle in part (a).', f'{L*W} cm²'),
                    (f'A square has an area of {sq*sq} cm². What is its perimeter?', f'{4*sq} cm')])

def y_seq(r, v, tag):
    m = v % 3
    if m == 0:
        a = r.choice([2350, 1450, 3275, 950]); st = r.choice([100, 25, 50, 250])
        seq = [a + k * st for k in range(3)]
        return Q(None, [(f'Write the next three numbers in this sequence:  {", ".join(map(str, seq))}, ___, ___, ___', ', '.join(str(a + k * st) for k in range(3, 6))),
                        (f'Write the missing numbers:  {a}, ___, {a+2*st*3}, {a+3*st*3}, ___', f'{a+st*3} and {a+4*st*3}'),
                        (f'This sequence goes down in steps of {st}:  {a+3*st}, {a+2*st}, {a+st}, ___, ___. Write the next two numbers.', f'{a}, {a-st}')])
    if m == 1:
        st = r.choice([300, 250, 200, 400]); top = st * r.randint(2, 4) + r.choice([100, 50])
        s = [top - st * k for k in range(3)]; ans = [top - st * k for k in range(3, 6)]
        return Q(None, [(f'This sequence goes down in steps of {st}. Write the next three numbers:  {", ".join(map(str,s))}, ___, ___, ___', ', '.join(map(str, ans))),
                        (f'Write the next number in this sequence:  7, 14, 21, 28, ___', 35), (f'Write the next two numbers:  {r.choice([4,6])*2}, {r.choice([4,6])*2+6}, ___, ___' , None)]) if False else Q(None, [
                        (f'This sequence goes down in steps of {st}. Write the next three numbers:  {", ".join(map(str,s))}, ___, ___, ___', ', '.join(str(x) for x in ans)),
                        (lambda k_: (f'Write the next two numbers in this sequence:  {k_}, {2*k_}, {3*k_}, {4*k_}, ___, ___', f'{5*k_}, {6*k_}'))(r.choice([6, 7, 8, 9, 11, 12])),
                        (f'Counting on in 25s from {r.choice([950, 975, 925])}, what is the first number greater than 1000?', 1025)])
    a = r.choice([6, 5, 8, 9]); st = r.choice([7, 6, 4, 9]); seq = [a + st * k for k in range(4)]
    k = r.randint(8, 12)
    return Q(f'A sequence starts at {a} and goes up by {st} each time.', [('Write the first four terms.', ', '.join(map(str, seq))), ('What is the 10th term?', a + st * 9), (f'Which term is {a+st*(k-1)}?', f'term {k}')])

def y_chart(r, v, tag):
    path = make_fig_path(tag); cats = r.choice([['Apples', 'Bananas', 'Grapes', 'Pears', 'Oranges'], ['Cycling', 'Swimming', 'Football', 'Tennis', 'Rugby'], ['Cat', 'Dog', 'Fish', 'Rabbit', 'Hamster']])
    vals = r.sample(range(2, 16), 5)
    bar_chart(path, cats, vals, 'Choice', 'Number of children', ymax=max(vals) + 1, step=1)
    a, b = r.sample(range(5), 2); hi = max(vals); lo = min(vals)
    return Q('Children in Class 4 voted for their favourite choice. The bar chart shows the results.',
             [(f'How many children chose {cats[a]}?', vals[a]), (f'How many more children chose {cats[vals.index(hi)]} than {cats[vals.index(lo)]}?', hi - lo), ('How many children voted altogether?', sum(vals))], fig=(path, 4.6))

def y_missing(r, v, tag):
    a = r.randint(120, 600); s = a + r.randint(150, 480); b = r.randint(250, 480); c = r.randint(b + 150, 999)
    if v % 2 == 0:
        return Q(None, [(f'Fill in the box.   □ + {a} = {s}', s - a), (f'Fill in the box.   {c} − □ = {b}', c - b)])
    n = r.randint(3, 9); k = r.randint(6, 12); r2 = r.randint(120, 700)
    return Q(None, [(f'Fill in the box.   □ − {a} = {r2}', a + r2), (f'Fill in the box.   □ ÷ {n} = {k}', n * k)])
