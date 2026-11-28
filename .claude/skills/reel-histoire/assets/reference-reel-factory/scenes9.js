/* ===== reel n°9 — Reel Factory : faire des reels avec Claude (vrais extraits des reels 1 à 8, vrais avant/après du n°8) ===== */
const SHADOW = '0 24px 60px rgba(0,0,0,.45)';
const pill = (root, text, x, y, w, h, css = '') => { const e = mk(root, 'abs tx', text); place(e, x, y, w, h); e.style.cssText += ';display:flex;align-items:center;justify-content:center;border-radius:999px;font:900 46px/1 var(--font);letter-spacing:-.02em;white-space:nowrap;' + css; return e; };
const thumb = (parent, src, x, y, w, h, pos = '50% 0%', rad = 18) => { const d = mk(parent, 'abs', null); d.dataset.deco = ''; place(d, x, y, w, h); d.style.cssText += `;overflow:hidden;border-radius:${rad}px;box-shadow:${SHADOW};background:#fff`; const i = img(d, src); i.style.cssText += `;display:block;width:100%;height:100%;object-fit:cover;object-position:${pos}`; return d; };

/* ----- un reel qui tourne : extrait réel (15 i/s, 45 images), une seule image changée à chaque instant, décodage attendu par render.cjs ----- */
const PEND = []; window.__wait = () => Promise.all(PEND.splice(0));
const FR = (k, n) => `assets/clips/${k}/${String(n).padStart(2, '0')}.jpg`;
function vid(parent, key, x, y, w, h, rad = 30) {
  const d = mk(parent, 'abs vid', null); d.dataset.deco = ''; place(d, x, y, w, h);
  d.style.cssText += `;overflow:hidden;border-radius:${rad}px;box-shadow:${SHADOW};background:#0B1230;outline:4px solid rgba(255,255,255,.14);outline-offset:-2px`;
  const i = img(d, FR(key, 1)); i.style.cssText += ';display:block;width:100%;height:100%;object-fit:cover';
  let cur = FR(key, 1), k = key;
  const set = (t, t0 = 0, key2) => { if (key2) k = key2; const n = 1 + (Math.floor(Math.max(0, t - t0) * 15) % 45); const s = FR(k, n); if (s !== cur) { cur = s; i.src = s; PEND.push(i.decode().catch(() => {})); } };
  return { el: d, set };
}
const REELS = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8'];

/* ----- logo Claude en 3D léger ----- */
function claude3D(root, x, y, size) {
  const wrap = mk(root, 'abs', null); wrap.dataset.deco = ''; place(wrap, x - size / 2, y - size / 2, size, size); wrap.style.perspective = '900px';
  const body = mk(wrap, 'abs', null); place(body, 0, 0, size, size); body.style.transformStyle = 'preserve-3d';
  for (let k = 7; k >= 0; k--) { const i = img(body, 'assets/claude.png'); i.style.cssText += `;position:absolute;left:0;top:0;width:${size}px;height:${size}px;transform:translateZ(${-k * 3.2}px);filter:${k ? `brightness(${.55 + .03 * (7 - k)})` : 'drop-shadow(0 18px 22px rgba(120,50,20,.35))'}`; }
  return (t, p, extra = {}) => { put(wrap, Object.assign({ s: .4 + .6 * eoBack(p), op: cl(p * 3) }, extra)); body.style.transform = `rotateY(${Math.sin(t * 1.3) * 20}deg) rotateX(${10 + Math.sin(t * .9) * 6}deg) rotateZ(${Math.sin(t * .7) * 4}deg)`; };
}

