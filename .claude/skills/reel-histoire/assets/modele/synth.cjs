/**
 * Bruitages (sfx) et nappe musicale (bed) du reel, SYNTHÉTISÉS ici en JavaScript (aucun service externe, aucun échantillon).
 * Version « histoire » : les bruitages sont lus dans events.json (émis par story.html : une seule source de vérité pour l'image et le son).
 * Déterministe : même entrée, mêmes fichiers. Usage : node synth.cjs <dossier_de_sortie>  -> sfx.wav et bed.wav (stéréo, 48 kHz, 16 bits)
 */
const fs = require('fs');
const path = require('path');

const EVT = JSON.parse(fs.readFileSync(path.join(__dirname, 'events.json'), 'utf8'));
const SR = 48000, DUR = Math.ceil(EVT.total * 10) / 10, N = Math.round(SR * DUR);
const OUT = path.resolve(process.argv[2] || '/tmp/reel-audio');
fs.mkdirSync(OUT, { recursive: true });

let seed = 20261126;
const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
const noise = () => rnd() * 2 - 1;
const mkStem = () => [new Float32Array(N), new Float32Array(N)];
const sfx = mkStem(), bed = mkStem();

/* ---------- briques ---------- */
function put(stem, t0, arr, gain = 1, p0 = 0, p1 = p0) {
  const i0 = Math.round(t0 * SR);
  for (let i = 0; i < arr.length; i++) {
    const j = i0 + i; if (j < 0 || j >= N) continue;
    const p = p0 + (p1 - p0) * (i / Math.max(1, arr.length - 1)); // -1 gauche … +1 droite
    const a = (p + 1) * Math.PI / 4;                                 // pan à puissance constante
    stem[0][j] += arr[i] * gain * Math.cos(a);
    stem[1][j] += arr[i] * gain * Math.sin(a);
  }
}
const gen = (dur, fn) => { const n = Math.floor(dur * SR), a = new Float32Array(n); for (let i = 0; i < n; i++) a[i] = fn(i / SR, i); return a; };
const dec = (t, k) => Math.exp(-t * k);

function svf(fc, q, type) { // filtre à variables d'état (Chamberlin) ; fc peut varier par échantillon
  let low = 0, band = 0;
  return (x, fcNow) => {
    const f = 2 * Math.sin(Math.PI * Math.min(fcNow ?? fc, SR * 0.45) / SR);
    low += f * band; const high = x - low - q * band; band += f * high;
    return type === 'low' ? low : type === 'high' ? high : band;
  };
}
const lerpLog = (a, b, k) => a * Math.pow(b / a, k);

function thump(dur = .5, f0 = 110, f1 = 42) {
  let ph = 0;
  return gen(dur, (t) => { const f = f1 + (f0 - f1) * dec(t, 22); ph += 2 * Math.PI * f / SR; return Math.sin(ph) * dec(t, 7) * 0.95 + (t < .008 ? noise() * .3 : 0); });
}
function whoosh(dur, f0, f1, q = .9) {
  const flt = svf(1000, 1 / q, 'band');
  return gen(dur, (t) => { const k = t / dur; const env = Math.pow(Math.sin(Math.PI * Math.min(1, k * 1.15)), 2) * (k < .88 ? 1 : (1 - k) / .12);
    return flt(noise(), lerpLog(f0, f1, k)) * env * 2.2; });
}
function riser(dur, f0 = 900, f1 = 8000) {
  const flt = svf(1000, 1.1, 'high');
  return gen(dur, (t) => { const k = t / dur; return flt(noise(), lerpLog(f0, f1, k)) * Math.pow(k, 2.2) * .9; });
}
const tick = (f = 2400, dur = .035) => gen(dur, (t) => Math.sin(2 * Math.PI * f * t) * dec(t, 140));
function pop(f0 = 420, f1 = 900, dur = .11) { let ph = 0; return gen(dur, (t) => { const f = f0 + (f1 - f0) * Math.min(1, t / .05); ph += 2 * Math.PI * f / SR; return Math.sin(ph) * dec(t, 38); }); }
function thunk(dur = .16) {
  const flt = svf(320, 1.2, 'low'); let ph = 0;
  return gen(dur, (t) => { ph += 2 * Math.PI * (150 - 80 * Math.min(1, t / .1)) / SR; return (flt(noise()) * .9 + Math.sin(ph)) * dec(t, 24) + (t < .004 ? noise() * .4 : 0); });
}
function ding(f, dur = .8) {
  return gen(dur, (t) => (Math.sin(2 * Math.PI * f * t) + .4 * Math.sin(2 * Math.PI * f * 2.01 * t) + .18 * Math.sin(2 * Math.PI * f * 3.02 * t)) * Math.min(1, t / .004) * dec(t, 5.5) * .55);
}
function flap(dur = .16) { const flt = svf(1500, 1.2, 'band'); return gen(dur, (t) => flt(noise(), 1500 - 700 * (t / dur)) * dec(t, 24) * 2.2); }
function beep(f, dur = .09) { return gen(dur, (t) => (Math.sin(2 * Math.PI * f * t) + .3 * Math.sin(2 * Math.PI * f * 3 * t)) * Math.min(1, t / .004) * (1 - t / dur) * .7); }
function hat(dur = .03) { const flt = svf(7000, 1, 'high'); return gen(dur, (t) => flt(noise()) * dec(t, 120)); }
function swipe(dur = .25) { return whoosh(dur, 2500, 7000, 1.4); }

