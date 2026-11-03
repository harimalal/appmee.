// Enregistre le diaporama en vidéo 1920×1080, en avançant tout seul d'étape en étape.
// Sert d'aperçu à valider, ou de piste vidéo à monter sous la voix (l'enregistrement d'écran
// à la main, avec la flèche droite, reste le plus souple pour caler sur l'oral).
//
// Usage :
//   NODE_PATH=$(npm root -g) node enregistrer.cjs demo.html sortie.mp4 [--temps temps.json] [--defaut 2600] [--de 0 --a 19]
// temps.json : {"prompt":[2500,9000,3000,2500], "manuel":[1500,9000,3500,4000,6000,3000,3000]}
//   -> durée de chaque étape d'une slide (en ms), par id de slide. Les étapes non listées prennent --defaut.
// Sortie : .webm brut de Playwright, converti en .mp4 (H.264) si ffmpeg est présent.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [src, out] = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
if (!src || !out) { console.error('usage : enregistrer.cjs demo.html sortie.mp4 [--temps t.json] [--defaut 2600]'); process.exit(1); }
const T = opt('--temps') ? JSON.parse(fs.readFileSync(opt('--temps'), 'utf8')) : {};
const def = +opt('--defaut', 2600);

(async () => {
  const dir = fs.mkdtempSync(path.join(path.dirname(path.resolve(out)), '.rec-'));
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, recordVideo: { dir, size: { width: 1920, height: 1080 } } });
  const p = await ctx.newPage();
  await p.goto('file://' + path.resolve(src));
  // plein cadre : pas de marge, barre de contrôle et pointeur masqués
  await p.addStyleTag({ content: '#ui,#notes{display:none!important} body{cursor:none}' });
  await p.evaluate(() => { const s = document.getElementById('stage'); s.style.transform = 'translate(-50%,-50%) scale(' + Math.min(innerWidth / 1920, innerHeight / 1080) + ')'; });
  const S = await p.evaluate(() => window.__S);
  const de = +opt('--de', 0), a = +opt('--a', S.length - 1);
  await p.evaluate((i) => window.__go(i, 0), de);
  await p.keyboard.press('r');
  let total = 0;
  for (let i = de; i <= a; i++) {
    const [id, max] = S[i];
    for (let st = 0; st <= max; st++) {
      const ms = (T[id] && T[id][st]) || def;
      await p.waitForTimeout(ms);
      total += ms;
      if (!(i === a && st === max)) await p.keyboard.press('ArrowRight');
    }
  }
  await p.waitForTimeout(800);
  const v = p.video();
  await ctx.close(); await b.close();
  const webm = await v.path();
  if (out.endsWith('.mp4')) {
    try {
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', webm, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-r', '30', out]);
    } catch (e) { fs.copyFileSync(webm, out.replace(/\.mp4$/, '.webm')); console.error('ffmpeg absent ou en échec : .webm gardé'); }
  } else fs.copyFileSync(webm, out);
  fs.rmSync(dir, { recursive: true, force: true });
  console.log(`${out} : ${S.slice(de, a + 1).length} slides, ≈ ${Math.round(total / 1000)} s`);
})();
