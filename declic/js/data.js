/* ============================================================
   DÉCLIC — Catalogue métier (tiré du document BusinessFlow Pro)
   Offres, parcours client, formulaires, emails, ressources.
   Tout ce que Claire n'a PAS à saisir est défini ici.
   ============================================================ */
(function () {
  'use strict';

  const BRAND = {
    name: 'Déclic',
    owner: 'Claire RTH',
    tagline: 'De la mise en veille à la mise en mouvement.',
    uvp: 'Je suis la coach qui vous aide à vous remettre au centre de votre propre vie — pour que vos rêves ne restent plus en stand-by.',
    goals: { m3: 2000, m6: 7000 },
  };

  /* ---------- Offres (Output 13, §5) ---------- */
  const OFFERS = {
    premier: {
      id: 'premier', name: 'Session PREMIER DÉCLIC', short: 'Premier Déclic', level: 'Entrée',
      price: 197, installments: null, duration: '1 séance de 90 min',
      pitch: 'Tester le coaching à faible risque : un diagnostic complet et un plan d’action sur 30 jours.',
      includes: ['Diagnostic complet de ta situation', 'Identification de ton blocage principal', 'Plan d’action immédiat sur 30 jours', 'Enregistrement audio de la séance'],
      sessions: [{ theme: 'Diagnostic express & plan 30 jours', minutes: 90 }],
    },
    declic: {
      id: 'declic', name: 'Programme DÉCLIC', short: 'Déclic', level: 'Offre cœur', featured: true,
      price: 1200, installments: { n: 3, amount: 450 }, duration: '8 semaines · 8 séances de 60 min',
      pitch: 'L’accompagnement intensif de 8 semaines pour franchir enfin ta prochaine étape.',
      includes: ['8 séances individuelles de 60 min (1 par semaine)', 'Support WhatsApp entre les séances (réponse sous 24 h ouvrées)', 'Exercices et outils personnalisés après chaque séance', 'Audios et fiches pratiques', 'Bilan de transformation final', 'Garantie satisfaction 100 % après la séance 2'],
      sessions: [
        { theme: 'Diagnostic & Clarté', minutes: 60 }, { theme: 'Croyances limitantes', minutes: 60 },
        { theme: 'Vision & Désirs profonds', minutes: 60 }, { theme: 'Plan d’action', minutes: 60 },
        { theme: 'Obstacles & Peurs', minutes: 60 }, { theme: 'Confiance & Légitimité', minutes: 60 },
        { theme: 'Passage à l’action', minutes: 60 }, { theme: 'Ancrage & Projection', minutes: 60 },
      ],
    },
    transformation: {
      id: 'transformation', name: 'Programme TRANSFORMATION', short: 'Transformation', level: 'Premium',
      price: 2800, installments: { n: 3, amount: 1000 }, duration: '12 semaines · 12 séances',
      pitch: 'Réinventer ta trajectoire : reconversion totale, création d’entreprise ou transformation majeure.',
      includes: ['Tout le programme DÉCLIC', '4 séances supplémentaires de suivi', 'WhatsApp illimité (réponse sous 12 h)', 'Préparation spécifique à ton objectif (entretien, pitch, lancement)', 'Accès à vie aux ressources', 'Séance bilan à 6 mois offerte'],
      sessions: [
        { theme: 'Diagnostic & Clarté', minutes: 60 }, { theme: 'Croyances limitantes', minutes: 60 },
        { theme: 'Vision & Désirs profonds', minutes: 60 }, { theme: 'Plan d’action', minutes: 60 },
        { theme: 'Obstacles & Peurs', minutes: 60 }, { theme: 'Confiance & Légitimité', minutes: 60 },
        { theme: 'Passage à l’action', minutes: 60 }, { theme: 'Ancrage & Projection', minutes: 60 },
        { theme: 'Préparation de ton objectif', minutes: 60 }, { theme: 'Mise en situation', minutes: 60 },
        { theme: 'Accélération', minutes: 60 }, { theme: 'Bilan & projection à 6 mois', minutes: 60 },
      ],
    },
    momentum: {
      id: 'momentum', name: 'Suivi MOMENTUM', short: 'Momentum', level: 'Continuité',
      price: 450, installments: null, perMonth: true, duration: '2 séances de 45 min / mois',
      pitch: 'Garder ta dynamique après le programme.',
      includes: ['2 séances de 45 min par mois', 'Support WhatsApp'],
      sessions: [{ theme: 'Séance de suivi 1', minutes: 45 }, { theme: 'Séance de suivi 2', minutes: 45 }],
    },
  };

  /* ---------- Exercices débloqués après chaque thème de séance ---------- */
  const EXERCISES = {
    'Diagnostic express & plan 30 jours': ['Relire le plan d’action des 30 jours et choisir UNE action pour demain', 'Écouter l’enregistrement audio de la séance', 'Noter 3 victoires de la semaine, même minuscules'],
    'Diagnostic & Clarté': ['Écrire ce que tu ne veux plus (10 lignes sans te censurer)', 'Noter chaque soir 1 moment où tu t’es oubliée aujourd’hui', 'Formuler en une phrase ton objectif de transformation'],
    'Croyances limitantes': ['Relever tes 3 croyances limitantes majeures et leur « preuve »', 'Réécrire chaque croyance en phrase alliée', 'Relire tes phrases alliées matin et soir'],
    'Vision & Désirs profonds': ['Décrire ta journée idéale dans 12 mois (une page)', 'Lister 5 désirs profonds, sans te demander « comment »', 'Choisir le désir qui te fait le plus vibrer'],
    'Plan d’action': ['Découper ton objectif en 3 étapes', 'Fixer une action de 15 minutes par jour cette semaine', 'Bloquer 2 créneaux « pour moi » dans ton agenda'],
    'Obstacles & Peurs': ['Écrire ta peur la plus forte et le pire scénario réaliste', 'Préparer ta réponse à « et si ça arrive ? »', 'Demander du soutien à une personne de confiance'],
    'Confiance & Légitimité': ['Rédiger tes 10 réussites professionnelles', 'Demander 2 retours positifs à des collègues ou amies', 'Faire l’exercice du miroir : te présenter à voix haute en 1 minute'],
    'Passage à l’action': ['Réaliser la première action concrète (demande, candidature, message…)', 'Répéter ta demande à voix haute (simulation)', 'Noter ce que tu as ressenti avant / après'],
    'Ancrage & Projection': ['Relire ton parcours depuis la séance 1', 'Définir tes 3 prochaines actions à 6 mois', 'Te féliciter : écrire une lettre à la toi d’il y a 8 semaines'],
    'Préparation de ton objectif': ['Rassembler les éléments de ton dossier (CV, chiffres, arguments)', 'Écrire ton pitch en 3 phrases'],
    'Mise en situation': ['Faire une simulation avec une personne de confiance', 'Noter 3 ajustements à apporter'],
    'Accélération': ['Lancer l’action la plus importante de ta liste', 'Mesurer le résultat obtenu'],
    'Bilan & projection à 6 mois': ['Compléter ton tableau de bord de progression', 'Planifier ta séance bilan à 6 mois'],
    'Séance de suivi 1': ['Faire le point sur tes 3 actions du mois'],
    'Séance de suivi 2': ['Définir ton objectif du mois suivant'],
  };

  /* ---------- Formulaires (condensés des templates A1, B1, B4, B5, B6) ---------- */
  const FORMS = {
    prequal: {
      title: 'Questionnaire de pré-qualification', minutes: 4,
      intro: 'Quelques questions pour que notre appel soit vraiment utile. Il n’y a ni bonne ni mauvaise réponse.',
      fields: [
        { id: 'job', label: 'Quel est ton métier ou ton poste actuel ?', type: 'text' },
        { id: 'life', label: 'Comment décrirais-tu ta vie en ce moment ?', type: 'multi', options: ['Je jongle entre vie pro, vie de mère et peu de temps pour moi', 'Je suis compétente dans mon travail mais quelque chose me manque', 'J’ai l’impression de tourner en rond', 'Je suis épuisée'] },
        { id: 'situation', label: 'Quelle situation te pousse à chercher un accompagnement aujourd’hui ?', type: 'textarea' },
        { id: 'goal', label: 'Ce que tu veux le plus', type: 'choice', options: ['Demander une augmentation / promotion', 'Changer de poste ou de secteur', 'Me reconvertir complètement', 'Créer mon projet', 'Retrouver confiance en moi'] },
        { id: 'since', label: 'Depuis combien de temps ?', type: 'choice', options: ['Quelques semaines', '3 à 6 mois', 'Plus d’un an', 'Plusieurs années'] },
        { id: 'urgency', label: 'Urgence (1 = je réfléchis, 10 = maintenant)', type: 'scale', min: 1, max: 10 },
        { id: 'budget', label: 'Fourchette d’investissement envisagée', type: 'choice', options: ['Moins de 500 €', '500 – 1 000 €', '1 000 – 2 000 €', 'Plus de 2 000 € si la valeur est là', 'Je ne sais pas encore'] },
        { id: 'decider', label: 'La décision…', type: 'choice', options: ['M’appartient entièrement', 'Se prend avec mon/ma partenaire', 'Dépend d’un financement externe'] },
      ],
    },
    onboarding: {
      title: 'Questionnaire d’onboarding', minutes: 8,
      intro: 'Pour que notre première séance démarre sur du concret, raconte-moi ton histoire à ton rythme.',
      fields: [
        { id: 'phone', label: 'Téléphone / WhatsApp', type: 'text' },
        { id: 'family', label: 'Ta situation familiale (enfants, âges, organisation)', type: 'textarea' },
        { id: 'pro', label: 'Ton parcours professionnel en quelques lignes', type: 'textarea' },
        { id: 'dream', label: 'Le rêve que tu as mis de côté', type: 'textarea' },
        { id: 'blocks', label: 'Ce qui te freine le plus aujourd’hui', type: 'textarea' },
        { id: 'tried', label: 'Ce que tu as déjà essayé', type: 'textarea' },
        { id: 'success', label: 'À quoi ressemblera le succès dans 8 semaines ?', type: 'textarea' },
        { id: 'confidence_start', label: 'Ton niveau de confiance aujourd’hui (1-10)', type: 'scale', min: 1, max: 10 },
        { id: 'style', label: 'Tu te décrirais plutôt…', type: 'choice', options: ['Introvertie, j’ai besoin de temps', 'Extravertie, j’aime parler et agir', 'Un mélange des deux'] },
        { id: 'slots', label: 'Créneaux habituellement possibles', type: 'multi', options: ['Matin', 'Midi', 'Fin de journée', 'Soirée', 'Week-end'] },
      ],
    },
    mid: {
      title: 'Bilan de mi-parcours', minutes: 3,
      intro: 'Un point rapide pour ajuster la suite à ton rythme.',
      fields: [
        { id: 'progress', label: 'Ce qui a le plus bougé pour toi', type: 'textarea' },
        { id: 'difficult', label: 'Ce qui reste difficile', type: 'textarea' },
        { id: 'confidence_mid', label: 'Ta confiance aujourd’hui (1-10)', type: 'scale', min: 1, max: 10 },
        { id: 'rhythm', label: 'Le rythme te convient-il ?', type: 'choice', options: ['Parfait', 'Un peu rapide', 'Un peu lent'] },
        { id: 'wish', label: 'Ce que tu aimerais que je fasse différemment', type: 'textarea' },
      ],
    },
    bilan: {
      title: 'Bilan de transformation', minutes: 5,
      intro: 'Mesurons le chemin parcouru ensemble.',
      fields: [
        { id: 'confidence_end', label: 'Ta confiance aujourd’hui (1-10)', type: 'scale', min: 1, max: 10 },
        { id: 'actions', label: 'Les actions concrètes que tu as réalisées', type: 'textarea' },
        { id: 'blocks_lifted', label: 'Les blocages levés', type: 'textarea' },
        { id: 'result', label: 'Ton résultat principal', type: 'choice', options: ['Augmentation', 'Promotion', 'Mobilité / nouveau poste', 'Reconversion engagée', 'Projet lancé', 'Autre'] },
        { id: 'next', label: 'Tes 3 prochaines actions', type: 'textarea' },
      ],
    },
    satisfaction: {
      title: 'Questionnaire de satisfaction', minutes: 2,
      intro: 'Ton avis m’aide à m’améliorer.',
      fields: [
        { id: 'nps', label: 'Recommanderais-tu cet accompagnement ? (0-10)', type: 'scale', min: 0, max: 10 },
        { id: 'best', label: 'Ce que tu as le plus apprécié', type: 'textarea' },
        { id: 'better', label: 'Ce qui pourrait être mieux', type: 'textarea' },
      ],
    },
    testimonial: {
      title: 'Ton témoignage', minutes: 3,
      intro: 'Quelques mots de toi peuvent aider une autre femme à oser. Tu restes libre de rester anonyme.',
      fields: [
        { id: 'before', label: 'Avant l’accompagnement, tu étais…', type: 'textarea' },
        { id: 'after', label: 'Aujourd’hui, tu es…', type: 'textarea' },
        { id: 'quote', label: 'Une phrase pour une femme qui hésite', type: 'textarea' },
        { id: 'consent', label: 'Autorisation de publication', type: 'choice', options: ['Oui, avec mon prénom', 'Oui, de façon anonyme', 'Non, usage interne uniquement'] },
      ],
    },
  };

  /* ---------- Parcours client : 5 étapes, chaque case cochée déclenche la suite ---------- */
  // who: client | coach ; kind: check | read | form | book | sign | pay | propose | session
  const STAGES = [
    {
      id: 'decouverte', label: 'Je me découvre', icon: '🌱',
      promise: 'Comprendre ce qui te retient et voir si on peut avancer ensemble.',
      tasks: [
        { id: 'quiz', who: 'client', kind: 'check', label: 'Faire le quiz diagnostic', hint: 'Fait depuis le site.', unlock: ['guide'], mail: ['welcome1'] },
        { id: 'guide', who: 'client', kind: 'read', label: 'Lire le guide « Les 5 blocages invisibles »', resource: 'guide', hint: '10 minutes de lecture.' },
        { id: 'prequal', who: 'client', kind: 'form', form: 'prequal', label: 'Remplir le questionnaire de pré-qualification', hint: '4 minutes.', mail: ['callinvite'] },
        { id: 'book_call', who: 'client', kind: 'book', slotKind: 'call', label: 'Réserver mon appel découverte gratuit (30 min)', hint: 'Choisis le créneau qui te va.', mail: ['callconfirm'] },
        { id: 'prep_call', who: 'coach', kind: 'check', label: 'Relire ses réponses avant l’appel (15 min)', resource: 'script_appel', hint: 'Son score et ses réponses sont dans sa fiche.' },
        { id: 'call_done', who: 'coach', kind: 'propose', label: 'Appel réalisé → choisir l’offre à proposer', hint: 'Un clic : la proposition est générée et envoyée.' },
      ],
    },
    {
      id: 'decision', label: 'Je choisis', icon: '✨',
      promise: 'Une proposition claire, un engagement serein.',
      tasks: [
        { id: 'read_prop', who: 'client', kind: 'read', resource: 'proposition', label: 'Lire ma proposition personnalisée', hint: 'Garantie incluse.' },
        { id: 'sign', who: 'client', kind: 'sign', resource: 'contrat', label: 'Accepter les conditions et signer', hint: 'Signature électronique simple.', unlock: ['contrat'] },
        { id: 'pay', who: 'client', kind: 'pay', label: 'Régler mon accompagnement', hint: 'Comptant ou en plusieurs fois.', mail: ['paid'] },
      ],
    },
    {
      id: 'onboarding', label: 'Je démarre', icon: '🧭',
      promise: 'Tout est prêt pour que la 1re séance soit une vraie avancée.',
      onEnter: { unlock: ['livret', 'roadmap'], mail: ['onboarding'] },
      tasks: [
        { id: 'onb_form', who: 'client', kind: 'form', form: 'onboarding', label: 'Remplir mon questionnaire d’onboarding', hint: '8 minutes pour que Claire te connaisse.' },
        { id: 'livret', who: 'client', kind: 'read', resource: 'livret', label: 'Lire mon livret d’accueil', hint: '5 pages.' },
        { id: 'checklist1', who: 'client', kind: 'checklist', label: 'Préparer ma première séance', items: ['J’ai bloqué un créneau au calme', 'J’ai relu mon objectif de transformation', 'J’ai préparé mes 3 questions', 'J’ai testé ma connexion visio'], hint: '4 cases à cocher.' },
        { id: 'roadmap', who: 'client', kind: 'read', resource: 'roadmap', label: 'Découvrir ma feuille de route', hint: 'Générée pour toi.' },
      ],
    },
    {
      id: 'programme', label: 'Je me transforme', icon: '🔥',
      promise: 'Séance après séance, les ressources se débloquent.',
      tasks: [{ id: 'sessions', who: 'client', kind: 'session', label: 'Mes séances', hint: 'Chaque séance débloque tes exercices et la suivante.' }],
    },
    {
      id: 'bilan', label: 'J’ancre', icon: '🏁',
      promise: 'Mesurer, célébrer, et décider de la suite.',
      onEnter: { unlock: ['bilan_doc'], mail: ['finalbilan'] },
      tasks: [
        { id: 'bilan_form', who: 'client', kind: 'form', form: 'bilan', label: 'Compléter mon bilan de transformation' },
        { id: 'satisf', who: 'client', kind: 'form', form: 'satisfaction', label: 'Donner mon avis', hint: '2 minutes.' },
        { id: 'testi', who: 'client', kind: 'form', form: 'testimonial', label: 'Écrire mon témoignage', hint: 'Facultatif mais précieux.', optional: true, unlock: ['parrainage'], mail: ['thanks'] },
      ],
    },
    {
      id: 'ensuite', label: 'Et maintenant', icon: '🌳',
      promise: 'Garder l’élan, partager, continuer.',
      onEnter: { unlock: ['parrainage', 'momentum_doc'], mail: ['momentum'] },
      tasks: [
        { id: 'momentum', who: 'client', kind: 'choose', label: 'Continuer avec le Suivi MOMENTUM (450 €/mois)', optional: true, hint: 'Sans engagement de durée.' },
        { id: 'refer', who: 'client', kind: 'refer', label: 'Recommander Déclic à une amie', optional: true, hint: 'Ton kit de recommandation est prêt.' },
      ],
    },
  ];

  /* ---------- Ressources débloquables côté cliente ---------- */
  // type: doc (markdown) | gen (généré par moteur) | tpl (template du document)
  const RESOURCES = {
    guide: { title: 'Guide — Les 5 blocages invisibles', type: 'doc', icon: '📘', stage: 'decouverte' },
    script_appel: { title: 'Script d’appel découverte', type: 'tpl', tpl: 'A2', icon: '📞', audience: 'coach' },
    proposition: { title: 'Ma proposition', type: 'gen', icon: '📄', stage: 'decision' },
    contrat: { title: 'Contrat et conditions générales', type: 'tpl', tpl: 'A5', icon: '🖋️', stage: 'decision' },
    livret: { title: 'Livret d’accueil', type: 'tpl', tpl: 'B2', icon: '📗', stage: 'onboarding' },
    roadmap: { title: 'Ma feuille de route', type: 'gen', icon: '🗺️', stage: 'onboarding' },
    bilan_doc: { title: 'Bilan de fin d’accompagnement', type: 'tpl', tpl: 'B5', icon: '🏁', stage: 'bilan' },
    parrainage: { title: 'Kit de recommandation', type: 'gen', icon: '💌', stage: 'bilan' },
    momentum_doc: { title: 'Offre de continuité', type: 'tpl', tpl: 'B7', icon: '🌳', stage: 'ensuite' },
  };

  /* ---------- Emails automatiques (séquences du document, Output 7) ---------- */
  // Variables : {{prenom}} {{offre}} {{prix}} {{lien}} {{claire}}
  const EMAILS = {
    welcome1: { subject: 'Bienvenue. Tu as fait quelque chose d’important aujourd’hui.', body: 'Bonjour {{prenom}},\n\nJe m’appelle Claire, et avant tout, je veux que tu saches une chose : le fait que tu sois là aujourd’hui, ça compte.\n\nTon guide « Les 5 blocages invisibles » t’attend dans ton espace personnel.\n\n👉 {{lien}}\n\nRéponds-moi simplement à cet email pour me dire ce qui t’a fait venir : je lis tout.\n\nClaire' },
    welcome2: { subject: 'Le piège du « quand j’aurai le temps »…', body: 'Bonjour {{prenom}},\n\nJ’accompagne des femmes brillantes, capables de gérer une équipe de 10 personnes ET les devoirs de CM2. Et pourtant, leur propre projet reste dans un tiroir.\n\nCe n’est pas un manque de volonté : il y a trop de paramètres en jeu. Dans ton espace, tu peux faire le point en 4 minutes.\n\n👉 {{lien}}\n\nClaire' },
    welcome3: { subject: 'Mon histoire (et pourquoi je comprends vraiment ce que tu vis)', body: 'Bonjour {{prenom}},\n\nJ’ai moi aussi vécu de grands blocages personnels et professionnels qui ont mis mes rêves en stand-by. C’est pour cela que je ne te donnerai pas de conseils génériques : je suis là pour t’écouter, toi.\n\nClaire' },
    welcome4: { subject: 'Les 3 blocages qui t’empêchent d’avancer (et comment les reconnaître)', body: 'Bonjour {{prenom}},\n\n1. La peur du regard des autres.\n2. Le syndrome de la bonne élève qui attend la permission.\n3. La culpabilité de penser à soi.\n\nLequel te parle le plus ? Réponds-moi en une phrase.\n\nClaire' },
    welcome5: { subject: 'Un outil simple pour clarifier ta prochaine étape (offert)', body: 'Bonjour {{prenom}},\n\nTon questionnaire de pré-qualification prend 4 minutes et te donne déjà un premier éclairage. Il prépare aussi notre appel découverte gratuit.\n\n👉 {{lien}}\n\nClaire' },
    welcome6: { subject: 'Voilà comment je travaille (et ce que ça change vraiment)', body: 'Bonjour {{prenom}},\n\nTu me connais un peu mieux maintenant. Je voulais te montrer concrètement comment je travaille : un appel découverte de 30 minutes, sans engagement ni pression.\n\n👉 Réserver mon appel : {{lien}}\n\nClaire' },
    callinvite: { subject: '{{prenom}}, réserve ton appel découverte', body: 'Merci pour tes réponses, {{prenom}} !\n\nIl ne reste qu’à choisir un créneau de 30 minutes.\n\n👉 {{lien}}\n\nClaire' },
    callconfirm: { subject: 'Ton appel découverte est confirmé', body: 'Bonjour {{prenom}},\n\nTon appel est confirmé : {{date}}.\n\nCet appel n’est PAS une vente forcée : c’est un moment pour toi. Tu n’as rien à préparer.\n\nClaire' },
    callreminder: { subject: 'Rappel : notre appel de demain', body: 'Bonjour {{prenom}},\n\nPetit rappel pour notre appel découverte : {{date}}. Installe-toi au calme.\n\nClaire' },
    proposition: { subject: '{{prenom}}, voici ta proposition personnalisée', body: 'Bonjour {{prenom}},\n\nSuite à notre échange, j’ai préparé ta proposition : {{offre}}.\n\n👉 {{lien}}\n\nTu as 30 jours de garantie « satisfaction » après la séance 2.\n\nClaire' },
    relance48: { subject: '{{prenom}}, as-tu pu regarder ta proposition ?', body: 'Bonjour {{prenom}},\n\nJe voulais simplement savoir si tu avais pu jeter un œil à ma proposition. Une question ? Réponds-moi directement.\n\nClaire' },
    relance5j: { subject: 'Dernier message de ma part sur ce sujet (promis)', body: 'Bonjour {{prenom}},\n\nJe ne vais pas t’envoyer 15 relances : ce n’est pas mon style. Si ce n’est pas le bon moment, c’est ok. Ma porte reste ouverte.\n\nClaire' },
    paid: { subject: '🎉 Bienvenue, {{prenom}} — ton aventure commence maintenant !', body: 'Bonjour {{prenom}},\n\nJe viens de recevoir ton contrat signé et ton règlement. Tu viens de faire quelque chose d’important : tu t’es choisie.\n\nTu as choisi : {{offre}}.\n\nPROCHAINES ÉTAPES : ton questionnaire d’onboarding, ton livret d’accueil, ta première séance.\n\n👉 {{lien}}\n\nClaire' },
    onboarding: { subject: 'Ton espace est prêt : voici tes 4 prochaines étapes', body: 'Bonjour {{prenom}},\n\nTout est en place. Dans ton espace : questionnaire, livret d’accueil, préparation de la séance 1 et ta feuille de route.\n\n👉 {{lien}}\n\nClaire' },
    session_cr: { subject: 'Compte-rendu de ta séance {{n}} — {{theme}}', body: 'Bonjour {{prenom}},\n\nVoici le compte-rendu de notre séance {{n}} ({{theme}}).\n\nCe que nous avons travaillé :\n{{notes}}\n\nTes exercices sont débloqués dans ton espace.\n\n👉 {{lien}}\n\nClaire' },
    exos_nudge: { subject: 'Tes exercices de la séance {{n}} t’attendent', body: 'Bonjour {{prenom}},\n\nQuelques minutes par jour suffisent. Coche-les dans ton espace au fur et à mesure.\n\n👉 {{lien}}\n\nClaire' },
    finalbilan: { subject: 'Bravo {{prenom}} ! Place à ton bilan de transformation', body: 'Bonjour {{prenom}},\n\nTu as terminé ton accompagnement. Prends 10 minutes pour mesurer le chemin parcouru.\n\n👉 {{lien}}\n\nClaire' },
    thanks: { subject: 'Merci du fond du cœur, {{prenom}}', body: 'Bonjour {{prenom}},\n\nMerci pour ton témoignage. Ton kit de recommandation est disponible : si une amie a besoin de ce déclic, tu peux le lui offrir.\n\n👉 {{lien}}\n\nClaire' },
    momentum: { subject: 'Garder ton élan avec le Suivi MOMENTUM', body: 'Bonjour {{prenom}},\n\nPour consolider ce que tu as construit : 2 séances de 45 minutes par mois, 450 €/mois, sans engagement de durée.\n\n👉 {{lien}}\n\nClaire' },
    reactivation: { subject: 'Comment tu vas, {{prenom}} ?', body: 'Bonjour {{prenom}},\n\nJe pense à toi aujourd’hui. Où en es-tu de tes objectifs ? Je serais ravie d’avoir de tes nouvelles.\n\nClaire' },
  };

  // Séquence de bienvenue (délais en jours) déclenchée à l'inscription
  const WELCOME_SEQUENCE = [['welcome2', 1], ['welcome3', 3], ['welcome4', 5], ['welcome5', 7], ['welcome6', 10]];

  /* ---------- Mise en route de Claire : 39 templates du document → checklist ---------- */
  // auto = géré par la plateforme (coché d'office) ; sinon cas manuel
  const LAUNCH = [
    { phase: 1, n: 'Page de présentation / mini-site', p: 'ESSENTIEL', auto: 'Site public Déclic' },
    { phase: 1, n: 'Script de présentation (elevator pitch)', p: 'ESSENTIEL', help: 'Pitch prêt à l’emploi : « Je suis la coach qui vous aide à vous remettre au centre de votre propre vie — pour que vos rêves ne restent plus en stand-by. »' },
    { phase: 1, n: 'Kit de recommandation client', p: 'ESSENTIEL', auto: 'Débloqué dans le portail après le bilan' },
    { phase: 1, n: 'Fiche de suivi des recommandations', p: 'RECOMMANDÉ', auto: 'Dossiers clientes (source + recommandations)' },
    { phase: 1, n: 'Posts LinkedIn (3-4 / semaine)', p: 'RECOMMANDÉ', tpl: 'C5', help: 'Lundi témoignage, mercredi conseil, vendredi réflexion personnelle.' },
    { phase: 1, n: 'Email de présentation / prise de contact', p: 'ESSENTIEL', auto: 'Séquence d’emails automatique' },
    { phase: 2, n: 'Questionnaire de pré-qualification', p: 'RECOMMANDÉ', auto: 'Étape 1 du parcours' },
    { phase: 2, n: 'Guide d’entretien découverte', p: 'ESSENTIEL', auto: 'Script A2 dans la bibliothèque', tpl: 'A2' },
    { phase: 2, n: 'Proposition commerciale personnalisée', p: 'ESSENTIEL', auto: 'Générée à chaque appel' },
    { phase: 2, n: 'Contrat de coaching / CGV', p: 'ESSENTIEL', auto: 'Signature en ligne' },
    { phase: 2, n: 'Emails de relance post-découverte', p: 'RECOMMANDÉ', auto: 'J+2 et J+5 automatiques' },
    { phase: 2, n: 'Grille de tarification et packages', p: 'ESSENTIEL', auto: 'Offres du catalogue' },
    { phase: 3, n: 'Email de bienvenue', p: 'ESSENTIEL', auto: 'Envoyé au paiement' },
    { phase: 3, n: 'Questionnaire d’onboarding', p: 'ESSENTIEL', auto: 'Étape « Je démarre »' },
    { phase: 3, n: 'Livret d’accueil', p: 'RECOMMANDÉ', auto: 'Débloqué au paiement' },
    { phase: 3, n: 'Checklist de préparation 1re séance', p: 'RECOMMANDÉ', auto: 'Dans le portail' },
    { phase: 3, n: 'Feuille de route client', p: 'RECOMMANDÉ', auto: 'Générée selon l’offre' },
    { phase: 4, n: 'Trame de séance de coaching', p: 'ESSENTIEL', auto: 'Fiche de séance dans le dossier cliente' },
    { phase: 4, n: 'Fiche de prise de notes par séance', p: 'ESSENTIEL', auto: 'Notes de séance enregistrées' },
    { phase: 4, n: 'Compte-rendu de séance', p: 'RECOMMANDÉ', auto: 'Envoyé automatiquement' },
    { phase: 4, n: 'Bibliothèque d’exercices', p: 'RECOMMANDÉ', auto: 'Débloquée séance par séance' },
    { phase: 4, n: 'Tableau de suivi de progression', p: 'RECOMMANDÉ', auto: 'Dossier cliente' },
    { phase: 4, n: 'Gestion des annulations et reports', p: 'ESSENTIEL', help: 'Règle conseillée : report gratuit jusqu’à 24 h avant. Elle figure dans le contrat.', auto: 'Règle dans le contrat' },
    { phase: 5, n: 'Bilan de mi-parcours', p: 'RECOMMANDÉ', auto: 'Après la séance 4' },
    { phase: 5, n: 'Bilan de fin d’accompagnement', p: 'ESSENTIEL', auto: 'Étape « J’ancre »' },
    { phase: 5, n: 'Questionnaire de satisfaction finale', p: 'ESSENTIEL', auto: 'Étape « J’ancre »' },
    { phase: 5, n: 'Demande de témoignage', p: 'ESSENTIEL', auto: 'Étape « J’ancre »' },
    { phase: 5, n: 'Offre de renouvellement (Momentum)', p: 'RECOMMANDÉ', auto: 'Email + portail' },
    { phase: 5, n: 'Programme de parrainage', p: 'RECOMMANDÉ', auto: 'Kit + suivi' },
    { phase: 5, n: 'Newsletter hebdomadaire', p: 'OPTIONNEL', help: 'À lancer après les 3 premiers mois. Ratio conseillé : 80 % valeur / 20 % promo.' },
    { phase: 6, n: 'CGV (version publiée sur le site)', p: 'ESSENTIEL', page: 'legal.html#cgv', help: 'Complète tes informations légales dans Réglages.' },
    { phase: 6, n: 'Politique de confidentialité RGPD', p: 'ESSENTIEL', page: 'legal.html#rgpd', auto: 'Page générée' },
    { phase: 6, n: 'Modèle de facture', p: 'ESSENTIEL', auto: 'Factures automatiques' },
    { phase: 6, n: 'Registre des traitements de données', p: 'RECOMMANDÉ', help: 'Modèle CNIL à compléter une seule fois.' },
    { phase: 6, n: 'Mentions légales', p: 'ESSENTIEL', page: 'legal.html#mentions', help: 'Nécessite ton SIRET et ton adresse (Réglages).' },
    { phase: 6, n: 'Modèle d’avoir', p: 'OPTIONNEL', help: 'À créer en cas de besoin.' },
    { phase: 6, n: 'Tableau de suivi comptable', p: 'ESSENTIEL', auto: 'Vue Finances' },
    { phase: 6, n: 'Contrat de sous-traitance', p: 'OPTIONNEL', help: 'Seulement si tu sous-traites.' },
    { phase: 6, n: 'Assurance RC Professionnelle', p: 'RECOMMANDÉ', help: 'Fortement conseillée : demande 3 devis et joins l’attestation.' },
  ];
  const PHASES = { 1: 'Acquisition & marketing', 2: 'Vente & conversion', 3: 'Onboarding', 4: 'Livraison', 5: 'Suivi & fidélisation', 6: 'Administration & légal' };

  // Contenu du guide (lead magnet) — condensé du document
  const GUIDE_MD = `# Les 5 blocages invisibles qui empêchent les femmes actives de passer à l’étape suivante

*Par Claire RTH — de la mise en veille à la mise en mouvement.*

## Pourquoi tu lis ce guide
Tu gères tout : le travail, les enfants, le quotidien. Et petit à petit, tu t’es oubliée. Ce n’est pas que tu ne peux pas, ni que tu ne veux pas : il y a trop de paramètres en jeu, et tu as besoin d’un regard extérieur pour décider.

## Blocage 1 — « Ce n’est pas le bon moment »
Il n’y aura jamais de bon moment. Cette phrase protège de l’échec, mais elle protège aussi de la vie que tu veux.
- **Signe :** tu repousses depuis plus de 6 mois.
- **Premier pas :** bloque 15 minutes cette semaine, rien que pour ton projet.

## Blocage 2 — Le syndrome de l’imposteur
Tu doutes de tes compétences malgré tes réussites.
- **Signe :** tu minimises tes succès (« j’ai eu de la chance »).
- **Premier pas :** écris 5 réussites professionnelles et ce que TU as fait pour les obtenir.

## Blocage 3 — La culpabilité de penser à soi
Penser à toi n’est pas voler du temps à ta famille : c’est leur montrer l’exemple.
- **Signe :** tu t’excuses dès que tu demandes quelque chose pour toi.
- **Premier pas :** demande une chose pour toi cette semaine, sans justification.

## Blocage 4 — La peur du regard des autres
« Et si on pensait que je veux trop ? »
- **Signe :** tu imagines les critiques avant d’avoir agi.
- **Premier pas :** parle de ton projet à une seule personne bienveillante.

## Blocage 5 — L’attente de la permission
Tu attends qu’on te choisisse, qu’on te le propose.
- **Signe :** tu espères qu’on remarque ton travail sans le dire.
- **Premier pas :** formule ta demande (augmentation, promotion, mobilité) en une phrase et dis-la à voix haute.

## Et maintenant ?
Si un de ces blocages te parle, réserve ton **appel découverte gratuit de 30 minutes**. Pas de pression : un moment pour toi.`;

  window.DECLIC = { BRAND, OFFERS, EXERCISES, FORMS, STAGES, RESOURCES, EMAILS, WELCOME_SEQUENCE, LAUNCH, PHASES, GUIDE_MD };
})();
