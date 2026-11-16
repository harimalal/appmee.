/* NOVOLENS — animations légères, sans dépendance. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  /* En-tête : ombre au défilement, barre de progression, menu mobile */
  var header = $('.site-header'), bar = $('.progress'), burger = $('.burger'), menu = $('#menu');
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) header.classList.toggle('scrolled', y > 8);
    if (bar) {
      var h = d.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      menu.classList.toggle('open', !open);
    });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () {
      burger.setAttribute('aria-expanded', 'false'); menu.classList.remove('open'); }); });
  }

  /* Observateur générique : appelle cb une fois quand l'élément est visible */
  function whenVisible(el, cb, th) {
    if (!('IntersectionObserver' in window)) { cb(); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.disconnect(); cb(); } });
    }, { threshold: th || 0.25 });
    io.observe(el);
  }

  /* Révélation : seuls les blocs sous la ligne de flottaison sont masqués puis révélés */
  $$('[data-reveal]').forEach(function (el, i) {
    el.classList.add('reveal');
    var r = el.getBoundingClientRect();
    var below = r.top > window.innerHeight * 0.92;
    if (reduce || !below || !('IntersectionObserver' in window)) { el.classList.add('show'); return; }
    el.classList.add('pre');
    var delay = el.getAttribute('data-reveal');
    if (delay && !isNaN(+delay)) el.style.setProperty('--rd', delay + 'ms');
    whenVisible(el, function () { el.classList.add('show'); }, 0.12);
  });

  /* Compteurs */
  function fmt(n, dec) { return (dec ? n.toFixed(dec) : String(Math.round(n))).replace('.', ','); }
  $$('[data-count]').forEach(function (el) {
    var to = parseFloat(el.getAttribute('data-count')), dec = +(el.getAttribute('data-dec') || 0);
    var pre = el.getAttribute('data-pre') || '', suf = el.getAttribute('data-suf') || '';
    if (reduce) { el.textContent = pre + fmt(to, dec) + suf; return; }
    el.textContent = pre + fmt(0, dec) + suf;
    whenVisible(el, function () {
      var t0 = performance.now(), dur = 1400;
      (function tick(t) {
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + fmt(to * e, dec) + suf;
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }, 0.4);
  });

  /* Éléments qui s'animent quand ils entrent à l'écran (.in) */
  $$('[data-in]').forEach(function (el) { whenVisible(el, function () { el.classList.add('in'); }, 0.3); });

  /* Halo qui suit la souris sur les cartes */
  $$('.card').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* Hero : liste de rendez-vous qui arrivent en continu */
  var list = $('#notif-list');
  if (list) {
    var data = [
      ['19', 'NOV', 'Directeur Général', 'Industrie · 500 M€'],
      ['23', 'NOV', 'Directrice Achats', 'Santé · Groupe'],
      ['26', 'NOV', 'CEO', 'Tech & Logiciels'],
      ['30', 'NOV', 'Directeur Commercial', 'Distribution · ETI'],
      ['03', 'DÉC', 'DSI', 'Services B2B · 1 200 salariés']
    ];
    var arrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg>';
    var idx = 0;
    var mk = function (r) {
      var li = d.createElement('div'); li.className = 'rdv';
      li.innerHTML = '<div class="date"><span><b>' + r[0] + '</b>' + r[1] + '</span></div>' +
        '<div><strong>Rendez-vous qualifié</strong><span class="sub">' + r[2] + ' · ' + r[3] + '</span></div>' + arrow;
      return li;
    };
    for (var k = 0; k < 3; k++) list.appendChild(mk(data[idx++ % data.length]));
    if (!reduce) setInterval(function () {
      if (d.hidden) return;
      var li = mk(data[idx++ % data.length]);
      list.appendChild(li);
      var first = list.firstElementChild;
      first.style.transition = 'opacity .4s, transform .4s'; first.style.opacity = '0'; first.style.transform = 'translateX(-14px)';
      setTimeout(function () { if (first.parentNode) first.parentNode.removeChild(first); }, 420);
    }, 3200);
  }

  /* Comparateur Sans / Avec NOVOLENS */
  $$('.cmp').forEach(function (cmp) {
    var tabs = $$('[role="tab"]', cmp), timer = null, touched = false;
    function set(state) {
      cmp.setAttribute('data-state', state);
      tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-state') === state)); });
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () {
      touched = true; clearInterval(timer); set(t.getAttribute('data-state')); }); });
    $$('.slot.is-rdv', cmp).forEach(function (s, i) { s.style.setProperty('--i', i); });
    set('sans');
    whenVisible(cmp, function () {
      setTimeout(function () { if (!touched) set('avec'); }, reduce ? 0 : 900);
      if (!reduce) timer = setInterval(function () {
        if (touched || d.hidden) return;
        set(cmp.getAttribute('data-state') === 'avec' ? 'sans' : 'avec');
      }, 5200);
    }, 0.35);
  });

  /* Lecteur d'explication animée */
  $$('.player').forEach(function (pl) {
    var scenes = $$('.pscene', pl), btns = $$('.pbars button', pl), play = $('.pbtn', pl);
    var cur = 0, dur = 4200, timer = null, paused = false, started = false;
    var iPlay = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l13-7.5z"/></svg>';
    var iPause = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>';
    pl.style.setProperty('--dur', dur + 'ms');
    function show(i) {
      cur = (i + scenes.length) % scenes.length;
      scenes.forEach(function (s, n) { s.classList.toggle('on', n === cur); });
      btns.forEach(function (b, n) {
        b.classList.remove('cur', 'done'); void b.offsetWidth;
        if (n < cur) b.classList.add('done'); else if (n === cur) b.classList.add('cur');
      });
      clearTimeout(timer);
      if (!paused && !reduce) timer = setTimeout(function () { show(cur + 1); }, dur);
    }
    btns.forEach(function (b, n) { b.addEventListener('click', function () { show(n); }); });
    if (play) play.addEventListener('click', function () {
      paused = !paused; pl.classList.toggle('paused', paused);
      play.innerHTML = paused ? iPlay : iPause;
      play.setAttribute('aria-label', paused ? 'Lire' : 'Pause');
      if (paused) clearTimeout(timer); else show(cur);
    });
    show(0);
    if (!reduce) { // ne tourne que lorsque le lecteur est visible
      var vis = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) { clearTimeout(timer); }
          else if (!paused) { show(cur); }
        });
      }, { threshold: 0.2 }) : null;
      if (vis) vis.observe(pl);
    }
  });
  $$('[data-open-video]').forEach(function (b) { b.addEventListener('click', function () {
    var t = $('#video'); if (t) t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    else location.href = 'comment-ca-marche.html#video';
  }); });

  /* FAQ : tout ouvrir / fermer */
  var tog = $('#faq-toggle');
  if (tog) tog.addEventListener('click', function () {
    var all = $$('.faq details'), open = all.some(function (x) { return !x.open; });
    all.forEach(function (x) { x.open = open; });
    tog.textContent = open ? 'Tout fermer' : 'Tout ouvrir';
  });

  /* Contact : choix de créneau + envoi simulé */
  var form = $('#contact-form');
  if (form) {
    var chosen = null, wrap = form.closest('.form');
    $$('.tbtn', wrap).forEach(function (b) { b.addEventListener('click', function () {
      $$('.tbtn', wrap).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true'); chosen = b.getAttribute('data-label');
      var out = $('#chosen'); if (out) out.textContent = 'Créneau souhaité : ' + chosen;
    }); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      $$('[required]', form).forEach(function (f) {
        var err = $('.err', f.closest('.field') || f.parentNode), bad = f.type === 'checkbox' ? !f.checked : !f.value.trim();
        if (f.type === 'email' && f.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value)) bad = true;
        if (err) err.textContent = bad ? (f.type === 'email' ? 'Saisissez une adresse e-mail valide.' : 'Ce champ est requis.') : '';
        if (bad) ok = false;
      });
      if (!ok) { var first = $('.err:not(:empty)', form); if (first) first.scrollIntoView({ block: 'center' }); return; }
      var s = $('#success-slot'); if (s) s.textContent = chosen ? 'Créneau souhaité : ' + chosen + '.' : 'Nous vous proposerons un créneau.';
      wrap.classList.add('done');
    });
  }
})();

