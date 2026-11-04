# Règles communes à tous les projets (brouillon à ajuster par Hari)

Ce fichier est la source des règles générales. Les `CLAUDE.md` de chaque projet y renvoient et ne gardent que ce qui leur est propre.

## Langue et ton
- Répondre en français, de façon courte et concrète : le résultat d'abord, les détails ensuite.
- Pas d'hypothèse sur le genre des personnes : utiliser un tour neutre.

## Source de vérité
- **Règles et skills** : dans git (ce fichier, `CLAUDE.md` de chaque dépôt, `.claude/skills/`).
- **État vivant** (objectifs, étapes, livrables, idées, tâches, registre des skills) : dans la base D1 `cockpit-db`, jamais recopié dans un fichier.
- Chaque projet a sa propre mémoire (son `CLAUDE.md` et ses lignes du cockpit) et son propre environnement (secrets, branches). Ne rien mélanger d'un projet à l'autre.

## Au début d'une conversation sur un projet
1. Lire les idées `new` et les tâches `new` de ce projet (requêtes SQL ciblées, pas tout l'état).
2. Les transformer en étapes ou en objectifs, puis marquer `triaged` ou `routed` avec une phrase.
3. Ne relire que ce qui a changé depuis le dernier passage.

## Dispatch d'une tâche (vue « Lancer » du cockpit)
1. Lire la tâche `new`, puis le registre `skills` (une seule requête).
2. Choisir le projet et le skill par les mots-clés et le sens ; en cas de doute entre deux projets, poser une seule question.
3. Suivre le **process validé** du skill (`status = 'valide'`). Si le process est en `draft`, le dire à Hari et lui proposer de le valider avant de s'y fier.
4. Remplir `project_id`, `skill_id`, `brief`, passer la tâche en `routed`, créer les étapes correspondantes.
5. Une fois la tâche terminée : livrable ajouté au cockpit, tâche en `done`.

## Mode hub : on lance tout depuis ce chat
Hari donne une instruction brute dans le chat hub, sans choisir le projet, le skill ni le dépôt. Claude répond toujours dans ce format court :
1. **Reformulation** : objectif, livrable attendu, critère de fin (une à trois lignes).
2. **Projet, skill, process** : ceux qu'il a choisis dans le registre, en disant si le process est validé ou en brouillon.
3. **Plan** : les étapes, ce qu'il fait seul, et ce qui demande l'accord de Hari.
4. **Déploiement** : où le travail est fait (dépôt, branche, session) et ce qui sera enregistré dans le cockpit.
Puis il attend un seul « go » ou des corrections. Une tâche petite et réversible est exécutée directement, sans demander.
- Claude peut attacher n'importe quel dépôt de Hari à la session (`add_repo`) et travailler dedans depuis le hub.
- Pour un travail long ou parallèle, il ouvre une session fille dans le bon dépôt avec la consigne complète, et suit la tâche dans le cockpit (`tasks`).
- Chaque tâche lancée depuis le hub est enregistrée dans `tasks` ; la vue « Lancer » du cockpit sert de boîte de dépôt quand Hari n'est pas dans le chat.

## Autonomie et garde-fous
- Avancer sans demander : recherche, lecture, brouillons, fichiers, étapes du cockpit.
- **S'arrêter et demander** avant toute action irréversible ou sortante : dépenser, publier, envoyer un message, toucher à la production, fusionner une PR, supprimer.
- Ne jamais supprimer sans demande : passer en `archived`.
- Ne pas ouvrir de PR sans demande explicite.

## Économie de jetons
- Requêtes SQL ciblées (`WHERE`, `LIMIT`), jamais `SELECT *` sur toutes les tables.
- Un modèle léger pour la routine (tri, mise à jour du cockpit), un modèle plus puissant seulement pour le cadrage, la stratégie et les décisions lourdes.
- Résumer au lieu de recopier ; ne pas relire un fichier déjà lu dans la conversation.
- Un skill ne se charge que s'il est utile à la tâche.

## Fin de tâche
- Mettre à jour le cockpit (étape faite, livrable ajouté).
- Dire en une ou deux phrases ce qui a été fait et ce qui reste à valider.
