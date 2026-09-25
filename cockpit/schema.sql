-- Cockpit — schéma de la base D1 "cockpit-db"
-- Rejouable sans risque (IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS projects (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  icon        TEXT DEFAULT '',
  color       TEXT DEFAULT '#6E6A61',
  description TEXT DEFAULT '',
  repo        TEXT DEFAULT '',
  position    REAL DEFAULT 0,
  archived    INTEGER DEFAULT 0,
  created_at  TEXT NOT NULL,
  updated_at  TEXT NOT NULL
);

-- Thématique = le "grand pavé" dépliable (ex. Onboarding, Import IA, Commercial…)
CREATE TABLE IF NOT EXISTS themes (
  id          TEXT PRIMARY KEY,
  project_id  TEXT NOT NULL,
  title       TEXT NOT NULL,
  description TEXT DEFAULT '',
  position    REAL DEFAULT 0,
  collapsed   INTEGER DEFAULT 0,
  created_at  TEXT NOT NULL,
  updated_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_themes_project ON themes(project_id);

-- Élément = tâche, idée ou livrable (artefact/article). parent_id => sous-tâche.
-- kind     : task | idea | artifact
-- status   : todo | doing | blocked | done
-- priority : 0 aucune | 1 haute | 2 moyenne | 3 basse
-- source   : moi | claude
CREATE TABLE IF NOT EXISTS items (
  id          TEXT PRIMARY KEY,
  project_id  TEXT NOT NULL,
  theme_id    TEXT,
  parent_id   TEXT,
  kind        TEXT NOT NULL DEFAULT 'task',
  title       TEXT NOT NULL,
  notes       TEXT DEFAULT '',
  status      TEXT NOT NULL DEFAULT 'todo',
  priority    INTEGER DEFAULT 0,
  position    REAL DEFAULT 0,
  url         TEXT DEFAULT '',
  source      TEXT DEFAULT 'moi',
  created_at  TEXT NOT NULL,
  updated_at  TEXT NOT NULL,
  done_at     TEXT
);
CREATE INDEX IF NOT EXISTS idx_items_project ON items(project_id);
CREATE INDEX IF NOT EXISTS idx_items_parent  ON items(parent_id);

-- Journal : tout ce qui a été créé, terminé, supprimé — l'historique.
CREATE TABLE IF NOT EXISTS activity (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id  TEXT,
  item_id     TEXT,
  action      TEXT NOT NULL,
  label       TEXT NOT NULL,
  source      TEXT DEFAULT 'moi',
  at          TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_activity_at ON activity(at);

CREATE TABLE IF NOT EXISTS settings (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
