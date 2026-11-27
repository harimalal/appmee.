/* ===== reel n°8 — Content Factory : un article → tous tes posts (rendus FIDÈLES des vrais fichiers : atomes.md, positions.md, linkedin.md, x.md, sortie de content-qa) ===== */
const CM = /*CARDS*/null;
const ARTF = 1080 / 1280, ARTH = 6400 * ARTF;
const SL = k => 'assets/slides/' + k + '.jpg';
const CARD = id => 'assets/cards/' + id + '.png';
const SHADOW = '0 24px 60px rgba(20,20,60,.24)';
const cardImg = (cv, id, x, y) => { const i = img(cv, CARD(id), 'pgf'); place(i, x, y, CM[id].w, CM[id].h); i.style.borderRadius = '28px'; i.style.boxShadow = SHADOW; return i; };
const partR = (id, p, ox, oy, pad = 8) => { const q = CM[id].parts[p]; return { x: ox + q.x - pad, y: oy + q.y - pad, w: q.w + 2 * pad, h: q.h + 2 * pad }; };
const partC = (id, p, ox, oy) => { const q = CM[id].parts[p]; return { x: ox + q.x + q.w / 2, y: oy + q.y + q.h / 2 }; };
const thumb = (parent, src, x, y, w, h, pos = '50% 0%', rad = 18) => { const d = mk(parent, 'abs', null); d.dataset.deco = ''; place(d, x, y, w, h); d.style.cssText += `;overflow:hidden;border-radius:${rad}px;box-shadow:${SHADOW};background:#fff`; const i = img(d, src); i.style.cssText += `;display:block;width:100%;height:100%;object-fit:cover;object-position:${pos}`; return d; };
const camAtP = (K, t, px, py) => { const q = proj(camAt(K, t), px, py); return { t, x: q.x, y: q.y }; };
function makeVSwipe(root, a, b, x, y0, y1) { const e = mk(root, 'abs swp', null); e.dataset.deco = ''; e.style.zIndex = 48; return t => { const p = P(t, a, b - a); if (p <= 0 || p >= 1) { e.style.opacity = 0; return; } const k = io(p); e.style.transform = `translate(${x - 46}px,${lerp(y0, y1, k) - 46}px) scale(${1 - .18 * Math.sin(p * Math.PI)})`; e.style.opacity = Math.min(1, Math.sin(p * Math.PI) * 2.2); }; }