/* ----- 1 — hook : un mur de vrais reels qui tournent… puis le casse-tête ----- */
scene('hook', ['Les reels accrochent', 'Mais c’est un casse-tête'], (root, m) => {
  const s1 = S(m, 's1'), D = dv(s1), tMais = s1.start + D * .5;
  const lab = swap(root, 'lbl', [{ html: 'Les reels accrochent', a: s1.start + .05 }, { html: 'Mais c’est un casse-tête', a: tMais, fs: 60 }], 84, 304, 846, 150);
  const wall = mk(root, 'abs', null); wall.dataset.deco = ''; place(wall, -60, 520, 1200, 1500); wall.style.transformOrigin = '50% 30%';
  const CW = 340, CH = 604, G = 18, COLS = [['r1', 'r4', 'r7', 'r2'], ['r5', 'r8', 'r3', 'r6'], ['r6', 'r2', 'r8', 'r4']];
  const cols = COLS.map((ks, c) => ks.map((k, j) => ({ v: vid(wall, k, 60 + c * (CW + G), j * (CH + G), CW, CH, 28), c, j })));
  scrim(root, 'mid');
  ev('thump', m.start + .2, { amp: .7 }); ev('whoosh', m.start + .15, { dur: .5, up: true }); ev('thump', tMais + .4, { amp: .9 }); ev('tick', tMais + .45, { f: 1500 });
  return t => {
    lab(t);
    const shake = P(t, tMais + .35, .1) * (1 - P(t, tMais + .9, .4));
    put(wall, { x: Math.sin(t * 61) * 14 * shake, y: Math.cos(t * 53) * 10 * shake, r: -5 + Math.sin(t * 47) * 1.5 * shake, s: 1 + .04 * shake });
    wall.style.filter = `saturate(${1 - .65 * P(t, tMais + .3, .4)}) brightness(${1 - .25 * P(t, tMais + .3, .4)})`;
    cols.forEach(col => col.forEach(({ v, c, j }) => { const sp = (c % 2 ? 1 : -1) * 55; const off = ((t * sp) % (CH + G) + (CH + G)) % (CH + G); const p = P(t, m.start + .1 + c * .1 + j * .05, .5);
      put(v.el, { y: off - (CH + G) * .5 + (1 - eoBack(p)) * 260, op: cl(p * 3) }); v.set(t, m.start - c * .7 - j * .4); }));
  };
});

/* ----- 2 — le fond, puis la forme ----- */
scene('craft', ['Du fond', 'sinon on décroche', 'Et de la forme', 'Effets', 'Transitions', 'Script'], (root, m) => {
  const s2 = S(m, 's2'), s3 = S(m, 's3'), D3 = dv(s3);
  const lab = swap(root, 'lbl', [{ html: 'Du fond', a: s2.start + .05 }, { html: 'Et de la forme', a: s3.start }], 84, 304, 846, 150);
  const sub = swap(root, 'sublbl', [{ html: 'sinon on décroche', a: s2.start + dv(s2) * .45, b: s3.start - .3 }], 84, 466, 846, 40);
  const tSwipe = s2.start + dv(s2) * .62;
  const A = vid(root, 'r5', 240, 580, 600, 1066, 34);
  const B = vid(root, 'r7', 320, 580, 440, 782, 30);
  const swp = makeVSwipe(root, tSwipe, tSwipe + .45, 540, 1500, 900);
  const NM = ['Effets', 'Transitions', 'Script'], XS = [[84, 230], [330, 330], [676, 254]];
  const TC = [s3.start + D3 * .22, s3.start + D3 * .45, s3.start + D3 * .78];
  const chips = NM.map((n, i) => pill(root, n, XS[i][0], 1400, XS[i][1], 110, 'background:#fff;color:var(--ink);font-size:44px;box-shadow:0 14px 30px rgba(0,0,0,.35)'));
  const rip = mk(root, 'abs rip', null); rip.dataset.deco = ''; rip.style.zIndex = 49;
  const sheet = mk(root, 'abs', '<i></i><i></i><i></i><i></i><i></i><i></i>'); sheet.dataset.deco = ''; place(sheet, 340, 760, 400, 420);
  sheet.style.cssText += ';background:#fff;border-radius:22px;box-shadow:0 30px 70px rgba(0,0,0,.5);padding:40px 34px;display:flex;flex-direction:column;gap:22px';
  [...sheet.children].forEach((b, i) => b.style.cssText = `display:block;height:26px;border-radius:13px;background:${i === 2 ? 'var(--yellow)' : '#E4E1F3'};width:${[100, 86, 94, 70, 90, 60][i]}%`);
  scrim(root, 'mid');
  ev('whoosh', tSwipe, { dur: .4, up: true }); TC.forEach((t, i) => { ev('pop', t); ev('tick', t + .05, { f: 1800 + i * 200 }); }); ev('whoosh', TC[1] + .05, { dur: .35 });
  return t => {
    lab(t); sub(t); swp(t);
    const pa = P(t, m.start + .05, .45), gone = io(P(t, tSwipe + .1, .45));
    put(A.el, { y: (1 - eoBack(pa)) * 200 - gone * 1500 + Math.sin(t * 1.4) * 6, s: .92 + .08 * eoBack(pa), op: cl(pa * 3) * (1 - P(t, tSwipe + .45, .1)) }); A.set(t, m.start);
    const pb = P(t, s3.start - .1, .45), punch = Math.sin(P(t, TC[0], .35) * Math.PI), whip = P(t, TC[1], .3), dim = P(t, TC[2], .3);
    const wx = whip > 0 && whip < 1 ? (whip < .5 ? -whip * 2 * 700 : (1 - whip) * 2 * 700) : 0;
    put(B.el, { x: wx, y: (1 - eoBack(pb)) * 300 + Math.sin(t * 1.3) * 6, s: (.9 + .1 * eoBack(pb)) * (1 + .08 * punch), r: wx / 120, op: cl(pb * 3) });
    B.set(t, s3.start, t >= TC[1] + .15 ? 'r3' : 'r7'); B.el.style.filter = `brightness(${1 - .35 * dim})`;
    { const p = P(t, TC[0] + .05, .6); rip.style.opacity = p > 0 && p < 1 ? .95 * (1 - p) : 0; rip.style.transform = `translate(${540 - 60}px,${960 - 60}px) scale(${.3 + 1.6 * eo(p)})`; }
    { const p = P(t, TC[2] + .05, .45); put(sheet, { y: (1 - eoBack(p)) * 500, r: -3 * p, op: cl(p * 3) }); }
    chips.forEach((e, i) => { const p = P(t, TC[i], .4), on = t >= TC[i] && (i === 2 || t < TC[i + 1]); put(e, { y: (1 - eoBack(p)) * 80, s: on ? 1.08 : 1, op: cl(p * 3) }); e.style.background = on ? 'var(--violet)' : '#fff'; e.style.color = on ? '#fff' : 'var(--ink)'; });
  };
});

