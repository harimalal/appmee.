# Pages et fichiers propres à la V3 : cas client (gabarit), 404, sitemap et robots.
# Ce fichier est exécuté par build.py dans son espace de noms (il réutilise ses fonctions).

def ucards_section_inner():
    from ucards import section as _s
    html = _s(ic, P, "x", "x")
    start = html.index('<div class="ugrid"')
    return html[start:html.rindex('</div></section>')]


def build_cas():
    hero = f"""<section class="page-hero"><div class="wrap">{crumbs("Cas client modèle")}<p class="eyebrow">Cas client · gabarit</p>
<h1>Un cas client, <mark class="hl">du ciblage au contrat.</mark></h1>
<p class="lead">Ce gabarit montre comment un cas réel sera présenté : le contexte, l'action, le résultat et la parole du dirigeant. <strong class="vi">Toutes les données ci-dessous sont des exemples illustratifs.</strong></p>
<p class="exemple-flag">Exemple illustratif, à remplacer par un client réel</p></div></section>"""
    fiche = """<section class="section"><div class="wrap"><div class="fiche" data-reveal>
<div><small>Secteur</small><b>Industrie (exemple)</b></div><div><small>Taille</small><b>ETI (exemple)</b></div><div><small>Cible visée</small><b>Directions générales (exemple)</b></div><div><small>Durée</small><b>3 mois (exemple)</b></div></div></div></section>"""
    ctx = f"""<section class="section"><div class="wrap split"><div class="sec-head" data-reveal style="margin:0"><p class="eyebrow">Le contexte</p><h2>Un agenda commercial qui <mark class="hl">ne se remplissait plus.</mark></h2>
<p class="lead">Une équipe commerciale compétente, mais sans temps pour prospecter les grands comptes. Les relances s'oubliaient et le pipeline dépendait de quelques clients historiques.</p></div>
<div data-reveal="120">{DUO}</div></div></section>"""
    act = f"""<section class="section"><div class="wrap">{sec_head("L'action", "Quatre étapes, un seul objectif : le rendez-vous qualifié.")}{ucards_section_inner()}</div></section>"""
    res = f"""<section class="section"><div class="wrap split"><div data-reveal>{laptop()}</div><div class="sec-head" data-reveal="120" style="margin:0"><p class="eyebrow">Le résultat</p><h2>Un pipeline <mark class="hl">devenu prévisible.</mark></h2>
<p class="lead">Dans cet exemple, 128 comptes ciblés donnent 8 rendez-vous planifiés. Le reporting partagé montre où se situe chaque contact.</p>{funnel()}<p class="note">Chiffres d'exemple, à titre illustratif.</p></div></div></section>"""
    quote = f"""<section class="section"><div class="wrap"><div class="grid-2" style="align-items:stretch">{tcard("Une équipe très professionnelle, déterminée et persévérante. Les rendez-vous sont bien qualifiés et nous gagnons un temps considérable.", "Marc D. (exemple)", "CEO · Tech & Logiciels", initials="M")}
<article class="card" data-reveal><span class="ico">{ic("file")}</span><h3>Ce que ce cas contiendra</h3><p>Le nom du client avec son accord, les objectifs de départ, le nombre de rendez-vous réels, le nombre de projets ouverts et la durée du cycle de vente.</p></article></div></div></section>"""
    body = hero + fiche + ctx + act + res + quote + cta()
    page("cas-client.html", "Cas client modèle NOVOLENS", "Gabarit de cas client NOVOLENS : contexte, action, résultat et parole du dirigeant. Données d'exemple.", body, "resultats.html", [ORG])


def build_404():
    body = f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">Erreur 404</p><h1>Cette page <mark class="hl">n'existe pas.</mark></h1>
<p class="lead">Le lien est peut-être ancien. Revenez à l'accueil ou réservez directement un échange.</p>
<div class="cta-row"><a class="btn btn-primary" href="index.html">Retour à l'accueil {ic("arrow","arr")}</a><a class="btn btn-ghost" href="contact.html">Réserver un échange</a></div></div></section>"""
    page("404.html", "Page introuvable NOVOLENS", "Cette page de NOVOLENS est introuvable. Revenez à l accueil ou réservez un échange de 15 minutes.", body, None, [])


def build_seo():
    pages = ["index.html", "pourquoi-nous.html", "comment-ca-marche.html", "resultats.html", "tarifs.html", "faq.html", "contact.html"]
    base = "https://www.novolens.fr/"  # domaine d'exemple, à remplacer (voir guide.md)
    urls = "".join("<url><loc>" + base + ("" if p == "index.html" else p) + "</loc></url>" for p in pages)
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n")
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: " + base + "sitemap.xml\n")