/* ----- 1 — ouverture : l'article, d'où sortent les posts ; puis zoom sur le titre ----- */
scene('ouverture', ['Un article → tous tes posts', 'Le coût réel d’OpenClaw'], (root, m) => {
  const o1 = S(m, 'o1'), o2 = S(m, 'o2');
  const L = lyr(root); const art = img(L.cv, 'assets/pc/article.jpg', 'pgf'); place(art, 0, 0, 1080, ARTH);
  const pops = makePops(L.cv, 'assets/pc/article.jpg', 1080, ARTH, 0, 0);
  const H1 = { x: 294 * ARTF - 10, y: 201 * ARTF - 10, w: 692 * ARTF + 20, h: 101 * ARTF + 20 }, h1c = { x: H1.x + H1.w / 2, y: H1.y + H1.h / 2 };
  const dim = mk(root, 'abs', null); dim.dataset.deco = ''; place(dim, 0, 0, 1080, 1920); dim.style.background = 'rgba(15,16,32,.5)'; dim.style.opacity = 0;
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Un article → <span class="hl">tous tes posts</span>', a: o1.start + .1, upd: (e, t) => hlSet(e, P(t, o1.start + 1.1, .5)) }, { html: 'Le coût réel d’OpenClaw', a: o2.start }], 84, 304, 846, 150);
  // les trois sorties réelles jaillissent de l'article
  const FAN = [[CARD('linkedin'), '50% 0%'], [SL('oc1'), '50% 50%'], [CARD('x'), '50% 0%']];
  const fan = FAN.map(([src, pos], i) => thumb(root, src, 540 - 170, 1060, 340, 425, pos, 22));
  fan[1].style.zIndex = 3;
  const tIn = o1.start + .8, tOut = o2.start - .15;
  const K = [{ t: m.start, ...camTop(1) }, { t: o1.start + 1.5, x: 540, y: camTop(1).y + 40, z: 1.05 }, { t: o2.start + .1, x: 560, y: camTop(1).y + 30, z: 1.08 },
    { t: o2.start + 1.0, x: h1c.x, y: h1c.y + 40, z: 1.7, dip: .06 }, { t: m.end + .45, x: h1c.x + 10, y: h1c.y + 46, z: 1.76 }];
  const tc = o2.start + 1.35; pops.add(H1, tc, m.end + 2, 1.08);
  const cur = makeCursor(root, [{ t: o2.start + .2, x: 950, y: 1640 }, camAtP(K, tc - .45, h1c.x + 160, h1c.y + 110), camAtP(K, tc, h1c.x + 60, h1c.y + 18)]);
  const clk = makeClicks(root, cur, [tc]);
  ev('thump', m.start + .25, { amp: .7 }); fan.forEach((_, i) => ev('pop', tIn + i * .14)); ev('ding', tIn + .7, { f: 988 }); ev('whoosh', tOut, { dur: .5, down: true }); ev('tick', tc, { f: 1800 }); ev('pop', tc + .1);
  return t => {
    lab(t); applyScr(L.cv, camAt(K, t)); pops.upd(t);
    const out = P(t, tOut, .5);
    dim.style.opacity = .55 * P(t, tIn - .2, .4) * (1 - out);
    fan.forEach((e, i) => { const p = P(t, tIn + i * .14, .6), k = eoBack(p), d = i - 1;
      put(e, { x: d * 300 * k, y: (1 - k) * 60 + Math.abs(d) * 50 * k + Math.sin(t * 1.6 + i) * 8 * p + out * 900, r: d * 9 * k, s: .35 + .65 * k, op: cl(p * 3) * (1 - out) }); });
    cur.upd(t, t > tc + .6 ? Math.max(0, 1 - P(t, tc + .6, .3)) : 1); clk(t);
  };
});

/* ----- 2 — la fiche d'atomes : les faits, chaque chiffre avec sa source ----- */
scene('fiche', ['Une fiche, chaque chiffre sourcé'], (root, m) => {
  const f1 = S(m, 'f1'), D = dv(f1), OX = 40, OY = 600;
  const L = lyr(root); cardImg(L.cv, 'fiche', OX, OY);
  const pops = makePops(L.cv, CARD('fiche'), CM.fiche.w, CM.fiche.h, OX, OY);
  const ids = ['A1', 'A2', 'A6', 'A8', 'A12', 'A14'];
  const covers = ids.map(id => { const r = partR('fiche', 'at-' + id, OX, OY, 0); const c = mk(L.cv, 'abs', null); c.dataset.deco = ''; place(c, r.x, r.y + 2, r.w, r.h - 2); c.style.background = '#fff'; return c; });
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Une fiche, chaque <span class="hl">chiffre sourcé</span>', a: f1.start + .1, fs: 58, upd: (e, t) => hlSet(e, P(t, f1.start + D * .7, .5)) }], 84, 304, 846, 190);
  const RT = ids.map((_, i) => f1.start + .3 + i * .3), a6 = partC('fiche', 'at-A6', OX, OY), tc = f1.start + D * .72;
  const K = [{ t: m.start, x: 540, y: 980, z: 1 }, { t: tc - .5, x: 540, y: 1000, z: 1.02 }, { t: tc + .3, x: a6.x + 20, y: a6.y + 40, z: 1.5, dip: .05 }, { t: tc + 1.8, x: a6.x + 26, y: a6.y + 46, z: 1.52 }, { t: tc + 2.5, x: 540, y: 1040, z: 1.0 }, { t: m.end + .45, x: 545, y: 1060, z: 1.03 }];
  pops.add(partR('fiche', 'at-A6', OX, OY, 10), tc, tc + 1.9, 1.06);
  const cur = makeCursor(root, [{ t: tc - 1.2, x: 950, y: 1650 }, camAtP(K, tc - .4, a6.x + 220, a6.y + 120), camAtP(K, tc, a6.x + 120, a6.y + 20)]);
  const clk = makeClicks(root, cur, [tc]);
  ev('whoosh', m.start + .3, { dur: .5 }); RT.forEach(t => ev('tick', t, { f: 2400 })); ev('tick', tc, { f: 1800 }); ev('pop', tc + .1); ev('ding', tc + .5, { f: 1046 });
  return t => {
    lab(t); applyScr(L.cv, camAt(K, t)); pops.upd(t);
    covers.forEach((c, i) => { const p = P(t, RT[i], .35); c.style.opacity = 1 - p; c.style.transform = `translateX(${60 * eo(p)}px)`; });
    cur.upd(t, t > tc + .7 ? Math.max(0, 1 - P(t, tc + .7, .3)) : 1); clk(t);
  };
});

