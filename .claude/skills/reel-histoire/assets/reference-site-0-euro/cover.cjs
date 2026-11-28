/** Couverture : NODE_PATH=$(npm root -g) node cover.cjs  -> out/couverture.png (1080x1920) et out/couverture-carre.png (recadrage 1:1 central, pour vérifier la grille de profil). */
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + path.resolve(__dirname, 'cover.html')); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(__dirname, 'out', 'couverture.png') });
  await p.screenshot({ path: path.join(__dirname, 'out', 'couverture-carre.png'), clip: { x: 0, y: 420, width: 1080, height: 1080 } });
  // mesure : tout élément de texte dans le carré central ?
  const boxes = await p.evaluate(() => [...document.querySelectorAll('.brand,.win,.ttl,.pill,.sub')].map(e => { const r = e.getBoundingClientRect(); return { c: e.className, y0: Math.round(r.top), y1: Math.round(r.bottom), x0: Math.round(r.left), x1: Math.round(r.right) }; }));
  console.log(errs.length ? 'erreurs : ' + errs.join(' | ') : 'aucune erreur'); console.table(boxes); await b.close();
})();
