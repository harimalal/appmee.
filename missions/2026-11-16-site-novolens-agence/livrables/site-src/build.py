#!/usr/bin/env python3
"""Assemble le site NOVOLENS (multi-pages) dans ../dist."""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story import story
from ucards import section as ucards_section

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.environ.get("V2") == "1"
V3 = os.environ.get("V3") == "1"
DIST = os.path.join(HERE, "..", "site" if V3 else ("dist-v2" if V2 else "dist"))
shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(DIST)

from PIL import Image as _PIL
def IMG(name, alt, cls="", eager=False):
    w, h = _PIL.open(os.path.join(HERE, "img", name)).size
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="img/{name}" alt="{alt}" width="{w}" height="{h}" decoding="async"' + ('' if eager else ' loading="lazy"') + '>'

# ---------- icônes ----------
P = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "check": '<path d="m5 12 4.5 4.5L19 7"/>',
 "checkc": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16 9.5"/>',
 "xc": '<circle cx="12" cy="12" r="9"/><path d="m9 9 6 6M15 9l-6 6"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
 "send": '<path d="M21 3 10 14"/><path d="M21 3l-6.5 18-3.5-8-8-3.5z"/>',
 "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
 "calcheck": '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17M9 15l2 2 4-4"/>',
 "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><path d="M16 5.2a3 3 0 0 1 0 5.6M18 14.8c1.9.7 3 2.4 3 5.2"/>',
 "building": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
 "chart": '<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
 "shield": '<path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6z"/><path d="m9 12 2.2 2.2L15 10"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
 "filter": '<path d="M4 5h16l-6 8v6l-4-2v-4z"/>',
 "file": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 "zap": '<path d="M13 3 5 13.5h6L10 21l8-10.5h-6z"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
 "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
 "gauge": '<path d="M4 17a8 8 0 1 1 16 0"/><path d="m12 17 4-5"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
 "trend": '<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 "sliders": '<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
}
def ic(n, cls=""):
    if V3:
        return f'<svg class="i{(" " + cls) if cls else ""}" viewBox="0 0 24 24" aria-hidden="true">{P[n]}</svg>'
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[n]}</svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>'
PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>'

def logo(uid="a"):
    return (f'<svg viewBox="0 0 32 32" aria-hidden="true"><defs><linearGradient id="lg{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#4B39DD"/><stop offset="1" stop-color="#8A6BFF"/></linearGradient></defs>'
            f'<circle cx="16" cy="16" r="12" fill="none" stroke="url(#lg{uid})" stroke-width="4"/>'
            f'<circle cx="16" cy="16" r="4.5" fill="url(#lg{uid})"/><circle cx="22" cy="10" r="1.8" fill="#fff"/></svg>')

NAV = [("pourquoi-nous.html", "Pourquoi nous"), ("comment-ca-marche.html", "Comment ça marche"),
       ("resultats.html", "Résultats"), ("tarifs.html", "Tarifs"), ("faq.html", "FAQ")]

def header(active):
    links = "".join(f'<a href="{h}"' + (' aria-current="page"' if h == active else "") + f'>{t}</a>' for h, t in NAV)
    return f'''<a class="sr" href="#main">Aller au contenu</a>
<header class="site-header"><div class="wrap nav">
<a class="logo" href="index.html" aria-label="NOVOLENS, accueil">{logo("h")}<span>NOVOLENS</span></a>
<nav class="menu" id="menu" aria-label="Navigation principale">{links}</nav>
<a class="btn btn-primary btn-sm nav-cta" href="contact.html">Réserver un échange {ic("arrow","arr")}</a>
<button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Menu"><span></span></button>
</div><div class="progress" aria-hidden="true"></div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="index.html" aria-label="NOVOLENS, accueil">{logo("f")}<span>NOVOLENS</span></a>
<p class="muted" style="margin-top:14px;max-width:34ch">Prospection B2B externalisée : des rendez-vous qualifiés avec des décideurs, livrés directement dans votre agenda.</p></div>
<div><h4>Site</h4><ul><li><a href="index.html">Accueil</a></li><li><a href="pourquoi-nous.html">Pourquoi nous</a></li><li><a href="comment-ca-marche.html">Comment ça marche</a></li><li><a href="resultats.html">Résultats</a></li><li><a href="cas-client.html">Cas client (modèle)</a></li></ul></div>
<div><h4>Offre</h4><ul><li><a href="tarifs.html">Tarifs</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Réserver un échange</a></li></ul></div>
<div><h4>Contact</h4><ul><li>contact@novolens.fr</li><li>Réponse sous 24 h</li></ul></div>
</div>
<div class="foot-bottom"><span>© 2026 NOVOLENS. Tous droits réservés.</span><span>* Objectif indicatif. Les chiffres, exemples de cas et coordonnées de cette maquette sont donnés à titre illustratif.</span></div>
</div></footer>'''

def cta(title="Parlons de vos objectifs de croissance.", text="Un échange de 15 minutes avec un expert NOVOLENS pour comprendre vos enjeux et voir comment nous pouvons vous apporter des rendez-vous qualifiés."):
    sky = '''<svg class="skyline" viewBox="0 0 600 300" preserveAspectRatio="xMaxYMax meet" aria-hidden="true"><g fill="#8F7DFF" opacity=".35">
<rect x="20" y="170" width="46" height="130"/><rect x="80" y="110" width="58" height="190"/><rect x="152" y="150" width="40" height="150"/><rect x="206" y="60" width="64" height="240"/><rect x="284" y="130" width="50" height="170"/><rect x="348" y="90" width="70" height="210"/><rect x="432" y="150" width="44" height="150"/><rect x="490" y="40" width="60" height="260"/></g>
<g fill="#fff" opacity=".7"><rect x="92" y="130" width="6" height="6"/><rect x="112" y="150" width="6" height="6"/><rect x="220" y="90" width="6" height="6"/><rect x="240" y="120" width="6" height="6"/><rect x="362" y="120" width="6" height="6"/><rect x="390" y="150" width="6" height="6"/><rect x="504" y="70" width="6" height="6"/><rect x="524" y="100" width="6" height="6"/></g></svg>'''
    return f'''<section class="cta-section"><div class="wrap"><div class="cta-band" data-reveal>{sky}<div class="cta-photo" aria-hidden="true"></div><div class="cta-in">
<p class="eyebrow">Échange stratégique</p><h2>{title}</h2><p class="lead">{text}</p>
<div class="cta-row"><a class="btn btn-primary" href="contact.html">Réserver un échange de 15 min {ic("arrow","arr")}</a></div>
<ul class="checks"><li>{ic("checkc")}Sans engagement</li><li>{ic("checkc")}Réponse sous 24 h</li><li>{ic("checkc")}Échange avec un expert</li></ul>
</div></div></div></section>'''

# ---------- preuve sociale ----------
def tcard(quote, name, role, draft=True, initials="?"):
    q = f"<q>{quote}</q>" if quote else '<div class="shimmer" aria-hidden="true"><i></i><i style="width:88%"></i><i style="width:62%"></i></div>'
    badge = '<span class="draft">Texte provisoire</span>' if (draft and quote) else ('<span class="draft">Témoignage à venir</span>' if not quote else "")
    return f'''<figure class="tcard" style="margin:0">{badge}{q}<figcaption class="who"><span class="avatar" aria-hidden="true">{initials}</span><span><strong>{name}</strong>{role}</span></figcaption></figure>'''

