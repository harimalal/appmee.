---
name: turf-bilan-reunion
description: Présenter l'analyse d'une course de trot dans le format structuré de Hari (configuration de la course, tableau d'analyse avec cotes, arrivée des 4 premiers et lesquels viennent de l'analyse, gains simulés avec les vrais rapports) et tenir le bilan d'une réunion ou d'une série. À invoquer pour « bilan de la réunion », « format structuré », « résultats Vincennes / Caen », « enregistre les résultats », « compare avec les 3 premières cotes », ou à la fin de chaque lecture de course.
---

# Bilan structuré d'une course ou d'une réunion

Workflow W3 de `turf/WORKFLOWS.md`. Résultats enregistrés dans `turf/RESULTATS_<HIPPODROME>_<date>.md` et `turf/resultats/analyses_<date>.csv`.

## Format d'une course (toujours le même)
1. **Configuration de la course** (tableau) : discipline, distance, allocation et catégorie, conditions, nombre de partants et non-partants, départ, risque de faute de l'hippodrome (disqualifiés à Vincennes monté 29 %, Caen attelé 43 %), pronostic Equidia, lisibilité.
2. **Tableau d'analyse** : N°, cheval (jockey), **cote au départ**, lecture en une ou deux phrases, score en %. Regrouper les chevaux faibles. Les 3 retenus en gras.
3. **Arrivée des 4 premiers** : rang, N°, cheval, cote, score dans l'analyse, « issu de l'analyse ? » (oui, partiellement, non).
4. **Gains simulés** sur les 3 retenus avec les rapports officiels de l'API PMU : 1 € gagnant sur chacun, 3 couples en couplé placé + 2 sur 4 (le 2 sur 4 n'existe pas à 8 partants, la mise est alors de 3 €), 3 simples placés.
5. **Vérification** : disqualifiés et leur score, comparaison avec les 3 premières cotes (nombre de places trouvées), total courant de la série.

## Calcul des gains
- Rapports : `/rapports-definitifs`, `dividendePourUnEuro` en centimes ; ignorer les lignes `NP` (non-partant) ; couple placé et 2 sur 4 indexés par combinaison triée.
- Net d'un couple = (couple placé + 2 sur 4) − 2 € ; net total = somme des 3 couples.
- Base de comparaison : les 3 plus bas cotés ; nombre de places trouvées sur la même course.

## Honnêteté
- Dire si l'analyse est **après coup** (arrivée connue) ou **aveugle** (avant le départ, horodatée).
- Ne pas conclure sur moins de 50 courses ; rappeler que les gains simulés dépendent d'un ou deux outsiders.
- Signaler les omissions (un cheval non noté) et les corrections.

## Enregistrement
Après chaque course ou réunion : ajouter la ligne au CSV, mettre à jour le fichier `RESULTATS_*`, puis écrire dans le cockpit (skill `cockpit`) : étapes faites, livrables.
