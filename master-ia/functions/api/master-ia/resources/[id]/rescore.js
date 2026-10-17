import { json } from '../../../../_lib/master-ia/http.js';
import { rescoreResource } from '../../../../_lib/master-ia/service.js';

export async function onRequestPost({ env, params }) {
  return json({ resource: await rescoreResource(env, params.id) });
}
