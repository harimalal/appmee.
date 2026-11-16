// Audit mécanique du site NOVOLENS V3. Usage : node audit.js ../site > resultat.json
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = path.resolve(process.argv[2] || '../site');
const pages = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
const lum = h => { const c = [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255).map(v => v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4)); return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]; };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
// paires texte / fond réellement utilisées (seuil : 4,5 texte normal, 3 grand texte)
const pairs = [
  ['encre sur blanc', '#14102F', '#FFFFFF', 4.5], ['encre sur violet clair', '#14102F', '#F1EBFF', 4.5], ['encre sur violet fin de dégradé', '#14102F', '#D9CDFF', 4.5],
  ['texte secondaire sur blanc', '#35325C', '#FFFFFF', 4.5], ['texte secondaire sur violet clair', '#35325C', '#F1EBFF', 4.5], ['texte secondaire sur violet fin de dégradé', '#35325C', '#D9CDFF', 4.5],
  ['gris muted sur blanc', '#4F4B78', '#FFFFFF', 4.5], ['gris muted sur violet fin de dégradé', '#4F4B78', '#D9CDFF', 4.5],
  ['violet de marque sur blanc', '#4B39DD', '#FFFFFF', 4.5], ['violet de marque sur violet clair', '#4B39DD', '#F1EBFF', 4.5], ['violet de marque sur violet fin de dégradé', '#4B39DD', '#D9CDFF', 4.5],
  ['blanc sur bouton violet', '#FFFFFF', '#4B39DD', 4.5], ['blanc sur violet clair du bouton', '#FFFFFF', '#7656F5', 4.5],
  ['encre sur jaune', '#14102F', '#FFD84D', 4.5], ['rouge pastille sans', '#FFFFFF', '#B03A52', 4.5],
];
(async () => {
  const out = { pages: [], contrast: [], summary: {} };
  for (const [n, a, b, min] of pairs) { const r = ratio(a, b); out.contrast.push({ pair: n, ratio: +r.toFixed(2), min, ok: r >= min }); }
  const browser = await chromium.launch();
  for (const f of pages) {
    const rec = { page: f, size_kb: +(fs.statSync(path.join(dir, f)).size / 1024).toFixed(1), widths: {} };
    const html = fs.readFileSync(path.join(dir, f), 'utf8');
    rec.title = (html.match(/<title>(.*?)<\/title>/) || [])[1] || '';
    rec.description = /<meta name="description" content="[^"]{40,}/.test(html);
    rec.h1 = (html.match(/<h1[ >]/g) || []).length;
    rec.imgs_without_dims = (html.match(/<img(?![^>]*width=)[^>]*>/g) || []).length;
    rec.imgs_without_alt = (html.match(/<img(?![^>]*alt=)[^>]*>/g) || []).length;
    rec.links_broken = [];
    for (const m of html.matchAll(/href="([^"#:]+\.html|[^"#:]+\.xml|[^"#:]+\.txt)"/g)) if (!fs.existsSync(path.join(dir, m[1]))) rec.links_broken.push(m[1]);
    for (const w of [400, 820, 1360]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: 860 } });
      const p = await ctx.newPage(); const errs = [];
      p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/fonts\.g|ERR_|Failed to load resource/.test(m.text())) errs.push(m.text()); });
      await p.goto('file://' + path.join(dir, f)); await p.waitForTimeout(700);
      const H = await p.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < H; y += 600) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(60); }
      rec.widths[w] = { overflow: await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), console_errors: errs.length, errors: errs.slice(0, 3) };
      await ctx.close();
    }
    // clavier : le premier Tab atteint le lien d'évitement, 12 Tab de suite donnent un focus visible
    const ctx = await browser.newContext({ viewport: { width: 1360, height: 860 } });
    const p = await ctx.newPage(); await p.goto('file://' + path.join(dir, f));
    let focusOk = true;
    for (let i = 0; i < 8; i++) { await p.keyboard.press('Tab'); const o = await p.evaluate(() => { const e = document.activeElement; if (!e || e === document.body) return 'none'; const s = getComputedStyle(e); return s.outlineStyle + '|' + s.outlineWidth; }); if (o === 'none') focusOk = false; }
    rec.keyboard_focus_visible = focusOk; await ctx.close();
    // mouvement réduit : aucun contenu masqué
    const c2 = await browser.newContext({ viewport: { width: 1360, height: 860 }, reducedMotion: 'reduce' });
    const p2 = await c2.newPage(); await p2.goto('file://' + path.join(dir, f)); await p2.waitForTimeout(600);
    rec.reduced_motion_hidden = await p2.evaluate(() => Array.from(document.querySelectorAll('.pre')).filter(e => getComputedStyle(e).opacity < 0.5).length); await c2.close();
    out.pages.push(rec);
  }
  await browser.close();
  const imgs = fs.readdirSync(path.join(dir, 'img')).map(n => ({ n, kb: +(fs.statSync(path.join(dir, 'img', n)).size / 1024).toFixed(0) }));
  out.images = imgs;
  out.summary = {
    pages: out.pages.length,
    html_over_60kb: out.pages.filter(p => p.size_kb > 60).map(p => p.page),
    images_over_250kb: imgs.filter(i => i.kb > 250).map(i => i.n),
    overflow: out.pages.filter(p => Object.values(p.widths).some(x => x.overflow)).map(p => p.page),
    console_errors: out.pages.filter(p => Object.values(p.widths).some(x => x.console_errors)).map(p => p.page),
    h1_not_one: out.pages.filter(p => p.h1 !== 1).map(p => p.page),
    no_description: out.pages.filter(p => !p.description).map(p => p.page),
    imgs_without_dims: out.pages.filter(p => p.imgs_without_dims).map(p => p.page),
    imgs_without_alt: out.pages.filter(p => p.imgs_without_alt).map(p => p.page),
    broken_links: out.pages.filter(p => p.links_broken.length).map(p => [p.page, p.links_broken]),
    focus_not_visible: out.pages.filter(p => !p.keyboard_focus_visible).map(p => p.page),
    reduced_motion_hidden: out.pages.filter(p => p.reduced_motion_hidden).map(p => p.page),
    contrast_failures: out.contrast.filter(c => !c.ok),
  };
  console.log(JSON.stringify(out, null, 1));
})();
