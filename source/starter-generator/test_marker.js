const MK = require('./marker.js'); const D = require('./starter-data.json');
let fails = 0, n = 0, bad = 0;
const good = (p) => {
  const inMulti = p.s.k === 'multi';  // list of inputs that must mark correct
  const s = p.s, out = [];
  const one = (s) => {
    switch (s.k) {
      case 'n': return [s.v, ...(s.alt || [])].concat(p.a && !inMulti ? [p.a] : []);
      case 'f': return s.den ? [p.a] : [p.a, s.v];
      case 't': case 'd': case 'c': case 'list': case 'x': return [p.a];
      case 'ch': return [s.v];
      case 'set': return [s.v.join(' and '), s.v.join(', ')];
      case 'pairs': return s.v.length ? [s.v[0].join(' and '), s.v[s.v.length - 1].join(', ')] : [''];
    }
    return [];
  };
  if (s.k === 'multi') { const per = s.parts.map(one); const k = Math.max(...per.map(x => x.length)); for (let i = 0; i < k; i++) out.push(per.map(x => x[Math.min(i, x.length - 1)])); return out; }
  if (s.k === 'lin') { const m = [...p.a.matchAll(/(\d+) goals and (\d+) penalties/g)]; return m.map(x => [x[1], x[2]]); }
  if (s.k === 'dig') { for (let x = 1; x < 10; x++) for (let y = 1; y < 10; y++) for (let z = 1; z < 10; z++) if (new Set([x, y, z]).size === 3 && s.a * (10 * x + y + z) === s.T) out.push(`${x}${y}${z}`, `${x}${y} + ${z}`); return out; }
  return one(s);
};
const wrong = (p) => {
  const s = p.s, one = (s) => {
    switch (s.k) {
      case 'n': return ['', String(+s.v + 1), String(+s.v * 10 + 7), 'abc'];
      case 'f': return ['', '1/97', String(+MK.value(s.v)[0] / MK.value(s.v)[1] + 0.013)];
      case 't': return ['', '99:99', String(Math.floor(s.v / 60)) + ':' + String((s.v % 60 + 1) % 60).padStart(2, '0')];
      case 'd': return ['', String(s.v + 1) + ' minutes', '0 hours 1 minute'];
      case 'c': return ['', '(0, 0)', `(${s.v[1]}, ${s.v[0] + 1})`];
      case 'list': return ['', s.v.slice().reverse().join(', ') + ',1', s.v.slice(0, -1).join(', ')];
      case 'ch': return ['', 'zzz'];
      case 'set': return ['', 'q and z'];
      case 'pairs': return ['', '1 and 1'];
      case 'x': return ['', 'zzz'];
    }
    return [''];
  };
  if (s.k === 'multi') return s.parts.map((pp, i) => one(pp).map(w => s.parts.map((q, j) => j === i ? w : (good({ s, a: p.a })[0] || [])[j])));
  if (s.k === 'lin') return [[['0', '0'], ['', ''], ['6', '0'], ['1', '1']]];
  if (s.k === 'dig') return [['', '123', '999', '12']];
  return [one(s)];
};
for (const P of D.papers) for (const q of P.qs) for (const [pi, p] of q.parts.entries()) {
  n++;
  const g = good(p);
  if (!g.length || g.some(x => !MK.mark(p.s, x))) { fails++; console.log('GOOD FAIL', P.id, q.n, pi, p.t.slice(0, 60), '|', p.a, '|', JSON.stringify(p.s), JSON.stringify(g.filter(x => !MK.mark(p.s, x)))); }
  const w = p.s.k === 'multi' ? wrong(p).flat() : (p.s.k === 'lin' || p.s.k === 'dig') ? wrong(p)[0] : wrong(p)[0];
  for (const x of w) { if (p.s.k === 'multi' && p.s.parts.some(pp => pp.optional)) continue; if (MK.mark(p.s, x)) { bad++; console.log('WRONG ACCEPTED', P.id, q.n, pi, p.t.slice(0, 50), JSON.stringify(x)); } }
}
console.log('parts', n, 'good-fail', fails, 'wrong-accepted', bad);
