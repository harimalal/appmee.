/**
 * Captures d'ÉLÉMENTS réels d'une page (tableau, grille de cartes…) pour un reel : aucune image générée.
 * Prérequis : le site est construit et servi en local (ex. `cd dist && python3 -m http.server 4399 --bind 127.0.0.1`).
 * Usage : NODE_PATH=$(npm root -g) node capture-elements.cjs <url_page> <dossier_sortie> <nom>=<sélecteur>[@large] ...
 *   ex. node capture-elements.cjs http://127.0.0.1:4399/blog/mon-comparatif/ assets/captures tableau=.cmp-table@large usages=.cmp-content-grid
 *   - sans « @large » : rendu mobile (540 px de large, échelle 2) ;
 *   - avec « @large » : page à 1 400 px, et tous les ancêtres de l'élément passent en `overflow: visible` (un tableau qui défile
 *     horizontalement est alors capté en entier, toutes les colonnes).
 * Les éléments collants (en-tête, barre de lecture, panneaux latéraux, pop-ups) sont masqués : variable d'environnement HIDE
 * (sélecteurs CSS séparés par des virgules ; défaut adapté au site Reflex IA : `.site-header,.reading-bar,.sidebar,.nlp-overlay`).
 * À faire ensuite : OUVRIR chaque image, vérifier le contenu réel, choisir des exemples qui passent le contrôle de la source
 * (ex. un tableau bien trié), et le dire dans SCRIPT.md.
 */
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const [url, out, ...specs] = process.argv.slice(2);
if (!url || !out || !specs.length) { console.error('Usage : node capture-elements.cjs <url_page> <dossier_sortie> <nom>=<sélecteur>[@large] ...'); process.exit(1); }
const HIDE = (process.env.HIDE || '.site-header,.reading-bar,.sidebar,.nlp-overlay') + '{display:none !important}';
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const spec of specs) {
    const [name, rest] = spec.split(/=(.+)/); const large = rest.endsWith('@large'); const sel = rest.replace(/@large$/, '');
    const p = await b.newPage({ viewport: { width: large ? 1400 : 540, height: 960 }, deviceScaleFactor: 2 });
    await p.goto(url, { waitUntil: 'networkidle' }); await p.addStyleTag({ content: HIDE }); await p.evaluate(() => document.fonts.ready);
    const h = await p.$(sel); if (!h) { console.log(name, 'ABSENT :', sel); await p.close(); continue; }
    if (large) await h.evaluate(t => { const w = t.scrollWidth; let n = t; while (n && n !== document.body) { n.style.overflow = 'visible'; n.style.maxWidth = 'none'; if (n !== t && n.tagName === 'DIV') n.style.width = (w + 40) + 'px'; n = n.parentElement; } t.style.width = w + 'px'; });
    const bb = await h.boundingBox(); console.log(name, Math.round(bb.width) + 'x' + Math.round(bb.height), '(css)');
    await h.screenshot({ path: path.join(out, name + '.png') }); await p.close();
  }
  await b.close();
})();
