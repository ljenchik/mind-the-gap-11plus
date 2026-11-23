from common import *
from y56a import isprime
from y4b import *
import itertools

R4 = range(1, 61); ODD4 = list(range(1, 60, 2)); EVEN4 = list(range(2, 60, 2))
S4 = [
    ('When you add two odd numbers, you get an even number.', [(a, b) for a in ODD4 for b in ODD4], lambda a, b: (a + b) % 2 == 0),
    ('A multiple of 10 is also a multiple of 5.', [(x,) for x in range(10, 200, 10)], lambda a: a % 5 == 0),
    ('A multiple of 5 ends in 5.', [(x,) for x in range(5, 200, 5)], lambda a: a % 10 == 5),
    ('Doubling an odd number gives an even number.', [(x,) for x in ODD4], lambda a: (2 * a) % 2 == 0),
    ('An even number is a multiple of 4.', [(x,) for x in EVEN4], lambda a: a % 4 == 0),
    ('When you add three odd numbers, the answer is even.', [(a, b, c) for a in ODD4[:12] for b in ODD4[:12] for c in ODD4[:12]], lambda a, b, c: (a + b + c) % 2 == 0),
    ('A number that ends in 0 is a multiple of 5.', [(x,) for x in range(10, 300, 10)], lambda a: a % 5 == 0),
    ('When you subtract one even number from another, the answer is even.', [(a, b) for a in EVEN4 for b in EVEN4 if a >= b], lambda a, b: (a - b) % 2 == 0),
    ('A multiple of 3 is an odd number.', [(x,) for x in range(3, 100, 3)], lambda a: a % 2 == 1),
    ('When you multiply an odd number by an even number, the answer is even.', [(a, b) for a in ODD4 for b in EVEN4], lambda a, b: (a * b) % 2 == 0),
    ('A number that ends in 2 is a multiple of 4.', [(x,) for x in range(2, 200, 10)], lambda a: a % 4 == 0),
    ('When you add 1 to an even number, the answer is odd.', [(x,) for x in EVEN4], lambda a: (a + 1) % 2 == 1),
    ('A multiple of 6 is also a multiple of 3.', [(x,) for x in range(6, 200, 6)], lambda a: a % 3 == 0),
    ('When you multiply a number by 10, the answer ends in 0.', [(x,) for x in range(1, 200)], lambda a: (a * 10) % 10 == 0),
    ('The sum of two even numbers is a multiple of 4.', [(a, b) for a in EVEN4 for b in EVEN4], lambda a, b: (a + b) % 4 == 0),
    ('A number that is a multiple of 2 and a multiple of 5 is a multiple of 10.', [(x,) for x in range(10, 200, 10)], lambda a: a % 10 == 0),
]
def cls4(i):
    t, dom, f = S4[i]; res = [bool(f(*d)) for d in dom]
    return 'always' if all(res) else ('never' if not any(res) else 'sometimes')
C4 = [cls4(i) for i in range(len(S4))]

def y_asn(r, v, tag):
    byc = {c: [i for i in range(len(S4)) if C4[i] == c] for c in ('always', 'sometimes', 'never')}
    pat = [['always', 'sometimes', 'never'], ['sometimes', 'always', 'sometimes'], ['always', 'sometimes', 'sometimes'], ['sometimes', 'never', 'always']][v % 4]
    chosen = []
    for c in pat:
        pool = [i for i in byc[c] if i not in chosen]
        chosen.append(r.choice(pool))
    return Q('For each of these statements, say whether it is always true, sometimes true or never true.',
             [(S4[i][0], 'Sometimes true' if C4[i] == 'sometimes' else C4[i].capitalize() + ' true') for i in chosen])

def y_bounds(r, v, tag):
    if v % 2 == 0:
        N = r.randint(4, 14) * 10; xs = [x for x in range(N - 20, N + 20) if rnd10(x) == N]
        return Q(f'A whole number rounds to {N} when it is rounded to the nearest 10.',
                 [('What is the smallest the number could be?', min(xs)), ('What is the largest the number could be?', max(xs)), (f'How many different whole numbers round to {N}?', len(xs))])
    N = r.randint(2, 9) * 1000; xs = [x for x in range(N - 600, N + 600) if rnd10(x, 1000) == N]
    t = N + r.choice([-501, -450, 499, 500, 501, -499]); ok = rnd10(t, 1000) == N
    return Q(f'A whole number rounds to {N} when it is rounded to the nearest 1000.',
             [('What is the smallest the number could be?', min(xs)), ('What is the largest the number could be?', max(xs)), (f'Could the number be {t}? Answer yes or no.', 'Yes' if ok else 'No')])

