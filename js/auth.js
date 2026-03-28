'use strict';

/**
 * APPMETIER PLATFORM — auth.js
 * Authentification : connexion, inscription, session, réinitialisation
 *
 * Architecture locale (localStorage) — remplacer _api* par Supabase en production.
 * Aucune dépendance externe.
 */

const Auth = (() => {

  // ============================================================
  // CONFIG
  // ============================================================
  const CFG = {
    SESSION_KEY:   'appmetier_session_v1',
    USERS_KEY:     'appmetier_users_v1',
    DASHBOARD_URL: '/dashboard.html',
    TTL:           7 * 24 * 60 * 60 * 1000, // 7 jours en ms
  };

  // ============================================================
  // SÉCURITÉ
  // ============================================================

  /** Échappe les caractères HTML pour prévenir les injections XSS. */
  function esc(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /**
   * Hash SHA-256 côté client (démo uniquement).
   * En production avec Supabase : le hash est géré côté serveur (bcrypt).
   */
  async function hashPw(pw) {
    const buf  = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(pw));
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // ============================================================
  // COUCHE DONNÉES (remplacer par Supabase SDK en prod)
  // ============================================================

  function getUsers() {
    try { return JSON.parse(localStorage.getItem(CFG.USERS_KEY) || '[]'); }
    catch { return []; }
  }

  function saveUsers(users) {
    try { localStorage.setItem(CFG.USERS_KEY, JSON.stringify(users)); return true; }
    catch { return false; }
  }

  /** Retire le hash du mot de passe avant d'exposer l'utilisateur. */
  function sanitize(user) {
    const { password, ...safe } = user; // eslint-disable-line no-unused-vars
    return safe;
  }

  const delay = ms => new Promise(r => setTimeout(r, ms));

  async function _apiRegister({ prenom, nom, email, password }) {
    await delay(550);
    const users  = getUsers();
    const exists = users.find(u => u.email.toLowerCase() === email.toLowerCase().trim());
    if (exists) throw new Error('Un compte existe déjà avec cet e-mail.');
    const user = {
      id:            crypto.randomUUID(),
      email:         email.toLowerCase().trim(),
      prenom:        prenom.trim(),
      nom:           nom.trim(),
      password:      await hashPw(password),
      created_at:    new Date().toISOString(),
      subscriptions: [],
    };
    users.push(user);
    saveUsers(users);
    return { user: sanitize(user) };
  }

  async function _apiLogin({ email, password }) {
    await delay(480);
    const user = getUsers().find(u => u.email.toLowerCase() === email.toLowerCase().trim());
    if (!user) throw new Error('E-mail ou mot de passe incorrect.');
    if ((await hashPw(password)) !== user.password) throw new Error('E-mail ou mot de passe incorrect.');
    return { user: sanitize(user) };
  }

  async function _apiReset({ email }) { // eslint-disable-line no-unused-vars
    await delay(400);
    return { ok: true }; // Ne pas révéler si l'email existe
  }

  // ============================================================
  // SESSION
  // ============================================================

  function saveSession(user) {
    try {
      localStorage.setItem(CFG.SESSION_KEY, JSON.stringify({
        user,
        expires_at: Date.now() + CFG.TTL,
      }));
    } catch (e) { console.error('Session save failed:', e); }
  }

  function getSession() {
    try {
      const raw = JSON.parse(localStorage.getItem(CFG.SESSION_KEY));
      if (!raw?.user || !raw?.expires_at) return null;
      if (Date.now() > raw.expires_at) { clearSession(); return null; }
      return raw;
    } catch { return null; }
  }

  function clearSession() { localStorage.removeItem(CFG.SESSION_KEY); }

  function requireAuth() {
    const s = getSession();
    if (!s) {
      // Ne rediriger que si on est sur le dashboard
      const path = window.location.pathname;
      const onDashboard = path.includes('dashboard');
      if (onDashboard) window.location.href = '/index.html';
      return null;
    }
    return s.user;
  }

  function redirectIfAuth() {
    // Ne rediriger que si on est sur la page de login (index.html)
    const path = window.location.pathname;
    const onLoginPage = path === '/' || path === '/index.html' || path.endsWith('index.html');
    if (onLoginPage && getSession()) {
      window.location.href = CFG.DASHBOARD_URL;
    }
  }

  // ============================================================
  // VALIDATION
  // ============================================================
  const isValidEmail = e => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.trim());
  const isValidPw    = p => p.length >= 8 && /[A-Z]/.test(p) && /[0-9]/.test(p);

  // ============================================================
  // UI HELPERS
  // ============================================================

  function el(id) { return document.getElementById(id); }

  function showAlert(msg, type = 'error') {
    const a = el('authAlert');
    if (!a) return;
    a.textContent = msg;
    a.className = `auth-alert ${type} show`;
    a.setAttribute('role', 'alert');
  }

  function hideAlert() {
    const a = el('authAlert');
    if (a) a.className = 'auth-alert';
  }

  function fieldError(id, msg) {
    const f = el(id);
    if (f) f.setAttribute('aria-invalid', 'true');
    const e = el(id + '_err');
    if (e) { e.textContent = msg; e.classList.add('show'); }
  }

  function clearErrors() {
    document.querySelectorAll('[aria-invalid]').forEach(f => f.removeAttribute('aria-invalid'));
    document.querySelectorAll('.form-error').forEach(e => e.classList.remove('show'));
  }

  function setLoading(btnId, on) {
    const b = el(btnId);
    if (!b) return;
    b.disabled = on;
    if (on) { b._orig = b.innerHTML; b.innerHTML = '<span class="spinner"></span> Chargement…'; }
    else if (b._orig) b.innerHTML = b._orig;
  }

  // ============================================================
  // FORCE MOT DE PASSE
  // ============================================================
  function updatePwStrength() {
    const pw  = el('reg_pw')?.value || '';
    const bar = el('pwBar');
    const lbl = el('pwLbl');
    if (!bar || !lbl) return;
    let score = 0;
    if (pw.length >= 8)   score++;
    if (pw.length >= 12)  score++;
    if (/[A-Z]/.test(pw)) score++;
    if (/[0-9]/.test(pw)) score++;
    if (/[^A-Za-z0-9]/.test(pw)) score++;
    const lvls = [
      { lbl: '',          bg: 'transparent', w: '0%'   },
      { lbl: 'Faible',    bg: '#c8432b',     w: '25%'  },
      { lbl: 'Moyen',     bg: '#c8830a',     w: '50%'  },
      { lbl: 'Bon',       bg: '#e8a44a',     w: '75%'  },
      { lbl: 'Fort',      bg: '#2d6a4f',     w: '90%'  },
      { lbl: 'Excellent', bg: '#2d6a4f',     w: '100%' },
    ];
    const lvl = lvls[Math.min(score, 5)];
    bar.style.width      = pw ? lvl.w : '0%';
    bar.style.background = lvl.bg;
    lbl.textContent      = pw ? lvl.lbl : '';
    lbl.style.color      = lvl.bg;
  }

  // ============================================================
  // TOGGLE PASSWORD
  // ============================================================
  function togglePw(inputId, btnId) {
    const inp = el(inputId);
    const btn = el(btnId);
    if (!inp || !btn) return;
    const vis  = inp.type === 'text';
    inp.type   = vis ? 'password' : 'text';
    btn.textContent = vis ? '👁' : '🙈';
    btn.setAttribute('aria-label', vis ? 'Afficher le mot de passe' : 'Masquer le mot de passe');
  }

  // ============================================================
  // SWITCH TAB
  // ============================================================
  function switchTab(tab) {
    document.querySelectorAll('.auth-tab').forEach(b => {
      b.classList.toggle('active', b.dataset.tab === tab);
      b.setAttribute('aria-selected', b.dataset.tab === tab ? 'true' : 'false');
    });
    document.querySelectorAll('.auth-panel').forEach(p => {
      p.classList.toggle('active', p.dataset.panel === tab);
    });
    hideAlert(); clearErrors();
    const titles = {
      login:    ['Bon retour.',          'Connectez-vous à votre espace AppMee.'],
      register: ['Créer un compte.',     'Rejoignez la plateforme AppMee.'],
      reset:    ['Mot de passe oublié.', 'Saisissez votre e-mail pour recevoir un lien.'],
    };
    const [t, s] = titles[tab] || ['', ''];
    if (el('formTitle'))  el('formTitle').textContent  = t;
    if (el('formSub'))    el('formSub').textContent    = s;
    // Focus
    const panel = document.querySelector(`.auth-panel[data-panel="${tab}"]`);
    if (panel) { const first = panel.querySelector('input'); if (first) setTimeout(() => first.focus(), 120); }
  }

  // ============================================================
  // HANDLERS
  // ============================================================
  async function handleLogin(e) {
    e.preventDefault();
    clearErrors(); hideAlert();
    const email = el('login_email')?.value?.trim() || '';
    const pw    = el('login_pw')?.value || '';
    let ok = true;
    if (!isValidEmail(email)) { fieldError('login_email', 'E-mail invalide.'); ok = false; }
    if (!pw) { fieldError('login_pw', 'Mot de passe requis.'); ok = false; }
    if (!ok) return;
    setLoading('loginBtn', true);
    try {
      const { user } = await _apiLogin({ email, password: pw });
      saveSession(user);
      window.location.href = CFG.DASHBOARD_URL;
    } catch (err) {
      showAlert(err.message);
      if (el('login_pw')) el('login_pw').value = '';
      setLoading('loginBtn', false);
    }
  }

  async function handleRegister(e) {
    e.preventDefault();
    clearErrors(); hideAlert();
    const prenom  = el('reg_prenom')?.value?.trim() || '';
    const nom     = el('reg_nom')?.value?.trim() || '';
    const email   = el('reg_email')?.value?.trim() || '';
    const pw      = el('reg_pw')?.value || '';
    const confirm = el('reg_confirm')?.value || '';
    const cgu     = el('reg_cgu')?.checked;
    let ok = true;
    if (!prenom) { fieldError('reg_prenom', 'Prénom requis.'); ok = false; }
    if (!nom)    { fieldError('reg_nom',    'Nom requis.');    ok = false; }
    if (!isValidEmail(email)) { fieldError('reg_email', 'E-mail invalide.'); ok = false; }
    if (!isValidPw(pw)) { fieldError('reg_pw', 'Min. 8 caractères, 1 majuscule, 1 chiffre.'); ok = false; }
    if (pw !== confirm) { fieldError('reg_confirm', 'Les mots de passe ne correspondent pas.'); ok = false; }
    if (!cgu) { showAlert('Veuillez accepter les conditions d\'utilisation.'); ok = false; }
    if (!ok) return;
    setLoading('registerBtn', true);
    try {
      const { user } = await _apiRegister({ prenom, nom, email, password: pw });
      saveSession(user);
      window.location.href = CFG.DASHBOARD_URL;
    } catch (err) {
      showAlert(err.message);
      setLoading('registerBtn', false);
    }
  }

  async function handleReset(e) {
    e.preventDefault();
    clearErrors(); hideAlert();
    const email = el('reset_email')?.value?.trim() || '';
    if (!isValidEmail(email)) { fieldError('reset_email', 'E-mail invalide.'); return; }
    setLoading('resetBtn', true);
    try {
      await _apiReset({ email });
      showAlert('Si un compte existe pour cet e-mail, un lien a été envoyé.', 'success');
    } catch (err) {
      showAlert(err.message);
    } finally {
      setLoading('resetBtn', false);
    }
  }

  // ============================================================
  // INIT PAGE AUTH
  // ============================================================
  function initAuthPage() {
    clearErrors();
    hideAlert();
    redirectIfAuth();

    // Tabs
    document.querySelectorAll('.auth-tab').forEach(b => {
      b.addEventListener('click', () => switchTab(b.dataset.tab));
    });

    // Formulaires
    el('loginForm')?.addEventListener('submit', handleLogin);
    el('registerForm')?.addEventListener('submit', handleRegister);
    el('resetForm')?.addEventListener('submit', handleReset);

    // Toggle passwords
    document.querySelectorAll('[data-toggle-pw]').forEach(b => {
      b.addEventListener('click', () => {
        const [inp, btn] = b.dataset.togglePw.split(',').map(s => s.trim());
        togglePw(inp, btn);
      });
    });

    // Liens switch tabs
    document.querySelectorAll('[data-switch-tab]').forEach(a => {
      a.addEventListener('click', () => switchTab(a.dataset.switchTab));
      a.addEventListener('keydown', e => { if (e.key === 'Enter') switchTab(a.dataset.switchTab); });
    });

    // Lien mot de passe oublié
    el('forgotLink')?.addEventListener('click', () => switchTab('reset'));

    // Force mot de passe
    el('reg_pw')?.addEventListener('input', updatePwStrength);
  }

  // ============================================================
  // API PUBLIQUE
  // ============================================================
  return {
    initAuthPage,
    getSession,
    clearSession,
    requireAuth,
    saveSession,
    switchTab,
  };

})();

// Auto-démarrage
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', Auth.initAuthPage);
} else {
  Auth.initAuthPage();
}
