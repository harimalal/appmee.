// Voix off : prépare le texte à envoyer à ElevenLabs, puis cale la prise sur le film court et écrit les sous-titres.
//
// 1) Texte pour ElevenLabs (une seule prise de tout le texte, répliques séparées par une ligne vide, consigne de ton en tête) :
//      node voix-off.cjs --montage montage-60s.cjs --texte
// 2) Calage, une fois la prise téléchargée (prise.mp3) et sa transcription horodatée enregistrée à côté (prise.mots.json, format
//    ElevenLabs Scribe : { "words": [ { "text", "type": "word", "start", "end" }, … ] }) :
//      node voix-off.cjs --montage montage-60s.cjs --prise voix/prise.mp3 --muet sortie/video/film-60s-court-muet.mp4 --sortie sortie/video --nom film-60s --langue en
//    Ajouter --essai pour seulement afficher le placement des répliques.
// Sorties : <nom>.mp4 (voix + piste de sous-titres activable, vidéo copiée), <nom>-web.mp4 (crf 26), <nom>-voix.m4a, <nom>.<langue>.srt et .vtt
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { charger } = require('./montage.cjs');
const argv = process.argv.slice(2), opt = {};
for (let i = 0; i < argv.length; i++) { const k = argv[i].slice(2); opt[k] = (argv[i + 1] && !argv[i + 1].startsWith('--')) ? argv[++i] : true; }
const M = charger(opt.montage || 'montage-60s.cjs');

if (opt.texte) { console.log([M.TON, ...M.VOIX.map(v => v.dit)].filter(Boolean).join('\n\n').replace(/^(\[[^\]]*\])\n\n/, '$1 ')); process.exit(0); }

const prise = path.resolve(opt.prise), SORTIE = path.resolve(opt.sortie || 'sortie'), NOM = opt.nom || 'film-60s', LANGUE = opt.langue || 'en';
fs.mkdirSync(SORTIE, { recursive: true });
const ff = (...a) => execFileSync('ffmpeg', ['-y', '-hide_banner', '-nostats', '-loglevel', 'error', ...a]);
const total = +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', prise], { encoding: 'utf8' });

// lettres et chiffres seulement, sans accents : on compare la transcription au texte dit sans dépendre du découpage en mots
const norme = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
const mots = JSON.parse(fs.readFileSync(opt.mots || prise.replace(/\.[^.]+$/, '.mots.json'), 'utf8')).words.filter(w => w.type === 'word');
if (mots.length && /^\[/.test(mots[0].text)) mots.splice(0, mots.findIndex(w => /\]$/.test(w.text)) + 1);   // consigne de ton, non dite
let n = 0;
const morceaux = M.VOIX.map(v => {
  const cible = norme(v.dit); let lu = '', j = n;
  while (j < mots.length && lu.length < cible.length) lu += norme(mots[j++].text);
  if (lu !== cible) throw new Error(`réplique mal alignée (vérifier la transcription ou le texte dit) :\n  lu      ${lu}\n  attendu ${cible}`);
  const r = { ...v, a: mots[n].start, b: mots[j - 1].end }; n = j; return r;
});
if (n !== mots.length) console.log(`ATTENTION : ${mots.length - n} mots de la prise ne correspondent à aucune réplique`);
// marges : à mi-chemin entre deux répliques, 0,1 s avant et 0,15 s après au plus
morceaux.forEach((m, i) => { const av = morceaux[i - 1], ap = morceaux[i + 1];
  m.a = Math.max(av ? (av.b + m.a) / 2 : 0, m.a - 0.1); m.b = Math.min(ap ? (m.b + ap.a) / 2 : total, m.b + 0.15); });
// placement : chaque réplique à son instant, ou 0,15 s après la précédente si celle-ci déborde
let libre = 0;
for (const m of morceaux) { m.pose = Math.max(m.debut, libre + 0.15); m.duree = m.b - m.a; libre = m.pose + m.duree; }
morceaux.forEach(m => console.log(`${m.pose.toFixed(2)} → ${(m.pose + m.duree).toFixed(2)}${m.pose - m.debut > .3 ? `  (prévu ${m.debut.toFixed(2)}, retard ${(m.pose - m.debut).toFixed(1)} s)` : ''}  ${m.texte}`));
if (libre > M.DUREE - 0.3) console.log(`ATTENTION : la voix finit à ${libre.toFixed(2)} s pour un film de ${M.DUREE.toFixed(2)} s : ralentir la fin ou accélérer un morceau du montage`);
if (opt.essai) process.exit(0);

const piste = path.join(SORTIE, NOM + '-voix.m4a'), entrees = [], filtres = [];
morceaux.forEach((m, i) => { entrees.push('-ss', m.a.toFixed(3), '-t', m.duree.toFixed(3), '-i', prise);
  filtres.push(`[${i}:a]aresample=48000,afade=t=in:d=0.03,afade=t=out:st=${(m.duree - 0.05).toFixed(3)}:d=0.05,adelay=${Math.round(m.pose * 1000)}:all=1[v${i}]`); });
ff(...entrees, '-filter_complex', filtres.join(';') + ';' + morceaux.map((_, i) => `[v${i}]`).join('') +
  `amix=inputs=${morceaux.length}:normalize=0,apad,atrim=0:${M.DUREE.toFixed(3)},loudnorm=I=-16:TP=-1.5:LRA=11[a]`, '-map', '[a]', '-c:a', 'aac', '-b:a', '160k', piste);

// sous-titres : le texte écrit (pas le texte dit), affiché pendant la réplique et 0,6 s après au plus
const tc = (s, sep) => { const ms = Math.round(s * 1000); return [Math.floor(ms / 3600000), Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60].map(x => String(x).padStart(2, '0')).join(':') + sep + String(ms % 1000).padStart(3, '0'); };
const cues = morceaux.map((m, i) => ({ a: m.pose, b: Math.min(morceaux[i + 1] ? morceaux[i + 1].pose - 0.05 : M.DUREE, m.pose + m.duree + 0.6), t: m.texte }));
const srt = path.join(SORTIE, `${NOM}.${LANGUE}.srt`), vtt = path.join(SORTIE, `${NOM}.${LANGUE}.vtt`);
fs.writeFileSync(srt, cues.map((c, i) => `${i + 1}\n${tc(c.a, ',')} --> ${tc(c.b, ',')}\n${c.t}\n`).join('\n'));
fs.writeFileSync(vtt, 'WEBVTT\n\n' + cues.map(c => `${tc(c.a, '.')} --> ${tc(c.b, '.')}\n${c.t}\n`).join('\n'));

const ISO3 = { en: 'eng', fr: 'fra', es: 'spa', de: 'deu', it: 'ita', pt: 'por', nl: 'nld', ja: 'jpn', zh: 'zho', ko: 'kor', ar: 'ara' };
const muet = path.resolve(opt.muet), out = path.join(SORTIE, NOM + '.mp4'), web = path.join(SORTIE, NOM + '-web.mp4');
ff('-i', muet, '-i', piste, '-i', srt, '-map', '0:v', '-map', '1:a', '-map', '2:s', '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text',
  '-metadata:s:s:0', 'language=' + (ISO3[LANGUE] || LANGUE), '-shortest', '-movflags', '+faststart', out);
ff('-i', muet, '-i', piste, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '26', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', web);
for (const f of [out, web, piste, srt, vtt]) console.log('écrit :', f, `${(fs.statSync(f).size / 1048576).toFixed(1)} Mo`);
