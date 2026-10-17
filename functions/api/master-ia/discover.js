import { json, readJson, HttpError } from '../../_lib/master-ia/http.js';
import { SOURCES } from '../../_lib/master-ia/taxonomy.js';
import { discover } from '../../_lib/master-ia/claude.js';
import { getProfile, findByCanonical } from '../../_lib/master-ia/db.js';
import { canonicalize, detectSource, parseUrl } from '../../_lib/master-ia/sources.js';

// Corps : { query, sources: ['youtube','udemy',…,'web'], domains: ['huggingface.co'], limit }
// Cherche des ressources via web_search côté Anthropic, restreint aux plateformes choisies.
export async function onRequestPost({ request, env }) {
  const body = await readJson(request);
  const query = String(body.query || '').trim().slice(0, 400);
  if (query.length < 3) throw new HttpError(400, 'Décris ce que tu cherches (3 caractères minimum)');
  const limit = Math.max(1, Math.min(15, Math.round(+body.limit || 8)));

  const sources = (Array.isArray(body.sources) ? body.sources : []).filter((s) => s in SOURCES);
  const custom = (Array.isArray(body.domains) ? body.domains : [])
    .map((d) => String(d).trim().toLowerCase().replace(/^https?:\/\//, '').replace(/\/.*$/, ''))
    .filter((d) => /^[a-z0-9-]+(\.[a-z0-9-]+)+$/.test(d));
  let domains = [...new Set([...sources.flatMap((s) => SOURCES[s].domains), ...custom])];
  // « Site web » sans domaine précisé = recherche libre sur tout le web.
  if (sources.includes('web') && !custom.length) domains = [];
  if (!sources.length && !custom.length) throw new HttpError(400, 'Choisis au moins une source');

  const candidates = await discover(env, { query, domains, limit, profile: await getProfile(env) });

  const out = [];
  const seen = new Set();
  for (const c of candidates) {
    try {
      const canonical = canonicalize(c.url);
      if (seen.has(canonical)) continue;
      const host = parseUrl(canonical).hostname;
      if (domains.length && !domains.some((d) => host === d || host.endsWith('.' + d))) continue;
      seen.add(canonical);
      out.push({
        url: canonical,
        title: String(c.title || canonical).slice(0, 200),
        source: detectSource(parseUrl(canonical)),
        language: c.language || 'autre',
        why: String(c.why || '').slice(0, 300),
        preliminary_score: Math.max(0, Math.min(10, Math.round(+c.preliminary_score) || 0)),
        exists: !!(await findByCanonical(env, canonical)),
      });
    } catch { /* URL invalide renvoyée par le modèle : écartée */ }
  }
  return json({ candidates: out.sort((a, b) => b.preliminary_score - a.preliminary_score) });
}