def y_share(r, v, tag):
    m = v % 3; nm = r.sample(NAMES, 2)
    if m == 0:
        B = r.randint(8, 30); A = 2 * B; T = A + B; extra = r.randint(3, 9)
        return Q(f'{nm[0]} has twice as many stickers as {nm[1]}. Together they have {T} stickers.', [(f'How many stickers does {nm[1]} have?', B), (f'How many stickers does {nm[0]} have?', A),
                                                                                         (f'Their friend has {extra} more stickers than {nm[0]}. How many stickers does the friend have?', A + extra)])
    if m == 1:
        sm = r.randint(20, 40); df = r.choice([7, 9, 11, 13, 15]); big = sm + df; T = sm + big
        return Q(f'Two numbers add up to {T}. The difference between them is {df}.', [('What is the larger number?', big), ('What is the smaller number?', sm), ('Add 6 to each number. What is the difference between the two new numbers?', df)])
    C = r.randint(3, 9); B = 3 * C; A = 2 * B; T = A + B + C
    return Q(f'Three children share {T} marbles. {nm[0]} has {"twice"} as many as {nm[1]}, and {nm[1]} has three times as many as Dani.',
             [('How many marbles does Dani have?', C), (f'How many marbles does {nm[1]} have?', B), (f'How many marbles does {nm[0]} have?', A)])

def y_ages(r, v, tag):
    p, q = r.choice([(3, 7), (2, 9), (4, 11), (5, 8)])
    D = r.choice([9, 12, 15]); dad = 3 * D; bro = D - 6
    assert dad % bro == 0
    E = r.choice([8, 10, 12, 14]); aunt = 4 * E; T = E + aunt
    return Q(None, [(f'Anna is {p} years younger than Brian. Brian is {q} years older than Callum. How much older is Anna than Callum?', f'{q-p} years'),
                    (f"Derek is {D} years old. His dad is three times his age. Derek's brother is 6 years younger than Derek. How many times older is Dad than Derek's brother?", dad // bro),
                    (f'Emily is one quarter of the age of her Aunt Ingrid. Their ages add up to {T}. How old is Emily?', E)])

def y_count(r, v, tag):
    m = v % 2
    if m == 0:
        T, S, H = r.choice([(3, 4, 2), (4, 3, 2), (3, 5, 2), (2, 4, 3)])
        return Q(f'Jess has {T} different tops, {S} different skirts and {H} different hats.', [('How many different outfits can she make from one top and one skirt?', T * S),
                                                                                  ('How many different outfits can she make from one top, one skirt and one hat?', T * S * H),
                                                                                  (f'She wears a top and a skirt but no hat on Monday. On Tuesday she changes both the top and the skirt. How many different Tuesday outfits are there?', (T - 1) * (S - 1))])
    n = r.choice([4, 5, 6])
    return Q(f'A lock uses the digits 1 to {n}. A code is made of two digits.', [('How many two-digit codes are possible if the same digit can be used twice?', n * n),
                                                                       ('How many two-digit codes are possible if the two digits must be different?', n * (n - 1)),
                                                                       ('How many of the codes with two different digits have a first digit larger than the second?', n * (n - 1) // 2)])

def y_machine(r, v, tag):
    m, c = r.choice([(3, 4), (4, 5), (5, 3), (6, 2), (7, 3), (8, 1)]); op = '+' if v % 2 == 0 else '−'
    f = (lambda x: m * x + c) if op == '+' else (lambda x: m * x - c)
    x0 = r.randint(6, 12); x1 = r.randint(13, 25)
    m2, c2 = r.choice([(5, 11), (4, 9), (6, 7), (3, 13), (7, 4), (9, 5)])
    g = lambda x: m2 * x + c2
    return Q(f'A number machine works like this.   Input → × {m} → {op} {c} → Output',
             [(f'What is the output when the input is {x0}?', f(x0)), (f'The output is {f(x1)}. What was the input?', x1),
              (f'A different machine multiplies by a number and then adds a number. Input 3 gives output {g(3)}. Input 5 gives output {g(5)}. What is the output when the input is 4?', g(4))])

def y_digits(r, v, tag):
    dg = r.choice([(3, 8, 1, 6), (5, 0, 7, 2), (4, 9, 2, 7), (6, 1, 8, 3), (2, 6, 0, 9), (7, 3, 5, 1)])
    nums = sorted({int(''.join(map(str, p))) for p in itertools.permutations(dg) if p[0] != 0})
    big = max(nums); small = min(nums)
    for t in (5000, 4000, 6000, 3000, 7000, 2000):
        d_ = sorted((abs(n - t), n) for n in nums)
        if d_[0][0] != d_[1][0]: break
    close = d_[0][1]
    return Q(f'Use each of the digits {", ".join(map(str, dg[:-1]))} and {dg[-1]} once to make a four-digit number.',
             [('Make the largest possible number.', big), ('Make the smallest possible number.', small), (f'Make the number that is closest to {t}.', close)])
