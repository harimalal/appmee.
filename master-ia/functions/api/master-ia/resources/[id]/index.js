import { json, readJson } from '../../../../_lib/master-ia/http.js';
import { deleteResource, getResource, updateResource } from '../../../../_lib/master-ia/db.js';

export async function onRequestGet({ env, params }) {
  return json({ resource: await getResource(env, params.id) });
}

export async function onRequestPatch({ request, env, params }) {
  return json({ resource: await updateResource(env, params.id, await readJson(request)) });
}

export async function onRequestDelete({ env, params }) {
  await getResource(env, params.id);
  await deleteResource(env, params.id);
  return json({ ok: true });
}
