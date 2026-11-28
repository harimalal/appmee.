/* ===== reel n°10 — Nouvelle charte, tout le site d'un coup (captures RÉELLES : avant = commit df3b980 du 02/05/2026, après = cffda46 du 13/05/2026, même contenu ; maquette réelle du dépôt) ===== */
const SHADOW = '0 24px 60px rgba(0,0,0,.45)';
const pill = (root, text, x, y, w, h, css = '') => { const e = mk(root, 'abs tx', text); place(e, x, y, w, h); e.style.cssText += ';display:flex;align-items:center;justify-content:center;border-radius:999px;font:900 46px/1 var(--font);letter-spacing:-.02em;white-space:nowrap;' + css; return e; };
const thumb = (parent, src, x, y, w, h, pos = '50% 0%', rad = 18) => { const d = mk(parent, 'abs', null); d.dataset.deco = ''; place(d, x, y, w, h); d.style.cssText += `;overflow:hidden;border-radius:${rad}px;box-shadow:${SHADOW};background:#fff`; const i = img(d, src); i.style.cssText += `;display:block;width:100%;height:100%;object-fit:cover;object-position:${pos}`; return d; };
const PH = { 'avant-accueil': 1034, 'apres-accueil': 2246, 'avant-blog': 1034, 'apres-blog': 1369, 'avant-article': 2278, 'apres-article': 2278, 'avant-rubrique': 1019, 'apres-rubrique': 701, 'avant-manifeste': 1445, 'apres-manifeste': 1450, 'avant-comparatif': 2278, 'apres-comparatif': 2278 };
const PG = (t, k) => `assets/pg/${t}-${k}.jpg`;

/* une vraie page avant/après dans un cadre : balayage (w de 0 à 1) et défilement (sy en px affichés) */
function pgBA(parent, key, x, y, w, h, rad = 26) {
  const d = mk(parent, 'abs', null); d.dataset.deco = ''; place(d, x, y, w, h);
  d.style.cssText += `;overflow:hidden;border-radius:${rad}px;box-shadow:${SHADOW};background:#fff;outline:4px solid rgba(255,255,255,.14);outline-offset:-2px`;
  const L = t => { const i = img(d, PG(t, key)); i.style.cssText += ';position:absolute;left:0;top:0;width:100%;height:auto'; return i; };
  let k = key, A = L('avant'), B = L('apres');
  const bar = mk(d, 'abs', null); place(bar, 0, 0, 8, h); bar.style.cssText += ';background:#fff;box-shadow:0 0 30px rgba(255,255,255,.9);z-index:3';
  return { el: d, set(wp, sy = 0) {
    const s = w / 1080, mA = Math.max(0, PH['avant-' + k] * s - h), mB = Math.max(0, PH['apres-' + k] * s - h);
    A.style.transform = `translateY(${-Math.min(sy, mA)}px)`; B.style.transform = `translateY(${-Math.min(sy, mB)}px)`;
    B.style.clipPath = `inset(0 ${(1 - wp) * 100}% 0 0)`; bar.style.opacity = wp > .001 && wp < .999 ? 1 : 0; bar.style.transform = `translateX(${wp * w - 4}px)`;
  }, key(nk) { if (nk !== k) { k = nk; A.src = PG('avant', k); B.src = PG('apres', k); PEND.push(A.decode().catch(() => {}), B.decode().catch(() => {})); } } };
}
const PEND = []; window.__wait = () => Promise.all(PEND.splice(0));

