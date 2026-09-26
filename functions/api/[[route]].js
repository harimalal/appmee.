// Cockpit Projets — API (Cloudflare Pages Functions + D1)
// Liaison requise dans le projet Pages : D1, nom de variable "DB" → base "cockpit-db".
// Toutes les routes exigent  Authorization: Bearer <jeton>  (settings.token_hash = SHA-256 du jeton).
//
// GET    /api/state                     → tout (projets, axes, objectifs, étapes, livrables, idées)
// POST   /api/{projects|axes|steps|deliverables|ideas}          crée
// PATCH  /api/{table}/{id}                                       modifie
// DELETE /api/{table}/{id}                                       supprime
// PUT    /api/goals/{projet}/{horizon}   { objective }           crée ou remplace l'objectif

const TABLES = {
  projects: ['name', 'icon', 'color', 'description', 'repo', 'position', 'hidden'],
  axes: ['label', 'project_id', 'position'],
  steps: ['project_id', 'horizon', 'axis', 'title', 'detail', 'status', 'position', 'ref', 'source'],
  deliverables: ['project_id', 'kind', 'title', 'url', 'note', 'created_at'],
  ideas: ['project_id', 'text', 'status', 'claude_note'],
  substeps: ['step_id', 'section', 'title', 'status', 'position'],
};
const STAMPED = new Set(['projects', 'steps']); // tables avec created_at / updated_at
const HORIZONS = ['court', 'moyen', 'long'];
const STATUSES = ['todo', 'doing', 'done', 'archived'];
const SUB_STATUSES = ['todo', 'done'];

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
const fail = (status, error) => json({ error }, status);
const now = () => new Date().toISOString();
const newId = () => crypto.randomUUID().replace(/-/g, '').slice(0, 16);

async function sha256(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function authorized(request, db) {
  const header = request.headers.get('authorization') || '';
  const token = header.startsWith('Bearer ') ? header.slice(7).trim() : '';
  if (!token) return false;
  const row = await db.prepare("SELECT value FROM settings WHERE key = 'token_hash'").first();
  if (!row) return false;
  const hash = await sha256(token);
  let diff = hash.length ^ row.value.length;
  for (let i = 0; i < hash.length; i++) diff |= hash.charCodeAt(i) ^ row.value.charCodeAt(i);
  return diff === 0;
}

function pick(table, body) {
  const out = {};
  for (const col of TABLES[table]) {
    if (body[col] === undefined) continue;
    let v = body[col];
    if (typeof v === 'string') v = v.slice(0, ['detail', 'note', 'text', 'description', 'claude_note'].includes(col) ? 20000 : 500);
    if (col === 'status' && table === 'steps' && !STATUSES.includes(v)) throw new Error('status invalide');
    if (col === 'status' && table === 'substeps' && !SUB_STATUSES.includes(v)) throw new Error('status invalide');
    if (col === 'horizon' && !HORIZONS.includes(v)) throw new Error('horizon invalide');
    if (['position', 'hidden'].includes(col)) v = Number(v) || 0;
    out[col] = v;
  }
  return out;
}

async function readState(db) {
  const [projects, axes, goals, steps, deliverables, ideas, substeps] = await db.batch([
    db.prepare('SELECT * FROM projects ORDER BY position, name'),
    db.prepare('SELECT * FROM axes ORDER BY position, label'),
    db.prepare('SELECT * FROM goals'),
    db.prepare('SELECT * FROM steps ORDER BY position, created_at'),
    db.prepare('SELECT * FROM deliverables ORDER BY created_at DESC'),
    db.prepare('SELECT * FROM ideas ORDER BY created_at DESC'),
    db.prepare('SELECT * FROM substeps ORDER BY step_id, position'),
  ]);
  return {
    projects: projects.results, axes: axes.results, goals: goals.results, steps: steps.results,
    deliverables: deliverables.results, ideas: ideas.results, substeps: substeps.results, at: now(),
  };
}

async function create(db, table, body) {
  const data = pick(table, body);
  const id = typeof body.id === 'string' && /^[\w-]{1,64}$/.test(body.id) ? body.id : newId();
  const ts = now();
  const row = { id, ...data };
  if (STAMPED.has(table)) { row.created_at = ts; row.updated_at = ts; }
  if (table === 'ideas') { row.created_at = ts; row.status = row.status || 'new'; }
  if (table === 'deliverables' && !row.created_at) row.created_at = ts.slice(0, 10);
  if (table === 'steps' && row.status === 'done') row.done_at = ts;
  const cols = Object.keys(row);
  await db.prepare(`INSERT INTO ${table} (${cols.join(',')}) VALUES (${cols.map(() => '?').join(',')})`)
    .bind(...cols.map(c => row[c])).run();
  return json(await db.prepare(`SELECT * FROM ${table} WHERE id = ?`).bind(id).first(), 201);
}

async function update(db, table, id, body) {
  const before = await db.prepare(`SELECT * FROM ${table} WHERE id = ?`).bind(id).first();
  if (!before) return fail(404, 'introuvable');
  const data = pick(table, body);
  if (!Object.keys(data).length) return json(before);
  if (STAMPED.has(table)) data.updated_at = now();
  if (table === 'steps' && data.status && data.status !== before.status) data.done_at = data.status === 'done' ? now() : '';
  const cols = Object.keys(data);
  await db.prepare(`UPDATE ${table} SET ${cols.map(c => `${c} = ?`).join(', ')} WHERE id = ?`)
    .bind(...cols.map(c => data[c]), id).run();
  return json(await db.prepare(`SELECT * FROM ${table} WHERE id = ?`).bind(id).first());
}

export async function onRequest({ request, env, params }) {
  const db = env.DB;
  if (!db) return fail(503, 'Liaison D1 « DB » absente : Pages → Settings → Bindings → D1 → DB = cockpit-db, puis redéployer.');
  try {
    if (!(await authorized(request, db))) return fail(401, 'Jeton invalide');
    const [resource, id, extra] = (params.route || []).filter(Boolean);
    const method = request.method;
    const body = ['POST', 'PATCH', 'PUT'].includes(method) ? await request.json().catch(() => ({})) : {};

    if (resource === 'state' && method === 'GET') return json(await readState(db));

    if (resource === 'goals' && method === 'PUT' && id && HORIZONS.includes(extra)) {
      const objective = String(body.objective || '').slice(0, 500);
      if (!objective) return fail(400, 'objective requis');
      await db.prepare('INSERT OR REPLACE INTO goals (project_id, horizon, objective, updated_at) VALUES (?, ?, ?, ?)')
        .bind(id, extra, objective, now()).run();
      return json({ ok: true });
    }

    if (!TABLES[resource]) return fail(404, 'route inconnue');
    if (method === 'POST' && !id) return create(db, resource, body);
    if (method === 'PATCH' && id) return update(db, resource, id, body);
    if (method === 'DELETE' && id) {
      await db.prepare(`DELETE FROM ${resource} WHERE id = ?`).bind(id).run();
      return json({ ok: true });
    }
    return fail(405, 'méthode non prise en charge');
  } catch (err) {
    return fail(400, err.message || 'erreur');
  }
}