def proof_wall():
    cards = [
      tcard("En moins d'un mois, nous avons obtenu des rendez-vous qualifiés avec des décideurs que nous n'arrivions pas à contacter.", "Thomas L.", "Dirigeant · Industrie", initials="T"),
      tcard("NOVOLENS nous a permis de réactiver des prospects que nous avions mis de côté faute de temps. Des opportunités concrètes et à fort potentiel.", "Sophie M.", "Directrice Commerciale · Services B2B", initials="S"),
      tcard("Une équipe très professionnelle, déterminée et persévérante. Les rendez-vous sont bien qualifiés et nous gagnons un temps considérable.", "Marc D.", "CEO · Tech & Logiciels", initials="M"),
      tcard("", "Nom du client", "Fonction · Secteur"),
      tcard("", "Nom du client", "Fonction · Secteur"),
      tcard("", "Nom du client", "Fonction · Secteur"),
    ]
    one = "".join(cards)
    dup = one.replace('<figure class="tcard"', '<figure aria-hidden="true" class="tcard"')
    return f'<div class="proof"><div class="marquee">{one}</div></div>' if V3 else f'<div class="proof"><div class="marquee">{one}{dup}</div></div>'

# ---------- lecteur animé ----------
def player():
    s1 = '''<div class="pstage"><svg viewBox="0 0 220 150" aria-hidden="true"><g fill="none" stroke="#B7A8FF" stroke-width="2">
<circle class="pop" style="--d:0" cx="110" cy="75" r="58"/><circle class="pop" style="--d:150" cx="110" cy="75" r="38"/><circle class="pop" style="--d:300" cx="110" cy="75" r="19"/></g>
<circle class="pop" style="--d:450" cx="110" cy="75" r="6" fill="#fff"/>
<g font-size="10" font-weight="600" font-family="Inter,sans-serif" fill="#fff">
<g class="pop" style="--d:700"><rect x="-6" y="10" width="62" height="22" rx="11" fill="#6D55F2"/><text x="25" y="25" text-anchor="middle">Secteur</text></g>
<g class="pop" style="--d:900"><rect x="164" y="22" width="56" height="22" rx="11" fill="#6D55F2"/><text x="192" y="37" text-anchor="middle">Taille</text></g>
<g class="pop" style="--d:1100"><rect x="150" y="112" width="70" height="22" rx="11" fill="#6D55F2"/><text x="185" y="127" text-anchor="middle">Fonction</text></g></g></svg></div>'''
    s2 = '''<div class="pstage"><svg viewBox="0 0 220 150" aria-hidden="true"><g stroke="#B7A8FF" stroke-width="1.6" fill="none">
<path class="draw" style="--d:0" d="M110 75 40 30"/><path class="draw" style="--d:100" d="M110 75 70 120"/><path class="draw" style="--d:200" d="M110 75 180 28"/><path class="draw" style="--d:300" d="M110 75 190 100"/><path class="draw" style="--d:400" d="M110 75 110 14"/><path class="draw" style="--d:500" d="M110 75 150 134"/></g>
<g fill="#fff"><circle class="pop" style="--d:300" cx="40" cy="30" r="6"/><circle class="pop" style="--d:400" cx="70" cy="120" r="6"/><circle class="pop" style="--d:500" cx="180" cy="28" r="6"/><circle class="pop" style="--d:600" cx="190" cy="100" r="6"/><circle class="pop" style="--d:700" cx="110" cy="14" r="6"/><circle class="pop" style="--d:800" cx="150" cy="134" r="6"/></g>
<circle class="pop" style="--d:0" cx="110" cy="75" r="20" fill="#6D55F2"/><circle cx="110" cy="75" r="7" fill="none" stroke="#fff" stroke-width="2.5" class="pop" style="--d:100"/></svg></div>'''
    s3 = '''<div class="pstage"><svg viewBox="0 0 220 150" aria-hidden="true">
<path class="pop" style="--d:0" d="M40 20h140l-52 56v50l-36-16V76z" fill="none" stroke="#B7A8FF" stroke-width="2.2" stroke-linejoin="round"/>
<g fill="#fff"><circle class="travel" style="--d:0;--x0:-30px;--y0:0px;--x1:10px;--y1:70px" cx="90" cy="10" r="5"/><circle class="travel" style="--d:500;--x0:30px;--y0:0px;--x1:-6px;--y1:70px" cx="130" cy="10" r="5"/><circle class="travel" style="--d:1000;--x0:0px;--y0:0px;--x1:0px;--y1:70px" cx="110" cy="8" r="5"/></g>
<g class="pop" style="--d:900"><circle cx="110" cy="136" r="11" fill="#2FCF8E"/><path d="m104.5 136 4 4 7-8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g></svg></div>'''
    cells = ""
    hot = {2: 0, 5: 200, 9: 400}
    for i in range(15):
        x, y = 30 + (i % 5) * 32, 18 + (i // 5) * 32
        if i in hot:
            cells += f'<g class="pop" style="--d:{500+hot[i]}"><rect x="{x}" y="{y}" width="26" height="26" rx="6" fill="#6D55F2"/><path d="m{x+7} {y+13} 4 4 8-8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g>'
        else:
            cells += f'<rect class="pop" style="--d:{i*30}" x="{x}" y="{y}" width="26" height="26" rx="6" fill="none" stroke="#6F63C7" stroke-width="1.6"/>'
    s4 = f'<div class="pstage"><svg viewBox="0 0 220 120" aria-hidden="true">{cells}</svg></div>'
    caps = [
      ("Nous calibrons votre cible", "Secteur, taille, fonction : nous définissons ensemble le rendez-vous idéal."),
      ("Nous contactons les bons décideurs", "Téléphone, e-mail, LinkedIn : une prospection persévérante."),
      ("Nous qualifions intérêt et besoin", "Seuls les échanges réellement prometteurs passent le filtre."),
      ("Les rendez-vous arrivent dans votre agenda", "Avec le contexte, le compte rendu et le reporting."),
    ]
    out = ""
    for (t, s), st in zip(caps, [s1, s2, s3, s4]):
        out += f'<div class="pscene">{st}<div class="pcap"><b>{t}</b><span>{s}</span></div></div>'
    bars = "".join(f'<button aria-label="Scène {i+1}"><i></i></button>' for i in range(4))
    return f'''<div class="player" role="group" aria-label="Explication animée en 4 étapes">{out}
<div class="pctl"><button class="pbtn" aria-label="Pause">{PAUSE}</button><div class="pbars">{bars}</div><span class="dur">0:17</span></div></div>'''

# ---------- comparateur ----------
def compare():
    labels = {1: "RDV · DG", 3: "RDV · DAF", 6: "RDV · DSI", 8: "RDV · CEO", 13: "RDV · DRH", 15: "RDV · DA", 18: "RDV · DG"}
    ghosts = {0, 5, 11, 17}
    cells = ""
    for i in range(20):
        if i in labels:
            cells += f'<div class="slot is-rdv"><span class="fill">{labels[i]}</span></div>'
        elif i in ghosts:
            cells += '<div class="slot is-ghost"><span class="ghost">à relancer</span></div>'
        else:
            cells += '<div class="slot"></div>'
    dow = "".join(f'<div class="dow">{d}</div>' for d in ["Lun", "Mar", "Mer", "Jeu", "Ven"])
    no = ["Pas le temps de prospecter", "Des opportunités qui passent à côté", "Des commerciaux qui s'éparpillent", "Des relances oubliées", "Un pipeline irrégulier", "Des mois sans nouveaux clients"]
    yes = ["Des rendez-vous qualifiés dans votre agenda", "Des décideurs réellement intéressés", "Un pipeline régulier et prévisible", "Vos équipes concentrées sur la vente", "Une croissance accélérée"]
    lno = "".join(f"<li>{ic('xc')}{t}</li>" for t in no)
    lyes = "".join(f"<li>{ic('checkc')}{t}</li>" for t in yes)
    return f'''<div class="cmp" data-state="sans">
<div class="tabs" role="tablist" aria-label="Comparer"><span class="thumb" aria-hidden="true"></span>
<button role="tab" aria-selected="true" data-state="sans">Sans NOVOLENS</button><button role="tab" aria-selected="false" data-state="avec">Avec NOVOLENS</button></div>
<div class="week" aria-label="Exemple d'agenda sur une semaine">{dow}{cells}</div>
<div class="cmp-lists" aria-live="polite"><ul class="no">{lno}</ul><ul class="yes">{lyes}</ul></div>
<p class="cmp-foot">{ic("clock")}<span>Exemple illustratif d'une semaine d'agenda.</span></p></div>'''

# ---------- livraison ----------
def delivery(card_only=False):
    meter = '<span class="meter" aria-hidden="true"><i class="on"></i><i class="on"></i><i class="on"></i></span>'
    rows = [("layers", "Contexte", "Projet de modernisation en cours"), ("target", "Besoin identifié", "Recherche de solutions pour optimiser ses opérations"),
            ("gauge", "Intérêt", "Élevé" + meter), ("calendar", "Prochain échange", "Jeudi · 10h00"), ("file", "Documents", "Compte rendu + notes")]
    rr = "".join(f'<div class="drow"><span class="i">{ic(i)}</span><span class="k">{k}</span><span class="v">{v}</span></div>' for i, k, v in rows)
    card = f'''<div class="dcard" data-in><div class="dhead"><span class="avatar" aria-hidden="true">DG</span><span><strong>Directeur Général</strong><span class="sub">Industrie · 500 M€ · France</span></span><span class="tag">Rendez-vous qualifié</span></div>{rr}</div>'''
    items = ["Profil du décideur", "Contexte et enjeux", "Besoin identifié", "Niveau d'intérêt", "Compte rendu détaillé", "Accès au reporting global"]
    tl = "".join(f'<li style="--i:{i}">{ic("checkc")}{t}</li>' for i, t in enumerate(items))
    return f'''<div class="deliver"><div>{card}</div>
<div class="deliver-side" data-in><div class="hand-wrap"><svg viewBox="0 0 70 56" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M64 6C40 2 16 14 10 44"/><path d="m2 36 8 10 10-8"/></svg><p class="hand">Un rendez-vous qualifié, avec tout le contexte.</p></div>
<ul class="tick-list">{tl}</ul>{'<figure class="solid">' + IMG("livraison.jpg", "Un rendez-vous préparé avec le dossier complet") + '</figure>' if V2 else ''}</div></div>'''

# ---------- gabarits de page ----------
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500&family=Inter:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,700;1,6..72,400&display=swap">'

PH = {"pourquoi-nous.html": "card-1", "comment-ca-marche.html": "card-2", "resultats.html": "cta-bg", "tarifs.html": "card-4", "faq.html": "pme", "contact.html": "livraison"}
DUO = '<div class="duo"><figure>' + IMG("sans.jpg", "Dirigeant épuisé par la prospection") + '<figcaption class="no">Sans NOVOLENS</figcaption></figure><figure>' + IMG("avec.jpg", "Dirigeante sereine, agenda rempli") + '<figcaption class="yes">Avec NOVOLENS</figcaption></figure></div>'
def v2body(fname, body):
    if fname in PH:
        body = body.replace('<section class="page-hero"><div class="wrap">', '<section class="page-hero has-ph"><div class="wrap"><div class="ph-photo" role="img" aria-label="Illustration photo" style="background-image:url(img/%s.jpg)"></div>' % PH[fname], 1)
    body = body.replace('<div class="cmp" data-state="sans">', DUO + '<div class="cmp" data-state="sans">', 1)
    for k, img in (("PME en croissance", "pme"), ("<h3>ETI</h3>", "eti"), ("Grands groupes", "grand")):
        pass
    return body

def page(fname, title, desc, body, active=None, ld=None, index=False):
    if V2:
        body = v2body(fname, body)
        if index: title = "NOVOLENS V2"
    if V3 and index: title = "NOVOLENS"
    head = f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="description" content="{desc}">\n'
    head += f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n<meta property="og:type" content="website">\n<meta name="theme-color" content="#FCFBFF">\n'
    if V3:
        head += '<meta name="color-scheme" content="light">\n'
        if fname == 'cas-client.html': head += '<meta name="robots" content="noindex">\n'
        if index: head += '<link rel="preload" as="image" href="img/hero-bg.jpg" fetchpriority="high">\n'
    head += FONTS + '\n<link rel="stylesheet" href="style.css">\n'
    if V3 and fname not in ("index.html", "404.html"):
        crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "index.html"},
            {"@type": "ListItem", "position": 2, "name": title.replace(" NOVOLENS", "").replace("NOVOLENS ", ""), "item": fname}]}
        ld = (ld or []) + [crumb]
    if V3 and index:
        ld = (ld or []) + [{"@context": "https://schema.org", "@type": "WebSite", "name": "NOVOLENS", "inLanguage": "fr"}]
    for l in (ld or []):
        head += f'<script type="application/ld+json">{json.dumps(l, ensure_ascii=False)}</script>\n'
    sticky = '' if (not V3 or fname in ("contact.html", "404.html")) else f'<a class="sticky-cta" href="contact.html">Réserver un échange de 15 min {ic("arrow")}</a>'
    main = f'{header(active)}\n<main id="main">{body}</main>\n{footer()}\n{sticky}\n<script src="app.js" defer></script>'
    if index and V3:
        frag = head + main
        full = ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>\n'
                + head.replace('<title>NOVOLENS</title>', '<title>NOVOLENS, prospection B2B externalisée</title>', 1).replace('og:title" content="NOVOLENS"', 'og:title" content="NOVOLENS, prospection B2B externalisée"') + '</head>\n<body>\n' + main + '\n</body></html>')
        os.makedirs(os.path.join(DIST, "..", "site-artefact"), exist_ok=True)
        import re as _r2
        with open(os.path.join(DIST, "..", "site-artefact", "index.html"), "w", encoding="utf-8") as f2:
            f2.write(_r2.sub(r'>\s*\n\s*<', '><', frag))
        html = full
    elif index:
        html = head + main
    else:
        html = ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>\n'
                + head + '</head>\n<body>\n' + main + '\n</body></html>')
    if V3:
        import re as _re
        html = _re.sub(r'>\s*\n\s*<', '><', html)
    with open(os.path.join(DIST, fname), "w", encoding="utf-8") as f:
        f.write(html)

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "NOVOLENS",
       "description": "Prospection B2B externalisée : rendez-vous qualifiés avec des décideurs pour PME, ETI et grands groupes."}

