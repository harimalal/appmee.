/* Helpers d'interface : échappement, markdown léger, modales, toasts */
(function () {
  'use strict';
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  function inline(s) {
    return s
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
      .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  }

  // Markdown minimal et sûr (échappe d'abord tout le HTML)
  function md(src) {
    const lines = esc(src || '').replace(/&gt;/g, '>').split('\n');
    const out = []; let list = null; let tbl = null; let para = [];
    const flushP = () => { if (para.length) { out.push('<p>' + inline(para.join('<br>')) + '</p>'); para = []; } };
    const flushL = () => { if (list) { out.push(`</${list}>`); list = null; } };
    const flushT = () => { if (tbl) { out.push('<div class="tbl"><table>' + tbl.map((r, i) => '<tr>' + r.map((c) => `<${i === 0 ? 'th' : 'td'}>${inline(c)}</${i === 0 ? 'th' : 'td'}>`).join('') + '</tr>').join('') + '</table></div>'); tbl = null; } };
    for (const raw of lines) {
      const l = raw.replace(/\s+$/, '');
      let m;
      if (/^\|.*\|$/.test(l.trim())) {
        flushP(); flushL();
        if (/^\|[\s:|-]+\|$/.test(l.trim())) continue;
        (tbl = tbl || []).push(l.trim().slice(1, -1).split('|').map((c) => c.trim())); continue;
      } else flushT();
      if (!l.trim()) { flushP(); flushL(); continue; }
      if ((m = l.match(/^(#{1,4})\s+(.*)$/))) { flushP(); flushL(); out.push(`<h${m[1].length + 1}>${inline(m[2])}</h${m[1].length + 1}>`); continue; }
      if (/^-{3,}$/.test(l.trim())) { flushP(); flushL(); out.push('<hr>'); continue; }
      if ((m = l.match(/^>\s?(.*)$/))) { flushP(); flushL(); out.push(`<blockquote>${inline(m[1])}</blockquote>`); continue; }
      if ((m = l.match(/^\s*[-*•]\s+(.*)$/))) { flushP(); if (list !== 'ul') { flushL(); out.push('<ul>'); list = 'ul'; } out.push(`<li>${inline(m[1])}</li>`); continue; }
      if ((m = l.match(/^\s*(\d+)[.)]\s+(.*)$/))) { flushP(); if (list !== 'ol') { flushL(); out.push(`<ol start="${m[1]}">`); list = 'ol'; } out.push(`<li>${inline(m[2])}</li>`); continue; }
      flushL(); para.push(l);
    }
    flushP(); flushL(); flushT();
    return out.join('\n');
  }

  function toast(msg, kind) {
    let box = document.getElementById('toasts');
    if (!box) { box = document.createElement('div'); box.id = 'toasts'; box.setAttribute('aria-live', 'polite'); document.body.appendChild(box); }
    const t = document.createElement('div'); t.className = 'toast ' + (kind || ''); t.textContent = msg; box.appendChild(t);
    setTimeout(() => { t.classList.add('out'); setTimeout(() => t.remove(), 300); }, 3200);
  }

  function modal(html, opts) {
    opts = opts || {};
    const wrap = document.createElement('div'); wrap.className = 'modal-wrap';
    wrap.innerHTML = `<div class="modal ${opts.wide ? 'wide' : ''}" role="dialog" aria-modal="true"><button class="modal-x" aria-label="Fermer">×</button>${html}</div>`;
    document.body.appendChild(wrap);
    const close = () => { wrap.remove(); document.removeEventListener('keydown', onKey); if (opts.onClose) opts.onClose(); };
    const onKey = (e) => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', onKey);
    wrap.addEventListener('click', (e) => { if (e.target === wrap) close(); });
    wrap.querySelector('.modal-x').addEventListener('click', close);
    const first = wrap.querySelector('input,select,textarea,button:not(.modal-x)'); if (first) first.focus();
    return { el: wrap.firstElementChild, close };
  }

  function confirmBox(msg, onYes, yesLabel) {
    const m = modal(`<p style="margin:8px 0 18px">${esc(msg)}</p><div class="row end"><button class="btn ghost" data-no>Annuler</button><button class="btn" data-yes>${esc(yesLabel || 'Confirmer')}</button></div>`);
    m.el.querySelector('[data-no]').onclick = m.close;
    m.el.querySelector('[data-yes]').onclick = () => { m.close(); onYes(); };
  }

  const initials = (c) => ((c.prenom || '?')[0] + ((c.nom || '')[0] || '')).toUpperCase();
  const rel = (iso) => {
    const d = Math.round((Date.now() - new Date(iso).getTime()) / 86400000);
    if (d <= 0) return 'aujourd’hui'; if (d === 1) return 'hier'; if (d < 30) return `il y a ${d} j`; return `il y a ${Math.round(d / 30)} mois`;
  };

  window.UI = { esc, md, toast, modal, confirmBox, initials, rel };
})();
