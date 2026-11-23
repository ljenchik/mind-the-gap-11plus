from common import *
from y56a import isprime, rnd10
from y56b import NAMES

def to_roman(n):
    out = ''
    for v_, s in [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]:
        while n >= v_: out += s; n -= v_
    return out
ONES = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
def words(n):
    def below100(k): return ONES[k] if k < 20 else TENS[k // 10] + ('-' + ONES[k % 10] if k % 10 else '')
    parts = []
    th, rest = divmod(n, 1000)
    if th: parts.append(ONES[th] + ' thousand')
    h, t = divmod(rest, 100)
    if h: parts.append(ONES[h] + ' hundred')
    s = ', '.join(parts)
    if t: s = (s + ' and ' if h or (th and not h) else s) + below100(t)
    return s

def y_arith(r, v, tag):
    if v % 2 == 0:
        while True:
            a = r.randint(120, 899); b = r.randint(36, 98)
            if a % 100 + b >= 100 and a % 10 + b % 10 >= 10: break
        while True:
            c = r.randint(1100, 2400); d = r.randint(150, 899)
            if c % 10 < d % 10 and c - d > 0: break
        dv = r.choice([3, 4, 5, 6, 7, 8, 9]); qq = r.choice([k for k in range(21, 99) if k % 10])
        return Q(None, [(f'Calculate {a} + {b}.', a + b), (f'Calculate {c} − {d}.', c - d), (f'Calculate {dv*qq} ÷ {dv}.', qq)])
    while True:
        a = r.randint(1200, 4800); b = r.randint(245, 899)
        if a % 100 + b % 100 >= 100: break
    c = r.randint(2000, 5999); d = r.choice([k for k in range(46, 99) if k % 10 > 1])
    while not (c % 10 < d % 10): c += 1
    x = r.randint(112, 349); y = r.choice([3, 4, 5, 6])
    return Q(None, [(f'Calculate {a} + {b}.', a + b), (f'Calculate {c} − {d}.', c - d), (f'Calculate {x} × {y}.', x * y)])

def y_tables(r, v, tag):
    a, b = r.sample([6, 7, 8, 9, 11, 12], 2); c, d = r.sample([6, 7, 8, 9, 12], 2); e = r.choice([6, 7, 8, 9, 11, 12]); f_ = r.randint(6, 12)
    if v % 2 == 0:
        return Q(None, [(f'Find {a} × {b}.', a * b), (f'Find {c*d} ÷ {d}.', c), (f'Fill in the box.   □ × {e} = {e*f_}', f_)])
    return Q(None, [(f'Find {b} × {a}.', a * b), (f'How many groups of {d} can be made from {c*d}?', c), (f'Fill in the box.   {f_} × □ = {e*f_}', e)])

def raw(n, d):
    return VUL.get((n, d)) or (str(n).translate(SUP) + '⁄' + str(d).translate(SUB))

def y_pv(r, v, tag):
    m = v % 3
    if m == 0:
        while True:
            n = r.randint(1000, 9999); s_ = str(n)
            if '0' not in s_ and len(set(s_)) == 4: break
        parts_ = [int(s_[0]) * 1000, int(s_[1]) * 100, int(s_[2]) * 10, int(s_[3])]
        k = r.choice([1, 2])
        shown = ' + '.join('□' if i == k else str(p) for i, p in enumerate(parts_))
        t = r.randint(2000, 8990)
        return Q(None, [(f'Fill in the box.   {n} = {shown}', parts_[k]), (f'What number is 1000 more than {t}?', t + 1000),
                        (f'What is the value of the digit {s_[2]} in the number {n}?', parts_[2])])
    if m == 1:
        n = r.choice([3406, 5062, 7280, 4915, 6038, 2704, 8150]); n2 = n + r.choice([111, 222, 333, 1010])
        return Q(None, [(f'Write {n} in words.', words(n)), (f'What number is 100 less than {n}?', n - 100), (f'Write this number in figures: {words(n2)}', n2)])
    while True:
        n = r.randint(3, 8) * 1000 + r.randint(1, 9) * 100 + r.randint(1, 9) * 10 + r.randint(1, 9)
        if (n // 10) % 10 < 8: break
    lst = [n, n + 1000, n - 100, n + 10]; r.shuffle(lst)
    return Q(None, [(f'What number is 10 more than {n}?', n + 10), (f'What is the tens digit in {n}?', (n // 10) % 10),
                    (f'Write these numbers in order, smallest first: {",  ".join(map(str, lst))}', ',  '.join(map(str, sorted(lst))))])

def y_round(r, v, tag):
    if v % 2 == 0:
        n = r.randint(1100, 8999)
        while n % 10 in (0, 5) or (n // 10) % 10 in (0, 5) or (n // 100) % 10 in (0, 5): n = r.randint(1100, 8999)
        return Q(f'Round {n} to the nearest:', [('10', rnd10(n)), ('100', rnd10(n, 100)), ('1000', rnd10(n, 1000))])
    d = r.randint(150, 4999)
    while d % 10 == 0 or d % 100 in range(20, 30) or d % 5 == 0 or (2 * d) % 100 in (50, 0): d = r.randint(150, 4999)
    tot = 2 * d
    p = [f'A lorry driver travels {d} km to a port and drives back the same way. How far is the round trip?', 'Round the round trip distance to the nearest 100 km.', 'Round the round trip distance to the nearest 1000 km.']
    return Q(None, [(p[0], f'{tot} km'), (p[1], f'{rnd10(tot,100)} km'), (p[2], f'{rnd10(tot,1000)} km')])

def y_negroman(r, v, tag):
    a = r.randint(2, 6); b = r.randint(a + 2, 9)
    n1 = r.choice([x for x in range(14, 49) if x not in (19, 29, 39)]); n2 = r.randint(51, 99)
    m = v % 2
    if m == 0:
        t1 = r.randint(2, 6); fall = r.randint(t1 + 2, 10)
        p0 = (f'At 6 pm the temperature was {t1}°C. By midnight it had fallen by {fall} degrees. What was the temperature at midnight?', f'{t1-fall}°C')
    else:
        p0 = (f'One winter morning it is −{a}°C in Colchester and −{b}°C in Southend. Which town is colder, and by how many degrees?', f'Southend, by {b-a} degrees')
    return Q(None, [p0, (f'What number is {to_roman(n1)}?', n1), (f'Write {n2} in Roman numerals.', to_roman(n2))])

def y_fractions(r, v, tag):
    d = r.choice([4, 5, 8, 10]); n = r.randint(1, d - 1); amt = d * r.randint(3, 9)
    pa = (f'Find {raw(n, d)} of {amt}.', dec(F(n * amt, d)))
    d2 = r.choice([5, 8, 10, 12]); x = r.randint(1, d2 - 2)
    y = r.randint(1, d2 - 1 - x) if v % 2 == 0 else r.randint(d2 - x + 1, d2 - 1)
    pb = (f'Calculate  {raw(x, d2)} + {raw(y, d2)}.', frac(F(x + y, d2)))
    k = r.choice([2, 3, 4]); base = r.choice([(1, 2), (2, 3), (3, 4), (1, 3), (2, 5)]); den = base[1] * k
    pc = (f'Fill in the box to make the fractions equal.   {raw(*base)} = □ ⁄ {den}', base[0] * k)
    return Q(None, [pa, pb, pc])

def y_decimals(r, v, tag):
    m = v % 2
    if m == 0:
        k = r.randint(1, 9); j = r.randint(1, 3)
        a, b = F(r.randint(11, 39), 10), F(r.randint(11, 39), 10)
        return Q(None, [(f'Write {raw(k, 10)} as a decimal.', dec(F(k, 10))),
                        (f'Which is bigger, {dec(F(k,10))} or {dec(F(k,10)-F(j,100))}?', dec(F(k, 10))),
                        (f'Calculate {dec(a)} + {dec(b)}.', dec(a + b))])
    vals = r.sample([F(x, 100) for x in (6, 8, 9, 50, 56, 57, 60, 65, 70, 75, 80, 85, 90, 95)], 5)
    a, b = F(r.randint(2, 9), 10), F(r.randint(2, 9), 10); c = F(r.randint(3, 9), 10) + F(r.randint(1, 9), 100)
    return Q(None, [(f'Write these numbers in order, smallest first:  {",  ".join(dec(x) for x in vals)}', ',  '.join(dec(x) for x in sorted(vals))),
                    (f'Calculate {dec(a)} + {dec(b)}.', dec(a + b)),
                    (f'Write {dec(c)} as a fraction with denominator 100.', raw(int(c*100), 100))])

