# AUDIT — prosens-site-vente

Une ligne par livrable et par passe. Verdict : `OK` (score >= 80 et aucun critère à 0 ou 1) ou `A_CORRIGER`. 2 passes maximum, sinon blocage. Voir `references/quality-gates.md`.

Vérification mécanique faite avant le score (colonne note) : ouverture, rendu, tests, recomptage… ou limite signalée.

| livrable | grille | passe | score | critère min | verdict | note |
|---|---|---|---|---|---|---|
| L01-prosens | ad hoc (page de vente) | 1 | 83 | 4 | OK | Vérification mécanique d'abord : 4 défauts trouvés et corrigés avant le score (débordement horizontal de 13 px à 375 px, double espace du bouton d'en-tête, heures de l'agenda coupées, note du tableau coupée sur mobile) puis visuel collant mobile corrigé. Résultat final : 375, 768 et 1440 px sans défilement horizontal ni erreur console, 21 éléments atteints au clavier, panneau et onglets testés, mouvement réduit sans aucune animation active, contenu visible sans JavaScript, contrastes de 5,6 à 13,9 pour 1. Clarté 16/20, différenciation 12/15 (pages concurrentes non lues directement), honnêteté des preuves 12/15 (engagements à faire valider, voir L02), design 16/20, mouvement 15/15, technique 12/15 (vitesse et référencement non mesurés). |
| L02-guide-mise-en-ligne.md | document formel | 1 | 84 | 4 | OK | Destinataire et usage 20/25, structure 16/20, exact et sourcé 16/20 (repères de conversion indicatifs signalés comme tels), actionnable 20/20, mise en forme 12/15. Relu : aucun placeholder, chemins et noms de fichiers vérifiés. |
