# Grilles d'audit

Aucun livrable ne sort sous le seuil. Boucle de correction : 2 passes maximum, sinon blocage.

## Fonctionnement

1. Identifier le type du livrable (colonne "Type" de `formats.md`) et choisir sa grille ci-dessous.
2. Scorer chaque critère de 0 à 5. Score = somme des (note / 5 × poids), sur 100.
3. **Seuil : 80/100 ET aucun critère à 0 ou 1.**
4. Faire la **vérification mécanique** du format (section suivante) avant de scorer : un livrable qui n'ouvre pas, ne compile pas ou casse un test n'est pas scoré, il est corrigé.
5. Sous le seuil : corriger les critères faibles, re-scorer. 2e passe si besoin.
6. Toujours sous le seuil après 2 passes : `etat.md` en `BLOQUÉ`, remonter le critère précis qui coince.
7. Consigner dans `audit.md`, une ligne par livrable et par passe (format en bas).
8. Mode éclair : grille de base seulement, 1 passe. Mode complète : revue finale du panel (chaque rôle relit son domaine) en plus.

## Vérification mécanique par format

| Format | Vérifier |
|---|---|
| Texte, doc, rapport | Relecture complète, liens ouverts, chiffres recoupés avec `BENCHMARK.md`, noms propres exacts, longueur et langue du brief |
| Docx, pptx, xlsx, pdf | Ouvrir ou convertir le fichier avec le skill correspondant, rendre en image si possible, recalculer les formules, vérifier les débordements |
| Page web, artefact | Rendre avec Playwright (pré-installé) ou l'aperçu d'artefact, desktop et téléphone, clair et sombre, console sans erreur |
| Code, automatisation | Lancer lint et tests du dépôt, exécuter le cas nominal et un cas d'échec, relire le diff comme un relecteur hostile |
| Données, dataviz | Recompter à la main un échantillon, vérifier les axes, l'échelle et les sources |
| Vidéo, audio, visuel | Contrôler durée, format, cadrage, sous-titres ou voix, lisibilité, poids du fichier |
| Email, séquence, post | Relire à voix haute, vérifier liens, variables, objet, longueur ; envoi interdit (brouillon) |
| Autre | Une vérification concrète choisie au cadrage et notée dans `brief.md` |

Une vérification impossible dans l'environnement (outil absent, réseau fermé) est dite dans `audit.md`, jamais passée sous silence.

## Grille de base (tout type non couvert, et mode éclair)

| Critère | Poids |
|---|---|
| Répond exactement à l'objectif, la cible et la définition de "fini" du brief | 25 |
| Utilisable tel quel : zéro placeholder, format et extension finaux | 25 |
| Fondé : cas benchmarkés ou sources, pas des généralités | 20 |
| Exact et cohérent : chiffres, noms, liens, terminologie | 15 |
| Conforme aux contraintes : ton, langue, longueur, interdits | 15 |

## Grille : stratégie, plan d'action

| Critère | Poids |
|---|---|
| Chaque action est exécutable telle quelle (qui, quoi, quand, avec quel outil) | 25 |
| Fondé sur des cas benchmarkés, pas des généralités | 20 |
| Chiffrage réaliste (objectifs, délais, ressources), sourcé | 20 |
| Séquencement logique, dépendances explicites | 15 |
| Risques identifiés et plan B | 10 |
| Cohérent avec les contraintes du cadrage (budget, niche, ton) | 10 |

## Grille : contenu (article, page, script, séquence, post)

| Critère | Poids |
|---|---|
| Répond exactement à l'intention et à la cible du cadrage | 25 |
| Structure calquée sur un pattern benchmarké | 20 |
| Zéro placeholder, formats finaux, copier-coller-ready | 20 |
| Voix conforme aux règles de style du projet (anti-IA, test à voix haute) | 20 |
| Affirmations chiffrées sourcées (3 sources) | 15 |

## Grille : système, process, playbook

