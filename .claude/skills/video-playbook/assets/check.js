// Contrôle d'un playbook : erreurs console, infobulles par page, débordement mobile, captures.
// Usage : NODE_PATH=<dossier node_modules de playwright> node check.js <dossier_de_travail>
// Sans Playwright : ouvrir playbook.full.html dans un navigateur, regarder la console et passer en largeur 400 px.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const wd = path.resolve(process.argv[2] || '.');
  const url = 'file://' + path.join(wd, 'playbook.full.html');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(600);
  const ids = await p.evaluate(() => Array.from(document.querySelectorAll('section.page')).map(s => s.id));
  await (await p.$('.map')).screenshot({ path: path.join(wd, 'check_map.png') });
  const defs = {}; let shot = 0;
  for (const id of ids) {
    await p.goto(url + '#' + id); await p.waitForTimeout(150);
    defs[id] = await p.evaluate(i => document.querySelectorAll('#' + i + ' .def').length, id);
    const figs = await p.$$('#' + id + ' figure');
    if (figs.length && shot < 4) { await figs[0].screenshot({ path: path.join(wd, 'check_fig_' + id + '.png') }); shot++; }
    const calc = await p.$('#' + id + ' .calc');
    if (calc) await calc.screenshot({ path: path.join(wd, 'check_calc_' + id + '.png') });
  }
  console.log('pages', ids.length, 'infobulles', JSON.stringify(defs));
  console.log('erreurs', JSON.stringify(errs));
  const m = await b.newPage({ viewport: { width: 400, height: 800 } });
  const wide = {};
  for (const id of ids) {
    await m.goto(url + '#' + id); await m.waitForTimeout(150);
    const sw = await m.evaluate(() => document.documentElement.scrollWidth);
    if (sw > 400) wide[id] = sw;
  }
  console.log('debordement mobile', JSON.stringify(wide));
  await b.close();
})();