/* Parcours animé : défile tout seul, cliquable, met en pause hors écran */
(function () {
  var d = document, reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  Array.prototype.forEach.call(d.querySelectorAll('[data-story]'), function (st) {
    var tabs = Array.prototype.slice.call(st.querySelectorAll('.story-tab'));
    var slides = Array.prototype.slice.call(st.querySelectorAll('.slide'));
    var dur = +(st.getAttribute('data-dur') || 7000), cur = 0, timer = null, visible = false, hold = false;
    st.style.setProperty('--dur', dur + 'ms');
    function go(i) {
      var prev = cur; cur = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        if (n === cur) { s.classList.remove('out'); void s.offsetWidth; s.classList.add('on'); }
        else if (n === prev && prev !== cur) { s.classList.remove('on'); s.classList.add('out');
          (function (x) { setTimeout(function () { if (!x.classList.contains('on')) x.classList.remove('out'); }, 850); })(s); }
        else { s.classList.remove('on', 'out'); }
      });
      tabs.forEach(function (t, n) {
        t.setAttribute('aria-selected', String(n === cur));
        t.classList.remove('cur'); void t.offsetWidth; if (n === cur) t.classList.add('cur');
      });
      clearTimeout(timer);
      if (!reduce && visible && !hold) timer = setTimeout(function () { go(cur + 1); }, dur);
    }
    tabs.forEach(function (t, n) { t.addEventListener('click', function () { go(n); }); });
    st.addEventListener('mouseenter', function () { hold = true; st.classList.add('paused'); clearTimeout(timer); });
    st.addEventListener('mouseleave', function () { hold = false; st.classList.remove('paused'); go(cur); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { visible = e.isIntersecting; if (visible) go(cur); else clearTimeout(timer); });
      }, { threshold: 0.35 }).observe(st);
    } else { visible = true; go(0); }
    go(0);
  });
  /* Photos remplaçables : si img/etape-N.jpg existe, elle remplace l'illustration */
  Array.prototype.forEach.call(d.querySelectorAll('img[data-src]'), function (img) {
    var t = new Image();
    t.onload = function () { img.src = t.src; img.hidden = false; var s = img.closest('.stage, .scene'); if (s) s.classList.add('has-photo'); };
    t.src = img.getAttribute('data-src');
  });
})();