| Critère | Poids |
|---|---|
| Un tiers peut l'exécuter sans poser de question | 30 |
| Chaque étape a un critère de "fait" vérifiable | 20 |
| Outils et connecteurs nécessaires identifiés et disponibles | 20 |
| Cas d'échec et reprises documentés | 15 |
| Fondé sur des systèmes réels éprouvés | 15 |

## Grille : créatif, design, visuel, média

| Critère | Poids |
|---|---|
| Répond au brief et aux contraintes de marque | 25 |
| Fini : exportable et utilisable tel quel | 25 |
| Choix justifiés par des références réelles | 20 |
| Cohérence interne (grille, typo, palette, rythme) | 15 |
| Accessible (contraste, lisibilité, sous-titres) | 15 |

## Grille : produit, fonctionnalité, interface

| Critère | Poids |
|---|---|
| Chaque story Gherkin de `brief.md` est vérifiée telle quelle (étant donné, quand, alors observable) | 30 |
| Conforme à la doctrine d'arbitrage du brief (fiable > évident > beau) | 20 |
| Zéro placeholder, parcours au nombre de gestes annoncé | 20 |
| Direction visuelle conforme aux tokens du brief | 15 |
| Actions irréversibles protégées par confirmation explicite | 15 |

## Grille : code, automatisation, script

| Critère | Poids |
|---|---|
| Fait exactement ce que demandent les stories ou le brief (cas nominal vérifié) | 30 |
| Tests et lint du dépôt passent, cas d'échec couverts | 20 |
| Lisible et minimal : pas de code mort, pas de dépendance inutile, conventions du dépôt | 15 |
| Sûr : entrées validées, aucun secret en clair, aucune action destructrice sans garde-fou | 20 |
| Documenté pour l'exécuter et le reprendre (lancement, variables, limites) | 15 |

## Grille : données, analyse, tableur, tableau de bord

| Critère | Poids |
|---|---|
| Les chiffres sont justes (recomptage d'un échantillon, formules recalculées) | 30 |
| Répond à la question posée, conclusions en tête | 20 |
| Sources et méthode traçables | 20 |
| Lisibilité (axes, échelles, légendes, couleurs adaptées aux deux thèmes) | 15 |
| Limites et incertitudes dites | 15 |

## Grille : document formel (rapport, procédure, note, document de référence)

| Critère | Poids |
|---|---|
| Répond au destinataire et à l'usage prévu | 25 |
| Structure claire : on trouve chaque réponse en moins de 30 secondes | 20 |
| Exact, sourcé, daté | 20 |
| Actionnable : décisions, responsables, échéances | 20 |
| Mise en forme finale (titres, numérotation, tableaux, export testé) | 15 |

## Grille : présentation (deck, slides)

| Critère | Poids |
|---|---|
| Un message par slide, fil narratif clair de la première à la dernière | 25 |
| Preuves chiffrées et visuels lisibles | 20 |
| Fini : aucun texte hors cadre, polices et couleurs cohérentes | 20 |
| Adapté au public et à la durée | 20 |
| Notes de l'orateur ou appel à l'action présents si prévus | 15 |

## Livrable non couvert : grille ad hoc

Au cadrage, construire 4 à 6 critères pondérés (somme 100) qui disent ce qu'est un bon livrable de ce type, avec les références réelles qui les justifient. Les noter dans `brief.md` (section Livrables). Même seuil de 80/100, même règle du critère à 0-1.

## Format de audit.md

Une ligne par livrable et par passe. La colonne verdict vaut `OK` ou `A_CORRIGER` ; `check-mission.sh` lit la **dernière** ligne de chaque livrable.

```
| livrable | grille | passe | score | critère min | verdict | note |
|---|---|---|---|---|---|---|
| L01-plan.md | stratégie | 1 | 74 | 2 | A_CORRIGER | chiffrage non sourcé |
| L01-plan.md | stratégie | 2 | 88 | 3 | OK | |
```
