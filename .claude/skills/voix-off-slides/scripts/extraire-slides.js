// Lit un deck HTML : id, nombre d'étapes, texte à l'écran (à la dernière étape) de chaque slide.
//   NODE_PATH=$(npm root -g) node extraire-slides.js deck.html slides.json
// Le deck doit exposer window.__S ([id, étapes]) et window.__go(i, étape).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [deck, sortie] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.resolve(deck)); await p.waitForTimeout(2500);
  const S = await p.evaluate(() => window.__S);
  if (!S) { console.error('Le deck n\'expose pas window.__S / window.__go'); process.exit(1); }
  const out = [];
  for (let i = 0; i < S.length; i++) {
    await p.evaluate(([i, m]) => window.__go(i, m), [i, S[i][1]]); await p.waitForTimeout(600);
    const text = await p.evaluate(i => document.querySelectorAll('.slide')[i].innerText.replace(/\s+/g, ' ').trim(), i);
    const note = await p.evaluate(() => (document.getElementById('nt') || {}).textContent || '');
    out.push({ i: i + 1, id: S[i][0], steps: S[i][1], note, text });
  }
  fs.writeFileSync(sortie, JSON.stringify(out, null, 1)); await b.close();
  console.log(out.length, 'slides →', sortie);
})();
