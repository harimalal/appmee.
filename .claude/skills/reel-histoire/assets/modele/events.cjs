/** Extrait les événements sonores de la page (window.EVENTS) -> events.json. Usage : NODE_PATH=$(npm root -g) node events.cjs */
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'story.html')); await p.evaluate(() => document.fonts.ready);
  const ev = await p.evaluate(() => ({ total: window.REEL.total, events: window.EVENTS.slice().sort((a, b) => a.t - b.t) }));
  fs.writeFileSync(path.join(__dirname, 'events.json'), JSON.stringify(ev, null, 1));
  const c = {}; ev.events.forEach(e => c[e.type] = (c[e.type] || 0) + 1);
  console.log('événements :', ev.events.length, JSON.stringify(c), '· durée', ev.total); await b.close();
})();
