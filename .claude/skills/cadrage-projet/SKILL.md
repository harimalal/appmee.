---
name: cadrage-projet
description: >-
  Cadrer un projet ou une mission avant de produire quoi que ce soit : reconnaissance, risques, dossier de choix argumenté, contradiction entre rôles, brief verrouillable (brief.md), équipe d'agents (equipe.md) et verdict lancer / lancer sous condition / ne pas lancer. C'est la Phase 0 du skill maestro. À utiliser avant toute mission large, ou quand l'utilisateur dit "cadre-moi ça", "avant de commencer", "fais-moi un brief", "est-ce que ça vaut le coup", "on part sur quoi ?".
---

# cadrage-projet — cadrer avant de produire

Transformer une demande brute (une dictée de trois lignes suffit) en un **brief verrouillable**, une **équipe de rôles** et un **verdict**, avec le moins de questions possible. Rien n'est produit ici : le cadrage décide, la production vient après.

Skill compagnon de `maestro` (qui l'invoque en phase 0). Utilisable seul : il s'arrête alors au gate et livre `brief.md`.

## Entrées et sorties

- **Entrée** : la demande de l'utilisateur, ses fichiers, le dossier de mission (`missions/AAAA-MM-JJ-<slug>/`). Si le dossier n'existe pas : `bash .claude/skills/maestro/scripts/new-mission.sh <slug> --mode <mode>` le crée avec tous les templates.
- **Sorties** (dans le dossier de mission) : `reconnaissance.md`, `dossier-de-choix.md`, `journal-decisions.md`, **`brief.md`**, `equipe.md`. Le brief est le seul document qui fait foi après verrouillage.
- **Langue** : français, court, résultat d'abord.

## Modes

| Mode | Phases | Gate |
|---|---|---|
| Éclair | A, F (brief en une ligne par section), G | Une phrase "go ?" ; aucune si la tâche est réversible |
| Standard | A à G, 1 à 4 décisions contradictoires | Un GO sur `brief.md` |
| Complète | A à G, 3 à 4 décisions contradictoires, revue d'équipe prévue | Un GO sur `brief.md` |

## Règle des questions

Poser **une seule série**, au plus 4 questions, et seulement celles dont la réponse change le plan et ne se déduit pas du contexte. Chaque question propose une réponse par défaut. Utiliser l'outil de question de la session ou le chat. Tout le reste devient une **hypothèse écrite** dans la section "Hypothèses, risques et plan B" du brief, que l'utilisateur corrige au gate s'il le veut. Ne jamais interroger au fil de l'eau après le gate.

## Les phases

### A — Réception
Reformuler : objectif en une phrase, destinataire, livrables et formats, "fini" mesurable, délai, contraintes, langue. Choisir le mode (avec `maestro` : triage). Lister ce qui manque.
Sortie : sections Objectif, Définition de « fini », Contraintes du brief. Fini quand l'objectif tient en une phrase sans "et aussi".

### B — Reconnaissance
Lire ce qui existe (dépôt, fichiers fournis, livrables précédents), cartographier les références du sujet, repérer ce qui se réutilise. Recherche web dès qu'un chiffre ou un standard compte. Une page maximum.
Sortie : `reconnaissance.md`. Fini quand on sait ce qu'on réutilise, ce qui contraint, ce qu'on ignore.

### C — Risques et hypothèses
Pré-mortem : "dans un mois, c'est un échec : pourquoi ?". Cinq risques maximum, chacun avec probabilité, impact, parade. Hypothèses explicites. Lignes rouges propres à la mission (dépense, publication, envoi, irréversible).
Sortie : sections "Hypothèses, risques et plan B" et "Actions exigeant un accord humain" du brief.

### D — Dossier de choix
Pour chaque option de fond (4 maximum) : au moins 2 cas réels décortiqués (mécanisme, chiffres, contre-intuitif), coût, risque, réversibilité, puis une **recommandation argumentée**. Méthode : `maestro/references/benchmark.md`.
Sortie : `dossier-de-choix.md`. Fini quand chaque option de fond a une recommandation et ce qui ferait changer d'avis.

### E — Contradiction
Sur les décisions structurantes seulement (celles qui engagent le périmètre, la promesse, le prix, la sécurité, la conformité ou l'irréversible). Protocole en deux tours : `references/contradiction.md`. Mode éclair : sautée.
Sortie : `journal-decisions.md` et tableau "Décisions de fond" du brief.

### F — Brief et équipe
Rédiger `brief.md` complet (template `templates/brief.md`) :
- **Livrables** : une ligne par livrable avec type et format (`maestro/references/formats.md`), langue, canal de livraison, grille d'audit (`maestro/references/quality-gates.md`) ; grille ad hoc pour un type non couvert.
- **Stories de vérification** (Gherkin) pour un produit, une fonctionnalité ou un process : étant donné, quand, alors observable.
- **Direction visuelle** (couleurs hex, typographies, rayons) si le livrable a une identité.
- **Doctrine d'arbitrage** : contrainte dure, puis fiable > évident > beau, puis le plus réversible ; règles propres si besoin.
- **Options d'exécution** : sous-agents (défaut non), reprise automatique (défaut non), modèle imposé (défaut aucun).
Composer `equipe.md` (template `templates/equipe.md`) : plafond 5 rôles actifs, un livrable nommé et un critère de succès par rôle, droit de veto, exigence portée, sortie de scène. Pour tout sujet, composer d'après les livrables, pas d'après un catalogue.
Fini quand `grep -F '[[' brief.md` ne trouve plus rien.

### G — Verdict et gate
Prononcer l'un des trois verdicts :
- **Lancer** : tout est tranché.
- **Lancer sous condition** : lister chaque condition (connecteur à ajouter, matériau à fournir, accord à obtenir). Les conditions remontent au gate et doivent être levées avant la phase 3.
- **Ne pas lancer** : donner les faits qui motivent (impossible, déjà fait, coût disproportionné, ligne rouge). Ce n'est pas un échec : c'est une sortie que le cadrage doit pouvoir produire.

Rédiger la section "À retenir" (5 à 8 lignes). Les points non tranchés de `dossier-de-choix.md` remontent au gate. Présenter le gate dans le format de `maestro` (reformulation, verdict, à retenir, plan, options d'exécution, chemin du brief) puis attendre un seul "go" ou des corrections. Le verrouillage (`maestro/scripts/lock-brief.sh`) se fait après le GO.

## Ce que le cadrage ne fait jamais

- Produire un livrable, même "pour montrer".
- Poser des questions en cascade ou après le gate.
- Laisser un champ `[[…]]` dans un brief proposé au gate.
- Recommander sans cas réel à l'appui sur une décision de fond.
- Cacher une réserve : un doute sérieux se transforme en condition ou en verdict "ne pas lancer".
- Composer plus de 5 rôles actifs.