/* Encarts : l'animation se rejoue à chaque fois que la section entre à l'écran */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('[data-in-loop]'), function (el) {
    if (!('IntersectionObserver' in window)) { el.classList.add('in'); return; }
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { el.classList.toggle('in', e.isIntersecting); });
    }, { threshold: 0.3 }).observe(el);
  });
})();

/* V3 : rotateur, simulateur, barre collante, flèches clavier sur les onglets */
(function () {
  var d = document, reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rot = d.querySelector('[data-rotate]');
  if (rot && !reduce) {
    var words = rot.getAttribute('data-rotate').split('|'), i = 0;
    setInterval(function () {
      if (d.hidden) return;
      rot.classList.add('swap');
      setTimeout(function () { i = (i + 1) % words.length; rot.textContent = words[i]; rot.classList.remove('swap'); }, 360);
    }, 2600);
  }
  var sim = d.getElementById('sim');
  if (sim) {
    var f = function (n) { return new Intl.NumberFormat('fr-FR').format(Math.round(n)); };
    var val = d.getElementById('sim-val'), rate = d.getElementById('sim-rate'), rdv = d.getElementById('sim-rdv');
    var calc = function () {
      var v = Math.max(0, +val.value || 0), r = Math.min(100, Math.max(0, +rate.value || 0)), n = Math.max(0, +rdv.value || 0);
      var clients = n * r / 100, month = clients * v;
      d.getElementById('sim-clients').textContent = (Math.round(clients * 10) / 10).toString().replace('.', ',');
      d.getElementById('sim-month').textContent = f(month) + ' €';
      d.getElementById('sim-year').textContent = f(month * 12) + ' €';
    };
    [val, rate, rdv].forEach(function (x) { x.addEventListener('input', calc); });
    calc();
  }
  var cta = d.querySelector('.sticky-cta');
  if (cta && 'IntersectionObserver' in window) {
    var hide = new Set();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) hide.add(e.target); else hide.delete(e.target); });
      cta.classList.toggle('off', hide.size > 0);
    }, { threshold: 0.15 });
    Array.prototype.forEach.call(d.querySelectorAll('.cta-band, .site-footer, .form'), function (el) { io.observe(el); });
  }
  Array.prototype.forEach.call(d.querySelectorAll('[role="tablist"]'), function (tl) {
    tl.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var tabs = Array.prototype.slice.call(tl.querySelectorAll('[role="tab"]')), i = tabs.indexOf(d.activeElement);
      if (i < 0) return; e.preventDefault();
      var n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); n.click();
    });
  });
  var menu = d.getElementById('menu'), burger = d.querySelector('.burger');
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu && menu.classList.contains('open')) { menu.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); burger.focus(); }
  });
})();
