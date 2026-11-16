# BENCHMARK — site-novolens-agence

Les sources sont des blogs d'agences et des standards. Les chiffres de blogs ne vont dans aucun livrable ; seuls les seuils de standards (W3C, web.dev) sont repris.

## Conversion d'une page B2B (accueil, tarifs, contact)
- Cas 1 : Exemples de pages B2B (Perspective) — https://www.perspective.co/article/b2b-landing-page-examples
  Pattern extrait : une promesse unique en tête, une preuve chiffrée, un seul appel à l'action répété, un formulaire court. Les pages les plus performantes citées gardent un objectif unique par page.
  Chiffres : non repris (auto-déclarés).
- Cas 2 : Plan de page de génération de leads (Directive) — https://directiveconsulting.com/blog/lead-generation-landing-page-blueprint-for-qualified-pipeline/
  Pattern extrait : ordre promesse, problème, méthode, preuve, objection, appel à l'action ; réponse aux objections juste avant le formulaire.
  Chiffres : non repris.
- Cas 3 : Pages de démonstration B2B analysées (Apexure) — https://www.apexure.com/landing-page-examples/b2b-bandits-landing-page
  Pattern extrait : un cas détaillé avec métriques de pipeline pèse plus que plusieurs témoignages vagues ; cohérence entre titre et promesse.
  Chiffres : non repris.
Adaptation retenue : accueil = promesse, problème, méthode animée, livraison, preuve, objection (FAQ courte), un appel à l'action unique « réserver 15 min » ; une page cas client modèle avec contexte, action, résultat ; formulaire de 5 champs maximum (prénom, nom, e-mail pro, entreprise, objectif) avec téléphone facultatif.

## Performance et accessibilité (seuils)
- Cas 1 : Core Web Vitals, seuils « bon » (web.dev) — https://web.dev/articles/defining-core-web-vitals-thresholds
  Pattern extrait : LCP au plus 2,5 s, INP au plus 200 ms, CLS au plus 0,1, jugés au 75e centile. (LCP confirmé par sources secondaires.)
  Chiffres : seuils officiels.
- Cas 2 : WCAG 1.4.3 contraste minimum (W3C) — https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
  Pattern extrait : 4,5:1 pour le texte normal, 3:1 pour le grand texte (18 pt ou 14 pt gras).
  Chiffres : seuils officiels.
- Cas 3 : Mouvement et `prefers-reduced-motion` (Deque, spécification) — https://dequeuniversity.com/checklists/web/animation-motion-timed
  Pattern extrait : la requête de média est le moyen courant de désactiver le mouvement ; WCAG 2.3.3 est un critère AAA, donc un objectif de bonne pratique et non une obligation AA.
  Chiffres : sans objet.
Adaptation retenue : budgets de poids du brief (image au plus 250 Ko, HTML hors images au plus 60 Ko), images différées sous la ligne de flottaison, dimensions déclarées pour éviter les décalages de mise en page, contrastes calculés par script (AA), mouvement réduit respecté.

## Animation narrative au défilement
- Cas 1 : Pages produit de Linear — décrites par https://www.webstacks.com/blog/saas-home-page
  Pattern extrait : l'interface s'anime pendant qu'on passe devant la description d'une fonction ; l'animation démontre le comportement.
  Chiffres : sans objet. (Description secondaire à confirmer.)
- Cas 2 : Accueil de Stripe — décrit par https://framer.com/blog/website-animation-examples
  Pattern extrait : animation tenue et liée au défilement, une promesse en une ligne puis la preuve ; mise en garde : le dégradé animé est devenu générique.
  Chiffres : sans objet.
- Cas 3 : Pages d'Apple (référence du récit au défilement) — https://scrollersites-6fg.pages.dev/resources/apple-style-scroll-animation/
  Pattern extrait : progression d'animation liée à la position de défilement.
  Chiffres : avertissement de coût sur appareils lents (animations lourdes de 500 Ko à 2 Mo).
Adaptation retenue : animations en SVG/CSS léger qui montrent l'action et le gain, déclenchées à l'entrée à l'écran, sans dépendance et sans cacher le contenu à l'arrêt ; éviter l'effet de dégradé animé générique.

## Réécriture du texte, mise en forme du design system, 404, plan du site
Dispense : tâches mécaniques sur un contenu et une charte déjà fournis, sans chiffre externe.
