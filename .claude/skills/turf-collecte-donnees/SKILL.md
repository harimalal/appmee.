---
name: turf-collecte-donnees
description: Collecter les données de courses de trot pour le projet Turf, sans abus : programme, cotes, arrivée et rapports officiels via l'API publique PMU, page course, carrière complète des chevaux et commentaires de fin de course via letrot.com au rythme lent d'une requête toutes les 3 secondes. À invoquer pour « récupère l'historique », « collecte Caen / Vincennes », « lis les commentaires », « prépare les données pour analyser la course », avant toute lecture cheval par cheval.
---

# Collecte des données du projet Turf

Workflows W1 et W2 de `turf/WORKFLOWS.md`. Les scripts sont dans `turf/scripts/`, les données dans un dossier local `courses/data/` qui **n'est jamais commité ni publié**.

## Règles
- **PMU** : API publique `online.turfinfo.api.pmu.fr/rest/client/7/programme/<JJMMAAAA>…`, une pause d'une seconde par requête, 5 requêtes en parallèle au maximum.
- **letrot.com** : usage privé, **une requête toutes les 3 secondes** (3,5 s pour les commentaires), 5 en parallèle au maximum, jamais de contournement de protection anti-robot (l'IFCE est protégée par Incapsula : ne pas l'utiliser).
- Si un domaine est bloqué par le réseau de la session (403 du proxy), lire la documentation de l'environnement (`read_documentation`, rubrique réseau) et demander l'autorisation à Hari ; ne pas contourner.
- Lancer les collectes longues en tâche de fond et attendre la fin avec une boucle `until grep -q FINI log`, jamais avec `sleep`.
- Ne pas faire tourner deux collectes letrot en même temps sur le même hôte au-delà de ce qu'impose la reprise d'une collecte déjà lancée.

## Commandes
| Besoin | Commande |
|---|---|
| Historique de courses avec rapports officiels | `collecte_historique.py <sortie.jsonl> <jour_début> <jour_fin>` |
| 5 dernières performances de chaque partant d'attelé | `collecte_perfs.py <dossier>` |
| Page course letrot et carrière complète des partants | `deep_fetch.py <dossier> <AAAA-MM-JJ> <code_letrot> <courses>` |
| Commentaires de fin de course des courses passées | `deep_comments.py <dossier> <AAAA-MM-JJ> <code_letrot> <courses>` |
| Pages course d'un échantillon (flags avant course) | `collecte_letrot_pages.py <dossier>` |

Codes letrot : 7500 Vincennes, 1400 Caen ; les autres sont dans la page du jour `https://www.letrot.com/courses/<AAAA-MM-JJ>` (`numHippodrome`).

## Estimation du temps
Une course de 14 partants : environ 20 pages de carrière (1 à 2 pages par cheval) et 50 à 70 pages de commentaires, soit 5 à 8 minutes. Une réunion de 9 courses : 30 à 40 minutes.

## Contrôles
- Les perfs d'une course passée sont celles d'**avant** cette course ; exclure toute entrée datée du jour (le script `dossier_cheval.py` le fait).
- Compter les chevaux sans carrière (débutants, étrangers) avant d'analyser.
- Les cotes des courses futures ne sont publiées que le matin ; les pronostics Geny le soir ou le matin : dire ce qui manque.