/* ----- 3 — Claude fait le montage : script, images, effets, voix ----- */
scene('claude', ['Claude fait le montage', 'Il fait tout le reste', 'Le script', 'Les images', 'Les effets', 'La voix'], (root, m) => {
  const s4 = S(m, 's4'), s5 = S(m, 's5'), D5 = dv(s5), tClaude = s4.start + dv(s4) * .62;
  const lab = swap(root, 'lbl', [{ html: 'Claude fait le montage', a: s4.start + .05 }, { html: 'Il fait tout le reste', a: s5.start }], 84, 304, 846, 150);
  const logo = claude3D(root, 540, 1040, 420);
  const orbit = REELS.map(k => vid(root, k, 0, 0, 170, 302, 18));
  const CX = [84, 546], CY = [600, 1080], CWd = 384, CHt = 440;
  const NM = ['Le script', 'Les images', 'Les effets', 'La voix'], TC = [.08, .3, .55, .78].map(f => s5.start + D5 * f);
  const cards = NM.map((n, i) => { const e = mk(root, 'abs', null); place(e, CX[i % 2], CY[i >> 1], CWd, CHt); e.style.cssText += ';border-radius:30px;background:rgba(255,255,255,.96);box-shadow:0 30px 70px rgba(0,0,0,.45);overflow:hidden';
    const tt = mk(e, 'abs tx', n); place(tt, 28, 22, 330, 60); tt.style.cssText += ';font:900 46px/60px var(--font);letter-spacing:-.02em;color:var(--ink)'; return e; });
  // script : vraies lignes de story.json (décor)
  const code = mk(cards[0], 'abs tx', '<span style="color:#6C5CE7">"voice"</span>: "Il faut du fond…"<br><span style="color:#6C5CE7">"voice"</span>: "Et de la forme…"<br><span style="color:#6C5CE7">"voice"</span>: "Toi, tu valides…"'); code.dataset.deco = ''; place(code, 28, 110, 340, 300);
  code.style.cssText += ';font:600 22px/1.9 var(--mono);color:#1B1C2E;white-space:nowrap;overflow:hidden';
  const imgs = ['assets/oc1.jpg', 'assets/rf4.jpg', 'assets/rf2.jpg'].map((s, i) => thumb(cards[1], s, 40 + i * 92, 110 + i * 18, 190, 238, '50% 50%', 14));
  const fx = vid(cards[2], 'r5', 92, 100, 200, 320, 16); const fxr = mk(cards[2], 'abs rip', null); fxr.dataset.deco = '';
  const bars = Array.from({ length: 24 }, (_, i) => { const b = mk(cards[3], 'abs', null); b.dataset.deco = ''; place(b, 30 + i * 13.5, 200, 8, 120); b.style.cssText += ';border-radius:4px;background:var(--violet);transform-origin:50% 50%'; return b; });
  scrim(root, 'mid');
  ev('pop', tClaude); ev('ding', tClaude + .2, { f: 1174 }); TC.forEach((t, i) => { ev('pop', t); ev('tick', t + .04, { f: 2000 + i * 150 }); }); ev('whoosh', s5.start - .2, { dur: .4 });
  return t => {
    lab(t);
    const out = P(t, s5.start - .25, .35);
    logo(t, P(t, tClaude - .15, .55), { op: cl(P(t, tClaude - .15, .55) * 3) * (1 - out), y: Math.sin(t * 1.2) * 10 });
    orbit.forEach((v, i) => { const p = P(t, s4.start + .1 + i * .08, .5), a = i / 8 * Math.PI * 2 + t * .55, R = 360 + 30 * Math.sin(t + i);
      put(v.el, { x: 540 + Math.cos(a) * R - 85, y: 1040 + Math.sin(a) * R * 1.15 - 151, r: Math.sin(a) * 8, s: (.5 + .5 * eoBack(p)) * (1 - .5 * out), op: cl(p * 3) * (1 - out) }); v.set(t, s4.start - i * .5); });
    cards.forEach((e, i) => { const p = P(t, TC[i], .45); put(e, { y: (1 - eoBack(p)) * 260 + Math.sin(t * 1.4 + i) * 5 * p, r: (1 - p) * (i % 2 ? 6 : -6), s: .85 + .15 * eoBack(p), op: cl(p * 3) }); });
    imgs.forEach((e, i) => { const p = P(t, TC[1] + .1 + i * .15, .4); put(e, { y: (1 - eoBack(p)) * 120, r: (i - 1) * 6 * p, op: cl(p * 3) }); });
    fx.set(t, TC[2]); { const p = P(t, TC[2] + .5, .6); fxr.style.opacity = p > 0 && p < 1 ? .95 * (1 - p) : 0; fxr.style.transform = `translate(${192 - 60}px,${260 - 60}px) scale(${.3 + 1.2 * eo(p)})`; }
    bars.forEach((b, i) => { const on = P(t, TC[3], .3); const h = .15 + .85 * Math.abs(Math.sin(t * 9 + i * 1.7) * Math.sin(t * 3.1 + i * .6)); b.style.transform = `scaleY(${(.1 + .9 * h) * on})`; });
  };
});

