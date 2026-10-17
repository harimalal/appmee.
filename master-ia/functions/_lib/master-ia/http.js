export class HttpError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
}

export async function readJson(request) {
  try {
    return await request.json();
  } catch {
    throw new HttpError(400, 'Corps JSON invalide');
  }
}

export function requireDb(env) {
  if (!env.MASTER_IA_DB) throw new HttpError(500, 'Binding D1 MASTER_IA_DB manquant (voir master-ia/README.md)');
  return env.MASTER_IA_DB;
}
