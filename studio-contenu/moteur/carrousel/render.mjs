// Usage : node render.mjs <dossier-client> <slug-carrousel>
// Lit design.json (client) + carrousels/<slug>/carrousel.json, écrit out/slide-NN.png et out/carrousel.pdf.
import { readFileSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createRequire } from 'node:module';
import { printPage, W, H } from './lib.mjs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const [clientDir, slug] = process.argv.slice(2);
if (!clientDir || !slug) {
  console.error('Usage : node render.mjs <dossier-client> <slug-carrousel>');
  process.exit(1);
}
const root = resolve(clientDir);
const design = JSON.parse(readFileSync(join(root, 'design.json'), 'utf8'));
const dir = join(root, 'carrousels', slug);
const carousel = JSON.parse(readFileSync(join(dir, 'carrousel.json'), 'utf8'));
const out = join(dir, 'out');
mkdirSync(out, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.setContent(printPage(design, carousel), { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
const els = await page.$$('.slide');
for (let i = 0; i < els.length; i++) {
  await els[i].screenshot({ path: join(out, `slide-${String(i + 1).padStart(2, '0')}.png`) });
}
await page.pdf({ path: join(out, 'carrousel.pdf'), width: `${W}px`, height: `${H}px`, printBackground: true });
await browser.close();
console.log(`${els.length} slides + PDF → ${out}`);
