'use strict';

/**
 * APPMETIER PLATFORM — dashboard.js
 * Gestion du dashboard : applications, abonnements, profil
 */

const Dashboard = (() => {

  // ============================================================
  // CATALOGUE DES APPLICATIONS
  // ============================================================
  const APPS = [
    {
      id:       'facturation',
      label:    'FACTURATION',
      category: 'Gestion',
      desc:     'Factures, devis, relances. Tout votre cycle de facturation en un seul endroit.',
      url:      'apps/facturation/index.html',
      features: ['Factures & devis illimités', 'Gestion clients & produits', 'Export PDF', 'Tableau de bord CA'],
    },
    {
      id:       'vente',
      label:    'VENTE',
      category: 'Commercial',
      desc:     'Pipeline, prospects, relances. De la prise de contact à la signature.',
      url:      'apps/vente/index.html',
      features: ['Pipeline visuel', 'Historique des échanges', 'Relances automatiques', 'Rapports de performance'],
    },
    {
      id:       'stock',
      label:    'STOCK',
      category: 'Logistique',
      desc:     'Inventaire temps réel, alertes de seuil bas, gestion des fournisseurs.',
      url:      'apps/stock/index.html',
      features: ['Suivi temps réel', 'Alertes seuil bas', 'Gestion fournisseurs', 'Historique mouvements'],
    },
    {
      id:       'finance',
      label:    'FINANCE',
      category: 'Finance',
      desc:     'Trésorerie, dépenses, bilan simplifié. Votre santé financière en un coup d\'œil.',
      url:      'apps/finance/index.html',
      features: ['Tableau de trésorerie', 'Catégorisation auto', 'Export comptable', 'Bilan simplifié'],
    },
    {
      id:       'agenda',
      label:    'AGENDA',
      category: 'Organisation',
      desc:     'Rendez-vous en ligne, rappels automatiques, synchronisation calendrier.',
      url:      'apps/agenda/index.html',
      features: ['Prise de RDV en ligne', 'Rappels automatiques', 'Synchronisation calendrier', 'Pages de réservation'],
    },
    {
      id:       'crm',
      label:    'CRM',
      category: 'Relation client',
      desc:     'Historique client complet, notes, relances. Ne perdez plus aucune opportunité.',
      url:      'apps/crm/index.html',
      features: ['Fiche client 360°', 'Journal des interactions', 'Relances planifiées', 'Segments clients'],
    },
  ];

  // ============================================================
  // ÉTAT
  // ============================================================
  let currentUser  = null;
  let pendingAppId = null; // App en cours de souscription

  // ============================================================
  // SÉCURITÉ — XSS
  // ============================================================
  function esc(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ============================================================
  // TOAST
  // ============================================================
  function toast(msg, type = 'info', ms = 3500) {
    const c = document.getElementById('toastContainer');
    if (!c) return;
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.setAttribute('role', 'status');
    t.textContent = msg;
    c.appendChild(t);
    setTimeout(() => {
      t.classList.add('out');
      setTimeout(() => t.remove(), 320);
    }, ms);
  }

  // ============================================================
  // ABONNEMENTS — données locales (→ Supabase en prod)
  // ============================================================
function getSubs() {
    try {
      const userId = currentUser?.id || 'guest';
      return JSON.parse(localStorage.getItem(`appmetier_subs_${userId}`) || '[]');
    } catch { return []; }
  }

function saveSubs(subs) {
    try {
      const userId = currentUser?.id || 'guest';
      localStorage.setItem(`appmetier_subs_${userId}`, JSON.stringify(subs));
    } catch { toast('Erreur de sauvegarde.', 'error'); }
  }

  function isActive(appId) {
    return getSubs().some(s => s.app_id === appId && s.status === 'active');
  }

  function getSub(appId) {
    return getSubs().find(s => s.app_id === appId) || null;
  }

  /** Simule un appel Stripe + webhook en local. En prod : redirection Stripe Checkout. */
  function _mockSubscribe(appId) {
    return new Promise(resolve => setTimeout(() => {
      const subs  = getSubs();
      const idx   = subs.findIndex(s => s.app_id === appId);
      const sub   = {
        id:         crypto.randomUUID(),
        app_id:     appId,
        status:     'active',
        started_at: new Date().toISOString(),
        renews_at:  new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
      };
      if (idx >= 0) subs[idx] = sub; else subs.push(sub);
      saveSubs(subs);
      resolve(sub);
    }, 900));
  }

  function _mockCancel(appId) {
    return new Promise(resolve => setTimeout(() => {
      const subs = getSubs();
      const idx  = subs.findIndex(s => s.app_id === appId);
      if (idx >= 0) {
        subs[idx].status  = 'cancelled';
        subs[idx].ends_at = subs[idx].renews_at;
        subs[idx].renews_at = null;
        saveSubs(subs);
      }
      resolve();
    }, 700));
  }

  // ============================================================
  // NAVIGATION
  // ============================================================
  function showView(id) {
    document.querySelectorAll('.dash-view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.sidebar-item[data-view]').forEach(b => b.classList.remove('active'));
    document.getElementById('view-' + id)?.classList.add('active');
    document.querySelector(`.sidebar-item[data-view="${id}"]`)?.classList.add('active');
    closeSidebar();
  }

  function closeSidebar() {
    document.getElementById('dashSidebar')?.classList.remove('open');
    document.getElementById('sidebarOverlay')?.classList.remove('visible');
  }

  // ============================================================
  // RENDER HEADER
  // ============================================================
  function renderHeader() {
    const initials = ((currentUser.prenom || '')[0] || '') + ((currentUser.nom || '')[0] || '');
    const av  = document.getElementById('userAvatar');
    const nm  = document.getElementById('userName');
    const ddN = document.getElementById('ddName');
    const ddE = document.getElementById('ddEmail');
    if (av)  av.textContent  = initials.toUpperCase();
    if (nm)  nm.textContent  = currentUser.prenom || currentUser.email;
    if (ddN) ddN.textContent = `${currentUser.prenom || ''} ${currentUser.nom || ''}`.trim();
    if (ddE) ddE.textContent = currentUser.email;
  }

  // ============================================================
  // RENDER APPLICATIONS
  // ============================================================
  function renderApps(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = APPS.map(app => buildCard(app)).join('');
  }

  function buildCard(app) {
    const active   = isActive(app.id);
    const sub      = getSub(app.id);
    const renewTxt = sub?.renews_at
      ? new Date(sub.renews_at).toLocaleDateString('fr-FR')
      : null;

    const foot = active
      ? `<span class="status-dot active">Actif</span>
         <button class="app-card-open"
           onclick="Dashboard.launchApp('${esc(app.id)}')"
           type="button"
           aria-label="Ouvrir ${esc(app.label)}">
           Ouvrir
         </button>`
      : `<span class="status-dot inactive">Non activé</span>
         <button class="app-card-activate"
           onclick="Dashboard.openSubscribeModal('${esc(app.id)}')"
           type="button"
           aria-label="Activer ${esc(app.label)}">
           Activer
         </button>`;

    const lockIcon = !active
      ? `<svg class="app-lock-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
           <rect x="3" y="8" width="12" height="9" rx="2" stroke="#1a1814" stroke-width="1.4"/>
           <path d="M6 8V5.5a3 3 0 0 1 6 0V8" stroke="#1a1814" stroke-width="1.4"/>
         </svg>`
      : '';

    const renewInfo = active && renewTxt
      ? `<div style="font-size:10px;color:var(--ink-muted);font-weight:300;margin-top:2px;">Renouvellement le ${renewTxt}</div>`
      : '';

    return `
      <div class="app-card ${active ? 'unlocked' : 'locked'}"
           data-app="${esc(app.id)}"
           role="article"
           aria-label="Application ${esc(app.label)}">
        ${lockIcon}
        <div>
          <div class="app-card-tag">${esc(app.category)}</div>
          <div class="app-card-name">${esc(app.label)}</div>
        </div>
        <div class="app-card-desc">${esc(app.desc)}</div>
        <div class="app-card-foot">
          <div>${foot}${renewInfo}</div>
        </div>
      </div>`;
  }

  // ============================================================
  // RENDER ABONNEMENTS
  // ============================================================
  function renderSubs() {
    const el = document.getElementById('subsList');
    if (!el) return;
    const subs = getSubs();
    if (subs.length === 0) {
      el.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">—</div>
          <div class="empty-state-title">Aucun abonnement actif</div>
          <div class="empty-state-desc">Activez vos premières applications depuis la vue principale.</div>
          <button class="btn btn-primary" onclick="Dashboard.showView('apps')" type="button">
            Voir les applications
          </button>
        </div>`;
      return;
    }
    el.innerHTML = subs.map(sub => {
      const app     = APPS.find(a => a.id === sub.app_id);
      if (!app) return '';
      const active  = sub.status === 'active';
      const start   = new Date(sub.started_at).toLocaleDateString('fr-FR');
      const renew   = sub.renews_at ? new Date(sub.renews_at).toLocaleDateString('fr-FR') : null;
      const ends    = sub.ends_at   ? new Date(sub.ends_at).toLocaleDateString('fr-FR')   : null;
      return `
        <div class="sub-row">
          <div class="sub-row-info">
            <div class="sub-row-name">${esc(app.label)}</div>
            <div class="sub-row-meta">
              Depuis le ${start} ·
              ${active
                ? `Renouvellement <strong>${renew}</strong>`
                : `<span style="color:var(--red);">Résiliation au ${ends}</span>`}
            </div>
          </div>
          <div class="sub-row-actions">
            <span class="status-dot ${active ? 'active' : 'inactive'}">${active ? 'Actif' : 'Résilié'}</span>
            ${active
              ? `<button class="btn btn-outline btn-sm"
                   onclick="Dashboard.confirmCancel('${esc(app.id)}')"
                   type="button">Résilier</button>
                 <button class="btn btn-primary btn-sm"
                   onclick="Dashboard.launchApp('${esc(app.id)}')"
                   type="button">Ouvrir</button>`
              : `<button class="btn btn-primary btn-sm"
                   onclick="Dashboard.openSubscribeModal('${esc(app.id)}')"
                   type="button">Réactiver</button>`}
          </div>
        </div>`;
    }).join('');
  }

  // ============================================================
  // RENDER PROFIL
  // ============================================================
  function renderProfile() {
    const fields = {
      prof_prenom: currentUser.prenom || '',
      prof_nom:    currentUser.nom    || '',
      prof_email:  currentUser.email  || '',
      prof_since:  new Date(currentUser.created_at).toLocaleDateString('fr-FR'),
    };
    Object.entries(fields).forEach(([id, val]) => {
      const el = document.getElementById(id);
      if (el) el.value = val;
    });
  }

  // ============================================================
  // ACTIONS
  // ============================================================
  function launchApp(appId) {
    if (!isActive(appId)) { openSubscribeModal(appId); return; }
    const app = APPS.find(a => a.id === appId);
    if (app) window.location.href = app.url;
  }

  function openSubscribeModal(appId) {
    const app    = APPS.find(a => a.id === appId);
    if (!app) return;
    pendingAppId = appId;
    const active = isActive(appId);
    const sub    = getSub(appId);

    document.getElementById('subModalCat').textContent   = app.category;
    document.getElementById('subModalName').textContent  = app.label;
    document.getElementById('subModalName2').textContent = app.label;
    document.getElementById('subModalMeta').textContent  = active
      ? `Actif depuis le ${new Date(sub.started_at).toLocaleDateString('fr-FR')}`
      : 'Non activé';

    document.getElementById('subModalFeatures').innerHTML = app.features.map(f => `
      <div class="sub-modal-feature">
        <div class="sub-modal-check">✓</div>
        <span>${esc(f)}</span>
      </div>`).join('');

    const btn = document.getElementById('subModalBtn');
    btn.disabled = false;
    if (active) {
      btn.textContent = 'Ouvrir l\'application';
      btn.onclick = () => { closeModal('subModal'); launchApp(appId); };
    } else {
      btn.textContent = 'Activer cette application';
      btn.onclick = () => handleSubscribe(appId);
    }
    document.getElementById('subModalNote').textContent = active
      ? 'Votre application est active.'
      : 'Sans engagement · Résiliable à tout moment';

    openModal('subModal');
  }

  async function handleSubscribe(appId) {
    const btn = document.getElementById('subModalBtn');
    const app = APPS.find(a => a.id === appId);
    if (!btn || !app) return;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Activation…';
    try {
      // En prod : window.location.href = `/api/checkout?app=${appId}`
      await _mockSubscribe(appId);
      closeModal('subModal');
      renderAll();
      toast(`${app.label} activé avec succès.`, 'success');
    } catch {
      btn.disabled = false;
      btn.textContent = 'Activer cette application';
      toast('Erreur lors de l\'activation. Réessayez.', 'error');
    }
  }

  function confirmCancel(appId) {
    const app = APPS.find(a => a.id === appId);
    const sub = getSub(appId);
    if (!app || !sub) return;
    const renew = sub.renews_at ? new Date(sub.renews_at).toLocaleDateString('fr-FR') : '—';
    document.getElementById('cancelText').innerHTML =
      `Résilier <strong>${esc(app.label)}</strong> ? Votre accès reste actif jusqu'au <strong>${renew}</strong>.`;
    const btn = document.getElementById('cancelConfirmBtn');
    btn.disabled = false;
    btn.textContent = 'Confirmer la résiliation'; /* <-- LIGNE AJOUTÉE : On remet le texte à neuf */
    btn.onclick = () => handleCancel(appId);
    
    openModal('cancelModal');
    }

  async function handleCancel(appId) {
    const btn = document.getElementById('cancelConfirmBtn');
    const app = APPS.find(a => a.id === appId);
    if (!btn || !app) return;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span>';
    try {
      await _mockCancel(appId);
      closeModal('cancelModal');
      renderAll();
      toast(`${app.label} résilié. Accès maintenu jusqu'à la fin de la période.`, 'info', 5000);
    } catch {
      btn.disabled = false;
      btn.textContent = 'Confirmer la résiliation';
      toast('Erreur. Contactez le support.', 'error');
    }
  }

  function saveProfile(e) {
    e.preventDefault();
    const prenom = document.getElementById('prof_prenom')?.value?.trim();
    const nom    = document.getElementById('prof_nom')?.value?.trim();
    if (!prenom || !nom) { toast('Prénom et nom requis.', 'error'); return; }
    currentUser.prenom = prenom;
    currentUser.nom    = nom;
    Auth.saveSession(currentUser);
    // Persister dans le store users
    try {
      const users = JSON.parse(localStorage.getItem('appmetier_users_v1') || '[]');
      const idx   = users.findIndex(u => u.id === currentUser.id);
      if (idx >= 0) { users[idx].prenom = prenom; users[idx].nom = nom; }
      localStorage.setItem('appmetier_users_v1', JSON.stringify(users));
    } catch {}
    renderHeader();
    toast('Profil mis à jour.', 'success');
  }

  // ============================================================
  // MODALES
  // ============================================================
  function openModal(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.add('open');
    el.setAttribute('aria-hidden', 'false');
    setTimeout(() => {
      const first = el.querySelector('button:not([disabled]), input');
      if (first) first.focus();
    }, 120);
  }

  function closeModal(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove('open');
    el.setAttribute('aria-hidden', 'true');
  }

  // ============================================================
  // USER DROPDOWN
  // ============================================================
  function toggleDropdown() {
    const dd = document.getElementById('userDropdown');
    const btn = document.getElementById('userBtn');
    const open = dd?.classList.contains('open');
    dd?.classList.toggle('open', !open);
    btn?.setAttribute('aria-expanded', String(!open));
  }

  // ============================================================
  // RENDER ALL
  // ============================================================
  function renderAll() {
    renderHeader();
    renderApps('appsGrid');
    renderSubs();
    renderProfile();
  }

  // ============================================================
  // INIT
  // ============================================================
  function init() {
    currentUser = Auth.requireAuth();
    if (!currentUser) return;

    // Sidebar navigation
    document.querySelectorAll('.sidebar-item[data-view]').forEach(btn => {
      btn.addEventListener('click', () => showView(btn.dataset.view));
    });

    // Burger mobile
    document.getElementById('burgerBtn')?.addEventListener('click', () => {
      document.getElementById('dashSidebar')?.classList.toggle('open');
      document.getElementById('sidebarOverlay')?.classList.toggle('visible');
    });
    document.getElementById('sidebarOverlay')?.addEventListener('click', closeSidebar);

    // Dropdown user
    document.getElementById('userBtn')?.addEventListener('click', e => {
      e.stopPropagation();
      toggleDropdown();
    });
    document.addEventListener('click', e => {
      if (!e.target.closest('#userBtn') && !e.target.closest('#userDropdown')) {
        document.getElementById('userDropdown')?.classList.remove('open');
      }
    });

    // Déconnexion
    document.getElementById('logoutBtn')?.addEventListener('click', () => {
      Auth.clearSession();
      window.location.href = '/';
    });
    document.getElementById('ddLogoutBtn')?.addEventListener('click', () => {
      Auth.clearSession();
      window.location.href = '/';
    });

    // Fermeture modales
    document.querySelectorAll('.modal-overlay').forEach(m => {
      m.addEventListener('click', e => { if (e.target === m) closeModal(m.id); });
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.open').forEach(m => closeModal(m.id));
      }
    });

    // Profil
    document.getElementById('profileForm')?.addEventListener('submit', saveProfile);

    renderAll();
    showView('apps');
  }

  // ============================================================
  // API PUBLIQUE
  // ============================================================
  return {
    init,
    showView,
    launchApp,
    openSubscribeModal,
    confirmCancel,
    closeModal,
    renderAll,
  };

})();

document.addEventListener('DOMContentLoaded', Dashboard.init);
