/* Master IA — interface. Vanilla JS, aucune dépendance. */
(() => {
  'use strict';

  const API = '/api/master-ia';
  const KEY = 'masterIA.token';
  const $ = (s, r = document) => r.querySelector(s);
  const state = { taxonomy: null, resources: [] };

  const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const safeUrl = (u) => (/^https?:\/\//i.test(u) ? u : '#');

  const store = {
    get() { try { return localStorage.getItem(KEY) || ''; } catch { return ''; } },
    set(v) { try { v ? localStorage.setItem(KEY, v) : localStorage.removeItem(KEY); } catch { /* stockage indisponible */ } },
  };

  function toast(msg, err = false) {
    const t = $('#toast');
    t.textContent = msg;
    t.className = 'show' + (err ? ' err' : '');
    clearTimeout(toast.t);
    toast.t = setTimeout(() => (t.className = ''), 3500);
  }

  async function api(path, { method = 'GET', body } = {}) {
    const res = await fetch(API + path, {
      method,
      headers: { authorization: 'Bearer ' + store.get(), ...(body ? { 'content-type': 'application/json' } : {}) },
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await res.json().catch(() => ({}));
    if (res.status === 401) { lock(); throw new Error('Jeton invalide'); }
    if (!res.ok) throw new Error(data.error || `Erreur ${res.status}`);
    return data;
  }

  /* ---------- Accès ---------- */
  function lock() {
    store.set('');
    $('#gate').hidden = false;
    document.querySelectorAll('.tab').forEach((t) => (t.hidden = true));
    $('#logout').hidden = true;
  }
  function unlock() {
    $('#gate').hidden = true;
    $('#logout').hidden = false;
    showTab(document.querySelector('#tabs [aria-selected="true"]').dataset.tab);
  }
  $('#gate-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    store.set($('#token').value.trim());
    try { await boot(); } catch (err) { toast(err.message, true); }
  });
  $('#logout').addEventListener('click', lock);

  function showTab(name) {
    document.querySelectorAll('#tabs button').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.tab === name)));
    document.querySelectorAll('.tab').forEach((t) => (t.hidden = t.id !== 'tab-' + name));
    if (name === 'library') loadLibrary();
  }
  $('#tabs').addEventListener('click', (e) => { const b = e.target.closest('button'); if (b && $('#gate').hidden) showTab(b.dataset.tab); });

  /* ---------- Bibliothèque ---------- */
  const scoreClass = (s) => (s >= 8 ? 's-hi' : s >= 5 ? 's-mid' : 's-lo');
  const dur = (m) => (m ? (m >= 60 ? `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, '0')}` : `${m} min`) : '');

  function card(r) {
    const t = state.taxonomy;
    const meta = [t.sources[r.source] || r.source, r.type, r.level !== 'tous' ? r.level : '', r.language !== 'autre' ? r.language.toUpperCase() : '', dur(r.duration_minutes), r.author]
      .filter(Boolean).map(esc).join(' · ');
    return `<article class="card" data-id="${esc(r.id)}">
      <div class="score ${scoreClass(r.score)}" title="Note de pertinence">${r.score}<small>/10</small></div>
      <div>
        <h3><a href="${esc(safeUrl(r.url))}" target="_blank" rel="noopener noreferrer">${esc(r.title)}</a></h3>
        <div class="meta"><span class="chip cat">${esc(r.category)}</span><span>${meta}</span>${r.confidence === 'faible' ? '<span class="chip warn" title="Peu d\'informations disponibles : note à prendre avec prudence">note peu fiable</span>' : ''}</div>
        <p class="desc">${esc(r.description)}</p>
        ${r.score_rationale ? `<p class="why">${esc(r.score_rationale)}</p>` : ''}
        <div class="meta">${r.tags.map((x) => `<span class="chip tag">${esc(x)}</span>`).join('')}</div>
        <div class="actions">
          <select data-act="status" aria-label="Statut">${t.statuses.map((s) => `<option value="${s}"${s === r.status ? ' selected' : ''}>${statusLabel(s)}</option>`).join('')}</select>
          <button class="ghost" data-act="rescore">Re-noter</button>
          <button class="ghost danger" data-act="delete">Supprimer</button>
        </div>
        <details><summary>Notes personnelles</summary>
          <textarea rows="3" data-field="notes" placeholder="Ce que j'en retiens…">${esc(r.notes)}</textarea>
          <button class="ghost" data-act="save-notes">Enregistrer</button>
        </details>
      </div></article>`;
  }
  const statusLabel = (s) => ({ a_voir: 'À voir', en_cours: 'En cours', termine: 'Terminé', abandonne: 'Abandonné' }[s] || s);

  function filters() {
    return new URLSearchParams(Object.entries({
      q: $('#f-q').value.trim(), category: $('#f-category').value, source: $('#f-source').value,
      status: $('#f-status').value, min_score: $('#f-score').value, sort: $('#f-sort').value,
    }).filter(([, v]) => v)).toString();
  }

  async function loadLibrary() {
    try {
      const { resources, stats } = await api('/resources?' + filters());
      state.resources = resources;
      $('#stats').innerHTML = [
        [stats.total, 'ressources'], [stats.avg_score + '/10', 'note moyenne'],
        [stats.by_status.a_voir || 0, 'à voir'], [stats.by_status.termine || 0, 'terminées'],
      ].map(([v, l]) => `<div class="stat"><b>${esc(v)}</b><span>${l}</span></div>`).join('');
      $('#list').innerHTML = resources.length ? resources.map(card).join('')
        : `<p class="empty">${stats.total ? 'Aucune ressource ne correspond aux filtres.' : 'Bibliothèque vide : ajoute des liens ou lance une recherche dans « Découvrir ».'}</p>`;
    } catch (e) { toast(e.message, true); }
  }
  $('#filters').addEventListener('input', debounce(loadLibrary, 250));
  $('#filters').addEventListener('submit', (e) => e.preventDefault());
  function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; }

  $('#list').addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-act]');
    if (!btn || btn.tagName === 'SELECT') return;
    const el = btn.closest('.card');
    const id = el.dataset.id;
    try {
      if (btn.dataset.act === 'delete') {
        if (!confirm('Supprimer cette ressource ?')) return;
        await api('/resources/' + id, { method: 'DELETE' });
        toast('Supprimée');
      } else if (btn.dataset.act === 'rescore') {
        btn.disabled = true; btn.textContent = 'Analyse…';
        await api(`/resources/${id}/rescore`, { method: 'POST' });
        toast('Fiche mise à jour');
      } else if (btn.dataset.act === 'save-notes') {
        await api('/resources/' + id, { method: 'PATCH', body: { notes: $('[data-field=notes]', el).value } });
        toast('Notes enregistrées');
        return;
      }
      loadLibrary();
    } catch (err) { toast(err.message, true); loadLibrary(); }
  });
  $('#list').addEventListener('change', async (e) => {
    if (e.target.dataset.act !== 'status') return;
    try {
      await api('/resources/' + e.target.closest('.card').dataset.id, { method: 'PATCH', body: { status: e.target.value } });
      toast('Statut mis à jour');
    } catch (err) { toast(err.message, true); }
  });

  function download(name, mime, content) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([content], { type: mime }));
    a.download = name;
    a.click();
    URL.revokeObjectURL(a.href);
  }
  $('#export-json').addEventListener('click', () => download('master-ia.json', 'application/json', JSON.stringify(state.resources, null, 2)));
  $('#export-csv').addEventListener('click', () => {
    const cols = ['title', 'url', 'source', 'category', 'tags', 'type', 'level', 'language', 'score', 'status', 'description'];
    // Neutralise l'injection de formules (=, +, -, @) à l'ouverture dans un tableur.
    const cell = (v) => { let s = Array.isArray(v) ? v.join('; ') : String(v ?? ''); if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; return '"' + s.replace(/"/g, '""') + '"'; };
    download('master-ia.csv', 'text/csv;charset=utf-8', '﻿' + [cols.join(','), ...state.resources.map((r) => cols.map((c) => cell(r[c])).join(','))].join('\n'));
  });

  /* ---------- Ajouter ---------- */
  function logLine(ul, cls, text) {
    const li = document.createElement('li');
    li.className = cls;
    li.textContent = text;
    ul.prepend(li);
    return li;
  }

  $('#add-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const urls = [...new Set($('#add-urls').value.split(/\s+/).map((s) => s.trim()).filter(Boolean))];
    if (!urls.length) return;
    const btn = $('#add-go'); btn.disabled = true;
    const ul = $('#add-log'); ul.innerHTML = '';
    let n = 0;
    for (const url of urls) {
      const li = logLine(ul, '', `⏳ ${url}`);
      try {
        const { resource, duplicate } = await api('/resources', { method: 'POST', body: { url } });
        li.className = duplicate ? 'dup' : 'ok';
        li.textContent = `${duplicate ? '↺ Déjà présente' : '✓ Ajoutée'} — ${resource.title} (${resource.score}/10, ${resource.category})`;
        if (!duplicate) n++;
      } catch (err) { li.className = 'ko'; li.textContent = `✗ ${url} — ${err.message}`; }
    }
    btn.disabled = false;
    $('#add-urls').value = '';
    toast(`${n} ressource(s) ajoutée(s)`);
  });

  /* ---------- Découvrir ---------- */
  $('#discover-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const sources = [...document.querySelectorAll('#d-sources input:checked')].map((i) => i.value);
    const btn = $('#d-go'); btn.disabled = true; btn.textContent = 'Recherche…';
    $('#d-results').innerHTML = '<p class="empty">Claude cherche… (jusqu\'à une minute)</p>';
    try {
      const { candidates } = await api('/discover', { method: 'POST', body: {
        query: $('#d-query').value, sources, limit: +$('#d-limit').value || 8,
        domains: $('#d-domains').value.split(/[,\s]+/).filter(Boolean),
      } });
      $('#d-results').innerHTML = candidates.length
        ? `<div class="row"><button class="primary" id="add-all">Tout ajouter (${candidates.filter((c) => !c.exists).length})</button></div>` + candidates.map(candidateCard).join('')
        : '<p class="empty">Aucun résultat. Essaie une demande plus large ou d\'autres sources.</p>';
    } catch (err) { $('#d-results').innerHTML = ''; toast(err.message, true); }
    btn.disabled = false; btn.textContent = 'Chercher';
  });

  function candidateCard(c) {
    return `<article class="card" data-url="${esc(c.url)}">
      <div class="score ${scoreClass(c.preliminary_score)}" title="Estimation préliminaire">${c.preliminary_score}<small>/10</small></div>
      <div><h3><a href="${esc(safeUrl(c.url))}" target="_blank" rel="noopener noreferrer">${esc(c.title)}</a></h3>
        <div class="meta"><span class="chip">${esc(state.taxonomy.sources[c.source] || c.source)}</span><span>${esc(c.language.toUpperCase())}</span></div>
        <p class="why">${esc(c.why)}</p>
        <div class="actions"><button class="primary" data-add ${c.exists ? 'disabled' : ''}>${c.exists ? 'Déjà dans la bibliothèque' : 'Ajouter'}</button></div></div></article>`;
  }

  async function addCandidate(card) {
    const btn = $('[data-add]', card);
    btn.disabled = true; btn.textContent = 'Analyse…';
    try {
      const { resource } = await api('/resources', { method: 'POST', body: { url: card.dataset.url } });
      btn.textContent = `Ajoutée — ${resource.score}/10`;
      $('.score', card).className = 'score ' + scoreClass(resource.score);
      $('.score', card).firstChild.textContent = resource.score;
    } catch (err) { btn.disabled = false; btn.textContent = 'Réessayer'; toast(err.message, true); }
  }
  $('#d-results').addEventListener('click', async (e) => {
    if (e.target.closest('#add-all')) {
      e.target.disabled = true;
      for (const c of document.querySelectorAll('#d-results .card')) if (!$('[data-add]', c).disabled) await addCandidate(c);
      return;
    }
    const b = e.target.closest('[data-add]');
    if (b) addCandidate(b.closest('.card'));
  });

  /* ---------- Profil ---------- */
  $('#profile-save').addEventListener('click', async () => {
    try { await api('/settings', { method: 'PUT', body: { profile: $('#profile').value } }); toast('Profil enregistré — les prochaines notes l\'utiliseront'); }
    catch (err) { toast(err.message, true); }
  });
  $('#rescore-all').addEventListener('click', async () => {
    if (!confirm('Relancer l\'analyse Claude sur toutes les ressources ? Un appel par ressource (coût API).')) return;
    const btn = $('#rescore-all'); btn.disabled = true;
    const ul = $('#rescore-log'); ul.innerHTML = '';
    try {
      const { resources } = await api('/resources?sort=recent');
      for (const [i, r] of resources.entries()) {
        const li = logLine(ul, '', `⏳ ${i + 1}/${resources.length} ${r.title}`);
        try { const { resource } = await api(`/resources/${r.id}/rescore`, { method: 'POST' }); li.className = 'ok'; li.textContent = `✓ ${resource.title} : ${r.score} → ${resource.score}/10`; }
        catch (err) { li.className = 'ko'; li.textContent = `✗ ${r.title} — ${err.message}`; }
      }
    } catch (err) { toast(err.message, true); }
    btn.disabled = false;
  });

  /* ---------- Démarrage ---------- */
  function fillSelect(sel, values, label = (v) => v) {
    sel.insertAdjacentHTML('beforeend', values.map((v) => `<option value="${esc(v)}">${esc(label(v))}</option>`).join(''));
  }

  async function boot() {
    const s = await api('/settings');
    const first = !state.taxonomy;
    state.taxonomy = s.taxonomy;
    $('#profile').value = s.profile;
    $('#caps').textContent = `Modèle : ${s.capabilities.model} · API YouTube : ${s.capabilities.youtube_api ? 'active (durée, vues, description complète)' : 'non configurée (titre et chaîne seulement)'}`;
    if (first) {
      fillSelect($('#f-category'), s.taxonomy.categories);
      fillSelect($('#f-source'), Object.keys(s.taxonomy.sources), (k) => s.taxonomy.sources[k]);
      fillSelect($('#f-status'), s.taxonomy.statuses, statusLabel);
      $('#d-sources').innerHTML = Object.entries(s.taxonomy.sources)
        .map(([k, l]) => `<label><input type="checkbox" value="${esc(k)}"${k !== 'web' ? ' checked' : ''}> ${esc(l)}</label>`).join('');
    }
    unlock();
  }

  if (store.get()) boot().catch((e) => { toast(e.message, true); lock(); });
  else lock();
})();