function claude3D(root, x, y, size) {
  const wrap = mk(root, 'abs', null); wrap.dataset.deco = ''; place(wrap, x - size / 2, y - size / 2, size, size); wrap.style.perspective = '900px';
  const body = mk(wrap, 'abs', null); place(body, 0, 0, size, size); body.style.transformStyle = 'preserve-3d';
  for (let k = 7; k >= 0; k--) { const i = img(body, 'assets/claude.png'); i.style.cssText += `;position:absolute;left:0;top:0;width:${size}px;height:${size}px;transform:translateZ(${-k * 3.2}px);filter:${k ? `brightness(${.55 + .03 * (7 - k)})` : 'drop-shadow(0 18px 22px rgba(120,50,20,.35))'}`; }
  return (t, p, extra = {}) => { put(wrap, Object.assign({ s: .4 + .6 * eoBack(p), op: cl(p * 3) }, extra)); body.style.transform = `rotateY(${Math.sin(t * 1.3) * 20}deg) rotateX(${10 + Math.sin(t * .9) * 6}deg) rotateZ(${Math.sin(t * .7) * 4}deg)`; };
}
const dot = (root, col, x, y, d, border = '') => { const e = mk(root, 'abs', null); e.dataset.deco = ''; place(e, x, y, d, d); e.style.cssText += `;border-radius:50%;background:${col};box-shadow:0 18px 40px rgba(0,0,0,.4);${border}`; return e; };

/* ----- 1 — hook : l'accueil bascule d'une charte à l'autre ----- */
scene('hook', ['Tout le site, d’un coup'], (root, m) => {
  const s1 = S(m, 's1'), D = dv(s1), tW = s1.start + D * .5;
  const lab = swap(root, 'lbl', [{ html: 'Tout le site, d’un coup', a: s1.start + .05 }], 84, 304, 846, 150);
  const F = pgBA(root, 'accueil', 60, 580, 960, 900, 30);
  scrim(root, 'mid');
  ev('thump', m.start + .2, { amp: .7 }); ev('whoosh', tW, { dur: .6 }); ev('ding', tW + .65, { f: 1318 });
  return t => {
    lab(t); const p = P(t, m.start + .05, .5);
    put(F.el, { y: (1 - eoBack(p)) * 260 + Math.sin(t * 1.2) * 5, s: .92 + .08 * eoBack(p), op: cl(p * 3) });
    F.set(io(P(t, tW, .7)), Math.max(0, t - tW - .7) * 60);
  };
});

/* ----- 2 — avant : crème et orange, trop proche de Claude ----- */
scene('avant', ['Avant : crème et orange', 'Trop proche de Claude'], (root, m) => {
  const s2 = S(m, 's2'), D = dv(s2), tC = s2.start + D * .55;
  const lab = swap(root, 'lbl', [{ html: 'Avant : crème et orange', a: s2.start + .05 }, { html: 'Trop proche de Claude', a: tC }], 84, 304, 846, 150);
  const pg = thumb(root, PG('avant', 'accueil'), 60, 590, 620, 900, '50% 0%', 28);
  const c1 = dot(root, '#faf8f5', 760, 640, 200, 'border:6px solid rgba(255,255,255,.25)'), c2 = dot(root, '#c8522a', 760, 880, 200);
  const logo = claude3D(root, 860, 1310, 240);
  scrim(root, 'mid');
  ev('whoosh', m.start + .2, { dur: .4 }); ev('pop', s2.start + D * .2); ev('pop', s2.start + D * .32); ev('pop', tC + .1); ev('ding', tC + .25, { f: 1174 });
  return t => {
    lab(t); const p = P(t, m.start + .05, .5); put(pg, { y: (1 - eoBack(p)) * 300 + Math.sin(t * 1.3) * 5, r: -2 * p, op: cl(p * 3) });
    [c1, c2].forEach((c, i) => { const q = P(t, s2.start + D * (.2 + .12 * i), .45); put(c, { y: Math.sin(t * 2 + i) * 6 * q, s: .3 + .7 * eoBack(q), op: cl(q * 3) }); });
    logo(t, P(t, tC, .5), { op: cl(P(t, tC, .5) * 3), y: Math.sin(t * 1.4) * 8 });
  };
});