def PHOTO(n):
    return IMG(n + ".jpg", "", "cphoto") if V2 else ''

def sec_head(eyebrow, h, lead="", center=False):
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="sec-head{" center" if center else ""}" data-reveal><p class="eyebrow">{eyebrow}</p><h2>{h}</h2>{l}</div>'

def crumbs(name):
    return f'<p class="crumbs"><a href="index.html">Accueil</a> / {name}</p>'

# ---------- étapes ----------
STEP_ICON = {
 1: '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle class="pulse-ring" cx="20" cy="20" r="15"/><circle class="pulse-ring" cx="20" cy="20" r="15"/><circle cx="20" cy="20" r="10"/><circle cx="20" cy="20" r="4" fill="currentColor" stroke="none"/></svg>',
 2: '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path class="dash-flow" d="M4 32C14 32 14 14 30 12"/><path d="M36 8 24 20M36 8l-7 24-5-12-12-5z"/></svg>',
 3: '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="8" width="30" height="26" rx="5"/><path d="M13 4v7M27 4v7M5 16h30"/><path class="draw-on" d="m14 26 4.5 4.5L27 22" style="stroke-dasharray:30;stroke-dashoffset:30;animation:drawl 1.4s 1s ease infinite alternate"/></svg>',
}
def steps(detail=False):
    data = [
      (1, "Calibrage", "Nous définissons ensemble vos objectifs, votre cible et les critères d'un rendez-vous qualifié.",
         ["Atelier de cadrage avec votre équipe", "Profil de client idéal et comptes prioritaires", "Message et argumentaire validés"]),
      (2, "Prospection", "Nous recherchons les bons contacts, nous contactons et relançons avec persévérance, et nous qualifions l'intérêt et le besoin.",
         ["Sélection et enrichissement des contacts", "Séquences multicanales personnalisées", "Relances jusqu'à une réponse claire"]),
      (3, "Rendez-vous qualifiés", "Vous recevez des rendez-vous avec des décideurs qualifiés, avec les éléments de contexte et un reporting clair.",
         ["Rendez-vous confirmés dans votre agenda", "Fiche de contexte et compte rendu", "Reporting partagé et point régulier"]),
    ]
    out = ""
    for n, t, p, ul in data:
        lis = "".join(f"<li>{ic('check')}{x}</li>" for x in ul) if detail else ""
        ulh = f"<ul>{lis}</ul>" if detail else ""
        out += f'<div class="step" data-reveal="{(n-1)*120}"><div class="ico">{STEP_ICON[n]}<span class="num">{n}</span></div><h3>{t}</h3><p>{p}</p>{ulh}</div>'
    return f'<div class="steps" data-in>{out}</div>'

