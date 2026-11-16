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
    page("404.html", "Page introuvable NOVOLENS", "Page introuvable.", body, None, [])


def build_seo():
    pages = ["index.html", "pourquoi-nous.html", "comment-ca-marche.html", "resultats.html", "cas-client.html", "tarifs.html", "faq.html", "contact.html"]
    base = "https://www.novolens.fr/"  # domaine d'exemple, à remplacer (voir guide.md)
    urls = "".join("<url><loc>" + base + ("" if p == "index.html" else p) + "</loc></url>" for p in pages)
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n")
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: " + base + "sitemap.xml\n")
