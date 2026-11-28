/**
 * Rendu image par image (déterministe) du reel « histoire », puis encodage H.264 (ffmpeg).
 * Usage : NODE_PATH=$(npm root -g) node render.cjs --out out/reel-histoire.mp4 --frames /chemin/frames [--workers 4] [--fps 30] [--limit N]
 * Aucune génération d'image ni de vidéo : HTML/CSS/JS rendu par Chromium, assemblé par ffmpeg. Piste audio silencieuse (remplacée par mix.py).
 */
const { chromium } = require('playwright'); const { spawnSync } = require('child_process'); const fs = require('fs'); const path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const FPS = parseInt(arg('fps', '30'), 10), WORKERS = parseInt(arg('workers', '4'), 10);
const OUT = path.resolve(arg('out', 'out/reel-histoire.mp4')), FRAMES = path.resolve(arg('frames', '/tmp/histoire-frames'));
const LIMIT = arg('limit', null) && parseInt(arg('limit'), 10);
const FILE = 'file://' + path.resolve(__dirname, 'story.html');
const TOTAL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json'), 'utf8')).total;
const pad = n => String(n).padStart(5, '0');
(async () => {
  fs.mkdirSync(FRAMES, { recursive: true }); fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const N = LIMIT ? Math.min(LIMIT, Math.ceil(TOTAL * FPS)) : Math.ceil(TOTAL * FPS);
  console.log(`${N} images (${(N / FPS).toFixed(2)} s)`);
  const t0 = Date.now(); const browser = await chromium.launch(); const pages = [];
  for (let w = 0; w < WORKERS; w++) { const pg = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 }); await pg.goto(FILE); await pg.evaluate(() => Promise.all([document.fonts.ready, window.__ready || 0])); pages.push(pg); }
  let done = 0;
  await Promise.all(pages.map(async (pg, w) => { for (let i = w; i < N; i += WORKERS) {
    await pg.evaluate(async t => { window.__setTime(t); if (window.__wait) await window.__wait(); }, i / FPS);
    await pg.screenshot({ path: path.join(FRAMES, pad(i) + '.png'), type: 'png' });
    if (++done % 300 === 0) console.log(`  ${done}/${N} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  } }));
  const poster = pages[0]; await poster.evaluate(t => window.__setTime(t), 1.6);
  await poster.screenshot({ path: path.join(path.dirname(OUT), 'poster-histoire.png'), type: 'png' });
  await browser.close(); console.log(`images : ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  const args = ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(FRAMES, '%05d.png'),
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000', '-t', String(N / FPS),
    '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high', '-level', '4.2', '-r', String(FPS),
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '96k', '-shortest', '-movflags', '+faststart', OUT];
  if (spawnSync('ffmpeg', args, { stdio: 'inherit' }).status !== 0) { console.error('ffmpeg a échoué'); process.exit(1); }
  console.log(`vidéo : ${OUT} (${(fs.statSync(OUT).size / 1048576).toFixed(1)} Mo) en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
})();
