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
const pill = (root, text, x, y, w, h, css = '') => { const e = mk(root, 'abs tx', text); place(e, x, y, w, h); e.style.cssText += ';display:flex;align-items:center;justify-content:center;border-radius:999px;font:900 46px/1 var(--font);letter-spacing:-.02em;white-space:nowrap;' + css; return e; };
const RENDERS = [[CARD('linkedin'), '50% 0%'], [SL('oc1'), '50% 50%'], [CARD('x'), '50% 0%'], [SL('oc2'), '50% 50%'], [CARD('fiche'), '50% 0%'], [SL('oc5'), '50% 50%'], [SL('tik1'), '50% 30%'], [SL('oc7'), '50% 50%'], [SL('pin1'), '50% 20%'], [CARD('position'), '50% 0%']];

/* ----- 1 — hook : une seule source se démultiplie en tout ton contenu ----- */
scene('hook', ['Une source, tout ton contenu', 'production automatique · publication par toi'], (root, m) => {
  const h1 = S(m, 'h1'), D = dv(h1);
  const c = circle(root, 'rgba(108,92,231,.12)', -300, 1180, 820);
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Une source, tout ton contenu', a: h1.start + .1, fs: 58 }], 84, 304, 846, 150);
  const sub = swap(root, 'sublbl', [{ html: 'production automatique · publication par toi', a: h1.start + D * .55, b: m.end + 1, fs: 26 }], 84, 466, 846, 40);
  const tBurst = h1.start + 1.5;
  // les rendus réels, en grille 3 × 3 qui remplit l'écran
  const GW = 300, GH = 375, GX = 24, GY = 24, X0 = (1080 - 3 * GW - 2 * GX) / 2, Y0 = 600;
  const grid = RENDERS.slice(0, 9).map(([src, pos], i) => { const e = thumb(root, src, X0 + (i % 3) * (GW + GX), Y0 + Math.floor(i / 3) * (GH + GY), GW, GH, pos, 18); return e; });
  // la source : la vraie page de l'article, au centre, devant
  const src = thumb(root, 'assets/pc/article.jpg', 540 - 210, 780, 420, 520, '50% 0%', 22); src.style.zIndex = 5; src.style.border = '6px solid #fff';
  ev('thump', m.start + .25, { amp: .7 }); ev('whoosh', tBurst - .1, { dur: .5, up: true }); grid.forEach((_, i) => ev('pop', tBurst + i * .07)); ev('ding', tBurst + .8, { f: 988 });
  return t => {
    drift(c, t, 1.6); lab(t); sub(t);
    const ps = P(t, m.start + .15, .5), shrink = eo(P(t, tBurst + .7, .6));
    put(src, { y: (1 - eoBack(ps)) * 200 + shrink * 560 + Math.sin(t * 1.4) * 6, s: (.9 + .1 * eoBack(ps)) * (1 - .55 * shrink), op: cl(ps * 3) * (1 - .9 * shrink) });
    grid.forEach((e, i) => { const p = P(t, tBurst + i * .07, .55), k = eoBack(p); const cx = X0 + (i % 3) * (GW + GX) + GW / 2, cy = Y0 + Math.floor(i / 3) * (GH + GY) + GH / 2;
      put(e, { x: (540 - cx) * (1 - k), y: (1040 - cy) * (1 - k) + Math.sin(t * 1.5 + i) * 6 * p, r: (1 - k) * (i % 2 ? 12 : -12), s: .3 + .7 * k, op: cl(p * 3) }); });
  };
});

