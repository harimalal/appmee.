# AUDIT — site-novolens-agence

Une ligne par livrable et par passe. Verdict : `OK` (score >= 80 et aucun critère à 0 ou 1) ou `A_CORRIGER`.

Vérification mécanique faite avant le score : rendu Playwright à 400, 820 et 1360 px, console, débordement, poids, contrastes calculés, clavier, mouvement réduit (livrables/audit/resultat.json). Limites dites : pas de Lighthouse, pas de mesure LCP/INP/CLS, pas de test sur appareils réels ni de lecteur d'écran ; thème sombre non applicable (clair uniquement, voulu par le brief).

| livrable | grille | passe | score | critère min | verdict | note |
|---|---|---|---|---|---|---|
| L01-site.md (dossier site) | ad hoc brief (charte 20, valeur 20, accessibilité 20, perf et SEO 20, texte 20) | 1 | 72 | 3 (texte) | A_CORRIGER | relecture : index incomplet pour le dépôt, textes de remplissage, chiffres incohérents, comparatif non neutre |
| L01-site.md (dossier site) | idem | 2 | 85 | 4 | OK | charte 5, valeur 4, accessibilité 4, perf et SEO 4, texte 4 ; audit mécanique 9 pages au vert ; perf non mesurée en conditions réelles |
| L02-design-system.html | idem | 1 | 84 | 4 | OK | 15 paires de contraste calculées ; une seule largeur testée |
| L03-contenu.md | base (25/25/20/15/15) | 1 | 84 | 4 | OK | 126 citations sur 205 retrouvées telles quelles dans le site ; les autres sont des reformulations proposées ou des textes retirés ; aucun marqueur de remplissage |
| L04-guide.md | base | 1 | 84 | 4 | OK | procédures non exécutées de bout en bout (hébergement, formulaire) ; reconstruction du site vérifiée |
| L05-rapport-audit.md | base | 1 | 88 | 4 | OK | chiffres issus de resultat.json ; limites listées |
| site-src (sources du site) | base | 1 | 84 | 4 | OK | reconstruction vérifiée (build.py produit les 9 pages) ; code relu, pas de test unitaire |
| site-artefact (variante fragment) | base | 1 | 84 | 4 | OK | sert uniquement à l'aperçu privé ; contrôlée par la publication |
| audit (script et résultats) | base | 1 | 84 | 4 | OK | script exécuté trois fois sur les pages ; résultats dans resultat.json |
