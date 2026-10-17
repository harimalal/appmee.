import { canonicalize, detectSource, fetchMetadata, parseUrl } from './sources.js';
import { enrich } from './claude.js';
import { findByCanonical, getProfile, insertResource, applyEnrichment, getResource } from './db.js';

// Ajoute une ressource à partir d'une URL : métadonnées -> fiche Claude -> insertion.
export async function addResource(env, rawUrl) {
  const canonical = canonicalize(rawUrl);
  const existing = await findByCanonical(env, canonical);
  if (existing) return { resource: existing, duplicate: true };

  const url = parseUrl(rawUrl).toString();
  const source = detectSource(parseUrl(rawUrl));
  const [meta, profile] = await Promise.all([fetchMetadata(url, env), getProfile(env)]);
  const fiche = await enrich(env, { url: canonical, source, meta, profile });
  const resource = await insertResource(env, {
    ...fiche,
    url,
    canonical_url: canonical,
    source,
    author: meta.author || '',
    thumbnail: meta.image || '',
  });
  return { resource, duplicate: false };
}

// Relance la fiche d'une ressource existante (après un changement de profil, par ex.) sans toucher au statut ni aux notes.
export async function rescoreResource(env, id) {
  const r = await getResource(env, id);
  const [meta, profile] = await Promise.all([fetchMetadata(r.url, env), getProfile(env)]);
  const fiche = await enrich(env, { url: r.canonical_url, source: r.source, meta, profile });
  return applyEnrichment(env, id, fiche, { author: meta.author || r.author, thumbnail: meta.image || r.thumbnail });
}