/* ----- 3 — d'habitude : long, et ça casse des pages ----- */
scene('dur', ['D’habitude : long et risqué'], (root, m) => {
  const s3 = S(m, 's3'), D = dv(s3), tK = s3.start + D * .62;
  const lab = swap(root, 'lbl', [{ html: 'D’habitude : long et risqué', a: s3.start + .05 }], 84, 304, 846, 150);
  const K = ['accueil', 'blog', 'article', 'manifeste'];
  const th = K.map((k, i) => thumb(root, PG('avant', k), 84 + (i % 2) * 436, 600 + Math.floor(i / 2) * 470, 410, 440, '50% 0%', 22));
  const bad = th.map(e => { const b = mk(e, 'abs', ICON.x ? ICON.x() : '<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M14 14l20 20M34 14L14 34" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>'); b.dataset.deco = ''; place(b, 300, 20, 90, 90); b.style.cssText += ';border-radius:50%;background:var(--red);padding:14px;opacity:0'; return b; });
  const clock = mk(root, 'abs', '<svg viewBox="0 0 48 48" width="100%" height="100%"><circle cx="24" cy="24" r="19" fill="#fff" stroke="#fff" stroke-width="2"/><path id="hand" d="M24 24V11" stroke="#0F1020" stroke-width="4" stroke-linecap="round"/><path d="M24 24l8 5" stroke="#0F1020" stroke-width="4" stroke-linecap="round"/></svg>'); clock.dataset.deco = ''; place(clock, 440, 1020, 200, 200);
  const hand = clock.querySelector('#hand');
  scrim(root, 'mid');
  ev('whoosh', m.start + .2, { dur: .4 }); for (let i = 0; i < 6; i++) ev('tick', s3.start + .3 + i * .3, { f: 1400 }); [0, 1, 2, 3].forEach(i => ev('pop', tK + i * .12)); ev('thump', tK + .1, { amp: .8 });
  return t => {
    lab(t);
    th.forEach((e, i) => { const p = P(t, m.start + .05 + i * .08, .45), sh = P(t, tK + i * .12, .1) * (1 - P(t, tK + .6 + i * .12, .4)); put(e, { x: Math.sin(t * 57 + i) * 10 * sh, y: (1 - eoBack(p)) * 200, r: Math.sin(t * 41 + i) * 2 * sh, op: cl(p * 3) });
      e.style.outline = t >= tK + i * .12 ? '6px solid var(--red)' : 'none'; put(bad[i], { s: .3 + .7 * eoBack(P(t, tK + i * .12, .35)), op: cl(P(t, tK + i * .12, .2) * 3) }); });
    const q = P(t, s3.start + .1, .4); put(clock, { s: .4 + .6 * eoBack(q), op: cl(q * 3) * (1 - P(t, tK, .3)) }); hand.setAttribute('transform', `rotate(${t * 240} 24 24)`);
  };
});

/* ----- 4 — cinq ou six maquettes, une seule donnée à Claude ----- */
scene('maquettes', ['Cinq ou six maquettes', 'générées par GPT Image', 'Une seule, donnée à Claude'], (root, m) => {
  const s4 = S(m, 's4'), s5 = S(m, 's5'), D5 = dv(s5), tC = s5.start + D5 * .78;
  const lab = swap(root, 'lbl', [{ html: 'Cinq ou six maquettes', a: s4.start + .05 }, { html: 'Une seule, donnée à Claude', a: s5.start }], 84, 304, 846, 150);
  const sub = swap(root, 'sublbl', [{ html: 'générées par GPT Image', a: s4.start + dv(s4) * .55, b: s5.start - .3 }], 84, 466, 846, 40);
  const W = 296, H = 420, G = 24, X0 = (1080 - 3 * W - 2 * G) / 2, Y0 = 600, REAL = 4;
  const slots = Array.from({ length: 6 }, (_, i) => { const x = X0 + (i % 3) * (W + G), y = Y0 + Math.floor(i / 3) * (H + G);
    if (i === REAL) { const e = thumb(root, 'assets/maquette-1.jpg', x, y, W, H, '50% 0%', 20); e.style.zIndex = 5; return { e, x, y }; }
    const e = mk(root, 'abs', '<i></i><i></i><i></i><i></i><i></i>'); e.dataset.deco = ''; place(e, x, y, W, H);
    e.style.cssText += `;border-radius:20px;background:linear-gradient(160deg,rgba(255,255,255,.16),rgba(255,255,255,.06));border:3px solid rgba(255,255,255,.18);padding:30px 24px;display:flex;flex-direction:column;gap:18px;backdrop-filter:blur(2px)`;
    [...e.children].forEach((b, k) => b.style.cssText = `display:block;height:${k ? 18 : 60}px;border-radius:10px;background:rgba(255,255,255,${k ? .18 : .26});width:${[90, 100, 80, 94, 60][k]}%`); return { e, x, y }; });
  const logo = claude3D(root, 540, 1420, 230);
  scrim(root, 'mid');
  ev('whoosh', m.start + .2, { dur: .4 }); slots.forEach((_, i) => ev('pop', s4.start + .2 + i * .12)); ev('whoosh', s5.start + .2, { dur: .5, up: true }); ev('pop', tC); ev('ding', tC + .2, { f: 1318 });
  return t => {
    lab(t); sub(t);
    const pick = io(P(t, s5.start + .15, .6)), gone = io(P(t, tC + .1, .6));
    slots.forEach(({ e, x, y }, i) => { const p = P(t, s4.start + .2 + i * .12, .45);
      if (i === REAL) { const tx = 540 - (x + W / 2), ty = 980 - (y + H / 2); put(e, { x: tx * pick, y: ty * pick - gone * 160 + (1 - eoBack(p)) * 160, s: (1 + 1.1 * pick) * (1 - .55 * gone), r: Math.sin(t * 1.2) * 1.2 * pick, op: cl(p * 3) * (1 - gone * .9) }); }
      else put(e, { y: (1 - eoBack(p)) * 160 + Math.sin(t * 1.5 + i) * 5, s: 1 - .2 * pick, op: cl(p * 3) * (1 - pick) }); });
    logo(t, P(t, tC - .1, .5), { op: cl(P(t, tC - .1, .5) * 3), y: Math.sin(t * 1.3) * 8 - gone * 60 });
  };
});

