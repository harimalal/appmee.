/* ============================================================
   DÉCLIC — Moteur d'automatisation
   Chaque case cochée → étape suivante, ressources débloquées,
   emails programmés, factures, tâches pour Claire.
   ============================================================ */
(function () {
  'use strict';
  const D = window.DECLIC, S = window.Store;
  const db = () => S.get();
  const DAY = 86400000;

  const stageIndex = (id) => D.STAGES.findIndex((s) => s.id === id);
  const stageById = (id) => D.STAGES.find((s) => s.id === id);
  const offerOf = (c) => (c.offerId ? D.OFFERS[c.offerId] : null);
  const isDone = (c, t) => !!c.done[t];
  const fullName = (c) => [c.prenom, c.nom].filter(Boolean).join(' ');
  const appLink = (hash) => new URL('app.html#' + (hash || '/me'), location.href).href;
  const money = (n) => new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n || 0);
  const dateFr = (iso, withTime) => iso ? new Date(iso).toLocaleString('fr-FR', withTime ? { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' } : { day: 'numeric', month: 'short', year: 'numeric' }) : '—';

  /* ---------- Statut dérivé ---------- */
  function status(c) {
    if (c.lost) return 'perdue';
    if (c.stage === 'ensuite') return 'alumni';
    if (['onboarding', 'programme', 'bilan'].includes(c.stage)) return 'cliente';
    if (c.stage === 'decision' || c.done.book_call || c.done.prequal) return 'prospect';
    return 'lead';
  }

  /* ---------- Création d'une prospecte ---------- */
  async function createLead(o) {
    const d = db();
    const email = String(o.email || '').trim().toLowerCase();
    if (o.password && d.users.some((u) => u.email === email)) throw new Error('Un compte existe déjà avec cet email. Connecte-toi.');
    if (d.clients.some((c) => c.email === email)) throw new Error('Cette personne existe déjà dans la base.');
    const c = {
      id: S.uid('c'), prenom: o.prenom, nom: o.nom || '', email, phone: o.phone || '', source: o.source || 'Site',
      createdAt: S.now(), stage: 'decouverte', offerId: null, done: {}, answers: {}, unlocked: [], sessions: [],
      appts: [], notes: [], checklist: {}, signed: null, payPending: false, lost: false, quiz: o.quiz || null,
      referrer: o.referrer || null, refCode: Math.random().toString(36).slice(2, 8).toUpperCase(), lastActivity: S.now(),
    };
    d.clients.push(c);
    if (o.password) await S.addUser({ email, password: o.password, role: 'client', clientId: c.id });
    if (c.referrer) {
      const r = d.clients.find((x) => x.refCode === c.referrer);
      if (r) { d.refs.push({ id: S.uid('r'), fromId: r.id, toId: c.id, at: S.now() }); S.log(r.id, `${c.prenom} est arrivée grâce à ${r.prenom} (recommandation)`, 'ref'); }
    }
    S.log(c.id, `Nouvelle prospecte : ${fullName(c)} (${c.source})`, 'lead');
    // Séquence de bienvenue (s'arrête dès que l'appel est réservé)
    D.WELCOME_SEQUENCE.forEach(([key, days]) => queueMail(c, key, { days, unlessDone: 'book_call' }));
    complete(c.id, 'quiz', null, { silent: true });
    S.save();
    return c;
  }

  /* ---------- Emails ---------- */
  function render(str, vars) { return String(str).replace(/\{\{(\w+)\}\}/g, (_, k) => (vars[k] !== undefined ? vars[k] : '')); }
  function mailVars(c, extra) {
    const o = offerOf(c);
    return Object.assign({ prenom: c.prenom, offre: o ? o.name : '', prix: o ? money(o.price) : '', lien: appLink('/me'), claire: db().settings.owner, date: '', n: '', theme: '', notes: '' }, extra || {});
  }
  function queueMail(c, key, opts) {
    opts = opts || {};
    const t = D.EMAILS[key]; if (!t) return;
    const vars = mailVars(c, opts.vars);
    const sendAt = opts.at ? new Date(opts.at).toISOString() : new Date(S.nowDate().getTime() + (opts.days || 0) * DAY).toISOString();
    db().outbox.push({
      id: S.uid('m'), clientId: c.id, key, to: c.email, subject: render(t.subject, vars), body: render(t.body, vars),
      createdAt: S.now(), sendAt, status: 'scheduled', unlessDone: opts.unlessDone || null,
    });
  }
  async function deliver(m) {
    m.status = 'sent'; m.sentAt = S.now();
    const url = db().settings.mailWebhook;
    if (url) { try { await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ to: m.to, subject: m.subject, body: m.body }) }); m.real = true; } catch (e) { m.real = false; } }
    S.log(m.clientId, `Email envoyé : « ${m.subject} »`, 'mail');
  }
  // À appeler au chargement et périodiquement : envoie ce qui est dû
  async function tick() {
    const d = db(); const nowMs = S.nowDate().getTime(); let changed = false;
    for (const m of d.outbox) {
      if (m.status !== 'scheduled' && m.status !== 'review') continue;
      if (new Date(m.sendAt).getTime() > nowMs) continue;
      const c = S.clientById(m.clientId);
      if (!c || (m.unlessDone && c.done[m.unlessDone])) { m.status = 'cancelled'; changed = true; continue; }
      if (d.settings.autopilot) { await deliver(m); changed = true; } else if (m.status === 'scheduled') { m.status = 'review'; changed = true; }
    }
    if (changed) S.save();
    return changed;
  }
  async function sendNow(id) { const m = db().outbox.find((x) => x.id === id); if (m && m.status !== 'sent') { await deliver(m); S.save(); } }
  function cancelMail(id) { const m = db().outbox.find((x) => x.id === id); if (m && m.status !== 'sent') { m.status = 'cancelled'; S.save(); } }

  /* ---------- Ressources ---------- */
  function unlock(c, ids) {
    (ids || []).forEach((id) => { if (!c.unlocked.includes(id)) { c.unlocked.push(id); S.log(c.id, `Ressource débloquée pour ${c.prenom} : ${D.RESOURCES[id].title}`, 'unlock'); } });
  }

  /* ---------- Cœur : cocher une case ---------- */
  function findTask(tid) { for (const s of D.STAGES) { const t = s.tasks.find((x) => x.id === tid); if (t) return { stage: s, task: t }; } return null; }

  function complete(cid, tid, payload, opts) {
    const c = S.clientById(cid); const f = findTask(tid);
    if (!c || !f || c.done[tid]) return c;
    const { task } = f;
    c.done[tid] = S.now(); c.lastActivity = S.now();
    if (task.form && payload) { c.answers[task.form] = payload; if (task.form === 'prequal') c.score = scorePrequal(payload); }
    if (task.id === 'checklist1' && payload) c.checklist.checklist1 = payload;
    unlock(c, task.unlock);
    (task.mail || []).forEach((k) => queueMail(c, k));
    if (!opts || !opts.silent) S.log(c.id, `${task.who === 'coach' ? 'Claire' : c.prenom} a validé : ${task.label}`, 'task');
    advance(c);
    S.save();
    return c;
  }

  // Annule une case (utile pour corriger une erreur côté coach)
  function undo(cid, tid) { const c = S.clientById(cid); if (c && c.done[tid]) { delete c.done[tid]; S.save(); } }

  function requiredDone(c, stage) {
    return stage.tasks.filter((t) => !t.optional).every((t) => (t.kind === 'session' ? sessionsAllDone(c) : isDone(c, t.id)));
  }
  function advance(c) {
    let guard = 0;
    while (guard++ < 8) {
      const st = stageById(c.stage); const i = stageIndex(c.stage);
      if (st.id === 'ensuite' || i >= D.STAGES.length - 1 || !requiredDone(c, st)) break;
      c.stage = D.STAGES[i + 1].id;
      enter(c, D.STAGES[i + 1]);
    }
  }
  function enter(c, st) {
    S.log(c.id, `${c.prenom} passe à l’étape « ${st.label} »`, 'stage');
    if (st.onEnter) { unlock(c, st.onEnter.unlock); (st.onEnter.mail || []).forEach((k) => queueMail(c, k)); }
    if (st.id === 'programme') initSessions(c);
    if (st.id === 'ensuite') { c.completedAt = S.now(); queueMail(c, 'reactivation', { days: 90 }); }
  }

  /* ---------- Appel découverte → proposition ---------- */
  function proposeOffer(cid, offerId) {
    const c = S.clientById(cid); if (!c) return;
    c.offerId = offerId; c.proposedAt = S.now();
    unlock(c, ['proposition']);
    queueMail(c, 'proposition');
    queueMail(c, 'relance48', { days: 2, unlessDone: 'sign' });
    queueMail(c, 'relance5j', { days: 5, unlessDone: 'sign' });
    complete(cid, 'prep_call', null, { silent: true });
    complete(cid, 'call_done');
    // Claire a décidé : on avance même si la cliente n'a pas tout coché en amont
    if (c.stage === 'decouverte') { c.stage = 'decision'; enter(c, stageById('decision')); S.save(); }
  }

  /* ---------- Contrat, paiement, factures ---------- */
  function sign(cid, name) {
    const c = S.clientById(cid); if (!c || c.done.sign) return;
    c.signed = { name, at: S.now() };
    complete(cid, 'sign');
  }
  function nextInvoiceNumber() { const y = S.nowDate().getFullYear(); return `F-${y}-${String(db().invoices.length + 1).padStart(4, '0')}`; }
  function addInvoice(c, label, amount, status, dueAt, extra) {
    const inv = Object.assign({ id: S.uid('i'), number: nextInvoiceNumber(), clientId: c.id, label, amount, status, issuedAt: S.now(), dueAt: dueAt || S.now(), paidAt: status === 'paid' ? S.now() : null }, extra || {});
    db().invoices.push(inv); return inv;
  }
  function pay(cid, mode, opts) {
    const c = S.clientById(cid); const o = offerOf(c); if (!c || !o || c.done.pay) return;
    const pending = !!(opts && opts.pending); const status = pending ? 'due' : 'paid';
    if (mode === 'inst' && o.installments) {
      const { n, amount } = o.installments;
      for (let i = 0; i < n; i++) {
        const due = new Date(S.nowDate().getTime() + i * 30 * DAY).toISOString();
        addInvoice(c, `${o.name} — échéance ${i + 1}/${n}`, amount, i === 0 ? status : 'due', due, { mode: 'inst' });
      }
    } else addInvoice(c, o.name, o.price, status, null, { mode: 'full' });
    c.payMode = mode;
    if (pending) { c.payPending = true; S.log(c.id, `${c.prenom} a demandé à régler via le lien de paiement`, 'pay'); S.save(); return; }
    complete(cid, 'pay');
  }
  function markPaid(invId) {
    const inv = db().invoices.find((i) => i.id === invId); if (!inv) return;
    inv.status = 'paid'; inv.paidAt = S.now();
    const c = S.clientById(inv.clientId);
    S.log(inv.clientId, `Paiement reçu : ${money(inv.amount)} (${inv.number})`, 'pay');
    if (c && c.payPending && !c.done.pay) { c.payPending = false; complete(c.id, 'pay'); }
    S.save();
  }
  function subscribeMomentum(cid) {
    const c = S.clientById(cid); if (!c || c.done.momentum) return;
    addInvoice(c, D.OFFERS.momentum.name + ' — mois 1', D.OFFERS.momentum.price, 'due', null, { mode: 'monthly' });
    c.momentum = true;
    complete(cid, 'momentum');
  }
  function referDone(cid) { complete(cid, 'refer'); }

  /* ---------- Rendez-vous ---------- */
  function slots(kind) {
    const taken = new Set(); db().clients.forEach((c) => (c.appts || []).forEach((a) => taken.add(a.date)));
    db().clients.forEach((c) => (c.sessions || []).forEach((s) => s.date && taken.add(s.date)));
    const out = []; const base = S.nowDate();
    for (let i = 1; out.length < 36 && i < 30; i++) {
      const d = new Date(base.getTime() + i * DAY); const wd = d.getDay();
      if (wd === 0 || (wd === 6 && kind === 'call')) continue;
      const times = kind === 'call' ? ['10:00', '14:00', '18:30'] : ['09:00', '12:30', '18:00', '20:00'];
      times.forEach((tm) => {
        const [h, m] = tm.split(':'); const x = new Date(d); x.setHours(+h, +m, 0, 0);
        const iso = x.toISOString(); if (!taken.has(iso)) out.push(iso);
      });
    }
    return out;
  }
  function bookCall(cid, iso) {
    const c = S.clientById(cid); if (!c) return;
    c.appts = (c.appts || []).filter((a) => a.kind !== 'call');
    c.appts.push({ id: S.uid('a'), kind: 'call', date: iso, label: 'Appel découverte (30 min)' });
    const d = new Date(iso);
    queueMail(c, 'callreminder', { at: new Date(d.getTime() - DAY), vars: { date: dateFr(iso, true) } });
    if (!c.done.book_call) {
      const t = findTask('book_call').task;
      (t.mail || []).forEach((k) => queueMail(c, k, { vars: { date: dateFr(iso, true) } }));
      c.done.book_call = S.now(); c.lastActivity = S.now();
      S.log(c.id, `${c.prenom} a réservé son appel : ${dateFr(iso, true)}`, 'task');
      advance(c);
    } else S.log(c.id, `${c.prenom} a déplacé son appel : ${dateFr(iso, true)}`, 'task');
    S.save();
  }

  /* ---------- Séances ---------- */
  function initSessions(c) {
    const o = offerOf(c); if (!o || c.sessions.length) return;
    c.sessions = o.sessions.map((s, i) => ({ n: i + 1, theme: s.theme, minutes: s.minutes, state: i === 0 ? 'bookable' : 'locked', date: null, notes: '', exoDone: [], exoUnlocked: false }));
  }
  function sessionsAllDone(c) { return c.sessions.length > 0 && c.sessions.every((s) => s.state === 'done'); }
  function bookSession(cid, n, iso) {
    const c = S.clientById(cid); const s = c && c.sessions[n - 1]; if (!s || s.state === 'locked' || s.state === 'done') return;
    s.date = iso; s.state = 'booked'; c.lastActivity = S.now();
    S.log(c.id, `${c.prenom} a réservé la séance ${n} : ${dateFr(iso, true)}`, 'task'); S.save();
  }
  function completeSession(cid, n, notes) {
    const c = S.clientById(cid); const s = c && c.sessions[n - 1]; if (!s || s.state === 'done') return;
    s.state = 'done'; s.doneAt = S.now(); s.notes = notes || ''; s.exoUnlocked = true;
    const nxt = c.sessions[n]; if (nxt && nxt.state === 'locked') nxt.state = 'bookable';
    queueMail(c, 'session_cr', { vars: { n, theme: s.theme, notes: s.notes || '• Les points clés de la séance sont dans ton espace.' } });
    queueMail(c, 'exos_nudge', { days: 3, vars: { n } });
    S.log(c.id, `Séance ${n} réalisée (${s.theme}) — exercices débloqués, compte-rendu envoyé`, 'session');
    c.lastActivity = S.now();
    if (sessionsAllDone(c)) { c.done.sessions = S.now(); advance(c); }
    S.save();
  }
  function toggleExercise(cid, n, idx) {
    const c = S.clientById(cid); const s = c && c.sessions[n - 1]; if (!s) return;
    const i = s.exoDone.indexOf(idx); if (i >= 0) s.exoDone.splice(i, 1); else s.exoDone.push(idx);
    c.lastActivity = S.now(); S.save();
  }
  function midpointSession(c) { return Math.ceil(c.sessions.length / 2); }
  function submitMid(cid, answers) { const c = S.clientById(cid); if (c) { c.answers.mid = answers; S.log(c.id, `${c.prenom} a rempli son bilan de mi-parcours`, 'task'); S.save(); } }

  /* ---------- Score, notes, divers ---------- */
  function scorePrequal(a) {
    let s = 0;
    s += Math.min(10, +a.urgency || 0) * 5; // 50
    const b = { 'Moins de 500 €': 5, '500 – 1 000 €': 15, '1 000 – 2 000 €': 25, 'Plus de 2 000 € si la valeur est là': 30, 'Je ne sais pas encore': 12 }; s += b[a.budget] || 10;
    s += a.decider === 'M’appartient entièrement' ? 20 : 10;
    return Math.min(100, s);
  }
  function addNote(cid, text) { const c = S.clientById(cid); if (c && text.trim()) { c.notes.unshift({ t: S.now(), text: text.trim() }); S.save(); } }
  function markLost(cid, lost) { const c = S.clientById(cid); if (c) { c.lost = !!lost; S.log(cid, lost ? `${c.prenom} marquée comme perdue` : `${c.prenom} réactivée`, 'info'); S.save(); } }

  /* ---------- Documents générés ---------- */
  function genProposition(c) {
    const o = offerOf(c); if (!o) return '*Ta proposition sera prête après notre appel.*';
    const s = db().settings;
    const pay = o.installments ? `**${money(o.price)}** comptant, ou **${o.installments.n} × ${money(o.installments.amount)}**` : `**${money(o.price)}**${o.perMonth ? ' / mois' : ''}`;
    return `# Proposition d’accompagnement pour ${c.prenom}\n\n*Préparée par ${s.owner} — ${dateFr(c.proposedAt || S.now())}*\n\n## Ce que nous avons identifié ensemble\n${(c.answers.prequal && c.answers.prequal.situation) ? '> ' + c.answers.prequal.situation + '\n' : '> Tes blocages, tes désirs et ta prochaine étape ont été clarifiés pendant notre appel.\n'}\n## Mon accompagnement : ${o.name}\n${o.pitch}\n\n**Format :** ${o.duration}\n\n### Ce qui est inclus\n${o.includes.map((x) => '- ' + x).join('\n')}\n\n### Investissement\n${pay}\n\n### Ma garantie\n« Satisfaction ou remboursement » : si après les 2 premières séances tu ne ressens pas de valeur, je te rembourse intégralement.\n\n### Pour démarrer\nIl te reste à **accepter les conditions**, puis à **régler** : ton espace se débloque aussitôt.`;
  }
  function genContract(c) {
    const o = offerOf(c); const s = db().settings; if (!o) return '';
    const total = o.installments ? `${money(o.price)} comptant ou ${o.installments.n} × ${money(o.installments.amount)}` : money(o.price);
    return `# Contrat de prestation de coaching individuel\n\n**Le Prestataire :** ${s.owner} — ${s.status}${s.siret ? ' — SIRET ' + s.siret : ''}${s.address ? ' — ' + s.address : ''} — ${s.email}\n\n**La Cliente :** ${fullName(c)} — ${c.email}\n\n## Article 1 — Objet\nPrestations de coaching individuel. Le coaching est un accompagnement visant à atteindre des objectifs et à passer à l’action. **Il ne constitue pas une thérapie, ni un conseil psychologique, médical, juridique ou financier.**\n\n## Article 2 — Prestation\n**Formule :** ${o.name}. **Contenu :** ${o.duration}.\n${o.includes.map((x) => '- ' + x).join('\n')}\n\n## Article 3 — Obligations du Prestataire\nConduire les séances avec professionnalisme, bienveillance et confidentialité ; adapter son approche à la personnalité et au rythme de la Cliente ; respecter le Code de déontologie des coachs.\n\n## Article 4 — Obligations de la Cliente\nParticiper activement, être ponctuelle, régler les honoraires. Les résultats dépendent de son engagement personnel.\n\n## Article 5 — Tarifs\nMontant total : **${total}**${s.tva ? ' (' + s.tva + ')' : ''}.\n\n## Article 6 — Annulation et report\nReport sans frais jusqu’à 24 h avant la séance. En deçà, la séance est décomptée sauf cas de force majeure.\n\n## Article 7 — Droit de rétractation\n14 jours à compter de la signature, par email à ${s.email}. Si la Cliente demande un démarrage avant l’expiration du délai, elle renonce à ce droit pour les séances déjà effectuées.\n\n## Article 8 — Garantie satisfaction\nSi après la séance 2 la Cliente estime que l’accompagnement ne lui convient pas, elle est remboursée intégralement.\n\n## Article 9 — Confidentialité\nStricte confidentialité sur tout ce qui est partagé en séance. Des éléments anonymisés ne peuvent être utilisés qu’avec accord de la Cliente.\n\n## Article 10 — Propriété intellectuelle\nLes outils, méthodes et documents fournis restent la propriété du Prestataire.\n\n*Modèle à faire relire par un juriste avant usage commercial.*`;
  }
  function genRoadmap(c) {
    const o = offerOf(c); if (!o) return '';
    const rows = o.sessions.map((s, i) => `| ${i + 1} | ${s.theme} | ${s.minutes} min | ${c.sessions[i] && c.sessions[i].date ? dateFr(c.sessions[i].date, true) : 'À réserver'} |`).join('\n');
    return `# Ma feuille de route — ${o.name}\n\n**Objectif de transformation :** ${(c.answers.onboarding && c.answers.onboarding.success) || 'défini avec Claire à la séance 1'}\n\n| Séance | Thème | Durée | Date |\n|---|---|---|---|\n${rows}\n\n## Jalons\n- **Séance 1** — premier diagnostic, premiers déclics\n- **À mi-parcours (séance ${Math.ceil(o.sessions.length / 2)})** — bilan rapide et ajustement\n- **Dernière séance** — ancrage et plan à 6 mois`;
  }
  function genParrainage(c) {
    const link = new URL('index.html?ref=' + c.refCode, location.href).href;
    return `# Mon kit de recommandation\n\nMerci d’avoir confiance en Déclic. Si une amie a besoin de ce déclic, voici tout ce qu’il te faut.\n\n## Ton lien personnel\n\`${link}\`\n\n## Message prêt à copier\n> Coucou, j’ai fait un accompagnement avec Claire (Déclic) et ça m’a vraiment aidée à avancer sur mon projet. Elle propose un appel découverte gratuit de 30 minutes, sans engagement. Si ça te tente : ${link}\n\n## Comment ça marche\n1. Ton amie fait le quiz et réserve son appel avec ton lien.\n2. Tu es prévenue dès qu’elle démarre.\n3. Remerciement de Claire à chaque recommandation aboutie.`;
  }

  window.Engine = { stageIndex, stageById, offerOf, isDone, fullName, appLink, money, dateFr, status, createLead, queueMail, tick, sendNow, cancelMail, unlock, complete, undo, requiredDone, proposeOffer, sign, pay, markPaid, subscribeMomentum, referDone, slots, bookCall, initSessions, sessionsAllDone, bookSession, completeSession, toggleExercise, midpointSession, submitMid, scorePrequal, addNote, markLost, genProposition, genContract, genRoadmap, genParrainage, findTask, advance, render, addInvoice };
})();
