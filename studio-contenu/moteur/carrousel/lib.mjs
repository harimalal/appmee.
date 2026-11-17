// Moteur de carrousel : commun à tous les clients.
// Entrées : design.json du client + carrousel.json. Sortie : HTML des slides (1080x1350).
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
export const W = 1080;
export const H = 1350;

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// [[texte]] = donnée manquante, rendue comme un repère « à compléter » (jamais inventée).
const rich = (s) => esc(s).replace(/'/g, '\u2019').replace(/\[\[(.+?)\]\]/g, '<span class="todo">$1</span>').replace(/\n/g, '<br>');

function fontFace() {
  const b64 = (f) => readFileSync(join(here, 'fonts', f)).toString('base64');
  return `
@font-face{font-family:"Bricolage Grotesque";font-weight:700;src:url(data:font/woff2;base64,${b64('bricolage-700.woff2')}) format("woff2")}
@font-face{font-family:"DM Sans";font-weight:400 700;src:url(data:font/woff2;base64,${b64('dmsans-var.woff2')}) format("woff2")}`;
}

export function css(design) {
  const c = design.couleurs;
  return `${fontFace()}
.slide{--encre:${c.encre};--papier:${c.papier};position:relative;width:${W}px;height:${H}px;overflow:hidden;
  font-family:"${design.polices.texte}",system-ui,sans-serif;color:var(--encre);background:var(--papier);
  display:flex;flex-direction:column;padding:96px 88px 80px;box-sizing:border-box}
.slide *{box-sizing:border-box}
.slide.fond-fruit{background:var(--f);color:var(--ft)}
.slide.fond-encre{background:var(--encre);color:var(--papier)}
.slide h1,.slide h2{font-family:"${design.polices.titre}",system-ui,sans-serif;font-weight:700;margin:0;letter-spacing:-0.02em;line-height:1.02}
.kicker{font-size:30px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:36px}
.slide:not(.fond-fruit):not(.fond-encre) .kicker{color:var(--f)}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px;min-height:0}
.t-cover h1{font-size:132px}
.t-cover .sous{font-size:44px;line-height:1.3;max-width:800px;opacity:.95}
h2{font-size:84px}
.corps{font-size:42px;line-height:1.38;max-width:860px}
.liste{display:flex;flex-direction:column;gap:34px;margin-top:8px}
.item{display:grid;grid-template-columns:110px 1fr;gap:28px;align-items:start}
.item .n{font-family:"${design.polices.titre}",sans-serif;font-weight:700;font-size:104px;line-height:.9;color:var(--f)}
.fond-fruit .item .n{color:var(--ft)}
.item .t{font-size:54px;font-weight:700;line-height:1.1;margin-bottom:8px}
.item .d{font-size:40px;line-height:1.35;opacity:.9}
.chiffre{font-family:"${design.polices.titre}",sans-serif;font-weight:700;font-size:280px;line-height:.9;letter-spacing:-0.04em}
.etape .num{font-family:"${design.polices.titre}",sans-serif;font-weight:700;font-size:260px;line-height:.8;color:var(--f)}
.fond-fruit .etape .num{color:var(--ft)}
.photo{flex:1;min-height:420px;border:4px dashed currentColor;border-radius:24px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;text-align:center;padding:40px;opacity:.8}
.photo b{font-size:30px;letter-spacing:.14em;text-transform:uppercase}
.photo span{font-size:38px;line-height:1.3;max-width:700px}
.photo-wrap{display:flex;flex-direction:column;gap:36px;flex:1;min-height:0;justify-content:center}
.todo{display:inline-block;margin:10px 0;font-size:.62em;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:#FFE08A;color:#4A3500;border-radius:8px;padding:.08em .5em;vertical-align:middle;line-height:1.5}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-top:40px}
.foot .pg{display:flex;gap:20px;align-items:center}
.foot .fl{font-size:44px;letter-spacing:0}
.fond-encre .accent,.cta .accent{color:var(--f)}
`;
}

function palette(design, nom) {
  const p = design.couleurs.fruits[nom] ?? Object.values(design.couleurs.fruits)[0];
  return `--f:${p.fond};--ft:${p.texte}`;
}

function inner(s) {
  switch (s.type) {
    case 'cover':
      return `<div class="main cover">${s.kicker ? `<div class="kicker">${rich(s.kicker)}</div>` : ''}<h1>${rich(s.titre)}</h1>${s.sous ? `<p class="sous">${rich(s.sous)}</p>` : ''}</div>`;
    case 'texte':
      return `<div class="main">${s.kicker ? `<div class="kicker">${rich(s.kicker)}</div>` : ''}<h2>${rich(s.titre)}</h2><p class="corps">${rich(s.texte)}</p></div>`;
    case 'liste':
      return `<div class="main"><h2>${rich(s.titre)}</h2><div class="liste">${s.items
        .map((it, i) => `<div class="item"><div class="n">${i + 1}</div><div><div class="t">${rich(it.t)}</div>${it.d ? `<div class="d">${rich(it.d)}</div>` : ''}</div></div>`)
        .join('')}</div></div>`;
    case 'etape':
      return `<div class="main etape"><div class="num">${rich(s.numero)}</div><h2>${rich(s.titre)}</h2><p class="corps">${rich(s.texte)}</p></div>`;
    case 'chiffre':
      return `<div class="main"><div class="chiffre">${rich(s.valeur)}</div><p class="corps">${rich(s.texte)}</p></div>`;
    case 'photo':
      return `<div class="photo-wrap"><h2>${rich(s.titre)}</h2><div class="photo"><b>Photo de Pascal</b><span>${rich(s.consigne)}</span></div>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}</div>`;
    case 'cta':
      return `<div class="main"><h2>${rich(s.titre)}</h2><p class="corps">${rich(s.texte)}</p></div>`;
    default:
      throw new Error(`Type de slide inconnu : ${s.type}`);
  }
}

export function slideHtml(s, i, n, design, carousel) {
  const fond = s.fond ?? (s.type === 'cover' ? 'fruit' : s.type === 'cta' ? 'encre' : 'papier');
  const cls = ['slide', 't-' + s.type, fond === 'fruit' ? 'fond-fruit' : fond === 'encre' ? 'fond-encre' : ''].join(' ');
  const last = i === n - 1;
  return `<section class="${cls}" style="${palette(design, carousel.fruit)}">${inner(s)}
<div class="foot"><span>${esc(design.marque)}</span><span class="pg">${i + 1} / ${n}${last ? '' : '<span class="fl">→</span>'}</span></div></section>`;
}

export function slides(design, carousel) {
  const n = carousel.slides.length;
  return carousel.slides.map((s, i) => slideHtml(s, i, n, design, carousel));
}

export function printPage(design, carousel) {
  return `<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>@page{size:${W}px ${H}px;margin:0}html,body{margin:0}
.slide{break-after:page;page-break-after:always}${css(design)}</style></head><body>${slides(design, carousel).join('')}</body></html>`;
}
