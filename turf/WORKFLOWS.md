# Workflows du projet Turf

Cinq enchaînements pour reproduire ce qui a été fait. Chaque workflow a son skill (`.claude/skills/turf-*`). Toutes les commandes se lancent depuis `turf/scripts/` avec un **dossier de travail local** `courses/` qui contient un sous-dossier `data/` (non versionné). Python 3 avec `numpy`, `pandas`, `statsmodels`, `scikit-learn`, `scipy`. Toujours lancer avec `python3 -I`.

```
courses/                     # dossier de travail (hors dépôt)
  data/
    historique_courses.jsonl   # courses collectées (PMU) : cotes, arrivée, rapports
    perfs/<id_cheval>.json     # carrière complète d'un cheval (letrot, cache privé)
    perfs_hist.jsonl           # 5 dernières performances par course (PMU)
    deep/<date>_<code>_C<n>.json  # page course letrot (partants, flags, pronostic Equidia)
    comments_prev.jsonl        # commentaires de fin de course lus
    series/ fiches/ web/live/  # relevés et fiches du direct
```

## Règles de collecte
- **PMU** (`online.turfinfo.api.pmu.fr/rest/client/7/programme/<JJMMAAAA>[/R<r>/C<c>[/participants|/rapports-definitifs|/performances-detaillees/pretty]]`) : API publique, plusieurs requêtes en parallèle acceptées, une pause d'une seconde par requête.
- **letrot.com** : usage privé, **une requête toutes les 3 secondes** (3,5 s pour les commentaires), jamais plus de 5 requêtes en parallèle, jamais de contournement de protection. Les pages sont lues puis effacées pour les commentaires.
- Ne jamais committer ni publier de données letrot.
- Les rapports PMU sont en centimes (`dividendePourUnEuro`) ; le 2 sur 4 paie un rapport fixe ; il n'existe pas à 8 partants.

## W1 — Collecter l'historique des courses (pour tester)
1. `collecte_historique.py <sortie.jsonl> <jour_début> <jour_fin>` : pour chaque jour, du plus récent au plus ancien, enregistre cotes finales, cotes du matin, arrivée, disqualifiés, terrain, allocation et rapports (SIMPLE_GAGNANT, SIMPLE_PLACE, COUPLE_PLACE, COUPLE_GAGNANT, DEUX_SUR_QUATRE, TRIO). Environ 66 courses par jour, 1 heure pour 60 jours. Lancer en tâche de fond.
2. `collecte_perfs.py <dossier>` : 5 dernières performances détaillées de chaque partant des courses d'attelé collectées (cinq requêtes en parallèle, environ 6 minutes pour 1 036 courses).

## W2 — Lire une course cheval par cheval (le protocole TURFITUP)
1. Trouver le code letrot de l'hippodrome dans la page du jour `https://www.letrot.com/courses/<AAAA-MM-JJ>` (`numHippodrome` : 7500 Vincennes, 1400 Caen).
2. `deep_fetch.py <dossier> <AAAA-MM-JJ> <code> <courses>` : page course letrot de chaque course et carrière complète de chaque partant (cache `perfs/`).
3. `deep_comments.py <dossier> <AAAA-MM-JJ> <code> <courses>` : commentaires de fin de course des 5 dernières courses de chaque partant (une page par course passée, partagée entre les chevaux).
4. `dossier_cheval.py <dossier> <AAAA-MM-JJ> <course> <nb_courses> <code>` : pour chaque cheval, les N dernières courses avec place, cote, chrono, driver, ferrure et commentaire. **Exclut tout ce qui est daté du jour de la course** (étape 1 du protocole).
5. `stats_course.py <dossier> <AAAA-MM-JJ> <code> <course> <A|M> --cotes <réunion>` : conditions de la course, pronostic Equidia, stats driver / entraîneur / tandem sur l'échantillon en cache (courses, victoires, placés, disqualifications) et cotes du matin et du départ.
6. **Lecture manuelle** selon `references/protocole-pronostic-trot.md` : musique et tendance, correspondance hippodrome / catégorie / distance, chrono à distance équivalente, driver et entraîneur séparés, commentaires, face-à-face, carrière étendue, rentrée.
7. **Notation** : grille en % (85-95 dossier complet, 65-84 solide, 40-64 incertain, moins de 40 contradiction) ; seuil de 60 % pour retenir un cheval ; trio seulement si 3 dossiers dépassent 60 % ; sinon 2 bases et un 3e en couverture ; aucun cheval à 60 % : passer la course.
8. **Lisibilité** : facile, modérée ou difficile, avec la raison factuelle (étape 5 du protocole).
9. Alertes de fautes à rétrograder, jamais à exclure sur un seul signal : DQ à la dernière sortie, 2 DA ou plus sur 8 courses, jockey à plus de 30 % de disqualifications.

## W3 — Bilan d'une course et d'une réunion
Format structuré, toujours le même :
1. **Configuration de la course** : discipline, distance, allocation, conditions, partants, départ, risque de faute de l'hippodrome, pronostic Equidia, lisibilité.
2. **Tableau d'analyse** : N°, cheval (jockey), cote au départ, lecture, score.
3. **Arrivée des 4 premiers** : numéro, cheval, cote, score dans l'analyse, « issu de l'analyse ? » (oui, partiellement, non).
4. **Gains** sur les 3 retenus : 1 € gagnant sur chacun, 3 couples en couplé placé + 2 sur 4, simples placés, avec les vrais rapports.
5. **Vérification** : disqualifiés, comparaison avec les 3 premières cotes (nombre de places trouvées), total courant.
6. Enregistrer la ligne dans `resultats/analyses_<date>.csv` et mettre à jour les fichiers `RESULTATS_*`.

## W4 — Tester une idée à grande échelle (backtest)
Toujours sur les vrais rapports, avec une coupure chronologique (première moitié pour fixer les règles, seconde moitié pour les tester) et un intervalle de confiance.
- `analyse_profils.py`, `analyse2.py`, `analyse3.py` : profils de course et couplés avec les vrais rapports.
- `fiabilite_hippodromes.py` : fiabilité de chaque piste.
- `methode_3temps.py` et `regress_signaux.py` : méthode « écarter les évidents, signaux faibles, départager par la cote » et effet de chaque signal au-delà de la cote.
- `proba_top3.py`, `scenario1_complet.py`, `historique_chevaux.py`, `test_tendances.py`, `validation_novembre.py`, `simulation_jeu.py` : modélisations d'origine (logit, Plackett-Luce, arbres, 21 signaux).

## W5 — Suivi en direct d'une réunion
1. `live_watch.py` : relevés de cotes toutes les 20 secondes jusqu'au départ (`data/series/`).
2. `pmu_live.py <dossier> <JJMMAAAA> <réunion> <courses>` : lecture avant course (lisibilité, profil, règles appliquées, mouvements de cote depuis le matin, flags Geny).
3. `fiche_course.py <dossier> <JJMMAAAA> <réunion> <course> [--prevus a,b,c]` : fiche standard (chevaux à T-5, mouvements à T-3, arrivée, rapports officiels, résultat des couples).
4. Test aveugle : appliquer W2 **avant** le départ, horodater le choix, comparer ensuite au favori à la cote.