def funnel():
    rows = [("Entreprises ciblées", 128, 100, ""), ("Décideurs contactés", 86, 67, "67 %"), ("Projets qualifiés", 24, 19, "28 %"), ("Rendez-vous planifiés", 8, 6.3, "33 %")]
    out = ""
    for i, (k, v, w, r) in enumerate(rows):
        out += f'<div class="frow"><span>{k}</span><div class="fbar"><i style="--w:{max(w,12)}%;--i:{i}">{v}</i></div><span class="rate">{r}</span></div>'
    return f'<div class="funnel" data-in>{out}</div>'

def laptop():
    return f'''<div class="laptop" data-in role="img" aria-label="Aperçu du tableau de bord de reporting NOVOLENS"><span class="brand-s">NOVOLENS · REPORTING</span>
<div class="kpis"><div class="kpi"><b data-count="128">128</b><span>Entreprises ciblées</span></div><div class="kpi"><b data-count="86">86</b><span>Décideurs contactés</span></div><div class="kpi"><b data-count="24">24</b><span>Projets qualifiés</span></div><div class="kpi"><b data-count="8">8</b><span>Rendez-vous planifiés</span></div></div>
<div class="chart" data-in><div class="bars">{"".join(f'<div class="bar"><em>{v}</em><i style="--h:{v*11}%;--i:{i}"></i></div>' for i, v in enumerate([1, 2, 4, 5, 7, 8]))}</div><div class="bar-labels"><span>Sem. 1</span><span>Sem. 2</span><span>Sem. 3</span><span>Sem. 4</span><span>Sem. 5</span><span>Sem. 6</span></div></div>
<p class="note">Données d'exemple, à titre illustratif.</p></div>'''

# =====================================================================
# ACCUEIL
# =====================================================================
hero_svg = '''<svg class="scene-svg" viewBox="0 0 480 560" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Illustration : un dirigeant pensif devant une baie vitrée, face à la ville">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9D1FF"/><stop offset="1" stop-color="#F5F2FF"/></linearGradient>
<linearGradient id="suit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A2178"/><stop offset="1" stop-color="#17114A"/></linearGradient></defs>
<rect width="480" height="560" fill="url(#sky)"/>
<g fill="#C4BAFA" opacity=".75"><rect x="10" y="300" width="60" height="260"/><rect x="84" y="240" width="74" height="320"/><rect x="170" y="330" width="52" height="230"/><rect x="330" y="270" width="70" height="290"/><rect x="412" y="210" width="68" height="350"/></g>
<g fill="#A99CF5" opacity=".8"><rect x="40" y="360" width="56" height="200"/><rect x="120" y="300" width="48" height="260"/><rect x="360" y="340" width="60" height="220"/></g>
<g fill="#fff"><rect class="win" x="98" y="260" width="8" height="8" opacity=".9"/><rect class="win" x="120" y="280" width="8" height="8" opacity=".9"/><rect class="win" x="98" y="300" width="8" height="8" opacity=".9"/><rect class="win" x="348" y="290" width="8" height="8" opacity=".9"/><rect class="win" x="372" y="310" width="8" height="8" opacity=".9"/><rect class="win" x="428" y="230" width="8" height="8" opacity=".9"/><rect class="win" x="450" y="260" width="8" height="8" opacity=".9"/><rect class="win" x="428" y="290" width="8" height="8" opacity=".9"/></g>
<g stroke="#fff" stroke-width="7" opacity=".85"><path d="M150 0V560M330 0V560M0 190H480"/></g>
<g transform="translate(-82 0)"><g class="person"><path d="M60 560c0-105 66-150 130-160h100c64 10 130 55 130 160z" fill="url(#suit)"/><path d="M204 398 240 482l36-84z" fill="#fff"/><path d="m236 440-9 16 13 60 13-60-9-16z" fill="#6D55F2"/>
<path d="M196 392l-16 30 30 60-24-70zM284 392l16 30-30 60 24-70z" fill="#120C3A" opacity=".6"/><rect x="216" y="346" width="48" height="56" rx="16" fill="#D5A383"/>
<ellipse cx="240" cy="308" rx="47" ry="58" fill="#E3B697"/><path d="M192 304c-6-52 94-60 96 0-18-30-70-34-96 0z" fill="#2B2430"/><ellipse cx="193" cy="312" rx="6" ry="12" fill="#D5A383"/><ellipse cx="287" cy="312" rx="6" ry="12" fill="#D5A383"/>
<path d="M222 322q6 4 12 0M246 322q6 4 12 0" stroke="#3A2A2A" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M228 348q12 8 24 0" stroke="#A8664E" stroke-width="3" fill="none" stroke-linecap="round"/></g></g></svg>'''

ROT = '<p class="rotator" data-reveal>Des rendez-vous avec <b data-rotate="dirigeants|directeurs achats|DSI|directeurs commerciaux">dirigeants</b></p>'

