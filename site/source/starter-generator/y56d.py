from common import *
from y56a import isprime
from y56b import NAMES

def t_count(r, v, tag):
    if v % 2 == 0:
        n = r.choice([9, 9, 10]); L = r.choice([3, 4, 5, 6]); digs = '1 to 9' if n == 9 else '0 to 9'
        letters = ', '.join('ABCDEF'[:L])
        return Q(f'A security system uses a keypad with the digits {digs} and the letters {letters}. Codes are made by pressing keys one after the other.',
                 [('How many two-digit codes are possible if the same digit can be used twice?', n * n), ('How many two-digit codes are possible if the same digit cannot be used twice?', n * (n - 1)),
                  ('How many codes are possible if a code is one letter followed by one digit?', L * n), ('How many codes are possible if a code is one letter followed by two different digits?', L * n * (n - 1))])
    S = r.choice([4, 5, 6]); M = r.choice([3, 4, 5]); D = r.choice([2, 3, 4])
    return Q(f'A restaurant menu has {S} different side dishes, {M} different main courses and {D} different desserts.',
             [('A guest chooses one side dish and one main course. How many different meals are possible?', S * M),
              ('A guest chooses two different side dishes and one main course. How many different meals are possible?', S * (S - 1) // 2 * M),
              ('A guest chooses one side dish, one main course and one dessert. How many different meals are possible?', S * M * D)])

def t_digits(r, v, tag):
    while True:
        a = r.choice([3, 4, 5, 6, 7, 8, 9]); x, y, z = r.sample(range(1, 10), 3); T = a * (10 * x + y + z)
        sols = [(p, q, s) for p in range(1, 10) for q in range(1, 10) for s in range(1, 10) if len({p, q, s}) == 3 and a * (10 * p + q + s) == T]
        if 2 <= len(sols) <= 6 and T > 100: break
    ex = sols[0]
    return Q('In this question each box is filled with a single digit from 1 to 9. The three boxes must contain three different digits.',
             [(f'Fill in the boxes to show one way of completing the calculation correctly.    {a} × (□□ + □) = {T}', f'e.g. {a} × ({ex[0]}{ex[1]} + {ex[2]}) = {T}'),
              (f'In how many different ways can the calculation {a} × (□□ + □) = {T} be completed correctly?', len(sols))])

def t_cost(r, v, tag):
    if v % 2 == 0:
        c = r.randrange(180, 330, 10); k = r.randrange(200, 360, 10); s = r.randrange(250, 460, 10)
        T1 = c + k + s; T2 = c + 2 * k + s; T3 = 3 * c + k
        assert T2 - T1 == k and (T3 - k) // 3 == c
        return Q('Milly runs a café. One customer orders a coffee, a slice of cake and a sandwich, and pays ' + gbp(T1) + '. The next customer orders a coffee, two slices of cake and a sandwich, and pays ' + gbp(T2) + '. A third customer orders three coffees and a slice of cake, and pays ' + gbp(T3) + '.',
                 [('How much does one slice of cake cost?', gbp(k)), ('How much does one cup of coffee cost?', gbp(c)), ('How much does one sandwich cost?', gbp(s))])
    while True:
        o = r.randrange(25, 60, 5); a = r.choice([20, 24, 30, 40]); p = r.choice([25, 50])
        extra = F(5 * a * p, 100)
        if extra.denominator == 1: break
    T1 = 3 * o + 5 * a; T2 = T1 + int(extra)
    return Q(f'At the supermarket, three oranges and five apples cost {gbp(T1)}. At the corner shop, oranges cost the same as at the supermarket but apples are {p}% more expensive. At the corner shop, three oranges and five apples cost {gbp(T2)}.',
             [('How much more do five apples cost at the corner shop than at the supermarket?', gbp(extra)), ('What is the price of one apple at the supermarket?', gbp(a)), ('What is the price of one orange at the supermarket?', gbp(o))])

def t_relations(r, v, tag):
    m = v % 3
    if m == 0:
        mu, nu = r.choice([(2, 3), (3, 2), (2, 2), (3, 3), (2, 4)]); C = r.randint(3, 12); B = nu * C; A = mu * B; T = A + B + C
        w = lambda k: {2: 'double', 3: 'three times', 4: 'four times'}[k]
        return Q(f'A, B and C are whole numbers. A is {w(mu)} B, and B is {w(nu)} C. A + B + C = {T}.', [('Find C.', C), ('Find A.', A), ('What is the difference between A and B?', A - B)])
    if m == 1:
        k = r.randint(2, 6); A = 2 * k; B = 2 * A; C = F(A, 2); T = A + B + C
        return Q(f'A, B and C are numbers. B = 2A and 2C = A. A + B + C = {frac(T)}.', [('Find A.', A), ('Find C.', frac(C)), ('Find B.', B)])
    k = r.randint(2, 5)
    for B in (3, 7, 12): 
        A = B + k; C = k * B; D = B * B
        assert k * A - C == k * k and F(C, A - k) == k and A * B - C - D == 0
    intro = f'A, B, C and D are positive numbers. You are not told their values, but you are told that A = B + {k}, C = {k}B and D = B × B.'
    return Q(intro, [(f'Find the value of {k}A − C.', k * k), (f'Find the value of C ÷ (A − {k}).', k), ('Find the value of (A × B) − C − D.', 0)])

def t_puzzle(r, v, tag):
    if v % 2 == 0:
        lo = r.choice([60, 80, 100, 120, 140])
        tw = next(p for p in range(lo + 1, 400) if isprime(p) and isprime(p + 2))
        d, lim = r.choice([(12, 40), (14, 40), (18, 50), (20, 40), (22, 40), (24, 50), (30, 50)])
        prs = [(p, p + d) for p in range(2, lim) if isprime(p) and p + d < lim and isprime(p + d)]
        assert prs
        dd = r.choice([25, 21, 19, 27, 15, 13])
        poss = isprime(dd + 2)
        return Q('Some prime numbers come in pairs with a difference of 2, for example 5 and 7, or 11 and 13.',
                 [(f'What is the lowest such pair where both numbers are greater than {lo}?', f'{tw} and {tw+2}'),
                  (f'Find a pair of prime numbers with a difference of {d}, where both numbers are less than {lim}.', ' or '.join(f'{p} and {q}' for p, q in prs)),
                  (f'A mathematician says it is impossible to find two prime numbers that are {dd} apart. Is this true or false?', 'False (2 and ' + str(dd + 2) + ')' if poss else 'True (one number would have to be 2, and ' + str(dd + 2) + ' is not prime)')])
    a, b = r.choice([(7, 3), (7, 4), (5, 4), (9, 4), (8, 3), (7, 5)])
    ach = lambda n: [(x, (n - a * x) // b) for x in range(n // a + 1) if (n - a * x) % b == 0]
    imp = [n for n in range(1, 60) if not ach(n)]
    show = imp[:5]; nxt = imp[5]
    two = next(n for n in range(1, 200) if len(ach(n)) >= 2)
    N = 2 * a * b
    others = [p for p in ach(N) if p[0] not in (0, N // a)]
    assert others
    return Q(f'In a game, a goal from open play scores {a} points and a penalty scores {b} points. A player cannot score exactly {", ".join(map(str,show[:-1]))} or {show[-1]} points.',
             [('What is the next lowest score that is impossible?', nxt), ('What is the lowest score that can be achieved in two different ways?', two),
              (f'A score of {N} can be achieved with {N//a} goals and no penalties, or with {N//b} penalties and no goals. Find another way of scoring {N} points.', ' or '.join(f'{g} goals and {p} penalties' for g, p in others))])

def t_ages(r, v, tag):
    while True:
        y1 = r.choice([1928, 1930, 1932, 1934, 1936]); y2 = y1 + r.choice([28, 30, 32, 33, 34, 36])
        t = r.randint(1990, 2012); S = (t - y1) + (t - y2)
        sq = [yr for yr in range(y2 + 1, 2040) if (yr - y1) ** .5 % 1 == 0 and (yr - y2) ** .5 % 1 == 0]
        half = 2 * y2 - y1
        if sq and y2 < half < 2030: break
    mn, dn = r.sample(['Mrs Patel', 'Mrs Okoro', 'Mrs Evans', 'Mrs Clarke'], 1)[0], r.choice(['Anya', 'Beth', 'Chloe', 'Dani'])
    return Q(f'{mn} was born on 1st January {y1} and her daughter {dn} was born on 1st January {y2}. For example, in {y2+10} {mn} was {y2+10-y1} and {dn} was 10.',
             [(f'In which year was {dn} exactly half as old as her mother?', half), (f'In which year did their two ages add up to {S}?', t), ('Find a year when both of their ages were square numbers.', ' or '.join(map(str, sq)))])