/* ---------- événements -> sons ---------- */
let k = 0;
const pan = () => (k++ % 2 ? .35 : -.35);
for (const e of EVT.events) {
  const t = e.t;
  switch (e.type) {
    case 'thump': put(sfx, t, thump(e.big ? .9 : .5, e.big ? 80 : 110, e.big ? 32 : 42), e.amp ?? .8); break;
    case 'riser': put(sfx, t, riser(e.dur ?? .8), .5, -.3, .3); break;
    case 'pop': put(sfx, t, pop(380 + 40 * (k % 5), 760 + 40 * (k % 5), .1), .34, pan()); k++; break;
    case 'swipe': put(sfx, t, swipe(.28), .2, -.4, .4); break;
    case 'whoosh': { const d = e.dur ?? .4; put(sfx, t, e.up ? whoosh(d, 250, 6500, .7) : e.down ? whoosh(d, 3000, 500) : whoosh(d, 500, 3600), e.up ? .3 : .3, e.up ? .8 : pan(), e.up ? -.8 : -pan()); break; }
    case 'ticks': { const n = e.n ?? 16, d = e.dur ?? .8; for (let i = 0; i < n; i++) put(sfx, t + i * (d / n), tick(1500 + 90 * (i % 12) + rnd() * 500, .022), .2, rnd() * .8 - .4); break; }
    case 'tick': put(sfx, t, tick(e.f ?? 2400, .045), .38); break;
    case 'ding': put(sfx, t, ding(e.f ?? 1046, .7), .55, pan()); break;
    case 'thunk': put(sfx, t, thunk(), (e.amp ?? .85) * .9); break;
    case 'beep': put(sfx, t, beep(e.f ?? 880, .09), .55); break;
    case 'flap': put(sfx, t, flap(.2), .7, -.2, .2); break;
    default: throw new Error('événement inconnu : ' + e.type);
  }
}
// transitions entre scènes : léger balayage (déjà dans les événements « whoosh » de chaque scène)

/* ---------- nappe musicale (120 bpm : un temps = 0,5 s, accords de 4 s : Am – F – C – G) ---------- */
const CH = [[220, 261.6, 329.6, 440, 55], [174.6, 220, 261.6, 349.2, 43.65], [261.6, 329.6, 392, 523.3, 65.4], [196, 246.9, 293.7, 392, 49]];
for (let s = 0; s * 4 < DUR; s++) {
  const t0 = s * 4 - .2, ch = CH[s % 4];
  const len = 4.8, arr = gen(len, (t) => {
    const e = Math.min(1, t / .6) * Math.min(1, (len - t) / .6);
    let v = 0; for (let q = 0; q < 4; q++) { const f = ch[q]; v += Math.sin(2 * Math.PI * f * t) + .6 * Math.sin(2 * Math.PI * f * 1.0035 * t + q); }
    return v * e * .028 * (1 + .12 * Math.sin(2 * Math.PI * .25 * t));
  });
  put(bed, t0, arr, 1, -.15, .15);
}
for (let b = 0; b < DUR * 2; b++) {
  const t = b * .5, ch = CH[Math.floor(t / 4) % 4];
  if (b % 2 === 0) {
    put(bed, t, gen(.22, (u) => Math.sin(2 * Math.PI * (44 + 40 * dec(u, 35)) * u) * dec(u, 16)), .22);
    put(bed, t, gen(.45, (u) => Math.sin(2 * Math.PI * ch[4] * u) * Math.min(1, u / .01) * dec(u, 6)), .13);
  } else put(bed, t, hat(), .06 + .02 * (Math.floor(b / 2) % 2), .3 * ((Math.floor(b / 2) % 2) ? 1 : -1));
}
const fade = (stem) => { for (let c = 0; c < 2; c++) for (let i = 0; i < N; i++) { const t = i / SR; const g = Math.min(1, t / .05) * Math.min(1, (DUR - t) / .25); stem[c][i] *= g; } };
fade(bed); fade(sfx);

/* ---------- écriture WAV 16 bits ---------- */
function wav(stem, file) {
  const peak = Math.max(...stem.map(ch => ch.reduce((m, v) => Math.max(m, Math.abs(v)), 0)));
  const buf = Buffer.alloc(44 + N * 4);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write('WAVEfmt ', 8); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
  buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34); buf.write('data', 36); buf.writeUInt32LE(N * 4, 40);
  const norm = peak > .98 ? .98 / peak : 1; // jamais d'écrêtage à l'écriture
  for (let i = 0; i < N; i++) for (let c = 0; c < 2; c++) buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, stem[c][i] * norm)) * 32767), 44 + i * 4 + c * 2);
  fs.writeFileSync(path.join(OUT, file), buf);
  console.log(`${file} : crête avant normalisation ${peak.toFixed(2)}${norm < 1 ? ' (réduite)' : ''}`);
}
wav(sfx, 'sfx.wav'); wav(bed, 'bed.wav');
