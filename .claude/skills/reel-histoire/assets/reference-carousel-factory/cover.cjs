/** Couverture : node cover.cjs  -> out/couverture.png (1080x1920), out/couverture-grille.png (3:4 central, 1080x1440) et out/couverture-carre.png (1:1 central). */
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + path.resolve(__dirname, 'cover.html')); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await p.screenshot({ path: path.join(__dirname, 'out', 'couverture.png') });
  await p.screenshot({ path: path.join(__dirname, 'out', 'couverture-grille.png'), clip: { x: 0, y: 240, width: 1080, height: 1440 } });
  await p.screenshot({ path: path.join(__dirname, 'out', 'couverture-carre.png'), clip: { x: 0, y: 420, width: 1080, height: 1080 } });
  console.log(errs.length ? 'erreurs : ' + errs.join(' | ') : 'aucune erreur'); await b.close();
})();
