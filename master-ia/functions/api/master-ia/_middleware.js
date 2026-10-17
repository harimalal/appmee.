import { HttpError, json } from '../../_lib/master-ia/http.js';

// Outil mono-utilisateur : un jeton partagé (variable MASTER_IA_TOKEN) protège toute l'API.
// Refuse tout si le jeton n'est pas configuré, plutôt que de laisser l'API ouverte.
export async function onRequest({ request, env, next }) {
  try {
    if (!env.MASTER_IA_TOKEN) throw new HttpError(500, 'MASTER_IA_TOKEN non configuré (voir master-ia/README.md)');
    const given = (request.headers.get('authorization') || '').replace(/^Bearer\s+/i, '');
    const enc = new TextEncoder();
    const [a, b] = [enc.encode(given), enc.encode(env.MASTER_IA_TOKEN)];
    let diff = a.length ^ b.length;
    for (let i = 0; i < b.length; i++) diff |= (a[i] ?? 0) ^ b[i];
    if (diff !== 0) throw new HttpError(401, 'Jeton invalide');
    return await next();
  } catch (e) {
    if (!(e instanceof HttpError)) console.error(e);
    const status = e instanceof HttpError ? e.status : e?.status >= 400 && e.status < 600 ? 502 : 500;
    return json({ error: e instanceof HttpError ? e.message : `Erreur serveur : ${e?.message || e}` }, status);
  }
}