def build_index():
    notif = f'<div class="notifs"><p class="notifs-title"><span class="live"></span>De nouveaux clients dans votre agenda</p><div class="notif-list" id="notif-list" aria-live="polite"></div></div>'
    hero = f'''<section class="hero"><div class="hero-bg" role="img" aria-label="Rendez-vous d'affaires entre décideurs dans un hall de bureaux lumineux"></div><div class="wrap hero-grid">
<div class="hero-copy"><p class="eyebrow" data-reveal>Prospection B2B externalisée</p>
<h1 data-reveal>Des <mark class="hl">rendez-vous qualifiés.</mark><br><span class="accent">Sans effort</span> de prospection.</h1>
<p class="lead" data-reveal>Nous identifions <strong class="vi">les bons prospects</strong>, les contactons, les qualifions et vous livrons des rendez-vous avec <strong class="vi">des décideurs réellement intéressés</strong>.</p>
<div class="cta-row" data-reveal><a class="btn btn-primary" href="contact.html">Réserver un échange de 15 min {ic("arrow","arr")}</a>
<button class="btn btn-ghost" type="button" data-open-video><span class="play-dot">{PLAY}</span>Voir comment ça marche</button></div>
{ROT if V3 else ""}<ul class="checks" data-reveal><li>{ic("check")}Sans engagement</li><li>{ic("check")}Réponse sous 24 h</li><li>{ic("check")}Échange avec un expert</li></ul></div>
<div class="hero-visual">
<span class="chip-float a"><i></i>Décideur confirmé</span><span class="chip-float b"><i></i>Besoin qualifié</span>{notif}</div>
</div>
<div class="wrap stats-wrap"><div class="stats" data-reveal>
<div class="stat"><b data-count="70" data-pre="+" data-suf=" %">+70 %</b><span>de rendez-vous qualifiés*</span></div>
<div class="stat"><b>&lt; 1 mois</b><span>pour les premiers résultats</span></div>
<div class="stat"><b>Des comptes stratégiques</b><span>et un fort potentiel commercial</span></div>
<div class="stat"><b>Un pipeline</b><span>prévisible et mesurable</span></div></div></div></section>'''
    reality = f'''<section class="section band-white"><div class="wrap split"><div class="sec-head" data-reveal style="margin:0"><p class="eyebrow">Votre réalité aujourd'hui</p>
<h2>Et si votre prochain <mark class="hl">gros client</mark> arrivait déjà <span class="accent">dans votre agenda</span> ?</h2>
<p class="lead">Pendant que vous gérez votre entreprise, notre équipe s'occupe de la prospection. Vous recevez des rendez-vous qualifiés avec des décideurs prêts à échanger sur vos solutions.</p>
<a class="btn btn-ghost" href="pourquoi-nous.html" style="margin-top:8px">Pourquoi externaliser {ic("arrow","arr")}</a></div>
<div data-reveal="120">{compare()}</div></div></section>'''
    approach = f'''<section class="section"><div class="wrap">{sec_head("Notre approche", "De la stratégie au rendez-vous, <mark class='hl'>nous nous occupons de tout.</mark>", "Quatre étapes, une équipe experte en prospection à froid. <strong class='vi'>Regardez ce que vous y gagnez à chaque étape.</strong>")}
{story(ic, 4)}<div class="cta-row" style="margin-top:40px" data-reveal><a class="btn btn-ghost" href="comment-ca-marche.html">Voir la méthode en détail {ic("arrow","arr")}</a></div></div></section>'''
    livraison = f'''<section class="section band-soft"><div class="wrap">{sec_head("Notre livraison", "Des rendez-vous <mark class='hl'>prêts à être exploités.</mark>", "Chaque rendez-vous est qualifié et accompagné de toutes les informations nécessaires pour des échanges productifs.")}
{delivery()}</div></section>'''
    video = ucards_section(ic, P, "Comprendre NOVOLENS <mark class='hl'>en un coup d'œil.</mark>", "Quatre étapes qui se suivent. À chaque fois, <strong class='vi'>l'action</strong> et <strong class='vi'>le moyen</strong> utilisé pour obtenir vos rendez-vous.")
    cibles = f'''<section class="section"><div class="wrap">{sec_head("Pour qui", "Pensé pour les entreprises qui <mark class='hl'>ont des ambitions.</mark>", "Des PME aux grands groupes, la même exigence : des décideurs, du contexte, de la régularité.")}
<div class="grid-3">
<article class="card" data-reveal>{PHOTO("pme")}<span class="ico">{ic("briefcase")}</span><h3>PME en croissance</h3><p>Vous avez une offre qui a fait ses preuves et un besoin de nouveaux comptes, sans recruter ni structurer une équipe de prospection.</p><ul class="target-list"><li>Dirigeants</li><li>Directions commerciales</li></ul></article>
<article class="card" data-reveal="100">{PHOTO("eti")}<span class="ico">{ic("building")}</span><h3>ETI</h3><p>Vous visez des comptes plus complexes et plus structurés, avec plusieurs interlocuteurs à convaincre.</p><ul class="target-list"><li>Développement</li><li>Business units</li></ul></article>
<article class="card" data-reveal="200">{PHOTO("grand")}<span class="ico">{ic("layers")}</span><h3>Grands groupes</h3><p>Vous souhaitez ouvrir de nouveaux marchés ou comptes stratégiques avec une approche ciblée, qualifiée et mesurable.</p><ul class="target-list"><li>Comptes stratégiques</li><li>Nouveaux marchés</li></ul></article>
</div></div></section>'''
    preuves = f'''<section class="section band-soft"><div class="wrap">{sec_head("Ils en parlent mieux que nous", "Des dirigeants qui accélèrent leur croissance avec NOVOLENS.", "Textes provisoires en attendant les vrais avis clients.")}</div>{proof_wall()}</section>'''
    body = hero + reality + approach + livraison + video + cibles + preuves + cta()
    page("index.html", "NOVOLENS", "NOVOLENS livre des rendez-vous qualifiés avec des décideurs : prospection B2B externalisée pour PME, ETI et grands groupes.", body, None, [ORG], index=True)

# =====================================================================
# POURQUOI NOUS
# =====================================================================
def build_pourquoi():
    arguments = [
      ("zap", "Un démarrage rapide", "Après le calibrage, la prospection démarre sans délai de recrutement ni de formation. Premiers résultats visés en moins d'un mois."),
      ("target", "Un ciblage sur mesure", "Secteur, taille, fonction, signaux d'achat : chaque campagne part de votre client idéal, pas d'un fichier générique."),
      ("shield", "Une qualification rigoureuse", "Un rendez-vous n'est livré que si le décideur, le besoin et l'intérêt sont confirmés selon vos critères."),
      ("phone", "L'expertise du démarchage à froid", "Une équipe dédiée à la prospection, rompue aux objections et à la relance persévérante."),
      ("chart", "Un pilotage mesurable", "Reporting partagé, indicateurs de chaque étape et points réguliers pour ajuster la cible et le message."),
      ("sliders", "Une souplesse totale", "Vous gardez la main sur la cible et le rythme, sans structure fixe à porter ni engagement sur l'échange initial."),
    ]
    cards = "".join(f'<article class="card" data-reveal="{(i%3)*100}"><span class="ico">{ic(i_)}</span><h3>{t}</h3><p>{p}</p></article>' for i, (i_, t, p) in enumerate(arguments))
    hero = f'''<section class="page-hero"><div class="wrap">{crumbs("Pourquoi nous")}<p class="eyebrow">Pourquoi NOVOLENS</p>
<h1>Vos commerciaux vendent. <mark class="hl">Nous remplissons leur agenda.</mark></h1>
<p class="lead">La prospection à froid demande du temps, de la régularité et du savoir-faire. Nous la prenons en charge de bout en bout pour que vos équipes se concentrent sur ce qu'elles font le mieux : convaincre et signer.</p>
<div class="cta-row"><a class="btn btn-primary" href="contact.html">Réserver un échange de 15 min {ic("arrow","arr")}</a></div></div></section>'''
    contrast = f'''<section class="section band-white"><div class="wrap split"><div class="sec-head" data-reveal style="margin:0"><p class="eyebrow">Le constat</p><h2>La prospection passe toujours après l'urgent.</h2>
<p class="lead">Les relances s'oublient, les listes vieillissent, le pipeline se vide en silence. Une activité qui exige de la constance ne tient pas entre deux réunions clients.</p></div>
<div data-reveal="120">{compare()}</div></div></section>'''
    avantages = f'<section class="section"><div class="wrap">{sec_head("Six raisons", "Ce que vous gagnez en nous confiant la prospection.")}<div class="grid-3">{cards}</div></div></section>'
    def row(a, b, c, d):
        return f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class="us">{d}</td></tr>'
    table = f'''<section class="section band-soft"><div class="wrap">{sec_head("Comparatif", "Trois façons de remplir un pipeline.", "Repères généraux, à adapter à votre situation.")}
<div class="tbl-wrap" data-reveal><table class="tbl"><thead><tr><th scope="col">Critère</th><th scope="col">Recruter en interne</th><th scope="col">Autres approches</th><th scope="col" class="us">NOVOLENS</th></tr></thead><tbody>
{row("Démarrage", '<span class="pill mid">Selon le recrutement</span>', '<span class="pill mid">Selon le prestataire</span>', '<span class="pill ok">Moins d\'un mois visé</span>')}
{row("Coût", "Fixe, chargé", "Variable", "Sur devis, adapté à votre cible")}
{row("Expertise du froid", "À construire", "Variable", "Équipe dédiée et rodée")}
{row("Qualification", "Dépend du profil", "Dépend du prestataire", "Critères définis avec vous")}
{row("Visibilité", "Dépend du CRM", "Dépend du prestataire", "Reporting partagé en continu")}
{row("Flexibilité", "Faible", "Variable", "Élevée, sans engagement initial")}
</tbody></table></div></div></section>'''
    engage = f'''<section class="section"><div class="wrap">{sec_head("Nos engagements", "Une prospection sérieuse, transparente, respectueuse.", "Engagements proposés, à valider avant publication.")}
<div class="grid-3"><article class="card" data-reveal><span class="ico">{ic("eye")}</span><h3>Transparence</h3><p>Vous voyez qui est contacté, ce qui est dit et où en est chaque piste.</p></article>
<article class="card" data-reveal="100"><span class="ico">{ic("lock")}</span><h3>Conformité</h3><p>Prospection B2B encadrée, respectueuse du RGPD et du droit d'opposition.</p></article>
<article class="card" data-reveal="200"><span class="ico">{ic("users")}</span><h3>Image de marque</h3><p>Un discours validé avec vous, un ton professionnel, jamais de relance agressive.</p></article></div></div></section>'''
    body = hero + contrast + avantages + table + engage + cta()
    page("pourquoi-nous.html", "Pourquoi NOVOLENS", "Pourquoi externaliser sa prospection B2B avec NOVOLENS : démarrage rapide, ciblage sur mesure, qualification rigoureuse et pilotage mesurable.", body, "pourquoi-nous.html", [ORG])

