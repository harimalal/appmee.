# Projet Turf — analyse des courses de trot (Vincennes, Caen, autres hippodromes)

Projet du cockpit : `turf`. Objectif : lire chaque course de trot cheval par cheval selon le protocole TURFITUP de Hari, mesurer honnêtement ce qui marche (par rapport à la cote) et enregistrer les résultats de façon reproductible.

**Statut au 15/11/2026 :** le protocole est utilisable comme grille de lecture, il n'est **pas validé** comme méthode gagnante. Sur 7 courses de Vincennes (14/11) il trouve 9 places sur 21, les 3 premières cotes en trouvent 11 ; au gagnant +2,1 € sur 21 € misés, en couples −25,6 € sur 39 € misés. Aucun signal testé ne bat la cote sur 1 035 courses d'attelé. Décision proposée : suivre le protocole en test aveugle sur au moins 50 courses avant toute mise réelle. Aucune mise réelle n'a été faite, tous les gains sont simulés avec les rapports officiels du PMU.

## Contenu

| Élément | Où | Rôle |
|---|---|---|
| Synthèse des premières modélisations | `SYNTHESE_MODELISATIONS.md` | Ce qui a été testé, ce qui marche, ce qui ne marche pas |
| Règles et tendances | `REGLES_COURSES.md` | 33 règles et 9 tendances avec leur statut (établi, piste, rejeté) |
| Résultats Vincennes 14/11 | `RESULTATS_VINCENNES_2026-11-14.md` | 7 courses lues cheval par cheval, picks, cotes, arrivée, gains |
| Résultats Caen 14/11 | `RESULTATS_CAEN_2026-11-14.md` | 3 courses lues cheval par cheval, 6 lues en mode mécanique |
| Tableau structuré | `resultats/analyses_2026-11-14.csv` | Une ligne par course analysée (reprenable dans un tableur) |
| Workflows | `WORKFLOWS.md` | Les 5 enchaînements pour reproduire (collecte, lecture, bilan, backtest, live) |
| Protocole et référentiel de Hari | `references/` | `protocole-pronostic-trot.md` (déroulé) et `methodologie-trot.md` (critères) |
| Scripts | `scripts/` | Tout le code Python utilisé, sans données |
| Skills | `.claude/skills/turf-*` | Quatre skills pour relancer chaque workflow |

## Ce qui n'est pas dans le dépôt (volontairement)
Les données brutes (pages et API de letrot.com, cache des carrières, commentaires de fin de course) sont privées : usage personnel, rythme lent d'une requête toutes les 3 secondes, jamais commitées ni publiées. Les scripts les recréent à la demande dans un dossier `data/` local. Ce dépôt est public : aucune donnée letrot ni aucun cache n'y figure.

## Données sources
- **PMU** (API publique `online.turfinfo.api.pmu.fr`) : programme, partants, cotes en direct et du matin, arrivée, rapports officiels, 5 dernières performances détaillées.
- **letrot.com** (usage privé, lent) : page course (partants, driver, entraîneur, flags avant course, pronostic Equidia), carrière complète de chaque cheval, commentaires de fin de course.
- **Geny** (pronostics, records) : lu à la demande, souvent publié trop tard pour l'avant-course.
- **Rapports officiels** `dividendePourUnEuro` en centimes ; le 2 sur 4 paie un rapport fixe.

## Avertissements
- Aucun conseil financier. Les paris ne sont pas conseillés : le prélèvement du PMU (25 à 30 %) explique la perte moyenne d'un joueur sans avantage réel.
- Les analyses « après coup » (Vincennes et Caen du 14/11) ont été faites alors que l'arrivée était connue de Claude : ce ne sont pas des tests aveugles. Le test aveugle commence avec Vincennes du 16/11/2026.
