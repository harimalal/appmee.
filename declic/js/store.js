/* ============================================================
   DÉCLIC — Stockage + authentification
   Mode démo : localStorage. Toutes les lectures/écritures passent
   par ce module : pour passer sur Supabase, seul ce fichier change
   (voir supabase/schema.sql et README).
   ============================================================ */
(function () {
  'use strict';
  const KEY = 'declic.db.v1';
  const SESSION_KEY = 'declic.session.v1';

  let clockShift = 0; // ms, utilisé uniquement par le jeu de données de démo
  const nowDate = () => new Date(Date.now() + clockShift);
  const now = () => nowDate().toISOString();
  const uid = (p) => (p || 'id') + '_' + Math.random().toString(36).slice(2, 9) + Date.now().toString(36).slice(-3);

  const defaults = () => ({
    v: 1,
    seeded: false,
    settings: {
      owner: 'Claire RTH', email: 'claire@declic.fr', phone: '', city: '', siret: '', address: '',
      status: 'Micro-entrepreneur', tva: 'TVA non applicable, art. 293 B du CGI', iban: '', whatsapp: '',
      calendarUrl: '', stripe: { premier: '', declic: '', transformation: '', momentum: '' },
      autopilot: true, // les emails partent seuls
      brandColor: '#b5533c',
    },
    users: [],
    clients: [],
    invoices: [],
    outbox: [],
    activity: [],
    launch: {},
    refs: [],
  });

  let db = null;

  function load() {
    try { const raw = localStorage.getItem(KEY); if (raw) { db = JSON.parse(raw); if (db && db.v === 1) return db; } } catch (e) { /* ignore */ }
    db = defaults();
    return db;
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(db)); } catch (e) { console.warn('Stockage indisponible', e); } }
  function reset() { db = defaults(); save(); }
  function get() { return db || load(); }

  async function hash(pw) {
    try {
      if (crypto && crypto.subtle) {
        const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode('declic:' + pw));
        return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, '0')).join('');
      }
    } catch (e) { /* fallthrough */ }
    let h = 5381; const s = 'declic:' + pw;
    for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
    return 'x' + (h >>> 0).toString(16);
  }

  /* ---------- Sessions ---------- */
  const session = {
    get() { try { return JSON.parse(localStorage.getItem(SESSION_KEY)); } catch (e) { return null; } },
    set(s) { localStorage.setItem(SESSION_KEY, JSON.stringify(s)); },
    clear() { localStorage.removeItem(SESSION_KEY); },
  };

  async function addUser({ email, password, role, clientId }) {
    const d = get();
    email = String(email).trim().toLowerCase();
    if (d.users.some((u) => u.email === email)) throw new Error('Un compte existe déjà avec cet email.');
    const u = { id: uid('u'), email, pw: await hash(password), role, clientId: clientId || null };
    d.users.push(u); save(); return u;
  }

  async function login(email, password) {
    const d = get();
    email = String(email).trim().toLowerCase();
    const u = d.users.find((x) => x.email === email);
    if (!u || u.pw !== (await hash(password))) throw new Error('Email ou mot de passe incorrect.');
    const s = { userId: u.id, role: u.role, clientId: u.clientId, email: u.email };
    session.set(s); return s;
  }

  async function ensureCoach() {
    const d = get();
    if (!d.users.some((u) => u.role === 'coach')) {
      await addUser({ email: d.settings.email, password: 'declic2026', role: 'coach' });
    }
  }

  const clientById = (id) => get().clients.find((c) => c.id === id);
  function log(clientId, text, kind) {
    get().activity.unshift({ id: uid('a'), t: now(), clientId: clientId || null, text, kind: kind || 'info' });
    if (get().activity.length > 400) get().activity.length = 400;
  }

  window.Store = { load, save, reset, get, uid, now, nowDate, hash, session, addUser, login, ensureCoach, clientById, log,
    shiftClock(days) { clockShift += days * 86400000; }, setClock(ms) { clockShift = ms; }, getClock() { return clockShift; } };
})();
