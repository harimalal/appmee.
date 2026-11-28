/** Capture les rendus de cards.html (échelle 2) dans assets/cards/<id>.png et relève la position des éléments utiles (pixels CSS, relatifs à la carte). */
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const out = path.join(__dirname, 'assets', 'cards'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1400 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'cards.html')); await p.evaluate(() => document.fonts.ready);
  const meta = {};
  for (const id of ['fiche', 'position', 'linkedin', 'x', 'term']) {
    const el = await p.$('#' + id); await el.screenshot({ path: path.join(out, id + '.png') });
    meta[id] = await p.evaluate(id => {
      const c = document.getElementById(id).getBoundingClientRect(); const o = { w: c.width, h: c.height, parts: {} };
      document.getElementById(id).querySelectorAll('[id]').forEach(e => { const r = e.getBoundingClientRect(); o.parts[e.id] = { x: r.left - c.left, y: r.top - c.top, w: r.width, h: r.height }; });
      document.getElementById(id).querySelectorAll('.pp').forEach((e, i) => { const r = e.getBoundingClientRect(); o.parts['pp-' + i] = { x: r.left - c.left, y: r.top - c.top, w: r.width, h: r.height, txt: e.textContent.slice(0, 40) }; });
      return o;
    }, id);
    console.log(id, Math.round(meta[id].w), 'x', Math.round(meta[id].h));
  }
  fs.writeFileSync(path.join(out, 'cards.json'), JSON.stringify(meta, null, 1));
  await b.close();
})();
