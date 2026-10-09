/* Jeu de données de démonstration — rejoue de vrais parcours via le moteur */
(function () {
  'use strict';
  const D = window.DECLIC, S = window.Store, E = window.Engine;

  function fill(formId, over) {
    const a = {};
    D.FORMS[formId].fields.forEach((f) => {
      if (f.type === 'scale') a[f.id] = Math.round((f.min + f.max) / 2) + 1;
      else if (f.type === 'choice') a[f.id] = f.options[0];
      else if (f.type === 'multi') a[f.id] = [f.options[0]];
      else a[f.id] = 'Réponse exemple.';
    });
    return Object.assign(a, over || {});
  }
  const day = (n) => S.shiftClock(n);

  async function journey(spec) {
    S.setClock(-spec.start * 86400000);
    const c = await E.createLead({ prenom: spec.prenom, nom: spec.nom, email: spec.email, source: spec.source, password: 'demo1234' });
    const id = c.id; const reach = spec.reach;
    day(1); E.complete(id, 'guide');
    if (reach === 'lead') return c;
    day(1); E.complete(id, 'prequal', fill('prequal', { urgency: spec.urgency || 8, situation: spec.situation || 'Je veux demander une promotion mais je n’ose pas.', budget: '1 000 – 2 000 €' }));
    if (reach === 'prequal') return c;
    day(1); E.bookCall(id, new Date(S.nowDate().getTime() + (spec.callIn || -2) * 86400000).toISOString());
    if (reach === 'call') return c;
    day(2); E.proposeOffer(id, spec.offer);
    if (reach === 'proposed') return c;
    day(1); E.complete(id, 'read_prop'); E.sign(id, E.fullName(c));
    if (reach === 'signed') return c;
    E.pay(id, spec.inst ? 'inst' : 'full');
    day(1); E.complete(id, 'onb_form', fill('onboarding', { success: spec.goal || 'Obtenir ma promotion' }));
    E.complete(id, 'livret'); E.complete(id, 'checklist1', [0, 1, 2, 3]); E.complete(id, 'roadmap');
    if (reach === 'onboarded') return c;
    const cl = S.clientById(id);
    for (let n = 1; n <= spec.sessions; n++) {
      day(1); E.bookSession(id, n, S.nowDate().toISOString());
      day(6); E.completeSession(id, n, `Travail sur « ${cl.sessions[n - 1].theme} » : prise de conscience importante et premier plan d’action.`);
      const exo = (D.EXERCISES[cl.sessions[n - 1].theme] || []).length;
      for (let k = 0; k < exo && n < spec.sessions; k++) E.toggleExercise(id, n, k);
      if (n === E.midpointSession(cl)) E.submitMid(id, fill('mid'));
      await E.tick();
    }
    if (spec.finish) {
      day(1); E.complete(id, 'bilan_form', fill('bilan', { confidence_end: 9, result: 'Promotion' }));
      E.complete(id, 'satisf', fill('satisfaction', { nps: 10 })); E.complete(id, 'testi', fill('testimonial', { quote: 'Elle m’a aidée à oser. Foncez !' }));
      E.subscribeMomentum(id);
    }
    return c;
  }

  async function run() {
    S.reset(); S.load();
    await S.ensureCoach();
    S.get().seeded = true;
    const base = Date.now();
    await journey({ prenom: 'Sophie', nom: 'Martin', email: 'sophie@exemple.fr', source: 'Bouche-à-oreille', start: 62, reach: 'done', offer: 'declic', sessions: 8, finish: true, goal: 'Obtenir ma promotion', urgency: 9 });
    await journey({ prenom: 'Amélie', nom: 'Durand', email: 'amelie@exemple.fr', source: 'LinkedIn', start: 40, reach: 'done', offer: 'declic', sessions: 4, inst: true, urgency: 8 });
    await journey({ prenom: 'Nadia', nom: 'Kerbrat', email: 'nadia@exemple.fr', source: 'Instagram', start: 26, reach: 'done', offer: 'transformation', sessions: 2, inst: true, urgency: 10, goal: 'Me reconvertir' });
    await journey({ prenom: 'Inès', nom: 'Traore', email: 'ines@exemple.fr', source: 'Bouche-à-oreille', start: 9, reach: 'onboarded', offer: 'premier', sessions: 0 });
    await journey({ prenom: 'Julie', nom: 'Perrin', email: 'julie@exemple.fr', source: 'LinkedIn', start: 8, reach: 'proposed', offer: 'declic', urgency: 7 });
    await journey({ prenom: 'Camille', nom: 'Roux', email: 'camille@exemple.fr', source: 'Bouche-à-oreille', start: 4, reach: 'call', callIn: 2, urgency: 6 });
    await journey({ prenom: 'Léa', nom: 'Bernard', email: 'lea@exemple.fr', source: 'Site (quiz)', start: 1, reach: 'lead' });
    S.setClock(0);
    // Un dossier "Julie" à relancer : la proposition date de plus de 5 jours dans la vraie horloge
    await E.tick();
    // Quelques cases de lancement déjà cochées par Claire
    const L = S.get().launch; [1, 4].forEach((i) => (L[i] = true));
    S.get().settings.siret = ''; S.save();
    return Date.now() - base;
  }

  window.Seed = { run };
})();
