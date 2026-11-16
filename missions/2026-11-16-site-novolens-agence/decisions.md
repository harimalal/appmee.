# DÉCISIONS — site-novolens-agence

## Choix validés au cadrage
Recopiés depuis `brief.md` (verrouillé) : site statique multi-pages, un seul appel à l'action par page, animations HTML/SVG et photos Unsplash, niveau agence défini par critères vérifiables, thème clair, fonds alternés blanc et dégradé violet.

## Fiches des rôles
### Directeur artistique (expert de domaine)
- Sortie attendue : design-system.html, validation visuelle
- Droit de veto : sortie de charte, alternance des fonds
- Exigence portée : élégance
- Sortie de scène : design system validé et dernière page relue
- Persona : s'inspire des studios de design B2B qui documentent leurs composants avant les pages ; refuse le dégradé animé générique relevé au benchmark.

### Responsable conversion et texte (expert de domaine)
- Sortie attendue : contenu.md
- Droit de veto : phrase promettant un résultat non sourcé
- Exigence portée : fiabilité
- Sortie de scène : contenu relu et intégré
- Persona : rédacteur de pages B2B qui suit le plan promesse, problème, méthode, preuve, objection, appel.

### Motion designer (expert de domaine)
- Sortie attendue : animations des étapes
- Droit de veto : animation qui cache du contenu ou ignore le mouvement réduit
- Exigence portée : simplicité
- Sortie de scène : animations validées à 3 largeurs

### Développeur front et performance
- Sortie attendue : code des pages, guide
- Droit de veto : dépassement des budgets de poids, accessibilité cassée
- Exigence portée : fiabilité
- Sortie de scène : audit technique passé

### Vérificateur
- Sortie attendue : rapport-audit.md
- Droit de veto : affirmation non sourcée
- Exigence portée : fiabilité
- Sortie de scène : audit passé sur tous les livrables

## Débats structurants

### Décision #1 : ajouter un simulateur de gain sur la page Tarifs
- Tour 1 — Conversion : un simulateur rend la valeur concrète (valeur d'un client, nombre de rendez-vous, taux de signature) — preuve : les guides B2B recommandent de montrer la valeur avant le prix — coût : un script court — signal : le résultat serait pris pour une promesse.
- Tour 1 — Vérificateur : risque de chiffres pris pour une garantie — preuve : aucune donnée de performance fournie — signal : étiquette absente.
- Tour 2 : le simulateur ne contient aucune valeur par défaut présentée comme un résultat ; il calcule uniquement à partir des chiffres saisis par le visiteur, avec une mention « estimation à partir de vos propres chiffres ».
- CLÔTURE : simulateur retenu avec saisie visiteur et mention explicite — motif : fiable > évident > beau — écarté : valeurs préremplies présentées comme résultats — Réversible : oui, coût faible.

### Décision #2 : structure de la page cas client modèle
- Tour 1 — Conversion : contexte, action, résultat chiffré, citation, appel unique (pattern Apexure du benchmark).
- Tour 1 — Vérificateur : toute donnée doit être étiquetée « exemple » tant qu'il n'y a pas de vrai client.
- Tour 2 : gabarit complet avec bandeau « Exemple illustratif » visible en haut et sur chaque chiffre.
- CLÔTURE : gabarit étiqueté — motif : contrainte dure du brief (aucun chiffre non étiqueté) — écarté : faux client crédible sans étiquette — Réversible : oui.

### Décision #3 : barre d'appel à l'action collante sur mobile
- Tour 1 — Conversion : un bouton collant maintient l'appel unique visible. Développeur : risque de masquer le contenu et de gêner le pied de page.
- Tour 2 : barre discrète, masquée près du formulaire et du pied de page, respect des zones de sécurité des téléphones.
- CLÔTURE : barre collante mobile retenue avec masquage près du formulaire — motif : doctrine (appel unique) — Réversible : oui.

## Décisions d'exécution (non structurantes)
- 2026-11-16 — sources recopiées dans `livrables/site-src/`, sortie du site dans `livrables/site/` (MAESTRO)
- 2026-11-16 — fichiers de texte (contenu, guide) confiés à un sous-agent, le site et l'audit restent au chef de mission (MAESTRO)
