/* more figures: venn, pie, angline, tri, rectfig, dicenet, symgrid, spinner, shapeq, sqpat, tilepat (25 Nov) */
function picMore(kind, rest) {
  const arg = rest.join(" "), esc = s => String(s).replace(/_/g, " ").replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const T = (x, y, s, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.a || "middle"}" font-size="${o.f || 15}" ${o.b ? 'font-weight="700"' : ""} fill="${o.c || "currentColor"}">${esc(s)}</text>`;
  const ink = 'stroke="currentColor" stroke-width="2" fill="none"';
  if (kind === "machine") {   /* machine ×6;−20;in=8;out=? : a number machine with one box per step */
    const parts = arg.split(";"), steps = parts.filter(x => !/^(in|out)=/.test(x)), get = k => (parts.find(x => x.startsWith(k + "=")) || "").slice(k.length + 1);
    const vin = get("in"), vout = get("out"), bw = 74, gap = 26, n = steps.length, ends = 56, W = ends * 2 + n * bw + (n + 1) * gap, y = 34, h = 52;
    const cols = ["#1971c2", "#e8590c", "#2f9e44", "#9c36b5"];
    const arrow = x => `<line x1="${x}" y1="${y + h / 2}" x2="${x + gap - 6}" y2="${y + h / 2}" stroke="currentColor" stroke-width="2.5"/><path d="M${x + gap - 8},${y + h / 2 - 6} L${x + gap},${y + h / 2} L${x + gap - 8},${y + h / 2 + 6} Z" fill="currentColor"/>`;
    const end = (x, lab, v) => `<rect x="${x}" y="${y + 4}" width="${ends}" height="${h - 8}" rx="22" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="${v ? "0" : "5 4"}"/>${T(x + ends / 2, y - 4, lab, { f: 12, b: 1 })}${T(x + ends / 2, y + h / 2 + 7, v || "", { f: 19, b: 1 })}`;
    let x = 0, g = end(x, "IN", vin); x += ends;
    steps.forEach((st, i) => { g += arrow(x); x += gap; g += `<rect x="${x}" y="${y}" width="${bw}" height="${h}" rx="8" fill="${cols[i % 4]}" fill-opacity=".14" stroke="${cols[i % 4]}" stroke-width="2.5"/>` + T(x + bw / 2, y + h / 2 + 8, st, { f: 21, b: 1, c: cols[i % 4] }); x += bw; });
    g += arrow(x); x += gap; g += end(x, "OUT", vout);
    return `<svg viewBox="-2 0 ${W + 4} ${y + h + 12}" width="${Math.min(340, W + 4)}" role="img" aria-label="Number machine: ${esc(steps.join(", then "))}">${g}</svg>`;
  }
  if (kind === "journeys") {   /* journeys Name,start,end,km;Name,start,end,km : two steady journeys on one distance–time graph */
    const js = arg.split(";").map(j => { const [n, t0, t1, d] = j.split(","); const mm = t => { const [h, m] = t.split(":").map(Number); return h * 60 + m; }; return { n, a: mm(t0), b: mm(t1), d: +d }; });
    const a = Math.floor(Math.min(...js.map(j => j.a)) / 60) * 60, b = Math.ceil(Math.max(...js.map(j => j.b)) / 60) * 60, D = Math.max(...js.map(j => j.d));
    const W = 250, H = 160, ox = 52, oy = 190, ystep = [10, 12, 15, 16, 20, 24, 25, 30].find(k => D / k <= 6 && D % k === 0) || D / 4;
    const X = m => ox + (m - a) / (b - a) * W, Y = d => oy - d / D * H, cols = ["#1971c2", "#e8590c"];
    let g = "";
    for (let m = a; m <= b; m += 15) { const x = X(m).toFixed(1); g += `<line x1="${x}" y1="${oy}" x2="${x}" y2="${oy - H}" stroke="currentColor" stroke-opacity="${m % 60 ? .08 : .2}"/>` + (m % 60 ? "" : T(x, oy + 18, String(m / 60).padStart(2, "0") + ":00", { f: 12 })); }
    for (let d = 0; d <= D + 0.001; d += ystep) { const y = Y(d).toFixed(1); g += `<line x1="${ox}" y1="${y}" x2="${ox + W}" y2="${y}" stroke="currentColor" stroke-opacity=".15"/>` + T(ox - 6, +y + 4, String(Math.round(d)), { f: 12, a: "end" }); }
    const lines = js.map((j, i) => `<line x1="${X(j.a)}" y1="${Y(0)}" x2="${X(j.b)}" y2="${Y(j.d)}" stroke="${cols[i]}" stroke-width="3"/>` + T(Math.min(X(j.b) + 4, ox + W - 10), Y(j.d) - 6 - i * 14, j.n, { f: 12, b: 1, a: "end" })).join("");
    return `<svg viewBox="0 0 320 236" width="320" role="img" aria-label="Distance–time graph">${g}<line x1="${ox}" y1="${oy}" x2="${ox + W}" y2="${oy}" ${ink}/><line x1="${ox}" y1="${oy}" x2="${ox}" y2="${oy - H}" ${ink}/>${lines}${T(ox + W / 2, 232, "Time", { f: 12, b: 1 })}${T(12, oy - H / 2, "km", { f: 12, b: 1 })}</svg>`;
  }
  if (kind === "travel") {   /* travel start end distance: a distance–time graph with a steady speed */
    const [t0, t1, dist] = rest, D = +dist, mins = t => { const [h, m] = t.split(":").map(Number); return h * 60 + m; }, a = mins(t0), b = mins(t1);
    const W = 250, H = 160, ox = 52, oy = 190, half = (b - a) / 30, ystep = [10, 20, 24, 25, 30, 40, 50, 60, 100].find(k => D / k <= 6 && D % k === 0) || D / 4;
    const X = m => ox + (m - a) / (b - a) * W, Y = d => oy - d / D * H, hhmm = m => String(Math.floor(m / 60)).padStart(2, "0") + ":" + String(m % 60).padStart(2, "0");
    let g = "";
    for (let i = 0; i <= half; i++) { const m = a + i * 30, x = X(m).toFixed(1); g += `<line x1="${x}" y1="${oy}" x2="${x}" y2="${oy - H}" stroke="currentColor" stroke-opacity=".15"/>` + T(x, oy + 18, hhmm(m), { f: 12 }); }
    for (let d = 0; d <= D + 0.001; d += ystep) { const y = Y(d).toFixed(1); g += `<line x1="${ox}" y1="${y}" x2="${ox + W}" y2="${y}" stroke="currentColor" stroke-opacity=".15"/>` + T(ox - 6, +y + 4, String(Math.round(d)), { f: 12, a: "end" }); }
    return `<svg viewBox="0 0 320 236" width="320" role="img" aria-label="Distance–time graph">${g}<line x1="${ox}" y1="${oy}" x2="${ox + W}" y2="${oy}" ${ink}/><line x1="${ox}" y1="${oy}" x2="${ox}" y2="${oy - H}" ${ink}/>
      <line x1="${X(a)}" y1="${Y(0)}" x2="${X(b)}" y2="${Y(D)}" stroke="#1971c2" stroke-width="3"/>${T(ox + W / 2, 232, "Time", { f: 12, b: 1 })}${T(12, oy - H / 2, "km", { f: 12, b: 1 })}</svg>`;
  }
  if (kind === "lshape") {   /* lshape bottom left top lowerRight unit: an L with right angles, four sides labelled */
    const [b, l, t, r, u] = rest, B = +b, L = +l, Tt = +t, R = +r, k = Math.min(220 / B, 150 / L), ox = 50, oy = 175;
    const X = v => (ox + v * k).toFixed(1), Y = v => (oy - v * k).toFixed(1);
    const pts = [[0, 0], [B, 0], [B, R], [Tt, R], [Tt, L], [0, L]].map(([x, y]) => X(x) + "," + Y(y)).join(" ");
    return `<svg viewBox="0 0 320 210" width="320" role="img" aria-label="L-shape"><polygon points="${pts}" ${ink} fill="#4c6ef5" fill-opacity=".1"/>
      ${T(X(B / 2), +Y(0) + 22, b + " " + u, { b: 1 })}${T(+X(0) - 8, Y(L / 2), l + " " + u, { a: "end", b: 1 })}${T(X(Tt / 2), +Y(L) - 8, t + " " + u, { b: 1 })}${T(+X(B) + 8, Y(R / 2), r + " " + u, { a: "start", b: 1 })}</svg>`;
  }
  if (kind === "venn") {
    const [la, lb, a, both, b, nei] = arg.split(";");
    return `<svg viewBox="0 0 320 190" width="320" role="img" aria-label="Venn diagram"><rect x="4" y="4" width="312" height="182" rx="6" ${ink} stroke-width="1.5"/>
      <circle cx="120" cy="100" r="62" ${ink} fill="#4c6ef5" fill-opacity=".12"/><circle cx="200" cy="100" r="62" ${ink} fill="#f08c00" fill-opacity=".12"/>
      ${T(92, 24, la, { a: "middle", f: 14, b: 1 })}${T(228, 24, lb, { f: 14, b: 1 })}${T(90, 106, a, { f: 20, b: 1 })}${T(160, 106, both, { f: 20, b: 1 })}${T(230, 106, b, { f: 20, b: 1 })}${T(292, 176, nei, { f: 18, b: 1 })}</svg>`;
  }
  if (kind === "pie") {
    const items = arg.split(",").map(x => { const i = x.lastIndexOf("="); return [x.slice(0, i), x.slice(i + 1)]; });
    const cols = ["#4c6ef5", "#f08c00", "#2f9e44", "#e03131", "#ae3ec9", "#1098ad", "#868e96"], cx = 150, cy = 120, r = 82;
    const tot = items.reduce((s, [, d]) => s + (+d || 0), 0), known = items.every(([, d]) => !isNaN(+d));
    let ang = -Math.PI / 2, s = "";
    items.forEach(([l, d], i) => {
      const deg = known ? +d : (360 - items.reduce((q, [, e]) => q + (+e || 0), 0)) / items.filter(([, e]) => isNaN(+e)).length, a2 = ang + deg * Math.PI / 180, big = deg > 180 ? 1 : 0;
      const p = (a, rr) => [cx + rr * Math.cos(a), cy + rr * Math.sin(a)], [x1, y1] = p(ang, r), [x2, y2] = p(a2, r), m = (ang + a2) / 2, [lx, ly] = p(m, r + 20), [dx, dy] = p(m, r * .6);
      s += `<path d="M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${big} 1 ${x2},${y2} Z" fill="${cols[i % cols.length]}" fill-opacity=".28" stroke="currentColor" stroke-width="1.5"/>` +
        T(lx, ly + 5, l, { f: 13, a: Math.cos(m) > .25 ? "start" : Math.cos(m) < -.25 ? "end" : "middle" }) + T(dx, dy + 5, isNaN(+d) ? "?" : d + "°", { f: 14, b: 1 });
      ang = a2;
    });
    return `<svg viewBox="0 0 300 240" width="300" role="img" aria-label="Pie chart">${s}</svg>`;
  }
  if (kind === "angline") {
    /* angles on a straight line: each angle is a coloured sector with its label in the same colour (bigger and clearer, owner review 25 Nov) */
    const labs = arg.split(","), deg = labs.some(l => /°/.test(l)), known = labs.filter(l => /°/.test(l)).reduce((a, l) => a + parseInt(l), 0), unk = labs.filter(l => !/°/.test(l)).length;
    const ks = labs.map(l => deg ? (/°/.test(l) ? parseInt(l) : (180 - known) / Math.max(1, unk)) : (parseInt(l) || 1)), tot = ks.reduce((a, b) => a + b, 0), ox = 170, oy = 150, R = 135;
    const cols = ["#e03131", "#1971c2", "#2f9e44", "#e8590c", "#9c36b5"];
    const pt = (a, rr) => [ox - rr * Math.cos(a), oy - rr * Math.sin(a)];
    let acc = 0, sec = "", rays = "", txt = "";
    labs.forEach((l, i) => {
      const a0 = acc / tot * Math.PI, a1 = (acc + ks[i]) / tot * Math.PI, m = (a0 + a1) / 2, r0 = 44 + 6 * (i % 2);
      const [x0, y0] = pt(a0, r0), [x1, y1] = pt(a1, r0);
      sec += `<path d="M${ox},${oy} L${x0},${y0} A${r0},${r0} 0 0 1 ${x1},${y1} Z" fill="${cols[i % 5]}" fill-opacity=".2" stroke="${cols[i % 5]}" stroke-width="2.5"/>`;
      if (i > 0) { const [x, y] = pt(a0, R); rays += `<line x1="${ox}" y1="${oy}" x2="${x}" y2="${y}" stroke="currentColor" stroke-width="2.5"/>`; }
      const [lx, ly] = pt(m, r0 + 26); txt += T(lx, ly + 7, l, { f: 20, b: 1, c: cols[i % 5] });
      acc += ks[i];
    });
    return `<svg viewBox="0 0 340 168" width="340" role="img" aria-label="Angles on a straight line: ${esc(labs.join(", "))}">${sec}<line x1="16" y1="${oy}" x2="324" y2="${oy}" stroke="currentColor" stroke-width="2.5"/>${rays}<circle cx="${ox}" cy="${oy}" r="4" fill="currentColor"/>${txt}</svg>`;
  }
  if (kind === "tri") {
    const [a, b, c] = arg.split(","), P = [[30, 150], [270, 150], [130, 26]], cols = ["#e03131", "#1971c2", "#2f9e44"];
    const arc = (i, r0) => { const [x, y] = P[i], [ux, uy] = P[(i + 1) % 3], [vx, vy] = P[(i + 2) % 3];
      const n = (dx, dy) => { const L = Math.hypot(dx, dy); return [dx / L, dy / L]; }, [p1, q1] = n(ux - x, uy - y), [p2, q2] = n(vx - x, vy - y);
      const sw = (p1 * q2 - q1 * p2) > 0 ? 1 : 0, [mx, my] = n(p1 + p2, q1 + q2);
      return { d: `M${x},${y} L${x + r0 * p1},${y + r0 * q1} A${r0},${r0} 0 0 ${sw} ${x + r0 * p2},${y + r0 * q2} Z`, lx: x + (r0 + 22) * mx, ly: y + (r0 + 22) * my }; };
    let g = `<path d="M${P[0]} L${P[1]} L${P[2]} Z" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linejoin="round"/>`;
    [a, b, c].forEach((l, i) => { const A = arc(i, 34); g += `<path d="${A.d}" fill="${cols[i]}" fill-opacity=".2" stroke="${cols[i]}" stroke-width="2.5"/>` + T(A.lx, A.ly + 7, l, { f: 18, b: 1, c: cols[i] }); });
    return `<svg viewBox="0 0 300 172" width="300" role="img" aria-label="Triangle with angles ${esc(a)}, ${esc(b)} and ${esc(c)}">${g}</svg>`;
  }
  if (kind === "sqpat") {
    /* sqpat dots 1,2,3  or  sqpat tiles 2,3,4 : square patterns, pattern n is size × size */
    const style = rest[0], sizes = (rest[1] || "1,2,3").split(",").map(Number), u = 18;
    let x = 8, g = "", H = Math.max(...sizes) * u + 34;
    sizes.forEach((k, i) => {
      const pad = Math.max(0, (64 - k * u) / 2); x += pad;
      for (let r = 0; r < k; r++) for (let c = 0; c < k; c++) g += style === "dots" ? `<circle cx="${x + c * u + u / 2}" cy="${8 + r * u + u / 2}" r="5" fill="#1971c2"/>` : `<rect x="${x + c * u + 1}" y="${8 + r * u + 1}" width="${u - 2}" height="${u - 2}" rx="2" fill="#4c6ef5" fill-opacity=".7"/>`;
      g += T(x + k * u / 2, H - 6, "Pattern " + (i + 1), { f: 13 }); x += k * u + pad + 20;
    });
    return `<svg viewBox="0 0 ${x} ${H}" width="${Math.min(340, x * 1.1)}" role="img" aria-label="Square patterns ${sizes.join(", ")}">${g}</svg>`;
  }
  if (kind === "tilepat") {
    /* tilepat a b : pattern n has a tiles in the first column and b more tiles for each step (patterns 1 to 3) */
    const a = +rest[0], b = +rest[1], u = 16, rows = Math.max(a, b);
    let x = 8, g = "", H = rows * u + 34;
    for (let n = 1; n <= 3; n++) {
      const pad = Math.max(0, (64 - (n + 1) * u) / 2); x += pad;
      const col = (cx, k, c) => { for (let r = 0; r < k; r++) g += `<rect x="${cx + 1}" y="${8 + (rows - 1 - r) * u + 1}" width="${u - 2}" height="${u - 2}" rx="2" fill="${c}" fill-opacity=".75"/>`; };
      col(x, a, "#f08c00"); for (let j = 1; j <= n; j++) col(x + j * u, b, "#4c6ef5");
      g += T(x + (n + 1) * u / 2, H - 6, "Pattern " + n, { f: 13 }); x += (n + 1) * u + pad + 20;
    }
    return `<svg viewBox="0 0 ${x} ${H}" width="${Math.min(340, x * 1.1)}" role="img" aria-label="Growing tile pattern">${g}</svg>`;
  }
  if (kind === "rectfig") {
    const [L, W, u] = [+rest[0], +rest[1], rest[2] || "cm"], mx = 210, k = mx / Math.max(L, W * 1.6), w = Math.max(70, Math.min(mx, L * k)), h = Math.max(46, Math.min(130, W * k * 1.6 > 130 ? 130 : W * k * 1.6)), x0 = 50, y0 = 30;
    return `<svg viewBox="0 0 320 ${y0 + h + 40}" width="320" role="img" aria-label="Rectangle ${L} ${u} by ${W} ${u}"><rect x="${x0}" y="${y0}" width="${w}" height="${h}" ${ink}/>
      ${T(x0 + w / 2, y0 - 10, L + " " + u, { f: 15, b: 1 })}${T(x0 - 8, y0 + h / 2 + 5, W + " " + u, { f: 15, b: 1, a: "end" })}</svg>`;
  }
  if (kind === "dicenet") {
    const cells = arg.split(";").map(c => { const [xy, d] = c.split("="); const [x, y] = xy.split(",").map(Number); return [x, y, +d]; });
    const S = 54, W = (Math.max(...cells.map(c => c[0])) + 1) * S + 8, H = (Math.max(...cells.map(c => c[1])) + 1) * S + 8;
    const P = { 1: [[.5, .5]], 2: [[.25, .25], [.75, .75]], 3: [[.25, .25], [.5, .5], [.75, .75]], 4: [[.25, .25], [.75, .25], [.25, .75], [.75, .75]], 5: [[.25, .25], [.75, .25], [.5, .5], [.25, .75], [.75, .75]], 6: [[.25, .22], [.75, .22], [.25, .5], [.75, .5], [.25, .78], [.75, .78]] };
    return `<svg viewBox="0 0 ${W} ${H}" width="${Math.min(320, W * 1.2)}" role="img" aria-label="Net of a dice">${cells.map(([x, y, d]) => `<rect x="${4 + x * S}" y="${4 + y * S}" width="${S}" height="${S}" ${ink} fill="var(--surface, #fff)"/>` + P[d].map(([a, b]) => `<circle cx="${4 + x * S + a * S}" cy="${4 + y * S + b * S}" r="5.5" fill="currentColor"/>`).join("")).join("")}</svg>`;
  }
  if (kind === "symgrid") {
    const cols = +rest[0], rows = +rest[1], ax = rest[2], on = new Set((rest[3] || "").split(";")), S = 30, W = cols * S + 8, H = rows * S + 8;
    let g = "";
    for (let y = 0; y < rows; y++) for (let x = 0; x < cols; x++) g += `<rect x="${4 + x * S}" y="${4 + y * S}" width="${S}" height="${S}" stroke="currentColor" stroke-width="1" fill="${on.has(x + "," + y) ? "#4c6ef5" : "none"}" fill-opacity="${on.has(x + "," + y) ? .75 : 0}"/>`;
    const line = ax === "v" ? `<line x1="${4 + cols * S / 2}" x2="${4 + cols * S / 2}" y1="0" y2="${H}" stroke="#e03131" stroke-width="3" stroke-dasharray="7 5"/>` : `<line y1="${4 + rows * S / 2}" y2="${4 + rows * S / 2}" x1="0" x2="${W}" stroke="#e03131" stroke-width="3" stroke-dasharray="7 5"/>`;
    return `<svg viewBox="0 0 ${W} ${H}" width="${Math.min(320, W * 1.1)}" role="img" aria-label="Grid with shaded squares and a dashed mirror line">${g}${line}</svg>`;
  }
  if (kind === "spinner") {
    const ns = arg.split(","), k = ns.length, cx = 110, cy = 110, R = 92, cols = ["#4c6ef5", "#f08c00", "#2f9e44", "#e03131", "#ae3ec9", "#1098ad", "#868e96", "#f59f00"];
    let g = "";
    ns.forEach((n, i) => { const a0 = 2 * Math.PI * i / k - Math.PI / 2, a1 = 2 * Math.PI * (i + 1) / k - Math.PI / 2, am = (a0 + a1) / 2;
      g += `<path d="M${cx},${cy} L${cx + R * Math.cos(a0)},${cy + R * Math.sin(a0)} A${R},${R} 0 0 1 ${cx + R * Math.cos(a1)},${cy + R * Math.sin(a1)} Z" fill="${cols[i % 8]}" fill-opacity=".22" stroke="currentColor" stroke-width="2"/>` + T(cx + R * .62 * Math.cos(am), cy + R * .62 * Math.sin(am) + 7, n, { f: 20, b: 1 }); });
    return `<svg viewBox="0 0 220 220" width="220" role="img" aria-label="Spinner with ${k} equal parts: ${ns.join(", ")}">${g}<circle cx="${cx}" cy="${cy}" r="6" fill="currentColor"/><line x1="${cx}" y1="${cy}" x2="${cx + 40}" y2="${cy - 40}" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>`;
  }
  if (kind === "shapeq") {
    /* shapeq tri+tri+sq=20;sq-cir=3;tri×cir=?   the same shape always has the same value */
    const C = { tri: "#f08c00", sq: "#4c6ef5", cir: "#e03131", star: "#f5b700", hex: "#2f9e44", heart: "#d6336c" };
    const icon = (s, x, y) => {
      const f = `fill="${C[s]}" stroke="currentColor" stroke-width="1.5"`;
      if (s === "tri") return `<polygon points="${x + 18},${y + 4} ${x + 34},${y + 34} ${x + 2},${y + 34}" ${f}/>`;
      if (s === "sq") return `<rect x="${x + 4}" y="${y + 5}" width="28" height="28" rx="3" ${f}/>`;
      if (s === "cir") return `<circle cx="${x + 18}" cy="${y + 19}" r="15" ${f}/>`;
      if (s === "hex") return `<polygon points="${x + 10},${y + 5} ${x + 26},${y + 5} ${x + 34},${y + 19} ${x + 26},${y + 33} ${x + 10},${y + 33} ${x + 2},${y + 19}" ${f}/>`;
      if (s === "heart") return `<path d="M${x + 18},${y + 34} C${x - 6},${y + 18} ${x + 6},${y} ${x + 18},${y + 12} C${x + 30},${y} ${x + 42},${y + 18} ${x + 18},${y + 34} Z" ${f}/>`;
      return `<polygon points="${x + 18},${y + 2} ${x + 23},${y + 14} ${x + 35},${y + 14} ${x + 25},${y + 22} ${x + 29},${y + 35} ${x + 18},${y + 27} ${x + 7},${y + 35} ${x + 11},${y + 22} ${x + 1},${y + 14} ${x + 13},${y + 14}" ${f}/>`;
    };
    const rows = arg.split(";"), h = 46; let g = "", w = 0;
    rows.forEach((row, i) => {
      const [lhs, rhs] = row.split("="), y = i * h + 4, toks = lhs.split(/([+−×-])/); let x = 4;
      toks.forEach(t => { if (!t) return; if (/^[+−×-]$/.test(t)) { g += T(x + 10, y + 26, t === "-" ? "−" : t, { f: 22, b: 1 }); x += 22; } else { g += icon(t, x, y); x += 38; } });
      g += T(x + 10, y + 26, "=", { f: 22, b: 1 }) + T(x + 26, y + 26, rhs, { f: 22, b: 1, a: "start" });
      w = Math.max(w, x + 30 + 14 * rhs.length);
    });
    return `<svg viewBox="0 0 ${w} ${rows.length * h + 6}" width="${Math.min(340, w * 1.15)}" role="img" aria-label="Shape puzzle: each shape stands for a number">${g}</svg>`;
  }
  return "";
}
