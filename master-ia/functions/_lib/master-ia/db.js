import { HttpError, requireDb } from './http.js';
import { DEFAULT_PROFILE, STATUSES, CATEGORIES, LEVELS } from './taxonomy.js';

export function rowToResource(r) {
  if (!r) return null;
  let tags = [];
  try { tags = JSON.parse(r.tags || '[]'); } catch { /* tags corrompus : liste vide */ }
  return { ...r, tags };
}

export async function getProfile(env) {
  const row = await requireDb(env).prepare('SELECT value FROM settings WHERE key = ?').bind('profile').first();
  return row?.value || DEFAULT_PROFILE;
}

export async function setProfile(env, value) {
  await requireDb(env)
    .prepare('INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value')
    .bind('profile', value)
    .run();
}

export async function findByCanonical(env, canonical) {
  return rowToResource(await requireDb(env).prepare('SELECT * FROM resources WHERE canonical_url = ?').bind(canonical).first());
}

export async function getResource(env, id) {
  const r = rowToResource(await requireDb(env).prepare('SELECT * FROM resources WHERE id = ?').bind(id).first());
  if (!r) throw new HttpError(404, 'Ressource introuvable');
  return r;
}

export async function insertResource(env, r) {
  const now = new Date().toISOString();
  const id = crypto.randomUUID();
  await requireDb(env)
    .prepare(
      `INSERT INTO resources (id, url, canonical_url, source, title, description, category, tags, type, level, language,
         author, duration_minutes, thumbnail, score, score_rationale, confidence, status, notes, created_at, updated_at)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
    )
    .bind(id, r.url, r.canonical_url, r.source, r.title, r.description, r.category, JSON.stringify(r.tags), r.type, r.level,
      r.language, r.author || '', r.duration_minutes ?? null, r.thumbnail || '', r.score, r.score_rationale, r.confidence,
      'a_voir', '', now, now)
    .run();
  return getResource(env, id);
}

const like = (s) => `%${s.replace(/[\\%_]/g, '\\$&')}%`;

export async function listResources(env, q) {
  const db = requireDb(env);
  const where = [];
  const args = [];
  const eq = (col, v) => { if (v) { where.push(`${col} = ?`); args.push(v); } };
  eq('category', q.category); eq('source', q.source); eq('status', q.status); eq('level', q.level); eq('language', q.language);
  if (q.tag) { where.push(`tags LIKE ? ESCAPE '\\'`); args.push(like(`"${q.tag.toLowerCase()}"`)); }
  if (q.min_score) { where.push('score >= ?'); args.push(Math.max(0, Math.min(10, +q.min_score || 0))); }
  if (q.q) {
    where.push(`(title LIKE ? ESCAPE '\\' OR description LIKE ? ESCAPE '\\' OR tags LIKE ? ESCAPE '\\' OR author LIKE ? ESCAPE '\\')`);
    args.push(...Array(4).fill(like(q.q)));
  }
  const order = { recent: 'created_at DESC', title: 'title COLLATE NOCASE ASC', score: 'score DESC, created_at DESC' }[q.sort] || 'score DESC, created_at DESC';
  const sql = `SELECT * FROM resources ${where.length ? 'WHERE ' + where.join(' AND ') : ''} ORDER BY ${order} LIMIT 500`;
  const { results } = await db.prepare(sql).bind(...args).all();

  const { results: stats } = await db
    .prepare(`SELECT category, source, status, score FROM resources`)
    .all();
  const count = (key) => stats.reduce((m, r) => ((m[r[key]] = (m[r[key]] || 0) + 1), m), {});
  return {
    resources: results.map(rowToResource),
    stats: {
      total: stats.length,
      avg_score: stats.length ? +(stats.reduce((a, r) => a + r.score, 0) / stats.length).toFixed(1) : 0,
      by_category: count('category'),
      by_source: count('source'),
      by_status: count('status'),
    },
  };
}

export async function updateResource(env, id, patch) {
  const current = await getResource(env, id);
  const next = { ...current };
  const str = (k, max) => { if (typeof patch[k] === 'string') next[k] = patch[k].slice(0, max); };
  str('title', 200); str('description', 800); str('notes', 5000); str('score_rationale', 600);
  if (CATEGORIES.includes(patch.category)) next.category = patch.category;
  if (LEVELS.includes(patch.level)) next.level = patch.level;
  if (STATUSES.includes(patch.status)) next.status = patch.status;
  if (Array.isArray(patch.tags)) next.tags = [...new Set(patch.tags.map((t) => String(t).toLowerCase().trim()).filter(Boolean))].slice(0, 12);
  if (Number.isFinite(+patch.score) && patch.score !== null && patch.score !== '') next.score = Math.max(0, Math.min(10, Math.round(+patch.score) || 0));
  if (!next.title) throw new HttpError(400, 'Le titre ne peut pas être vide');
  await requireDb(env)
    .prepare(`UPDATE resources SET title=?, description=?, category=?, tags=?, level=?, status=?, notes=?, score=?, score_rationale=?, updated_at=? WHERE id=?`)
    .bind(next.title, next.description, next.category, JSON.stringify(next.tags), next.level, next.status, next.notes, next.score, next.score_rationale, new Date().toISOString(), id)
    .run();
  return getResource(env, id);
}

export async function applyEnrichment(env, id, e, extra = {}) {
  await requireDb(env)
    .prepare(`UPDATE resources SET title=?, description=?, category=?, tags=?, type=?, level=?, language=?, duration_minutes=?, score=?, score_rationale=?, confidence=?, author=?, thumbnail=?, updated_at=? WHERE id=?`)
    .bind(e.title, e.description, e.category, JSON.stringify(e.tags), e.type, e.level, e.language, e.duration_minutes ?? null, e.score, e.score_rationale, e.confidence, extra.author || '', extra.thumbnail || '', new Date().toISOString(), id)
    .run();
  return getResource(env, id);
}

export async function deleteResource(env, id) {
  await requireDb(env).prepare('DELETE FROM resources WHERE id = ?').bind(id).run();
}
