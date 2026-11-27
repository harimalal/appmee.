/**
 * Captures de VRAIES pages d'un site pour une scène de défilé (aucune image générée).
 * Prérequis : le site est construit (ex. `npm ci && npm run build`) et servi en local (ex. `cd dist && python3 -m http.server 4399 --bind 127.0.0.1`).
 * Usage : NODE_PATH=$(npm root -g) node capture-pages.cjs <url_de_base> <dossier_sortie> <chemin1> [<chemin2> ...]
 *   ex. node capture-pages.cjs http://127.0.0.1:4399 assets/captures /blog/mon-article/ /blog/un-autre/
 * Sortie : <dossier_sortie>/art1.jpg, art2.jpg… (1080 px de large = page de 540 px en échelle 2, rendu mobile, 4 200 px css de haut au plus).
 * À faire ensuite : OUVRIR chaque image (titre, chapô, corps réels), choisir des pages de structures différentes, dire dans SCRIPT.md qu'elles sont choisies.
 */
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const [base, out, ...pages] = process.argv.slice(2);
if (!base || !out || !pages.length) { console.error('Usage : node capture-pages.cjs <url_de_base> <dossier_sortie> <chemin1> [<chemin2> ...]'); process.exit(1); }
const W = 540, MAXH = 4200;
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: 960 }, deviceScaleFactor: 2 });
  for (let i = 0; i < pages.length; i++) {
    const r = await p.goto(base.replace(/\/$/, '') + pages[i], { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    const h = await p.evaluate(() => document.documentElement.scrollHeight);
    console.log(i + 1, pages[i], 'HTTP', r.status(), '| hauteur css', h, '|', await p.title());
    await p.screenshot({ path: path.join(out, `art${i + 1}.jpg`), type: 'jpeg', quality: 82, fullPage: true, clip: { x: 0, y: 0, width: W, height: Math.min(h, MAXH) } });
  }
  await b.close();
})();
