// MODÈLE — à copier dans le dossier du film puis à adapter à l'app (sélecteurs, routes d'API, données de démonstration).
// Joue le scénario de démonstration dans la VRAIE app web, au format téléphone, et capture chaque état du storyboard.
// Sorties : captures/NN-nom.png (390×844 en CSS, échelle 3 → 1170×2532), captures/saisie/NN.png (barre de saisie à chaque lettre),
//           captures/boites.json (positions des éléments à animer, repère 390×844).
// Usage : NODE_PATH=$(npm root -g) node capture.cjs
// Principes (tirés du film Dropit) :
//  - l'app tourne en local (serveur statique ci-dessous) ou sur une adresse de test ; tout appel réseau est remplacé par des données de démo
//    (authentification, API, IA simulée avec des réponses écrites pour le film), pour que chaque capture retombe identique ;
//  - Math.random est fixé (graine) : couleurs, émojis, identifiants tirés au hasard restent les mêmes d'une capture à l'autre ;
//  - un identifiant créé pendant le scénario (ex. projet créé) est récupéré et réutilisé dans les captures suivantes ;
//  - les photos viennent de fichiers locaux (medias/), servis à la place des adresses distantes de l'app ;
//  - masquer ce qui gêne (bandeaux, encoche simulée, bulles d'aide) par une feuille de style injectée.
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const ICI = __dirname;
const APP = process.env.APP_DIR || path.resolve(ICI, '..');              // TODO : dossier de l'app (ou passer par APP_URL)
const APP_URL = process.env.APP_URL || null;                             // ex. https://staging.example.com — sinon serveur local
const OUT = path.join(ICI, 'captures'); fs.mkdirSync(path.join(OUT, 'saisie'), { recursive: true });
const W = 390, H = 844, SCALE = 3;
const TEXTE_TAPE = 'TODO: what the demo user types';

// --- serveur statique local de l'app (si APP_URL n'est pas donné) ---
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.json': 'application/json' };
const srv = http.createServer((q, r) => { let f = path.join(APP, decodeURIComponent(q.url.split('?')[0])); if (f.endsWith('/')) f += 'index.html';
  try { r.setHeader('Content-Type', TYPES[path.extname(f)] || 'application/octet-stream'); r.end(fs.readFileSync(f)); } catch (e) { r.statusCode = 404; r.end(); } });

// --- données de démonstration (TODO) ---
const DEMO = { user: { id: 'u1', email: 'sarah@example.com', name: 'Sarah' }, items: [] };
function reponseIA(corps) { return JSON.stringify({}); }                  // TODO : réponse écrite à la main selon la requête

const boxes = {};
async function box(p, nom, sel) { const b = await p.evaluate(s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; }, sel); if (b) boxes[nom] = b; else console.log('introuvable :', nom, sel); return b; }
async function shot(p, nom) { await p.screenshot({ path: path.join(OUT, nom + '.png') }); console.log('capture', nom); }

async function ouvrir(b, base, etat) {
  const ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE, isMobile: true, hasTouch: true, serviceWorkers: 'block', locale: 'en-US',
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148' });
  await ctx.addInitScript(() => { let a = 20261013; Math.random = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; });
  await ctx.addInitScript(etat => { try { /* TODO : session simulée, tutoriels déjà vus, langue… */ localStorage.setItem('demo', JSON.stringify(etat)); } catch (e) {} }, etat || {});
  const p = await ctx.newPage(); p.errs = []; p.on('pageerror', e => p.errs.push(String(e)));
  // TODO : une route par appel de l'app. Exemple :
  await p.route('**/api/ai', async r => { const corps = JSON.parse(r.request().postData() || '{}'); await new Promise(s => setTimeout(s, p.delaiIA || 300));
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ content: [{ type: 'text', text: reponseIA(corps) }] }) }); });
  // photos : adresse distante → fichier local
  await p.route('https://images.example.com/**', r => r.fulfill({ status: 200, contentType: 'image/jpeg', body: fs.readFileSync(path.join(ICI, 'medias', r.request().url().split('/').pop())) }));
  await p.goto(base);
  await p.addStyleTag({ content: '/* TODO : masquer ce qui gêne */' });
  await p.waitForTimeout(1500);
  return p;
}

srv.listen(0, async () => {
  const base = APP_URL || `http://localhost:${srv.address().port}/`;
  const b = await chromium.launch({ args: ['--no-sandbox'] });   // ou executablePath: '/opt/pw-browsers/chromium-…/chrome-linux/chrome'

  // 1. Accueil, puis saisie lettre par lettre dans la vraie barre (une image de la barre par lettre)
  { const p = await ouvrir(b, base);
    await shot(p, '01-accueil');
    const champ = '#TODO-champ', barre = '#TODO-barre';
    await box(p, 'barre', barre);
    for (let i = 0; i <= TEXTE_TAPE.length; i++) {
      await p.fill(champ, TEXTE_TAPE.slice(0, i));
      await p.locator(barre).screenshot({ path: path.join(OUT, 'saisie', String(i).padStart(2, '0') + '.png') });
    }
    await shot(p, '02-saisie');
    // 2. Envoi, état d'attente, résultat ; mesurer ce que la scène doit animer (zooms, anneaux, touchers)
    // await p.click('#TODO-envoyer'); await p.waitForTimeout(900); await shot(p, '03-attente');
    // await p.waitForSelector('#TODO-resultat'); await box(p, 'resultat', '#TODO-resultat'); await shot(p, '04-resultat');
    console.log('erreurs JS :', p.errs.length ? p.errs : 'aucune');
    await p.context().close(); }

  fs.writeFileSync(path.join(OUT, 'boites.json'), JSON.stringify({ scale: SCALE, viewport: { w: W, h: H }, boxes }, null, 1));
  await b.close(); srv.close();
});
