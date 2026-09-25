// Cockpit — API (Cloudflare Pages Functions + D1)
// Liaison requise dans le projet Pages : D1 database, nom de variable "DB" → cockpit-db.
// Toutes les routes exigent l'en-tête  Authorization: Bearer <jeton>.
// Le jeton n'est jamais stocké en clair : settings.token_hash = SHA-256(jeton).

const TABLES = {
  projects: ['name', 'icon', 'color', 'description', 'repo', 'position', 'archived'],
  themes:   ['project_id', 'title', 'description', 'position', 'collapsed'],
  items:    ['project_id', 'theme_id', 'parent_id', 'kind', 'title', 'notes', 'status', 'priority', 'position', 'url', 'source'],
};
const KINDS = ['task', 'idea', 'artifact'];
const STATUSES = ['todo', 'doing', 'blocked', 'done'];

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
const fail = (status, message) => json({ error: message }, status);
const now = () => new Date().toISOString();
const newId = () => crypto.randomUUID().replace(/-/g, '').slice(0, 16);

async function sha256(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function authorized(request, db) {
  const header = request.headers.get('authorization') || '';
  const token = header.startsWith('Bearer ') ? header.slice(7).trim() : '';
  if (!token) return false;
  const row = await db.prepare("SELECT value FROM settings WHERE key = 'token_hash'").first();
  if (!row) return false;
  return timingSafeEqual(await sha256(token), row.value);
}

// Ne garde que les colonnes autorisées, et valide les valeurs sensibles.
function pick(table, body) {
  const out = {};
  for (const col of TABLES[table]) {
    if (body[col] === undefined) continue;
    let v = body[col];
    if (typeof v === 'string') v = v.slice(0, col === 'notes' || col === 'description' ? 20000 : 500);
    if (col === 'kind' && !KINDS.includes(v)) throw new Error('kind invalide');
    if (col === 'status' && !STATUSES.includes(v)) throw new Error('status invalide');
    if (['position', 'priority', 'archived', 'collapsed'].includes(col)) v = Number(v) || 0;
    if (v === '' && ['theme_id', 'parent_id'].includes(col)) v = null;
    out[col] = v;
  }
  return out;
}

function log(db, { project_id, item_id = null, action, label, source = 'moi' }) {
  return db
    .prepare('INSERT INTO activity (project_id, item_id, action, label, source, at) VALUES (?, ?, ?, ?, ?, ?)')
    .bind(project_id || null, item_id, action, String(label || '').slice(0, 300), source, now());
}

async function readState(db) {
  const [projects, themes, items, activity] = await db.batch([
    db.prepare('SELECT * FROM projects ORDER BY position, name'),
    db.prepare('SELECT * FROM themes ORDER BY position, created_at'),
    db.prepare('SELECT * FROM items ORDER BY position, created_at'),
    db.prepare('SELECT * FROM activity ORDER BY at DESC, id DESC LIMIT 400'),
  ]);
  return {
    projects: projects.results,
    themes: themes.results,
    items: items.results,
    activity: activity.results,
    at: now(),
  };
}

async function create(db, table, body) {
  const data = pick(table, body);
  if (table === 'projects' && !data.name) return fail(400, 'name requis');
  if (table === 'themes' && (!data.project_id || !data.title)) return fail(400, 'project_id et title requis');
  if (table === 'items' && (!data.project_id || !data.title)) return fail(400, 'project_id et title requis');

  const id = (typeof body.id === 'string' && /^[\w-]{1,64}$/.test(body.id)) ? body.id : newId();
  const ts = now();
  const row = { id, ...data, created_at: ts, updated_at: ts };
  if (table === 'items') {
    row.kind = row.kind || 'task';
    row.status = row.status || (row.kind === 'artifact' ? 'done' : 'todo');
    if (row.status === 'done') row.done_at = ts;
  }
  if (row.position === undefined) {
    const scope = table === 'projects' ? '' : ' WHERE project_id = ?';
    const stmt = db.prepare(`SELECT COALESCE(MAX(position), 0) + 1 AS p FROM ${table}${scope}`);
    row.position = (await (scope ? stmt.bind(row.project_id) : stmt).first()).p;
  }
  const cols = Object.keys(row);
  const stmts = [
    db.prepare(`INSERT INTO ${table} (${cols.join(',')}) VALUES (${cols.map(() => '?').join(',')})`).bind(...cols.map(c => row[c])),
  ];
  if (table === 'items') {
    const action = row.kind === 'artifact' ? 'artifact' : row.kind === 'idea' ? 'idea' : 'create';
    stmts.push(log(db, { project_id: row.project_id, item_id: id, action, label: row.title, source: row.source || 'moi' }));
  } else if (table === 'projects') {
    stmts.push(log(db, { project_id: id, action: 'project', label: `Nouveau projet : ${row.name}` }));
  }
  await db.batch(stmts);
  return json(await db.prepare(`SELECT * FROM ${table} WHERE id = ?`).bind(id).first(), 201);
}

async function update(db, table, id, body) {
  const before = await db.prepare(`SELECT * FROM ${table} WHERE id = ?`).bind(id).first();
  if (!before) return fail(404, 'introuvable');
  const data = pick(table, body);
  if (!Object.keys(data).length) return json(before);
  data.updated_at = now();
  const stmts = [];
  if (table === 'items' && data.status && data.status !== before.status) {
    data.done_at = data.status === 'done' ? data.updated_at : null;
    if (data.status === 'done') {
      stmts.push(log(db, { project_id: before.project_id, item_id: id, action: 'done', label: before.title, source: body.source || 'moi' }));
    } else if (before.status === 'done') {
      stmts.push(log(db, { project_id: before.project_id, item_id: id, action: 'reopen', label: before.title, source: body.source || 'moi' }));
    } else if (data.status === 'doing') {
      stmts.push(log(db, { project_id: before.project_id, item_id: id, action: 'start', label: before.title, source: body.source || 'moi' }));
    }
  }
  // Un élément qui change de projet emmène ses sous-tâches.
  if (table === 'items' && data.project_id && data.project_id !== before.project_id) {
    stmts.push(db.prepare('UPDATE items SET project_id = ?, theme_id = NULL WHERE parent_id = ?').bind(data.project_id, id));
    if (data.theme_id === undefined) data.theme_id = null;
  }
  const cols = Object.keys(data);
  stmts.unshift(
    db.prepare(`UPDATE ${table} SET ${cols.map(c => `${c} = ?`).join(', ')} WHERE id = ?`).bind(...cols.map(c => data[c]), id),
  );
  await db.batch(stmts);
  return json(await db.prepare(`SELECT * FROM ${table} WHERE id = ?`).bind(id).first());
}

async function remove(db, table, id) {
  const before = await db.prepare(`SELECT * FROM ${table} WHERE id = ?`).bind(id).first();
  if (!before) return fail(404, 'introuvable');
  const stmts = [];
  if (table === 'items') {
    // Supprime l'élément et toute sa descendance.
    const all = (await db.prepare('SELECT id, parent_id FROM items WHERE project_id = ?').bind(before.project_id).all()).results;
    const doomed = new Set([id]);
    let grew = true;
    while (grew) {
      grew = false;
      for (const r of all) if (r.parent_id && doomed.has(r.parent_id) && !doomed.has(r.id)) { doomed.add(r.id); grew = true; }
    }
    for (const d of doomed) stmts.push(db.prepare('DELETE FROM items WHERE id = ?').bind(d));
    stmts.push(log(db, { project_id: before.project_id, item_id: id, action: 'delete', label: before.title }));
  } else if (table === 'themes') {
    // Les éléments du thème ne sont pas perdus : ils passent en "Sans thématique".
    stmts.push(db.prepare('UPDATE items SET theme_id = NULL WHERE theme_id = ?').bind(id));
    stmts.push(db.prepare('DELETE FROM themes WHERE id = ?').bind(id));
    stmts.push(log(db, { project_id: before.project_id, action: 'delete', label: `Thématique « ${before.title} »` }));
  } else {
    stmts.push(db.prepare('DELETE FROM items WHERE project_id = ?').bind(id));
    stmts.push(db.prepare('DELETE FROM themes WHERE project_id = ?').bind(id));
    stmts.push(db.prepare('DELETE FROM projects WHERE id = ?').bind(id));
    stmts.push(log(db, { project_id: null, action: 'delete', label: `Projet « ${before.name} » supprimé` }));
  }
  await db.batch(stmts);
  return json({ ok: true });
}

// Réordonnancement après glisser-déposer : [{ id, position, theme_id?, parent_id?, project_id? }]
async function reorder(db, table, moves) {
  if (!Array.isArray(moves) || !moves.length || moves.length > 500) return fail(400, 'moves invalide');
  const ts = now();
  const stmts = moves.map(m => {
    const data = pick(table, m);
    const cols = Object.keys(data);
    return db
      .prepare(`UPDATE ${table} SET ${cols.map(c => `${c} = ?, `).join('')}updated_at = ? WHERE id = ?`)
      .bind(...cols.map(c => data[c]), ts, String(m.id));
  });
  await db.batch(stmts);
  return json({ ok: true });
}

export async function onRequest({ request, env, params }) {
  const db = env.DB;
  if (!db) return fail(503, 'Liaison D1 "DB" absente : Pages → Settings → Bindings → D1 → DB = cockpit-db, puis redéployer.');

  try {
    if (!(await authorized(request, db))) return fail(401, 'Jeton invalide');

    const parts = (params.route || []).filter(Boolean);
    const [resource, id] = parts;
    const method = request.method;
    const body = ['POST', 'PATCH', 'PUT'].includes(method) ? await request.json().catch(() => ({})) : {};

    if (resource === 'state' && method === 'GET') return json(await readState(db));

    if (resource === 'reorder' && method === 'POST') {
      if (!TABLES[body.table]) return fail(400, 'table invalide');
      return reorder(db, body.table, body.moves);
    }

    if (!TABLES[resource]) return fail(404, 'route inconnue');
    if (method === 'GET' && !id) {
      return json((await db.prepare(`SELECT * FROM ${resource} ORDER BY position`).all()).results);
    }
    if (method === 'POST' && !id) return create(db, resource, body);
    if ((method === 'PATCH' || method === 'PUT') && id) return update(db, resource, id, body);
    if (method === 'DELETE' && id) return remove(db, resource, id);
    return fail(405, 'méthode non prise en charge');
  } catch (err) {
    return fail(400, err.message || 'erreur');
  }
}