def build_ds():
    sw = [("Violet marque", "#4B39DD", "#FFFFFF"), ("Violet clair", "#7656F5", "#FFFFFF"), ("Jaune surlignage", "#FFD84D", "#14102F"), ("Encre", "#14102F", "#FFFFFF"),
          ("Texte secondaire", "#4F4B78", "#FFFFFF"), ("Fond blanc", "#FFFFFF", "#14102F"), ("Violet très clair", "#F1EBFF", "#14102F"), ("Violet fin de dégradé", "#D9CDFF", "#14102F"),
          ("Succès", "#157F57", "#FFFFFF"), ("Alerte", "#B03A52", "#FFFFFF")]
    def lumv(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4 for v in c]
        return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
    def rt(a, b):
        x, y = sorted([lumv(a), lumv(b)], reverse=True)
        return (x + .05) / (y + .05)
    sws = "".join(f'<div class="ds-sw" style="background:{h};color:{t}"><b>{n}</b><span>{h}</span><small>texte {t} : {rt(h, t):.1f}:1</small></div>' for n, h, t in sw)
    body = f"""<main id="main" class="ds"><div class="wrap">
<p class="eyebrow">Design system NOVOLENS V3</p><h1>Charte et <mark class="hl">composants.</mark></h1>
<p class="lead">Référence unique des couleurs, textes, composants, mouvements et règles d'usage du site. Thème clair uniquement. Tous les composants ci-dessous sont rendus par la feuille de style du site.</p>

<h2>Couleurs</h2><div class="ds-grid">{sws}</div>
<p class="note">Fonds de section : blanc, puis dégradé violet (#F1EBFF, #E4DBFF, #D9CDFF), en alternance. Un texte de marque sur le violet de fin de dégradé reste à 4,5:1 ou plus.</p>

<h2>Typographie</h2>
<div class="ds-type"><p class="eyebrow">Eyebrow, Inter 700, majuscules espacées</p><h1 style="font-size:2.6rem">Titre 1, Newsreader 700</h1><h2 style="font-size:2rem">Titre 2, Newsreader 700</h2><h3>Titre 3, Newsreader 600</h3>
<p class="lead">Chapô, Inter 400, ligne de 65 caractères au plus pour la lecture.</p><p>Texte courant, Inter 400, 16 px, interligne 1,6. <strong class="vi">Mot important en violet gras</strong> et <mark class="hl">surlignage jaune</mark> pour la valeur.</p><p style="font-family:var(--f-hand);font-size:1.6rem;color:var(--brand)">Annotation manuscrite, Caveat</p></div>

<h2>Boutons et pastilles</h2>
<div class="ds-row"><a class="btn btn-primary" href="#main">Bouton principal</a><a class="btn btn-ghost" href="#main">Bouton secondaire</a><span class="s-label">Étape 1 sur 4</span><span class="mean">Pastille moyen</span><span class="tag">Rendez-vous qualifié</span><span class="draft">Texte provisoire</span><span class="sim-flag">Valeurs d'exemple</span></div>

<h2>Cartes, champs, gain</h2>
<div class="grid-3"><article class="card"><span class="ico">{ic("target")}</span><h3>Carte</h3><p>Bordure fine, ombre douce, halo violet au survol.</p></article>
<div class="form" style="box-shadow:none"><div class="field"><label for="ds-f">Champ de formulaire</label><input id="ds-f" value="Exemple" type="text"><span class="err">Message d'erreur clair sous le champ.</span></div></div>
<div class="gain-line"><span>Ce que vous gagnez</span><b>Un agenda qui se remplit</b></div></div>

<h2>Mouvement</h2>
<table class="tbl-wrap tbl" style="display:table"><thead><tr><th>Effet</th><th>Usage</th><th>Règle</th></tr></thead><tbody>
<tr><td>Apparition au défilement</td><td>Sections sous la ligne de flottaison</td><td>Contenu visible à l'arrêt et en mouvement réduit</td></tr>
<tr><td>Animation d'étape</td><td>Action, moyen, gain pour chaque étape</td><td>Déclenchée à l'entrée à l'écran, rejouable, sans dépendance</td></tr>
<tr><td>Surlignage jaune</td><td>Mots clés des titres</td><td>Un seul groupe de mots par titre</td></tr>
<tr><td>Transition de page</td><td>Navigation entre pages</td><td>Ignorée par les navigateurs qui ne la gèrent pas</td></tr>
<tr><td>Rotation de cibles</td><td>Accueil</td><td>Désactivée en mouvement réduit</td></tr></tbody></table>

<h2>Règles d'usage</h2>
<div class="grid-2"><article class="card"><h3>À faire</h3><ul class="s-list"><li>{ic("checkc")}Alterner fonds blanc et dégradé violet.</li><li>{ic("checkc")}Un seul appel à l'action principal par page.</li><li>{ic("checkc")}Étiqueter « exemple » tout chiffre non fourni.</li><li>{ic("checkc")}Photos pleines, sans transparence.</li></ul></article>
<article class="card"><h3>À éviter</h3><ul class="s-list"><li>{ic("xc")}Thème sombre ou fond noir.</li><li>{ic("xc")}Dégradé animé générique en arrière-plan.</li><li>{ic("xc")}Promesse de résultat non sourcée.</li><li>{ic("xc")}Animation qui cache du texte à l'arrêt.</li></ul></article></div>
</div></main>"""
    css = """.ds{padding-block:48px 80px}.ds h2{margin:48px 0 18px;font-size:1.8rem}.ds-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px}.ds-sw{display:grid;gap:4px;padding:18px;border-radius:18px;border:1px solid rgba(120,100,240,.2)}.ds-sw span{font:600 .85rem var(--f-body)}.ds-sw small{opacity:.9}.ds-type{display:grid;gap:12px;padding:24px;border-radius:24px;background:#fff;border:1px solid var(--line)}.ds-row{display:flex;flex-wrap:wrap;gap:12px;align-items:center}"""
    html = ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
            '<meta name="color-scheme" content="light"><title>Design system NOVOLENS</title><meta name="description" content="Design system du site NOVOLENS V3 : couleurs, typographie, composants, mouvement et règles d\'usage.">'
            + FONTS + '<link rel="stylesheet" href="site/style.css"><style>' + css + '</style></head><body>' + html_body_wrap(body) + '</body></html>')
    with open(os.path.join(DIST, "..", "L02-design-system.html"), "w", encoding="utf-8") as f:
        f.write(html)


def html_body_wrap(b):
    return b
