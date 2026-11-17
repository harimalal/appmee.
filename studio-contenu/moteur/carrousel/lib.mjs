// Moteur de carrousel : commun à tous les clients.
// Entrées : design.json + template + carrousel.json (+ photos du client). Sortie : slides HTML 1080x1350.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
export const W = 1080;
export const H = 1350;

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// [[texte]] = donnée manquante (repère jaune, jamais inventée). *mot* = mot mis en valeur.
const rich = (s) =>
  esc(s)
    .replace(/'/g, '’')
    .replace(/\[\[(.+?)\]\]/g, '<span class="todo">$1</span>')
    .replace(/\*(.+?)\*/g, '<mark>$1</mark>')
    .replace(/\n/g, '<br>');

// Charge design + template + carrousel et fusionne : le template donne la structure (layout, type, fond),
// le carrousel donne le contenu et les photos.
export function load(root) {
  return (slug) => {
    const design = JSON.parse(readFileSync(join(root, 'design.json'), 'utf8'));
    const carousel = JSON.parse(readFileSync(join(root, 'carrousels', slug, 'carrousel.json'), 'utf8'));
    const tplFile = join(root, 'templates', `${carousel.template}.json`);
    const tpl = existsSync(tplFile) ? JSON.parse(readFileSync(tplFile, 'utf8')) : { slides: [] };
    carousel.slides = carousel.slides.map((c, i) => ({ ...(tpl.slides[i] ?? {}), ...c }));
    return { design, carousel, root };
  };
}

function fontFace() {
  const b64 = (f) => readFileSync(join(here, 'fonts', f)).toString('base64');
  return `@font-face{font-family:"Bricolage Grotesque";font-weight:700;src:url(data:font/woff2;base64,${b64('bricolage-700.woff2')}) format("woff2")}
@font-face{font-family:"DM Sans";font-weight:400 700;src:url(data:font/woff2;base64,${b64('dmsans-var.woff2')}) format("woff2")}`;
}

export function css(design) {
  const c = design.couleurs;
  const T = `"${design.polices.titre}",system-ui,sans-serif`;
  return `${fontFace()}
.slide{--encre:${c.encre};--papier:${c.papier};position:relative;width:${W}px;height:${H}px;overflow:hidden;
  font-family:"${design.polices.texte}",system-ui,sans-serif;color:var(--encre);background:var(--papier);box-sizing:border-box}
.slide *{box-sizing:border-box}
.slide.fond-fruit{background:var(--f);color:var(--ft)}
.slide.fond-encre{background:var(--encre);color:var(--papier)}
.slide h1,.slide h2{font-family:${T};font-weight:700;margin:0;letter-spacing:-0.025em;line-height:.98}
mark{white-space:nowrap;background:var(--f);color:var(--ft);padding:0 .14em;border-radius:.1em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.fond-fruit mark{background:var(--encre);color:var(--papier)}
.kicker{align-self:flex-start;display:inline-block;font-size:28px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;background:var(--f);color:var(--ft);padding:10px 22px;border-radius:99px}
.fond-fruit .kicker{background:var(--encre);color:var(--papier)}
.corps{font-size:42px;line-height:1.36;margin:0}
.todo{display:inline-block;margin:8px 0;font-size:.6em;font-weight:700;letter-spacing:.05em;text-transform:uppercase;background:#FFE08A;color:#4A3500;border-radius:8px;padding:.08em .5em;line-height:1.5;mark &{background:none}}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.bar{position:absolute;left:72px;right:72px;top:60px;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#fff;z-index:3;text-shadow:0 2px 12px rgba(0,0,0,.35)}
.bar.sombre{color:var(--encre);text-shadow:none}
.fond-fruit .bar.sombre{color:var(--ft)}
.arrow{position:absolute;right:72px;bottom:64px;width:96px;height:96px;border-radius:50%;background:var(--f);color:var(--ft);display:flex;align-items:center;justify-content:center;font-size:52px;z-index:3}
.fond-fruit .arrow{background:var(--encre);color:var(--papier)}

/* cover-photo : photo plein cadre, titre géant en bas */
.l-cover-photo .scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(20,8,14,.94) 0%,rgba(20,8,14,.72) 34%,rgba(20,8,14,.0) 68%),linear-gradient(to bottom,rgba(20,8,14,.62) 0%,rgba(20,8,14,0) 22%)}
.l-cover-photo .txt{position:absolute;left:72px;right:72px;bottom:96px;display:flex;flex-direction:column;gap:30px;color:#fff;z-index:2}
.l-cover-photo h1{font-size:190px;color:#fff}
.l-cover-photo .sous{font-size:46px;line-height:1.25;margin:0;max-width:760px}
/* plein : photo plein cadre, titre + légende */
.l-plein .scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(20,8,14,.92) 0%,rgba(20,8,14,.6) 40%,rgba(20,8,14,0) 70%),linear-gradient(to bottom,rgba(20,8,14,.45) 0%,rgba(20,8,14,0) 16%)}
.l-plein .txt{position:absolute;left:72px;right:130px;bottom:96px;display:flex;flex-direction:column;gap:26px;color:#fff;z-index:2}
.l-plein h2{font-size:150px;color:#fff}
.l-plein .corps{font-size:40px}
/* arche : photo en arche, texte dessous */
.l-arche{padding:130px 72px 72px;display:flex;flex-direction:column;gap:40px}
.l-arche .arche{width:100%;height:560px;border-radius:468px 468px 28px 28px;overflow:hidden;position:relative;flex:none}
.l-arche h2{font-size:112px}
.l-arche .corps{max-width:900px;font-size:44px}
.l-arche .arrow{bottom:56px}
.l-arche .txtw{display:flex;flex-direction:column;gap:26px;flex:1;min-height:0;padding-right:120px}
/* bande : photo en bandeau, titre chevauchant, liste */
.l-bande .bandeau{position:absolute;left:0;right:0;top:0;height:470px;overflow:hidden}
.l-bande .bandeau::after{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(20,8,14,.4) 0,rgba(20,8,14,0) 28%)}
.l-bande .corpsb{position:absolute;left:0;right:0;top:420px;bottom:0;padding:0 72px 150px;display:flex;flex-direction:column;gap:40px}
.l-bande h2{align-self:flex-start;background:var(--f);color:var(--ft);padding:22px 38px;font-size:90px;border-radius:6px;max-width:100%;overflow:visible}
.l-bande h2 mark{background:var(--encre);color:var(--papier)}
.liste{display:flex;flex-direction:column;gap:44px;margin-top:10px}
.item{display:grid;grid-template-columns:110px 1fr;gap:26px;align-items:start}
.item .n{font-family:${T};font-weight:700;font-size:112px;line-height:.86;color:var(--f)}
.item .t{font-size:58px;font-weight:700;line-height:1.08;margin-bottom:6px}
.item .d{font-size:42px;line-height:1.32;opacity:.9}
.l-bande .arrow{width:80px;height:80px;font-size:42px;bottom:48px}
/* duo : photo teintée de la couleur du fruit, titre géant */
.l-duo .teinte{position:absolute;inset:0;background:var(--f);mix-blend-mode:multiply;opacity:.9}
.l-duo .scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(20,8,14,.8) 0%,rgba(20,8,14,.2) 55%,rgba(20,8,14,.35) 100%)}
.l-duo .txt{position:absolute;left:72px;right:72px;bottom:110px;display:flex;flex-direction:column;gap:34px;color:#fff;z-index:2}
.l-duo h2{font-size:170px;color:#fff}
.l-duo mark{background:#fff;color:var(--f)}
.l-duo .corps{font-size:42px}
.l-duo .marque{font-family:${T};font-weight:700;font-size:44px;letter-spacing:-.01em}
/* chiffre : donnée géante sur fond de couleur */
.l-chiffre{padding:150px 72px 72px;display:flex;flex-direction:column;justify-content:center;gap:40px}
.l-chiffre .chiffre{font-family:${T};font-weight:700;font-size:400px;line-height:.82;letter-spacing:-0.05em;margin-left:-14px}
.l-chiffre .arrow{bottom:64px}
/* texte seul, sans photo (rétro-compatible) */
.l-texte{padding:150px 72px 72px;display:flex;flex-direction:column;justify-content:center;gap:40px}
.l-texte h2{font-size:120px}
`.replace('mark &{background:none}', '');
}

function imgTag(s, root, cls = 'bg') {
  const f = s.image?.fichier;
  if (!f) return '';
  const p = join(root, 'assets', 'unsplash', f);
  const data = readFileSync(p).toString('base64');
  return `<img class="${cls}" alt="" src="data:image/jpeg;base64,${data}" style="object-position:${s.image.pos ?? '50% 50%'}">`;
}

const bar = (i, n, design, sombre = false) =>
  `<div class="bar${sombre ? ' sombre' : ''}"><span>${esc(design.marque)}</span><span>${i + 1} / ${n}</span></div>`;
const arrow = (i, n) => (i < n - 1 ? '<div class="arrow">→</div>' : '');
const fit = (max, maxh) => `data-fit="${max}" data-maxh="${maxh}"`;

function inner(s, i, n, design, root) {
  const kick = s.kicker ? `<span class="kicker">${rich(s.kicker)}</span>` : '';
  switch (s.layout) {
    case 'cover-photo':
      return `${imgTag(s, root)}<div class="scrim"></div>${bar(i, n, design)}
<div class="txt">${kick}<h1 ${fit(190, 560)}>${rich(s.titre)}</h1>${s.sous ? `<p class="sous">${rich(s.sous)}</p>` : ''}</div>${arrow(i, n)}`;
    case 'plein':
      return `${imgTag(s, root)}<div class="scrim"></div>${bar(i, n, design)}
<div class="txt">${kick}<h2 ${fit(150, 440)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}</div>${arrow(i, n)}`;
    case 'arche':
      return `${bar(i, n, design, true)}<div class="arche">${imgTag(s, root)}</div>
<div class="txtw">${kick}<h2 ${fit(112, 230)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}</div>${arrow(i, n)}`;
    case 'bande':
      return `<div class="bandeau">${imgTag(s, root)}</div>${bar(i, n, design)}
<div class="corpsb"><h2>${rich(s.titre)}</h2><div class="liste">${(s.items ?? [])
        .map((it, k) => `<div class="item"><div class="n">${k + 1}</div><div><div class="t">${rich(it.t)}</div>${it.d ? `<div class="d">${rich(it.d)}</div>` : ''}</div></div>`)
        .join('')}</div></div>${arrow(i, n)}`;
    case 'duo':
      return `${imgTag(s, root)}<div class="teinte"></div><div class="scrim"></div>${bar(i, n, design)}
<div class="txt">${kick}<h2 ${fit(170, 520)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}<div class="marque">${esc(design.marque)} · ${esc(design.signature)}</div></div>`;
    case 'chiffre':
      return `${bar(i, n, design, true)}<div class="chiffre">${rich(s.valeur)}</div><p class="corps">${rich(s.texte)}</p>${arrow(i, n)}`;
    default:
      return `${bar(i, n, design, true)}${kick}<h2 ${fit(120, 360)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}${arrow(i, n)}`;
  }
}

export function slideHtml(s, i, n, design, carousel, root) {
  const layout = s.layout ?? 'texte';
  const fond = s.fond ?? 'papier';
  const cls = ['slide', `l-${layout}`, fond === 'fruit' ? 'fond-fruit' : fond === 'encre' ? 'fond-encre' : ''].join(' ');
  const p = design.couleurs.fruits[carousel.fruit] ?? Object.values(design.couleurs.fruits)[0];
  return `<section class="${cls}" style="--f:${p.fond};--ft:${p.texte}">${inner({ ...s, layout }, i, n, design, root)}</section>`;
}

export function slides(design, carousel, root) {
  const n = carousel.slides.length;
  return carousel.slides.map((s, i) => slideHtml(s, i, n, design, carousel, root));
}

// Réduit la taille des titres jusqu'à ce qu'ils tiennent (à appeler une fois les polices chargées).
export const fitScript = `(function(){document.querySelectorAll('[data-fit]').forEach(function(el){var s=parseInt(el.getAttribute('data-fit'),10),mh=parseInt(el.getAttribute('data-maxh'),10);el.style.fontSize=s+'px';var g=0;while((el.offsetHeight>mh||el.scrollWidth>el.clientWidth+1)&&s>48&&g++<90){s-=4;el.style.fontSize=s+'px';}});})();`;

export function printPage(design, carousel, root) {
  return `<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>@page{size:${W}px ${H}px;margin:0}html,body{margin:0}
.slide{break-after:page;page-break-after:always}${css(design)}</style></head><body>${slides(design, carousel, root).join('')}</body></html>`;
}