/* ----- 4 — toi, tu valides le texte ----- */
scene('valide', ['Toi, tu valides le texte', 'c’est tout', 'Valider', '✓ Validé', 'TEXTE_A_VALIDER.md'], (root, m) => {
  const s6 = S(m, 's6'), D = dv(s6), tClick = s6.start + D * .42;
  const lab = swap(root, 'lbl', [{ html: 'Toi, tu valides le texte', a: s6.start + .05 }], 84, 304, 846, 150);
  const sub = swap(root, 'sublbl', [{ html: 'c’est tout', a: s6.start + D * .66, b: m.end + 1 }], 84, 466, 846, 40);
  const doc = mk(root, 'abs', null); place(doc, 84, 580, 846, 600); doc.style.cssText += ';border-radius:30px;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.5);overflow:hidden';
  const hd = mk(doc, 'abs tx', 'TEXTE_A_VALIDER.md'); place(hd, 0, 0, 846, 84); hd.style.cssText += ';background:#F4F2FC;border-bottom:2px solid #E4E1F3;padding:0 34px;display:flex;align-items:center;font:700 30px/1 var(--mono);color:#5A5B75';
  const body = mk(doc, 'abs tx', '1. Les reels, c’est ce qui accroche le plus…<br>2. Il faut du fond, sinon on décroche.<br>3. Et de la forme : des effets…<br>4. Moi, je ne fais plus le montage.<br>5. Il écrit le script, choisit les images…'); body.dataset.deco = '';
  place(body, 34, 112, 780, 460); body.style.cssText += ';font:600 31px/1.75 var(--font);color:#1B1C2E;white-space:nowrap;overflow:hidden';
  const btn = mk(root, 'abs', null); btn.dataset.deco = ''; place(btn, 160, 1260, 760, 170); btn.style.cssText += ';border-radius:999px;background:#fff;border:6px solid var(--green);box-shadow:0 18px 40px rgba(0,0,0,.4)';
  const bA = pill(root, 'Valider', 160, 1260, 760, 170, 'color:var(--green);font-size:72px'), bB = pill(root, '✓ Validé', 160, 1260, 760, 170, 'color:#fff;font-size:72px;visibility:hidden');
  const cur = makeCursor(root, [{ t: tClick - .9, x: 960, y: 1800 }, { t: tClick, x: 600, y: 1350 }]); const clk = makeClicks(root, cur, [tClick]);
  scrim(root, 'mid');
  ev('whoosh', m.start + .2, { dur: .45 }); ev('tick', tClick, { f: 1800 }); ev('ding', tClick + .1, { f: 1318 }); ev('ding', tClick + .3, { f: 1760 });
  return t => {
    lab(t); sub(t);
    const p = P(t, m.start + .05, .5); put(doc, { y: (1 - eoBack(p)) * 300 + Math.sin(t * 1.3) * 6, s: .92 + .08 * eoBack(p), op: cl(p * 3) });
    const q = P(t, m.start + .35, .45), ok = t >= tClick, b = ok ? Math.sin(P(t, tClick, .4) * Math.PI) : 0;
    [btn, bA, bB].forEach(x => put(x, { y: (1 - eoBack(q)) * 160, s: (.8 + .2 * eoBack(q)) * (1 + .08 * b), op: cl(q * 3) }));
    btn.style.background = ok ? 'var(--green)' : '#fff'; bA.style.visibility = ok ? 'hidden' : 'visible'; bB.style.visibility = ok ? 'visible' : 'hidden';
    cur.upd(t, t > tClick + .6 ? Math.max(0, 1 - P(t, tClick + .6, .3)) : 1); clk(t);
  };
});

