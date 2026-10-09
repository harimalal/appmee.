/* Routeur, authentification et coque de l'application (cliente + coach) */
(function () {
  'use strict';
  const D = window.DECLIC, S = window.Store, E = window.Engine, U = window.UI;
  const { esc } = U;
  const A = window.Actions;
  const IMP = 'declic.impersonate';

  const App = {
    query: '', tab: 'queue',
    session() { return S.session.get(); },
    impersonated() { try { return sessionStorage.getItem(IMP); } catch (e) { return null; } },
    clientId() { const s = App.session(); return (s && s.role === 'coach' && App.impersonated()) || (s && s.clientId); },
    impersonate(id) { sessionStorage.setItem(IMP, id); location.hash = '#/me'; App.render(); },
    stopImpersonate() { sessionStorage.removeItem(IMP); location.hash = '#/admin'; App.render(); },
    render() { route(); },
  };
  window.App = App;

  const $ = (s, r) => (r || document).querySelector(s);
  // Change de page ; si le hash est inchangé, force le rendu (évite un double rendu asynchrone)
  function go(h) { if (location.hash === h) route(); else location.hash = h; }

  /* ---------- Connexion ---------- */
  function loginView() {
    const empty = !S.get().clients.length;
    $('#app').innerHTML = `<main class="auth"><div class="auth-card"><a href="index.html" class="brand-name big">Déclic</a><p class="muted">${esc(D.BRAND.tagline)}</p>
    <div class="tabs"><button class="on" data-m="login">Connexion</button><button data-m="reg">Créer mon espace</button></div>
    <form id="lf" novalidate><div class="fld"><label class="lbl" for="le">Email</label><input class="inp" id="le" type="email" autocomplete="username" required></div><div class="fld"><label class="lbl" for="lp">Mot de passe</label><input class="inp" id="lp" type="password" autocomplete="current-password" required></div><div class="fld reg" hidden><label class="lbl" for="lpr">Prénom</label><input class="inp" id="lpr" autocomplete="given-name"></div><div class="err" id="le-err" role="alert"></div><button class="btn block" id="lsub">Se connecter</button></form>
    <div class="demo"><p class="muted">🧪 Mode démonstration</p><div class="row wrap"><button class="btn ghost sm" id="d-coach">Entrer comme Claire (coach)</button><button class="btn ghost sm" id="d-cli">Voir une cliente</button></div>${empty ? '<p class="muted">Aucune donnée : la démo les crée en 2 secondes.</p>' : ''}</div></div></main>`;
    let mode = 'login';
    document.querySelectorAll('.tabs [data-m]').forEach((b) => (b.onclick = () => {
      mode = b.dataset.m; document.querySelectorAll('.tabs button').forEach((x) => x.classList.toggle('on', x === b));
      $('.reg').hidden = mode !== 'reg'; $('#lsub').textContent = mode === 'reg' ? 'Créer mon espace' : 'Se connecter'; $('#le-err').textContent = '';
    }));
    $('#lf').onsubmit = async (e) => {
      e.preventDefault(); const err = $('#le-err'); err.textContent = '';
      const em = $('#le').value, pw = $('#lp').value;
      try {
        if (mode === 'reg') {
          if (pw.length < 8) throw new Error('Mot de passe : 8 caractères minimum.');
          const pr = $('#lpr').value.trim(); if (!pr) throw new Error('Indique ton prénom.');
          await E.createLead({ prenom: pr, email: em, source: 'Création de compte', password: pw });
        }
        await S.login(em, pw); go('#/');
      } catch (x) { err.textContent = x.message; }
    };
    const demo = async (who) => {
      if (!S.get().seeded) { $('#d-coach').disabled = $('#d-cli').disabled = true; await window.Seed.run(); }
      if (who === 'coach') await S.login(S.get().settings.email, 'declic2026'); else await S.login('amelie@exemple.fr', 'demo1234');
      go('#/');
    };
    $('#d-coach').onclick = () => demo('coach'); $('#d-cli').onclick = () => demo('cli');
  }

  /* ---------- Coque ---------- */
  function shell(role, active, inner) {
    const db = () => S.get();
    const s = App.session(); const imp = role === 'client' && s.role === 'coach';
    const nav = role === 'coach'
      ? [['admin', 'Tableau de bord'], ['admin/todo', 'À faire' + (window.AdminViews.badgeCount() ? ` <span class="pill-n">${window.AdminViews.badgeCount()}</span>` : '')], ['admin/pipeline', 'Pipeline'], ['admin/clients', 'Clientes'], ['admin/launch', 'Mise en route'], ['admin/library', 'Bibliothèque'], ['admin/emails', 'Emails'], ['admin/finance', 'Finances'], ['admin/settings', 'Réglages']]
      : [['me', 'Mon parcours'], ['me/ressources', 'Mes ressources'], ['me/seances', 'Mes séances'], ['me/factures', 'Paiements']];
    const c = role === 'client' ? S.clientById(App.clientId()) : null;
    $('#app').innerHTML = `${imp ? `<div class="imp">👁 Tu vois l’espace de <strong>${esc(c ? E.fullName(c) : '')}</strong> <button class="btn sm" id="imp-stop">Retour à mon espace</button></div>` : ''}
    <header class="top"><a class="brand-name" href="${role === 'coach' ? '#/admin' : '#/me'}">Déclic</a><nav class="nav" aria-label="Navigation">${nav.map(([h, l]) => `<a href="#/${h}" class="${active === h ? 'on' : ''}">${l}</a>`).join('')}</nav><div class="who"><span>${esc(role === 'coach' ? db().settings.owner : (c ? c.prenom : ''))}</span><button class="link" id="logout">Déconnexion</button></div></header>
    <main id="view" class="wrap">${inner}</main>`;
    $('#logout').onclick = () => { S.session.clear(); sessionStorage.removeItem(IMP); go('#/'); };
    const st = $('#imp-stop'); if (st) st.onclick = App.stopImpersonate;
  }

  function route() {
    const s = App.session();
    if (!s) return loginView();
    const parts = (location.hash.replace(/^#\/?/, '') || '').split('/').filter(Boolean);
    const isCoach = s.role === 'coach';
    const wantsMe = parts[0] === 'me';
    if (isCoach && !wantsMe) {
      const AV = window.AdminViews; const sub = parts[1];
      let key = 'admin', html;
      if (!sub) html = AV.dashboard();
      else if (sub === 'todo') { key = 'admin/todo'; html = AV.todoView(); }
      else if (sub === 'pipeline') { key = 'admin/pipeline'; html = AV.pipeline(); }
      else if (sub === 'clients') { key = 'admin/clients'; html = parts[2] ? AV.clientDetail(parts[2]) : AV.clientsList(); }
      else if (sub === 'launch') { key = 'admin/launch'; html = AV.launch(); }
      else if (sub === 'library') { key = 'admin/library'; html = AV.library(); }
      else if (sub === 'emails') { key = 'admin/emails'; html = AV.emails(); }
      else if (sub === 'finance') { key = 'admin/finance'; html = AV.finance(); }
      else if (sub === 'settings') { key = 'admin/settings'; html = AV.settings(); }
      else html = AV.dashboard();
      shell('coach', key, html); AV.bindSettings($('#view')); return;
    }
    const c = S.clientById(App.clientId());
    if (!c) { S.session.clear(); return loginView(); }
    const CV = window.ClientViews; const sub = parts[1];
    const map = { ressources: CV.ressources, seances: CV.seances, factures: CV.factures };
    shell('client', sub && map[sub] ? 'me/' + sub : 'me', (sub && map[sub] ? map[sub] : CV.parcours)(c));
  }

  /* ---------- Délégation d'événements ---------- */
  function wire() {
    document.addEventListener('click', (e) => {
      const el = e.target.closest('[data-act]'); if (!el || el.matches('input[type=checkbox],input.search,form')) return;
      const fn = A[el.dataset.act]; if (fn) { e.preventDefault(); fn(el.dataset, el); }
    });
    document.addEventListener('change', (e) => {
      const el = e.target.closest('input[type=checkbox][data-act]'); if (el && A[el.dataset.act]) A[el.dataset.act](el.dataset, el);
    });
    document.addEventListener('input', (e) => { const el = e.target; if (el.matches && el.matches('input.search[data-act]') && A[el.dataset.act]) A[el.dataset.act](el.dataset, el); });
    document.addEventListener('submit', (e) => {
      const f = e.target.closest('form[data-act="note"]'); if (!f) return;
      e.preventDefault(); const v = f.n.value; E.addNote(f.dataset.c, v); App.render();
    });
    window.addEventListener('hashchange', route);
  }

  async function start() {
    S.load(); await S.ensureCoach();
    await E.tick();
    route();
  }

  document.addEventListener('DOMContentLoaded', async () => {
    wire(); await start();
    setInterval(async () => { if (await E.tick() && !document.querySelector('.modal-wrap')) route(); }, 60000);
  });
})();
