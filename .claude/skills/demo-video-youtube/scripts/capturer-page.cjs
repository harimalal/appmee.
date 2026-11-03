// Capture pleine page d'un résultat réel (artefact, tableau, app) + positions des encarts,
// pour les slides qui zooment dans la vraie page (data-cam calculées depuis A.geo).
//
// Usage :
//   NODE_PATH=$(npm root -g) node capturer-page.cjs <url-ou-fichier.html> <sortie.jpg> \
//     [--largeur 1720] [--boites boites.json] [--clic "#bouton"] [--attente 1500] [--defiler]
// boites.json : {"chart":"#chart", "angle":".synth .angle", "v":[".vrow:nth-child(1)", ".vrow:nth-child(2)"]}
// Écrit <sortie>.geo.json : chaque clé -> [x, y, largeur, hauteur] en pixels de la capture, et H (hauteur totale).
// Ces coordonnées sont celles de l'image affichée à sa taille (classe .pageimg, 1720 px de large).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [cible, sortie] = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
if (!cible || !sortie) { console.error('usage : capturer-page.cjs <url|fichier> <sortie.jpg> [--largeur 1720] [--boites f.json]'); process.exit(1); }
const largeur = +opt('--largeur', 1720);
const boites = opt('--boites') ? JSON.parse(fs.readFileSync(opt('--boites'), 'utf8')) : {};

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: largeur, height: 1000 }, deviceScaleFactor: 1, colorScheme: 'light' });
  const url = /^https?:/.test(cible) ? cible : 'file://' + path.resolve(cible);
  await p.goto(url, { waitUntil: 'networkidle' });
  if (opt('--clic')) await p.click(opt('--clic'));
  await p.waitForTimeout(+opt('--attente', 1500));
  // --defiler (à mettre en dernier) : parcourt la page pour déclencher les apparitions au défilement
  if (args[args.length - 1] === '--defiler') {
    const h = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < h; y += 400) { await p.evaluate((y) => scrollTo(0, y), y); await p.waitForTimeout(120); }
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(800);
  }
  const geo = { H: await p.evaluate(() => document.documentElement.scrollHeight) };
  for (const [k, sel] of Object.entries(boites)) {
    const one = async (s) => {
      const r = await p.$eval(s, (e) => { const b = e.getBoundingClientRect(); return [b.left + scrollX, b.top + scrollY, b.width, b.height].map(Math.round); }).catch(() => null);
      if (!r) console.error(`introuvable : ${k} (${s})`);
      return r;
    };
    geo[k] = Array.isArray(sel) ? await Promise.all(sel.map(one)) : await one(sel);
  }
  await p.screenshot({ path: sortie, fullPage: true, type: sortie.endsWith('.png') ? 'png' : 'jpeg', ...(sortie.endsWith('.png') ? {} : { quality: 82 }) });
  fs.writeFileSync(sortie.replace(/\.\w+$/, '') + '.geo.json', JSON.stringify(geo, null, 1));
  console.log(`${sortie} (${largeur}×${geo.H}) + géométrie de ${Object.keys(boites).length} encarts`);
  await b.close();
})();
