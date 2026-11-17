// Usage : node apercu.mjs <dossier-client> <fichier-sortie.html>
// Génère une page d'aperçu (tous les carrousels d'un client) à partir des carrousel.json.
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { load, css, slides, fitScript, W, H } from './lib.mjs';

const [clientDir, outFile] = process.argv.slice(2);
const root = resolve(clientDir);
const loader = load(root);
const D0 = loader(readdirSync(join(root, 'carrousels')).sort()[0]).design;
const A = D0.apercu ?? {};
const credits = JSON.parse(readFileSync(join(root, 'assets', 'unsplash', 'credits.json'), 'utf8')).photos;
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const todos = (c) => [...JSON.stringify(c.slides).matchAll(/\[\[(.+?)\]\]/g)].map((m) => m[1].replace(/\\u2019/g, '’'));

const sections = readdirSync(join(root, 'carrousels')).sort().map((slug) => {
  const { design, carousel: c } = loader(slug);
  const photos = [...new Set(c.slides.map((x) => x.image?.fichier).filter(Boolean))];
  const t = todos(c);
  return `<section class="car">
  <header><span class="tpl">Template : ${esc(c.template)}</span><h2>${esc(c.titre_interne)}</h2></header>
  <div class="rail" tabindex="0" aria-label="Slides de ${esc(c.titre_interne)}">${slides(design, c, root).map((h) => `<div class="frame"><div class="scale">${h}</div></div>`).join('')}</div>
  <div class="meta">
    <div><h3>Légende proposée</h3><p>${esc(c.legende).replace(/\[\[(.+?)\]\]/g, '<span class="todo-i">$1</span>')}</p></div>
    <div><h3>Photos Unsplash</h3><ul>${photos.map((f) => `<li>${esc(credits[f]?.auteur ?? f)}</li>`).join('')}</ul></div>
    <div><h3>À compléter par ${esc(A.complement ?? 'le client')}</h3>${t.length ? `<ul>${t.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : '<p>Rien.</p>'}</div>
  </div>
</section>`;
});

let html = `<meta name="claude:viewport-fit-sides" content="cover">
<title>${esc(A.titre ?? 'Carrousels')}</title>
<style>
:root{--bg:#F6F5F8;--surface:#FFFFFF;--ink:#261A2C;--muted:#6B6074;--line:#DDD7E3;--accent:#8E2257;--warn-bg:#F6EAD0;--warn:#8F5B00}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#17111A;--surface:#211828;--ink:#F0EAF3;--muted:#A99DB3;--line:#392C42;--accent:#E680AB;--warn-bg:#3A2E14;--warn:#E8B558;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#17111A;--surface:#211828;--ink:#F0EAF3;--muted:#A99DB3;--line:#392C42;--accent:#E680AB;--warn-bg:#3A2E14;--warn:#E8B558;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:"DM Sans",system-ui,sans-serif;font-size:16px;line-height:1.55;padding-block:32px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:1080px;margin:0 auto;display:flex;flex-direction:column;gap:48px}
h1,h2,h3{font-family:"Bricolage Grotesque",system-ui,sans-serif;margin:0;line-height:1.1;text-wrap:balance}
h1{font-size:clamp(2rem,6vw,3.2rem)}h2{font-size:1.7rem}h3{font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-family:"DM Sans",sans-serif;margin-bottom:6px}
p{margin:0;max-width:65ch}.lede{color:var(--muted);font-size:1.1rem;margin-top:10px}
.eyebrow{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);font-weight:700;display:block;margin-bottom:8px}
.car{display:flex;flex-direction:column;gap:16px;min-width:0}
.tpl{font-size:.8rem;color:var(--muted);font-weight:700;letter-spacing:.06em;text-transform:uppercase;display:block;margin-bottom:6px}
.rail{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:12px}
.frame{flex:0 0 min(78vw,340px);aspect-ratio:${W}/${H};position:relative;overflow:hidden;border-radius:10px;border:1px solid var(--line);scroll-snap-align:start}
.scale{position:absolute;left:0;top:0;width:${W}px;height:${H}px;transform-origin:0 0;transform:scale(var(--s,.3))}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px}
.meta ul{margin:0;padding-left:18px;display:grid;gap:4px}
.todo-i{background:var(--warn-bg);color:var(--warn);font-weight:700;border-radius:6px;padding:0 6px}
.note{color:var(--muted);font-size:.9rem;border-top:1px solid var(--line);padding-top:14px}
${css(loader(readdirSync(join(root, 'carrousels')).sort()[0]).design)}
</style>
<div class="wrap">
<header><span class="eyebrow">Test du moteur de carrousel</span><h1>${esc(A.h1 ?? D0.marque)}</h1>
<p class="lede">${esc(A.intro ?? '')}</p></header>
${sections.join('\n')}
<p class="note">${esc(A.note ?? '')}</p>
</div>
<script>
(function(){
  function fit(){document.querySelectorAll('.frame').forEach(function(f){f.querySelector('.scale').style.setProperty('--s',f.clientWidth/${W});});}
  fit();window.addEventListener('resize',fit);
  var go=function(){${fitScript}};if(document.fonts&&document.fonts.ready){document.fonts.ready.then(go);}else{go();}
  if(window.ResizeObserver){document.querySelectorAll('.frame').forEach(function(f){new ResizeObserver(fit).observe(f);});}
})();
</script>`;
// Dédoublonne les photos embarquées : chaque image n'est écrite qu'une fois.
const uniq = new Map();
html = html.replace(/src="data:image\/jpeg;base64,([A-Za-z0-9+/=]+)"/g, (m, b64) => {
  if (!uniq.has(b64)) uniq.set(b64, uniq.size);
  return `data-img="${uniq.get(b64)}"`;
});
const imgs = [...uniq.keys()];
html = html.replace('<script>', `<script>window.IMGS=${JSON.stringify(imgs)};document.querySelectorAll('img[data-img]').forEach(function(i){i.src='data:image/jpeg;base64,'+window.IMGS[+i.getAttribute('data-img')];});</script>\n<script>`);
writeFileSync(outFile, html);
console.log('ok', outFile, Math.round(html.length / 1024) + ' KB');
