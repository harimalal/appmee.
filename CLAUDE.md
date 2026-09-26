# Consignes pour Claude

## Cockpit Projets — le tenir à jour

Le tableau de bord de Hari est en ligne sur Cloudflare Pages, à l'adresse `/cockpit/` du site de ce dépôt.
Ses données sont dans la base D1 **`cockpit-db`** (id `18e5fbc0-71f2-46ea-9171-6070621d5709`).
Claude y écrit avec l'outil Cloudflare `d1_database_query` (une seule instruction SQL par appel quand on passe des `params`).
Hari ne tape presque rien : c'est à Claude de proposer et de tenir à jour les objectifs et les étapes.
Hari coche, archive, supprime, et écrit des idées depuis la page.

Projets affichés : `arteasy`, `reflexia`, `worthit`, `appmee`, `dropit`. Les autres (`yoitubesum`, `lyonjarrive`, `unclassified`)
ont `hidden = 1`.

**Tables**
- `projects (id, name, icon, color, description, repo, position, hidden, created_at, updated_at)`
- `axes (id, label, project_id, position)` — axes de travail. `project_id` NULL = axe commun à tous les projets
  (`strategie`, `produit`, `marketing`, `vente`). Pour un nouvel axe (ex. `recrutement`), insérer une ligne.
- `goals (project_id, horizon, objective, updated_at)` — une phrase par projet et par horizon (`court` | `moyen` | `long`).
- `steps (id, project_id, horizon, axis, title, detail, status, position, ref, source, created_at, updated_at, done_at)`
  - `status` : `todo` | `doing` | `done` | `archived` ; `done_at` = date ISO quand `done`, sinon `''`
  - `title` : une ligne courte. Le reste dans `detail`. `ref` : lien https direct ou `''`. `source` = `'claude'`.
  - id : `<projet>-<horizon>-<nn>`
- `deliverables (id, project_id, kind, title, url, note, created_at)` — `kind` : `artefact` | `article` | `doc`.
  `created_at` au format `AAAA-MM-JJ`. id = l'id de l'artefact, ou `art-<slug>` pour un article.
- `ideas (id, project_id, text, status, claude_note, created_at)` — écrites par Hari. `status` : `new` | `triaged`.
- `substeps (id, step_id, section, title, status, position)` — le plan pas-à-pas d'une étape, ouvert depuis le bouton
  « Plan » de la ligne. `status` : `todo` | `done`. `section` groupe les actions (ex. « Préparer », « Soumettre », « Suivre »).
  Quand Hari demande de détailler une étape, ou quand on scanne/analyse un dépôt pour en tirer un plan d'action,
  Claude écrit ce plan ici (plusieurs `INSERT INTO substeps` groupés par `section`), pas seulement dans `detail`.

**Quand agir, sans qu'on le demande**
- Au début d'une conversation sur un projet : lire `SELECT * FROM ideas WHERE status='new'`, transformer chaque idée en étapes
  (ou ajuster les objectifs), puis `UPDATE ideas SET status='triaged', claude_note='<une phrase>' WHERE id=…`.
- Un artefact, un article ou un document est publié → `INSERT INTO deliverables …`.
- Une étape est terminée pendant la session → `UPDATE steps SET status='done', done_at=…, updated_at=… WHERE id=…`.
- Hari demande « les prochaines choses à faire », un plan ou un nouvel axe → `INSERT OR REPLACE INTO goals …`, `INSERT INTO steps …`,
  `INSERT INTO axes …`.
Ne jamais supprimer sans que Hari le demande (passer en `archived` à la place).

```sql
INSERT INTO steps (id, project_id, horizon, axis, title, detail, status, position, ref, source, created_at, updated_at, done_at)
VALUES ('dropit-court-12', 'dropit', 'court', 'produit', 'Titre court', 'Détail', 'todo', 12, '', 'claude', ?1, ?1, '');
INSERT OR REPLACE INTO goals (project_id, horizon, objective, updated_at) VALUES ('dropit', 'moyen', 'Objectif en une phrase', ?1);
INSERT INTO deliverables (id, project_id, kind, title, url, note, created_at)
VALUES ('<id artefact>', 'reflexia', 'article', 'Titre', 'https://…', 'Résumé en une phrase', '2026-09-26');
```

L'ancien cockpit en artefact (https://claude.ai/artifact/9wYVLBBGwL521kfMMgAiVu) n'est plus mis à jour une fois le site en ligne.