# =====================================================================
# COMMENT ÇA MARCHE
# =====================================================================
def build_methode():
    hero = f'''<section class="page-hero"><div class="wrap">{crumbs("Comment ça marche")}<p class="eyebrow">Notre méthode</p>
<h1>De la stratégie au rendez-vous, <mark class="hl">nous nous occupons de tout.</mark></h1>
<p class="lead">Cinq étapes, une équipe experte en prospection à froid, un reporting clair. Vous n'intervenez que pour définir la cible et accueillir les rendez-vous.</p></div></section>'''
    s = f'<section class="section band-white"><div class="wrap">{story(ic, 5)}</div></section>'
    tl = f'''<section class="section"><div class="wrap">{sec_head("Vos 30 premiers jours", "Des premiers résultats en moins d'un mois.", "Calendrier type, ajusté à votre marché.")}
<div class="tl" data-reveal><div class="t"><b>Semaine 1</b><h3>Cadrage</h3><p>Objectifs, cible, critères de qualification et message validés ensemble.</p></div>
<div class="t"><b>Semaine 2</b><h3>Lancement</h3><p>Listes de contacts construites, séquences de prospection mises en route.</p></div>
<div class="t"><b>Semaine 3</b><h3>Premiers rendez-vous</h3><p>Les premiers décideurs qualifiés arrivent dans votre agenda.</p></div>
<div class="t"><b>Semaine 4</b><h3>Bilan et ajustements</h3><p>Point de pilotage : on affine la cible, le message, le rythme.</p></div></div></div></section>'''
    fun = f'''<section class="section band-soft"><div class="wrap split"><div class="sec-head" data-reveal style="margin:0"><p class="eyebrow">L'entonnoir</p><h2>Du ciblage au rendez-vous, chaque étape se mesure.</h2>
<p class="lead">Exemple d'un cycle de prospection : 128 entreprises ciblées donnent 8 rendez-vous planifiés. Vous voyez où se situe chaque contact et ce qui fonctionne.</p><p class="note">Chiffres d'exemple, à titre illustratif.</p></div>
<div data-reveal="120">{funnel()}</div></div></section>'''
    liv = f'<section class="section" id="livraison"><div class="wrap">{sec_head("Notre livraison", "Un dossier complet pour chaque rendez-vous.", "Vos commerciaux arrivent préparés : profil, contexte, besoin, niveau d\'intérêt et prochaine étape.")}{delivery()}</div></section>'
    rep = f'''<section class="section band-soft"><div class="wrap split"><div data-reveal>{laptop()}</div><div class="sec-head" data-reveal="120" style="margin:0"><p class="eyebrow">Reporting</p><h2>Un pipeline <mark class="hl">prévisible et mesurable.</mark></h2>
<p class="lead">Un tableau de bord partagé suit les entreprises ciblées, les décideurs contactés, les projets qualifiés et les rendez-vous planifiés. Vous pilotez avec des chiffres, pas des impressions.</p></div></div></section>'''
    vid = ucards_section(ic, P, "La méthode <mark class='hl'>en un coup d'œil.</mark>", "Quatre étapes qui se suivent : l'action, et le moyen utilisé pour chacune.")
    body = hero + s + tl + fun + liv + rep + vid + cta()
    page("comment-ca-marche.html", "Comment ça marche, NOVOLENS", "La méthode NOVOLENS en cinq étapes : calibrage, prospection, rendez-vous qualifiés livrés avec contexte et reporting.", body, "comment-ca-marche.html", [ORG])

# =====================================================================
# RÉSULTATS
# =====================================================================
def build_resultats():
    hero = f'''<section class="page-hero"><div class="wrap">{crumbs("Résultats")}<p class="eyebrow">Résultats</p>
<h1>Des rendez-vous qui <mark class="hl">font avancer votre pipeline.</mark></h1>
<p class="lead">Les indicateurs que nous suivons, les cas clients qui arrivent et les retours de dirigeants.</p></div></section>'''
    kp = f'''<section class="section band-white"><div class="wrap"><div class="grid-3">
<article class="card" data-reveal><span class="big" data-count="70" data-pre="+" data-suf=" %">+70 %</span><h3>de rendez-vous qualifiés*</h3><p>Objectif de progression fixé avec vous dès le calibrage, mesuré dans le reporting.</p></article>
<article class="card" data-reveal="100"><span class="big">&lt; 1 mois</span><h3>pour les premiers résultats</h3><p>Du calibrage aux premiers rendez-vous dans votre agenda.</p></article>
<article class="card" data-reveal="200"><span class="big" data-count="24">24</span><h3>projets qualifiés (exemple)</h3><p>Sur 128 entreprises ciblées, 8 rendez-vous planifiés dans l'exemple de reporting.</p></article></div></div></section>'''
    vals = [1, 2, 4, 5, 7, 8]
    bars = "".join(f'<div class="bar"><em>{v}</em><i style="--h:{round(v/8*100)}%;--i:{i}"></i></div>' for i, v in enumerate(vals))
    chart = f'''<section class="section"><div class="wrap split"><div class="sec-head" data-reveal style="margin:0"><p class="eyebrow">Montée en puissance</p><h2>Un pipeline qui se remplit semaine après semaine.</h2>
<p class="lead">La régularité fait la différence : chaque semaine ajoute de nouveaux rendez-vous qualifiés à vos équipes. Dans l'exemple, 8 rendez-vous cumulés en 6 semaines.</p><p class="note">Courbe d'exemple, à titre illustratif.</p></div>
<div class="card" data-reveal="120" style="padding:24px"><h4>Rendez-vous qualifiés cumulés, 6 semaines (exemple)</h4><div class="chart" data-in><div class="bars">{bars}</div><div class="bar-labels"><span>S1</span><span>S2</span><span>S3</span><span>S4</span><span>S5</span><span>S6</span></div></div></div></div></section>'''
    cas = f'''<section class="section band-soft"><div class="wrap">{sec_head("Secteurs ciblés", "Trois secteurs où nous construisons nos premiers cas.", "Un exemple de cas complet est présenté dans le <a class='vi' href='cas-client.html'>gabarit de cas client</a>.")}
<div class="grid-3">
<article class="card" data-reveal><span class="ico">{ic("building")}</span><h3>Industrie</h3><ul class="target-list"><li>Directeur Général</li><li>ETI</li></ul><p>Des décideurs difficiles à joindre et des cycles de vente longs : le rendez-vous qualifié ouvre le dialogue au bon niveau.</p></article>
<article class="card" data-reveal="100"><span class="ico">{ic("shield")}</span><h3>Santé</h3><ul class="target-list"><li>Direction Achats</li><li>Groupe</li></ul><p>Des achats structurés, plusieurs interlocuteurs : une approche par compte et un contexte clair avant chaque échange.</p></article>
<article class="card" data-reveal="200"><span class="ico">{ic("zap")}</span><h3>Tech &amp; Logiciels</h3><ul class="target-list"><li>CEO</li><li>Scale-up</li></ul><p>Des équipes qui vendent déjà : la prospection prend en charge les relances pour que le pipeline reste régulier.</p></article></div></div></section>'''
    vid = f'''<section class="section"><div class="wrap proof-feature"><figure class="solid" data-reveal style="margin:0">{IMG("livraison.jpg", "Rendez-vous d'affaires entre un dirigeant et deux interlocuteurs")}</figure>
<div class="sec-head" data-reveal="120" style="margin:0;align-content:center"><p class="eyebrow">La parole aux dirigeants</p><h2>Des retours qui parlent de rendez-vous, pas de promesses.</h2><p class="lead">Les vidéos et verbatims clients apparaîtront ici dès leur validation. Les textes affichés dans le mur ci-dessous sont des exemples.</p></div></div>{proof_wall()}</section>'''
    body = hero + kp + chart + cas + vid + cta()
    page("resultats.html", "Résultats NOVOLENS", "Résultats NOVOLENS : rendez-vous qualifiés, premiers résultats en moins d'un mois, cas clients et témoignages de dirigeants.", body, "resultats.html", [ORG])

