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
    .replace(/ ([?!:;»])/g, '\u00A0$1')
    .replace(/(«) /g, '$1\u00A0')
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

const FONTS = {
  'Bricolage Grotesque': [[700, 'bricolage-700.woff2'], [800, 'bricolage-800.woff2']],
  'DM Sans': [['400 700', 'dmsans-var.woff2']],
  Figtree: [['400 700', 'figtree-var.woff2']]
};
function fontFace(design) {
  const b64 = (f) => readFileSync(join(here, 'fonts', f)).toString('base64');
  const names = [...new Set([design.polices.titre, design.polices.texte])];
  return names
    .flatMap((n) => (FONTS[n] ?? []).map(([w, f]) => `@font-face{font-family:"${n}";font-weight:${w};src:url(data:font/woff2;base64,${b64(f)}) format("woff2")}`))
    .join('\n');
}


function clairCss(design, T) {
  const ch = design.charte;
  if (!ch) return '';
  const B = `"${design.polices.texte}",system-ui,sans-serif`;
  return `
/* clair : charte « claire » (fond crème, encre verte, surligneur jaune, arches) */
.l-clair,.l-clair-photo{--cc-card:${ch.card};--cc-ink:${ch.ink};--cc-ink2:${ch.ink2};--cc-ink3:${ch.ink3};--cc-accent:${ch.accent};--cc-accent-ink:${ch.accentInk};--cc-sun:${ch.sun};--cc-mark:${ch.mark};--cc-band:${ch.band};--cc-step:${ch.step};--cc-edge:${ch.edge};
  font-family:${B};padding:60px 72px 72px;display:flex;flex-direction:column}
.l-clair{background:radial-gradient(900px 700px at 105% -5%,rgba(255,218,110,.40),transparent 60%),radial-gradient(800px 700px at -10% 105%,rgba(176,208,170,.38),transparent 60%),${ch.bg};color:${ch.ink}}
/* clair-photo : photo plein cadre + charte (logo, surligneur jaune, cartes, bouton) */
.l-clair-photo{color:#fff;background:${ch.ink}}
.l-clair-photo .scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(10,32,20,.94) 0%,rgba(10,32,20,.72) 42%,rgba(10,32,20,.16) 72%),linear-gradient(to bottom,rgba(10,32,20,.6) 0%,rgba(10,32,20,0) 20%)}
.l-clair-photo.p-haut .scrim{background:linear-gradient(to bottom,rgba(10,32,20,.94) 0%,rgba(10,32,20,.72) 46%,rgba(10,32,20,.14) 82%)}
.l-clair-photo.p-centre .scrim{background:rgba(10,32,20,.62)}
.l-clair-photo .cl-head{position:relative;z-index:2}
.l-clair-photo .cl-head b,.l-clair-photo .cl-pg{color:#fff}
.l-clair-photo .cl-head small{color:rgba(255,255,255,.86)}
.l-clair-photo .cl-logo .m1{fill:${ch.bg}}
.l-clair-photo .cl-body{position:relative;z-index:2}
.l-clair-photo .cl-next{color:var(--cc-sun);z-index:2}
.slide.l-clair-photo h1,.slide.l-clair-photo h2{color:#fff;text-shadow:0 2px 24px rgba(0,0,0,.35)}
.slide.l-clair-photo mark{background:var(--cc-sun);color:${ch.ink};text-shadow:none;padding:0 .14em;margin:0 -.04em;border-radius:8px 4px 10px 4px}
.l-clair-photo .cl-eyebrow{background:var(--cc-mark);color:${ch.ink}}
.l-clair-photo .cl-texte{color:rgba(255,255,255,.96);text-shadow:0 2px 18px rgba(0,0,0,.4)}
.l-clair-photo .cl-gar{color:#fff}
.l-clair-photo .cl-src,.l-clair-photo .cl-mention{color:rgba(255,255,255,.84)}
.l-clair-photo .cl-card{color:${ch.ink}}
.l-clair-photo .cl-card h3{color:${ch.ink}}
.cl-body.air{gap:46px}
.cl-fig{display:flex;flex-direction:column;gap:30px;align-items:flex-start}
.cl-fig-num{font-family:${T};font-weight:800;font-size:250px;letter-spacing:-.05em;line-height:.92;color:var(--cc-accent-ink);white-space:nowrap;max-width:100%}
.cl-fig-num sup{font-size:.2em;font-weight:600;color:var(--cc-ink3);vertical-align:top;letter-spacing:0;margin-left:.12em}
.cl-wave{width:112px;height:44px}
.cl-fig-leg{font-size:56px;line-height:1.26;color:var(--cc-ink);margin:0;max-width:860px;font-weight:600}
.cl-fig-det{font-size:40px;line-height:1.3;color:var(--cc-ink3);margin:0;max-width:860px}
.cl-viz{width:100%;height:auto;margin-top:14px;display:block}
.cl-viz text{font-family:inherit}
.cl-viz.globe{width:230px;margin-top:0}
.cl-body.bas{justify-content:flex-end}
.cl-body.centre{justify-content:center}
.cl-body .cl-badge{position:static;align-self:flex-start}
.cl-photo{position:relative;flex:none;margin:14px 20px 8px 0}
.cl-photo::after{content:"";position:absolute;right:-20px;top:-14px;left:36px;bottom:30px;background:var(--cc-sun);border-radius:34px 64px 34px 34px;z-index:0}
.cl-photo-in{position:absolute;inset:0;border-radius:34px;overflow:hidden;z-index:1;box-shadow:0 26px 50px -28px rgba(18,48,31,.55)}
.cl-photo-in img{width:100%;height:100%;object-fit:cover}
.cl-head{display:flex;align-items:center;gap:18px;flex:none}
.cl-logo{width:68px;height:68px;flex:none}
.cl-head b{display:block;font-family:${T};font-weight:800;font-size:38px;letter-spacing:-.01em;line-height:1.05}
.cl-head small{display:block;font-size:22px;color:var(--cc-ink2);margin-top:2px}
.cl-pg{margin-left:auto;font-size:26px;font-weight:700;color:var(--cc-ink3)}
.cl-body{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:safe center;gap:26px;position:relative;padding-top:16px;padding-bottom:78px}
.cl-body.haut{justify-content:flex-start;padding-top:56px}
.cl-eyebrow{align-self:flex-start;font-size:28px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--cc-accent-ink);background:linear-gradient(transparent 52%,var(--cc-mark) 52%,var(--cc-mark) 94%,transparent 94%);padding:2px 14px;border-radius:6px}
.l-clair h1,.l-clair h2,.l-clair-photo h1,.l-clair-photo h2{font-family:${T};font-weight:800;letter-spacing:-.03em;line-height:1;color:var(--cc-ink);margin:0}
.l-clair mark,.l-clair-photo mark{background:linear-gradient(transparent 52%,var(--cc-mark) 52%,var(--cc-mark) 94%,transparent 94%);color:inherit;padding:0 .12em;margin:0 -.04em;border-radius:6px 3px 8px 3px}
.cl-texte{font-size:52px;line-height:1.32;color:var(--cc-ink2);margin:0;max-width:900px}
.cl-texte.etroit{max-width:340px;font-size:42px}
.cl-card{background:var(--cc-card);border-radius:30px;padding:36px 40px;box-shadow:0 22px 46px -30px rgba(18,48,31,.35),0 2px 0 rgba(18,48,31,.04)}
.cl-card.band{background:var(--cc-band);box-shadow:0 22px 46px -30px rgba(18,48,31,.28)}
.cl-card h3{font-family:${T};font-weight:800;font-size:60px;letter-spacing:-.02em;line-height:1.05;margin:0 0 14px}
.cl-card p{font-size:48px;line-height:1.34;color:var(--cc-ink2);margin:0}
.cl-big{font-family:${T};font-weight:800;font-size:150px;letter-spacing:-.04em;line-height:.9;color:var(--cc-accent-ink)}
.cl-big small{display:block;font-family:${B};font-size:36px;letter-spacing:0;font-weight:700;color:var(--cc-ink);margin-top:14px}
.cl-big sup,.cl-stat sup{font-size:.4em;font-weight:600;color:var(--cc-ink3)}
.cl-svg{width:100%;height:auto;margin-top:22px;display:block}
.cl-svg text{font-family:inherit}
.cl-stats{display:flex;flex-direction:column;gap:16px}
.cl-stat{display:flex;align-items:center;gap:34px;background:var(--cc-card);border-radius:30px;padding:22px 34px;box-shadow:0 22px 46px -30px rgba(18,48,31,.35),0 2px 0 rgba(18,48,31,.04)}
.cl-stat b{font-family:${T};font-weight:800;font-size:96px;letter-spacing:-.03em;line-height:1;color:var(--cc-accent-ink);flex:0 0 auto;min-width:360px;white-space:nowrap}
.cl-stat span{font-size:40px;line-height:1.3;color:var(--cc-ink2);flex:1}
.cl-liste{display:flex;flex-direction:column;gap:20px}
.cl-item{display:flex;align-items:flex-start;gap:28px;background:var(--cc-card);border-radius:30px;padding:30px 36px;box-shadow:0 22px 46px -30px rgba(18,48,31,.35),0 2px 0 rgba(18,48,31,.04)}
.cl-num,.cl-ck{flex:none;width:88px;height:88px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:${T};font-weight:800;font-size:48px;background:var(--cc-step);color:var(--cc-ink)}
.cl-item:nth-child(2) .cl-num{background:var(--cc-sun)}
.cl-ck{background:var(--cc-accent);width:72px;height:72px;margin-top:4px}
.cl-ck svg{width:34px;height:34px;stroke:#fff;fill:none;stroke-width:3.6;stroke-linecap:round;stroke-linejoin:round}
.cl-item b{display:block;font-family:${T};font-weight:800;font-size:54px;letter-spacing:-.015em;line-height:1.1}
.cl-item p{font-size:40px;line-height:1.3;color:var(--cc-ink2);margin:8px 0 0}
.cl-btn{align-self:flex-start;display:inline-flex;align-items:center;gap:18px;font-family:${T};font-weight:800;font-size:50px;letter-spacing:-.005em;padding:34px 56px;border-radius:999px;background:var(--cc-sun);color:var(--cc-ink);box-shadow:0 4px 0 var(--cc-edge),0 24px 40px -20px rgba(240,196,40,.75)}
.cl-btn svg{width:52px;height:52px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.cl-gar{display:flex;flex-wrap:wrap;gap:14px 30px;font-size:32px;font-weight:600;color:var(--cc-ink2)}
.cl-gar span{display:inline-flex;align-items:center;gap:12px}
.cl-gar i{width:36px;height:36px;border-radius:50%;background:var(--cc-accent);display:inline-flex;align-items:center;justify-content:center}
.cl-gar svg{width:20px;height:20px;stroke:#fff;fill:none;stroke-width:3.6;stroke-linecap:round;stroke-linejoin:round}
.cl-src{font-size:26px;line-height:1.35;color:var(--cc-ink3);margin:0;padding-right:90px}
.cl-mention{font-size:28px;line-height:1.35;color:var(--cc-ink3);margin:0;max-width:900px}
.cl-next{position:absolute;right:72px;bottom:60px;font-size:60px;color:var(--cc-accent);font-weight:700;line-height:1}
.cl-arche{position:absolute;right:92px;bottom:130px;width:460px;height:540px}
.cl-arche::before{content:"";position:absolute;left:-26px;top:-26px;width:100%;height:100%;border:4px solid var(--cc-accent);border-bottom:0;border-radius:230px 230px 0 0;z-index:3;pointer-events:none}
.cl-arche::after{content:"";position:absolute;right:-40px;bottom:-30px;width:94%;height:94%;background:var(--cc-sun);border-radius:70px 230px 40px 40px;z-index:0}
.cl-arche-in{position:absolute;inset:0;border-radius:230px 230px 36px 36px;overflow:hidden;z-index:1;box-shadow:0 30px 60px -30px rgba(18,48,31,.5)}
.cl-arche-in img{width:100%;height:100%;object-fit:cover}
.cl-bande{position:absolute;left:0;right:0;overflow:hidden;z-index:0;box-shadow:0 30px 60px -34px rgba(18,48,31,.5)}
.cl-bande img{width:100%;height:100%;object-fit:cover;display:block}
.cl-bande.haut{top:0;border-radius:0 0 72px 72px}
.cl-bande.haut::after{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(10,32,20,.55) 0%,rgba(10,32,20,0) 34%)}
.cl-bande.bas{bottom:0;border-radius:72px 72px 0 0}
.bd-haut .cl-head,.bd-bas .cl-head{position:relative;z-index:2}
.bd-haut .cl-head b,.bd-haut .cl-pg{color:#fff}
.bd-haut .cl-head small{color:rgba(255,255,255,.9)}
.bd-haut .cl-logo .m1{fill:${ch.bg}}
.bd-bas .cl-next{color:#fff;z-index:3}
.bd-bas .cl-body,.bd-haut .cl-body{position:relative;z-index:2}
.cl-schema{margin:0 auto;flex:none;width:100%}
.cl-schema .cl-svg{margin-top:0}
.cl-photos{display:flex;gap:22px;align-items:flex-end;margin:6px 0 4px}
.cl-ph{flex:1;position:relative;border-radius:999px 999px 30px 30px;overflow:hidden;box-shadow:0 26px 50px -28px rgba(18,48,31,.55)}
.cl-ph img{width:100%;height:100%;object-fit:cover;display:block}
.cl-ph em{position:absolute;left:50%;bottom:16px;transform:translateX(-50%);font-style:normal;font-weight:700;font-size:28px;color:${ch.ink};background:var(--cc-card);padding:6px 20px;border-radius:999px;white-space:nowrap;box-shadow:0 8px 20px -10px rgba(18,48,31,.5)}
.cl-badge{position:absolute;left:-120px;bottom:70px;z-index:4;background:var(--cc-card);border-radius:24px;padding:18px 26px;display:flex;align-items:center;gap:18px;box-shadow:0 20px 40px -22px rgba(18,48,31,.5)}
.cl-badge b{font-family:${T};font-weight:800;font-size:64px;letter-spacing:-.03em;color:var(--cc-accent-ink);line-height:1}
.cl-badge span{font-size:22px;line-height:1.25;color:var(--cc-ink2);max-width:210px}
`;
}

