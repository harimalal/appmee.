-- Base D1 de Master IA. Appliquer avec : npm run master-ia:migrate (ou wrangler d1 execute master-ia --remote --file=master-ia/schema.sql)

CREATE TABLE IF NOT EXISTS resources (
  id              TEXT PRIMARY KEY,
  url             TEXT NOT NULL,
  canonical_url   TEXT NOT NULL UNIQUE,
  source          TEXT NOT NULL,                 -- youtube | udemy | coursera | openclassrooms | web
  title           TEXT NOT NULL,
  description     TEXT NOT NULL DEFAULT '',
  category        TEXT NOT NULL DEFAULT 'Autre',
  tags            TEXT NOT NULL DEFAULT '[]',    -- tableau JSON
  type            TEXT NOT NULL DEFAULT 'autre', -- video | playlist | cours | article | ...
  level           TEXT NOT NULL DEFAULT 'tous',  -- debutant | intermediaire | avance | tous
  language        TEXT NOT NULL DEFAULT 'autre', -- fr | en | autre
  author          TEXT NOT NULL DEFAULT '',
  duration_minutes INTEGER,
  thumbnail       TEXT NOT NULL DEFAULT '',
  score           INTEGER NOT NULL DEFAULT 0,    -- pertinence /10
  score_rationale TEXT NOT NULL DEFAULT '',
  confidence      TEXT NOT NULL DEFAULT 'faible',-- fiabilité de la note : haute | moyenne | faible
  status          TEXT NOT NULL DEFAULT 'a_voir',-- a_voir | en_cours | termine | abandonne
  notes           TEXT NOT NULL DEFAULT '',
  created_at      TEXT NOT NULL,
  updated_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_resources_score    ON resources (score DESC);
CREATE INDEX IF NOT EXISTS idx_resources_category ON resources (category);
CREATE INDEX IF NOT EXISTS idx_resources_status   ON resources (status);

CREATE TABLE IF NOT EXISTS settings (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
