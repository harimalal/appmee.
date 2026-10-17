import { HttpError } from './http.js';

const TRACKING = /^(utm_|fbclid|gclid|ref$|referrer|si$|feature$|pp$|campaignid|couponcode$)/i;

export function parseUrl(raw) {
  let u;
  try {
    u = new URL(String(raw).trim());
  } catch {
    throw new HttpError(400, `URL invalide : ${raw}`);
  }
  if (!['http:', 'https:'].includes(u.protocol)) throw new HttpError(400, 'Seules les URL http(s) sont acceptées');
  const h = u.hostname.toLowerCase();
  // Garde-fou SSRF : on refuse localhost, IP littérales et noms sans point.
  if (!h.includes('.') || /^\d+\.\d+\.\d+\.\d+$/.test(h) || h.startsWith('[') || h.endsWith('.local') || h.endsWith('.internal')) {
    throw new HttpError(400, 'Hôte non autorisé');
  }
  return u;
}

const hostIs = (host, domain) => host === domain || host.endsWith('.' + domain);

export function detectSource(url) {
  const h = url.hostname.toLowerCase();
  if (hostIs(h, 'youtube.com') || hostIs(h, 'youtu.be')) return 'youtube';
  if (hostIs(h, 'udemy.com')) return 'udemy';
  if (hostIs(h, 'coursera.org')) return 'coursera';
  if (hostIs(h, 'openclassrooms.com')) return 'openclassrooms';
  return 'web';
}

export function youtubeIds(url) {
  const h = url.hostname.toLowerCase();
  let video = null;
  if (hostIs(h, 'youtu.be')) video = url.pathname.slice(1).split('/')[0] || null;
  else if (url.pathname === '/watch') video = url.searchParams.get('v');
  else {
    const m = url.pathname.match(/^\/(?:shorts|embed|live)\/([\w-]{6,})/);
    if (m) video = m[1];
  }
  return { video, playlist: url.searchParams.get('list') };
}

// URL canonique = clé de déduplication.
export function canonicalize(raw) {
  const u = parseUrl(raw);
  const source = detectSource(u);
  if (source === 'youtube') {
    const { video, playlist } = youtubeIds(u);
    if (video) return `https://www.youtube.com/watch?v=${video}`;
    if (playlist) return `https://www.youtube.com/playlist?list=${playlist}`;
    return `https://www.youtube.com${u.pathname}`.replace(/\/$/, '');
  }
  u.hash = '';
  for (const k of [...u.searchParams.keys()]) if (TRACKING.test(k)) u.searchParams.delete(k);
  u.hostname = u.hostname.toLowerCase();
  let out = u.toString();
  if (u.pathname !== '/') out = out.replace(/\/(\?|$)/, '$1');
  return out;
}

const decode = (s = '') =>
  s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#0?39;|&apos;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ');

