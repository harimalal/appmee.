# BENCHMARK — prosens-site-vente

Limite de méthode : les pages des concurrents n'ont pas pu être lues directement (l'hôte belkins.io est hors du réseau autorisé de la session, lecture tentée le 2026-11-06). Les patterns ci-dessous viennent d'extraits de résultats de recherche. Les sources sont en majorité commerciales (blogs de vendeurs, annuaires, comparatifs) : prix et taux de conversion sont **indicatifs** et n'iront dans aucun livrable.

## Positionnement face aux prestataires de prise de rendez-vous
- Cas 1 : Belkins — https://belkins.io/outsourced-sales.md (extraits de recherche)
  Pattern extrait : offre d'entrée chiffrée (« From $5,000 »), promesse de volume (« 100+ guaranteed appts / year ») avec une rubrique « The guarantee », et parcours d'escalade : prise de rendez-vous d'abord, puis équipe de SDR dédiée. Contre-intuitif : la page appointment-setting du même acteur précise qu'il ne peut pas garantir de résultats immédiats (https://belkins.io/appointment-setting).
  Chiffres : tarifs relevés par des tiers entre 5 000 et 14 800 dollars par mois, sources divergentes.
- Cas 2 : CIENCE — https://saleshive.com/vendors/cience (fiche d'annuaire) et blog de CIENCE
  Pattern extrait : prise de rendez-vous à la performance, « GTM System Setup » en 5 jours (la rapidité devient une preuve datée), prix « custom » selon la taille d'équipe et le périmètre.
  Chiffres : aucun chiffre fiable (la fiche affiche « $200+ / mo » en contradiction avec les autres sources).
- Cas 3 : offres françaises indépendantes (plateforme Comeup) — https://comeup.com/fr/service/486174/decrocher-vos-rendez-vous-b2b-qualifies-grace-a-une-prospection-efficace-et-100-a-la-performance
  Pattern extrait : rémunération au rendez-vous confirmé et accepté par le prospect, frais ou commission en plus par contrat conclu chez certains ; la définition du « qualifié » (acceptation explicite, rendez-vous tenu, cible conforme) est ce qui fait varier la valeur de l'offre.
  Chiffres : environ 45,88 et 57,14 dollars par rendez-vous selon deux annonces (freelances, non comparables à une agence).
Adaptation retenue pour la mission : ne pas copier la promesse de volume (Belkins la nuance lui-même). Afficher à la place ce que les offres françaises laissent flou : la **définition écrite** du rendez-vous qualifié, le **closing** qui prolonge le rendez-vous, et un **profil de fondateur** terrain. Pas de prix affiché (CIENCE, prix sur mesure).

---

## Structure d'une page de vente B2B de services
- Cas 1 : Linear (pages de fonctionnalités) — décrit dans https://htmlburger.com/blog/animation-in-b2b-websites-guide/ et https://www.bopdesign.com/bop-blog/2024/06/scrolling-animation-b2b-web-design/ (analyses de tiers, pages non lues)
  Pattern extrait : le défilement pilote une démonstration : en passant devant la description d'une fonction, l'interface s'anime pour montrer le comportement. Le mouvement sert à **expliquer le mécanisme**, pas à décorer.
- Cas 2 : Stripe (accueil et tarifs) — même source d'analyse
  Pattern extrait : effets liés au défilement (dégradé, cartes en 3D) volontairement retenus ; la séquence de la page est claire.
- Cas 3 : repères de conversion — https://predictableprofits.com/b2b-cro-benchmarks-by-industry-2025/ et https://www.revenuehero.io/blog/inbound-conversion-benchmarks-what-good-looks-like (sources commerciales)
  Pattern extrait : une page à une seule action ; pages de demande d'appel entre 1,5 % et 4 % ; services B2B 2,6 % en moyenne et 7,2 % pour le quart supérieur (non comparables entre eux).
Adaptation retenue pour la mission : une seule action (réserver un échange), répétée ; une séquence narrative claire (problème, mécanisme, définition du qualifié, offre, fondateur, objections) ; un mécanisme **démontré par un mouvement lié au défilement** (le rendez-vous qui se remplit dans l'agenda). Aucun taux de conversion n'est promis.

---

## Mouvement et accessibilité
- Cas 1 : guide « Animation in B2B websites » — https://htmlburger.com/blog/animation-in-b2b-websites-guide/
  Pattern extrait : risques principaux = performance et référencement ; préférer CSS et SVG au JavaScript quand c'est possible.
- Cas 2 : synthèse « Animation Systems (Stripe × Linear × Apple × Vercel) » — https://claudepluginhub.com/skills/rushyop-better-ux-quality-plugins-better-ux-quality/animation-systems
  Pattern extrait : peu d'animations, bien choisies ; un moment fort sur la page, le reste en appui ; le repli `prefers-reduced-motion` est à décider avant de construire.
- Cas 3 : norme WCAG 2.2, critères 2.2.2 (mettre en pause, arrêter, masquer) et 2.3.3 (animation issue d'interactions) — référence normative, non relue ici
  Pattern extrait : tout mouvement qui dure ou défile doit pouvoir être évité ; l'information ne dépend jamais du mouvement.
Adaptation retenue pour la mission : CSS et IntersectionObserver ; l'état final de chaque animation est l'état par défaut du HTML (contenu visible sans JavaScript et sans mouvement) ; un seul moment fort ; le mouvement est retiré sous `prefers-reduced-motion`.