/* ----- 5 — tu le dis, il refait : deux vrais avant/après (reel n°8) ----- */
scene('refait', ['Tu le dis, il refait', 'Fond trop sombre ?', 'Titre illisible ?', 'Une phrase, corrigé', 'avant', 'après', 'Refais la couverture, qu’on voie bien le titre', 'C’est refait.'], (root, m) => {
  const s7 = S(m, 's7'), s8 = S(m, 's8'), D8 = dv(s8);
  const tF0 = s8.start, tFw = s8.start + D8 * .24, tT0 = s8.start + D8 * .38, tTw = s8.start + D8 * .6, tFix = s8.start + D8 * .74;
  const lab = swap(root, 'lbl', [{ html: 'Tu le dis, il refait', a: s7.start + .05 }, { html: 'Fond trop sombre ?', a: tF0 }, { html: 'Titre illisible ?', a: tT0 }, { html: 'Une phrase, corrigé', a: tFix }], 84, 304, 846, 150);
  // s7 : la vraie demande de Hari, puis la réponse
  const me = mk(root, 'abs tx', 'Refais la couverture, qu’on voie bien le titre'); place(me, 230, 640, 700, 190); me.style.cssText += ';border-radius:40px 40px 10px 40px;background:var(--violet);color:#fff;font:800 46px/1.25 var(--font);padding:28px 36px;box-shadow:0 20px 50px rgba(0,0,0,.4)';
  const dots = mk(root, 'abs', '<i></i><i></i><i></i>'); dots.dataset.deco = ''; place(dots, 84, 900, 200, 100); dots.style.cssText += ';border-radius:40px 40px 40px 10px;background:#fff;display:flex;align-items:center;justify-content:center;gap:16px';
  [...dots.children].forEach(d => d.style.cssText = 'display:block;width:20px;height:20px;border-radius:50%;background:#9A9BB0');
  const re = mk(root, 'abs tx', 'C’est refait.'); place(re, 84, 900, 420, 100); re.style.cssText += ';border-radius:40px 40px 40px 10px;background:#fff;color:var(--ink);font:800 46px/100px var(--font);padding:0 36px;white-space:nowrap';
  const cv = claude3D(root, 760, 1250, 220);
  const tReply = s7.start + dv(s7) * .62;
  // s8 : avant / après (balayage)
  const BW = 495, BH = 880, BX = 293, BY = 575;
  const frame = mk(root, 'abs', null); frame.dataset.deco = ''; place(frame, BX, BY, BW, BH); frame.style.cssText += `;border-radius:34px;overflow:hidden;box-shadow:${SHADOW};outline:4px solid rgba(255,255,255,.14);outline-offset:-2px`;
  const L = k => { const i = img(frame, 'assets/ba/' + k + '.jpg'); i.style.cssText += ';position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover'; return i; };
  const fA = L('fond-avant'), fB = L('fond-apres'), cA = L('cover-avant'), cB = L('cover-apres');
  const bar = mk(frame, 'abs', null); place(bar, 0, 0, 8, BH); bar.style.cssText += ';background:#fff;box-shadow:0 0 30px rgba(255,255,255,.8)';
  const tagA = pill(root, 'avant', 300, 1470, 170, 64, 'background:rgba(255,255,255,.14);color:#fff;font-size:34px'), tagB = pill(root, 'après', 610, 1470, 170, 64, 'background:var(--yellow);color:var(--ink);font-size:34px');
  scrim(root, 'mid');
  ev('pop', s7.start + .3); ev('tick', s7.start + .3, { f: 2200 }); ev('pop', tReply); ev('ding', tReply + .1, { f: 1318 });
  ev('whoosh', tF0 - .1, { dur: .4, up: true }); ev('whoosh', tFw, { dur: .45 }); ev('pop', tT0); ev('whoosh', tTw, { dur: .45 }); ev('ding', tFix + .1, { f: 1568 });
  return t => {
    lab(t);
    const o7 = P(t, s8.start - .3, .3);
    { const p = P(t, s7.start + .2, .45); put(me, { x: (1 - eoBack(p)) * 300, s: .9 + .1 * eoBack(p), op: cl(p * 3) * (1 - o7) }); }
    { const p = P(t, s7.start + .8, .3), q = P(t, tReply, .2); put(dots, { y: (1 - eoBack(p)) * 60, op: cl(p * 3) * (1 - q) * (1 - o7) }); [...dots.children].forEach((d, i) => d.style.transform = `translateY(${Math.sin(t * 10 - i) * 6}px)`);
      put(re, { s: .85 + .15 * eoBack(P(t, tReply, .4)), op: cl(P(t, tReply, .3) * 3) * (1 - o7) }); }
    cv(t, P(t, s7.start + .5, .5), { op: cl(P(t, s7.start + .5, .5) * 3) * (1 - o7), y: Math.sin(t * 1.3) * 8 });
    const pf = P(t, s8.start - .15, .45); put(frame, { y: (1 - eoBack(pf)) * 400 + Math.sin(t * 1.2) * 5, s: .9 + .1 * eoBack(pf), op: cl(pf * 3) });
    const isCover = t >= tT0, w = isCover ? io(P(t, tTw, .55)) : io(P(t, tFw, .55));
    fA.style.display = fB.style.display = isCover ? 'none' : 'block'; cA.style.display = cB.style.display = isCover ? 'block' : 'none';
    (isCover ? cB : fB).style.clipPath = `inset(0 ${(1 - w) * 100}% 0 0)`;
    bar.style.opacity = w > 0 && w < 1 ? 1 : 0; bar.style.transform = `translateX(${w * BW - 4}px)`;
    if (t >= tT0 && t < tT0 + .3) put(frame, { y: Math.sin(t * 1.2) * 5, s: 1 + .04 * Math.sin(P(t, tT0, .3) * Math.PI), op: 1 });
    const sw = isCover ? P(t, tTw, .55) : P(t, tFw, .55), done = sw >= 1;
    put(tagA, { op: cl(pf * 3) * (done ? .35 : 1) }); put(tagB, { s: done ? 1.06 : 1, op: cl(pf * 3) * (done ? 1 : .35) });
  };
});