/* ----- 3 — la position : proposée, puis validée par Hari ----- */
scene('position', ['Une position, je valide', 'Valider', '✓ Validée'], (root, m) => {
  const p1 = S(m, 'p1'), D = dv(p1), OX = 40, OY = 590;
  const L = lyr(root); cardImg(L.cv, 'position', OX, OY);
  const pops = makePops(L.cv, CARD('position'), CM.position.w, CM.position.h, OX, OY);
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Une position, <span class="hl">je valide</span>', a: p1.start + .1, upd: (e, t) => hlSet(e, P(t, p1.start + D * .75, .5)) }], 84, 304, 846, 150);
  const st = partC('position', 'pos-statut', OX, OY), ts = p1.start + .5, tv = p1.start + D * .72;
  pops.add(partR('position', 'pos-statut', OX, OY, 8), ts, tv - .4, 1.06);
  const K = [{ t: m.start, x: 540, y: 980, z: 1 }, { t: ts + .3, x: st.x, y: st.y + 160, z: 1.22 }, { t: tv - .5, x: st.x + 10, y: st.y + 170, z: 1.24 }, { t: tv + .2, x: 540, y: 990, z: 1 }, { t: m.end + .45, x: 545, y: 1005, z: 1.03 }];
  const btn = mk(root, 'abs', null); btn.dataset.deco = ''; place(btn, 300, 1446, 480, 92); btn.style.cssText += ';border-radius:999px;background:#fff;border:5px solid var(--violet);box-shadow:0 14px 34px rgba(60,40,140,.25)';
  const b1 = mk(root, 'abs tx', 'Valider'); place(b1, 300, 1446, 480, 92); b1.style.cssText += ';display:flex;align-items:center;justify-content:center;font:900 46px/1 var(--font);color:var(--violet)';
  const b2 = mk(root, 'abs tx', '✓ Validée'); place(b2, 300, 1446, 480, 92); b2.style.cssText += ';display:flex;align-items:center;justify-content:center;font:900 46px/1 var(--font);color:#fff;visibility:hidden';
  const bc = { x: 540, y: 1492 };
  const cur = makeCursor(root, [{ t: tv - 1.1, x: 950, y: 1700 }, { t: tv - .35, x: bc.x + 120, y: bc.y + 70 }, { t: tv, x: bc.x + 30, y: bc.y + 10 }]);
  const clk = makeClicks(root, cur, [tv]);
  ev('whoosh', m.start + .3, { dur: .5 }); ev('pop', ts); ev('tick', tv, { f: 1800 }); ev('ding', tv + .15, { f: 1174 });
  return t => {
    lab(t); applyScr(L.cv, camAt(K, t)); pops.upd(t);
    const pin = P(t, p1.start + .8, .5); [btn, b1, b2].forEach(e => put(e, { y: (1 - eoBack(pin)) * 160, s: t >= tv ? 1 + .06 * Math.sin(P(t, tv, .4) * Math.PI) : 1, op: cl(pin * 3) }));
    const ok = t >= tv; btn.style.background = ok ? 'var(--green)' : '#fff'; btn.style.borderColor = ok ? 'var(--green)' : 'var(--violet)';
    b1.style.visibility = ok ? 'hidden' : 'visible'; b2.style.visibility = ok ? 'visible' : 'hidden';
    cur.upd(t, t > tv + .6 ? Math.max(0, 1 - P(t, tv + .6, .3)) : 1); clk(t);
  };
});