/* ----- 5 — Claude fait tout le reste : chaque type de page bascule ----- */
scene('pages', ['Claude fait tout le reste', 'La page d’accueil', 'Le blog', 'Les articles', 'Les rubriques'], (root, m) => {
  const s6 = S(m, 's6'), D = dv(s6), TS = [.4, .6, .75, .88].map(f => s6.start + D * f);
  const lab = swap(root, 'lbl', [{ html: 'Claude fait tout le reste', a: s6.start + .05 }, { html: 'La page d’accueil', a: TS[0] }, { html: 'Le blog', a: TS[1] }, { html: 'Les articles', a: TS[2] }, { html: 'Les rubriques', a: TS[3] }], 84, 304, 846, 150);
  const K = ['accueil', 'blog', 'article', 'rubrique'];
  const F = pgBA(root, 'accueil', 60, 580, 960, 920, 30);
  const logo = claude3D(root, 900, 1470, 170);
  scrim(root, 'mid');
  ev('whoosh', m.start + .2, { dur: .4 }); ev('pop', s6.start + .3); TS.forEach((t, i) => { ev('whoosh', t - .05, { dur: .3 }); ev('tick', t + .35, { f: 1700 + i * 180 }); });
  return t => {
    lab(t);
    let i = -1; TS.forEach((ts, k) => { if (t >= ts - .15) i = k; }); const ki = Math.max(0, i); F.key(K[ki]);
    const p = P(t, m.start + .05, .5), sw = i >= 0 ? P(t, TS[i] - .15, .25) : 1, whip = i > 0 && sw < 1 ? (1 - io(sw)) * 900 : 0;
    put(F.el, { x: whip, y: (1 - eoBack(p)) * 260 + Math.sin(t * 1.2) * 5, s: .92 + .08 * eoBack(p), r: whip / 200, op: cl(p * 3) });
    F.set(i < 0 ? 0 : io(P(t, TS[i] + .05, .4)), i < 0 ? 0 : Math.max(0, t - TS[i]) * 120);
    logo(t, P(t, s6.start + .2, .5), { op: cl(P(t, s6.start + .2, .5) * 3), y: Math.sin(t * 1.4) * 8 });
  };
});