export function parseHtmlMeta(html) {
  const meta = {};
  for (const tag of html.match(/<meta\s[^>]*>/gi) || []) {
    const key = (tag.match(/(?:property|name)\s*=\s*["']([^"']+)["']/i) || [])[1];
    const val = (tag.match(/content\s*=\s*(?:"([^"]*)"|'([^']*)')/i) || []).slice(1).find((v) => v !== undefined);
    if (key && val !== undefined && !(key.toLowerCase() in meta)) meta[key.toLowerCase()] = decode(val);
  }
  const titleTag = decode((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '').trim();

  const jsonld = [];
  for (const m of html.matchAll(/<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
    try {
      const data = JSON.parse(m[1]);
      for (const node of Array.isArray(data) ? data : data['@graph'] || [data]) {
        const t = [].concat(node['@type'] || []);
        if (t.some((x) => /Course|VideoObject|Article|LearningResource|Product|WebPage/i.test(x))) {
          jsonld.push({
            type: t.join(','),
            name: node.name,
            description: node.description,
            author: node.author?.name || node.creator?.name || node.provider?.name,
            inLanguage: node.inLanguage,
            duration: node.duration || node.timeRequired,
            datePublished: node.datePublished,
            rating: node.aggregateRating?.ratingValue,
            ratingCount: node.aggregateRating?.ratingCount || node.aggregateRating?.reviewCount,
          });
        }
      }
    } catch { /* JSON-LD invalide : on ignore */ }
  }

  const text = decode(
    html
      .replace(/<(script|style|noscript|svg|nav|footer|header|title)[\s\S]*?<\/\1>/gi, ' ')
      .replace(/<[^>]+>/g, ' ')
  )
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 5000);

  return {
    title: meta['og:title'] || meta['twitter:title'] || titleTag || '',
    description: meta['og:description'] || meta['description'] || meta['twitter:description'] || '',
    image: meta['og:image'] || meta['twitter:image'] || '',
    siteName: meta['og:site_name'] || '',
    author: meta['author'] || '',
    jsonld: jsonld.slice(0, 3),
    text,
  };
}

function isoDurationToMinutes(iso) {
  const m = /^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/.exec(iso || '');
  if (!m) return null;
  return Math.round((+m[1] || 0) * 1440 + (+m[2] || 0) * 60 + (+m[3] || 0) + (+m[4] || 0) / 60);
}
export { isoDurationToMinutes };

const UA = 'Mozilla/5.0 (compatible; MasterIA-Bot/1.0)';

async function fetchText(url, { timeout = 8000, headers = {} } = {}) {
  const res = await fetch(url, {
    headers: { 'user-agent': UA, accept: 'text/html,application/json', 'accept-language': 'fr,en;q=0.8', ...headers },
    redirect: 'follow',
    signal: AbortSignal.timeout(timeout),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return (await res.text()).slice(0, 600_000);
}

async function youtubeMeta(url, env) {
  const { video, playlist } = youtubeIds(url);
  const out = { source: 'youtube', kind: video ? 'video' : playlist ? 'playlist' : 'channel' };

  try {
    const o = JSON.parse(await fetchText(`https://www.youtube.com/oembed?format=json&url=${encodeURIComponent(url.toString())}`));
    Object.assign(out, { title: o.title, author: o.author_name, image: o.thumbnail_url });
  } catch (e) {
    out.oembedError = e.message;
  }

  // Avec une clé YouTube Data API v3 (gratuite, 10 000 unités/jour) : description, durée, vues, date.
  if (env.YOUTUBE_API_KEY && (video || playlist)) {
    try {
      const api = video
        ? `https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=${video}&key=${env.YOUTUBE_API_KEY}`
        : `https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&id=${playlist}&key=${env.YOUTUBE_API_KEY}`;
      const item = JSON.parse(await fetchText(api)).items?.[0];
      if (item) {
        const s = item.snippet || {};
        Object.assign(out, {
          title: s.title || out.title,
          author: s.channelTitle || out.author,
          description: (s.description || '').slice(0, 3000),
          publishedAt: s.publishedAt,
          youtubeTags: (s.tags || []).slice(0, 15),
          language: s.defaultAudioLanguage || s.defaultLanguage,
          durationMinutes: isoDurationToMinutes(item.contentDetails?.duration),
          itemCount: item.contentDetails?.itemCount,
          views: item.statistics?.viewCount && Number(item.statistics.viewCount),
          likes: item.statistics?.likeCount && Number(item.statistics.likeCount),
        });
      }
    } catch (e) {
      out.apiError = e.message;
    }
  }
  return out;
}

// Récupère ce qu'on peut sans scraper agressivement : oEmbed/API pour YouTube, balises Open Graph + JSON-LD ailleurs.
// Udemy / Coursera / OpenClassrooms bloquent souvent les requêtes serveur : on renvoie alors `blocked: true`
// et c'est l'outil web_fetch côté Claude qui prend le relais.
export async function fetchMetadata(rawUrl, env) {
  const url = parseUrl(rawUrl);
  const source = detectSource(url);
  if (source === 'youtube') return youtubeMeta(url, env);
  try {
    const html = await fetchText(url.toString());
    const meta = parseHtmlMeta(html);
    return { source, ...meta, blocked: !meta.title && !meta.description && meta.text.length < 200 };
  } catch (e) {
    return { source, blocked: true, error: e.message };
  }
}