/* ----- 6 — un système : réglé une fois ----- */
scene('systeme', ['Un système, réglé une fois', 'Ta charte', 'Ton ton', 'Tes effets', 'copain', 'clic', 'zoom', 'swipe', 'Aa'], (root, m) => {
  const s9 = S(m, 's9'), s10 = S(m, 's10'), D10 = dv(s10);
  const lab = swap(root, 'lbl', [{ html: 'Un système, réglé une fois', a: s9.start + .05, fs: 60 }], 84, 304, 846, 150);
  const ROWS = [['Ta charte', 'var(--yellow)'], ['Ton ton', 'var(--violet)'], ['Tes effets', '#E84393']], TL = [.1, .4, .68].map(f => s10.start + D10 * f);
  const rows = ROWS.map(([n, col], i) => { const e = mk(root, 'abs', null); place(e, 84, 600 + i * 300, 846, 270); e.style.cssText += ';border-radius:34px;background:rgba(255,255,255,.96);box-shadow:0 26px 60px rgba(0,0,0,.4);border:6px solid transparent';
    const tt = mk(e, 'abs tx', n); place(tt, 40, 30, 500, 70); tt.style.cssText += ';font:900 60px/70px var(--font);letter-spacing:-.03em;color:var(--ink)';
    const lk = mk(e, 'abs', ICON.check()); lk.dataset.deco = ''; place(lk, 720, 30, 80, 80); lk.style.cssText += ';border-radius:50%;background:var(--green);padding:16px'; return { e, lk }; });
  const sw = ['var(--yellow)', 'var(--violet)', 'var(--red)', 'var(--green)', '#0F1020'].map((c, i) => { const d = mk(rows[0].e, 'abs', null); d.dataset.deco = ''; place(d, 40 + i * 104, 140, 84, 84); d.style.cssText += `;border-radius:50%;background:${c};box-shadow:0 6px 14px rgba(0,0,0,.18)`; return d; });
  const aa = mk(rows[0].e, 'abs tx', 'Aa'); place(aa, 600, 128, 160, 110); aa.style.cssText += ';font:900 96px/110px var(--font);color:var(--ink);letter-spacing:-.04em';
  const tone = pill(rows[1].e, 'copain', 40, 140, 280, 90, 'background:var(--violet);color:#fff;font-size:44px'); tone.style.position = 'absolute';
  const FX = ['clic', 'zoom', 'swipe'].map((n, i) => { const e = pill(rows[2].e, n, 40 + i * 230, 140, 210, 90, 'background:#F1EFFD;color:var(--ink);font-size:44px'); e.style.position = 'absolute'; return e; });
  scrim(root, 'mid');
  ev('whoosh', m.start + .2, { dur: .45 }); [0, 1, 2].forEach(i => ev('pop', s9.start + .4 + i * .3)); TL.forEach((t, i) => { ev('tick', t, { f: 1700 + i * 200 }); ev('ding', t + .08, { f: 1174 + i * 200 }); });
  return t => {
    lab(t);
    rows.forEach(({ e, lk }, i) => { const p = P(t, s9.start + .4 + i * .3, .45), on = t >= TL[i], q = P(t, TL[i], .35);
      put(e, { x: (i % 2 ? 1 : -1) * 200 * (1 - eoBack(p)), y: Math.sin(t * 1.4 + i) * 5 * p, s: 1 + .04 * Math.sin(q * Math.PI), op: cl(p * 3) });
      e.style.borderColor = on ? 'var(--green)' : 'transparent'; put(lk, { s: .3 + .7 * eoBack(q), op: cl(q * 3) }); });
    sw.forEach((d, i) => put(d, { y: Math.sin(t * 2 + i) * 5, s: 1 })); FX.forEach((e, i) => { const k = Math.floor(t * 1.6) % 3 === i; e.style.background = k ? 'var(--ink)' : '#F1EFFD'; e.style.color = k ? '#fff' : 'var(--ink)'; });
  };
});