/* ----- 2 — les avantages : une fois, tous les réseaux, trente jours, zéro outil en plus ----- */
scene('avantages', ['Une seule fois', 'Tous tes réseaux', 'Trente jours prêts à l’avance', 'Tout tourne avec Claude', 'Article', 'Test', 'Idée', 'LinkedIn', 'X', 'Instagram', 'Pinterest', 'TikTok', 'prêts, pas encore publiés', '0 €', 'd’outil en plus', 'hors abonnement Claude'], (root, m) => {
  const a1 = S(m, 'a1'), a2 = S(m, 'a2'), a3 = S(m, 'a3'), a4 = S(m, 'a4');
  const c = circle(root, 'rgba(25,169,116,.12)', -300, 1180, 820);
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Une seule fois', a: a1.start + .1 }, { html: 'Tous tes réseaux', a: a2.start }, { html: 'Trente jours prêts à l’avance', a: a3.start, fs: 58 }, { html: 'Tout tourne avec Claude', a: a4.start }], 84, 304, 846, 150);
  const sub = swap(root, 'sublbl', [{ html: 'prêts, pas encore publiés', a: a3.start + .6 }, { html: 'hors abonnement Claude', a: a4.start + .9, b: m.end + 1 }], 84, 466, 846, 40);
  // (a1) trois entrées qui convergent
  const IN = ['Article', 'Test', 'Idée'].map((n, i) => pill(root, n, 84 + i * 293, 700, 260, 110, 'background:#fff;color:var(--ink);box-shadow:0 12px 30px rgba(20,20,60,.14)'));
  const one = pill(root, '', 290, 1040, 500, 500, 'background:transparent'); one.classList.remove('tx'); one.dataset.deco = '';
  const srcT = thumb(one, 'assets/pc/article.jpg', 50, 0, 400, 500, '50% 0%', 22);
  // (a2) cinq réseaux + le vrai rendu de chacun
  const NETS = [['LinkedIn', CARD('linkedin'), '50% 0%'], ['X', CARD('x'), '50% 0%'], ['Instagram', SL('oc1'), '50% 50%'], ['Pinterest', SL('pin1'), '50% 20%'], ['TikTok', SL('tik1'), '50% 30%']];
  const chips = NETS.map(([n], i) => pill(root, n, i < 3 ? 84 + i * 289 : 230 + (i - 3) * 330, i < 3 ? 600 : 712, i < 3 ? 268 : 290, 90, 'background:#fff;color:var(--ink);font-size:38px;box-shadow:0 10px 24px rgba(20,20,60,.12)'));
  const shots = NETS.map(([, src, pos]) => thumb(root, src, 540 - 230, 850, 460, 640, pos, 24));
  const tN = NETS.map((_, i) => a2.start + .35 + i * (dv(a2) * .82 / 5));
  // (a3) calendrier de trente cases
  const CW = 132, CH = 150, CG = 12, CX0 = (1080 - (6 * CW + 5 * CG)) / 2, CY0 = 620;
  const cells = Array.from({ length: 30 }, (_, i) => { const w = mk(root, 'abs', null); w.dataset.deco = ''; place(w, CX0 + (i % 6) * (CW + CG), CY0 + Math.floor(i / 6) * (CH + CG), CW, CH); w.style.cssText += ';border-radius:14px;background:#fff;border:3px solid #E4E1F3;overflow:hidden'; const [s, p] = RENDERS[i % RENDERS.length]; const t = thumb(w, s, 0, 0, CW - 6, CH - 6, p, 10); t.style.boxShadow = 'none'; return { w, t }; });
  const tC = i => a3.start + .3 + i * .055;
  // (a4) zéro euro d'outil en plus
  const big = mk(root, 'abs tx', '0 €'); place(big, 84, 680, 846, 300); big.style.cssText += ';display:flex;align-items:center;justify-content:center;font:900 300px/1 var(--font);letter-spacing:-.05em;color:var(--green)';
  const bigS = mk(root, 'abs tx', 'd’outil en plus'); place(bigS, 84, 1110, 846, 90); bigS.style.cssText += ';display:flex;align-items:center;justify-content:center;font:900 64px/1 var(--font);letter-spacing:-.03em';
  ev('whoosh', m.start + .3, { dur: .5 }); IN.forEach((_, i) => ev('pop', a1.start + .2 + i * .25)); ev('whoosh', a1.start + 1.6, { dur: .4 });
  tN.forEach(t => { ev('tick', t, { f: 2000 }); ev('pop', t + .05); }); for (let i = 0; i < 30; i += 3) ev('tick', tC(i), { f: 2400 + i * 20 }); ev('ding', tC(29) + .3, { f: 1174 }); ev('pop', a4.start + .2); ev('ding', a4.start + .6, { f: 1568 });
  return t => {
    drift(c, t, 3); lab(t); sub(t);
    const out1 = P(t, a2.start - .3, .3), out2 = P(t, a3.start - .3, .3), out3 = P(t, a4.start - .3, .3);
    // a1
    IN.forEach((e, i) => { const p = P(t, a1.start + .2 + i * .25, .45), conv = io(P(t, a1.start + 1.5, .6)); const cx = 84 + i * 293 + 130; put(e, { x: (540 - cx) * conv, y: (1 - eoBack(p)) * 120 + conv * 330, s: 1 - .5 * conv, op: cl(p * 3) * (1 - conv) * (1 - out1) }); });
    { const p = P(t, a1.start + 1.8, .5); put(one, { y: (1 - eoBack(p)) * 120 - 70 + Math.sin(t * 1.4) * 6, s: .8 + .2 * eoBack(p), op: cl(p * 3) * (1 - out1) }); }
    // a2
    chips.forEach((e, i) => { const p = P(t, a2.start + i * .08, .4), on = t >= tN[i] && (i === 4 || t < tN[i + 1]); put(e, { y: (1 - eoBack(p)) * 60, s: on ? 1.08 : 1, op: cl(p * 3) * (1 - out2) }); e.style.background = on ? 'var(--violet)' : '#fff'; e.style.color = on ? '#fff' : 'var(--ink)'; });
    shots.forEach((e, i) => { const on = P(t, tN[i], .3), off = i < 4 ? P(t, tN[i + 1], .3) : out2; put(e, { x: (1 - eo(on)) * 500 - eo(off) * 500, y: Math.sin(t * 1.5) * 6, r: (1 - on) * 6 - off * 6, op: cl(on * 3) * (1 - off) }); });
    // a3
    cells.forEach(({ w, t: im }, i) => { const p = P(t, a3.start - .1, .4); put(w, { y: (1 - eoBack(p)) * 80, op: cl(p * 3) * (1 - out3) }); const q = P(t, tC(i), .3); im.style.opacity = q; im.style.transform = `scale(${.6 + .4 * eoBack(q)})`; w.style.borderColor = q >= 1 ? 'var(--green)' : '#E4E1F3'; });
    // a4
    const b = P(t, a4.start + .2, .5); put(big, { y: (1 - eoBack(b)) * 160 + Math.sin(t * 1.7) * 12 * b, r: Math.sin(t * 1.1) * 1.5 * b, s: (.7 + .3 * eoBack(b)) * (1 + .02 * Math.sin(t * 3)), op: cl(b * 3) });
    const bs = P(t, a4.start + .6, .45); put(bigS, { y: (1 - eoBack(bs)) * 90 + Math.sin(t * 1.5 + 1) * 8 * bs, op: cl(bs * 2.4) });
  };
});

