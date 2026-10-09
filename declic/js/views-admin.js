/* Back-office de Claire */
(function () {
  'use strict';
  const D = window.DECLIC, S = window.Store, E = window.Engine, U = window.UI, V = window.Views;
  const { esc } = U;
  const A = (window.Actions = window.Actions || {});
  const DAY = 86400000;
  const db = () => S.get();
  const clients = () => db().clients;
  const nameOf = (c) => E.fullName(c);
  const clientLink = (c) => `<a href="#/admin/clients/${c.id}">${esc(nameOf(c))}</a>`;
  const avatar = (c) => `<span class="avatar">${esc(U.initials(c))}</span>`;
  const STATUS_LABEL = { lead: 'Lead', prospect: 'Prospecte', cliente: 'Cliente', alumni: 'Ancienne cliente', perdue: 'Perdue' };
  const badge = (c) => { const s = E.status(c); return `<span class="badge st-${s}">${STATUS_LABEL[s]}</span>`; };
  const rerender = () => window.App.render();

  /* ---------- Calculs ---------- */
  function money() {
    const paid = db().invoices.filter((i) => i.status === 'paid');
    const now = S.nowDate();
    const inMonth = (iso, back) => { const d = new Date(iso); const t = new Date(now.getFullYear(), now.getMonth() - back, 1); return d.getFullYear() === t.getFullYear() && d.getMonth() === t.getMonth(); };
    const months = [5, 4, 3, 2, 1, 0].map((b) => { const d = new Date(now.getFullYear(), now.getMonth() - b, 1); return { label: d.toLocaleDateString('fr-FR', { month: 'short' }), value: paid.filter((i) => inMonth(i.paidAt, b)).reduce((s, i) => s + i.amount, 0) }; });
    const due = db().invoices.filter((i) => i.status === 'due');
    return { month: months[5].value, months, total: paid.reduce((s, i) => s + i.amount, 0), due: due.reduce((s, i) => s + i.amount, 0), dueCount: due.length };
  }
  function kpis() {
    const cs = clients();
    const active = cs.filter((c) => E.status(c) === 'cliente').length;
    const proposals = cs.filter((c) => c.stage === 'decision' && !c.lost);
    const pipe = proposals.reduce((s, c) => s + (E.offerOf(c) ? E.offerOf(c).price : 0), 0);
    const calls = cs.filter((c) => c.done.call_done).length;
    const won = cs.filter((c) => c.done.pay).length;
    return { active, pipe, proposals: proposals.length, conv: calls ? Math.round(won / calls * 100) : 0, leads: cs.filter((c) => E.status(c) === 'lead').length, total: cs.length };
  }

  /* ---------- À faire (dérivé automatiquement) ---------- */
  function todos() {
    const out = []; const nowMs = S.nowDate().getTime();
    clients().forEach((c) => {
      if (c.lost) return;
      const name = nameOf(c);
      const call = (c.appts || []).find((a) => a.kind === 'call');
      if (call && !c.done.call_done) {
        const t = new Date(call.date).getTime();
        if (t - nowMs < DAY && !c.done.prep_call) out.push({ prio: 2, icon: '📖', title: `Relire le dossier de ${name}`, sub: `Appel ${E.dateFr(call.date, true)} · score ${c.score != null ? c.score + '/100' : 'n/a'}`, c, act: 'prep', label: 'C’est lu' });
        if (t <= nowMs + 3600000) out.push({ prio: 1, icon: '📞', title: `Appel découverte avec ${name}`, sub: E.dateFr(call.date, true), c, act: 'propose', label: 'Appel fait → proposer' });
      }
      if (c.stage === 'decouverte' && c.done.prequal && !call && E.status(c) === 'prospect' && Date.now() - new Date(c.done.prequal).getTime() > 2 * DAY) out.push({ prio: 4, icon: '📩', title: `${name} n’a pas réservé son appel`, sub: 'Questionnaire rempli il y a plus de 2 jours', c, act: 'nudgeCall', label: 'Relancer' });
      if (c.stage === 'decision' && c.proposedAt && Date.now() - new Date(c.proposedAt).getTime() > 6 * DAY && !c.done.sign) out.push({ prio: 3, icon: '⏰', title: `Proposition sans réponse : ${name}`, sub: `Envoyée ${U.rel(c.proposedAt)} (relances auto déjà parties)`, c, act: 'lost', label: 'Clore le dossier' });
      if (c.payPending) out.push({ prio: 1, icon: '💶', title: `Confirmer le paiement de ${name}`, sub: 'Elle a utilisé ton lien de paiement', c, act: 'confirmPay', label: 'Paiement reçu' });
      c.sessions.forEach((s) => { if (s.state === 'booked' && new Date(s.date).getTime() <= nowMs) out.push({ prio: 1, icon: '🎯', title: `Séance ${s.n} réalisée avec ${name} ?`, sub: `${s.theme} · ${E.dateFr(s.date, true)}`, c, act: 'doneS', data: s.n, label: 'Séance faite' }); });
      if (E.status(c) === 'cliente' && c.stage === 'programme' && Date.now() - new Date(c.lastActivity).getTime() > 10 * DAY && !c.sessions.some((s) => s.state === 'booked')) out.push({ prio: 3, icon: '💤', title: `${name} est inactive`, sub: `Dernière activité ${U.rel(c.lastActivity)}`, c, act: 'nudgeS', label: 'Envoyer un rappel' });
      if (c.answers.testimonial && c.answers.testimonial.consent && !c.answers.testimonial.consent.startsWith('Non') && !c.testiUsed) out.push({ prio: 5, icon: '⭐', title: `Témoignage de ${name} à utiliser`, sub: c.answers.testimonial.quote, c, act: 'testiUsed', label: 'C’est publié' });
    });
    db().invoices.filter((i) => i.status === 'due' && new Date(i.dueAt).getTime() < nowMs).forEach((i) => { const c = S.clientById(i.clientId); if (c && !c.payPending) out.push({ prio: 2, icon: '💶', title: `Échéance due : ${nameOf(c)} (${E.money(i.amount)})`, sub: i.number, c, act: 'paid', data: i.id, label: 'Marquer payée' }); });
    db().outbox.filter((m) => m.status === 'review').forEach((m) => { const c = S.clientById(m.clientId); out.push({ prio: 3, icon: '✉️', title: `Email à valider : ${m.subject}`, sub: c ? nameOf(c) : '', c, act: 'sendMail', data: m.id, label: 'Envoyer' }); });
    const s = db().settings;
    if (!s.siret || !s.address) out.push({ prio: 2, icon: '⚙️', title: 'Complète tes informations légales', sub: 'SIRET et adresse pour les contrats, factures et mentions légales', c: null, act: 'goSettings', label: 'Compléter' });
    return out.sort((a, b) => a.prio - b.prio);
  }

  function todoRow(t) {
    return `<li class="todo p${t.prio}"><span class="todo-i">${t.icon}</span><div class="t-main"><div class="t-label">${esc(t.title)}</div><div class="t-hint">${esc(t.sub || '')}</div></div><button class="btn sm" data-act="todo" data-k="${t.act}" data-c="${t.c ? t.c.id : ''}" data-d="${esc(t.data == null ? '' : t.data)}">${esc(t.label)}</button></li>`;
  }

  /* ---------- Vues ---------- */
  function dashboard() {
    const m = money(); const k = kpis(); const td = todos();
    const g3 = D.BRAND.goals.m3, g6 = D.BRAND.goals.m6;
    const max = Math.max(...m.months.map((x) => x.value), 1);
    const feed = db().activity.slice(0, 8).map((a) => `<li><span class="muted">${U.rel(a.t)}</span> ${esc(a.text)}</li>`).join('');
    const cols = [['decouverte', 'Découverte'], ['decision', 'Décision'], ['onboarding', 'Onboarding'], ['programme', 'Programme'], ['bilan', 'Bilan'], ['ensuite', 'Anciennes']];
    return `<div class="hello"><h1>Bonjour ${esc(db().settings.owner.split(' ')[0])} 👋</h1><p class="muted">${td.length ? `Il te reste <strong>${td.length}</strong> action${td.length > 1 ? 's' : ''} humaine${td.length > 1 ? 's' : ''} aujourd’hui — tout le reste est automatique.` : 'Rien à faire : la plateforme gère tout. Profite !'}</p></div>
    <div class="kpis">
      <div class="kpi"><div class="k-l">Encaissé ce mois</div><div class="k-v">${E.money(m.month)}</div><div class="bar"><i style="width:${Math.min(100, m.month / g3 * 100)}%"></i></div><div class="k-s">Objectif 3 mois : ${E.money(g3)} net</div></div>
      <div class="kpi"><div class="k-l">Objectif 6 mois</div><div class="k-v">${E.money(g6)}<small>/mois</small></div><div class="bar alt"><i style="width:${Math.min(100, m.month / g6 * 100)}%"></i></div><div class="k-s">${Math.round(m.month / g6 * 100)} % atteint</div></div>
      <div class="kpi"><div class="k-l">Clientes en cours</div><div class="k-v">${k.active}</div><div class="k-s">${k.leads} lead${k.leads > 1 ? 's' : ''} · ${k.total} dossier${k.total > 1 ? 's' : ''}</div></div>
      <div class="kpi"><div class="k-l">Propositions en attente</div><div class="k-v">${E.money(k.pipe)}</div><div class="k-s">${k.proposals} dossier${k.proposals > 1 ? 's' : ''} · conversion ${k.conv} %</div></div>
    </div>
    <div class="grid2">
      <section class="card"><h2>À faire <a class="more" href="#/admin/todo">Tout voir</a></h2><ul class="todos">${td.slice(0, 5).map(todoRow).join('') || '<li class="empty-s">✨ Rien à faire pour le moment.</li>'}</ul></section>
      <section class="card"><h2>Encaissements (6 mois)</h2><div class="chart" role="img" aria-label="Encaissements par mois">${m.months.map((x) => `<div class="c-col"><div class="c-v">${x.value ? E.money(x.value) : ''}</div><div class="c-b" style="height:${Math.round(x.value / max * 100)}%"></div><div class="c-l">${esc(x.label)}</div></div>`).join('')}</div></section>
    </div>
    <section class="card"><h2>Pipeline <a class="more" href="#/admin/pipeline">Ouvrir</a></h2><div class="funnel">${cols.map(([id, l]) => `<div class="f-col"><div class="f-n">${clients().filter((c) => c.stage === id && !c.lost).length}</div><div class="f-l">${l}</div></div>`).join('')}</div></section>
    <section class="card"><h2>Activité récente</h2><ul class="feed">${feed || '<li class="muted">Aucune activité.</li>'}</ul></section>`;
  }

  function todoView() {
    const td = todos();
    return `<h1>À faire</h1><p class="muted">Uniquement ce qui demande vraiment ta présence. Chaque ligne se règle en un clic.</p><ul class="todos card">${td.map(todoRow).join('') || '<li class="empty-s">✨ Tout est à jour.</li>'}</ul>`;
  }

  function pipeline() {
    const colDefs = [
      ['lead', 'Leads', (c) => c.stage === 'decouverte' && E.status(c) === 'lead'], ['prospect', 'Prospectes', (c) => c.stage === 'decouverte' && E.status(c) === 'prospect'],
      ['decision', 'Proposition', (c) => c.stage === 'decision'], ['onboarding', 'Onboarding', (c) => c.stage === 'onboarding'],
      ['programme', 'En programme', (c) => c.stage === 'programme'], ['bilan', 'Bilan', (c) => c.stage === 'bilan'], ['ensuite', 'Anciennes', (c) => c.stage === 'ensuite'],
    ];
    const card = (c) => { const o = E.offerOf(c); const done = c.sessions.filter((s) => s.state === 'done').length; return `<a class="kcard" href="#/admin/clients/${c.id}">${avatar(c)}<div><strong>${esc(nameOf(c))}</strong><div class="muted">${o ? esc(o.short) + ' · ' + E.money(o.price) : esc(c.source)}</div>${c.sessions.length && c.stage === 'programme' ? `<div class="bar sm"><i style="width:${done / c.sessions.length * 100}%"></i></div>` : ''}${c.score != null && c.stage === 'decouverte' ? `<div class="muted">Score ${c.score}/100</div>` : ''}</div></a>`; };
    return `<div class="row between"><h1>Pipeline</h1><button class="btn" data-act="addLead">+ Ajouter une prospecte</button></div><div class="kanban">${colDefs.map(([id, l, f]) => { const list = clients().filter((c) => !c.lost && f(c)); return `<section class="kcol"><h3>${l} <span class="count">${list.length}</span></h3>${list.map(card).join('') || '<div class="kempty">—</div>'}</section>`; }).join('')}</div>`;
  }

  function clientsList() {
    const q = (window.App.query || '').toLowerCase();
    const list = clients().filter((c) => !q || (nameOf(c) + c.email).toLowerCase().includes(q));
    return `<div class="row between"><h1>Clientes</h1><button class="btn" data-act="addLead">+ Ajouter</button></div><input class="inp search" placeholder="Rechercher…" value="${esc(window.App.query || '')}" data-act="search"><div class="card"><table class="list"><tr><th></th><th>Nom</th><th>Statut</th><th>Étape</th><th>Offre</th><th>Source</th><th>Dernière activité</th></tr>${list.map((c) => `<tr><td>${avatar(c)}</td><td>${clientLink(c)}<div class="muted">${esc(c.email)}</div></td><td>${badge(c)}</td><td>${esc(E.stageById(c.stage).label)}</td><td>${E.offerOf(c) ? esc(E.offerOf(c).short) : '—'}</td><td>${esc(c.source)}${c.referrer ? ' 💌' : ''}</td><td>${U.rel(c.lastActivity)}</td></tr>`).join('')}</table></div>`;
  }

  function clientDetail(id) {
    const c = S.clientById(id); if (!c) return '<p>Dossier introuvable.</p>';
    const o = E.offerOf(c); const cur = E.stageIndex(c.stage);
    const steps = D.STAGES.map((s, i) => `<li class="${i < cur ? 'done' : i === cur ? 'cur' : 'pend'}"><span class="dot">${i < cur ? '✓' : s.icon}</span><span class="s-l">${esc(s.label)}</span></li>`).join('');
    const st = E.stageById(c.stage);
    const rows = st.tasks.filter((t) => t.id !== 'prep_call' || true).map((t) => {
      const done = E.isDone(c, t.id) || (t.kind === 'session' && E.sessionsAllDone(c));
      const btn = done ? `<span class="done-at">✓ ${t.kind === 'session' ? '' : E.dateFr(c.done[t.id])}</span>` : t.kind === 'propose' ? `<button class="btn sm" data-act="propose" data-c="${c.id}">Appel fait → proposer</button>` : t.kind === 'session' ? '' : `<button class="btn sm ghost" data-act="forceTask" data-c="${c.id}" data-t="${t.id}">Valider pour elle</button>`;
      return `<li class="task ${done ? 'is-done' : ''} ${t.who === 'coach' ? 'is-coach' : ''}"><span class="box">${done ? '✓' : t.who === 'coach' ? '👤' : ''}</span><div class="t-main"><div class="t-label">${esc(t.label)} <span class="tag">${t.who === 'coach' ? 'toi' : 'elle'}</span></div></div><div class="t-act">${btn}</div></li>`;
    }).join('');
    const sess = c.sessions.length ? c.sessions.map((s) => `<tr><td>${s.n}</td><td>${esc(s.theme)}</td><td>${s.date ? E.dateFr(s.date, true) : '—'}</td><td>${s.state === 'done' ? `<span class="badge ok">Réalisée</span> <span class="muted">${s.exoDone.length}/${(D.EXERCISES[s.theme] || []).length} exos</span>` : s.state === 'locked' ? '<span class="badge">À venir</span>' : `<button class="btn sm" data-act="doneS" data-c="${c.id}" data-n="${s.n}">Marquer réalisée</button>`}</td></tr>`).join('') : '';
    const answers = Object.entries(c.answers).map(([fid, a]) => { const f = D.FORMS[fid]; if (!f) return ''; return `<details class="card-in"><summary>${esc(f.title)}</summary>${f.fields.map((q) => `<p><strong>${esc(q.label)}</strong><br>${esc(Array.isArray(a[q.id]) ? a[q.id].join(', ') : a[q.id] || '—')}</p>`).join('')}</details>`; }).join('');
    const inv = db().invoices.filter((i) => i.clientId === c.id);
    const mails = db().outbox.filter((m) => m.clientId === c.id).sort((a, b) => new Date(b.sendAt) - new Date(a.sendAt)).slice(0, 8);
    const act = db().activity.filter((a) => a.clientId === c.id).slice(0, 10);
    const ref = c.referrer ? clients().find((x) => x.refCode === c.referrer) : null;
    return `<a class="back" href="#/admin/clients">← Clientes</a>
    <div class="cl-head">${avatar(c)}<div><h1>${esc(nameOf(c))} ${badge(c)}</h1><p class="muted">${esc(c.email)}${c.phone ? ' · ' + esc(c.phone) : ''} · ${esc(c.source)}${ref ? ' · recommandée par ' + esc(nameOf(ref)) : ''}</p></div><div class="cl-actions"><button class="btn ghost sm" data-act="viewAs" data-c="${c.id}">👁 Voir comme elle</button>${c.lost ? `<button class="btn sm" data-act="restore" data-c="${c.id}">Réactiver</button>` : `<button class="btn ghost sm" data-act="lost" data-c="${c.id}">Marquer perdue</button>`}</div></div>
    <div class="facts"><div><span class="muted">Offre</span><strong>${o ? esc(o.short) + ' · ' + E.money(o.price) : 'À définir'}</strong></div><div><span class="muted">Score</span><strong>${c.score != null ? c.score + '/100' : '—'}</strong></div><div><span class="muted">Depuis</span><strong>${E.dateFr(c.createdAt)}</strong></div><div><span class="muted">Dernière activité</span><strong>${U.rel(c.lastActivity)}</strong></div></div>
    <ol class="stepper">${steps}</ol>
    <section class="card"><h2>Étape en cours : ${esc(st.label)}</h2><ul class="tasks">${rows}</ul></section>
    ${sess ? `<section class="card"><h2>Séances</h2><table class="list"><tr><th>#</th><th>Thème</th><th>Date</th><th></th></tr>${sess}</table></section>` : ''}
    <div class="grid2"><section class="card"><h2>Notes privées</h2><form data-act="note" data-c="${c.id}" class="row"><input class="inp" name="n" placeholder="Ajouter une note…"><button class="btn sm">Ajouter</button></form><ul class="feed">${c.notes.map((n) => `<li><span class="muted">${U.rel(n.t)}</span> ${esc(n.text)}</li>`).join('') || '<li class="muted">Aucune note.</li>'}</ul></section>
    <section class="card"><h2>Ses réponses</h2>${answers || '<p class="muted">Aucune réponse pour l’instant.</p>'}</section></div>
    <div class="grid2"><section class="card"><h2>Paiements</h2>${inv.length ? `<table class="list">${inv.map((i) => `<tr><td>${esc(i.number)}</td><td>${E.money(i.amount)}</td><td>${i.status === 'paid' ? '<span class="badge ok">Payée</span>' : `<button class="btn sm" data-act="markPaid" data-id="${i.id}">Marquer payée</button>`}</td><td><button class="link" data-act="inv" data-id="${i.id}">Voir</button></td></tr>`).join('')}</table>` : '<p class="muted">Aucune facture.</p>'}</section>
    <section class="card"><h2>Emails</h2><ul class="feed">${mails.map((m) => `<li><span class="badge ${m.status === 'sent' ? 'ok' : m.status === 'cancelled' ? '' : 'warn'}">${{ sent: 'Envoyé', scheduled: 'Programmé', review: 'À valider', cancelled: 'Annulé' }[m.status]}</span> ${esc(m.subject)}</li>`).join('') || '<li class="muted">Aucun email.</li>'}</ul></section></div>
    <section class="card"><h2>Historique</h2><ul class="feed">${act.map((a) => `<li><span class="muted">${U.rel(a.t)}</span> ${esc(a.text)}</li>`).join('')}</ul></section>`;
  }

  function launch() {
    const L = db().launch; let doneN = 0;
    const phases = [1, 2, 3, 4, 5, 6].map((p) => {
      const items = D.LAUNCH.map((it, i) => ({ it, i })).filter((x) => x.it.phase === p);
      const rows = items.map(({ it, i }) => {
        const auto = !!it.auto; const done = auto || !!L[i];
        if (done) doneN++;
        const pr = { ESSENTIEL: 'ess', RECOMMANDÉ: 'rec', OPTIONNEL: 'optl' }[it.p];
        return `<li class="lrow ${done ? 'is-done' : ''}"><label class="opt">${auto ? '<span class="auto">✓</span>' : `<input type="checkbox" data-act="lch" data-i="${i}" ${L[i] ? 'checked' : ''}>`}<span><strong>${esc(it.n)}</strong> <span class="tag ${pr}">${it.p}</span>${it.auto ? `<span class="auto-t"> ⚡ ${esc(it.auto)}</span>` : ''}${it.help ? `<div class="t-hint">${esc(it.help)}</div>` : ''}${it.tpl ? ` <button class="link" data-act="tpl" data-id="${it.tpl}">Voir le modèle</button>` : ''}${it.page ? ` <a href="${it.page}" target="_blank">Voir la page</a>` : ''}</span></label></li>`;
      }).join('');
      return `<section class="card"><h2>Phase ${p} — ${esc(D.PHASES[p])}</h2><ul class="lrows">${rows}</ul></section>`;
    }).join('');
    const pct = Math.round(doneN / D.LAUNCH.length * 100);
    const autoN = D.LAUNCH.filter((x) => x.auto).length;
    return `<h1>Mise en route</h1><p class="muted">Les ${D.LAUNCH.length} éléments du document, déjà préparés. <strong>${autoN}</strong> sont gérés automatiquement par la plateforme ; il ne te reste que quelques cases à cocher.</p><div class="card progress"><div class="bar big"><i style="width:${pct}%"></i></div><strong>${pct} %</strong><span class="muted">${doneN} / ${D.LAUNCH.length}</span></div>${phases}`;
  }

  function library() {
    const groups = [
      ['Acquisition & vente', ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']],
      ['Onboarding, livraison, fidélisation', ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']],
      ['Administration, reporting, pilotage', ['C1', 'C2', 'C3', 'C4', 'C5']],
    ];
    return `<h1>Bibliothèque</h1><p class="muted">Tous les modèles du document, prêts à l’emploi. Les parties utiles sont déjà intégrées automatiquement dans le parcours.</p>${groups.map(([t, ids]) => `<section class="card"><h2>${esc(t)}</h2><div class="res-grid">${ids.map((id) => `<button class="res" data-act="tpl" data-id="${id}"><span class="res-i">📄</span><span class="res-t">${esc(window.TEMPLATES[id].title)}</span><span class="res-s">Template ${id}</span></button>`).join('')}</div></section>`).join('')}<section class="card"><h2>Guide offert (lead magnet)</h2><div class="res-grid"><button class="res" data-act="guide"><span class="res-i">📘</span><span class="res-t">Les 5 blocages invisibles</span><span class="res-s">Débloqué à l’inscription</span></button></div></section>`;
  }

  function emails() {
    const tab = window.App.tab || 'queue'; const ob = db().outbox.slice().sort((a, b) => new Date(b.sendAt) - new Date(a.sendAt));
    const lab = { sent: 'Envoyé', scheduled: 'Programmé', review: 'À valider', cancelled: 'Annulé' };
    const rows = ob.filter((m) => tab === 'queue' ? m.status !== 'sent' && m.status !== 'cancelled' : tab === 'sent' ? m.status === 'sent' : true).slice(0, 80).map((m) => { const c = S.clientById(m.clientId); return `<tr><td><span class="badge ${m.status === 'sent' ? 'ok' : m.status === 'review' ? 'warn' : ''}">${lab[m.status]}</span></td><td>${E.dateFr(m.sendAt, true)}</td><td>${c ? esc(nameOf(c)) : '—'}</td><td><button class="link" data-act="mail" data-id="${m.id}">${esc(m.subject)}</button></td><td>${m.status === 'scheduled' || m.status === 'review' ? `<button class="btn sm" data-act="sendMailNow" data-id="${m.id}">Envoyer</button> <button class="link" data-act="cancelMail" data-id="${m.id}">Annuler</button>` : ''}</td></tr>`; }).join('');
    const tpls = Object.entries(D.EMAILS).map(([k, t]) => `<details class="card-in"><summary>${esc(t.subject)} <span class="muted">· ${k}</span></summary><pre class="mailbody">${esc(t.body)}</pre></details>`).join('');
    const st = db().settings;
    return `<h1>Emails automatiques</h1><div class="card note">${st.autopilot ? '🤖 Pilote automatique activé : les emails partent seuls au bon moment.' : '✋ Tu valides chaque email avant envoi.'} ${st.mailWebhook ? 'Envoi réel branché.' : '<span class="muted">Mode démo : les envois sont simulés — branche ton service d’emailing dans Réglages.</span>'}</div>
    <div class="tabs"><button class="${tab === 'queue' ? 'on' : ''}" data-act="tab" data-t="queue">À venir</button><button class="${tab === 'sent' ? 'on' : ''}" data-act="tab" data-t="sent">Envoyés</button><button class="${tab === 'all' ? 'on' : ''}" data-act="tab" data-t="all">Tous</button><button class="${tab === 'tpl' ? 'on' : ''}" data-act="tab" data-t="tpl">Modèles</button></div>
    ${tab === 'tpl' ? `<section class="card"><p class="muted">Séquence de bienvenue : J0, J+1, J+3, J+5, J+7, J+10 (s’arrête dès que l’appel est réservé). Relances proposition : J+2 et J+5.</p>${tpls}</section>` : `<div class="card"><table class="list"><tr><th>Statut</th><th>Date</th><th>Destinataire</th><th>Sujet</th><th></th></tr>${rows || '<tr><td colspan="5" class="muted">Rien ici.</td></tr>'}</table></div>`}`;
  }

  function finance() {
    const m = money(); const inv = db().invoices.slice().sort((a, b) => new Date(b.issuedAt) - new Date(a.issuedAt)); const max = Math.max(...m.months.map((x) => x.value), 1);
    const upcoming = inv.filter((i) => i.status === 'due');
    return `<div class="row between"><h1>Finances</h1><button class="btn ghost" data-act="csv">Exporter (CSV)</button></div>
    <div class="kpis"><div class="kpi"><div class="k-l">Encaissé au total</div><div class="k-v">${E.money(m.total)}</div></div><div class="kpi"><div class="k-l">Ce mois</div><div class="k-v">${E.money(m.month)}</div><div class="bar"><i style="width:${Math.min(100, m.month / D.BRAND.goals.m3 * 100)}%"></i></div><div class="k-s">sur ${E.money(D.BRAND.goals.m3)}</div></div><div class="kpi"><div class="k-l">À encaisser</div><div class="k-v">${E.money(m.due)}</div><div class="k-s">${m.dueCount} échéance${m.dueCount > 1 ? 's' : ''}</div></div></div>
    <section class="card"><h2>Encaissements par mois</h2><div class="chart" role="img" aria-label="Encaissements par mois">${m.months.map((x) => `<div class="c-col"><div class="c-v">${x.value ? E.money(x.value) : ''}</div><div class="c-b" style="height:${Math.round(x.value / max * 100)}%"></div><div class="c-l">${esc(x.label)}</div></div>`).join('')}</div></section>
    <section class="card"><h2>Factures</h2><table class="list"><tr><th>N°</th><th>Cliente</th><th>Libellé</th><th>Montant</th><th>Statut</th><th></th></tr>${inv.map((i) => { const c = S.clientById(i.clientId); return `<tr><td>${esc(i.number)}</td><td>${c ? clientLink(c) : ''}</td><td>${esc(i.label)}</td><td>${E.money(i.amount)}</td><td>${i.status === 'paid' ? '<span class="badge ok">Payée ' + E.dateFr(i.paidAt) + '</span>' : `<button class="btn sm" data-act="markPaid" data-id="${i.id}">Marquer payée</button>`}</td><td><button class="link" data-act="inv" data-id="${i.id}">Voir</button></td></tr>`; }).join('')}</table></section>`;
  }

  function settings() {
    const s = db().settings;
    const f = (k, l, type, ph) => `<div class="fld"><label class="lbl">${l}</label><input class="inp" name="${k}" type="${type || 'text'}" value="${esc(s[k] || '')}" placeholder="${esc(ph || '')}"></div>`;
    return `<h1>Réglages</h1>
    <form id="set" class="card"><h2>Mon activité (utilisé dans contrats, factures, mentions légales)</h2><div class="grid2f">${f('owner', 'Nom')}${f('email', 'Email pro', 'email')}${f('phone', 'Téléphone')}${f('whatsapp', 'WhatsApp (lien)')}${f('status', 'Statut juridique')}${f('siret', 'SIRET')}${f('address', 'Adresse')}${f('tva', 'Mention TVA')}${f('calendarUrl', 'Lien agenda (Calendly, optionnel)')}</div>
    <h2>Paiement (Stripe Payment Links — optionnel)</h2><p class="muted">Laisse vide pour le mode démo. Sinon colle un lien par offre.</p><div class="grid2f">${Object.keys(D.OFFERS).map((o) => `<div class="fld"><label class="lbl">${esc(D.OFFERS[o].short)}</label><input class="inp" name="stripe_${o}" value="${esc((s.stripe || {})[o] || '')}" placeholder="https://buy.stripe.com/…"></div>`).join('')}</div>
    <h2>Automatisation</h2><label class="opt"><input type="checkbox" name="autopilot" ${s.autopilot ? 'checked' : ''}><span><strong>Pilote automatique</strong> — les emails partent seuls (sinon tu valides chacun).</span></label>${f('mailWebhook', 'Webhook d’envoi d’emails (Zapier / Make / Worker)', 'url', 'https://hooks.zapier.com/…')}
    <div class="row end"><button class="btn">Enregistrer</button></div></form>
    <section class="card"><h2>Données</h2><div class="row wrap"><button class="btn ghost" data-act="seed">Charger les données de démonstration</button><button class="btn ghost" data-act="export">Exporter (JSON)</button><label class="btn ghost" style="cursor:pointer">Importer<input type="file" id="imp" accept="application/json" hidden></label><button class="btn danger" data-act="wipe">Tout effacer</button></div><p class="muted">Mode démo : les données restent dans ce navigateur. Voir <code>declic/README.md</code> pour passer sur Supabase.</p></section>`;
  }

  /* ---------- Actions admin ---------- */
  function afterAction(msg) { if (msg) U.toast(msg); rerender(); }

  A.todo = async (d) => {
    const c = d.c ? S.clientById(d.c) : null; const k = d.k;
    if (k === 'prep') { E.complete(c.id, 'prep_call', null, { silent: true }); afterAction('Noté ✓'); }
    else if (k === 'propose') A.propose({ c: c.id });
    else if (k === 'nudgeCall') { E.queueMail(c, 'callinvite'); await E.tick(); afterAction('Relance envoyée'); }
    else if (k === 'lost') U.confirmBox(`Clore le dossier de ${nameOf(c)} ?`, () => { E.markLost(c.id, true); afterAction('Dossier clos'); });
    else if (k === 'confirmPay') { const i = db().invoices.find((x) => x.clientId === c.id && x.status === 'due'); if (i) E.markPaid(i.id); afterAction('Paiement confirmé — son espace est débloqué 🎉'); }
    else if (k === 'doneS') A.doneS({ c: c.id, n: d.d });
    else if (k === 'nudgeS') { E.queueMail(c, 'exos_nudge', { vars: { n: c.sessions.filter((s) => s.state === 'done').length } }); await E.tick(); c.lastActivity = S.now(); S.save(); afterAction('Rappel envoyé'); }
    else if (k === 'testiUsed') { c.testiUsed = true; S.save(); afterAction('Merci !'); }
    else if (k === 'paid') { E.markPaid(d.d); afterAction('Marquée payée'); }
    else if (k === 'sendMail') { await E.sendNow(d.d); afterAction('Envoyé'); }
    else if (k === 'goSettings') location.hash = '#/admin/settings';
  };
  A.propose = (d) => {
    const c = S.clientById(d.c); const rec = (c.answers.prequal && c.answers.prequal.goal === 'Me reconvertir complètement') ? 'transformation' : 'declic';
    const m = U.modal(`<h2 class="modal-title">Quelle offre proposer à ${esc(c.prenom)} ?</h2><p class="muted">La proposition est générée et envoyée automatiquement, avec relances à J+2 et J+5.</p><div class="pay">${['premier', 'declic', 'transformation'].map((id) => { const o = D.OFFERS[id]; return `<label class="payopt"><input type="radio" name="of" value="${id}" ${id === rec ? 'checked' : ''}><span><strong>${esc(o.name)}</strong> · ${E.money(o.price)}<br><span class="muted">${esc(o.pitch)}</span>${id === rec ? '<br><span class="tag ess">Suggérée</span>' : ''}</span></label>`; }).join('')}</div><div class="row end"><button class="btn ghost" data-no>Annuler</button><button class="btn" data-ok>Envoyer la proposition</button></div>`);
    m.el.querySelector('[data-no]').onclick = m.close;
    m.el.querySelector('[data-ok]').onclick = () => { const id = m.el.querySelector('input[name=of]:checked').value; m.close(); E.proposeOffer(c.id, id); E.tick().then(() => afterAction('Proposition envoyée ✉️')); };
  };
  A.doneS = (d) => {
    const c = S.clientById(d.c); const s = c.sessions[d.n - 1];
    const m = U.modal(`<h2 class="modal-title">Séance ${s.n} avec ${esc(c.prenom)}</h2><p class="muted">${esc(s.theme)} — Le compte-rendu part automatiquement et les exercices sont débloqués. Une note rapide suffit (facultatif).</p><textarea class="inp" id="sn" rows="4" placeholder="Ce qui a été travaillé, le déclic, la prochaine étape…"></textarea><div class="row end" style="margin-top:12px"><button class="btn ghost" data-no>Annuler</button><button class="btn" data-ok>Séance réalisée ✓</button></div>`);
    m.el.querySelector('[data-no]').onclick = m.close;
    m.el.querySelector('[data-ok]').onclick = () => { const n = m.el.querySelector('#sn').value; m.close(); E.completeSession(c.id, +d.n, n); E.tick().then(() => afterAction('Séance validée — exercices débloqués 🔓')); };
  };
  A.forceTask = (d) => { const c = S.clientById(d.c); const f = E.findTask(d.t); U.confirmBox(`Valider « ${f.task.label} » à la place de ${c.prenom} ?`, () => { E.complete(c.id, d.t); afterAction('Validé'); }); };
  A.restore = (d) => { E.markLost(d.c, false); rerender(); };
  A.lost = (d) => U.confirmBox('Marquer ce dossier comme perdu ?', () => { E.markLost(d.c, true); rerender(); });
  A.viewAs = (d) => { window.App.impersonate(d.c); };
  A.markPaid = (d) => { E.markPaid(d.id); afterAction('Paiement enregistré'); };
  A.inv = (d) => V.openInvoice(db().invoices.find((i) => i.id === d.id));
  A.search = (d, el) => { window.App.query = el.value; const pos = el.selectionStart; rerender(); const n = document.querySelector('.search'); if (n) { n.focus(); n.setSelectionRange(pos, pos); } };
  A.tab = (d) => { window.App.tab = d.t; rerender(); };
  A.tpl = (d) => { const t = window.TEMPLATES[d.id]; const m = V.openDoc(t.title, V.tplBody(d.id, null), '<button class="btn ghost" data-cp>Copier le texte</button>'); m.el.querySelector('[data-cp]').onclick = () => { navigator.clipboard.writeText(t.md).then(() => U.toast('Copié ✓')); }; };
  A.guide = () => V.openDoc('Guide — Les 5 blocages invisibles', D.GUIDE_MD);
  A.mail = (d) => { const m = db().outbox.find((x) => x.id === d.id); V.openDoc(m.subject, 'À : ' + m.to + '\n\n' + m.body); };
  A.sendMailNow = async (d) => { await E.sendNow(d.id); afterAction('Envoyé'); };
  A.cancelMail = (d) => { E.cancelMail(d.id); rerender(); };
  A.lch = (d, el) => { db().launch[d.i] = el.checked; S.save(); rerender(); };
  A.addLead = () => {
    const m = U.modal(`<h2 class="modal-title">Ajouter une prospecte</h2><form id="al"><div class="fld"><label class="lbl">Prénom</label><input class="inp" name="p" required></div><div class="fld"><label class="lbl">Nom</label><input class="inp" name="n"></div><div class="fld"><label class="lbl">Email</label><input class="inp" name="e" type="email" required></div><div class="fld"><label class="lbl">D’où vient-elle ?</label><select class="inp" name="s"><option>Bouche-à-oreille</option><option>LinkedIn</option><option>Instagram</option><option>Événement</option><option>Autre</option></select></div><div class="err" id="al-e"></div><div class="row end"><button class="btn">Créer et lancer la séquence</button></div></form>`);
    m.el.querySelector('#al').onsubmit = async (e) => {
      e.preventDefault(); const f = e.target; const pw = 'declic-' + Math.random().toString(36).slice(2, 7);
      try { await E.createLead({ prenom: f.p.value.trim(), nom: f.n.value.trim(), email: f.e.value, source: f.s.value, password: pw }); m.close(); await E.tick();
        U.modal(`<h2 class="modal-title">Prospecte créée ✓</h2><p>Son espace est prêt et la séquence de bienvenue est programmée. Pour qu’elle se connecte :</p><p class="doc"><code>${esc(f.e.value)}</code><br>mot de passe provisoire : <code>${esc(pw)}</code></p><p class="muted">Elle pourra le changer dans son profil.</p>`);
        rerender(); } catch (err) { m.el.querySelector('#al-e').textContent = err.message; }
    };
  };
  A.csv = () => {
    const rows = [['Numéro', 'Date', 'Cliente', 'Libellé', 'Montant', 'Statut', 'Payée le']].concat(db().invoices.map((i) => { const c = S.clientById(i.clientId); return [i.number, i.issuedAt.slice(0, 10), c ? nameOf(c) : '', i.label, i.amount, i.status === 'paid' ? 'payée' : 'à régler', i.paidAt ? i.paidAt.slice(0, 10) : '']; }));
    const csv = rows.map((r) => r.map((x) => `"${String(x).replace(/"/g, '""')}"`).join(';')).join('\n');
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob(['﻿' + csv], { type: 'text/csv' })); a.download = 'factures-declic.csv'; a.click();
  };
  A.seed = () => U.confirmBox('Remplacer toutes les données par la démonstration ?', async () => { await window.Seed.run(); await S.login(db().settings.email, 'declic2026'); location.hash = '#/admin'; location.reload(); }, 'Charger');
  A.wipe = () => U.confirmBox('Effacer toutes les données ? (irréversible)', async () => { S.reset(); S.session.clear(); location.href = 'index.html'; }, 'Tout effacer');
  A.export = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify(db(), null, 1)], { type: 'application/json' })); a.download = 'declic-sauvegarde.json'; a.click(); };

  function bindSettings(root) {
    const form = root.querySelector('#set');
    if (form) form.onsubmit = (e) => {
      e.preventDefault(); const s = db().settings; const f = new FormData(form);
      ['owner', 'email', 'phone', 'whatsapp', 'status', 'siret', 'address', 'tva', 'calendarUrl', 'mailWebhook'].forEach((k) => (s[k] = (f.get(k) || '').toString().trim()));
      Object.keys(D.OFFERS).forEach((o) => (s.stripe[o] = (f.get('stripe_' + o) || '').toString().trim()));
      s.autopilot = !!form.autopilot.checked; S.save(); afterAction('Réglages enregistrés ✓');
    };
    const imp = root.querySelector('#imp');
    if (imp) imp.onchange = () => { const r = new FileReader(); r.onload = () => { try { const j = JSON.parse(r.result); if (j.v !== 1) throw new Error(); localStorage.setItem('declic.db.v1', JSON.stringify(j)); location.reload(); } catch (e) { U.toast('Fichier invalide', 'err'); } }; r.readAsText(imp.files[0]); };
  }

  function badgeCount() { return todos().length; }
  window.AdminViews = { dashboard, todoView, pipeline, clientsList, clientDetail, launch, library, emails, finance, settings, bindSettings, badgeCount };
})();
