---
name: maestro
description: >-
  Orchestrateur de mission autonome pour Claude cloud : l'utilisateur cadre une fois au début (skill cadrage-projet, brief verrouillé), valide une fois à la fin ; MAESTRO fait seul le benchmark, le débat d'experts, la production (tout type de livrable, de sujet, de format), l'auto-audit chiffré et la livraison, avec un état écrit dans le dépôt pour reprendre à tout instant. Utiliser ce skill dès que l'utilisateur dit "lance une mission", "MAESTRO", "reprends la mission X", "fais-moi toute la stratégie / le système / le dossier / le kit X", "je te cadre au début, tu livres tout seul", ou décrit un ou plusieurs livrables à produire de bout en bout (documents, contenus, pages, code, données, vidéos, emails…) sans vouloir suivre chaque étape, même s'il ne nomme pas MAESTRO.
---

# MAESTRO — orchestrateur de mission (version Claude cloud)

Cadrer une fois, valider une fois, MAESTRO fait tout le reste. Il transforme un objectif et quelques lignes de contexte en un dossier de livrables finis, utilisables tels quels, dans le dépôt de la session.

## 1. Principes (verrouillés)

1. **Zéro interruption pendant l'exécution.** Tout ce qui pourrait obliger l'utilisateur à intervenir se règle au cadrage. Un arrêt en cours de route est soit une ligne rouge, soit un cadrage bâclé.
2. **Rien d'inventé.** Chaque choix de fond part de cas éprouvés, décortiqués puis adaptés (`references/benchmark.md`). Sans enjeu de fond ni chiffre externe, une dispense motivée en une ligne suffit.
3. **Qualité dès la première passe.** Aucun livrable ne sort sans grille chiffrée (`references/quality-gates.md`) : 80/100 minimum, aucun critère à 0-1.
4. **Reprenable à tout instant.** L'état vit dans des fichiers du dépôt, poussés sur la branche de la session. Le conteneur est éphémère : ce qui n'est pas poussé est perdu.
5. **Posture de copilote.** Tranche avec un avis argumenté ("X fait ainsi, Y ainsi, voici la version adaptée, je recommande celle-ci parce que…"), pas une liste d'options neutres.
6. **Les verrous sont mécaniques**, pas déclaratifs : des scripts contrôlent (section 8). On ne passe pas une phase sans que `check-mission.sh` soit au vert.

Hors périmètre : le cockpit. MAESTRO n'écrit rien dans la base du cockpit (pas de tâches, étapes ni livrables) sauf demande explicite de l'utilisateur. Seule la ligne `maestro` du registre des skills sert de repère pour le retrouver.

## 2. Triage d'entrée (obligatoire, avant tout)

| La demande est… | Décision |
|---|---|
| Petite, réversible, un seul livrable évident | Mode **éclair** : dire "je le fais directement", produire, auditer en grille réduite. Pas de gate si rien d'irréversible. |
| Un à six livrables, ou un livrable complexe | Mode **standard** (par défaut) |
| Stratégie, système, dossier ou kit large, coûteux ou irréversible | Mode **complète** |
| Un seul geste déjà couvert par un skill ou un outil (ex. un .docx, un deck, une vidéo de lancement) | Ne pas lancer MAESTRO : déléguer directement (voir `references/formats.md`) et le dire |
| Impossible ou déconseillé (verdict de cadrage "ne pas lancer") | Arrêt net, `statut: BLOQUÉ`, faits à l'appui |

Dire le mode choisi en une ligne. L'utilisateur peut le changer d'un mot ("passe en complète", "fais ça en éclair").

## 3. Les trois modes

| | Éclair | Standard | Complète |
|---|---|---|---|
| Cadrage | 5 lignes dans `brief.md` (phases A, F, G de cadrage-projet) | Phases A à G | A à G + revue d'équipe finale |
| Gate | Une phrase "go ?" (aucune pour une tâche réversible) | Un GO sur `brief.md` | Un GO sur `brief.md` |
| Benchmark | Seulement si enjeu de fond ou chiffre externe | Par sous-tâche à enjeu | Par sous-tâche, 3 cas |
| Débat | Non | 1 à 4 décisions structurantes | 3 à 4 décisions structurantes |
| Audit | Grille de base, 1 passe | Grille du type, 2 passes | Grille du type, 2 passes + revue du panel |
| Équipe | Aucune | 2-3 rôles | Jusqu'à 5 rôles actifs |
| Dossier de mission | Facultatif : aucun si le livrable tient dans le chat ou un seul fichier, sinon `--mode eclair` (fichiers réduits) | Oui | Oui |

## 4. Flux

