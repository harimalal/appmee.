// Lecture d'un fichier de montage (voir assets/montage-60s-modele.cjs) : morceaux du film long joués à une vitesse donnée,
// et répliques de la voix off placées sur un instant de la scène. Utilisé par rendre.cjs (mode court) et voix-off.cjs.
// Seul : node montage.cjs <montage.cjs>  → affiche le découpage, la durée et la place de chaque réplique.
const path = require('path');
function charger(fichier) {
  const m = require(path.resolve(fichier));
  let acc = 0;
  const PARTS = m.SEG.map(([a, b, v, net]) => { const d = (b - a) / v, p = { a, b, v, net: net === 'net', o0: acc, o1: acc + d }; acc += d; return p; });
  const DUREE = acc;
  const sceneTime = o => { const p = PARTS.find(p => o < p.o1) || PARTS[PARTS.length - 1]; return Math.min(p.b, p.a + (o - p.o0) * p.v); };
  const outTime = s => { const p = PARTS.find(p => s >= p.a && s <= p.b); if (!p) throw new Error(`instant ${s} s hors des morceaux du montage`); return p.o0 + (s - p.a) / p.v; };
  const DIT = m.DIT || {};                                   // { 'écrit': 'dit' } : ce que la voix prononce autrement qu'à l'écrit
  const dire = s => Object.entries(DIT).reduce((x, [a, b]) => x.split(a).join(b), s);
  const VOIX = (m.VOIX || []).map(([s, texte]) => ({ debut: outTime(s), texte, dit: dire(texte) }));
  return { SEG: m.SEG, PARTS, DUREE, sceneTime, outTime, VOIX, TON: m.TON || '', DIT };
}
module.exports = { charger };
if (require.main === module) {
  const M = charger(process.argv[2]);
  console.log('durée', M.DUREE.toFixed(2), 's');
  M.PARTS.forEach(p => console.log(`  ${p.a} → ${p.b} ×${p.v}${p.net ? ' (coupe franche)' : ''} : ${p.o0.toFixed(2)} → ${p.o1.toFixed(2)}`));
  let mots = 0;
  M.VOIX.forEach((l, i) => { const n = l.dit.split(/\s+/).length, place = (M.VOIX[i + 1] ? M.VOIX[i + 1].debut : M.DUREE) - l.debut; mots += n;
    console.log(`  ${l.debut.toFixed(2)} s · ${n} mots pour ${place.toFixed(1)} s${n / 2.3 > place ? '  ← trop long à 2,3 mots/s' : ''} · ${l.texte}`); });
  console.log(`voix : ${mots} mots (≈ ${(mots / 2.3).toFixed(0)} s de parole posée)`);
}
