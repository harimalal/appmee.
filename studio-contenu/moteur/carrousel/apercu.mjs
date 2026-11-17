// Usage : node apercu.mjs <dossier-client> <fichier-sortie.html>
// Génère une page d'aperçu (tous les carrousels d'un client) à partir des carrousel.json.
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { css, slides, W, H } from './lib.mjs';

const [clientDir, outFile] = process.argv.slice(2);
const root = resolve(clientDir);
const design = JSON.parse(readFileSync(join(root, 'design.json'), 'utf8'));
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const todos = (c) => [...JSON.stringify(c.slides).matchAll(/\[\[(.+?)\]\]/g)].map((m) => m[1].replace(/\\u2019/g, '’'));

const sections = readdirSync(join(root, 'carrousels')).sort().map((slug) => {
  const c = JSON.parse(readFileSync(join(root, 'carrousels', slug, 'carrousel.json'), 'utf8'));
  const t = todos(c);
  return `<section class="car">
  <header><span class="tpl">Template : ${esc(c.template)}</span><h2>${esc(c.titre_interne)}</h2></header>
  <div class="rail" tabindex="0" aria-label="Slides de ${esc(c.titre_interne)}">${slides(design, c).map((h) => `<div class="frame"><div class="scale">${h}</div></div>`).join('')}</div>
  <div class="meta">
    <div><h3>Légende proposée</h3><p>${esc(c.legende).replace(/\[\[(.+?)\]\]/g, '<span class="todo-i">$1</span>')}</p></div>
    <div><h3>À compléter par Pascal</h3>${t.length ? `<ul>${t.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : '<p>Rien.</p>'}</div>
  </div>
</section>`;
});

const html = `<meta name="claude:viewport-fit-sides" content="cover">
<title>Carrousels Les Confits</title>
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
${css(design)}
</style>
<div class="wrap">
<header><span class="eyebrow">Test du moteur de carrousel</span><h1>Les Confits</h1>
<p class="lede">Trois carrousels produits par le même moteur, avec le pack client des Confits : voix, design, thématiques et verrous. Les zones jaunes sont des informations que seul Pascal peut donner, elles ne sont pas inventées.</p></header>
${sections.join('\n')}
<p class="note">Format 1080 × 1350 (4:5) pour Instagram et LinkedIn. Les images PNG et le PDF de chaque carrousel sont dans le dépôt, dossier studio-contenu/clients/confits/carrousels. Brouillons : rien n'est publié.</p>
</div>
<script>
(function(){
  function fit(){document.querySelectorAll('.frame').forEach(function(f){f.querySelector('.scale').style.setProperty('--s',f.clientWidth/${W});});}
  fit();window.addEventListener('resize',fit);
  if(window.ResizeObserver){document.querySelectorAll('.frame').forEach(function(f){new ResizeObserver(fit).observe(f);});}
})();
</script>`;
writeFileSync(outFile, html);
console.log('ok', outFile, Math.round(html.length / 1024) + ' KB');