# =====================================================================
# TARIFS
# =====================================================================
def build_tarifs():
    def plan(name, tag, desc, feats, hot=False, cta_t="Demander un devis"):
        lis = "".join(f"<li>{ic('check')}{f}</li>" for f in feats)
        badge = '<span class="badge">Le plus choisi</span>' if hot else ""
        btn = "btn-primary" if hot else "btn-ghost"
        return f'''<article class="plan{" hot" if hot else ""}" data-reveal>{badge}<div><h3>{name}</h3><p class="muted" style="margin-top:6px">{tag}</p></div>
<div class="price">Sur devis<small>{desc}</small></div><ul>{lis}</ul><a class="btn {btn}" href="contact.html">{cta_t}</a></article>'''
    plans = (plan("Lancement", "Tester sur une cible", "Mission pilote d'un mois", ["Atelier de cadrage", "Une cible et un message", "Prospection et qualification", "Rendez-vous livrés avec contexte", "Bilan de fin de mission"]) +
             plan("Croissance", "Un flux régulier de rendez-vous", "Engagement mensuel, durée à définir", ["Tout Lancement", "Plusieurs cibles et messages", "Relances multicanales persévérantes", "Reporting partagé en continu", "Point de pilotage hebdomadaire"], hot=True) +
             plan("Grands comptes", "Comptes stratégiques et nouveaux marchés", "Approche sur mesure", ["Tout Croissance", "Approche par compte, multi-interlocuteurs", "Recherche de signaux d'achat", "Coordination avec vos équipes ventes", "Pilotage dédié"]))
    hero = f'''<section class="page-hero"><div class="wrap">{crumbs("Tarifs")}<p class="eyebrow">Tarifs</p>
<h1>Une offre sur mesure, <span class="accent">calée sur votre cible.</span></h1>
<p class="lead">Le prix dépend de la cible, du volume de rendez-vous visé et de la durée. Nous construisons un devis après un échange de 15 minutes, sans engagement.</p></div></section>'''
    pl = f'<section class="section band-white"><div class="wrap"><div class="plans">{plans}</div><p class="note" style="margin-top:24px;text-align:center">Chaque devis est établi après un échange de 15 minutes.</p></div></section>'
    inc = [("target", "Ciblage sur mesure"), ("send", "Prospection multicanale"), ("filter", "Qualification des besoins"), ("calcheck", "Prise de rendez-vous"), ("file", "Dossier de contexte"), ("chart", "Reporting partagé")]
    cc = "".join(f'<article class="card" data-reveal="{(i%3)*80}" style="padding:22px"><span class="ico">{ic(i_)}</span><h4>{t}</h4></article>' for i, (i_, t) in enumerate(inc))
    incl = f'<section class="section"><div class="wrap">{sec_head("Dans toutes les formules", "Ce qui est toujours inclus.")}<div class="grid-3">{cc}</div></div></section>'
    how = f'''<section class="section band-soft"><div class="wrap split"><div class="sec-head" data-reveal style="margin:0"><p class="eyebrow">Votre devis</p><h2>Comment nous construisons votre prix.</h2>
<p class="lead">Un seul gros client signé suffit souvent à rentabiliser une mission. Nous partons donc de la valeur d'un client pour calibrer l'effort de prospection.</p></div>
<div class="side-steps" data-reveal="120"><div class="s"><span class="n">1</span><div><h4>Valeur d'un client</h4><p>Panier moyen, cycle de vente et taux de signature de vos équipes.</p></div></div>
<div class="s"><span class="n">2</span><div><h4>Cible et volume</h4><p>Nombre de comptes à atteindre et de rendez-vous visés par mois.</p></div></div>
<div class="s"><span class="n">3</span><div><h4>Durée et rythme</h4><p>Mission pilote ou engagement mensuel, selon votre besoin.</p></div></div></div></div></section>'''
    sim = f"""<section class="section" id="simulateur"><div class="wrap split"><div class="sec-head" data-reveal style="margin:0"><p class="eyebrow">Simulateur de gain</p><h2>Combien vaut <mark class="hl">un flux de rendez-vous</mark> pour vous ?</h2>
<p class="lead">Entrez vos propres chiffres. Le calcul se fait dans votre navigateur et n'est <strong class="vi">pas une promesse de résultat</strong>.</p></div>
<div class="sim card" data-reveal="120" id="sim"><p class="sim-flag">Valeurs d'exemple, remplacez-les par les vôtres</p>
<div class="sim-fields"><div class="field"><label for="sim-val">Valeur moyenne d'un client (€)</label><input id="sim-val" type="number" inputmode="numeric" min="0" step="500" value="20000"></div>
<div class="field"><label for="sim-rate">Rendez-vous qui deviennent clients (%)</label><input id="sim-rate" type="number" inputmode="numeric" min="0" max="100" step="1" value="20"></div>
<div class="field"><label for="sim-rdv">Rendez-vous qualifiés par mois</label><input id="sim-rdv" type="number" inputmode="numeric" min="0" step="1" value="8"></div></div>
<div class="sim-out" aria-live="polite"><div><small>Nouveaux clients par mois</small><b id="sim-clients">0</b></div><div><small>Chiffre d'affaires par mois</small><b id="sim-month">0</b></div><div><small>Sur 12 mois</small><b id="sim-year">0</b></div></div>
<p class="note">Estimation calculée uniquement à partir de vos chiffres : rendez-vous par mois × taux × valeur d'un client.</p></div></div></section>"""
    body = hero + pl + sim + incl + how + cta("Demandez votre devis en 15 minutes.", "Dites-nous qui vous voulez rencontrer. Nous revenons vers vous sous 24 h avec une proposition adaptée.")
    page("tarifs.html", "Tarifs NOVOLENS", "Tarifs NOVOLENS : trois formules de prospection B2B externalisée, sur devis, adaptées à votre cible et à votre volume de rendez-vous.", body, "tarifs.html", [ORG])

