// Pose une grille graduée (repère 390×844 de la scène) sur des captures, pour lire à l'œil la position des éléments à animer
// quand on ne peut pas les mesurer dans le navigateur (app mobile native). Reporter ensuite { x, y, w, h } dans captures/boites.json.
// Usage : NODE_PATH=$(npm root -g) node quadrillage.cjs <capture.png> [autres…]   → <capture>-grille.png à côté de chaque capture
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  let b; try { b = await chromium.launch({ args: ['--no-sandbox'] }); } catch (e) {
    const d = fs.readdirSync('/opt/pw-browsers').find(x => x.startsWith('chromium-')); b = await chromium.launch({ executablePath: `/opt/pw-browsers/${d}/chrome-linux/chrome`, args: ['--no-sandbox'] }); }
  const p = await b.newPage({ viewport: { width: 470, height: 900 }, deviceScaleFactor: 2 });
  for (const f of process.argv.slice(2)) {
    const src = 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
    let lignes = '';
    for (let x = 0; x <= 390; x += 10) lignes += `<div style="position:absolute;left:${40 + x}px;top:20px;width:1px;height:844px;background:rgba(230,38,74,${x % 50 ? .18 : .6})"></div>` + (x % 50 ? '' : `<span style="position:absolute;left:${34 + x}px;top:2px;font:600 11px sans-serif;color:#E6264A">${x}</span>`);
    for (let y = 0; y <= 844; y += 10) lignes += `<div style="position:absolute;left:40px;top:${20 + y}px;width:390px;height:1px;background:rgba(47,111,235,${y % 50 ? .18 : .6})"></div>` + (y % 50 ? '' : `<span style="position:absolute;left:4px;top:${13 + y}px;font:600 11px sans-serif;color:#2F6FEB">${y}</span>`);
    await p.setContent(`<body style="margin:0;background:#fff"><img src="${src}" style="position:absolute;left:40px;top:20px;width:390px;height:844px">${lignes}</body>`);
    await p.waitForTimeout(100);
    const out = f.replace(/\.[^.]+$/, '-grille.png'); await p.screenshot({ path: out }); console.log(out);
  }
  await b.close();
})();
