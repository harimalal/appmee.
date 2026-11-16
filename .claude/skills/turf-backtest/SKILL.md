---
name: turf-backtest
description: Tester sur des centaines de courses, avec les vrais rapports du PMU, si une idée de sélection de chevaux bat la cote (signaux, profils de course, fiabilité d'un hippodrome, méthode en 3 temps). À invoquer pour « teste cette idée », « est-ce que ça marche sur toutes les courses », « quel hippodrome est fiable », « backtest », « fais une modélisation », et chaque fois qu'une règle doit passer de « piste » à « établi ».
---

# Backtest des idées de sélection

Workflow W4 de `turf/WORKFLOWS.md`. Synthèse des résultats : `turf/SYNTHESE_MODELISATIONS.md`. Règles : `turf/REGLES_COURSES.md` (statuts établi, piste, rejeté).

## Méthode
1. **Fixer la règle avant le test** (pas de chasse aux corrélations) : critères, seuils, pari simulé.
2. **Données** : `historique_courses.jsonl` (cotes finales, cotes du matin, arrivée, vrais rapports) et `perfs_hist.jsonl` (5 dernières performances, avant la course). Exclure les courses de moins de 6 partants.
3. **Coupure chronologique** : première moitié pour construire, seconde pour valider. Comparer toujours avec les 3 plus bas cotés.
4. **Mesures** : places trouvées par course ; observé contre attendu par la cote (probabilité calibrée sur la cote, `proba_top3_82.csv`) ; régression logistique avec la cote en variable de base et regroupement par course pour l'intervalle de confiance ; retour sur mise avec les vrais rapports et intervalle à 95 %.
5. **Verdicts** : « établi » si confirmé hors échantillon sur 300 courses ; « piste » si non significatif ; « rejeté » si perdant ou sans effet. Corriger les comparaisons multiples (Holm).

## Scripts
- `analyse_profils.py`, `analyse2.py`, `analyse3.py` : couples et profils avec les vrais rapports.
- `fiabilite_hippodromes.py` : fiabilité des pistes (FIABLE, ALEATOIRE, dans la moyenne).
- `methode_3temps.py`, `regress_signaux.py` : écarter les évidents, signaux faibles, départage par la cote.
- `historique_chevaux.py`, `scenario1_complet.py`, `proba_top3.py`, `test_tendances.py`, `validation_novembre.py`, `simulation_jeu.py` : modélisations d'origine.

## Rappels de résultats (ne pas refaire sans raison)
- La cote bat chaque signal testé ; trier par signaux perd 0,05 à 0,25 place par course.
- Le prélèvement du PMU (25 à 30 %) explique la perte moyenne.
- Les disqualifications n'existent qu'au trot : trois quarts des surprises à Vincennes et Caen.
- Pistes ouvertes : baisse de la cote depuis le matin (p = 0,07), signal « classe » (p = 0,013 non corrigé), favori du trot attelé au simple placé (+9,7 %), alerte de fautes.

## Honnêteté
Dire combien de courses, quelle période, quel intervalle ; ne jamais présenter un gain simulé sur peu de courses comme un avantage. Après chaque test, mettre à jour `REGLES_COURSES.md` et le cockpit.
