/* Site public : quiz diagnostic → création automatique de l'espace cliente */
(function () {
  'use strict';
  const D = window.DECLIC, S = window.Store, E = window.Engine, U = window.UI;
  const { esc } = U;

  const BLOCKS = {
    temps: { name: 'Le « ce n’est pas le bon moment »', text: 'Tu repousses ce qui compte pour toi en attendant un moment parfait qui ne viendra pas. Bonne nouvelle : c’est une croyance, pas une réalité — et elle se travaille.' },
    imposteur: { name: 'Le syndrome de l’imposteur', text: 'Tu doutes de ta légitimité malgré tes réussites. Tu as déjà les compétences : il manque la confiance pour les assumer à voix haute.' },
    culpabilite: { name: 'La culpabilité de penser à toi', text: 'Tu passes toujours après les autres. Prendre de la place n’est pas voler ta famille : c’est leur montrer l’exemple.' },
    regard: { name: 'La peur du regard des autres', text: 'Tu anticipes les jugements avant d’avoir agi. Apprendre à avancer malgré eux est exactement ce qui te libérera.' },
    permission: { name: 'L’attente de la permission', text: 'Tu attends qu’on te choisisse ou qu’on te le propose. Il est temps de te donner ta propre autorisation.' },
  };
  const Q = [
    ['Quand tu penses à ta prochaine étape professionnelle, tu te dis surtout…', { temps: 'Ce n’est pas le bon moment', imposteur: 'Et si je n’étais pas à la hauteur ?', culpabilite: 'Je ne peux pas penser à moi avant les autres', regard: 'Qu’est-ce qu’on va penser de moi ?', permission: 'Si on me le proposait, j’accepterais' }],
    ['Ce qui te retient le plus pour demander une évolution :', { temps: 'Je n’ai pas une minute à moi', imposteur: 'Je ne me sens pas légitime', culpabilite: 'J’ai peur de négliger ma famille', regard: 'J’ai peur d’être jugée', permission: 'J’attends qu’on remarque mon travail' }],
    ['Un succès récent, tu le décrirais comme…', { temps: 'Un coup de chance, il faut que je passe à autre chose', imposteur: 'Un coup de chance', culpabilite: 'Pas si important comparé à ce que font les autres pour moi', regard: 'Quelque chose dont je ne parle pas trop', permission: 'Normal, je fais mon travail' }],
    ['Ton agenda de la semaine prochaine…', { temps: 'Est plein à craquer, aucune place pour mon projet', imposteur: 'Contient plein de tâches pour prouver que je mérite ma place', culpabilite: 'Est rempli par les besoins de tout le monde sauf les miens', regard: 'Évite tout ce qui m’exposerait', permission: 'Attend un feu vert pour avancer' }],
    ['Si tout était possible, ce qui te manquerait le plus ?', { temps: 'Du temps et de l’énergie', imposteur: 'De la confiance en moi', culpabilite: 'L’autorisation de me choisir', regard: 'Le courage d’oser', permission: 'Un déclic, un oui' }],
  ];
  let step = 0; const tally = {}; const answers = [];

  function el(id) { return document.getElementById(id); }

  function renderQ() {
    const [q, opts] = Q[step];
    el('quiz-body').innerHTML = `<div class="q-prog" aria-hidden="true"><i style="width:${step / Q.length * 100}%"></i></div><p class="eyebrow">Question ${step + 1} / ${Q.length}</p><h3>${esc(q)}</h3><div class="q-opts">${Object.entries(opts).map(([k, t]) => `<button class="q-opt" data-k="${k}">${esc(t)}</button>`).join('')}</div>`;
    el('quiz-body').querySelectorAll('.q-opt').forEach((b) => (b.onclick = () => { tally[b.dataset.k] = (tally[b.dataset.k] || 0) + 1; answers.push(b.dataset.k); step++; step < Q.length ? renderQ() : renderResult(); }));
  }

  function renderResult() {
    const top = Object.entries(tally).sort((a, b) => b[1] - a[1])[0][0]; const b = BLOCKS[top];
    el('quiz-body').innerHTML = `<div class="q-prog"><i style="width:100%"></i></div><p class="eyebrow">Ton résultat</p><h3>Ton blocage dominant : ${esc(b.name)}</h3><p>${esc(b.text)}</p><div class="q-form"><p><strong>Reçois ton guide « Les 5 blocages invisibles » et ouvre ton espace gratuit</strong> — tu y trouveras aussi la réservation de ton appel découverte offert (30 min).</p>
    <form id="qf" novalidate><div class="fld"><label class="lbl" for="qp">Prénom</label><input class="inp" id="qp" autocomplete="given-name" required></div><div class="fld"><label class="lbl" for="qe">Email</label><input class="inp" id="qe" type="email" autocomplete="email" required></div><div class="fld"><label class="lbl" for="qw">Choisis un mot de passe (8 caractères min.)</label><input class="inp" id="qw" type="password" autocomplete="new-password" required></div>
    <label class="opt"><input type="checkbox" id="qc"><span>J’accepte de recevoir les emails de Claire et la <a href="legal.html#rgpd" target="_blank">politique de confidentialité</a>.</span></label><div class="err" id="qerr" role="alert"></div><button class="btn block">Ouvrir mon espace</button></form></div>`;
    el('qf').onsubmit = async (e) => {
      e.preventDefault(); const err = el('qerr'); err.textContent = '';
      const prenom = el('qp').value.trim(), email = el('qe').value.trim(), pw = el('qw').value;
      if (!prenom || !/^\S+@\S+\.\S+$/.test(email)) { err.textContent = 'Prénom et email valides, s’il te plaît.'; return; }
      if (pw.length < 8) { err.textContent = 'Mot de passe : 8 caractères minimum.'; return; }
      if (!el('qc').checked) { err.textContent = 'Coche la case pour continuer.'; return; }
      try {
        S.load(); await S.ensureCoach();
        const ref = new URLSearchParams(location.search).get('ref');
        await E.createLead({ prenom, email, password: pw, source: ref ? 'Recommandation' : 'Site (quiz)', referrer: ref || null, quiz: { top, answers } });
        await S.login(email, pw); await E.tick();
        location.href = 'app.html#/me';
      } catch (x) { err.textContent = x.message; }
    };
  }

  function open() { step = 0; Object.keys(tally).forEach((k) => delete tally[k]); answers.length = 0; el('quiz').hidden = false; document.body.classList.add('noscroll'); renderQ(); el('quiz').querySelector('.modal-x').focus(); }
  function close() { el('quiz').hidden = true; document.body.classList.remove('noscroll'); }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-quiz]').forEach((b) => b.addEventListener('click', (e) => { e.preventDefault(); open(); }));
    el('quiz').querySelector('.modal-x').onclick = close;
    el('quiz').addEventListener('click', (e) => { if (e.target === el('quiz')) close(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !el('quiz').hidden) close(); });
    if (new URLSearchParams(location.search).get('ref')) el('ref-note').hidden = false;
    // Offres dynamiques
    el('offers').innerHTML = ['premier', 'declic', 'transformation'].map((id) => { const o = D.OFFERS[id]; return `<article class="offer ${o.featured ? 'feat' : ''}">${o.featured ? '<span class="ribbon">La plus choisie</span>' : ''}<p class="eyebrow">${esc(o.level)}</p><h3>${esc(o.name)}</h3><p class="price">${E.money(o.price)}</p>${o.installments ? `<p class="muted">ou ${o.installments.n} × ${E.money(o.installments.amount)}</p>` : '<p class="muted">&nbsp;</p>'}<p class="dur">${esc(o.duration)}</p><p>${esc(o.pitch)}</p><ul>${o.includes.map((x) => `<li>${esc(x)}</li>`).join('')}</ul><button class="btn ${o.featured ? '' : 'ghost'} block" data-quiz>Commencer par mon appel offert</button></article>`; }).join('');
    document.querySelectorAll('#offers [data-quiz]').forEach((b) => b.addEventListener('click', (e) => { e.preventDefault(); open(); }));
    el('year').textContent = new Date().getFullYear();
  });
})();