/* ----- 4 — trois fabriques : LinkedIn, fil X, carrousel ----- */
scene('fabriques', ['Trois fabriques', 'Le post LinkedIn', 'Le fil X', 'Le carrousel', 'LinkedIn', 'X', 'Carrousel', 'le verdict pour chaque profil', 'un fil de six posts', 'Instagram · LinkedIn · Pinterest · TikTok'], (root, m) => {
  const b1 = S(m, 'b1'), b2 = S(m, 'b2'), b3 = S(m, 'b3'), b4 = S(m, 'b4');
  const OX = 40, OY = 600;
  // couche LinkedIn
  const LL = lyr(root); cardImg(LL.cv, 'linkedin', OX, OY);
  const popL = makePops(LL.cv, CARD('linkedin'), CM.linkedin.w, CM.linkedin.h, OX, OY);
  const pq = CM.linkedin.parts['pp-2'], pr = CM.linkedin.parts['pp-3'];
  const R2 = { x: OX + 22, y: OY + pq.y - 12, w: CM.linkedin.w - 44, h: pr.y - pq.y + 4 }, r2c = { x: R2.x + R2.w / 2, y: R2.y + R2.h / 2 };
  const t2c = b2.start + 1.7;
  popL.add(R2, t2c, b3.start + .2, 1.05);
  const KL = [{ t: b2.start - .2, x: 540, y: 960, z: 1 }, { t: t2c - .2, x: 540, y: r2c.y - 140, z: 1.02 }, { t: t2c + .4, x: r2c.x, y: r2c.y - 120, z: 1.18 }, { t: b3.start + .3, x: r2c.x, y: r2c.y - 110, z: 1.2 }];
  // couche fil X
  const LX = lyr(root); cardImg(LX.cv, 'x', OX, OY);
  const KX = [{ t: b3.start - .2, x: 540, y: 960, z: 1 }, { t: b3.start + .5, x: 540, y: 1000, z: 1 }, { t: b4.start, x: 540, y: 1700, z: 1 }];
  // couche carrousel (7 vraies slides)
  const LC = mk(root, 'abs', null); LC.dataset.deco = ''; place(LC, 0, 0, 1080, 1920);
  const SWd = 1080 * .74, SHt = 1350 * .74, GAP = 34, STEP = SWd + GAP, CY = 1150, TOP = CY - SHt / 2;
  const tr = mk(LC, 'abs', null); place(tr, 0, TOP, 7 * STEP + 1080, SHt);
  for (let i = 1; i <= 7; i++) { const s = thumb(tr, SL('oc' + i), 540 - SWd / 2 + (i - 1) * STEP, 0, SWd, SHt, '50% 50%', 24); }
  const SWT = Array.from({ length: 6 }, (_, i) => b4.start + .55 + i * .42), tp = SWT[5] + .75;
  const veil = mk(LC, 'abs', null); place(veil, 0, 0, 1080, 1920); veil.style.cssText += ';background:#fff;opacity:0';
  const pp = thumb(LC, SL('oc7'), 540 - SWd / 2, TOP, SWd, SHt, '50% 50%', 24); pp.style.opacity = 0;
  // tuiles des trois fabriques
  const TILES = [['LinkedIn', CARD('linkedin'), '50% 0%'], ['X', CARD('x'), '50% 0%'], ['Carrousel', SL('oc1'), '50% 50%']];
  const tiles = TILES.map(([nm, src, pos], i) => { const w = mk(root, 'abs', null); w.dataset.deco = ''; place(w, 84 + i * 293, 640, 260, 430); thumb(w, src, 0, 0, 260, 340, pos, 18); const n = mk(w, 'tx', nm); n.style.cssText += ';position:absolute;left:0;top:362px;width:260px;text-align:center;font:900 44px/1 var(--font);letter-spacing:-.02em'; return w; });
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Trois <span class="hl">fabriques</span>', a: b1.start + .1, upd: (e, t) => hlSet(e, P(t, b1.start + .8, .5)) }, { html: 'Le post LinkedIn', a: b2.start }, { html: 'Le fil X', a: b3.start }, { html: 'Le carrousel', a: b4.start }], 84, 304, 846, 150);
  const sub = swap(root, 'sublbl', [{ html: 'le verdict pour chaque profil', a: b2.start + .6 }, { html: 'un fil de six posts', a: b3.start + .4 }, { html: 'Instagram · LinkedIn · Pinterest · TikTok', a: b4.start + .5, b: m.end + 1 }], 84, 466, 846, 40);
  const vs = makeVSwipe(root, b3.start + .5, b4.start - .3, 900, 1560, 860);
  const sws = makeSwipes(root, SWT.map(t => ({ a: t - .12, b: t + .32, y: CY, x0: 900, x1: 300 })));
  const cur = makeCursor(root, [{ t: t2c - 1.0, x: 950, y: 1650 }, camAtP(KL, t2c - .35, r2c.x + 260, r2c.y + 60), camAtP(KL, t2c, r2c.x + 180, r2c.y - 10), { t: t2c + .9, x: 990, y: 1500 }, { t: tp - .5, x: 900, y: 1500 }, { t: tp, x: 620, y: CY + 70 }]);
  const clk = makeClicks(root, cur, [t2c, tp]);
  ev('whoosh', m.start + .3, { dur: .5 }); tiles.forEach((_, i) => ev('pop', b1.start + .5 + i * .3)); ev('whoosh', b2.start - .1, { dur: .5, up: true }); ev('tick', t2c, { f: 1800 }); ev('pop', t2c + .1);
  ev('swipe', b3.start - .1); ev('swipe', b4.start - .1); SWT.forEach(t => ev('swipe', t)); ev('tick', tp, { f: 1800 }); ev('pop', tp + .1); ev('ding', tp + .4, { f: 1046 });
  return t => {
    lab(t); sub(t);
    tiles.forEach((w, i) => { const p = P(t, b1.start + .5 + i * .3, .5), k = eoBack(p), out = P(t, b2.start - .35, .35); put(w, { y: (1 - k) * 200 * (i % 2 ? -1 : 1) + Math.sin(t * 1.5 + i) * 7 * p - out * 300, s: .9 + .1 * k, op: cl(p * 3) * (1 - out) }); });
    // LinkedIn : entre en plongée, sort par la gauche au swipe vers le fil X
    const lin = P(t, b2.start - .25, .45), lout = io(P(t, b3.start - .15, .45));
    LL.w.style.opacity = lin; LL.w.style.transform = `translateX(${-1080 * lout}px) scale(${lerp(.86, 1, eo(lin))})`; applyScr(LL.cv, camAt(KL, t)); popL.upd(t);
    const xin = io(P(t, b3.start - .15, .45)), xout = io(P(t, b4.start - .15, .45));
    LX.w.style.opacity = t < b3.start - .2 ? 0 : 1; LX.w.style.transform = `translateX(${1080 * (1 - xin) - 1080 * xout}px)`; applyScr(LX.cv, camAt(KX, t));
    const cin = io(P(t, b4.start - .15, .45)); LC.style.opacity = t < b4.start - .2 ? 0 : 1; LC.style.transform = `translateX(${1080 * (1 - cin)}px)`;
    let idx = 0; SWT.forEach(tt => { idx += io(P(t, tt, .38)); }); put(tr, { x: -idx * STEP });
    const pop = eo(P(t, tp, .3)); veil.style.opacity = .62 * pop; pp.style.opacity = pop > .01 ? 1 : 0; pp.style.transform = `translateY(${-14 * pop}px) scale(${1 + .14 * pop})`;
    vs(t); sws(t); cur.upd(t, (t > t2c + .7 && t < tp - 1.0) ? 0 : (t > tp + .6 ? Math.max(0, 1 - P(t, tp + .6, .3)) : 1)); clk(t);
  };
});

