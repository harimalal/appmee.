// Exporte chaque bloc [data-out] d'une planche HTML (assets/planche-modele.html) en image à sa taille exacte.
// Sert pour les visuels uniques de tailles différentes : galerie Product Hunt, miniature YouTube, image de partage (OG), bannières, fiches de store.
// Attributs d'un bloc :
//   data-out="nom.jpg"        nom du fichier (extension .jpg par défaut, .png possible)
//   data-echelle="2"          densité (2 = écrans Retina, ex. galerie Product Hunt 1270×760 exportée en 2540×1520) ; 1 par défaut
//   data-gif="anim:40:15"     ajoute aussi un GIF : la planche doit définir window.anim(k) (k de 0 à 1) ; 40 images à 15 images/s
// Usage : NODE_PATH=$(npm root -g) node exporter-planche.cjs --racine <dossier servi> --planche <planche.html depuis la racine> [--sortie <dossier>] [--seul nom]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), os = require('os'), { execFileSync } = require('child_process');
const argv = process.argv.slice(2), opt = {};
for (let i = 0; i < argv.length; i += 2) opt[argv[i].slice(2)] = argv[i + 1];
const RACINE = path.resolve(opt.racine || '.'), PL = path.resolve(RACINE, opt.planche);
const SORTIE = path.resolve(opt.sortie || path.join(path.dirname(PL), 'sortie')); fs.mkdirSync(SORTIE, { recursive: true });
const TMP = path.join(os.tmpdir(), 'planche-gif');
const TYPES = { '.html': 'text/html; charset=utf-8', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.css': 'text/css', '.js': 'text/javascript' };
const srv = http.createServer((q, r) => { const f = path.join(RACINE, decodeURIComponent(q.url.split('?')[0]));
  try { r.setHeader('Content-Type', TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream'); r.end(fs.readFileSync(f)); } catch (e) { r.statusCode = 404; r.end(); } });
srv.listen(0, async () => {
  let b; try { b = await chromium.launch({ args: ['--no-sandbox'] }); } catch (e) {
    const d = fs.readdirSync('/opt/pw-browsers').find(x => x.startsWith('chromium-')); b = await chromium.launch({ executablePath: `/opt/pw-browsers/${d}/chrome-linux/chrome`, args: ['--no-sandbox'] }); }
  const url = `http://localhost:${srv.address().port}/${path.relative(RACINE, PL).split(path.sep).join('/')}`;
  const pages = {};
  const page = async e => { if (pages[e]) return pages[e]; const p = await b.newPage({ viewport: { width: 2000, height: 1200 }, deviceScaleFactor: e });
    p.on('pageerror', x => console.log('ERREUR', x.message)); p.on('response', r => { if (r.status() >= 400) console.log('MANQUANT', r.url()); });
    await p.goto(url); await p.evaluate(() => window.ready || document.fonts.ready); return pages[e] = p; };
  const blocs = await (await page(1)).$$eval('[data-out]', l => l.map(e => ({ out: e.dataset.out, e: +(e.dataset.echelle || 1), gif: e.dataset.gif || '' })));
  for (const bl of blocs) {
    if (opt.seul && !bl.out.startsWith(opt.seul)) continue;
    const p = await page(bl.e), el = await p.$(`[data-out="${bl.out}"]`), nom = /\.(jpe?g|png)$/i.test(bl.out) ? bl.out : bl.out + '.jpg';
    if (bl.gif) await p.evaluate(() => window.anim && window.anim(1));
    const f = path.join(SORTIE, nom); await el.screenshot({ path: f, ...(/png$/i.test(nom) ? {} : { type: 'jpeg', quality: 90 }) });
    console.log(f, Math.round(fs.statSync(f).size / 1024) + ' Ko');
    if (bl.gif) {
      const [, n = 40, ips = 15] = bl.gif.split(':').map(Number); fs.rmSync(TMP, { recursive: true, force: true }); fs.mkdirSync(TMP, { recursive: true });
      for (let i = 0; i < n; i++) { await p.evaluate(k => window.anim(k), i / n); await el.screenshot({ path: path.join(TMP, String(i).padStart(3, '0') + '.png') }); }
      const g = f.replace(/\.(jpe?g|png)$/i, '.gif'), pal = path.join(TMP, 'pal.png');
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(ips), '-i', path.join(TMP, '%03d.png'), '-vf', 'palettegen=max_colors=48', pal]);
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(ips), '-i', path.join(TMP, '%03d.png'), '-i', pal, '-lavfi', 'paletteuse=dither=none', '-loop', '0', g]);
      console.log(g, Math.round(fs.statSync(g).size / 1024) + ' Ko');
      await p.evaluate(() => window.anim(1));
    }
  }
  await b.close(); srv.close();
});
