/* Vues partagées : ressources, formulaires, créneaux */
(function () {
  'use strict';
  const D = window.DECLIC, S = window.Store, E = window.Engine, U = window.UI;
  const { esc } = U;

  function tplBody(id, c) {
    const t = window.TEMPLATES[id]; if (!t) return '';
    return t.md.replace(/\{\{prenom\}\}/g, c ? c.prenom : '[Prénom]');
  }

  function resourceBody(c, id) {
    const r = D.RESOURCES[id];
    if (id === 'guide') return D.GUIDE_MD;
    if (id === 'proposition') return E.genProposition(c);
    if (id === 'contrat') return E.genContract(c);
    if (id === 'roadmap') return E.genRoadmap(c);
    if (id === 'parrainage') return E.genParrainage(c);
    if (r && r.type === 'tpl') return tplBody(r.tpl, c);
    return '';
  }

  function openDoc(title, body, footerHtml, opts) {
    const m = U.modal(`<h2 class="modal-title">${esc(title)}</h2><div class="doc md">${U.md(body)}</div>${footerHtml ? `<div class="modal-foot">${footerHtml}</div>` : ''}`, Object.assign({ wide: true }, opts));
    return m;
  }

  /* ---------- Formulaire générique ---------- */
  function openForm(formId, initial, onSubmit, opts) {
    const f = D.FORMS[formId]; initial = initial || {}; opts = opts || {};
    const field = (q) => {
      const v = initial[q.id];
      const name = `f_${q.id}`;
      let ctl = '';
      if (q.type === 'text') ctl = `<input class="inp" name="${name}" value="${esc(v || '')}">`;
      else if (q.type === 'textarea') ctl = `<textarea class="inp" rows="3" name="${name}">${esc(v || '')}</textarea>`;
      else if (q.type === 'choice') ctl = `<div class="opts">${q.options.map((o, i) => `<label class="opt"><input type="radio" name="${name}" value="${esc(o)}" ${v === o ? 'checked' : ''}><span>${esc(o)}</span></label>`).join('')}</div>`;
      else if (q.type === 'multi') ctl = `<div class="opts">${q.options.map((o) => `<label class="opt"><input type="checkbox" name="${name}" value="${esc(o)}" ${(v || []).includes(o) ? 'checked' : ''}><span>${esc(o)}</span></label>`).join('')}</div>`;
      else if (q.type === 'scale') { let s = ''; for (let i = q.min; i <= q.max; i++) s += `<label class="pill"><input type="radio" name="${name}" value="${i}" ${+v === i ? 'checked' : ''}><span>${i}</span></label>`; ctl = `<div class="scale">${s}</div>`; }
      return `<div class="fld"><label class="lbl">${esc(q.label)}</label>${ctl}</div>`;
    };
    const m = U.modal(`<h2 class="modal-title">${esc(f.title)}</h2><p class="muted">${esc(f.intro)} <span class="tag">${f.minutes} min</span></p><form id="gform" novalidate>${f.fields.map(field).join('')}<div class="err" id="gform-err" role="alert"></div><div class="row end"><button type="button" class="btn ghost" data-cancel>Plus tard</button><button class="btn" type="submit">${esc(opts.submit || 'Valider et continuer')}</button></div></form>`, { wide: true });
    const form = m.el.querySelector('#gform');
    m.el.querySelector('[data-cancel]').onclick = m.close;
    form.onsubmit = (e) => {
      e.preventDefault();
      const ans = {}; let missing = null;
      f.fields.forEach((q) => {
        const els = form.querySelectorAll(`[name="f_${q.id}"]`);
        if (q.type === 'multi') ans[q.id] = [...els].filter((x) => x.checked).map((x) => x.value);
        else if (q.type === 'choice' || q.type === 'scale') { const ch = [...els].find((x) => x.checked); ans[q.id] = ch ? ch.value : ''; }
        else ans[q.id] = els[0].value.trim();
        const empty = !ans[q.id] || (Array.isArray(ans[q.id]) && !ans[q.id].length);
        if (empty && q.type !== 'textarea' && !missing) missing = q;
      });
      if (missing) { form.querySelector('#gform-err').textContent = `Il manque une réponse : « ${missing.label} »`; return; }
      m.close(); onSubmit(ans);
    };
  }

  /* ---------- Sélecteur de créneaux ---------- */
  function openSlots(kind, title, onPick) {
    const all = E.slots(kind); const byDay = {};
    all.forEach((iso) => { const k = iso.slice(0, 10) + '|' + new Date(iso).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' }); (byDay[k] = byDay[k] || []).push(iso); });
    const html = Object.entries(byDay).slice(0, 10).map(([k, arr]) => `<div class="slotday"><div class="slotday-t">${esc(k.split('|')[1])}</div><div class="slotrow">${arr.map((iso) => `<button class="slot" data-iso="${iso}">${new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</button>`).join('')}</div></div>`).join('');
    const m = U.modal(`<h2 class="modal-title">${esc(title)}</h2><p class="muted">Choisis le créneau qui te va — il se déplace d’un clic.</p><div class="slots">${html}</div>`, { wide: true });
    m.el.querySelectorAll('.slot').forEach((b) => (b.onclick = () => { m.close(); onPick(b.dataset.iso); }));
  }

  /* ---------- Facture imprimable ---------- */
  function openInvoice(inv) {
    const c = S.clientById(inv.clientId); const s = S.get().settings;
    const m = U.modal(`<div class="invoice" id="inv-print"><div class="inv-h"><div><strong class="brand-name">Déclic</strong><br>${esc(s.owner)}<br>${esc(s.status)}${s.siret ? '<br>SIRET ' + esc(s.siret) : ''}${s.address ? '<br>' + esc(s.address) : ''}<br>${esc(s.email)}</div><div class="inv-n"><h2>FACTURE</h2><strong>${esc(inv.number)}</strong><br>Émise le ${E.dateFr(inv.issuedAt)}</div></div><div class="inv-to"><strong>Facturée à</strong><br>${esc(E.fullName(c))}<br>${esc(c.email)}</div><table class="inv-t"><tr><th>Désignation</th><th>Montant</th></tr><tr><td>${esc(inv.label)}</td><td>${E.money(inv.amount)}</td></tr><tr class="tot"><td>Total</td><td>${E.money(inv.amount)}</td></tr></table><p class="muted">${esc(s.tva)}</p><p><span class="badge ${inv.status === 'paid' ? 'ok' : 'warn'}">${inv.status === 'paid' ? 'Payée le ' + E.dateFr(inv.paidAt) : 'À régler avant le ' + E.dateFr(inv.dueAt)}</span></p></div><div class="row end"><button class="btn" data-print>Imprimer / PDF</button></div>`, { wide: true });
    m.el.querySelector('[data-print]').onclick = () => {
      const w = window.open('', '_blank'); if (!w) return;
      w.document.write(`<html><head><title>${esc(inv.number)}</title><link rel="stylesheet" href="${new URL('css/declic.css', location.href).href}"></head><body style="background:#fff;padding:24px">${m.el.querySelector('#inv-print').outerHTML}</body></html>`);
      w.document.close(); setTimeout(() => w.print(), 400);
    };
  }

  window.Views = Object.assign(window.Views || {}, { tplBody, resourceBody, openDoc, openForm, openSlots, openInvoice });
})();
