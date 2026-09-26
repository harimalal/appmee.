-- Cockpit Projets — base D1 "cockpit-db". Rejouable (IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS projects (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, icon TEXT DEFAULT '', color TEXT DEFAULT '#33587A',
  description TEXT DEFAULT '', repo TEXT DEFAULT '', position REAL DEFAULT 0, hidden INTEGER DEFAULT 0,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);

-- Axes de travail (produit, marketing, vente, stratégie… et tout nouvel axe). project_id NULL = axe commun.
CREATE TABLE IF NOT EXISTS axes (
  id TEXT PRIMARY KEY, label TEXT NOT NULL, project_id TEXT, position REAL DEFAULT 0
);

-- Un objectif par projet et par horizon (court | moyen | long).
CREATE TABLE IF NOT EXISTS goals (
  project_id TEXT NOT NULL, horizon TEXT NOT NULL, objective TEXT NOT NULL, updated_at TEXT NOT NULL,
  PRIMARY KEY (project_id, horizon)
);

-- Étapes. status : todo | doing | done | archived.
CREATE TABLE IF NOT EXISTS steps (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL, horizon TEXT NOT NULL, axis TEXT DEFAULT '',
  title TEXT NOT NULL, detail TEXT DEFAULT '', status TEXT NOT NULL DEFAULT 'todo', position REAL DEFAULT 0,
  ref TEXT DEFAULT '', source TEXT DEFAULT 'claude', created_at TEXT NOT NULL, updated_at TEXT NOT NULL, done_at TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_steps_project ON steps(project_id);

-- Livrables : artefacts, articles, documents. kind : artefact | article | doc.
CREATE TABLE IF NOT EXISTS deliverables (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL, kind TEXT DEFAULT 'artefact', title TEXT NOT NULL,
  url TEXT DEFAULT '', note TEXT DEFAULT '', created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_deliv_project ON deliverables(project_id);

-- Idées écrites par Hari. status : new | triaged.
CREATE TABLE IF NOT EXISTS ideas (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL, text TEXT NOT NULL, status TEXT DEFAULT 'new',
  claude_note TEXT DEFAULT '', created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
