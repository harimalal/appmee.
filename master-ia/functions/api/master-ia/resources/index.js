import { json, readJson, HttpError } from '../../../_lib/master-ia/http.js';
import { listResources } from '../../../_lib/master-ia/db.js';
import { addResource } from '../../../_lib/master-ia/service.js';

export async function onRequestGet({ request, env }) {
  return json(await listResources(env, Object.fromEntries(new URL(request.url).searchParams)));
}

// Corps : { url }. Les imports en lot sont séquencés côté navigateur (un appel Claude par lien).
export async function onRequestPost({ request, env }) {
  const { url } = await readJson(request);
  if (!url || typeof url !== 'string') throw new HttpError(400, 'Champ "url" requis');
  const { resource, duplicate } = await addResource(env, url);
  return json({ resource, duplicate }, duplicate ? 200 : 201);
}
