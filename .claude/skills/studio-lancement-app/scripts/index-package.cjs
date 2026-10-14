// Construit une page de revue (index.html) de tout ce qu'il y a dans un dossier de livrables : images, GIF, vidéos, PDF, sous-titres,
// regroupés par sous-dossier, avec le format en pixels et le poids de chaque fichier. Pour montrer un package d'un coup à l'utilisateur
// (l'ouvrir dans le navigateur, l'envoyer, ou la publier comme page).
// Usage : node index-package.cjs <dossier des livrables> [titre]   → <dossier>/index.html
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const D = path.resolve(process.argv[2] || 'sortie'), TITRE = process.argv[3] || 'Package de lancement';
const IMG = /\.(jpe?g|png|webp|gif)$/i, VID = /\.(mp4|webm)$/i, AUTRE = /\.(pdf|srt|vtt|m4a|mp3)$/i;
const dim = f => { try { return execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration', '-of', 'json', f], { encoding: 'utf8' }); } catch (e) { return null; } };
const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const groupes = {};
(function parcourir(dir) { for (const n of fs.readdirSync(dir).sort()) { const f = path.join(dir, n); if (fs.statSync(f).isDirectory()) { if (n !== 'apercu') parcourir(f); continue; }
  if (!(IMG.test(n) || VID.test(n) || AUTRE.test(n)) || n === 'index.html') continue; const g = path.relative(D, dir) || 'racine'; (groupes[g] = groupes[g] || []).push(f); } })(D);
let html = '';
for (const [g, fichiers] of Object.entries(groupes)) {
  html += `<h2>${esc(g)}</h2><div class="grille">`;
  for (const f of fichiers) {
    const rel = path.relative(D, f).split(path.sep).join('/'), n = path.basename(f), poids = (fs.statSync(f).size / 1048576).toFixed(2) + ' Mo';
    let info = '', apercu = `<div class="doc">${esc(path.extname(n).slice(1).toUpperCase())}</div>`;
    const j = (IMG.test(n) || VID.test(n)) && dim(f);
    if (j) { const o = JSON.parse(j), s = (o.streams || [])[0] || {}, d = o.format && o.format.duration; info = `${s.width}×${s.height}${VID.test(n) && d ? ' · ' + (+d).toFixed(1) + ' s' : ''}`; }
    if (IMG.test(n)) apercu = `<img loading="lazy" src="${rel}">`;
    if (VID.test(n)) apercu = `<video controls preload="metadata" src="${rel}"></video>`;
    html += `<figure>${apercu}<figcaption><a href="${rel}" download>${esc(n)}</a><span>${info ? info + ' · ' : ''}${poids}</span></figcaption></figure>`;
  }
  html += '</div>';
}
fs.writeFileSync(path.join(D, 'index.html'), `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(TITRE)}</title>
<style>:root{--bg:#F6F6F8;--card:#fff;--ink:#0B1020;--soft:#5A6275}@media (prefers-color-scheme:dark){:root{--bg:#0F1117;--card:#1A1D26;--ink:#EEF0F5;--soft:#9AA1B2}}
body{margin:0;padding:24px 16px;font:15px/1.4 system-ui,sans-serif;background:var(--bg);color:var(--ink)}h1{margin:0 0 8px}h2{margin:32px 0 12px;font-size:18px;color:var(--soft)}
.grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}figure{margin:0;background:var(--card);border-radius:14px;overflow:hidden;box-shadow:0 6px 20px -12px rgba(0,0,0,.35)}
figure img,figure video{display:block;width:100%;height:220px;object-fit:contain;background:repeating-conic-gradient(#0001 0 25%,#0000 0 50%) 0 0/16px 16px}
.doc{height:220px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:28px;color:var(--soft)}
figcaption{padding:10px 12px;display:flex;flex-direction:column;gap:2px}figcaption a{color:inherit;font-weight:600;word-break:break-all}figcaption span{color:var(--soft);font-size:13px}</style></head>
<body><h1>${esc(TITRE)}</h1>${html}</body></html>`);
console.log(path.join(D, 'index.html'));