/* ----- 7 — « fais-moi une nouvelle vidéo » : la demande, et le reel qui sort ----- */
scene('nouvelle', ['Tu demandes, ça sort', 'En vingt minutes', 'hors retouches', 'Fais-moi une nouvelle vidéo'], (root, m) => {
  const s11 = S(m, 's11'), D = dv(s11), t20 = s11.start + D * .66;
  const lab = swap(root, 'lbl', [{ html: 'Tu demandes, ça sort', a: s11.start + .05 }, { html: 'En vingt minutes', a: t20 }], 84, 304, 846, 150);
  const sub = swap(root, 'sublbl', [{ html: 'hors retouches', a: t20 + .4, b: m.end + 1 }], 84, 466, 846, 40);
  const cm = mk(root, 'abs cm', '<div class="av"></div><div class="tx ty" style="font-size:46px;line-height:1.1;letter-spacing:-.02em;right:150px;white-space:normal"></div><div class="snd">' + ICON.send() + '</div>'); place(cm, 84, 580, 846, 170);
  const ty = cm.querySelector('.ty'), snd = cm.querySelector('.snd');
  const PH = 'Fais-moi une nouvelle vidéo', typeAt = s11.start + .35, ST = .045, tSend = typeAt + PH.length * ST + .15;
  const out = vid(root, 'r8', 300, 800, 480, 853, 30);
  const glow = mk(root, 'abs', null); glow.dataset.deco = ''; place(glow, 200, 760, 680, 940); glow.style.cssText += ';border-radius:60px;background:radial-gradient(closest-side,rgba(255,217,59,.35),rgba(255,217,59,0))';
  scrim(root, 'mid');
  for (let i = 0; i < PH.length; i += 2) ev('tick', typeAt + i * ST, { f: 2600 + i * 25 }); ev('pop', tSend); ev('whoosh', tSend + .2, { dur: .5, up: true }); ev('ding', tSend + .6, { f: 1568 }); ev('pop', t20);
  return t => {
    lab(t); sub(t);
    const p = P(t, m.start + .05, .45); put(cm, { y: (1 - eoBack(p)) * 200, op: cl(p * 3) });
    ty.textContent = PH.slice(0, Math.floor(cl((t - typeAt) / ST, 0, PH.length)));
    const sp = P(t, tSend, .3); snd.style.transform = `scale(${1 + .25 * Math.sin(sp * Math.PI)})`; snd.style.background = sp >= 1 ? 'var(--green)' : 'var(--violet)';
    const q = P(t, tSend + .2, .6); put(out.el, { y: (1 - eoBack(q)) * -260 + Math.sin(t * 1.3) * 7, s: .3 + .7 * eoBack(q), r: (1 - q) * -10, op: cl(q * 3) }); out.set(t, tSend);
    put(glow, { s: .8 + .2 * eo(q) + .03 * Math.sin(t * 3), op: cl(q * 2) * .9 });
  };
});

