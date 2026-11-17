# Accueil V4 : mise en page inspirée de la référence fournie (ton lavande clair, titres gras noir et violet,
# visage à droite avec cartes de chiffres, bandeau de confiance, rangée de 6 fonctions, aperçu d'interface, carte d'appel final).
# Exécuté par build.py dans son espace de noms.

def _spark(cls=""):
    return f'<svg class="v4-spark {cls}" viewBox="0 0 40 40" aria-hidden="true"><path d="M20 3c1.2 9.5 7.5 15.8 17 17-9.5 1.2-15.8 7.5-17 17-1.2-9.5-7.5-15.8-17-17 9.5-1.2 15.8-7.5 17-17z" fill="none" stroke="#14102F" stroke-width="1.6" stroke-linejoin="round"/></svg>'


def build_index_v4():
    stats = "".join(
        f'<div class="v4-stat" style="--k:{i}"><span class="v4-sic">{ic(ico)}</span><div><b>{big}</b><small>{small}</small></div></div>'
        for i, (ico, big, small) in enumerate([
            ("trend", "+70 %*", "rendez-vous qualifiés visés"),
            ("clock", "24 h", "pour vous répondre"),
            ("calcheck", "15 min", "pour un premier échange"),
        ]))
    hero = f"""<section class="v4-hero"><div class="wrap v4-hero-grid">
<div class="v4-copy"><span class="v4-pill" data-reveal>Prospection B2B externalisée</span>
<h1 data-reveal>Des <span class="nw">rendez-vous</span> qualifiés.<br><span class="v4-vi">Sans effort de prospection.</span></h1>
<p class="lead" data-reveal>Nous identifions <strong class="vi">les bons prospects</strong>, les contactons, les qualifions et vous livrons des rendez-vous avec <strong class="vi">des décideurs réellement intéressés</strong>.</p>
<div class="cta-row" data-reveal><a class="btn btn-primary" href="contact.html">Réserver un échange {ic("arrow","arr")}</a><a class="v4-link" href="comment-ca-marche.html"><span class="play-dot">{PLAY}</span>Voir la méthode</a></div>
<ul class="checks" data-reveal><li>{ic("check")}Sans engagement</li><li>{ic("check")}Réponse sous 24 h</li><li>{ic("check")}Échange avec un expert</li></ul></div>
<div class="v4-visual"><svg class="v4-blob" viewBox="0 0 420 520" aria-hidden="true"><path d="M70 80C140 10 300 30 350 110c40 70 20 150-10 220-30 70-90 150-170 160C90 500 20 440 30 340 40 240 10 150 70 80z" fill="#8F7DFF" fill-opacity=".2"/></svg>
<svg class="v4-doodle" viewBox="0 0 120 70" aria-hidden="true"><path d="M2 4C40 6 70 20 75 40c4 18-18 22-20 8-2-12 20-10 28-4 10 8 22 12 36 10" fill="none" stroke="#14102F" stroke-width="1.8" stroke-linecap="round"/></svg>
{_spark("s1")}{_spark("s2")}
{IMG("hero-person.webp", "Dirigeant souriant, bras croisés", "v4-person", eager=True)}
<div class="v4-stats">{stats}</div></div></div></section>"""
    sectors = ["Industrie", "Santé", "Tech &amp; Logiciels", "Services B2B", "Distribution", "Finance"]
    trust = f"""<section class="v4-trust"><div class="wrap"><div class="v4-trustcard" data-reveal><p>Pensé pour les décideurs des PME, ETI et grands groupes</p>
<ul>{"".join(f'<li style="--w:{[800,700,800,700,800,700][i]}">{s}</li>' for i, s in enumerate(sectors))}</ul></div></div></section>"""
    feats = [("target", "Ciblage sur mesure", "Secteur, taille et fonction définis avec vous."), ("send", "Prospection multicanale", "Téléphone, e-mail et LinkedIn, avec relances."),
             ("filter", "Qualification rigoureuse", "Décideur, besoin et intérêt vérifiés."), ("calcheck", "Rendez-vous planifiés", "Directement dans votre agenda."),
             ("file", "Dossier de contexte", "Profil, enjeux et compte rendu pour chaque rendez-vous."), ("chart", "Reporting partagé", "Chaque étape suivie, du ciblage au rendez-vous.")]
    fe = "".join(f'<div class="v4-feat" style="--k:{i}"><span class="v4-fic">{ic(i_)}</span><h3>{t}</h3><p>{d}</p></div>' for i, (i_, t, d) in enumerate(feats))
    features = f"""<section class="v4-sec"><div class="wrap"><h2 class="v4-h2" data-reveal>Tout ce qu'il faut pour <span class="v4-vi">remplir votre agenda</span></h2><div class="v4-feats" data-reveal="100">{fe}</div></div></section>"""
    steps = ucards_section(ic, P, "Comprendre NOVOLENS <span class='v4-vi'>en un coup d'œil</span>", "Quatre étapes qui se suivent. À chaque fois, <strong class='vi'>l'action</strong> et <strong class='vi'>le moyen</strong> utilisé pour obtenir vos rendez-vous.")
    steps = steps.replace('<section class="section band-soft" id="video">', '<section class="v4-sec" id="video">', 1)
    rows = ""
    for i, (ini, role, sect, when) in enumerate([("DG", "Directeur Général", "Industrie · 500 M€", "Jeudi · 10h00"), ("DA", "Directrice Achats", "Santé · Groupe", "Vendredi · 14h30"), ("CE", "CEO", "Tech & Logiciels", "Lundi · 9h30")]):
        rows += f'<div class="v4-row" style="--k:{i}"><span class="avatar">{ini}</span><div><b>Rendez-vous qualifié</b><small>{role} · {sect}</small></div><span class="v4-when">{when}</span><span class="v4-open">Voir le dossier</span></div>'
    side = "".join(('<li class="on">' if i == 0 else '<li>') + t + '</li>' for i, t in enumerate(["Tous les rendez-vous", "Industrie", "Santé", "Tech & Logiciels", "Services B2B", "À relancer"]))
    mini = "".join(f'<div><span>{ic(i_)}</span><b>{t}</b><small>{d}</small></div>' for i_, t, d in [("search", "Recherche rapide", "Un compte, une fonction"), ("layers", "Classé par secteur", "Facile à parcourir"), ("calendar", "Nouveaux rendez-vous", "Chaque semaine"), ("file", "Dossier complet", "Avant chaque échange")])
    cockpit = f"""<section class="v4-sec"><div class="wrap v4-inside"><div class="v4-inside-l" data-reveal><h2 class="v4-h2 left">Dans votre <span class="v4-vi">espace de pilotage</span></h2><p class="lead">Un seul endroit pour suivre vos rendez-vous, leur contexte et le reporting. Illustration d'interface.</p><div class="v4-mini">{mini}</div></div>
<div class="v4-ui" data-reveal="120" data-in><div class="v4-search">{ic("search")}<span>Rechercher un compte, une fonction, un secteur…</span></div><div class="v4-ui-grid"><ul class="v4-side">{side}</ul><div class="v4-rows">{rows}</div></div></div></div></section>"""
    cibles = f"""<section class="v4-sec"><div class="wrap"><h2 class="v4-h2" data-reveal>Pensé pour les entreprises <span class="v4-vi">qui ont des ambitions</span></h2>
<div class="grid-3" style="margin-top:32px">
<article class="card" data-reveal>{PHOTO("pme")}<span class="ico">{ic("briefcase")}</span><h3>PME en croissance</h3><p>Vous avez une offre qui a fait ses preuves et un besoin de nouveaux comptes, sans recruter ni structurer une équipe de prospection.</p></article>
<article class="card" data-reveal="100">{PHOTO("eti")}<span class="ico">{ic("building")}</span><h3>ETI</h3><p>Vous visez des comptes plus complexes et plus structurés, avec plusieurs interlocuteurs à convaincre.</p></article>
<article class="card" data-reveal="200">{PHOTO("grand")}<span class="ico">{ic("layers")}</span><h3>Grands groupes</h3><p>Vous souhaitez ouvrir de nouveaux marchés ou comptes stratégiques avec une approche ciblée, qualifiée et mesurable.</p></article></div></div></section>"""
    proof = f"""<section class="v4-sec"><div class="wrap"><h2 class="v4-h2" data-reveal>Des dirigeants qui accélèrent <span class="v4-vi">leur croissance</span></h2><p class="note" style="margin:10px 0 22px">Exemples de retours, en attendant les avis clients validés.</p></div>{proof_wall()}</section>"""
    final = f"""<section class="v4-sec"><div class="wrap"><div class="v4-final" data-reveal><span class="v4-trophy">{ic("target")}</span><div><h2>Parlez à un expert.<br>Remplissez votre agenda.</h2><p>Un échange de 15 minutes pour comprendre vos enjeux et voir comment nous pouvons vous apporter des rendez-vous qualifiés.</p></div>
<div class="v4-final-cta"><a class="btn btn-primary" href="contact.html">Réserver un échange {ic("arrow","arr")}</a><small>{ic("shield")}Sans engagement · réponse sous 24 h</small></div></div></div></section>"""
    body = hero + trust + features + steps + cockpit + cibles + proof + final
    page("index.html", "NOVOLENS", "NOVOLENS livre des rendez-vous qualifiés avec des décideurs : prospection B2B externalisée pour PME, ETI et grands groupes.", body, None, [ORG], index=True)