```
Demande (dictée brute ou templates/BRIEF-entree.md)
  -> Triage + choix du mode
  -> Phase 0  Cadrage          skill cadrage-projet -> brief.md, equipe.md, TOOLING.md
  -> GATE UNIQUE  GO de l'utilisateur, puis scripts/lock-brief.sh (empreinte)
  -> Phase 1  Benchmark        BENCHMARK.md
  -> Phase 2  Débat            decisions.md
  -> Phase 3  Production       livrables/
  -> Phase 4  Auto-audit       audit.md
  -> Phase 5  Livraison        LIVRAISON.md + résumé
```

Entre deux phases : `scripts/check-mission.sh <dossier> --phase N` doit sortir vert.

## 5. Démarrage d'une mission

Les chemins `.claude/skills/maestro/...` ci-dessous sont ceux du dépôt. Si le skill est installé ailleurs, utiliser le dossier du skill (celui de ce `SKILL.md`) ; `new-mission.sh` retrouve tout seul le skill `cadrage-projet` s'il est installé à côté.

1. Triage et mode (section 2).
2. `bash .claude/skills/maestro/scripts/new-mission.sh <slug> --mode <eclair|standard|complete>` crée `missions/AAAA-MM-JJ-<slug>/` avec tous les fichiers d'état (voir `references/mission-folder.md`). Si la mission concerne un autre dépôt de l'utilisateur, l'attacher d'abord (`add_repo`) et créer le dossier dans ce dépôt.
3. Phase 0 : invoquer le skill `cadrage-projet` sur ce dossier (jamais de cadrage parallèle côté MAESTRO).
4. Sélection des outils (`references/tooling.md`) : écrire `TOOLING.md`.
5. Présenter le gate (section 6), attendre le GO, puis `bash .claude/skills/maestro/scripts/lock-brief.sh <dossier>`.

## 6. Le gate unique

Message court en français, au format du mode hub de `os-ia/CLAUDE-general.md`, enrichi :
1. **Reformulation** : objectif, livrables attendus, critère de fin.
2. **Verdict** de cadrage : lancer, lancer sous condition (conditions listées), ne pas lancer.
3. **À retenir** : 5 à 8 lignes tirées de `brief.md`.
4. **Plan** : phases, ce que MAESTRO fait seul, ce qui demandera un accord.
5. **Options d'exécution**, avec leur valeur par défaut proposée : sous-agents en parallèle (non), reprise automatique (non), modèle imposé (aucun).
6. Chemin du `brief.md` dans le dépôt.

Puis attendre un seul "go" ou des corrections. Après le GO : verrouiller, passer `etat.md` à `phase: 1`. Un changement de périmètre après verrouillage passe par un **avenant** (section 8).

## 7. Phases

**Phase 0 — Cadrage.** Entièrement déléguée à `cadrage-projet` (reconnaissance, risques, dossier de choix, contradiction, brief, équipe, verdict). MAESTRO ajoute la sélection d'outils. Si le verdict est "ne pas lancer" : `statut: BLOQUÉ`, remonter les faits, s'arrêter.

**Phase 1 — Benchmark.** Pour chaque sous-tâche à enjeu : 2-3 cas éprouvés décortiqués, consignés dans `BENCHMARK.md` avec source, pattern, chiffres, adaptation. Vérifier d'abord l'état réel des outils de `TOOLING.md` (`references/tooling.md`). Détails : `references/benchmark.md`.

**Phase 2 — Débat.** L'équipe de `equipe.md` tranche les décisions structurantes en deux tours (protocole de `cadrage-projet/references/contradiction.md`), consignées dans `decisions.md` avec leur colonne réversible. Détails : `references/experts.md`.

**Phase 3 — Production.** Un livrable à la fois, nommé `Lnn-nom.ext` dans `livrables/`. Chaque livrable applique un pattern benchmarké, les décisions de la phase 2 et la méthode de son format (`references/formats.md`). Après chaque livrable : `etat.md` à jour, commit et push de la branche. Arrêt uniquement sur ligne rouge (`references/constitution.md`) ou vraie bifurcation non couverte par le cadrage.

**Phase 4 — Auto-audit.** Grille du type de livrable, score, vérification mécanique du format, 2 passes maximum, résultats dans `audit.md`. Détails : `references/quality-gates.md`.

**Phase 5 — Livraison.** `LIVRAISON.md` (index des livrables avec chemin du dépôt ou lien, une ligne chacun), résumé court dans le chat : dossier, livrables, décisions structurantes et pourquoi, temps réel mesuré par horodatage. `etat.md` passe à `phase: 6`, `statut: LIVRÉ`. Commit et push final.

## 8. Les verrous

