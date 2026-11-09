"""Tire au sort un panel de spectateurs : 5 profils × 2 panels × 10, attributs stratifiés.

  python3 -I panel.py personas.json [graine]

Changer la graine donne 100 nouveaux spectateurs ; garder la même permet de rejouer le même panel
sur une nouvelle version (comparaison plus juste). Adapter PROFILS au sujet de la vidéo.
"""
import json, random, sys
PROFILS = {
 'A': ("Le public cœur : ceux qui ont le problème traité", ["développeuse freelance", "fondateur de SaaS B2B", "maker no-code", "designer qui lance un outil", "dev mobile indé", "consultant qui productise un service"]),
 'B': ("Curieux de l'outil ou du thème", ["chef de projet curieux d'IA", "prof qui teste les outils IA", "développeur back-end", "créateur de contenu tech", "analyste data", "étudiant en informatique"]),
 'C': ("Tout-venant poussé par l'accueil YouTube", ["commerçant", "infirmière", "commercial", "freelance en graphisme", "retraité curieux", "community manager"]),
 'D': ("Experts sceptiques du domaine", ["head of growth", "PM senior", "consultante go-to-market", "fondateur d'agence", "marketeur B2C", "investisseur early-stage"]),
 'E': ("Débutants, peu de contexte", ["lycéen passionné", "étudiante en reconversion", "salarié avec une idée", "stagiaire marketing", "apprenti développeur", "jeune diplômé"])}
SOURCES = ["recherche précise", "recherche large", "suggestion après une vidéo voisine", "page d'accueil", "lien partagé dans un groupe"]
APPAREILS = ["mobile", "mobile", "ordinateur", "ordinateur", "tablette", "TV"]
CONTEXTES = ["concentré, prend des notes", "en fond pendant une autre tâche", "transports, son bas", "pause déjeuner", "le soir, détendu", "entre deux réunions"]
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
out = {f"{s}{h}": [{"id": f"{s}{h}{k:02d}", "profil": lib, "metier": random.choice(m), "age": random.randint(18, 62), "source": random.choice(SOURCES),
                    "appareil": random.choice(APPAREILS), "contexte": random.choice(CONTEXTES), "expertise_1a5": random.randint(1, 5),
                    "patience": random.choice(["faible", "moyenne", "moyenne", "forte"])} for k in range(10)]
       for s, (lib, m) in PROFILS.items() for h in (1, 2)}
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(sum(map(len, out.values())), "spectateurs →", sys.argv[1])
