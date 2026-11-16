# Dossier de mission, état, persistance cloud, reprise

## Emplacement

`missions/AAAA-MM-JJ-<slug>/` à la racine du dépôt de la session. `<slug>` : 2 à 4 mots en kebab-case tirés de l'objectif.

- Mission pour un autre dépôt de l'utilisateur : l'attacher avec `add_repo`, créer le dossier dans ce dépôt (le contexte et la cohérence vivent avec le projet).
- Mission sans dépôt naturel : le dépôt de la session.
- Tout ce que l'utilisateur doit pouvoir ouvrir reste dans le dépôt de la session (l'application ne peut ouvrir que ces fichiers).

`new-mission.sh` crée le dossier et copie les templates.

## Structure

```
missions/AAAA-MM-JJ-<slug>/
├── reconnaissance.md      cadrage-projet : état des lieux
├── dossier-de-choix.md    cadrage-projet : options de fond et recommandation
├── brief.md               cadrage-projet : LE gate, fait foi une fois verrouillé
├── equipe.md              cadrage-projet : fiches des rôles
├── journal-decisions.md   cadrage-projet : contradictions closes
├── TOOLING.md             MAESTRO : tâche -> outil, connecteurs à ajouter
├── plan.md                phases et sous-tâches avec statut
├── etat.md                état courant (fichier de reprise)
├── decisions.md           fiches rôles et décisions des phases 2 à 4
├── BENCHMARK.md           sources et patterns, ou dispenses
├── audit.md               scores par livrable et par passe
├── livrables/             Lnn-nom.ext, copier-coller-ready
├── LIVRAISON.md           index final
└── .brief.lock            empreinte de brief.md (créée par lock-brief.sh)
```

## etat.md : le fichier de reprise

Une session fraîche lit ce fichier en premier. Il doit toujours refléter la réalité.

```
mission: <slug>
dossier: <chemin relatif au dépôt>
mode: eclair | standard | complete
phase: 0..6
statut: EN_COURS | BLOQUÉ | LIVRÉ
derniere_sous_tache_finie: <id + titre>
prochaine_sous_tache: <id + titre>
modele_courant: <modèle de la session ou du sous-agent>
branche: <branche de travail poussée>
options: sous-agents=non reprise_auto=non
blocage: <si BLOQUÉ : question précise + option recommandée>
maj: <horodatage ISO>

# Journal (append-only, une ligne par événement)
# <horodatage> — <ce qui vient d'être fait ou décidé>
```

Phases : 0 cadrage, 1 benchmark, 2 débat, 3 production, 4 audit, 5 livraison, 6 livré.

Mettre à jour après chaque sous-tâche, sans exception. Le journal sert aussi à mesurer le temps réel de la mission : jamais d'estimation vague en fin de mission, seulement des horodatages.

## Persistance dans le conteneur éphémère

Le conteneur est réclamé après inactivité. Donc :

1. Après chaque livrable, à la fin de chaque phase, et avant tout arrêt (blocage, attente du GO) : `git add missions/... && git commit` puis `git push -u origin <branche de travail>`.
2. Message de commit court : `Mission <slug> : <ce qui est fait>`.
3. Pas de pull request sans demande explicite. Pas de push sur une autre branche.
4. En cas d'échec réseau, réessayer 4 fois avec attente croissante (2 s, 4 s, 8 s, 16 s), puis écrire le blocage dans `etat.md`.

## Reprise d'une mission

Déclencheurs : "reprends la mission X", "où en est X ?", nouvelle session sur la branche, ou rappel programmé.

1. `bash .claude/skills/maestro/scripts/mission-status.sh` liste les missions, leur phase, leur statut et leur ancienneté.
2. Lire `etat.md`, puis `plan.md`, `decisions.md`, `brief.md` (et `equipe.md`, `TOOLING.md` selon la phase).
3. Lancer `check-mission.sh <dossier> --phase <phase courante>` pour vérifier l'intégrité (empreinte du brief, fichiers requis).
4. Si `statut: BLOQUÉ` : présenter le blocage à l'utilisateur, ne rien faire d'autre.
5. Sinon : reprendre à `prochaine_sous_tache`, sans recadrer.
6. Si `phase: 0` et que `brief.md` n'est pas verrouillé : le cadrage n'est pas fini, reprendre à la phase d'arrêt de `cadrage-projet`.

## Reprise automatique (optionnelle, autorisée au gate)

Le conteneur ne conserve rien entre deux sessions : une reprise automatique doit démarrer une **nouvelle session** sur la branche.

- Si l'utilisateur l'a autorisée au gate (`options: reprise_auto=oui`) : programmer une tâche planifiée à usage unique (outil `create_trigger`, session neuve dans le même environnement) avec la consigne complète : "Reprends la mission MAESTRO dans `missions/<dossier>` sur la branche `<branche>` : lis etat.md, plan.md, decisions.md, brief.md, vérifie avec check-mission.sh, reprends à prochaine_sous_tache sans recadrer, respecte la constitution." Re-programmer à chaque arrêt non terminal.
- Pour un simple rappel dans la session en cours : `send_later`.
- Sinon : aucune reprise automatique. L'utilisateur relance en disant "reprends la mission X".
- Ne jamais démarrer une mission en automatique : seulement reprendre une mission dont le brief est verrouillé et dont `statut` est `EN_COURS` avec `phase >= 1`.
- Une tâche planifiée qui trouve `BLOQUÉ` n'agit pas et se désactive.

## Mots légitimes dans les livrables

`check-mission.sh` refuse les placeholders (TODO, « à compléter », lorem ipsum, `[[…]]`, `{{…}}`). Si un livrable traite légitimement d'un de ces mots (un guide sur les « TODO », par exemple), écrire ce mot, un par ligne, dans `<dossier>/.placeholder-allow` : les lignes qui le contiennent sont alors ignorées. Ne pas s'en servir pour cacher un vrai manque.

## Avenants (changement de périmètre après le GO)

1. Dire à l'utilisateur ce qui change, son coût (temps, livrables touchés) et ce qui est écarté. Attendre son accord.
2. `bash .claude/skills/maestro/scripts/lock-brief.sh <dossier> --avenant "ce qui change et pourquoi"` : ajoute la ligne datée dans la section Avenants et recalcule l'empreinte.
3. Reporter l'impact dans `plan.md` et `decisions.md`.

Une demande de retouche de livrable qui reste dans le périmètre n'est pas un avenant.

## Nommage des livrables

`livrables/L01-nom-court.ext`, `L02-…` dans l'ordre du plan. Un livrable composé de plusieurs fichiers (site, projet de code) prend un sous-dossier `L03-nom/` ; `check-mission.sh` en contrôle le contenu. `LIVRAISON.md` liste chaque livrable.
