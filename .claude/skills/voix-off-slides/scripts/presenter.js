// Une seule prise continue : présente le deck en suivant minutage.json, comme un présentateur.
//   NODE_PATH=$(npm root -g) node presenter.js deck.html minutage.json prise/
// Fenêtre 1952×1080 pour que le deck s'affiche à l'échelle 1 (recadré ensuite à 1920×1080).
// Le son n'est pas enregistré : l'instant réel de chaque changement de slide va dans prise/journal.json.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const [deck, minutage, dossier] = process.argv.slice(2);
  const tl = JSON.parse(fs.readFileSync(minutage)); fs.rmSync(dossier, { recursive: true, force: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1952, height: 1080 }, recordVideo: { dir: dossier, size: { width: 1952, height: 1080 } } });
  const p = await ctx.newPage(); const t0 = Date.now();
  const ids = await (async () => { await p.goto('file://' + path.resolve(deck)); await p.waitForTimeout(500); return p.evaluate(() => window.__S.map(s => s[0])); })();
  // on part d'une autre slide pour que la première arrive avec son animation d'entrée
  await p.evaluate(h => { location.hash = '#' + h; }, ids[ids.length - 1] === tl[0].id ? ids[0] : ids[ids.length - 1]);
  await p.waitForTimeout(3500);                                    // le panneau du deck se cache tout seul
  const at = s => sleep(Math.max(0, t0 + s * 1000 - Date.now()));
  let clock = (Date.now() - t0) / 1000 + 0.2; const journal = [];
  for (let j = 0; j < tl.length; j++) {
    const s = tl[j]; await at(clock);
    if (j === 0) await p.evaluate(h => { location.hash = '#' + h; }, s.id); else await p.keyboard.press('ArrowRight');
    journal.push({ n: s.n, start: (Date.now() - t0) / 1000, prevu: clock });
    for (const st of s.steps) { await at(clock + st); await p.keyboard.press('ArrowRight'); }
    clock += s.T;
  }
  await at(clock); const end = (Date.now() - t0) / 1000;
  await ctx.close(); await b.close();
  const video = fs.readdirSync(dossier).find(f => f.endsWith('.webm'));
  fs.writeFileSync(path.join(dossier, 'journal.json'), JSON.stringify({ video: path.join(dossier, video), slides: journal, end }, null, 1));
  console.log('prise terminée :', end.toFixed(1), 's');
})();
