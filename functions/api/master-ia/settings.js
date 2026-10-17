import { json, readJson, HttpError } from '../../_lib/master-ia/http.js';
import { getProfile, setProfile } from '../../_lib/master-ia/db.js';
import { CATEGORIES, TYPES, LEVELS, LANGS, STATUSES, SOURCES } from '../../_lib/master-ia/taxonomy.js';

export async function onRequestGet({ env }) {
  return json({
    profile: await getProfile(env),
    taxonomy: { categories: CATEGORIES, types: TYPES, levels: LEVELS, languages: LANGS, statuses: STATUSES, sources: Object.fromEntries(Object.entries(SOURCES).map(([k, v]) => [k, v.label])) },
    capabilities: { youtube_api: !!env.YOUTUBE_API_KEY, model: env.ANTHROPIC_MODEL || 'claude-opus-5-5' },
  });
}

export async function onRequestPut({ request, env }) {
  const { profile } = await readJson(request);
  if (typeof profile !== 'string' || profile.trim().length < 10) throw new HttpError(400, 'Profil trop court');
  await setProfile(env, profile.trim().slice(0, 3000));
  return json({ ok: true });
}