# =====================================================================
# FAQ
# =====================================================================
FAQ = [
 ("Qu'est-ce qu'un rendez-vous qualifié ?", "C'est un échange confirmé avec un décideur dont nous avons vérifié la fonction, le besoin, l'intérêt et la disponibilité, selon les critères définis avec vous lors du calibrage."),
 ("En combien de temps obtient-on les premiers résultats ?", "Nous visons les premiers rendez-vous en moins d'un mois après le cadrage. Le délai exact dépend de votre cible et de votre marché."),
 ("À quelles entreprises s'adresse NOVOLENS ?", "Aux PME en croissance, aux ETI et aux grands groupes qui vendent en B2B et veulent remplir leur pipeline avec des décideurs, notamment dans l'industrie, la santé, la tech et les services B2B."),
 ("Comment prospectez-vous ?", "Par une approche multicanale personnalisée : appels, e-mails et messages professionnels, avec des relances persévérantes jusqu'à obtenir une réponse claire."),
 ("Qui contacte mes prospects, et en quel nom ?", "Une équipe dédiée, formée à votre offre. Le discours et le positionnement sont validés avec vous avant le lancement."),
 ("Comment suis-je tenu informé ?", "Vous disposez d'un reporting partagé qui suit chaque étape, du ciblage au rendez-vous planifié, et d'un point de pilotage régulier."),
 ("Que se passe-t-il après le rendez-vous ?", "Vos équipes prennent le relais avec un dossier complet : profil du décideur, contexte, besoin identifié, niveau d'intérêt et compte rendu."),
 ("Y a-t-il un engagement ?", "L'échange initial de 15 minutes est sans engagement. Ensuite, la durée dépend de la formule choisie, de la mission pilote à l'engagement mensuel."),
 ("Comment sont calculés vos tarifs ?", "Sur devis, selon la cible, le volume de rendez-vous visé et la durée. Nous partons de la valeur d'un client pour calibrer l'effort."),
 ("Et pour les données personnelles ?", "Nous menons une prospection B2B encadrée, respectueuse du RGPD, avec un droit d'opposition simple pour les personnes contactées."),
]
def build_faq():
    items = "".join(f'<details data-reveal><summary>{q}<span class="pm">{ic("plus")}</span></summary><div class="ans">{a}</div></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    hero = f'''<section class="page-hero"><div class="wrap">{crumbs("FAQ")}<p class="eyebrow">Questions fréquentes</p>
<h1>Tout ce que vous voulez savoir <span class="accent">avant de nous parler.</span></h1><p class="lead">Une question qui n'est pas ici ? Réservez un échange de 15 minutes, un expert vous répond.</p></div></section>'''
    body = hero + f'<section class="section band-white"><div class="wrap"><div class="faq-tools"><button class="linkbtn" id="faq-toggle" type="button">Tout ouvrir</button></div><div class="faq">{items}</div></div></section>' + cta("Une autre question ?", "Posez-la directement à un expert NOVOLENS, en 15 minutes, sans engagement.")
    page("faq.html", "FAQ NOVOLENS", "Réponses aux questions fréquentes sur NOVOLENS : rendez-vous qualifiés, délais, méthode, reporting, engagement et tarifs.", body, "faq.html", [ORG, ld])

# =====================================================================
# CONTACT
# =====================================================================
def build_contact():
    days = [("Mardi", ["9h30", "11h00", "14h30", "16h00"]), ("Mercredi", ["9h30", "11h00", "14h30", "16h00"]), ("Jeudi", ["9h30", "11h00", "14h30", "16h00"])]
    dd = "".join(f'<div class="day"><h4>{d}</h4>' + "".join(f'<button type="button" class="tbtn" aria-pressed="false" data-label="{d} à {t}">{t}</button>' for t in ts) + "</div>" for d, ts in days)
    def f(id_, label, typ="text", req=True, auto=""):
        r = " required" if req else ""
        return f'<div class="field"><label for="{id_}">{label}{" *" if req else ""}</label><input id="{id_}" name="{id_}" type="{typ}"{r}{(' autocomplete="' + auto + '"') if auto else ""}><span class="err" aria-live="polite"></span></div>'
    form = f'''<div class="form" data-reveal><form id="contact-form" novalidate>
<div class="row2">{f("prenom", "Prénom", auto="given-name")}{f("nom", "Nom", auto="family-name")}</div>
<div class="row2">{f("email", "E-mail professionnel", "email", auto="email")}{f("tel", "Téléphone", "tel", False, "tel")}</div>
<div class="row2">{f("societe", "Entreprise", auto="organization")}{f("poste", "Fonction", auto="organization-title")}</div>
<div class="field"><label for="taille">Taille de l'entreprise</label><select id="taille" name="taille"><option>PME (10 à 250 salariés)</option><option>ETI (250 à 5 000 salariés)</option><option>Grand groupe (5 000 salariés et plus)</option></select></div>
<div class="field"><label for="objectif">Votre objectif</label><textarea id="objectif" name="objectif" placeholder="Qui souhaitez-vous rencontrer ? Quel secteur, quelle fonction ?"></textarea></div>
<div class="slots-block"><p class="slots-title">Créneau souhaité (facultatif)</p><div class="days" style="margin-top:10px">{dd}</div><p class="note" id="chosen" style="margin-top:10px" aria-live="polite">Aucun créneau choisi.</p></div>
<label class="consent"><input type="checkbox" id="consent" required><span>J'accepte d'être recontacté au sujet de ma demande. <span class="err" aria-live="polite"></span></span></label>
<button class="btn btn-primary" type="submit">Réserver mon échange {ic("arrow","arr")}</button>
<p class="note">Aperçu : ce formulaire n'envoie rien tant qu'il n'est pas relié à votre messagerie ou à votre agenda.</p></form>
<div class="success" role="status"><svg viewBox="0 0 72 72" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="36" cy="36" r="30"/><path d="m23 37 9 9 17-19"/></svg>
<h3>Merci, votre demande est prête.</h3><p class="muted">Un expert NOVOLENS vous répond sous 24 h. <span id="success-slot"></span></p><a class="btn btn-ghost" href="index.html">Retour à l'accueil</a></div></div>'''
    side = f'''<div class="side-steps" data-reveal="120"><div class="sec-head" style="margin:0 0 6px"><p class="eyebrow">Et ensuite ?</p><h2>Trois étapes, sans engagement.</h2></div>
<div class="s"><span class="n">1</span><div><h4>Réponse sous 24 h</h4><p>Un expert confirme le créneau ou vous propose une alternative.</p></div></div>
<div class="s"><span class="n">2</span><div><h4>Échange de 15 minutes</h4><p>Vos objectifs, votre cible, vos contraintes. Nous écoutons d'abord.</p></div></div>
<div class="s"><span class="n">3</span><div><h4>Proposition sur mesure</h4><p>Si cela a du sens pour vous, nous vous envoyons un devis adapté.</p></div></div>
<ul class="checks" style="margin-top:8px"><li>{ic("check")}Sans engagement</li><li>{ic("check")}Réponse sous 24 h</li><li>{ic("check")}Échange avec un expert</li></ul>
<p class="muted">Vous préférez écrire ? contact@novolens.fr </p></div>'''
    hero = f'''<section class="page-hero"><div class="wrap">{crumbs("Contact")}<p class="eyebrow">Échange stratégique</p>
<h1>Parlons de vos <span class="accent">objectifs de croissance.</span></h1><p class="lead">Un échange de 15 minutes avec un expert NOVOLENS pour comprendre vos enjeux et voir comment nous pouvons vous apporter des rendez-vous qualifiés.</p></div></section>'''
    body = hero + f'<section class="section band-white" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap contact-grid">{form}{side}</div></section>'
    page("contact.html", "Contact NOVOLENS", "Réservez un échange de 15 minutes avec un expert NOVOLENS pour parler de vos objectifs de croissance. Sans engagement, réponse sous 24 h.", body, None, [ORG])

exec(open(os.path.join(HERE, 'v3_extra.py'), encoding='utf-8').read())
build_index(); build_pourquoi(); build_methode(); build_resultats(); build_tarifs(); build_faq(); build_contact()
if V3:
    build_cas(); build_404(); build_seo(); build_ds()
shutil.copytree(os.path.join(HERE, "img"), os.path.join(DIST, "img"))
for fn in ("style.css", "app.js"):
    shutil.copy(os.path.join(HERE, fn), os.path.join(DIST, fn))
if V3:
    with open(os.path.join(DIST, "style.css"), "a") as f:
        f.write(open(os.path.join(HERE, "style_v2.css")).read()); f.write(open(os.path.join(HERE, "style_v3.css")).read())
elif V2:
    with open(os.path.join(DIST, "style.css"), "a") as f:
        f.write(open(os.path.join(HERE, "style_v2.css")).read())
print("ok", sorted(os.listdir(DIST)))