/* ----- 5 — le contrôle : sortie réelle de content-qa ; un chiffre absent de la fiche est refusé ----- */
scene('controle', ['Le contrôle', 'Fidèle à l’article', 'Chiffre absent de la fiche : refusé', 'Aucun chiffre inventé'], (root, m) => {
  const c1 = S(m, 'c1'), c2 = S(m, 'c2'), D = dv(c1), OX = 40, OY = 620;
  const L = lyr(root); cardImg(L.cv, 'term', OX, OY);
  const pops = makePops(L.cv, CARD('term'), CM.term.w, CM.term.h, OX, OY);
  const NL = Object.keys(CM.term.parts).filter(k => k.startsWith('tl-')).length;
  const covers = Array.from({ length: NL }, (_, i) => { const r = partR('term', 'tl-' + i, OX, OY, 2); const c = mk(L.cv, 'abs', null); c.dataset.deco = ''; place(c, r.x, r.y, r.w + 30, r.h); c.style.background = '#12132A'; return c; });
  const T0 = c1.start + .25, TL = i => i === 0 ? T0 : T0 + .95 + (i - 1) * .2, tok = TL(NL - 1) + .35;
  const ok = partC('term', 'tl-' + (NL - 1), OX, OY);
  pops.add(partR('term', 'tl-' + (NL - 1), OX, OY, 10), tok, c2.start + .6, 1.1);
  const K = [{ t: m.start, x: 540, y: 960, z: 1 }, { t: tok - .2, x: 540, y: 960, z: 1.02 }, { t: tok + .4, x: ok.x, y: ok.y + 120, z: 1.32 }, { t: c2.start + .2, x: ok.x, y: ok.y + 130, z: 1.33 }, { t: c2.start + .9, x: 540, y: 960, z: 1 }, { t: m.end + .45, x: 545, y: 975, z: 1.03 }];
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Le <span class="hl">contrôle</span>', a: c1.start + .1, upd: (e, t) => hlSet(e, P(t, c1.start + .7, .5)) }, { html: 'Fidèle à l’article', a: c2.start }], 84, 304, 846, 150);
  const tRef = c1.start + D * .5;
  const red = mk(root, 'abs tx', 'Chiffre absent de la fiche : refusé'); place(red, 84, 1330, 846, 110); red.style.cssText += ';display:flex;align-items:center;justify-content:center;background:#FDECEC;color:#C62828;border:4px solid #E5383B;border-radius:999px;font:900 40px/1 var(--font);letter-spacing:-.02em;white-space:nowrap';
  const grn = mk(root, 'abs tx', 'Aucun chiffre inventé'); place(grn, 84, 1330, 846, 110); grn.style.cssText += ';display:flex;align-items:center;justify-content:center;background:var(--green);color:#fff;border-radius:999px;font:900 50px/1 var(--font);letter-spacing:-.02em;white-space:nowrap';
  ev('whoosh', m.start + .3, { dur: .5 }); ev('ticks', T0, { n: 14, dur: .8 }); for (let i = 1; i < NL; i++) ev('tick', TL(i), { f: 2200 + i * 60 }); ev('pop', tok); ev('ding', tok + .2, { f: 1174 }); ev('pop', tRef); ev('pop', c2.start + .3); ev('ding', c2.start + .6, { f: 1568 });
  return t => {
    lab(t); applyScr(L.cv, camAt(K, t)); pops.upd(t);
    covers.forEach((c, i) => { if (i === 0) { const p = P(t, T0, .8); c.style.clipPath = `inset(0 0 0 ${Math.floor(p * 40) / 40 * 100}%)`; } else { c.style.opacity = t >= TL(i) ? 0 : 1; } });
    const rp = P(t, tRef, .45), rout = P(t, c2.start - .1, .3); put(red, { y: (1 - eoBack(rp)) * 120 + rout * 140, op: cl(rp * 2.4) * (1 - rout) });
    const gp = P(t, c2.start + .3, .45); put(grn, { y: (1 - eoBack(gp)) * 120, s: gp >= 1 ? 1 + .02 * Math.sin((t - c2.start) * 5) : 1, op: cl(gp * 2.4) });
  };
});

