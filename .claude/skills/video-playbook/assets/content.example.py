"""Exemple de content.py : copier dans le dossier de travail sous le nom content.py et remplacer.
Les aides SVG viennent de build.py (box, ar, pa, dia, pill, band, chain, T, fig).
Repère des figures : viewBox 920 de large ; boîtes de 150 à 160 px ; texte ≤ 22 caractères par ligne dans une boîte.
Couleurs : "c" bleu = préparer/comprendre, "n" vert = faire, "h" jaune = accélérer, "d" pointillé = option ou échec.
"""
from build import *

META = {
    "video_id": "VIDEO_ID",            # identifiant YouTube (après v=)
    "slug": "sujet-court-v1",          # clé de mémoire locale (cases, canevas)
    "tab_title": "Playbook Sujet",     # titre d'onglet : 2 à 4 mots
    "releve": "novembre 2026",         # mois des recherches web
    "out": "",                         # dossier où copier index.html (non suivi par git), ou "" pour ne rien copier
}


def FIGURES():
    F = {}

    # 1. Boucle de la méthode (page methode) : rangée du haut, retour par le bas
    m = "f1"; xs = [10, 196, 382, 568, 754]
    L = [["Élément 1", "détail"], ["Élément 2", "détail"], ["Élément 3", "détail"], ["Élément 4", "détail"], ["Élément 5", "détail"]]
    i = ""
    for k, x in enumerate(xs):
        i += box(x, 30, 156, 60, L[k], "c" if k < 2 else "n")
        if k < 4: i += ar(x + 156, 60, x + 184, 60, m)
    i += ar(832, 90, 832, 176, m)
    i += box(754, 180, 156, 60, ["Élément 6", "détail"], "n") + ar(754, 210, 704, 210, m)
    i += box(500, 180, 200, 60, ["Élément 7", "détail"], "h") + ar(500, 210, 450, 210, m)
    i += box(226, 180, 220, 60, ["Mesure et rituel", "détail"], "")
    i += pa("M226 210 H88 V94", m, "d") + T(150, 160, "tour suivant", "sv-tm", "middle")
    i += band(10, 270, 900, 34, "L'idée qui relie tout")
    F["loop"] = fig(i, 920, 312, "Description complète de la boucle pour les lecteurs d'écran",
                    "<b>Titre de la figure.</b> Ce que montrent les couleurs. {O} d'après [[0:00]]", m)

    # 2. Chaîne simple (rituel, funnel, pipeline)
    m = "f2"
    i = chain([["Étape 1", "détail"], ["Étape 2", "détail"], ["Étape 3", "détail"], ["Étape 4", "détail"]], m, classes=["c", "", "", "n"], ops=["5 min", "10 min", "15 min"])
    F["ritual"] = fig(i, 920, 110, "Description", "<b>Titre.</b> Légende. {V} [[0:00]]", m)

    # 3. Logigramme avec décision
    m = "f3"
    i = pill(10, 70, 110, 40, "Départ", m) + ar(120, 90, 148, 90, m)
    i += dia(250, 90, 100, 50, ["Condition", "remplie ?"])
    i += ar(350, 90, 398, 90, m, "ok") + T(374, 80, "oui", "sv-oklbl", "middle")
    i += box(400, 60, 200, 60, ["Action A", "détail"], "n")
    i += ar(250, 140, 250, 188, m, "no") + T(262, 170, "non", "sv-nolbl")
    i += box(150, 190, 200, 60, ["Action B", "détail"], "d")
    F["case"] = fig(i, 920, 262, "Description", "<b>Titre.</b> Légende. {V} [[0:00]]", m)

    # 4. Courbe illustrative (croissance, positions dans le temps)
    m = "f4"
    i = '<line class="sv-ln d" x1="60" y1="230" x2="900" y2="230"/><line class="sv-ln d" x1="60" y1="20" x2="60" y2="230"/>'
    i += '<path class="sv-ac" d="M60 226 C200 222 300 216 380 200 C470 182 560 140 640 100 C720 62 800 40 900 28"/>'
    i += '<line class="sv-ln d" x1="380" y1="200" x2="380" y2="40"/>' + T(388, 52, "point de bascule", "sv-tb")
    i += T(60, 250, "0", "sv-tm", "middle") + T(900, 250, "temps", "sv-tm", "end")
    F["theme1"] = fig(i, 920, 262, "Description", "<b>Titre.</b> Forme illustrative, pas des données réelles. {O}", m)
    return F


# Glossaire : (terme affiché, [formes à repérer dans le texte], sensible à la casse, définition en une ligne, "acr" ou "jar")
# Mettre les formes au pluriel et au singulier ; les sigles en sensible à la casse (True).
G = [
    ("SEO", ["SEO"], True, "Search Engine Optimization : être bien placé dans Google sans payer.", "acr"),
    ("Churn", ["churn"], False, "Part des clients qui résilient sur une période.", "jar"),
]

# Chapitres de la vidéo : (horodatage, titre du chapitre, id de la page du playbook ou "")
CH = [("0:00", "Intro", ""), ("1:58", "Chapitre", "cas")]

# Noms mal transcrits, chiffres contradictoires, passages inaudibles (HTML permis)
VERIFY = ["« Nom transcrit » : probablement « nom réel »."]

# Sources de la recherche web : (url, libellé)
SRC = [("https://example.com/page", "Libellé de la source")]