/* ----- 6 — quatre couleurs, une nouvelle police, la même charte partout ----- */
scene('palette', ['Quatre couleurs', 'Une nouvelle police', 'Partout la même charte'], (root, m) => {
  const s7 = S(m, 's7'), D = dv(s7), tF = s7.start + D * .35, tP = s7.start + D * .62;
  const lab = swap(root, 'lbl', [{ html: 'Quatre couleurs', a: s7.start + .05 }, { html: 'Une nouvelle police', a: tF }, { html: 'Partout la même charte', a: tP }], 84, 304, 846, 150);
  const COL = ['#E84393', '#6C5CE7', '#00B388', '#FF6B35'];
  const dots = COL.map((c, i) => dot(root, c, 96 + i * 230, 620, 196));
  const ty = thumb(root, 'assets/typo.jpg', 130, 880, 820, 410, '50% 50%', 30); ty.querySelector('img').style.objectFit = 'contain';
  const mini = ['accueil', 'blog', 'article', 'manifeste'].map((k, i) => thumb(root, PG('apres', k), 84 + i * 216, 1330, 198, 240, '50% 0%', 16));
  scrim(root, 'mid');
  COL.forEach((_, i) => { ev('pop', s7.start + .15 + i * .14); ev('tick', s7.start + .15 + i * .14, { f: 1600 + i * 220 }); }); ev('whoosh', tF, { dur: .4 }); mini.forEach((_, i) => ev('pop', tP + .1 + i * .1)); ev('ding', tP + .6, { f: 1568 });
  return t => {
    lab(t);
    dots.forEach((d, i) => { const q = P(t, s7.start + .15 + i * .14, .45); put(d, { y: Math.sin(t * 2 + i) * 7 * q, s: .3 + .7 * eoBack(q), op: cl(q * 3) }); });
    { const q = P(t, tF, .5); put(ty, { y: (1 - eoBack(q)) * 200 + Math.sin(t * 1.3) * 5, s: .9 + .1 * eoBack(q), op: cl(q * 3) }); }
    mini.forEach((e, i) => { const q = P(t, tP + .1 + i * .1, .45); put(e, { y: (1 - eoBack(q)) * 200 + Math.sin(t * 1.5 + i) * 5 * q, r: (i - 1.5) * 2 * q, op: cl(q * 3) }); });
  };
});

/* ----- 7 — rien n'a cassé : mêmes pages, même contenu ----- */
scene('rien', ['Rien n’a cassé', 'Avant', 'Après', '✓ Mêmes pages', '✓ Même contenu'], (root, m) => {
  const s8 = S(m, 's8'), D = dv(s8), T1 = s8.start + D * .4, T2 = s8.start + D * .6;
  const lab = swap(root, 'lbl', [{ html: 'Rien n’a cassé', a: s8.start + .05 }], 84, 304, 846, 150);
  const hA = pill(root, 'Avant', 84, 660, 410, 64, 'background:rgba(255,255,255,.14);color:#fff;font-size:34px'), hB = pill(root, 'Après', 520, 660, 410, 64, 'background:var(--yellow);color:var(--ink);font-size:34px');
  const K = ['accueil', 'article'];
  const cols = ['avant', 'apres'].map((tg, c) => K.map((k, j) => thumb(root, PG(tg, k), 84 + c * 436, 744 + j * 290, 410, 270, '50% 0%', 18)));
  const ok = ['Mêmes pages', 'Même contenu'].map((n, i) => pill(root, '✓ ' + n, 84 + i * 436, 1350, 410, 110, 'background:var(--green);color:#fff;font-size:40px'));
  scrim(root, 'mid');
  ev('whoosh', m.start + .2, { dur: .4 }); [T1, T2].forEach((t, i) => { ev('pop', t); ev('ding', t + .08, { f: 1318 + i * 250 }); });
  return t => {
    lab(t);
    [hA, hB].forEach((e, i) => put(e, { op: cl(P(t, m.start + .1 + i * .1, .4) * 3) }));
    cols.forEach((col, c) => col.forEach((e, j) => { const q = P(t, m.start + .15 + c * .12 + j * .1, .45); put(e, { x: (c ? 1 : -1) * 200 * (1 - eoBack(q)), y: Math.sin(t * 1.4 + c + j) * 5, op: cl(q * 3) }); }));
    ok.forEach((e, i) => { const q = P(t, [T1, T2][i], .45); put(e, { y: (1 - eoBack(q)) * 100, s: .7 + .3 * eoBack(q), op: cl(q * 3) }); });
  };
});