export function css(design) {
  const c = design.couleurs;
  const T = `"${design.polices.titre}",system-ui,sans-serif`;
  return `${fontFace(design)}
.slide{--encre:${c.encre};--papier:${c.papier};position:relative;width:${W}px;height:${H}px;overflow:hidden;
  font-family:"${design.polices.texte}",system-ui,sans-serif;color:var(--encre);background:var(--papier);box-sizing:border-box}
.slide *{box-sizing:border-box}
.slide{--mkbg:var(--f);--mkfg:var(--ft);--mkline:var(--f);--mkstroke:var(--f);--mkbg2:var(--encre);--mkfg2:var(--papier)}
.l-cover-photo,.l-plein,.l-duo{--mkstroke:#fff;--mkbg2:#fff;--mkfg2:var(--f)}
.l-duo{--mkbg:#fff;--mkfg:var(--f);--mkline:#fff}
.slide.fond-fruit,.l-moitie .bas,.l-bande h2{--mkbg:var(--encre);--mkfg:var(--papier);--mkline:var(--encre);--mkstroke:var(--ft);--mkbg2:var(--papier);--mkfg2:var(--f)}
.slide.fond-fruit{background:var(--f);color:var(--ft)}
.slide.fond-encre{background:var(--encre);color:var(--papier)}
.slide h1,.slide h2{font-family:${T};font-weight:700;margin:0;letter-spacing:-0.025em;line-height:.98}
mark{white-space:nowrap;background:var(--mkbg);color:var(--mkfg);padding:0 .14em;border-radius:.1em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.mk-souligne mark{background:linear-gradient(var(--mkline),var(--mkline)) 0 94%/100% .17em no-repeat;color:inherit;padding:0}
.mk-contour mark{background:none;color:transparent;-webkit-text-stroke:.04em var(--mkstroke);padding:0}
.mk-pastille mark{display:inline-block;transform:rotate(-3deg);border-radius:.55em;padding:0 .3em}
.mk-blanc mark{background:var(--mkbg2);color:var(--mkfg2)}
.mk-couleur mark{background:none;color:var(--fc,var(--f));padding:0}
.mk-double mark{background:linear-gradient(var(--fc,var(--f)),var(--fc,var(--f))) 0 94%/100% .14em no-repeat;color:var(--fc,var(--f));padding:0}
.l-photo{--mkline:var(--fc);--mkstroke:#fff}
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
.l-bande .bandeau::after{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(20,8,14,.52) 0,rgba(20,8,14,0) 28%)}
.l-bande .corpsb{position:absolute;left:0;right:0;top:420px;bottom:0;padding:0 72px 150px;display:flex;flex-direction:column;gap:40px}
.l-bande h2{align-self:flex-start;background:var(--f);color:var(--ft);padding:22px 38px;font-size:90px;border-radius:6px;max-width:100%;overflow:visible}
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
.l-duo .corps{font-size:42px}
.l-duo .marque{font-family:${T};font-weight:700;font-size:44px;letter-spacing:-.01em}
/* chiffre : donnée géante sur fond de couleur */
.l-chiffre{padding:150px 72px 72px;display:flex;flex-direction:column;justify-content:center;gap:40px}
.l-chiffre .chiffre{font-family:${T};font-weight:700;font-size:400px;line-height:.82;letter-spacing:-0.05em;margin-left:-14px}
.l-chiffre .arrow{bottom:64px}
/* variantes : pos (bas|haut|centre), align (gauche|centre|droite), encart (bande : bloc|etiquette|contre|libre) */
.l-cover-photo.p-haut .txt,.l-duo.p-haut .txt,.l-plein.p-haut .txt{top:150px;bottom:auto}
.l-cover-photo.p-centre .txt,.l-duo.p-centre .txt,.l-plein.p-centre .txt{top:50%;bottom:auto;transform:translateY(-50%)}
.l-cover-photo.p-haut .scrim,.l-duo.p-haut .scrim,.l-plein.p-haut .scrim{background:linear-gradient(to bottom,rgba(20,8,14,.92) 0%,rgba(20,8,14,.6) 42%,rgba(20,8,14,.12) 100%)}
.l-cover-photo.p-centre .scrim,.l-plein.p-centre .scrim,.l-duo.p-centre .scrim{background:rgba(20,8,14,.58)}
.l-plein.a-droite .txt{right:72px}
.l-cover-photo.a-droite:not(.p-haut):not(.p-centre) .txt,.l-plein.a-droite:not(.p-haut):not(.p-centre) .txt{bottom:190px}
.a-centre .txt{align-items:center;text-align:center}
.a-droite .txt{align-items:flex-end;text-align:right}
.a-centre .kicker{align-self:center}
.a-droite .kicker{align-self:flex-end}
.l-bande.e-etiquette h2{transform:rotate(-3deg);transform-origin:left center;box-shadow:0 10px 30px rgba(20,8,14,.25)}
.l-bande.e-contre h2{background:var(--papier);color:var(--encre);border:6px solid var(--f)}
.l-bande.e-libre h2{background:none;color:var(--encre);padding:0;font-size:104px}
.l-bande.e-libre .corpsb{top:510px}
.l-bande.e-contre h2,.l-bande.e-libre h2{--mkbg:var(--f);--mkfg:var(--ft);--mkline:var(--f);--mkstroke:var(--f);--mkbg2:var(--encre);--mkfg2:var(--papier)}
/* carte : photo plein cadre, carte de texte posée dessus (liste-carte : la carte porte la liste) */
.l-carte .scrim,.l-liste-carte .scrim{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(20,8,14,.5) 0%,rgba(20,8,14,0) 26%,rgba(20,8,14,0) 60%,rgba(20,8,14,.4) 100%)}
.carte{position:absolute;left:72px;right:72px;bottom:170px;background:var(--papier);color:var(--encre);border-radius:40px;padding:52px 56px;display:flex;flex-direction:column;gap:24px;box-shadow:0 30px 80px rgba(0,0,0,.35);z-index:2}
.p-haut .carte{top:150px;bottom:auto}
.p-centre .carte{top:50%;bottom:auto;transform:translateY(-50%)}
.e-rotee .carte{transform:rotate(-2deg)}
.p-centre.e-rotee .carte{transform:translateY(-50%) rotate(-2deg)}
.carte h2{font-size:104px}
.carte .corps{font-size:42px}
.carte .liste{gap:28px;margin-top:0}
.carte .item{grid-template-columns:84px 1fr;gap:20px}
.carte .item .n{font-size:84px}
.carte .item .t{font-size:46px}
.carte .item .d{font-size:34px}
/* haut-texte : texte en haut, photo inclinée en bas */
.l-haut-texte{padding:150px 72px 72px;display:flex;flex-direction:column;gap:30px}
.l-haut-texte .txtw{display:flex;flex-direction:column;gap:24px}
.l-haut-texte h2{font-size:116px}
.l-haut-texte .corps{max-width:880px}
.l-haut-texte .cadre{margin-top:auto;height:500px;border-radius:28px;overflow:hidden;position:relative;transform:rotate(-2.5deg);box-shadow:0 24px 60px rgba(20,8,14,.3);flex:none}
/* moitie : photo sur une moitié, bloc de couleur sur l'autre */
.l-moitie .ph{position:absolute;left:0;right:0;top:0;height:640px;overflow:hidden}
.l-moitie .bas{position:absolute;left:0;right:0;top:640px;bottom:0;background:var(--f);color:var(--ft);padding:56px 72px 150px;display:flex;flex-direction:column;gap:24px}
.l-moitie.p-bas .ph{top:auto;bottom:0}
.l-moitie.p-bas .bas{top:0;bottom:640px;padding:150px 72px 50px}
.l-moitie .ph::after{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(20,8,14,.5) 0,rgba(20,8,14,0) 26%)}
.l-moitie h2{font-size:104px}
.l-moitie .kicker{background:var(--encre);color:var(--papier)}
.l-moitie .arrow{background:var(--encre);color:var(--papier);bottom:56px}
/* cercle : coupole de photo en bas, texte en haut */
.l-cercle .txtc{position:absolute;left:72px;right:72px;top:140px;display:flex;flex-direction:column;gap:24px}
.l-cercle h2{font-size:116px}
.l-cercle .rond{position:absolute;width:900px;height:900px;border-radius:50%;overflow:hidden;left:90px;bottom:-230px;box-shadow:0 0 0 18px var(--f)}
/* photo : image plein cadre, texte posé dessus sans fond ni cadre, le produit reste visible */
.l-photo .scrim{position:absolute;inset:0}
.l-photo.p-bas .scrim{background:linear-gradient(to top,rgba(10,4,8,.74) 0%,rgba(10,4,8,.4) 34%,rgba(10,4,8,0) 62%),linear-gradient(to bottom,rgba(10,4,8,.4) 0%,rgba(10,4,8,0) 14%)}
.l-photo.p-haut .scrim{background:linear-gradient(to bottom,rgba(10,4,8,.74) 0%,rgba(10,4,8,.4) 38%,rgba(10,4,8,0) 64%)}
.l-photo.p-centre .scrim{background:rgba(10,4,8,.42)}
.l-photo.p-bas.o-fort .scrim{background:linear-gradient(to top,rgba(10,4,8,.86) 0%,rgba(10,4,8,.56) 44%,rgba(10,4,8,0) 76%),linear-gradient(to bottom,rgba(10,4,8,.4) 0%,rgba(10,4,8,0) 14%)}
.l-photo.p-haut.o-fort .scrim{background:linear-gradient(to bottom,rgba(10,4,8,.9) 0%,rgba(10,4,8,.72) 50%,rgba(10,4,8,0) 82%)}
.l-photo .txt{position:absolute;left:72px;right:72px;display:flex;flex-direction:column;gap:26px;color:#fff;z-index:2;text-shadow:0 2px 26px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.45)}
.l-photo.p-bas .txt{bottom:150px}
.l-photo.p-haut .txt{top:150px}
.l-photo.p-centre .txt{top:50%;transform:translateY(-50%)}
.l-photo h1,.l-photo h2{color:#fff}
.l-photo .kick{font-size:28px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--fc);display:flex;align-items:center;gap:16px}
.l-photo .kick::before{content:"";width:56px;height:4px;background:var(--fc);flex:none}
.l-photo.a-centre .kick{justify-content:center}
.l-photo.a-droite .kick{flex-direction:row-reverse}
.l-photo .corps{font-size:44px;line-height:1.3;max-width:820px}
.l-photo .chiffre{font-family:${T};font-weight:700;font-size:340px;line-height:.85;letter-spacing:-0.05em;color:var(--fc)}
.l-photo .liste{gap:34px;margin-top:6px}
.l-photo .item{grid-template-columns:96px 1fr}
.l-photo .item .n{font-size:96px;color:var(--fc)}
.l-photo .item .t{font-size:52px}
.l-photo .item .d{font-size:38px;opacity:.95}
.l-photo .marque{font-family:${T};font-weight:700;font-size:44px;letter-spacing:-.01em}
.l-photo .marque span{color:var(--fc)}
.mention{font-size:28px;line-height:1.35;opacity:.85;max-width:880px;margin:6px 0 0}
/* typo : slide typographique sur fond uni (sombre par défaut), pour les contenus à lire */
.l-typo{padding:150px 72px 150px;display:flex;flex-direction:column;justify-content:center;--mkline:var(--fc)}
.l-typo.fond-encre{color:#fff}
.l-typo .txt-typo{display:flex;flex-direction:column;gap:34px}
.l-typo .kick,.l-photo .kick{font-size:28px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--fc);display:flex;align-items:center;gap:16px}
.l-typo .kick::before{content:"";width:56px;height:4px;background:var(--fc);flex:none}
.l-typo.fond-fruit .kick{color:var(--ft)}
.l-typo.fond-fruit .kick::before{background:var(--ft)}
.l-typo h2{font-size:130px}
.l-typo .corps{font-size:48px;line-height:1.32;max-width:900px}
.l-typo .liste{gap:38px;margin-top:6px}
.l-typo .item{grid-template-columns:96px 1fr}
.l-typo .item .n{font-size:84px;color:var(--fc)}
.l-typo.fond-fruit .item .n{color:var(--ft)}
.l-typo .item .t{font-size:56px}
.l-typo .item .d{font-size:40px;opacity:.9}
.l-typo .arrow{background:none;color:inherit;width:auto;height:auto;font-size:76px;bottom:60px}
.l-typo.fond-encre .bar{color:#fff}
.l-photo .arrow{background:none;color:#fff;width:auto;height:auto;font-size:76px;bottom:60px;text-shadow:0 2px 20px rgba(0,0,0,.6)}
/* texte seul, sans photo (rétro-compatible) */
.l-texte{padding:150px 72px 72px;display:flex;flex-direction:column;justify-content:center;gap:40px}
.l-texte h2{font-size:120px}
${clairCss(design, T)}
${(design.css ?? []).join('\n')}
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

const TICK = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
const ARROW_SVG = '<svg viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"/></svg>';
const svgFile = (root, f) => readFileSync(join(root, 'assets', 'svg', f), 'utf8').replace('<svg ', '<svg class="cl-svg" ');
const WAVE = '<svg class="cl-wave" viewBox="0 0 40 16"><path d="M2 8C10 0 14 0 20 8S30 16 38 6" fill="none" stroke="#F2B90F" stroke-width="4" stroke-linecap="round"/></svg>';
function visuel(v, ch, root) {
  if (!v) return '';
  const W0 = 936;
  switch (v.type) {
    case 'foule':
      return svgFile(root, 'foule.svg');
    case 'barre': {
      const f = Math.round((W0 * v.valeur) / 100);
      return `<svg class="cl-viz" viewBox="0 0 ${W0} 96"><rect x="0" y="16" width="${W0}" height="48" rx="24" fill="${ch.step}"/><rect x="0" y="16" width="${f}" height="48" rx="24" fill="${ch.accent}"/><circle cx="${Math.max(f, 24)}" cy="40" r="24" fill="${ch.sun}" stroke="${ch.ink}" stroke-width="4"/><text x="0" y="92" font-size="26" font-weight="600" fill="${ch.ink3}">0 %</text><text x="${W0}" y="92" font-size="26" font-weight="600" fill="${ch.ink3}" text-anchor="end">100 %</text></svg>`;
    }
    case 'frise': {
      const n = v.n, pl = v.pleins, r = 38, step = (W0 - 2 * r) / (n - 1);
      const dots = Array.from({ length: n }, (_, k) => {
        const cx = r + k * step, plein = k < pl;
        return `<circle cx="${cx}" cy="50" r="${r}" fill="${plein ? ch.step : ch.sun}" stroke="${plein ? 'none' : ch.ink}" stroke-width="${plein ? 0 : 3}"/><text x="${cx}" y="62" font-size="34" font-weight="800" fill="${ch.ink}" text-anchor="middle">${k + 1}</text>`;
      }).join('');
      return `<svg class="cl-viz" viewBox="0 0 ${W0} 130">${dots}<text x="0" y="124" font-size="26" font-weight="600" fill="${ch.ink3}">années</text></svg>`;
    }
    case 'globe':
      return `<svg class="cl-viz globe" viewBox="0 0 260 260"><g fill="none" stroke="${ch.accent}" stroke-width="6" stroke-linecap="round"><circle cx="130" cy="130" r="110"/><ellipse cx="130" cy="130" rx="46" ry="110"/><path d="M20 130h220M38 76h184M38 184h184"/></g><circle cx="176" cy="92" r="16" fill="${ch.sun}" stroke="${ch.ink}" stroke-width="4"/></svg>`;
    default:
      return '';
  }
}

function clairBloc(b, root, design) {
  switch (b.type) {
    case 'stats':
      return `<div class="cl-stats">${b.items.map((it) => `<div class="cl-stat"><b>${rich(it.valeur)}</b><span>${rich(it.texte)}${it.sup ? `<sup>${it.sup}</sup>` : ''}</span></div>`).join('')}</div>`;
    case 'carte':
      return `<div class="cl-card${b.fond === 'band' ? ' band' : ''}">${b.grand ? `<div class="cl-big">${rich(b.grand)}${b.sup ? `<sup>${b.sup}</sup>` : ''}${b.legende ? `<small>${rich(b.legende)}</small>` : ''}</div>` : ''}${b.titre ? `<h3>${rich(b.titre)}</h3>` : ''}${b.texte ? `<p>${rich(b.texte)}</p>` : ''}${b.svg ? svgFile(root, b.svg) : ''}</div>`;
    case 'liste':
      return `<div class="cl-liste">${b.items.map((it, k) => `<div class="cl-item">${b.mode === 'coche' ? `<span class="cl-ck">${TICK}</span>` : `<span class="cl-num">${k + 1}</span>`}<div><b>${rich(it.t)}</b>${it.d ? `<p>${rich(it.d)}</p>` : ''}</div></div>`).join('')}</div>`;
    case 'photo':
      return `<div class="cl-photo" style="height:${b.hauteur ?? 380}px"><div class="cl-photo-in">${imgTag({ image: { fichier: b.fichier, pos: b.pos } }, root, 'ph')}</div></div>`;
    case 'schema':
      return `<div class="cl-schema"${b.largeur ? ` style="width:${b.largeur}%"` : ''}>${svgFile(root, b.fichier)}</div>`;
    case 'photos': {
      const h = b.hauteur ?? 400, n = b.items.length;
      return `<div class="cl-photos">${b.items.map((it, k) => `<div class="cl-ph" style="height:${k === 1 && n === 3 ? h + 56 : h}px">${imgTag({ image: { fichier: it.fichier, pos: it.pos } }, root, 'ph')}${it.legende ? `<em>${rich(it.legende)}</em>` : ''}</div>`).join('')}</div>`;
    }
    case 'chiffre':
      return `<div class="cl-fig"><div class="cl-fig-num" data-fit="${b.taille ?? 250}" data-maxh="340">${rich(b.valeur)}${b.sup ? `<sup>${b.sup}</sup>` : ''}</div>${WAVE}<p class="cl-fig-leg">${rich(b.legende)}</p>${b.detail ? `<p class="cl-fig-det">${rich(b.detail)}</p>` : ''}${visuel(b.visuel, design.charte, root)}</div>`;
    case 'bouton':
      return `<div class="cl-btn">${rich(b.texte)} ${ARROW_SVG}</div>`;
    case 'garanties':
      return `<div class="cl-gar">${b.items.map((t) => `<span><i>${TICK}</i>${rich(t)}</span>`).join('')}</div>`;
    default:
      throw new Error(`Bloc inconnu : ${b.type}`);
  }
}

const listeHtml = (items = [], mode = 'num') =>
  `<div class="liste">${items
    .map((it, k) => `<div class="item"><div class="n">${mode === 'coche' ? '✓' : k + 1}</div><div><div class="t">${rich(it.t)}</div>${it.d ? `<div class="d">${rich(it.d)}</div>` : ''}</div></div>`)
    .join('')}</div>`;

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
<div class="corpsb"><h2>${rich(s.titre)}</h2>${listeHtml(s.items)}</div>${arrow(i, n)}`;
    case 'duo':
      return `${imgTag(s, root)}<div class="teinte"></div><div class="scrim"></div>${bar(i, n, design)}
<div class="txt">${kick}<h2 ${fit(170, 520)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}<div class="marque">${esc(design.marque)} · ${esc(design.signature)}</div></div>`;
    case 'photo': {
      const big = s.grand ?? i === 0;
      const head = s.titre ? (big ? `<h1 ${fit(190, 560)}>${rich(s.titre)}</h1>` : `<h2 ${fit(150, 420)}>${rich(s.titre)}</h2>`) : '';
      const lead = s.kicker ? `<div class="kick">${rich(s.kicker)}</div>` : '';
      const body = s.texte ?? s.sous;
      return `${imgTag(s, root)}<div class="scrim"></div>${bar(i, n, design)}
<div class="txt">${lead}${s.valeur ? `<div class="chiffre">${rich(s.valeur)}</div>` : ''}${head}${body ? `<p class="corps">${rich(body)}</p>` : ''}${s.items ? listeHtml(s.items, s.puces) : ''}${s.mention ? `<p class="mention">${rich(s.mention)}</p>` : ''}${i === n - 1 ? `<div class="marque"><span>${esc(design.marque)}</span> · ${esc(design.signature)}</div>` : ''}</div>${arrow(i, n)}`;
    }
    case 'clair':
    case 'clair-photo': {
      const cp = s.layout === 'clair-photo';
      const lg = design.charte?.logo ? readFileSync(join(root, 'assets', 'svg', design.charte.logo), 'utf8').replace('<svg ', '<svg class="cl-logo" ') : '';
      const head = `<header class="cl-head">${lg}<div><b>${esc(design.marque)}</b><small>${esc(design.charte?.sous_marque ?? '')}</small></div><span class="cl-pg">${i + 1} / ${n}</span></header>`;
      const big = s.grand ?? i === 0;
      const blocs = (s.blocs ?? []).map((b) => clairBloc(b, root, design)).join('');
      const a = s.arche;
      const arche = a ? `<div class="cl-arche"><div class="cl-arche-in">${imgTag({ image: { fichier: a.fichier, pos: a.pos } }, root, 'ph')}</div>${a.badge ? `<div class="cl-badge"><b>${rich(a.badge.valeur)}</b><span>${rich(a.badge.texte)}</span></div>` : ''}</div>` : '';
      const titre = s.titre ? (big ? `<h1 ${fit(124, 420)}>${rich(s.titre)}</h1>` : `<h2 ${fit(128, 330)}>${rich(s.titre)}</h2>`) : '';
      const air = s.air ? ' air' : '';
      const bodyCls = air + (cp ? (s.pos === 'haut' ? ' haut' : s.pos === 'centre' ? ' centre' : ' bas') : s.haut ? ' haut' : '');
      const bd = s.bande;
      const bh = bd?.hauteur ?? 560;
      const bande = bd ? `<div class="cl-bande ${bd.cote === 'bas' ? 'bas' : 'haut'}" style="height:${bh}px">${imgTag({ image: { fichier: bd.fichier, pos: bd.pos } }, root, 'ph')}</div>` : '';
      const bodyStyle = bd ? (bd.cote === 'bas' ? ` style="padding-bottom:${bh + 36}px"` : ` style="padding-top:${bh - 92}px"`) : '';
      const bg = cp ? `${imgTag(s, root)}<div class="scrim"></div>` : bande;
      const badge = s.badge ? `<div class="cl-badge"><b>${rich(s.badge.valeur)}</b><span>${rich(s.badge.texte)}</span></div>` : '';
      return `${bg}${head}<div class="cl-body${bodyCls}"${bodyStyle}>${badge}${s.eyebrow ? `<span class="cl-eyebrow">${rich(s.eyebrow)}</span>` : ''}${titre}${s.texte ? `<p class="cl-texte${s.etroit ? ' etroit' : ''}">${rich(s.texte)}</p>` : ''}${blocs}${s.source ? `<p class="cl-src">${rich(s.source)}</p>` : ''}${s.mention ? `<p class="cl-mention">${rich(s.mention)}</p>` : ''}</div>${arche}${i < n - 1 ? '<div class="cl-next">→</div>' : ''}`;
    }
    case 'typo': {
      const lead = s.kicker ? `<div class="kick">${rich(s.kicker)}</div>` : '';
      return `${bar(i, n, design, s.fond === 'fruit')}<div class="txt-typo">${lead}${s.titre ? `<h2 ${fit(130, 400)}>${rich(s.titre)}</h2>` : ''}${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}${s.items ? listeHtml(s.items, s.puces) : ''}${s.mention ? `<p class="mention">${rich(s.mention)}</p>` : ''}</div>${arrow(i, n)}`;
    }
    case 'carte':
      return `${imgTag(s, root)}<div class="scrim"></div>${bar(i, n, design)}
<div class="carte">${kick}<h2 ${fit(104, 260)}>${rich(s.titre)}</h2>${s.texte ?? s.sous ? `<p class="corps">${rich(s.texte ?? s.sous)}</p>` : ''}</div>${arrow(i, n)}`;
    case 'liste-carte':
      return `${imgTag(s, root)}<div class="scrim"></div>${bar(i, n, design)}
<div class="carte"><h2 ${fit(96, 130)}>${rich(s.titre)}</h2>${listeHtml(s.items)}</div>${arrow(i, n)}`;
    case 'haut-texte':
      return `${bar(i, n, design, true)}<div class="txtw">${kick}<h2 ${fit(116, 230)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}</div><div class="cadre">${imgTag(s, root)}</div>${arrow(i, n)}`;
    case 'moitie':
      return `<div class="ph">${imgTag(s, root)}</div>${bar(i, n, design)}
<div class="bas">${kick}<h2 ${fit(104, 230)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}</div>${arrow(i, n)}`;
    case 'cercle':
      return `${bar(i, n, design, true)}<div class="txtc">${kick}<h2 ${fit(116, 230)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}</div><div class="rond">${imgTag(s, root)}</div>${arrow(i, n)}`;
    case 'chiffre':
      return `${bar(i, n, design, true)}<div class="chiffre">${rich(s.valeur)}</div><p class="corps">${rich(s.texte)}</p>${arrow(i, n)}`;
    default:
      return `${bar(i, n, design, true)}${kick}<h2 ${fit(120, 360)}>${rich(s.titre)}</h2>${s.texte ? `<p class="corps">${rich(s.texte)}</p>` : ''}${arrow(i, n)}`;
  }
}

export function slideHtml(s, i, n, design, carousel, root) {
  const layout = s.layout ?? 'texte';
  const fond = s.fond ?? (layout === 'typo' ? 'encre' : 'papier');
  const cls = ['slide', `l-${layout}`, `mk-${carousel.marque ?? (layout === 'photo' ? 'couleur' : 'surligne')}`, s.pos ? `p-${s.pos}` : '', s.align ? `a-${s.align}` : '', s.encart ? `e-${s.encart}` : '', s.ombre ? `o-${s.ombre}` : '', s.bande ? `bd-${s.bande.cote === 'bas' ? 'bas' : 'haut'}` : '', fond === 'fruit' ? 'fond-fruit' : fond === 'encre' ? 'fond-encre' : ''].join(' ');
  const p = design.couleurs.fruits[carousel.fruit] ?? Object.values(design.couleurs.fruits)[0];
  return `<section class="${cls}" style="--f:${p.fond};--ft:${p.texte};--fc:${p.clair ?? p.fond}">${inner({ ...s, layout }, i, n, design, root)}</section>`;
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
