/* Cockpit — interface (vanilla JS + SortableJS). Données : /api (Pages Functions + D1). */
(function () {
  'use strict';

  // ---------------------------------------------------------------- état
  const TOKEN_KEY = 'cockpit.token';
  const PREFS_KEY = 'cockpit.prefs';
  let token = read(TOKEN_KEY) || '';
  let S = { projects: [], themes: [], items: [], activity: [] };
  let lastSig = '';
  let editing = false;
  let dragging = false;
  let sortables = [];
  let drawerCtx = null;
  let quietDrawer = false; // vrai quand la modif vient du panneau lui-même : ne pas le reconstruire
  const prefs = Object.assign({ hideDone: false, kind: 'all', quickKind: 'task', quickTheme: {}, openKids: {} }, safeJSON(read(PREFS_KEY)) || {});

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function write(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch (e) { /* stockage indisponible */ } }
  function safeJSON(s) { try { return JSON.parse(s); } catch (e) { return null; } }
  function savePrefs() { write(PREFS_KEY, JSON.stringify(prefs)); }
  function newId() { return (crypto.randomUUID ? crypto.randomUUID() : String(Math.random()).slice(2) + Date.now()).replace(/-/g, '').slice(0, 16); }
  function now() { return new Date().toISOString(); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }
  function safeUrl(u) { return /^https?:\/\//i.test(u || '') ? u : ''; }
  const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
  const MOIS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
  function fmtDate(iso) { const d = new Date(iso); return isNaN(d) ? '' : `${d.getDate()} ${MOIS[d.getMonth()]}`; }
  function fmtDay(iso) {
    const d = new Date(iso); if (isNaN(d)) return 'Sans date';
    const today = new Date(); const y = new Date(); y.setDate(today.getDate() - 1);
    if (d.toDateString() === today.toDateString()) return "Aujourd'hui";
    if (d.toDateString() === y.toDateString()) return 'Hier';
    return `${JOURS[d.getDay()]} ${d.getDate()} ${MOIS[d.getMonth()]}${d.getFullYear() !== today.getFullYear() ? ' ' + d.getFullYear() : ''}`;
  }
  function fmtTime(iso) { const d = new Date(iso); return isNaN(d) ? '' : d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }); }

  // ---------------------------------------------------------------- API
  async function api(method, path, body) {
    const res = await fetch('/api/' + path, {
      method,
      headers: Object.assign({ Authorization: 'Bearer ' + token }, body ? { 'content-type': 'application/json' } : {}),
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await res.json().catch(() => ({}));
    if (res.status === 401) { showLogin('Jeton refusé.'); throw new Error('401'); }
    if (!res.ok) throw new Error(data.error || ('Erreur ' + res.status));
    return data;
  }

  async function load(force) {
    try {
      const data = await api('GET', 'state');
      const sig = JSON.stringify([data.projects, data.themes, data.items, data.activity]);
      setSync('Synchronisé ' + fmtTime(data.at));
      if (!force && sig === lastSig) return;
      lastSig = sig;
      S = data;
      if (!editing && !dragging) render();
    } catch (e) {
      if (e.message !== '401') setSync('Hors ligne — ' + e.message, true);
      throw e;
    }
  }

  // Écritures optimistes : on modifie l'état local, on réaffiche, puis on envoie.
  function send(method, path, body) {
    setSync('Enregistrement…');
    return api(method, path, body)
      .then(r => { setSync('Enregistré ' + fmtTime(now())); lastSig = ''; return r; })
      .catch(e => {
        if (e.message !== '401') toast('Échec : ' + e.message + ' — rechargement');
        load(true).catch(() => {});
      });
  }

  function setSync(text, err) {
    const el = $('#sync'); if (!el) return;
    el.textContent = text; el.classList.toggle('err', !!err);
  }

  let toastTimer;
  function toast(msg) {
    const el = $('#toast');
    el.textContent = msg; el.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => { el.hidden = true; }, 3200);
  }

  // ---------------------------------------------------------------- accès données
  const byPos = (a, b) => (a.position - b.position) || String(a.created_at).localeCompare(String(b.created_at));
  const project = id => S.projects.find(p => p.id === id);
  const item = id => S.items.find(i => i.id === id);
  const theme = id => S.themes.find(t => t.id === id);
  const themesOf = pid => S.themes.filter(t => t.project_id === pid).sort(byPos);
  const kidsOf = id => S.items.filter(i => i.parent_id === id).sort(byPos);
  const workItems = pid => S.items.filter(i => i.project_id === pid && i.kind !== 'artifact');
  function descendants(id) {
    const out = []; const stack = [id];
    while (stack.length) { const cur = stack.pop(); for (const k of S.items) if (k.parent_id === cur) { out.push(k); stack.push(k.id); } }
    return out;
  }

  // ---------------------------------------------------------------- routage
  function route() {
    const h = location.hash.replace(/^#\/?/, '').split('/');
    if (h[0] === 'p' && h[1]) return { tab: decodeURIComponent(h[1]), sub: h[2] || 'plan' };
    return { tab: 'overview', sub: '' };
  }
  function go(tab, sub) { location.hash = tab === 'overview' ? '#/' : `#/p/${encodeURIComponent(tab)}/${sub || 'plan'}`; }
  window.addEventListener('hashchange', () => render());

  // ---------------------------------------------------------------- rendu
  function render() {
    closeSortables();
    renderTabs();
    const r = route();
    const view = $('#view');
    if (r.tab !== 'overview' && project(r.tab)) renderProject(view, project(r.tab), r.sub);
    else renderOverview(view);
    initSortables();
    if (drawerCtx && !quietDrawer) refreshDrawer();
    quietDrawer = false;
  }

  function renderTabs() {
    const r = route();
    const tabs = [`<button class="tab" role="tab" data-go="overview" aria-selected="${r.tab === 'overview'}">Vue d'ensemble</button>`];
    S.projects.filter(p => !p.archived).sort(byPos).forEach(p => {
      const open = workItems(p.id).filter(i => i.status !== 'done' && !i.parent_id).length;
      tabs.push(`<button class="tab" role="tab" data-go="${esc(p.id)}" aria-selected="${r.tab === p.id}" style="--tab-color:${esc(p.color)}">
        <span class="dot" style="background:${esc(p.color)}"></span>${esc(p.icon)} ${esc(p.name)}${open ? ` <span class="n">${open}</span>` : ''}</button>`);
    });
    tabs.push('<button class="tab add" data-action="new-project" title="Nouveau projet">＋ Projet</button>');
    $('#tabs').innerHTML = tabs.join('');
    const sel = $('#tabs [aria-selected="true"]');
    if (sel) sel.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }

  // ---------- vue d'ensemble
  function renderOverview(view) {
    const work = S.items.filter(i => i.kind !== 'artifact');
    const weekAgo = Date.now() - 7 * 864e5;
    const doing = work.filter(i => i.status === 'doing');
    const todo = work.filter(i => i.kind === 'task' && (i.status === 'todo' || i.status === 'blocked'));
    const ideas = work.filter(i => i.kind === 'idea' && i.status !== 'done');
    const doneWeek = S.items.filter(i => i.status === 'done' && i.done_at && new Date(i.done_at) > weekAgo);
    const focus = work.filter(i => i.status !== 'done' && (i.status === 'doing' || i.status === 'blocked' || i.priority === 1))
      .sort((a, b) => (a.status === 'doing' ? 0 : 1) - (b.status === 'doing' ? 0 : 1) || (a.priority || 9) - (b.priority || 9));

    const cards = S.projects.filter(p => !p.archived).sort(byPos).map(p => {
      const w = workItems(p.id).filter(i => i.kind === 'task');
      const done = w.filter(i => i.status === 'done').length;
      const pct = w.length ? Math.round(done / w.length * 100) : 0;
      const nIdeas = workItems(p.id).filter(i => i.kind === 'idea' && i.status !== 'done').length;
      const nDeliv = S.items.filter(i => i.project_id === p.id && i.kind === 'artifact').length;
      const nDoing = w.filter(i => i.status === 'doing').length;
      return `<button class="pcard" data-go="${esc(p.id)}" data-id="${esc(p.id)}" style="--pc:${esc(p.color)}">
        <div class="h"><span>${esc(p.icon)}</span><span>${esc(p.name)}</span></div>
        ${p.description ? `<div class="d">${esc(p.description)}</div>` : ''}
        <div class="s"><span><b>${w.length - done}</b> à faire</span><span><b>${nDoing}</b> en cours</span><span><b>${nIdeas}</b> idées</span><span><b>${nDeliv}</b> livrables</span></div>
        <div class="progress"><div class="bar"><i style="width:${pct}%"></i></div><span>${pct}%</span></div>
      </button>`;
    }).join('');

    view.innerHTML = `
      <h1 class="ov-title">Vue d'ensemble</h1>
      <p class="ov-dek">Tous tes projets. Clique un projet pour ouvrir son onglet ; glisse les cartes pour réordonner.</p>
      <div class="tiles">
        <div class="tile"><div class="n">${doing.length}</div><div class="l">en cours</div></div>
        <div class="tile"><div class="n">${todo.length}</div><div class="l">tâches à faire</div></div>
        <div class="tile"><div class="n">${ideas.length}</div><div class="l">idées en attente</div></div>
        <div class="tile"><div class="n">${doneWeek.length}</div><div class="l">faits ces 7 jours</div></div>
      </div>
      <div class="pgrid" id="pgrid">${cards}</div>
      <div class="cols">
        <section>
          <h2 class="section-h">Focus : en cours, bloqué, priorité haute</h2>
          ${focus.length ? focus.slice(0, 14).map(miniRow).join('') : '<div class="empty">Rien d\'urgent. Marque une tâche « en cours » ou « priorité haute » pour la voir ici.</div>'}
        </section>
        <section>
          <h2 class="section-h">Activité récente</h2>
          ${timeline(S.activity.slice(0, 14), true)}
        </section>
      </div>`;
  }

  function miniRow(i) {
    const p = project(i.project_id) || {};
    return `<div class="mini" data-open="${esc(i.id)}">
      <span class="pdot" style="background:${esc(p.color)}"></span>
      <div class="t">${esc(i.title)}<div class="item-sub">${statusChip(i)}${prioChip(i)}<span class="meta">${esc(p.name || '')}</span></div></div>
    </div>`;
  }

  // ---------- projet
  function renderProject(view, p, sub) {
    const nDeliv = S.items.filter(i => i.project_id === p.id && i.kind === 'artifact').length;
    const nHist = S.activity.filter(a => a.project_id === p.id).length;
    const head = `
      <div class="p-head">
        <div class="p-icon" data-action="project-settings" title="Réglages du projet">${esc(p.icon || '📁')}</div>
        <div class="p-main">
          <h1 class="p-name editable" data-edit="projects:${esc(p.id)}:name">${esc(p.name)}</h1>
          <div class="p-desc editable" data-edit="projects:${esc(p.id)}:description" data-placeholder="Ajouter une description…">${esc(p.description)}</div>
          ${p.repo ? `<div class="p-meta mono">${esc(p.repo)}</div>` : ''}
        </div>
        <button class="icon-btn" data-action="project-settings" title="Réglages du projet">⚙</button>
      </div>
      <div class="subtabs" role="tablist">
        <button class="subtab" data-sub="plan" aria-selected="${sub === 'plan'}">Plan d'action</button>
        <button class="subtab" data-sub="history" aria-selected="${sub === 'history'}">Historique<span class="n">${nHist}</span></button>
        <button class="subtab" data-sub="deliverables" aria-selected="${sub === 'deliverables'}">Livrables<span class="n">${nDeliv}</span></button>
      </div>`;

    let body = '';
    if (sub === 'history') body = timeline(S.activity.filter(a => a.project_id === p.id), false);
    else if (sub === 'deliverables') body = deliverables(p);
    else body = plan(p);
    view.innerHTML = head + body;
  }

  function plan(p) {
    const ths = themesOf(p.id);
    const themeIds = new Set(ths.map(t => t.id));
    const qTheme = prefs.quickTheme[p.id] && themeIds.has(prefs.quickTheme[p.id]) ? prefs.quickTheme[p.id] : '';
    const top = workItems(p.id).filter(i => !i.parent_id).sort(byPos);
    const inTheme = tid => top.filter(i => (tid ? i.theme_id === tid : !i.theme_id || !themeIds.has(i.theme_id)));

    const quick = `
      <form class="quick" data-form="quick" data-project="${esc(p.id)}">
        <div class="seg" role="group" aria-label="Type">
          <button type="button" data-kind="task" class="${prefs.quickKind === 'task' ? 'on' : ''}">☐ Tâche</button>
          <button type="button" data-kind="idea" class="${prefs.quickKind === 'idea' ? 'on' : ''}">💡 Idée</button>
        </div>
        <input type="text" name="title" placeholder="${prefs.quickKind === 'idea' ? 'Une idée, une piste d\'amélioration…' : 'Nouvelle tâche…'}" autocomplete="off" maxlength="500">
        <select name="theme" aria-label="Thématique">
          <option value="">Sans thématique</option>
          ${ths.map(t => `<option value="${esc(t.id)}" ${t.id === qTheme ? 'selected' : ''}>${esc(t.title)}</option>`).join('')}
        </select>
        <button class="btn primary small" type="submit">Ajouter</button>
      </form>
      <div class="toolbar">
        <div class="seg" role="group" aria-label="Filtre">
          <button type="button" data-filter="all" class="${prefs.kind === 'all' ? 'on' : ''}">Tout</button>
          <button type="button" data-filter="task" class="${prefs.kind === 'task' ? 'on' : ''}">Tâches</button>
          <button type="button" data-filter="idea" class="${prefs.kind === 'idea' ? 'on' : ''}">Idées</button>
        </div>
        <label><input type="checkbox" data-toggle="hideDone" ${prefs.hideDone ? 'checked' : ''}> Masquer ce qui est fait</label>
        <span class="spacer"></span>
        <button class="btn ghost small" data-action="collapse-all" data-project="${esc(p.id)}">Tout replier</button>
        <button class="btn ghost small" data-action="expand-all" data-project="${esc(p.id)}">Tout déplier</button>
      </div>`;

    const blocks = ths.map(t => themeBlock(p, t, inTheme(t.id))).join('');
    const loose = inTheme(null);
    const looseBlock = themeBlock(p, null, loose);

    return quick + `<div class="themes" id="themes" data-project="${esc(p.id)}">${blocks}${looseBlock}</div>
      <div class="add-theme"><button class="btn ghost" data-action="new-theme" data-project="${esc(p.id)}">＋ Nouvelle thématique</button></div>`;
  }

  function visible(i) {
    if (prefs.hideDone && i.status === 'done') return false;
    return true;
  }

  function themeBlock(p, t, list) {
    const all = list.concat(...list.map(i => descendants(i.id))).filter(i => i.kind === 'task');
    const done = all.filter(i => i.status === 'done').length;
    const pct = all.length ? Math.round(done / all.length * 100) : 0;
    const shown = list.filter(i => visible(i) && (prefs.kind === 'all' || i.kind === prefs.kind));
    const tid = t ? t.id : '';
    const collapsed = t && t.collapsed;
    return `
      <section class="theme ${t ? '' : 'loose'} ${collapsed ? 'collapsed' : ''}" ${t ? `data-theme-id="${esc(t.id)}"` : ''}>
        <div class="theme-head">
          ${t ? '<span class="handle theme-handle" title="Glisser pour déplacer">⋮⋮</span>' : '<span style="width:16px"></span>'}
          ${t ? `<button class="icon-btn chev" data-action="toggle-theme" data-id="${esc(t.id)}" aria-label="Replier / déplier">▾</button>` : ''}
          <div class="theme-title ${t ? 'editable' : ''}" ${t ? `data-edit="themes:${esc(t.id)}:title"` : ''}>${t ? esc(t.title) : 'Sans thématique'}</div>
          ${all.length ? `<div class="progress"><div class="bar"><i style="width:${pct}%"></i></div><span class="mono">${done}/${all.length}</span></div>` : ''}
          <button class="icon-btn" data-action="focus-add" title="Ajouter ici">＋</button>
          ${t ? `<button class="icon-btn" data-action="delete-theme" data-id="${esc(t.id)}" title="Supprimer la thématique">🗑</button>` : ''}
        </div>
        <div class="theme-body">
          <div class="list ${shown.length ? '' : 'empty-drop'}" data-project="${esc(p.id)}" data-theme="${esc(tid)}" data-parent="">
            ${shown.map(i => itemHtml(i, 0)).join('')}
          </div>
          <form class="add-inline" data-form="inline" data-project="${esc(p.id)}" data-theme="${esc(tid)}">
            <input type="text" name="title" placeholder="＋ Ajouter une tâche${t ? ' dans « ' + esc(t.title) + ' »' : ''}  (commence par « ? » pour une idée)" autocomplete="off" maxlength="500">
          </form>
        </div>
      </section>`;
  }

  function statusChip(i) {
    if (i.status === 'doing') return '<span class="chip doing" data-action="cycle-status" data-id="' + esc(i.id) + '">EN COURS</span>';
    if (i.status === 'blocked') return '<span class="chip blocked" data-action="cycle-status" data-id="' + esc(i.id) + '">BLOQUÉ</span>';
    return '';
  }
  function prioChip(i) {
    const lab = { 1: 'HAUTE', 2: 'MOYENNE', 3: 'BASSE' }[i.priority];
    return lab && i.status !== 'done' ? `<span class="chip p${i.priority}" data-action="cycle-prio" data-id="${esc(i.id)}" title="Priorité">${lab}</span>` : '';
  }

  function itemHtml(i, depth) {
    const kids = kidsOf(i.id).filter(visible);
    const allKids = descendants(i.id).filter(k => k.kind === 'task');
    const kidsDone = allKids.filter(k => k.status === 'done').length;
    const open = prefs.openKids[i.id] !== false;
    const isIdea = i.kind === 'idea';
    const lead = isIdea
      ? `<span class="bulb" data-action="idea-to-task" data-id="${esc(i.id)}" title="Idée — cliquer pour la transformer en tâche">💡</span>`
      : `<button class="check" data-action="toggle-done" data-id="${esc(i.id)}" aria-label="Terminer" title="${i.status === 'done' ? 'Rouvrir' : 'Marquer comme fait'}">✓</button>`;
    const sub = [
      statusChip(i),
      prioChip(i),
      i.source === 'claude' ? '<span class="chip claude">CLAUDE</span>' : '',
      allKids.length ? `<span class="meta mono">${kidsDone}/${allKids.length}</span>` : '',
      i.status === 'done' && i.done_at ? `<span class="meta">fait le ${fmtDate(i.done_at)}</span>` : '',
      safeUrl(i.url) ? `<a class="meta" href="${esc(i.url)}" target="_blank" rel="noopener">lien ↗</a>` : '',
    ].join('');
    const firstNote = (i.notes || '').trim();
    return `
      <div class="item-wrap" data-id="${esc(i.id)}">
        <div class="item ${i.status === 'done' ? 'done' : ''}">
          <span class="handle" title="Glisser pour déplacer">⋮⋮</span>
          ${lead}
          <div class="item-main">
            <div class="item-title editable" data-edit="items:${esc(i.id)}:title">${esc(i.title)}</div>
            <div class="item-sub">${sub}</div>
            ${firstNote && i.status !== 'done' ? `<div class="notes-peek">${esc(firstNote)}</div>` : ''}
          </div>
          <div class="item-actions">
            ${kids.length ? `<button class="icon-btn toggle-kids" data-action="toggle-kids" data-id="${esc(i.id)}" title="Sous-tâches">${open ? '▾' : '▸'}</button>` : ''}
            ${!isIdea ? `<button class="icon-btn" data-action="cycle-status" data-id="${esc(i.id)}" title="Statut : à faire → en cours → bloqué">◐</button>` : ''}
            <button class="icon-btn" data-action="cycle-prio" data-id="${esc(i.id)}" title="Priorité">⚑</button>
            ${depth < 3 ? `<button class="icon-btn" data-action="add-sub" data-id="${esc(i.id)}" title="Ajouter une sous-tâche">＋</button>` : ''}
            <button class="icon-btn" data-open="${esc(i.id)}" title="Détails, notes, déplacer, supprimer">⋯</button>
          </div>
        </div>
        <div class="list children" data-project="${esc(i.project_id)}" data-theme="${esc(i.theme_id || '')}" data-parent="${esc(i.id)}" ${open ? '' : 'hidden'}>
          ${kids.map(k => itemHtml(k, depth + 1)).join('')}
        </div>
      </div>`;
  }

  function timeline(events, withProject) {
    if (!events.length) return '<div class="empty">Rien dans l\'historique pour l\'instant.</div>';
    const ICON = { done: '✅', artifact: '📄', create: '➕', idea: '💡', start: '▶️', reopen: '↺', delete: '🗑', project: '📁' };
    const VERB = { done: 'Fait', artifact: 'Livrable', create: 'Ajouté', idea: 'Idée', start: 'Commencé', reopen: 'Rouvert', delete: 'Supprimé', project: '' };
    const days = [];
    events.forEach(e => {
      const key = fmtDay(e.at);
      if (!days.length || days[days.length - 1].key !== key) days.push({ key, list: [] });
      days[days.length - 1].list.push(e);
    });
    return days.map(d => `<div class="day"><h3>${esc(d.key)}</h3>${d.list.map(e => {
      const p = project(e.project_id);
      const it = e.item_id && item(e.item_id);
      return `<div class="ev" ${it ? `data-open="${esc(it.id)}" style="cursor:pointer"` : ''}>
        <span class="ic">${ICON[e.action] || '•'}</span>
        <div class="t">${VERB[e.action] ? `<span class="meta">${VERB[e.action]} · </span>` : ''}${esc(e.label)}
          ${withProject && p ? `<div class="p">${esc(p.icon)} ${esc(p.name)}</div>` : ''}</div>
        <span class="w">${e.source === 'claude' ? 'Claude · ' : ''}${fmtTime(e.at)}</span>
      </div>`;
    }).join('')}</div>`).join('');
  }

  function deliverables(p) {
    const list = S.items.filter(i => i.project_id === p.id && i.kind === 'artifact')
      .sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)));
    const form = `
      <form class="quick" data-form="deliverable" data-project="${esc(p.id)}">
        <input type="text" name="title" placeholder="Titre du livrable (article, doc, artefact…)" required maxlength="500">
        <input type="text" name="url" placeholder="https://…" style="flex:1 1 180px">
        <button class="btn primary small" type="submit">Ajouter</button>
      </form>`;
    if (!list.length) return form + '<div class="empty">Aucun livrable. Les artefacts et articles générés par Claude arrivent ici automatiquement.</div>';
    return form + list.map(i => `
      <div class="deliv">
        <span>📄</span>
        <div class="t">
          ${safeUrl(i.url) ? `<a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a>` : `<strong>${esc(i.title)}</strong>`}
          ${i.notes ? `<div class="n">${esc(i.notes)}</div>` : ''}
        </div>
        <span class="meta">${fmtDate(i.created_at)}</span>
        <button class="icon-btn" data-open="${esc(i.id)}" title="Modifier">⋯</button>
      </div>`).join('');
  }

  // ---------------------------------------------------------------- glisser-déposer
  function closeSortables() { sortables.forEach(s => s.destroy()); sortables = []; }
  function initSortables() {
    if (typeof Sortable === 'undefined') return;
    const common = { animation: 150, delay: 180, delayOnTouchOnly: true, forceFallback: true, fallbackTolerance: 4,
      onStart: () => { dragging = true; }, };
    $$('#view .list').forEach(el => {
      sortables.push(Sortable.create(el, Object.assign({}, common, {
        group: 'items', handle: '.handle', draggable: '.item-wrap', fallbackOnBody: true,
        swapThreshold: 0.6, emptyInsertThreshold: 12, onEnd: onItemDrop,
      })));
    });
    const th = $('#themes');
    if (th) sortables.push(Sortable.create(th, Object.assign({}, common, {
      handle: '.theme-handle', draggable: '.theme[data-theme-id]', onEnd: onThemeDrop,
    })));
    const pg = $('#pgrid');
    if (pg) sortables.push(Sortable.create(pg, Object.assign({}, common, { draggable: '.pcard', onEnd: onProjectDrop, delay: 120 })));
  }

  function onItemDrop(evt) {
    dragging = false;
    const lists = new Set([evt.from, evt.to]);
    const moves = [];
    lists.forEach(list => {
      const parent = list.dataset.parent || null;
      const themeId = parent ? ((item(parent) || {}).theme_id || null) : (list.dataset.theme || null);
      [...list.children].filter(c => c.dataset.id).forEach((c, idx) => {
        const it = item(c.dataset.id); if (!it) return;
        it.position = idx + 1; it.parent_id = parent; it.theme_id = themeId;
        moves.push({ id: it.id, position: idx + 1, parent_id: parent || '', theme_id: themeId || '' });
      });
    });
    if (evt.to.dataset.parent) prefs.openKids[evt.to.dataset.parent] = true;
    savePrefs();
    render();
    if (moves.length) send('POST', 'reorder', { table: 'items', moves });
  }
  function onThemeDrop() {
    dragging = false;
    const moves = $$('#themes > .theme[data-theme-id]').map((el, idx) => {
      const t = theme(el.dataset.themeId); if (t) t.position = idx + 1;
      return { id: el.dataset.themeId, position: idx + 1 };
    });
    render();
    send('POST', 'reorder', { table: 'themes', moves });
  }
  function onProjectDrop() {
    dragging = false;
    const moves = $$('#pgrid > .pcard').map((el, idx) => {
      const p = project(el.dataset.id); if (p) p.position = idx + 1;
      return { id: el.dataset.id, position: idx + 1 };
    });
    render();
    send('POST', 'reorder', { table: 'projects', moves });
  }

  // ---------------------------------------------------------------- mutations
  function addItem(data) {
    const siblings = S.items.filter(i => i.project_id === data.project_id && (i.parent_id || null) === (data.parent_id || null));
    const ts = now();
    const it = Object.assign({
      id: newId(), theme_id: null, parent_id: null, kind: 'task', notes: '', status: 'todo', priority: 0, url: '',
      source: 'moi', created_at: ts, updated_at: ts, done_at: null,
      position: siblings.reduce((m, i) => Math.max(m, i.position || 0), 0) + 1,
    }, data);
    if (it.kind === 'artifact') { it.status = 'done'; it.done_at = ts; }
    S.items.push(it);
    S.activity.unshift({ project_id: it.project_id, item_id: it.id, action: it.kind === 'artifact' ? 'artifact' : it.kind === 'idea' ? 'idea' : 'create', label: it.title, source: 'moi', at: ts });
    render();
    send('POST', 'items', it);
    return it;
  }

  function patch(table, id, data) {
    const coll = { items: S.items, themes: S.themes, projects: S.projects }[table];
    const obj = coll.find(x => x.id === id); if (!obj) return;
    if (table === 'items' && data.status && data.status !== obj.status) {
      data.done_at = data.status === 'done' ? now() : null;
      const action = data.status === 'done' ? 'done' : obj.status === 'done' ? 'reopen' : data.status === 'doing' ? 'start' : null;
      if (action) S.activity.unshift({ project_id: obj.project_id, item_id: id, action, label: obj.title, source: 'moi', at: now() });
    }
    Object.assign(obj, data, { updated_at: now() });
    const body = Object.assign({}, data); delete body.done_at;
    if (body.theme_id === null) body.theme_id = '';
    if (body.parent_id === null) body.parent_id = '';
    render();
    send('PATCH', `${table}/${encodeURIComponent(id)}`, body);
  }

  function removeItem(id) {
    const it = item(id); if (!it) return;
    const desc = descendants(id);
    if ((desc.length || (it.notes || '').length > 40) && !confirm(`Supprimer « ${it.title} »${desc.length ? ` et ses ${desc.length} sous-tâche(s)` : ''} ?`)) return;
    const gone = new Set([id, ...desc.map(d => d.id)]);
    S.items = S.items.filter(i => !gone.has(i.id));
    S.activity.unshift({ project_id: it.project_id, item_id: id, action: 'delete', label: it.title, source: 'moi', at: now() });
    closeDrawer();
    render();
    send('DELETE', `items/${encodeURIComponent(id)}`);
    toast('Supprimé : ' + it.title);
  }

  function cycleStatus(id) {
    const it = item(id); if (!it) return;
    const next = { todo: 'doing', doing: 'blocked', blocked: 'todo', done: 'todo' }[it.status] || 'todo';
    patch('items', id, { status: next });
  }
  function cyclePrio(id) {
    const it = item(id); if (!it) return;
    patch('items', id, { priority: { 0: 1, 1: 2, 2: 3, 3: 0 }[it.priority || 0] });
  }

  function newProject() {
    const name = prompt('Nom du nouveau projet ?');
    if (!name || !name.trim()) return;
    const ts = now();
    const colors = ['#33587A', '#BF5B44', '#D97B0A', '#2D7A6E', '#4739A8', '#2563EB', '#16A34A', '#DC2626', '#8B5CF6', '#0E7490'];
    const p = { id: newId(), name: name.trim().slice(0, 80), icon: '📁', color: colors[S.projects.length % colors.length],
      description: '', repo: '', archived: 0, position: S.projects.reduce((m, x) => Math.max(m, x.position || 0), 0) + 1, created_at: ts, updated_at: ts };
    S.projects.push(p);
    send('POST', 'projects', p);
    go(p.id, 'plan');
  }

  function newTheme(pid) {
    const title = prompt('Nom de la thématique ? (ex. Onboarding, Commercial, Bugs…)');
    if (!title || !title.trim()) return;
    const ts = now();
    const t = { id: newId(), project_id: pid, title: title.trim().slice(0, 200), description: '', collapsed: 0,
      position: themesOf(pid).reduce((m, x) => Math.max(m, x.position || 0), 0) + 1, created_at: ts, updated_at: ts };
    S.themes.push(t);
    prefs.quickTheme[pid] = t.id; savePrefs();
    render();
    send('POST', 'themes', t);
  }

  function deleteTheme(id) {
    const t = theme(id); if (!t) return;
    const n = S.items.filter(i => i.theme_id === id).length;
    if (!confirm(`Supprimer la thématique « ${t.title} » ?${n ? `\nSes ${n} élément(s) sont conservés et passent dans « Sans thématique ».` : ''}`)) return;
    S.themes = S.themes.filter(x => x.id !== id);
    S.items.forEach(i => { if (i.theme_id === id) i.theme_id = null; });
    render();
    send('DELETE', `themes/${encodeURIComponent(id)}`);
  }

  // ---------------------------------------------------------------- édition en ligne
  function startEdit(el) {
    if (el.isContentEditable) return;
    editing = true;
    const original = el.textContent;
    el.contentEditable = 'true';
    el.focus();
    const range = document.createRange(); range.selectNodeContents(el); range.collapse(false);
    const sel = getSelection(); sel.removeAllRanges(); sel.addRange(range);
    const finish = save => {
      el.removeEventListener('keydown', onKey); el.removeEventListener('blur', onBlur);
      el.contentEditable = 'false';
      editing = false;
      const val = el.textContent.replace(/\s+/g, ' ').trim();
      const [table, id, field] = el.dataset.edit.split(':');
      if (save && val !== original.trim() && (val || field === 'description')) patch(table, id, { [field]: val });
      else { el.textContent = original; render(); }
    };
    const onKey = e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); el.blur(); }
      if (e.key === 'Escape') { e.preventDefault(); finish(false); }
    };
    const onBlur = () => finish(true);
    el.addEventListener('keydown', onKey);
    el.addEventListener('blur', onBlur);
  }

  function openSubInput(parentId) {
    prefs.openKids[parentId] = true; savePrefs();
    render();
    const wrap = $(`.item-wrap[data-id="${CSS.escape(parentId)}"]`); if (!wrap) return;
    const list = wrap.querySelector(':scope > .list.children');
    list.hidden = false;
    const form = document.createElement('form');
    form.className = 'add-inline'; form.style.paddingLeft = '8px';
    form.innerHTML = '<input type="text" placeholder="Sous-tâche… (Entrée pour ajouter, Échap pour fermer)" maxlength="500">';
    list.after(form);
    const input = form.querySelector('input');
    editing = true;
    input.focus();
    form.addEventListener('submit', e => {
      e.preventDefault();
      const title = input.value.trim(); if (!title) return;
      const parent = item(parentId);
      editing = false;
      addItem({ project_id: parent.project_id, theme_id: parent.theme_id, parent_id: parentId, title });
      openSubInput(parentId);
    });
    input.addEventListener('keydown', e => { if (e.key === 'Escape') { editing = false; form.remove(); render(); } });
    input.addEventListener('blur', () => { setTimeout(() => { if (document.activeElement !== input) { editing = false; form.remove(); } }, 150); });
  }

  // ---------------------------------------------------------------- panneau détail
  function openDrawer(ctx) { drawerCtx = ctx; refreshDrawer(true); }
  function closeDrawer() { flushDrawer(); drawerCtx = null; $('#drawer').hidden = true; $('#drawerBackdrop').hidden = true; }

  function refreshDrawer(first) {
    const d = $('#drawer');
    if (!first && d.contains(document.activeElement) && /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) return;
    if (drawerCtx.type === 'item') {
      const it = item(drawerCtx.id); if (!it) return closeDrawer();
      const ths = themesOf(it.project_id);
      const parent = it.parent_id && item(it.parent_id);
      d.innerHTML = `
        <h2><span>${it.kind === 'idea' ? '💡 Idée' : it.kind === 'artifact' ? '📄 Livrable' : '☐ Tâche'}</span><button class="icon-btn" data-action="close-drawer" aria-label="Fermer">✕</button></h2>
        <label class="field"><span>Titre</span><input name="title" value="${esc(it.title)}" maxlength="500"></label>
        <div class="row2">
          <label class="field"><span>Type</span><select name="kind">
            <option value="task" ${it.kind === 'task' ? 'selected' : ''}>Tâche</option>
            <option value="idea" ${it.kind === 'idea' ? 'selected' : ''}>Idée</option>
            <option value="artifact" ${it.kind === 'artifact' ? 'selected' : ''}>Livrable</option></select></label>
          <label class="field"><span>Statut</span><select name="status">
            <option value="todo" ${it.status === 'todo' ? 'selected' : ''}>À faire</option>
            <option value="doing" ${it.status === 'doing' ? 'selected' : ''}>En cours</option>
            <option value="blocked" ${it.status === 'blocked' ? 'selected' : ''}>Bloqué</option>
            <option value="done" ${it.status === 'done' ? 'selected' : ''}>Fait</option></select></label>
        </div>
        <div class="row2">
          <label class="field"><span>Priorité</span><select name="priority">
            ${[[0, 'Aucune'], [1, 'Haute'], [2, 'Moyenne'], [3, 'Basse']].map(([v, l]) => `<option value="${v}" ${(it.priority || 0) === v ? 'selected' : ''}>${l}</option>`).join('')}</select></label>
          <label class="field"><span>Projet</span><select name="project_id">
            ${S.projects.slice().sort(byPos).map(p => `<option value="${esc(p.id)}" ${p.id === it.project_id ? 'selected' : ''}>${esc(p.icon)} ${esc(p.name)}</option>`).join('')}</select></label>
        </div>
        ${parent ? `<div class="stamp">Sous-tâche de « ${esc(parent.title)} » — <button class="btn ghost small" data-action="detach">Remonter au 1er niveau</button></div>` : `
        <label class="field"><span>Thématique</span><select name="theme_id">
          <option value="">Sans thématique</option>
          ${ths.map(t => `<option value="${esc(t.id)}" ${t.id === it.theme_id ? 'selected' : ''}>${esc(t.title)}</option>`).join('')}</select></label>`}
        <label class="field"><span>Lien</span><input name="url" value="${esc(it.url)}" placeholder="https://…"></label>
        <label class="field"><span>Notes</span><textarea name="notes" placeholder="Contexte, décisions, prochaines étapes…">${esc(it.notes)}</textarea></label>
        <div class="stamp">Créé le ${fmtDate(it.created_at)}${it.source === 'claude' ? ' par Claude' : ''} · modifié le ${fmtDate(it.updated_at)} ${fmtTime(it.updated_at)}${it.done_at ? ' · fait le ' + fmtDate(it.done_at) : ''}</div>
        <div class="foot">
          <button class="btn danger" data-action="delete-item" data-id="${esc(it.id)}">Supprimer</button>
          <button class="btn primary" data-action="close-drawer">Fermer</button>
        </div>`;
    } else if (drawerCtx.type === 'project') {
      const p = project(drawerCtx.id); if (!p) return closeDrawer();
      const colors = ['#33587A', '#BF5B44', '#D97B0A', '#2D7A6E', '#4739A8', '#2563EB', '#16A34A', '#DC2626', '#8B5CF6', '#0E7490', '#8B8680'];
      d.innerHTML = `
        <h2><span>Réglages du projet</span><button class="icon-btn" data-action="close-drawer" aria-label="Fermer">✕</button></h2>
        <div class="row2">
          <label class="field"><span>Nom</span><input name="name" value="${esc(p.name)}" maxlength="80"></label>
          <label class="field"><span>Icône (emoji)</span><input name="icon" value="${esc(p.icon)}" maxlength="8"></label>
        </div>
        <div class="field"><span>Couleur</span><div class="swatches">${colors.map(c => `<button type="button" data-color="${c}" class="${c === p.color ? 'on' : ''}" style="background:${c}" aria-label="${c}"></button>`).join('')}</div></div>
        <label class="field"><span>Description</span><input name="description" value="${esc(p.description)}"></label>
        <label class="field"><span>Dépôt GitHub</span><input name="repo" value="${esc(p.repo)}" placeholder="owner/repo"></label>
        <label class="field" style="flex-direction:row;align-items:center;gap:8px"><input type="checkbox" name="archived" ${p.archived ? 'checked' : ''} style="width:auto"> <span style="text-transform:none;letter-spacing:0;font-size:.88rem;font-weight:500">Archiver (masquer l'onglet)</span></label>
        <div class="foot">
          <button class="btn danger" data-action="delete-project" data-id="${esc(p.id)}">Supprimer le projet</button>
          <button class="btn primary" data-action="close-drawer">Fermer</button>
        </div>`;
    }
    d.hidden = false; $('#drawerBackdrop').hidden = false;
    if (first) { const f = d.querySelector('input'); if (f && window.matchMedia('(hover:hover)').matches) f.focus(); }
  }

  let drawerTimer, drawerPending = null;
  function flushDrawer() {
    clearTimeout(drawerTimer);
    if (drawerPending) { const f = drawerPending; drawerPending = null; f(); }
  }
  function onDrawerInput(e) {
    const el = e.target; if (!el.name || !drawerCtx) return;
    const table = drawerCtx.type === 'item' ? 'items' : 'projects';
    let val = el.type === 'checkbox' ? (el.checked ? 1 : 0) : el.value;
    if (el.name === 'priority') val = Number(val);
    if (el.name === 'title' || el.name === 'name') { if (!val.trim()) return; }
    const data = { [el.name]: val };
    if (el.name === 'project_id') { data.theme_id = null; data.parent_id = null; }
    if (el.name === 'theme_id' && !val) data.theme_id = null;
    const isText = el.tagName === 'TEXTAREA' || (el.tagName === 'INPUT' && el.type === 'text') || el.tagName === 'INPUT' && !el.type;
    const id = drawerCtx.id;
    const structural = ['project_id', 'theme_id', 'kind'].includes(el.name);
    const run = () => { quietDrawer = !structural; patch(table, id, data); };
    clearTimeout(drawerTimer); drawerPending = null;
    if (e.type === 'input' && isText) { drawerPending = run; drawerTimer = setTimeout(flushDrawer, 600); }
    else if (e.type === 'change') run();
    if (el.name === 'archived' && val) { closeDrawer(); go('overview'); }
  }

  // ---------------------------------------------------------------- événements
  document.addEventListener('click', e => {
    const t = e.target;
    const goEl = t.closest('[data-go]');
    if (goEl && !dragging) { go(goEl.dataset.go, 'plan'); return; }
    const sub = t.closest('[data-sub]');
    if (sub) { go(route().tab, sub.dataset.sub); return; }
    const openEl = t.closest('[data-open]');
    if (openEl && !t.closest('a')) { openDrawer({ type: 'item', id: openEl.dataset.open }); return; }
    const kindBtn = t.closest('.quick [data-kind]');
    if (kindBtn) { prefs.quickKind = kindBtn.dataset.kind; savePrefs(); render(); const i = $('.quick input[name=title]'); if (i) i.focus(); return; }
    const filt = t.closest('[data-filter]');
    if (filt) { prefs.kind = filt.dataset.filter; savePrefs(); render(); return; }
    const sw = t.closest('[data-color]');
    if (sw && drawerCtx && drawerCtx.type === 'project') { patch('projects', drawerCtx.id, { color: sw.dataset.color }); return; }
    const editEl = t.closest('[data-edit]');
    if (editEl && !t.closest('button')) { startEdit(editEl); return; }

    const a = t.closest('[data-action]'); if (!a) return;
    const id = a.dataset.id;
    switch (a.dataset.action) {
      case 'new-project': newProject(); break;
      case 'project-settings': openDrawer({ type: 'project', id: route().tab }); break;
      case 'new-theme': newTheme(a.dataset.project); break;
      case 'delete-theme': deleteTheme(id); break;
      case 'toggle-theme': { const th = theme(id); if (th) patch('themes', id, { collapsed: th.collapsed ? 0 : 1 }); break; }
      case 'collapse-all': case 'expand-all': {
        const v = a.dataset.action === 'collapse-all' ? 1 : 0;
        themesOf(a.dataset.project).filter(x => x.collapsed !== v).forEach(x => patch('themes', x.id, { collapsed: v }));
        break;
      }
      case 'focus-add': { const sec = a.closest('.theme'); if (sec.dataset.themeId) { const th = theme(sec.dataset.themeId); if (th && th.collapsed) { patch('themes', th.id, { collapsed: 0 }); } }
        const inp = $(`.theme${sec.dataset.themeId ? `[data-theme-id="${CSS.escape(sec.dataset.themeId)}"]` : '.loose'} .add-inline input`); if (inp) inp.focus(); break; }
      case 'toggle-done': { const it = item(id); if (it) patch('items', id, { status: it.status === 'done' ? 'todo' : 'done' }); break; }
      case 'idea-to-task': { const it = item(id); if (it && confirm(`Transformer l'idée « ${it.title} » en tâche ?`)) patch('items', id, { kind: 'task' }); break; }
      case 'cycle-status': cycleStatus(id); break;
      case 'cycle-prio': cyclePrio(id); break;
      case 'toggle-kids': prefs.openKids[id] = prefs.openKids[id] === false; savePrefs(); render(); break;
      case 'add-sub': openSubInput(id); break;
      case 'close-drawer': closeDrawer(); break;
      case 'delete-item': removeItem(id); break;
      case 'detach': { const it = item(drawerCtx.id); const par = it && item(it.parent_id); if (it) patch('items', it.id, { parent_id: null, theme_id: par ? par.theme_id : null }); break; }
      case 'delete-project': {
        const p = project(id); if (!p) break;
        const n = S.items.filter(i => i.project_id === id).length;
        if (!confirm(`Supprimer définitivement le projet « ${p.name} » et ses ${n} élément(s) ?\n(Pour juste le masquer, utilise « Archiver ».)`)) break;
        S.projects = S.projects.filter(x => x.id !== id);
        S.items = S.items.filter(i => i.project_id !== id);
        S.themes = S.themes.filter(x => x.project_id !== id);
        closeDrawer(); go('overview');
        send('DELETE', `projects/${encodeURIComponent(id)}`);
        break;
      }
    }
  });

  document.addEventListener('submit', e => {
    const f = e.target.closest('[data-form]'); if (!f) return;
    e.preventDefault();
    const input = f.querySelector('input[name=title]');
    let title = (input.value || '').trim(); if (!title) return;
    const pid = f.dataset.project;
    if (f.dataset.form === 'quick') {
      const themeId = f.querySelector('select[name=theme]').value || null;
      prefs.quickTheme[pid] = themeId || ''; savePrefs();
      addItem({ project_id: pid, theme_id: themeId, title, kind: prefs.quickKind });
      const again = $('.quick input[name=title]'); if (again) again.focus();
    } else if (f.dataset.form === 'inline') {
      let kind = 'task';
      if (title.startsWith('?')) { kind = 'idea'; title = title.slice(1).trim(); if (!title) return; }
      const themeId = f.dataset.theme || null;
      addItem({ project_id: pid, theme_id: themeId, title, kind });
      const sel = themeId ? `.theme[data-theme-id="${CSS.escape(themeId)}"] .add-inline input` : '.theme.loose .add-inline input';
      const again = $(sel); if (again) again.focus();
    } else if (f.dataset.form === 'deliverable') {
      const url = (f.querySelector('input[name=url]').value || '').trim();
      addItem({ project_id: pid, title, url, kind: 'artifact' });
    }
  });

  document.addEventListener('change', e => {
    if (e.target.matches('[data-toggle="hideDone"]')) { prefs.hideDone = e.target.checked; savePrefs(); render(); }
    if (e.target.closest('#drawer')) onDrawerInput(e);
  });
  document.addEventListener('input', e => { if (e.target.closest('#drawer')) onDrawerInput(e); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && drawerCtx) closeDrawer(); });
  $('#drawerBackdrop').addEventListener('click', closeDrawer);
  $('#logout').addEventListener('click', () => { write(TOKEN_KEY, null); token = ''; showLogin(); });

  // ---------------------------------------------------------------- démarrage
  function showLogin(msg) {
    $('#app').hidden = true; $('#login').hidden = false;
    const err = $('#loginError'); err.hidden = !msg; err.textContent = msg || '';
    $('#tokenInput').focus();
  }
  $('#loginForm').addEventListener('submit', async e => {
    e.preventDefault();
    token = $('#tokenInput').value.trim();
    try { await start(); write(TOKEN_KEY, token); } catch (err) { if (err.message !== '401') showLogin(err.message); }
  });

  async function start() {
    await load(true);
    $('#login').hidden = true; $('#app').hidden = false;
    render();
  }

  // Rafraîchissement : toutes les 20 s quand l'onglet est visible, et au retour sur l'onglet.
  setInterval(() => { if (token && !document.hidden && !editing && !dragging) load().catch(() => {}); }, 20000);
  document.addEventListener('visibilitychange', () => { if (token && !document.hidden) load().catch(() => {}); });

  if (token) start().catch(e => { if (e.message !== '401') { $('#login').hidden = true; $('#app').hidden = false; setSync(e.message, true); showLogin(e.message); } });
  else showLogin();
})();