/* ----- 3 — l'anatomie du skill : cinq pièces (vrais fichiers) ----- */
scene('anatomie', ['Un skill, cinq pièces', 'Ta voix', 'Ton style', 'Une fabrique par réseau', 'Direction artistique', 'Le contrôle', 'SKILL_VOIX_REFLEXIA.md', 'SKILL_STYLE_ECRITURE.md', 'SKILL_POST_LINKEDIN · X · CARROUSEL', 'SKILL_DIRECTION_ARTISTIQUE.md', 'content-qa.mjs'], (root, m) => {
  const n1 = S(m, 'n1'), D = dv(n1);
  const c = circle(root, 'rgba(255,193,7,.20)', -300, 1180, 820);
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Un skill, cinq pièces', a: n1.start + .1 }], 84, 304, 846, 150);
  const PIECES = [['Ta voix', 'SKILL_VOIX_REFLEXIA.md', '#6C5CE7'], ['Ton style', 'SKILL_STYLE_ECRITURE.md', '#E84393'], ['Une fabrique par réseau', 'SKILL_POST_LINKEDIN · X · CARROUSEL', '#3B8BD4'], ['Direction artistique', 'SKILL_DIRECTION_ARTISTIQUE.md', '#F2994A'], ['Le contrôle', 'content-qa.mjs', '#19A974']];
  const cards = PIECES.map(([n, f, col], i) => { const e = mk(root, 'abs lay', `<div class="dot" style="position:absolute;left:30px;top:34px;width:84px;height:84px;border-radius:24px;background:${col}"></div><div class="tx nm" style="left:140px;top:28px;font-size:52px">${n}</div><div class="tx sb" style="left:142px;top:96px;font:700 26px/1.1 var(--mono);color:#5A5B75;white-space:nowrap">${f}</div>`); place(e, 84, 590 + i * 172, 846, 152); return e; });
  const TT = [.12, .3, .48, .66, .84].map(k => n1.start + D * k);
  ev('whoosh', m.start + .3, { dur: .5 }); TT.forEach((t, i) => { ev('pop', t); ev('tick', t + .1, { f: 2000 + i * 150 }); }); ev('ding', TT[4] + .5, { f: 1174 });
  return t => {
    drift(c, t, 1.6); lab(t);
    cards.forEach((e, i) => { const p = P(t, TT[i] - .15, .45), k = eoBack(p), lit = t >= TT[i]; put(e, { x: (i % 2 ? 1 : -1) * 120 * (1 - k) + Math.sin(t * 1.2 + i) * 4 * p, y: Math.sin(t * 1.6 + i * 1.3) * 6 * p, s: (.94 + .06 * k) * (lit && t < TT[i] + .5 ? 1 + .04 * Math.sin(P(t, TT[i], .5) * Math.PI) : 1), op: cl(p * 2.4) }); e.style.borderColor = lit ? 'var(--violet)' : 'transparent'; });
  };
});

