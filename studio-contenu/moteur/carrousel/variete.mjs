// Usage : node variete.mjs <dossier-client> [slug]
// Contrôle de variété entre les carrousels d'un même client : photos réutilisées, infographies réutilisées,
// structures de slides trop proches. Sans slug : compare tous les carrousels entre eux.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const [clientDir, cible] = process.argv.slice(2);
if (!clientDir) {
  console.error('Usage : node variete.mjs <dossier-client> [slug]');
  process.exit(1);
}
const dir = join(resolve(clientDir), 'carrousels');
const slugs = readdirSync(dir).filter((s) => existsSync(join(dir, s, 'carrousel.json'))).sort();

function analyse(slug) {
  const c = JSON.parse(readFileSync(join(dir, slug, 'carrousel.json'), 'utf8'));
  const images = new Set();
  const infos = new Set();
  const structure = c.slides.map((s) => {
    const t = [s.layout ?? '?'];
    if (s.image?.fichier) images.add(s.image.fichier);
    if (s.bande) { t.push(`bande-${s.bande.cote ?? 'haut'}`); images.add(s.bande.fichier); }
    if (s.arche) { t.push('arche'); images.add(s.arche.fichier); }
    for (const b of s.blocs ?? []) {
      if (b.type === 'schema') infos.add(b.fichier);
      if (b.type === 'carte' && b.svg) infos.add(b.svg);
      if (b.type === 'chiffre' && b.visuel) infos.add(`visuel:${b.visuel.type}`);
      if (b.type === 'photo') { t.push('photo-forme'); images.add(b.fichier); }
      if (b.type === 'photos') { t.push('rangee'); b.items.forEach((i) => images.add(i.fichier)); }
      if (b.type === 'schema') t.push('infographie');
    }
    return t.join('+');
  });
  return { slug, images, infos, structure, n: c.slides.length };
}

const tous = slugs.map(analyse);
const cibles = cible ? tous.filter((a) => a.slug === cible) : tous;
let alertes = 0;
for (const a of cibles) {
  console.log(`\n== ${a.slug} (${a.n} slides)`);
  console.log(`   structures : ${[...new Set(a.structure)].join(' | ')}`);
  console.log(`   infographies : ${[...a.infos].join(', ') || 'aucune'}`);
  for (const b of tous) {
    if (b.slug === a.slug || (!cible && b.slug < a.slug)) continue;
    const imgs = [...a.images].filter((x) => b.images.has(x));
    const infs = [...a.infos].filter((x) => b.infos.has(x));
    const m = Math.min(a.n, b.n);
    let same = 0;
    for (let i = 0; i < m; i++) if (a.structure[i] === b.structure[i]) same++;
    const sim = Math.round((same / m) * 100);
    const flags = [];
    if (imgs.length) flags.push(`photos communes : ${imgs.join(', ')}`);
    if (infs.length) flags.push(`infographies communes : ${infs.join(', ')}`);
    if (sim >= 50) flags.push(`structure identique à ${sim} % des slides`);
    if (flags.length) {
      alertes++;
      console.log(`   ⚠ vs ${b.slug} : ${flags.join(' ; ')}`);
    }
  }
}
console.log(alertes ? `\n${alertes} point(s) de variété à revoir.` : '\nVariété : rien à signaler.');
