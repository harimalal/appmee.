// Rend une page animée (scene.html ou diaporama.html : window.DUREE, window.render(t), window.ready) image par image dans Chromium,
// puis l'encode avec ffmpeg. Sert pour le film, les vidéos courtes, les diaporamas animés, les carrousels et les posts.
// Usage :
//   node rendre.cjs --racine <dossier servi> --scene <page depuis la racine> [options] <mode> …
//   modes :
//     apercu <t> [t…]              images fixes JPEG aux instants donnés, dans <sortie>/apercu/
//     film [ips] [t0] [t1]         vidéo → <nom>.mp4 (crf 21) + <nom>-web.mp4 (crf 26), sans son
//     court [ips]                  version courte d'après --montage → <nom>-court-muet.mp4 (fondu enchaîné de 8 images aux coupes)
//     court [ips] <i0> <i1>        refait seulement les images i0 à i1 de la version courte (sans fondu), puis réencode
//     diapos                       une image par diapositive complète (window.DIAPOS) → <nom>-01.jpg, -02… (+ PDF avec --pdf)
//   options :
//     --format 1080x1920           format de la page (passé en ?format=, lu par le diaporama) ; sinon window.FORMAT ou 1920x1080
//     --montage <montage.cjs>      découpage de la version courte (mode court)
//     --sortie <dossier>           défaut : <dossier de la page>/sortie
//     --nom <base>                 défaut : film
//     --echelle 2                  densité des images fixes (diapos, apercu) ; 1 par défaut (taille exacte du format)
//     --type png                   images fixes en PNG au lieu de JPEG
//     --pdf                        mode diapos : assemble aussi <nom>.pdf (carrousel LinkedIn, diaporama statique)
//     --gif <largeur>              mode film : ajoute <nom>.gif (15 images/s, palette optimisée, en boucle)
//     --images <dossier>           dossier temporaire des images (défaut : dossier temporaire du système)
//     --chromium <exécutable>
// Node doit trouver playwright : préfixer au besoin par NODE_PATH=$(npm root -g).
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), os = require('os'), { execFileSync } = require('child_process');
const { charger } = require('./montage.cjs');

const argv = process.argv.slice(2), opt = {}, pos = [];
for (let i = 0; i < argv.length; i++) {
  if (!argv[i].startsWith('--')) { pos.push(argv[i]); continue; }
  const k = argv[i].slice(2); opt[k] = (argv[i + 1] !== undefined && !argv[i + 1].startsWith('--')) ? argv[++i] : true;
}
const [mode, ...args] = pos;
if (!opt.scene || !['apercu', 'film', 'court', 'diapos'].includes(mode)) { console.error('usage : node rendre.cjs --racine <dossier> --scene <page.html> apercu|film|court|diapos …'); process.exit(1); }
const RACINE = path.resolve(opt.racine || '.'), SCENE = path.resolve(RACINE, opt.scene);
const SORTIE = path.resolve(opt.sortie || path.join(path.dirname(SCENE), 'sortie')), NOM = opt.nom || 'film';
const IMAGES = path.resolve(opt.images || path.join(os.tmpdir(), 'film-images-' + NOM));
const ECHELLE = +(opt.echelle || 1), TYPE = opt.type === 'png' ? 'png' : 'jpeg', EXT = TYPE === 'png' ? 'png' : 'jpg';
fs.mkdirSync(SORTIE, { recursive: true });