/* ----- 4 — ce que ça t'apporte : ta voix, rien d'inventé, un style à chaque fois, toi tu valides ----- */
scene('apports', ['Ça sonne comme toi', 'Rien d’inventé', 'Un style à chaque carrousel', 'Toi, tu valides', 'Chiffre absent de la fiche : refusé', 'Relire', 'Valider', 'Publier', '✓ Relire', '✓ Valider', '✓ Publier'], (root, m) => {
  const r1 = S(m, 'r1'), r2 = S(m, 'r2'), r3 = S(m, 'r3'), r4 = S(m, 'r4');
  const c = circle(root, 'rgba(108,92,231,.12)', -300, 1180, 820);
  // (r1) le vrai post LinkedIn : le début ressort
  const LL = lyr(root); cardImg(LL.cv, 'linkedin', 40, 600);
  const popL = makePops(LL.cv, CARD('linkedin'), CM.linkedin.w, CM.linkedin.h, 40, 600);
  popL.add({ x: 52, y: 600 + 104, w: 976, h: 260 }, r1.start + .7, r2.start - .2, 1.06);
  // (r2) la vraie sortie du contrôle : la ligne verte ressort
  const LT = lyr(root); cardImg(LT.cv, 'term', 40, 640);
  const NL = Object.keys(CM.term.parts).filter(k => k.startsWith('tl-')).length;
  const popT = makePops(LT.cv, CARD('term'), CM.term.w, CM.term.h, 40, 640);
  popT.add(partR('term', 'tl-' + (NL - 1), 40, 640, 10), r2.start + .5, r3.start, 1.1);
  const red = pill(root, 'Chiffre absent de la fiche : refusé', 84, 1330, 846, 110, 'background:#FDECEC;color:#C62828;border:4px solid #E5383B;font-size:40px');
  // (r3) trois carrousels, trois styles
  const STY = ['oc1', 'rf4', 'rf2'];
  const sty = STY.map((k, i) => thumb(root, SL(k), 45 + i * 335, 700, 320, 400, '50% 50%', 18));
  // (r4) relire, valider, publier
  const NB = ['Relire', 'Valider', 'Publier'];
  const btns = NB.map((n, i) => { const e = mk(root, 'abs', null); e.dataset.deco = ''; place(e, 240, 650 + i * 200, 600, 130); e.style.cssText += ';border-radius:999px;background:#fff;border:5px solid var(--violet);box-shadow:0 14px 34px rgba(60,40,140,.2)'; const a = pill(root, n, 240, 650 + i * 200, 600, 130, 'color:var(--violet);font-size:54px'); const b = pill(root, '✓ ' + n, 240, 650 + i * 200, 600, 130, 'color:#fff;font-size:54px;visibility:hidden'); return { e, a, b }; });
  const TB = [0, 1, 2].map(i => r4.start + .4 + i * (dv(r4) * .8 / 3));
  scrim(root, 'mid');
  const lab = swap(root, 'lbl', [{ html: 'Ça sonne comme toi', a: r1.start + .1 }, { html: 'Rien d’inventé', a: r2.start }, { html: 'Un style à chaque carrousel', a: r3.start, fs: 58 }, { html: 'Toi, tu valides', a: r4.start }], 84, 304, 846, 150);
  const cur = makeCursor(root, [{ t: TB[0] - .8, x: 960, y: 1700 }, { t: TB[0], x: 600, y: 650 + 75 }, { t: TB[1], x: 610, y: 850 + 75 }, { t: TB[2], x: 620, y: 1050 + 75 }]);
  const clk = makeClicks(root, cur, TB);
  ev('whoosh', m.start + .3, { dur: .5 }); ev('pop', r1.start + .7); ev('whoosh', r2.start - .1, { dur: .4 }); ev('pop', r2.start + .5); ev('ding', r2.start + .7, { f: 1174 }); ev('pop', r2.start + 1.6);
  STY.forEach((_, i) => ev('pop', r3.start + .2 + i * .25)); TB.forEach((t, i) => { ev('tick', t, { f: 1800 }); ev('ding', t + .1, { f: 988 + i * 180 }); });
  return t => {
    drift(c, t, 1.6); lab(t);
    const l1 = P(t, m.start + .1, .4), o1 = P(t, r2.start - .25, .3);
    LL.w.style.opacity = l1 * (1 - o1); applyScr(LL.cv, camAt([{ t: m.start, x: 540, y: 960, z: 1 }, { t: r2.start, x: 545, y: 1000, z: 1.06 }], t)); popL.upd(t);
    const l2 = P(t, r2.start - .2, .35), o2 = P(t, r3.start - .25, .3);
    LT.w.style.opacity = l2 * (1 - o2); LT.w.style.transform = `translateY(${(1 - eo(l2)) * 120}px)`; applyScr(LT.cv, camAt([{ t: r2.start, x: 540, y: 960, z: 1 }, { t: r3.start, x: 545, y: 975, z: 1.05 }], t)); popT.upd(t);
    const rp = P(t, r2.start + 1.6, .45); put(red, { y: (1 - eoBack(rp)) * 120, op: cl(rp * 2.4) * (1 - o2) });
    const o3 = P(t, r4.start - .25, .3);
    sty.forEach((e, i) => { const p = P(t, r3.start + .2 + i * .25, .5), k = eoBack(p); put(e, { y: (1 - k) * 300 * (i % 2 ? -1 : 1) + Math.sin(t * 1.5 + i) * 7 * p, r: (i - 1) * 4 * k, s: .9 + .1 * k, op: cl(p * 3) * (1 - o3) }); });
    btns.forEach(({ e, a, b }, i) => { const p = P(t, r4.start + i * .1, .4), ok = t >= TB[i]; [e, a, b].forEach(x => put(x, { s: (.7 + .3 * eoBack(p)) * (ok && t < TB[i] + .4 ? 1 + .05 * Math.sin(P(t, TB[i], .4) * Math.PI) : 1), op: cl(p * 3) })); e.style.background = ok ? 'var(--green)' : '#fff'; e.style.borderColor = ok ? 'var(--green)' : 'var(--violet)'; a.style.visibility = ok ? 'hidden' : 'visible'; b.style.visibility = ok ? 'visible' : 'hidden'; });
    cur.upd(t, t > TB[2] + .6 ? Math.max(0, 1 - P(t, TB[2] + .6, .3)) : 1); clk(t);
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