/* ----- 8 — l'avant, l'après : balayage plein écran ----- */
scene('ba', ['L’avant, l’après', 'avant', 'après'], (root, m) => {
  const s9 = S(m, 's9');
  const lab = swap(root, 'lbl', [{ html: 'L’avant, l’après', a: s9.start + .05 }], 84, 304, 846, 150);
  const F = pgBA(root, 'article', 0, 570, 1080, 960, 0);
  const tA = pill(root, 'avant', 84, 1450, 170, 64, 'background:rgba(15,16,32,.85);color:#fff;font-size:34px'), tB = pill(root, 'après', 760, 1450, 170, 64, 'background:var(--yellow);color:var(--ink);font-size:34px');
  scrim(root, 'mid');
  ev('whoosh', m.start + .3, { dur: .5 }); ev('whoosh', m.start + 1.8, { dur: .5 }); ev('whoosh', m.start + 3.3, { dur: .5 });
  return t => {
    lab(t); const p = P(t, m.start + .05, .45), u = t - m.start;
    put(F.el, { y: (1 - eoBack(p)) * 300, op: cl(p * 3) });
    F.set(cl(.5 - .48 * Math.cos(Math.max(0, u - .4) * 2.1)), Math.max(0, u - .2) * 90);
    [tA, tB].forEach((e, i) => put(e, { op: cl(P(t, m.start + .4 + i * .1, .4) * 3) }));
  };
});

/* ----- 9 — appel : commente « charte » ----- */
scene('cta', ['Commente « charte »', 'charte', 'Tu veux faire pareil sur ton site ?'], (root, m) => {
  const k1 = S(m, 'k1');
  const lab = swap(root, 'lbl w', [{ html: 'Commente « <span class="hl" style="margin:0 .12em">charte</span> »', a: k1.start, upd: (e, t) => hlSet(e, P(t, k1.start + .5, .45)) }], 84, 304, 846, 150);
  const th = ['accueil', 'blog', 'article', 'manifeste', 'comparatif'].map((k, i) => thumb(root, PG('apres', k), 76 + i * 194, 560, 172, 300, '50% 0%', 16));
  const cm = mk(root, 'abs cm', '<div class="av"></div><div class="tx ty" style="font-size:96px"></div><div class="snd">' + ICON.send() + '</div>'); place(cm, 84, 960, 846, 210);
  const ty = cm.querySelector('.ty'), snd = cm.querySelector('.snd');
  const tag = txt(root, 'lbl w', 'Tu veux faire pareil sur ton site ?', 84, 1260, 846, 220); tag.style.fontSize = '56px';
  const WORD = 'charte', typeAt = k1.start + 1.0, ST = .14;
  ev('whoosh', m.start + .3, { dur: .5 }); th.forEach((_, i) => ev('pop', m.start + .5 + i * .12));
  WORD.split('').forEach((_, i) => ev('tick', typeAt + i * ST, { f: 2600 + i * 70 })); ev('pop', typeAt + WORD.length * ST + .3); ev('ding', typeAt + WORD.length * ST + .4, { f: 1174 }); ev('ding', k1.start + 3.8, { f: 1568 });
  return t => {
    lab(t);
    th.forEach((e, i) => { const dir = i % 2 ? 1 : -1, p = P(t, m.start + .5 + i * .12, .5), k = eoBack(p); put(e, { y: dir * 420 * (1 - k) + Math.sin(t * 1.3 + i) * 6 * p, s: .9 + .1 * k, op: cl(p * 3) }); });
    const p = P(t, m.start + .9, .5); put(cm, { y: (1 - eoBack(p)) * 300, s: .94 + .06 * eoBack(p), op: cl(p * 3) });
    ty.textContent = WORD.slice(0, Math.floor(cl((t - typeAt) / ST, 0, WORD.length)));
    const sp = P(t, typeAt + WORD.length * ST + .3, .3); snd.style.transform = `scale(${1 + .25 * Math.sin(sp * Math.PI)})`; snd.style.background = sp >= 1 ? 'var(--green)' : 'var(--violet)';
    const q = P(t, typeAt + WORD.length * ST + .8, .5); put(tag, { y: (1 - eoBack(q)) * 90, op: cl(q * 2.4) });
  };
});