const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.cjs': 'text/javascript', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.json': 'application/json', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf', '.css': 'text/css', '.mp4': 'video/mp4' };
const srv = http.createServer((q, r) => {
  const f = path.join(RACINE, decodeURIComponent(q.url.split('?')[0]));
  if (!f.startsWith(RACINE)) { r.statusCode = 403; return r.end(); }
  try { r.setHeader('Content-Type', TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream'); r.end(fs.readFileSync(f)); } catch (e) { r.statusCode = 404; r.end(); }
});

async function lancer() {
  const essais = [opt.chromium, process.env.CHROMIUM_PATH, undefined];
  try { for (const d of fs.readdirSync('/opt/pw-browsers')) if (d.startsWith('chromium-')) essais.push(`/opt/pw-browsers/${d}/chrome-linux/chrome`); } catch (e) {}
  let err; for (const e of essais) { try { return await chromium.launch({ executablePath: e, args: ['--no-sandbox'] }); } catch (x) { err = x; } }
  throw err;
}
const ff = (...a) => execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...a]);
const encoder = (motif, ips, crf, sortie) => ff('-framerate', String(ips), '-i', motif, '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
  '-c:v', 'libx264', '-preset', 'slow', '-crf', String(crf), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', sortie);
const taille = f => `${(fs.statSync(f).size / 1048576).toFixed(2)} Mo`;

srv.listen(0, async () => {
  const port = srv.address().port;
  let [W, H] = (typeof opt.format === 'string' ? opt.format : '1920x1080').split('x').map(Number);
  const url = `http://localhost:${port}/${path.relative(RACINE, SCENE).split(path.sep).join('/')}?t=0` + (typeof opt.format === 'string' ? `&format=${opt.format}` : '');
  const b = await lancer();
  const fixe = mode === 'diapos' || mode === 'apercu';
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: fixe ? ECHELLE : 1 });
  p.on('pageerror', e => console.log('ERREUR dans la page :', e.message));
  p.on('response', r => { if (r.status() >= 400) console.log('MANQUANT', r.status(), r.url()); });
  await p.goto(url); await p.evaluate(() => window.ready);
  const F = await p.evaluate(() => window.FORMAT || null);
  if (F && (F.w !== W || F.h !== H)) { W = F.w; H = F.h; await p.setViewportSize({ width: W, height: H }); }

  if (mode === 'apercu') {
    fs.mkdirSync(path.join(SORTIE, 'apercu'), { recursive: true });
    for (const t of args) { await p.evaluate(t => render(t), parseFloat(t)); const f = path.join(SORTIE, 'apercu', `${NOM}-t${(+t).toFixed(2).padStart(6, '0')}.jpg`); await p.screenshot({ path: f, type: 'jpeg', quality: 85 }); console.log(f); }
  } else if (mode === 'diapos') {
    const T = await p.evaluate(() => window.DIAPOS || [window.DUREE]), fichiers = [];
    for (const [i, t] of T.entries()) {
      await p.evaluate(t => render(t), t);
      const f = path.join(SORTIE, `${NOM}-${String(i + 1).padStart(2, '0')}.${EXT}`);
      await p.screenshot({ path: f, type: TYPE, ...(TYPE === 'jpeg' ? { quality: 92 } : {}) }); fichiers.push(f); console.log(f, taille(f));
    }
    if (opt.pdf) {   // une page par diapositive, à la taille du format
      const q = await b.newPage();
      await q.setContent(`<style>@page{size:${W}px ${H}px;margin:0}body{margin:0}img{display:block;width:${W}px;height:${H}px;page-break-after:always}</style>` +
        fichiers.map(f => `<img src="data:image/${TYPE};base64,${fs.readFileSync(f).toString('base64')}">`).join(''));
      const pdf = path.join(SORTIE, NOM + '.pdf'); await q.pdf({ path: pdf, width: W + 'px', height: H + 'px', printBackground: true }); console.log(pdf, taille(pdf));
    }
  } else {
    const court = mode === 'court', M = court && charger(opt.montage || path.join(path.dirname(SCENE), 'montage-60s.cjs'));
    const ips = +(args[0] || 30), reprise = court && args[2] !== undefined;
    const t0 = court ? 0 : +(args[1] || 0), t1 = court ? M.DUREE : +(args[2] || await p.evaluate(() => window.DUREE));
    const i0 = reprise ? +args[1] : 0, N = reprise ? +args[2] + 1 : Math.round((t1 - t0) * ips);
    if (!reprise) fs.rmSync(IMAGES, { recursive: true, force: true });
    fs.mkdirSync(IMAGES, { recursive: true });
    // fondu enchaîné aux coupes de la version courte : la dernière image du morceau précédent est posée par-dessus et s'efface en 8 images
    const FONDU = 8; let part = 0, depuis = 99, derniere = null;
    if (court) await p.evaluate(([w, h]) => { const o = document.createElement('img'); o.id = '__fondu'; o.style.cssText = `position:fixed;left:0;top:0;width:${w}px;height:${h}px;z-index:99999;opacity:0;pointer-events:none`; document.body.appendChild(o); }, [W, H]);
    const d0 = Date.now();
    for (let i = i0; i < N; i++) {
      if (court && !reprise) {
        const k = M.PARTS.findIndex(q => i / ips < q.o1);
        if (k > part && M.PARTS[k].net) { part = k; depuis = FONDU; }
        if (k > part && derniere) { part = k; depuis = 0; await p.evaluate(async src => { const f = document.getElementById('__fondu'); f.src = src; await f.decode(); }, 'data:image/jpeg;base64,' + derniere.toString('base64')); }
        await p.evaluate(a => { document.getElementById('__fondu').style.opacity = a; }, depuis < FONDU ? 1 - (depuis + 1) / (FONDU + 1) : 0); depuis++;
      }
      await p.evaluate(t => render(t), court ? M.sceneTime(i / ips) : t0 + i / ips);
      const f = path.join(IMAGES, String(i).padStart(5, '0') + '.jpg');
      await p.screenshot({ path: f, type: 'jpeg', quality: 94 });
      if (court && depuis >= FONDU) derniere = fs.readFileSync(f);
      if (i % 150 === 0) console.log(`image ${i}/${N} (${Math.round((Date.now() - d0) / 1000)} s)`);
    }
    const motif = path.join(IMAGES, '%05d.jpg');
    if (court) { const o = path.join(SORTIE, NOM + '-court-muet.mp4'); encoder(motif, ips, 21, o); console.log('écrit :', o, taille(o)); }
    else {
      const o = path.join(SORTIE, NOM + '.mp4'), w = path.join(SORTIE, NOM + '-web.mp4'); encoder(motif, ips, 21, o); encoder(motif, ips, 26, w); console.log('écrit :', o, taille(o), '·', w, taille(w));
      if (opt.gif) { const g = path.join(SORTIE, NOM + '.gif'), pal = path.join(IMAGES, 'palette.png'), lw = +opt.gif;
        ff('-framerate', String(ips), '-i', motif, '-vf', `fps=15,scale=${lw}:-1:flags=lanczos,palettegen=max_colors=64`, pal);
        ff('-framerate', String(ips), '-i', motif, '-i', pal, '-lavfi', `fps=15,scale=${lw}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4`, '-loop', '0', g);
        console.log('écrit :', g, taille(g)); }
    }
  }
  await b.close(); srv.close();
});