/* ----- 8 — toutes sorties comme ça : montage rapide des vrais reels ----- */
scene('montage', ['Toutes sorties comme ça'], (root, m) => {
  const s12 = S(m, 's12');
  const lab = swap(root, 'lbl', [{ html: 'Toutes sorties comme ça', a: s12.start + .05 }], 84, 304, 846, 150);
  const side = [vid(root, 'r3', -150, 700, 400, 711, 26), vid(root, 'r6', 830, 700, 400, 711, 26)];
  const main = vid(root, 'r1', 230, 580, 620, 1102, 34);
  const flash = mk(root, 'abs', null); flash.dataset.deco = ''; place(flash, 230, 580, 620, 1102); flash.style.cssText += ';border-radius:34px;background:#fff;pointer-events:none';
  const t0 = m.start + .25, CUT = .52, cuts = REELS.map((_, i) => t0 + i * CUT);
  scrim(root, 'mid');
  cuts.forEach((t, i) => { ev('tick', t, { f: 1500 + i * 120 }); if (i % 2) ev('whoosh', t - .05, { dur: .25 }); }); ev('ding', cuts[7] + .5, { f: 1568 });
  return t => {
    lab(t);
    const i = Math.max(0, Math.min(7, Math.floor((t - t0) / CUT))), lp = P(t, cuts[i], CUT);
    const p = P(t, m.start + .05, .4);
    put(main.el, { y: (1 - eoBack(p)) * 300, s: (1.08 - .08 * eo(lp)) * (.9 + .1 * eoBack(p)), r: Math.sin(t * 1.1) * 1.2, op: cl(p * 3) }); main.set(t, cuts[i] - 1, REELS[i]);
    flash.style.opacity = t >= t0 ? .7 * (1 - P(t, cuts[i], .14)) : 0; put(flash, { y: (1 - eoBack(p)) * 300, s: 1.08 - .08 * eo(lp), op: t >= t0 ? .7 * (1 - P(t, cuts[i], .14)) : 0 });
    side.forEach((v, k) => { const q = P(t, m.start + .2 + k * .1, .5); put(v.el, { y: (k ? -1 : 1) * ((t * 40) % 200) + (1 - eoBack(q)) * 300, r: k ? 8 : -8, s: .95, op: cl(q * 3) * .55 }); v.set(t, m.start, REELS[(i + 3 + k * 2) % 8]); });
  };
});

/* ----- 9 — appel : commente « reel » ----- */
scene('cta', ['Commente « reel »', 'reel', 'Tu veux le même système ?'], (root, m) => {
  const k1 = S(m, 'k1');
  const lab = swap(root, 'lbl w', [{ html: 'Commente « <span class="hl" style="margin:0 .12em">reel</span> »', a: k1.start, upd: (e, t) => hlSet(e, P(t, k1.start + .5, .45)) }], 84, 304, 846, 150);
  const th = ['r7', 'r5', 'r8', 'r6', 'r3'].map((k, i) => vid(root, k, 76 + i * 194, 560, 172, 306, 16));
  const cm = mk(root, 'abs cm', '<div class="av"></div><div class="tx ty" style="font-size:96px"></div><div class="snd">' + ICON.send() + '</div>'); place(cm, 84, 960, 846, 210);
  const ty = cm.querySelector('.ty'), snd = cm.querySelector('.snd');
  const tag = txt(root, 'lbl w', 'Tu veux le même système ?', 84, 1260, 846, 220); tag.style.fontSize = '58px';
  const WORD = 'reel', typeAt = k1.start + 1.0, ST = .16;
  ev('whoosh', m.start + .3, { dur: .5 }); th.forEach((_, i) => ev('pop', m.start + .5 + i * .12));
  WORD.split('').forEach((_, i) => ev('tick', typeAt + i * ST, { f: 2600 + i * 70 })); ev('pop', typeAt + WORD.length * ST + .3); ev('ding', typeAt + WORD.length * ST + .4, { f: 1174 }); ev('ding', k1.start + 3.6, { f: 1568 });
  return t => {
    lab(t);
    th.forEach((v, i) => { const dir = i % 2 ? 1 : -1, p = P(t, m.start + .5 + i * .12, .5), k = eoBack(p); put(v.el, { y: dir * 420 * (1 - k) + Math.sin(t * 1.3 + i) * 6 * p, s: .9 + .1 * k, op: cl(p * 3) }); v.set(t, m.start - i * .6); });
    const p = P(t, m.start + .9, .5); put(cm, { y: (1 - eoBack(p)) * 300, s: .94 + .06 * eoBack(p), op: cl(p * 3) });
    ty.textContent = WORD.slice(0, Math.floor(cl((t - typeAt) / ST, 0, WORD.length)));
    const sp = P(t, typeAt + WORD.length * ST + .3, .3); snd.style.transform = `scale(${1 + .25 * Math.sin(sp * Math.PI)})`; snd.style.background = sp >= 1 ? 'var(--green)' : 'var(--violet)';
    const q = P(t, typeAt + WORD.length * ST + .8, .5); put(tag, { y: (1 - eoBack(q)) * 90, op: cl(q * 2.4) });
  };
});