/* ----- 6 — appel : commente « contenu » ----- */
scene('cta', ['Commente « contenu »', 'contenu', 'Tu veux le même système ?'], (root, m) => {
  const k1 = S(m, 'k1');
  const c = circle(root, 'rgba(108,92,231,.28)', -260, 1100, 900);
  const lab = swap(root, 'lbl w', [{ html: 'Commente « <span class="hl" style="margin:0 .12em">contenu</span> »', a: k1.start, upd: (e, t) => hlSet(e, P(t, k1.start + .5, .45)) }], 84, 304, 846, 150);
  const TH = [[CARD('linkedin'), '50% 0%'], [CARD('x'), '50% 0%'], [SL('oc1'), '50% 50%'], [CARD('fiche'), '50% 0%'], [SL('oc5'), '50% 50%']];
  const th = TH.map(([src, pos], i) => { const w = mk(root, 'abs', null); w.dataset.deco = ''; place(w, 76 + i * 194, 560, 172, 215); thumb(w, src, 0, 0, 172, 215, pos, 14); return w; });
  const cm = mk(root, 'abs cm', '<div class="av"></div><div class="tx ty" style="font-size:96px"></div><div class="snd">' + ICON.send() + '</div>'); place(cm, 84, 940, 846, 210);
  const ty = cm.querySelector('.ty'), snd = cm.querySelector('.snd');
  const tag = txt(root, 'lbl w', 'Tu veux le même système ?', 84, 1250, 846, 220); tag.style.fontSize = '58px';
  const WORD = 'contenu', typeAt = k1.start + 1.0, ST = .13;
  ev('whoosh', m.start + .3, { dur: .5 }); th.forEach((_, i) => ev('pop', m.start + .5 + i * .12));
  WORD.split('').forEach((_, i) => ev('tick', typeAt + i * ST, { f: 2600 + i * 70 })); ev('pop', typeAt + WORD.length * ST + .3); ev('ding', typeAt + WORD.length * ST + .4, { f: 1174 }); ev('ding', k1.start + 3.8, { f: 1568 });
  return t => {
    drift(c, t); lab(t);
    th.forEach((w, i) => { const dir = i % 2 ? 1 : -1, p = P(t, m.start + .5 + i * .12, .5), k = eoBack(p); put(w, { y: dir * 420 * (1 - k) + Math.sin(t * 1.3 + i) * 6 * p, s: .9 + .1 * k, op: cl(p * 3) }); });
    const p = P(t, m.start + .9, .5); put(cm, { y: (1 - eoBack(p)) * 300, s: .94 + .06 * eoBack(p), op: cl(p * 3) });
    const n = Math.floor(cl((t - typeAt) / ST, 0, WORD.length)); ty.textContent = WORD.slice(0, n);
    const sp = P(t, typeAt + WORD.length * ST + .3, .3); snd.style.transform = `scale(${1 + .25 * Math.sin(sp * Math.PI)})`; snd.style.background = sp >= 1 ? 'var(--green)' : 'var(--violet)';
    const q = P(t, typeAt + WORD.length * ST + .8, .5); put(tag, { y: (1 - eoBack(q)) * 90, op: cl(q * 2.4) });
  };
});

