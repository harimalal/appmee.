(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const NS = 'http://www.w3.org/2000/svg';
  const f = n => +n.toFixed(1);

  /* ---------- Dessin procédural des planches ---------- */
  // Feuille en forme de fuseau : contour + nervure centrale
  const leaf = (x, y, a, l, w) => {
    const c = Math.cos(a), s = Math.sin(a);
    const p = (u, v) => [x + u * c - v * s, y + u * s + v * c];
    const [ex, ey] = p(l, 0), [ax, ay] = p(l * .5, w), [bx, by] = p(l * .5, -w);
    return [
      `M${f(x)} ${f(y)}Q${f(ax)} ${f(ay)} ${f(ex)} ${f(ey)}Q${f(bx)} ${f(by)} ${f(x)} ${f(y)}Z`,
      `M${f(x)} ${f(y)}L${f(ex)} ${f(ey)}`
    ];
  };
  // Point et angle sur une courbe de Bézier cubique
  const bez = (P, t) => {
    const m = 1 - t;
    const x = m*m*m*P[0] + 3*m*m*t*P[2] + 3*m*t*t*P[4] + t*t*t*P[6];
    const y = m*m*m*P[1] + 3*m*m*t*P[3] + 3*m*t*t*P[5] + t*t*t*P[7];
    const dx = 3*m*m*(P[2]-P[0]) + 6*m*t*(P[4]-P[2]) + 3*t*t*(P[6]-P[4]);
    const dy = 3*m*m*(P[3]-P[1]) + 6*m*t*(P[5]-P[3]) + 3*t*t*(P[7]-P[5]);
    return [x, y, Math.atan2(dy, dx)];
  };
  const stem = P => `M${P[0]} ${P[1]}C${P[2]} ${P[3]} ${P[4]} ${P[5]} ${P[6]} ${P[7]}`;
  const ring = (cx, cy, r) => `M${cx - r} ${cy}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0`;

  const DRAW = {
    fern() {
      const P = [150, 365, 120, 250, 215, 150, 175, 30], out = [{ d: stem(P) }];
      for (let i = 1; i <= 17; i++) {
        const t = .08 + i * .052, [x, y, a] = bez(P, t);
        const l = 12 + 74 * Math.pow(1 - t, .85);
        [-1, 1].forEach(k => leaf(x, y, a + k * 1.15, l, l * .17).forEach((d, j) => out.push({ d, c: j ? 'grn' : '' })));
      }
      return out;
    },
    ginkgo() {
      const out = [{ d: 'M150 372L150 238' }, { d: 'M150 238Q148 290 150 372', c: 'grn' }];
      const pts = [], N = 36;
      for (let i = 0; i <= N; i++) {
        const a = Math.PI * (1.17 - .34 * 0) - Math.PI * 1.34 * (i / N) + Math.PI * .17 * 0;
        const ang = -Math.PI * (.16 + .68 * (1 - i / N)) - 0; // éventail de -29° à -151°
        const r = 150 + (i % 3 === 0 ? 6 : 0) + (i === 18 ? -26 : 0);
        pts.push([150 + r * Math.cos(ang), 238 + r * Math.sin(ang) * .88, ang]);
      }
      out.push({ d: 'M150 238L' + pts.map(p => `${f(p[0])} ${f(p[1])}`).join('L') + 'Z' });
      for (let i = 1; i < N; i += 2) out.push({ d: `M150 238L${f(pts[i][0] * .96 + 6)} ${f(pts[i][1] * .96 + 9)}`, c: 'grn' });
      out.push({ d: 'M150 238Q150 180 150 168', c: 'acc' });
      return out;
    },
    poppy() {
      const P = [150, 372, 120, 300, 180, 240, 150, 168], out = [{ d: stem(P) }];
      [[.35, -1.1, 70], [.55, 1.0, 60]].forEach(([t, k, l]) => {
        const [x, y, a] = bez(P, t); leaf(x, y, a + k, l, 14).forEach((d, j) => out.push({ d, c: j ? 'grn' : '' }));
      });
      for (let i = 0; i < 4; i++) leaf(150, 150, i * Math.PI / 2 + .5, 78, 52).forEach((d, j) => out.push({ d, c: j ? 'grn' : 'acc' }));
      for (let i = 0; i < 4; i++) leaf(150, 150, i * Math.PI / 2 - .2, 52, 30).forEach(d => out.push({ d, c: 'acc' }));
      out.push({ d: ring(150, 150, 8) });
      for (let i = 0; i < 16; i++) { const a = i * Math.PI / 8; out.push({ d: `M${f(150 + 11 * Math.cos(a))} ${f(150 + 11 * Math.sin(a))}L${f(150 + 25 * Math.cos(a))} ${f(150 + 25 * Math.sin(a))}` }); }
      return out;
    },
    thistle() {
      const out = [{ d: 'M150 372C148 320 154 260 150 205' }];
      [[.75, -1.05, 95], [.45, 1.05, 85]].forEach(([t, k, l]) => {
        const y = 372 - t * 100; leaf(150, y, -Math.PI / 2 + k, l, 22).forEach((d, j) => out.push({ d, c: j ? 'grn' : '' }));
      });
      out.push({ d: 'M110 172A40 34 0 0 0 190 172A40 34 0 0 0 110 172Z' });
      for (let r = 0; r < 6; r++) for (let c = 0; c < 6; c++) {
        const x = 118 + c * 12 + (r % 2) * 6, y = 148 + r * 11;
        if (Math.pow((x - 150) / 40, 2) + Math.pow((y - 172) / 34, 2) < .78) out.push({ d: `M${x - 5} ${y}l5 6l5-6`, c: 'grn' });
      }
      for (let i = 0; i < 17; i++) {
        const a = -Math.PI + .2 + (Math.PI - .4) * i / 16, l = 34 + (i % 2) * 14;
        out.push({ d: `M${f(150 + 18 * Math.cos(a))} ${f(146 + 12 * Math.sin(a))}L${f(150 + (18 + l) * Math.cos(a))} ${f(146 + (12 + l) * Math.sin(a))}`, c: 'acc' });
      }
      return out;
    },
    olive() {
      const P = [30, 345, 110, 300, 180, 150, 270, 60], out = [{ d: stem(P) }];
      for (let i = 1; i <= 10; i++) {
        const t = .1 + i * .08, [x, y, a] = bez(P, t), k = i % 2 ? 1 : -1, l = 64 - i * 2.5;
        leaf(x, y, a + k * .85, l, 7).forEach((d, j) => out.push({ d, c: j ? 'grn' : '' }));
      }
      [[.42, 1], [.62, -1], [.78, 1]].forEach(([t, k]) => {
        const [x, y] = bez(P, t); const ox = x + k * 14, oy = y + 26;
        out.push({ d: `M${f(x)} ${f(y)}Q${f(x + k * 8)} ${f(y + 10)} ${f(ox)} ${f(oy - 9)}` });
        out.push({ d: `M${f(ox)} ${f(oy - 9)}a8 11 0 1 0 .1 0Z`, c: 'acc' });
      });
      return out;
    }
  };

  const render = (svg, kind) => {
    svg.classList.remove('draw'); svg.textContent = '';
    DRAW[kind]().forEach((s, i) => {
      const p = document.createElementNS(NS, 'path');
      p.setAttribute('d', s.d); p.setAttribute('pathLength', '1');
      p.setAttribute('class', s.c || 'ink'); p.style.setProperty('--d', (i * .012).toFixed(2) + 's');
      svg.appendChild(p);
    });
    void svg.getBoundingClientRect(); svg.classList.add('draw');
  };

  /* ---------- Spécimens ---------- */
  const SPEC = [
    { kind: 'fern',    name: 'Polypodium',        sub: 'Illustrations éditoriales',  text: 'Des planches pour les livres, magazines et guides de terrain : un trait clair, des légendes soignées, une lecture immédiate.', cap: 'Fougère, encre', notes: ['Format : A4 à A3.', 'Rendu : encre pigmentaire.', 'Délai : 10 jours.'] },
    { kind: 'ginkgo',  name: 'Ginkgo biloba',     sub: 'Identité de marque',         text: 'Un motif botanique devenu emblème : logo, déclinaisons et petite charte pour les marques qui veulent du caractère.', cap: 'Ginkgo, étude de forme', notes: ['Livrables : vectoriel + planches.', 'Usage : tous supports.', 'Délai : 3 semaines.'] },
    { kind: 'poppy',   name: 'Papaver rhoeas',    sub: 'Affiches & estampes',        text: 'Des tirages d\'art et des affiches en série limitée, signés et numérotés, pour la maison ou les lieux accueillant du public.', cap: 'Coquelicot, aquarelle', notes: ['Tirage : 30 exemplaires.', 'Papier chiffon 300 g.', 'Signature et numéro.'] },
    { kind: 'thistle', name: 'Carduus',           sub: 'Étiquettes & emballages',    text: 'Des étiquettes, sachets et coffrets illustrés pour les produits issus de la terre : tisanes, miels, cosmétiques.', cap: 'Chardon, tracé d\'étiquette', notes: ['Fichiers prêts à imprimer.', 'Déclinaisons de gammes.', 'Délai : 2 semaines.'] },
    { kind: 'olive',   name: 'Olea europaea',     sub: 'Fresques murales',           text: 'Des décors peints à grande échelle pour les restaurants, boutiques et salons, dessinés d\'après nature puis agrandis.', cap: 'Olivier, étude', notes: ['Surface : dès 4 m².', 'Peinture minérale.', 'Intervention sur site.'] }
  ];
  const STEP = 60, MAX = 120;               // cadran : 5 positions de -120° à +120°
  let idx = 0;
  const knob = $('#knob'), dial = $('#dial'), ticks = $('#ticks');
  const angOf = i => -MAX + i * STEP;
  for (let i = 0; i < SPEC.length; i++) {
    const a = angOf(i) * Math.PI / 180, g = document.createElementNS(NS, 'g');
    g.setAttribute('class', 'tick'); g.dataset.i = i;
    g.innerHTML = `<line x1="${f(Math.sin(a) * 52)}" y1="${f(-Math.cos(a) * 52)}" x2="${f(Math.sin(a) * 58)}" y2="${f(-Math.cos(a) * 58)}"/><text x="${f(Math.sin(a) * 64)}" y="${f(-Math.cos(a) * 64)}">${i + 1}</text>`;
    ticks.appendChild(g);
  }
  function setSpec(i, animate = true) {
    idx = (i + SPEC.length) % SPEC.length;
    const s = SPEC[idx];
    knob.style.transform = `rotate(${angOf(idx)}deg)`;
    dial.setAttribute('aria-valuenow', idx + 1);
    dial.setAttribute('aria-valuetext', `${s.name}, ${s.sub}`);
    $$('.tick').forEach(t => t.classList.toggle('on', +t.dataset.i === idx));
    $('#sp-title').textContent = s.name; $('#sp-sub').textContent = s.sub; $('#sp-text').textContent = s.text;
    $('#sp-cap').textContent = `fig. 2 — ${s.cap}.`;
    $('#sp-notes').innerHTML = s.notes.map((n, k) => `<p><span>(${k + 1})</span> ${n}</p>`).join('');
    if (animate) render($('#fig-specimen'), s.kind);
  }
  // Rotation à la souris / au doigt
  let dragging = false, moved = false;
  const pointerAngle = e => {
    const r = dial.getBoundingClientRect();
    const a = Math.atan2(e.clientX - (r.left + r.width / 2), -(e.clientY - (r.top + r.height / 2))) * 180 / Math.PI;
    return Math.max(-MAX, Math.min(MAX, a));
  };
  dial.addEventListener('pointerdown', e => { dragging = true; moved = false; dial.setPointerCapture(e.pointerId); knob.classList.add('drag'); });
  dial.addEventListener('pointermove', e => {
    if (!dragging) return; moved = true;
    const a = pointerAngle(e); knob.style.transform = `rotate(${a}deg)`;
    const i = Math.round((a + MAX) / STEP); if (i !== idx) setSpec(i);
  });
  const release = () => { if (!dragging) return; dragging = false; knob.classList.remove('drag'); knob.style.transform = `rotate(${angOf(idx)}deg)`; };
  dial.addEventListener('pointerup', e => {
    const wasTap = !moved; release();
    if (wasTap) { const t = e.target.closest('.tick'); setSpec(t ? +t.dataset.i : idx + 1); }
  });
  dial.addEventListener('pointercancel', release);
  dial.addEventListener('keydown', e => {
    const k = { ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1 }[e.key];
    if (k) { e.preventDefault(); setSpec(Math.max(0, Math.min(SPEC.length - 1, idx + k))); }
  });

  /* ---------- Tiroirs ---------- */
  const drawers = $$('.drawer'), ids = drawers.map(d => d.dataset.panel);
  let current = null;
  function open(id, push) {
    if (!ids.includes(id)) id = 'atelier';
    if (id === current) return;
    current = id;
    drawers.forEach(d => d.setAttribute('aria-expanded', d.dataset.panel === id));
    $$('.panel').forEach(p => { const on = p.id === 'p-' + id; p.hidden = !on; });
    const svg = { atelier: ['#fig-atelier', 'fern'], releves: ['#fig-releves', 'olive'], correspondance: ['#fig-contact', 'poppy'] }[id];
    if (svg) render($(svg[0]), svg[1]); else setSpec(idx);
    if (push) history.pushState(null, '', '#' + id);
    if (push && matchMedia('(max-width:900px)').matches) $('#plate').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  drawers.forEach(d => {
    d.addEventListener('click', () => open(d.dataset.panel, true));
    // Geste de traction : tirer le tiroir vers la droite
    let x0 = null;
    d.addEventListener('pointerdown', e => { x0 = e.clientX; });
    d.addEventListener('pointermove', e => {
      if (x0 === null) return; const dx = e.clientX - x0;
      if (dx > 6) { d.classList.add('pulling'); d.style.transform = `translateX(${Math.min(dx, 34)}px)`; }
    });
    const end = e => {
      if (x0 === null) return; const dx = e.clientX - x0; x0 = null;
      d.classList.remove('pulling'); d.style.transform = '';
      if (dx > 20) open(d.dataset.panel, true);
    };
    d.addEventListener('pointerup', end); d.addEventListener('pointerleave', end); d.addEventListener('pointercancel', end);
  });
  const fromHash = () => open(location.hash.slice(1), false);
  window.addEventListener('popstate', fromHash);
  window.addEventListener('hashchange', fromHash);

  /* ---------- Coordonnées au curseur ---------- */
  const coords = $('#coords'); let raf = 0;
  const dms = (v, pos, neg) => { const h = v >= 0 ? pos : neg; v = Math.abs(v); const d = Math.floor(v); return `${d}°${String(Math.floor((v - d) * 60)).padStart(2, '0')}′ ${h}`; };
  addEventListener('pointermove', e => {
    if (e.pointerType === 'touch' || raf) return;
    raf = requestAnimationFrame(() => {
      raf = 0;
      coords.textContent = `${dms(45.9 - e.clientY / innerHeight * .4, 'N', 'S')} · ${dms(4.6 + e.clientX / innerWidth * .5, 'E', 'W')}`;
    });
  });

  /* ---------- Formulaire ---------- */
  const form = $('#contactForm'), status = $('.status', form);
  form.addEventListener('submit', e => {
    e.preventDefault(); let ok = true;
    $$('input,textarea', form).forEach(el => {
      const bad = !el.value.trim() || (el.type === 'email' && !/^\S+@\S+\.\S+$/.test(el.value));
      el.classList.toggle('err', bad); if (bad) ok = false;
    });
    status.style.color = ok ? 'var(--green)' : '#c0272d';
    status.textContent = ok ? 'Fiche reçue (démo : branchez le formulaire à votre service d’e-mail).' : 'Merci de compléter chaque ligne de la fiche.';
    if (ok) form.reset();
  });

  $('#year').textContent = new Date().getFullYear();
  setSpec(0, false);
  fromHash();
  if (!current) open('atelier', false);
})();
