# BRIEF — [[titre de la mission]]

mission: __SLUG__
date: __DATE__
mode: __MODE__
verdict: [[lancer | lancer sous condition | ne pas lancer]]
verrouillé: non

Tout champ entre doubles crochets doit être remplacé avant le verrouillage. Mode éclair : une ligne par section suffit.

## À retenir
[[5 à 8 lignes : objectif, livrables, décisions clés, ce qui sera fait seul, ce qui demandera un accord, conditions du verdict]]

## Objectif
[[une phrase : quoi livrer, pour qui, pour quoi faire]]

## Définition de « fini »
[[critères observables et mesurables : à quoi ressemble le résultat quand il est parfait et utilisable tel quel]]

## Livrables
| id | livrable | type | format et extension | langue | canal de livraison | grille d'audit |
|---|---|---|---|---|---|---|
| L01 | [[nom]] | [[type de formats.md]] | [[ex. .docx]] | [[français]] | [[fichier du dépôt | lien privé]] | [[grille de quality-gates.md ou ad hoc]] |

Grille ad hoc (si un livrable n'est couvert par aucune grille) : [[4 à 6 critères pondérés, somme 100, avec la vérification concrète du format ; sinon "sans objet"]]

## Périmètre
- Inclus : [[…]]
- Exclu : [[…]]

## Contraintes
- Budget : [[…]]
- Délai : [[…]]
- Ton ou voix : [[…]]
- Langue : [[…]]
- À ne surtout pas faire : [[…]]

## Décisions de fond
| décision | choix | pourquoi | écarté | réversible (coût) |
|---|---|---|---|---|
| [[…]] | [[…]] | [[…]] | [[…]] | [[oui ou non, coût]] |

## Doctrine d'arbitrage
Ordre de tranchage par défaut : contrainte dure du brief, puis fiable > évident > beau, puis l'option la plus réversible.
Règles propres à cette mission : [[…ou "aucune"]]

## Stories de vérification
Pour un produit, une fonctionnalité, un process : une story par comportement observable.
- Étant donné [[contexte]], quand [[action]], alors [[résultat observable]].
Sans objet pour ce type de livrable : [[oui | non]]

## Direction visuelle
Si le livrable a une identité visuelle : couleurs (hex), typographies, rayons, espacements, références. [[ou "sans objet"]]

## Actions exigeant un accord humain
Lignes rouges de la mission, en plus de `maestro/references/constitution.md` : [[ex. publication du site, envoi de la séquence, dépense de crédits de voix ; ou "aucune en plus"]]

## Options d'exécution
- sous-agents en parallèle : [[non | oui]]
- reprise automatique : [[non | oui]]
- modèle imposé : [[aucun | lequel]]

## Hypothèses, risques et plan B
- Hypothèse retenue : [[…]]
- Risque : [[…]] — parade : [[…]]

## Matériaux fournis
[[fichiers, liens, exemples, marque, données ; ou "aucun"]]

## Avenants
Journal des changements de périmètre après verrouillage (ajoutés par `lock-brief.sh --avenant`).
