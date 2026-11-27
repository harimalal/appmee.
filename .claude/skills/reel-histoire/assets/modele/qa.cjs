/**
 * Contrôle qualité du reel « histoire » (contenu + mise en page + cohérence voix/image).
 * Usage : NODE_PATH=$(npm root -g) node qa.cjs      (code de sortie 1 si une règle échoue)
 * Règles (SKILL_VOIX_REFLEXIA.md, SKILL_STYLE_ECRITURE.md, scripts/content-qa.mjs) :
 *  - tout nombre affiché ou dit appartient à la liste autorisée (story.json -> nombres_autorises = la fiche de faits) ;
 *  - aucun mot banni, aucun emoji, jamais « reflexi-ai.com », « reflex-ia.com » présent dans la CTA ;
 *  - voix : aucun chiffre dans le texte lu (nombres en toutes lettres), transcription inverse OK pour toutes les phrases ;
 *  - hors légendes et décor : ≤ 34 mots visibles en même temps ; légendes ≤ 4,5 mots/s ;
 *  - tout texte visible tient dans les zones sûres (haut 200, bas 380, gauche 84, droite 150) ;
 *  - tout texte visible figure dans le script déclaré de la scène (aucun texte « fantôme »).
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const FILE = 'file://' + path.resolve(__dirname, 'story.html');
const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json'), 'utf8'));
const VR = JSON.parse(fs.readFileSync(path.join(__dirname, 'audio', 'voice-report.json'), 'utf8'));
const CFG = JSON.parse(fs.readFileSync(path.join(__dirname, 'story.json'), 'utf8'));
// Nombres autorisés = ceux de la fiche de faits (story.json -> nombres_autorises). Tout autre nombre affiché ou dit fait échouer le contrôle.
const ALLOWED = new Set((CFG.nombres_autorises || []).map(String));
const CTA = new RegExp((CFG.cta_contient || 'reflex-ia.com').replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
const BANNED = [/révolutionnaire/i, /game[ -]?changer/i, /incroyable/i, /magique/i, /ultime/i, /\b10x\b/i, /\bsecret/i, /fait tout à votre place/i];
const EMOJI = /\p{Extended_Pictographic}/u;
const MAX_VISIBLE = (typeof CFG !== "undefined" && CFG.max_mots_visibles) || 34, MAX_WPS = 4.5, TOL = 6;   // tolérance : ressort d'entrée (échelle < 1 pendant 0,5 s)
const norm = s => s.replace(/\s+/g, ' ').replace(/ /g, ' ').trim().toLowerCase();
const words = s => s.trim().split(/\s+/).filter(Boolean).length;

(async () => {
  const failures = [], fail = m => failures.push(m);
  // voix : texte lu et transcription inverse
  for (const r of VR) { if (!r.ok_texte) fail(`voix ${r.id} : transcription différente (sim ${r.similarite}) : « ${r.entendu} »`); if (/\d/.test(r.attendu)) fail(`voix ${r.id} : chiffre dans le texte lu`); if (BANNED.some(b => b.test(r.attendu))) fail(`voix ${r.id} : mot banni`); }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = []; page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto(FILE); await page.evaluate(() => document.fonts.ready);
  const reel = await page.evaluate(() => window.REEL); const S = reel.safe;
  if (errs.length) fail('erreurs console : ' + errs.join(' | '));
  if (Math.abs(reel.total - TL.total) > .001) fail('durée de la page ≠ timeline');

  // 1) script déclaré
  const scenesTab = [];
  for (const sc of reel.scenes) {
    const sentences = TL.scenes.find(x => x.id === sc.id).sent;
    const maxWps = Math.max(...sentences.map(s => words(s.cap) / (s.end - s.start)));
    scenesTab.push({ scène: sc.id, début: +sc.start.toFixed(1), durée: +(sc.end - sc.start).toFixed(1), phrases: sentences.length, 'mots/s max (légende)': +maxWps.toFixed(2) });
    if (sc.caps.length && maxWps > MAX_WPS) fail(`${sc.id} : légende à ${maxWps.toFixed(2)} mots/s (> ${MAX_WPS})`);
    for (const line of sc.copy) {
      if (BANNED.some(b => b.test(line))) fail(`${sc.id} : mot banni dans « ${line} »`);
      if (EMOJI.test(line)) fail(`${sc.id} : emoji dans « ${line} »`);
      if (/reflexi-ai/i.test(line)) fail(`${sc.id} : mauvais domaine dans « ${line} »`);
      if (!line.startsWith('/')) for (const n of (line.match(/\d+/g) || [])) if (!ALLOWED.has(n)) fail(`${sc.id} : nombre non autorisé « ${n} » dans « ${line} »`);
    }
  }
  if (!reel.scenes.some(s => s.copy.some(l => CTA.test(l)))) fail(`CTA : « ${CFG.cta_contient || 'reflex-ia.com'} » absent`);

  // 2) texte réellement rendu
  const times = new Set([0.05, 0.5, 1.5, TL.total - 0.05]);
  TL.scenes.forEach(sc => {
    [0.4, 1.0, (sc.end - sc.start) * .5, sc.end - sc.start - .12].forEach(x => times.add(+(sc.start + Math.min(Math.max(x, .2), sc.end - sc.start - .05)).toFixed(2)));
    sc.sent.forEach(s => [0.3, 0.9, 1.6, (s.end - s.start)].forEach(x => { const tt = s.start + Math.min(x, s.end - s.start + .2); if (tt < sc.end) times.add(+tt.toFixed(2)); }));
  });
  const allCopy = reel.scenes.map(sc => norm(sc.copy.join(' | ')));
  let samples = 0, maxVis = 0;
  for (const t of [...times].sort((a, b) => a - b)) {
    const items = await page.evaluate(t => window.__qa(t), t); samples++;
    const idx = reel.scenes.reduce((k, sc, i) => (t >= sc.start ? i : k), 0);
    const pool = allCopy[idx] + ' | ' + (idx > 0 ? allCopy[idx - 1] : '');
    let vis = 0; const seen = new Set();
    for (const it of items) {
      if (!it.bleed && (it.x0 < S.x0 - TOL || it.x1 > S.x1 + TOL || it.y0 < S.y0 - TOL || it.y1 > S.y1 + TOL))
        fail(`t=${t}s hors zone sûre : « ${it.text.slice(0, 40)} » [${Math.round(it.x0)},${Math.round(it.y0)}→${Math.round(it.x1)},${Math.round(it.y1)}]`);
      if (BANNED.some(b => b.test(it.text))) fail(`t=${t}s mot banni : « ${it.text} »`);
      if (EMOJI.test(it.text)) fail(`t=${t}s emoji : « ${it.text} »`);
      if (/reflexi-ai/i.test(it.text)) fail(`t=${t}s mauvais domaine : « ${it.text} »`);
      if (!it.deco && !it.count) {
        for (const n of (it.text.match(/\d+/g) || [])) if (!ALLOWED.has(n) && !it.text.startsWith('/')) fail(`t=${t}s nombre non autorisé « ${n} » dans « ${it.text} »`);
        if (!pool.includes(norm(it.text))) fail(`t=${t}s texte absent du script déclaré : « ${it.text} »`);
        if (!it.cap && !seen.has(norm(it.text))) { seen.add(norm(it.text)); vis += words(it.text); }  // textes identiques des deux calques avant/après : comptés une fois
      }
    }
    maxVis = Math.max(maxVis, vis);
    if (vis > MAX_VISIBLE) fail(`t=${t}s : ${vis} mots visibles en même temps (> ${MAX_VISIBLE})`);
  }
  await browser.close();
  fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
  fs.writeFileSync(path.join(__dirname, 'out', 'qa-report.json'), JSON.stringify({ total: TL.total, samples, maxVisibleWords: maxVis, scenes: scenesTab, failures }, null, 2));
  console.log(`\n${samples} instants contrôlés · durée ${TL.total} s · maximum de mots visibles en même temps (hors légendes) : ${maxVis}`);
  console.table(scenesTab);
  if (failures.length) { console.log('\nÉCHECS :'); failures.slice(0, 60).forEach(f => console.log(' - ' + f)); if (failures.length > 60) console.log(` … +${failures.length - 60}`); process.exit(1); }
  console.log('\nQA OK : aucun échec.');
})();
