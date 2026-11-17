// Usage : node render.mjs <dossier-client> <slug-carrousel>
// Écrit out/slide-NN.png et out/carrousel.pdf à partir du template, du carrousel et du design du client.
import { mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createRequire } from 'node:module';
import { load, printPage, fitScript, W, H } from './lib.mjs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const [clientDir, slug] = process.argv.slice(2);
if (!clientDir || !slug) {
  console.error('Usage : node render.mjs <dossier-client> <slug-carrousel>');
  process.exit(1);
}
const root = resolve(clientDir);
const { design, carousel } = load(root)(slug);
const out = join(root, 'carrousels', slug, 'out');
mkdirSync(out, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.setContent(printPage(design, carousel, root), { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.evaluate(fitScript);
// Contrôle de débordement : rien ne doit sortir du cadre ni chevaucher l'en-tête.
const problemes = await page.evaluate(({ W, H }) => {
  const out = [];
  document.querySelectorAll('.slide').forEach((sl, k) => {
    const sr = sl.getBoundingClientRect();
    const head = sl.querySelector('.cl-head');
    const hb = head ? head.getBoundingClientRect().bottom - sr.top : 0;
    const body = sl.querySelector('.cl-body');
    if (body && body.scrollHeight > body.clientHeight + 2) out.push(`slide ${k + 1} : le contenu dépasse de ${body.scrollHeight - body.clientHeight}px`);
    sl.querySelectorAll('.cl-body > *').forEach((el) => {
      const r = el.getBoundingClientRect();
      const top = r.top - sr.top, bottom = r.bottom - sr.top, right = r.right - sr.left, left = r.left - sr.left;
      const nom = el.className || el.tagName;
      if (bottom > H - 44) out.push(`slide ${k + 1} : « ${nom} » trop bas (${Math.round(bottom)}px)`);
      if (right > W - 36 || left < 36) out.push(`slide ${k + 1} : « ${nom} » touche le bord (${Math.round(left)}–${Math.round(right)}px)`);
      if (top < hb - 4) out.push(`slide ${k + 1} : « ${nom} » chevauche l'en-tête`);
    });
  });
  return out;
}, { W, H });
if (problemes.length) console.warn('Débordements :\n' + problemes.map((p) => '  - ' + p).join('\n'));
else console.log('Contrôle débordement : rien ne sort du cadre.');
const els = await page.$$('.slide');
for (let i = 0; i < els.length; i++) {
  await els[i].screenshot({ path: join(out, `slide-${String(i + 1).padStart(2, '0')}.png`) });
}
await page.pdf({ path: join(out, 'carrousel.pdf'), width: `${W}px`, height: `${H}px`, printBackground: true });
await browser.close();
console.log(`${els.length} slides + PDF → ${out}`);