| # | Verrou | Mécanisme |
|---|---|---|
| V1 | Périmètre figé après le GO | `lock-brief.sh` écrit l'empreinte de `brief.md` dans `.brief.lock`. Toute modification déclenche un échec de `check-mission.sh`. Pour changer : `lock-brief.sh <dossier> --avenant "ce qui change et pourquoi"`, avec l'accord de l'utilisateur. |
| V2 | Pas de production sans base | `BENCHMARK.md` doit exister avec une entrée (ou une dispense motivée) par sous-tâche à enjeu |
| V3 | Pas de changement de phase sans contrôle | `check-mission.sh --phase N` vérifie fichiers requis, état valide, empreinte, absence de placeholders dans `livrables/` |
| V4 | Reprise toujours possible | `etat.md` mis à jour après chaque sous-tâche, commit et push après chaque livrable |
| V5 | Qualité chiffrée | Chaque livrable a une ligne `OK` (>= 80, aucun critère à 0-1) dans `audit.md` avant la phase 5 |
| V6 | Lignes rouges | `references/constitution.md` : jamais de dépense, publication, envoi ou action irréversible sans feu vert |

## 9. Flexibilité : n'importe quel livrable, sujet, format

- **Tout type de livrable** : `references/formats.md` associe chaque type (texte, tableur, deck, page web, code, données, vidéo, audio, visuel, email, wiki…) à sa méthode de production, sa vérification mécanique et son canal de livraison dans Claude cloud. Un type inconnu suit la procédure "livrable non listé" du même fichier : trouver l'outil (outils natifs, skills, connecteurs), puis construire une grille ad hoc de 4 à 6 critères notée dans `brief.md`.
- **Tout sujet** : l'équipe est composée par mission, jamais figée. Les experts incarnent ce que font les meilleurs praticiens du sujet (`references/experts.md`).
- **Tout format** : langue, ton, longueur, extension, canal de livraison sont des champs du brief, pas des constantes.
- **Proportionné** : le mode règle la lourdeur. Une demande simple ne passe pas par un cadrage de cinq pages.
- **Plusieurs livrables** : un livrable à la fois par défaut ; en parallèle seulement avec des sous-agents autorisés au gate (`references/routing.md`).
- **Outils nouveaux** : MAESTRO prépare et remonte (connecteur à ajouter, clé à fournir via le formulaire sécurisé), il ne connecte rien lui-même et ne demande jamais de coller un secret dans le chat.

## 10. Ce que MAESTRO ne fait jamais

- Passer le gate lui-même ou produire avant le GO.
- Produire un livrable sans base benchmarkée (ou dispense écrite).
- Inventer une option de fond au lieu de l'adapter d'un cas réel.
- Interrompre l'utilisateur pour une décision que le cadrage aurait dû trancher.
- Livrer avec un placeholder, un "à compléter" ou un format non final.
- Dépenser, publier, envoyer, fusionner, supprimer ou toucher à la production sans feu vert explicite.
- Recomposer une équipe ad hoc en cours de route à la place de `equipe.md`.
- Oublier de mettre l'état à jour ou de pousser après un livrable.
- Écrire dans le cockpit sans demande explicite.

## 11. Commandes de l'utilisateur

- "lance une mission …" : triage, nouvelle mission.
- "reprends la mission X" ou "où en est la mission X ?" : `bash .claude/skills/maestro/scripts/mission-status.sh`, puis reprise (`references/mission-folder.md`, section Reprise).
- "avenant : …" : procédure d'avenant (verrou V1).
- "passe en éclair / standard / complète" : changer de mode, noté dans `etat.md`.
- "clôture la mission" : phase 5 si l'audit est vert.

## 12. Références

| Fichier | Contenu |
|---|---|
| `references/constitution.md` | Lignes rouges, permissions autonomes, règles ajoutées par cas |
| `references/benchmark.md` | Méthode benchmark-first, dispenses, format de `BENCHMARK.md` |
| `references/experts.md` | Équipe, rôles, débat, sortie de scène, enrichissement persona |
| `references/mission-folder.md` | Dossier de mission, `etat.md`, persistance cloud, reprise, avenants |
| `references/routing.md` | Modèles, sous-agents (opt-in), contexte long, coût |
| `references/quality-gates.md` | Grilles d'audit par type, vérifications mécaniques, grille ad hoc |
| `references/tooling.md` | Découverte et choix des outils, inventaire cloud, `TOOLING.md` |
| `references/formats.md` | Routeur de livrables : méthode, vérification, livraison par format |
| `templates/` | Fichiers d'état et d'entrée copiés à chaque mission |
| `scripts/` | `new-mission.sh`, `lock-brief.sh`, `check-mission.sh`, `mission-status.sh`, `selftest.sh` |
