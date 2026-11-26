(() => {
  'use strict';

  // --- Menu mobile ---
  const burger = document.querySelector('.burger');
  const menu = document.getElementById('menu');
  burger.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  menu.addEventListener('click', e => {
    if (e.target.closest('a')) { menu.classList.remove('open'); burger.setAttribute('aria-expanded', false); }
  });

  // --- Slider du hero ---
  const slides = [...document.querySelectorAll('.slide')];
  const dotsBox = document.querySelector('.dots');
  let current = 0, timer;
  const dots = slides.map((_, i) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', `Slide ${i + 1}`);
    b.addEventListener('click', () => { go(i); restart(); });
    dotsBox.appendChild(b);
    return b;
  });
  function go(i) {
    current = (i + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('is-active', k === current));
    dots.forEach((d, k) => d.classList.toggle('on', k === current));
  }
  function restart() { clearInterval(timer); timer = setInterval(() => go(current + 1), 6000); }
  document.querySelector('.prev').addEventListener('click', () => { go(current - 1); restart(); });
  document.querySelector('.next').addEventListener('click', () => { go(current + 1); restart(); });
  go(0); restart();

  // --- Grille de projets ---
  const projects = [
    ['Fitly', 'Suivi sportif connecté', 260], ['Payo', 'Paiement mobile', 150],
    ['Voyago', 'Carnet de voyage', 200], ['Tasko', 'Gestion de tâches', 320],
    ['Medly', 'Rendez-vous santé', 175], ['Bookie', 'Bibliothèque en ligne', 25],
    ['Cookr', 'Recettes et courses', 45], ['Learnix', 'Cours interactifs', 285]
  ];
  document.getElementById('projects').innerHTML = projects.map(([n, d, h]) =>
    `<div class="project" style="--h:${h}"><div><h4>${n}</h4><p>${d}</p></div></div>`).join('');

  // --- Compteurs animés ---
  const countUp = el => {
    const end = +el.dataset.count, t0 = performance.now(), dur = 1600;
    const step = t => {
      const p = Math.min((t - t0) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  // --- Apparition au scroll ---
  const targets = document.querySelectorAll('section > .container > *, .grid > *');
  targets.forEach(t => t.classList.add('reveal'));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      en.target.querySelectorAll('[data-count]').forEach(countUp);
      if (en.target.matches('[data-count]')) countUp(en.target);
      io.unobserve(en.target);
    }), { threshold: .15 });
    targets.forEach(t => io.observe(t));
  } else {
    targets.forEach(t => t.classList.add('in'));
    document.querySelectorAll('[data-count]').forEach(countUp);
  }

  // --- Formulaire (validation côté client uniquement) ---
  const form = document.getElementById('contactForm');
  const status = form.querySelector('.form-status');
  form.addEventListener('submit', e => {
    e.preventDefault();
    let ok = true;
    form.querySelectorAll('input,textarea').forEach(f => {
      const bad = !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
      f.classList.toggle('err', bad);
      if (bad) ok = false;
    });
    status.textContent = ok ? 'Merci ! Votre message est prêt à être envoyé (branchez le formulaire à votre service d’e-mail).' : 'Merci de remplir correctement tous les champs.';
    status.style.color = ok ? '#1a8a5a' : '#d93a5b';
    if (ok) form.reset();
  });

  document.getElementById('year').textContent = new Date().getFullYear();
})();
