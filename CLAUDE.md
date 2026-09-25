# Consignes pour Claude

## Cockpit projets — le tenir à jour

Le cockpit (`/cockpit/`, Cloudflare Pages + D1) est le tableau de bord de tous les projets de Hari.
Ses données vivent dans la base D1 **`cockpit-db`** (id `6c0e61f0-271c-43bc-998e-d01e6e4485f0`).
Écris-y avec l'outil Cloudflare `d1_database_query` (une seule instruction SQL par appel si tu passes des `params`).

**Quand le faire, sans qu'on te le demande :**
- Un artefact, un article ou un document a été publié → ajoute un livrable (`kind='artifact'`).
- Une tâche est terminée → passe-la en `done` et journalise-la.
- Hari demande « les prochaines choses à faire », un plan d'action, ou lâche une idée → crée les tâches / idées
  dans la bonne thématique (crée la thématique si elle n'existe pas), avec les sous-tâches (`parent_id`).

Toujours `source='claude'`. Dates au format ISO UTC (`2026-09-25T20:00:00Z`). Identifiants : courts, uniques (ex. `ck-` + 10 caractères aléatoires).

```sql
-- Lire l'existant d'abord (projets, thématiques)
SELECT id, name FROM projects ORDER BY position;
SELECT id, project_id, title FROM themes WHERE project_id = 'arteasy' ORDER BY position;

-- Nouvelle thématique (le « grand pavé » dépliable)
INSERT INTO themes (id, project_id, title, position, created_at, updated_at)
VALUES ('th-xxxx', 'dropit', 'Onboarding', (SELECT COALESCE(MAX(position),0)+1 FROM themes WHERE project_id='dropit'), ?1, ?1);

-- Tâche (kind = task | idea), éventuellement sous-tâche via parent_id ; priority 1 haute, 2 moyenne, 3 basse
INSERT INTO items (id, project_id, theme_id, parent_id, kind, title, notes, status, priority, position, source, created_at, updated_at)
VALUES ('it-xxxx', 'dropit', 'th-xxxx', NULL, 'task', 'Titre', 'Contexte', 'todo', 2, 99, 'claude', ?1, ?1);

-- Livrable (artefact / article) + journal
INSERT INTO items (id, project_id, kind, title, notes, status, url, source, created_at, updated_at, done_at)
VALUES ('a-<id artefact>', 'reflexia', 'artifact', 'Titre', 'Résumé en une phrase', 'done', 'https://claude.ai/artifact/…', 'claude', ?1, ?1, ?1);
INSERT INTO activity (project_id, item_id, action, label, source, at) VALUES ('reflexia', 'a-<id>', 'artifact', 'Titre', 'claude', ?1);

-- Tâche terminée + journal
UPDATE items SET status='done', done_at=?1, updated_at=?1 WHERE id='it-xxxx';
INSERT INTO activity (project_id, item_id, action, label, source, at) VALUES ('dropit', 'it-xxxx', 'done', 'Titre', 'claude', ?1);
```

Valeurs : `status` ∈ todo | doing | blocked | done ; `activity.action` ∈ create | idea | start | done | reopen | artifact | delete.
Projet inconnu → `unclassified` (onglet « À classer »). Ne supprime jamais rien sans que Hari le demande.
