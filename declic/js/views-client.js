/* Portail cliente : parcours guidé, ressources, séances, factures */
(function () {
  'use strict';
  const D = window.DECLIC, S = window.Store, E = window.Engine, U = window.UI, V = window.Views;
  const { esc } = U;
  const A = (window.Actions = window.Actions || {});
  const NEEDS = { book_call: 'prequal', sign: 'read_prop', pay: 'sign' };

  const cid = () => window.App.clientId();
  const me = () => S.clientById(cid());

  // Exécute une action, puis re-rend et célèbre un changement d'étape
  function run(fn) {
    const before = me().stage; fn(); const after = me().stage;
    window.App.render();
    if (before !== after) {
      const st = E.stageById(after);
      U.toast(`🎉 Étape franchie ! Bienvenue dans « ${st.label} »`, 'win');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  function taskAvailable(c, t) { const n = NEEDS[t.id]; return !n || E.isDone(c, n); }

  function sessionMini(c) {
    if (!c.sessions.length) return '<p class="muted">Tes séances apparaîtront dès que ton onboarding sera terminé.</p>';
    const done = c.sessions.filter((s) => s.state === 'done').length;
    return `<div class="bar"><i style="width:${Math.round(done / c.sessions.length * 100)}%"></i></div><p class="muted">${done} / ${c.sessions.length} séances réalisées · <a href="#/me/seances">Voir mes séances</a></p>`;
  }

  function taskRow(c, t) {
    const done = E.isDone(c, t.id) || (t.kind === 'session' && E.sessionsAllDone(c));
    const coach = t.who === 'coach';
    if (coach && t.id === 'prep_call') return '';
    const avail = taskAvailable(c, t);
    let action = '';
    if (done) action = `<span class="done-at">${t.kind === 'session' ? '' : '✓ ' + E.dateFr(c.done[t.id])}</span>`;
    else if (coach) action = '<span class="wait">⏳ Claire s’en occupe</span>';
    else if (!avail) action = '<span class="wait">Après l’étape précédente</span>';
    else {
      const lab = { read: 'Ouvrir', form: 'Remplir', book: 'Choisir un créneau', sign: 'Lire et signer', pay: 'Régler', check: 'Valider', choose: 'Oui, je continue', refer: 'Voir mon kit', session: 'Mes séances' }[t.kind] || 'Faire';
      if (t.kind === 'checklist') action = '';
      else if (t.kind === 'session') action = `<a class="btn sm" href="#/me/seances">Mes séances</a>`;
      else action = `<button class="btn sm" data-act="task" data-t="${t.id}">${lab}</button>`;
    }
    let extra = '';
    if (t.kind === 'checklist' && !done && avail) {
      const ck = c.checklist.checklist1h || [];
      extra = `<div class="checks">${t.items.map((it, i) => `<label class="opt"><input type="checkbox" data-act="ck" data-i="${i}" ${ck.includes(i) ? 'checked' : ''}><span>${esc(it)}</span></label>`).join('')}</div>`;
    }
    if (t.kind === 'session') extra = sessionMini(c);
    if (t.id === 'book_call' && done) { const a = (c.appts || []).find((x) => x.kind === 'call'); if (a) extra = `<p class="muted">📅 ${E.dateFr(a.date, true)} · <button class="link" data-act="task" data-t="book_call">Déplacer</button></p>`; }
    if (t.id === 'pay' && !done && c.payPending) action = '<span class="wait">⏳ Paiement en cours de confirmation</span>';
    return `<li class="task ${done ? 'is-done' : ''} ${coach ? 'is-coach' : ''}"><span class="box" aria-hidden="true">${done ? '✓' : coach ? '⏳' : ''}</span><div class="t-main"><div class="t-label">${esc(t.label)}${t.optional ? ' <span class="tag">facultatif</span>' : ''}</div>${t.hint ? `<div class="t-hint">${esc(t.hint)}</div>` : ''}${extra}</div><div class="t-act">${action}</div></li>`;
  }

  function stepper(c) {
    const cur = E.stageIndex(c.stage);
    return `<ol class="stepper">${D.STAGES.map((s, i) => `<li class="${i < cur ? 'done' : i === cur ? 'cur' : 'pend'}"><span class="dot">${i < cur ? '✓' : s.icon}</span><span class="s-l">${esc(s.label)}</span></li>`).join('')}</ol>`;
  }

  function nextAction(c) {
    const st = E.stageById(c.stage);
    const t = st.tasks.find((x) => x.who === 'client' && !x.optional && !E.isDone(c, x.id) && x.kind !== 'session' && taskAvailable(c, x));
    if (st.id === 'programme') {
      const s = c.sessions.find((x) => x.state === 'bookable' || x.state === 'booked');
      if (s) return `<div class="next"><div><div class="eyebrow">Prochaine action</div><h2>Séance ${s.n} · ${esc(s.theme)}</h2><p class="muted">${s.state === 'booked' ? '📅 ' + E.dateFr(s.date, true) : 'Réserve ton créneau.'}</p></div><a class="btn" href="#/me/seances">${s.state === 'booked' ? 'Voir ma séance' : 'Réserver'}</a></div>`;
    }
    if (st.id === 'ensuite') return `<div class="next"><div><div class="eyebrow">Bravo</div><h2>Tu as terminé ton parcours 🌳</h2><p class="muted">Garde l’élan avec MOMENTUM ou partage Déclic à une amie.</p></div></div>`;
    if (!t) return `<div class="next wait"><div><div class="eyebrow">En cours</div><h2>Claire prépare la suite pour toi</h2><p class="muted">Tu seras prévenue par email dès que c’est prêt.</p></div></div>`;
    return `<div class="next"><div><div class="eyebrow">Prochaine action</div><h2>${esc(t.label)}</h2><p class="muted">${esc(t.hint || '')}</p></div><button class="btn" data-act="task" data-t="${t.id}">Y aller</button></div>`;
  }

  function parcours(c) {
    const cur = E.stageIndex(c.stage);
    const o = E.offerOf(c);
    const blocks = D.STAGES.map((s, i) => {
      if (i > cur) return `<section class="stage locked"><header><span class="s-ico">🔒</span><div><h3>${esc(s.label)}</h3><p class="muted">${esc(s.promise)}</p></div></header></section>`;
      const done = i < cur;
      return `<section class="stage ${done ? 'finished' : 'current'}"><header><span class="s-ico">${done ? '✓' : s.icon}</span><div><h3>${esc(s.label)}</h3><p class="muted">${esc(s.promise)}</p></div></header><ul class="tasks">${s.tasks.map((t) => taskRow(c, t)).join('')}</ul></section>`;
    });
    // Étapes terminées repliées
    const html = blocks.map((b, i) => i < cur ? `<details class="fold">${b.replace('<section class="stage finished">', '<summary class="fold-s">').replace('</header><ul', '</header></summary><ul').replace('</ul></section>', '</ul>')}</details>` : b).join('');
    return `<div class="hello"><h1>Bonjour ${esc(c.prenom)} 🌸</h1><p class="muted">${o ? esc(o.name) + ' · ' : ''}${esc(D.BRAND.tagline)}</p></div>${stepper(c)}${nextAction(c)}${html}`;
  }

  /* ---------- Ressources ---------- */
  function ressources(c) {
    const items = Object.entries(D.RESOURCES).filter(([, r]) => r.audience !== 'coach').map(([id, r]) => {
      const open = c.unlocked.includes(id); const stg = E.stageById(r.stage);
      return `<button class="res ${open ? '' : 'locked'}" ${open ? `data-act="res" data-id="${id}"` : 'disabled'}><span class="res-i">${open ? r.icon : '🔒'}</span><span class="res-t">${esc(r.title)}</span><span class="res-s">${open ? 'Ouvrir' : 'Se débloque : « ' + esc(stg.label) + ' »'}</span></button>`;
    }).join('');
    const exos = c.sessions.filter((s) => s.exoUnlocked).map((s) => `<a class="res" href="#/me/seances"><span class="res-i">🧰</span><span class="res-t">Exercices séance ${s.n}</span><span class="res-s">${esc(s.theme)}</span></a>`).join('');
    const locked = c.sessions.filter((s) => !s.exoUnlocked).slice(0, 3).map((s) => `<div class="res locked"><span class="res-i">🔒</span><span class="res-t">Exercices séance ${s.n}</span><span class="res-s">Après la séance ${s.n}</span></div>`).join('');
    return `<h1>Mes ressources</h1><p class="muted">Elles se débloquent au fil de ton parcours.</p><div class="res-grid">${items}${exos}${locked}</div>`;
  }

  /* ---------- Séances ---------- */
  function seances(c) {
    if (!c.sessions.length) return `<h1>Mes séances</h1><div class="empty"><p>Tes séances apparaîtront ici dès que tu auras réglé ton accompagnement et terminé l’onboarding.</p><a class="btn" href="#/me">Retour à mon parcours</a></div>`;
    const mid = E.midpointSession(c);
    const cards = c.sessions.map((s) => {
      const exo = D.EXERCISES[s.theme] || [];
      let action = '';
      if (s.state === 'bookable') action = `<button class="btn sm" data-act="bookS" data-n="${s.n}">Réserver</button>`;
      else if (s.state === 'booked') action = `<span class="badge">📅 ${E.dateFr(s.date, true)}</span> <button class="link" data-act="bookS" data-n="${s.n}">Déplacer</button>`;
      else if (s.state === 'done') action = `<span class="badge ok">Réalisée ${E.dateFr(s.doneAt)}</span>`;
      else action = '<span class="badge">🔒 Après la séance précédente</span>';
      const body = s.state === 'done' ? `${s.notes ? `<div class="cr"><strong>Compte-rendu</strong><p>${esc(s.notes)}</p></div>` : ''}<div class="exos"><strong>Mes exercices</strong>${exo.map((x, i) => `<label class="opt"><input type="checkbox" data-act="exo" data-n="${s.n}" data-i="${i}" ${s.exoDone.includes(i) ? 'checked' : ''}><span>${esc(x)}</span></label>`).join('')}</div>` : '';
      const midCard = s.n === mid && s.state === 'done' ? (c.answers.mid ? '<p class="muted">✓ Bilan de mi-parcours envoyé.</p>' : '<button class="btn sm ghost" data-act="mid">Faire mon bilan de mi-parcours (3 min)</button>') : '';
      return `<article class="sess ${s.state}"><header><span class="sess-n">${s.n}</span><div><h3>${esc(s.theme)}</h3><p class="muted">${s.minutes} min</p></div><div class="sess-a">${action}</div></header>${body}${midCard}</article>`;
    }).join('');
    return `<h1>Mes séances</h1>${sessionMini(c)}<div class="sess-list">${cards}</div>`;
  }

  /* ---------- Factures ---------- */
  function factures(c) {
    const inv = S.get().invoices.filter((i) => i.clientId === c.id);
    if (!inv.length) return `<h1>Mes paiements</h1><div class="empty"><p>Tes factures apparaîtront ici après ton premier règlement.</p></div>`;
    return `<h1>Mes paiements</h1><div class="card"><table class="list"><tr><th>N°</th><th>Libellé</th><th>Montant</th><th>Statut</th><th></th></tr>${inv.map((i) => `<tr><td>${esc(i.number)}</td><td>${esc(i.label)}</td><td>${E.money(i.amount)}</td><td><span class="badge ${i.status === 'paid' ? 'ok' : 'warn'}">${i.status === 'paid' ? 'Payée' : 'À régler ' + E.dateFr(i.dueAt)}</span></td><td><button class="link" data-act="inv" data-id="${i.id}">Voir</button></td></tr>`).join('')}</table></div>`;
  }

  /* ---------- Actions ---------- */
  A.task = (d) => {
    const c = me(); const f = E.findTask(d.t); if (!f) return; const t = f.task;
    if (t.kind === 'read') {
      const body = V.resourceBody(c, t.resource);
      const m = V.openDoc(D.RESOURCES[t.resource].title, body, E.isDone(c, t.id) ? '' : '<button class="btn" data-ok>J’ai lu — continuer</button>');
      const b = m.el.querySelector('[data-ok]'); if (b) b.onclick = () => { m.close(); run(() => E.complete(c.id, t.id)); };
    } else if (t.kind === 'form') V.openForm(t.form, c.answers[t.form], (ans) => run(() => E.complete(c.id, t.id, ans)));
    else if (t.kind === 'book') V.openSlots('call', 'Réserver mon appel découverte (30 min)', (iso) => run(() => E.bookCall(c.id, iso)));
    else if (t.kind === 'sign') {
      const m = V.openDoc('Contrat et conditions', V.resourceBody(c, 'contrat'), `<label class="opt"><input type="checkbox" id="sg-ok"><span>J’ai lu et j’accepte le contrat, les conditions générales et la garantie.</span></label><div class="fld"><label class="lbl">Tape ton nom complet pour signer</label><input class="inp" id="sg-name" placeholder="${esc(E.fullName(c))}"></div><div class="err" id="sg-err"></div><button class="btn" data-ok>Signer</button>`);
      m.el.querySelector('[data-ok]').onclick = () => {
        const ok = m.el.querySelector('#sg-ok').checked; const nm = m.el.querySelector('#sg-name').value.trim();
        if (!ok || nm.length < 3) { m.el.querySelector('#sg-err').textContent = 'Coche la case et tape ton nom pour signer.'; return; }
        m.close(); run(() => E.sign(c.id, nm));
      };
    } else if (t.kind === 'pay') openPay(c);
    else if (t.kind === 'choose') run(() => E.subscribeMomentum(c.id));
    else if (t.kind === 'refer') { const m = V.openDoc('Mon kit de recommandation', V.resourceBody(c, 'parrainage'), '<button class="btn" data-ok>J’ai partagé mon lien</button>'); m.el.querySelector('[data-ok]').onclick = () => { m.close(); run(() => E.referDone(c.id)); }; }
    else if (t.kind === 'check') run(() => E.complete(c.id, t.id));
  };
  function openPay(c) {
    const o = E.offerOf(c); const st = S.get().settings; const link = st.stripe && st.stripe[o.id];
    const opt = (v, t, p) => `<label class="payopt"><input type="radio" name="pm" value="${v}" ${v === 'full' ? 'checked' : ''}><span><strong>${t}</strong><br><span class="muted">${p}</span></span></label>`;
    const m = U.modal(`<h2 class="modal-title">Régler ${esc(o.name)}</h2><div class="pay">${opt('full', 'Comptant', E.money(o.price))}${o.installments ? opt('inst', `En ${o.installments.n} fois`, `${o.installments.n} × ${E.money(o.installments.amount)}`) : ''}</div>${link ? '<p class="muted">Tu seras redirigée vers le paiement sécurisé. Claire confirme dès réception.</p>' : '<p class="muted">🧪 Mode démonstration : aucun prélèvement réel.</p>'}<div class="row end"><button class="btn ghost" data-no>Annuler</button><button class="btn" data-ok>${link ? 'Aller au paiement sécurisé' : 'Payer (démo)'}</button></div>`);
    m.el.querySelector('[data-no]').onclick = m.close;
    m.el.querySelector('[data-ok]').onclick = () => {
      const mode = m.el.querySelector('input[name=pm]:checked').value; m.close();
      if (link) { window.open(link, '_blank', 'noopener'); run(() => E.pay(c.id, mode, { pending: true })); } else run(() => E.pay(c.id, mode));
    };
  }
  A.ck = (d, el) => {
    const c = me(); const t = E.findTask('checklist1').task; const ck = new Set(c.checklist.checklist1h || []);
    el.checked ? ck.add(+d.i) : ck.delete(+d.i); c.checklist.checklist1h = [...ck]; S.save();
    if (ck.size === t.items.length) run(() => E.complete(c.id, 'checklist1', [...ck])); else window.App.render();
  };
  A.res = (d) => { const c = me(); const r = D.RESOURCES[d.id]; V.openDoc(r.title, V.resourceBody(c, d.id)); };
  A.bookS = (d) => { const c = me(); V.openSlots('session', `Réserver la séance ${d.n}`, (iso) => run(() => E.bookSession(c.id, +d.n, iso))); };
  A.exo = (d) => { E.toggleExercise(cid(), +d.n, +d.i); window.App.render(); };
  A.mid = () => { const c = me(); V.openForm('mid', c.answers.mid, (a) => run(() => E.submitMid(c.id, a))); };
  A.inv = (d) => V.openInvoice(S.get().invoices.find((i) => i.id === d.id));

  window.ClientViews = { parcours, ressources, seances, factures };
})();
