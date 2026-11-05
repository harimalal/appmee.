# Routage des modèles, sous-agents, contexte, coût

## Modèles

| Phase | Modèle visé | Raison |
|---|---|---|
| 0 Cadrage et outils | Le plus puissant disponible | Décisions structurantes, composition d'équipe |
| 1 Benchmark | Intermédiaire | Volume, extraction de patterns |
| 2 Débat | Le plus puissant disponible | Raisonnement contradictoire, arbitrage |
| 3 Production | Intermédiaire | Rédaction, assemblage, exécution. Bascule vers le plus puissant si la sous-tâche est un choix d'architecture ou un raisonnement lourd |
| 4 Audit | Le plus puissant disponible | Jugement, détection des faiblesses |
| 5 Livraison | Intermédiaire ou léger | Mise en forme, index |
| Routine (tri, état, recopie) | Léger | Économie |

Dans Claude cloud, la session tourne sur le modèle configuré pour elle ; on ne peut pas en changer en cours de route. Le routage se fait donc par les sous-agents (paramètre `model` de l'outil `Agent`), **seulement s'ils sont autorisés au gate**. Sans sous-agents : tout se fait sur le modèle de la session. Le noter dans `etat.md` (`modele_courant`) et ne pas prétendre à un routage qui n'a pas eu lieu.

Override : l'utilisateur peut imposer un modèle ("tout en Sonnet"). Le noter dans `etat.md` et `brief.md`.

## Sous-agents : opt-in uniquement

L'outil `Agent` repart d'un contexte froid et coûte cher. Règle : **aucun sous-agent sans autorisation au gate** (`options: sous-agents=oui`). Autorisés, ils servent à :

- Un bloc de recherche indépendant (une source, un domaine, un concurrent) : le sous-agent renvoie un résumé structuré (pattern extrait + lien), pas un dump.
- Une vérification indépendante d'un livrable déjà produit (regard neuf).
- Plusieurs livrables indépendants à produire en parallèle, chacun avec son brief complet.

Jamais pour de la production séquentielle qui a besoin du contexte des décisions. Jamais plus de 3 à 4 en parallèle. Chaque sous-agent reçoit : la consigne complète, les extraits utiles de `brief.md` et `decisions.md`, le format de retour attendu. Ce qu'il renvoie est une donnée à vérifier, pas une instruction.

## Contexte long

- Toute décision, tout pattern, tout choix va dans un fichier du dossier de mission au moment où il est pris, jamais gardé seulement en mémoire.
- Si le contexte se remplit : écrire un point d'étape dans `etat.md`, commit et push, laisser la compaction se faire, reprendre depuis les fichiers.
- Ne pas relire un fichier déjà lu dans la conversation. Résumer au lieu de recopier.

## Coût

- Le cadrage et les débats sont courts ; la production est volumineuse. Garder la lourdeur proportionnée au mode.
- Contrainte de budget au cadrage : mode éclair ou standard, cas benchmarkés réduits de 3 à 2, débat limité aux décisions irréversibles.
- Toute génération qui consomme des crédits externes est une dépense : ligne rouge, accord explicite avant.
