import test from 'node:test';
import assert from 'node:assert/strict';
import { canonicalize, detectSource, parseHtmlMeta, parseUrl, isoDurationToMinutes } from '../functions/_lib/master-ia/sources.js';
import { extractJson, normalize } from '../functions/_lib/master-ia/claude.js';

test('canonicalize : YouTube toutes formes -> même clé', () => {
  const want = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
  for (const u of [
    'https://youtu.be/dQw4w9WgXcQ?si=abc',
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s&utm_source=x',
    'https://m.youtube.com/watch?v=dQw4w9WgXcQ&list=PL1',
    'https://www.youtube.com/shorts/dQw4w9WgXcQ',
  ]) assert.equal(canonicalize(u), want, u);
  assert.equal(canonicalize('https://www.youtube.com/playlist?list=PLabc'), 'https://www.youtube.com/playlist?list=PLabc');
});

test('canonicalize : retire le tracking et le slash final', () => {
  assert.equal(canonicalize('https://www.udemy.com/course/llm/?couponCode=X&utm_medium=a#top'), 'https://www.udemy.com/course/llm');
  assert.equal(canonicalize('https://www.coursera.org/learn/ml?ref=1&specialization=2'), 'https://www.coursera.org/learn/ml?specialization=2');
});

test('detectSource', () => {
  const d = (u) => detectSource(parseUrl(u));
  assert.equal(d('https://fr.coursera.org/learn/x'), 'coursera');
  assert.equal(d('https://openclassrooms.com/fr/courses/1'), 'openclassrooms');
  assert.equal(d('https://notyoutube.com/x'), 'web');
});

test('parseUrl refuse les cibles internes', () => {
  for (const u of ['http://localhost/x', 'http://127.0.0.1/', 'http://169.254.169.254/latest', 'ftp://a.com/x', 'https://intranet/x', 'nope'])
    assert.throws(() => parseUrl(u), u);
});

test('parseHtmlMeta : Open Graph, JSON-LD, texte', () => {
  const html = `<html><head><title>Fallback</title>
    <meta property="og:title" content="Deep Learning &amp; LLM">
    <meta name="description" content="Un cours">
    <meta property="og:image" content="https://x/i.png">
    <script type="application/ld+json">{"@type":"Course","name":"DL","provider":{"name":"Stanford"},"aggregateRating":{"ratingValue":4.8,"ratingCount":120}}</script>
    <script>var x=1</script></head><body><nav>menu</nav><p>Bonjour   le monde</p></body></html>`;
  const m = parseHtmlMeta(html);
  assert.equal(m.title, 'Deep Learning & LLM');
  assert.equal(m.description, 'Un cours');
  assert.equal(m.jsonld[0].author, 'Stanford');
  assert.equal(m.jsonld[0].rating, 4.8);
  assert.equal(m.text, 'Bonjour le monde');
});

test('isoDurationToMinutes', () => {
  assert.equal(isoDurationToMinutes('PT1H2M30S'), 63);
  assert.equal(isoDurationToMinutes('PT45S'), 1);
  assert.equal(isoDurationToMinutes('nope'), null);
});

test('extractJson : fences, texte autour, accolades dans les chaînes', () => {
  assert.deepEqual(extractJson('Voici :\n```json\n{"a":"x}y","b":{"c":1}}\n```\nfin'), { a: 'x}y', b: { c: 1 } });
  assert.throws(() => extractJson('rien'));
});

test('normalize : refuse une fiche incomplète', () => {
  assert.throws(() => normalize({ candidates: [] }), /invalide/);
  assert.throws(() => normalize({ title: 'T' }), /invalide/);
});

test('normalize : bornes, enums, plafond de note si confiance faible', () => {
  const n = normalize({ title: 'T', category: 'x', score: 15, confidence: 'faible', category: 'inconnue', tags: ['LLM', 'llm', ' RAG '], type: 'zzz' });
  assert.equal(n.score, 7);
  assert.equal(n.category, 'Autre');
  assert.deepEqual(n.tags, ['llm', 'rag']);
  assert.equal(n.type, 'autre');
  assert.equal(normalize({ title: 'T', category: 'x', score: -3, confidence: 'haute' }).score, 0);
  assert.equal(normalize({ title: 'T', category: 'x', score: 9.6, confidence: 'haute' }).score, 10);
});
