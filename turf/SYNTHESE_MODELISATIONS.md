# Synthèse des modélisations — projet Turf (13 au 15/11/2026)

Tous les chiffres viennent de l'API PMU et de letrot.com, avec les **vrais rapports officiels** quand ils sont cités. « Cote » = cote finale PMU avant le départ. « Attendu par la cote » = nombre de places que la cote prévoit (probabilité calibrée sur les données).

## Verdict en cinq lignes
1. **La cote PMU est le meilleur prédicteur disponible.** Aucun modèle ni aucun signal testé ne la bat de façon fiable (jusqu'à 21 signaux, forêts, arbres, logit conditionnel, Plackett-Luce).
2. **Le prélèvement du PMU (25 à 30 %) explique la perte moyenne.** Une journée complète de lecture en direct à Vincennes donne −25 %, soit le niveau du prélèvement.
3. **Le filtre de course aide plus que les signaux du cheval** : lisibilité de la course (cote concentrée, favori net) et nombre de partants. Il sert à éviter les courses où la cote elle-même est peu fiable, pas à gagner de l'argent.
4. **Le trot a un aléa propre** : les disqualifications pour allure irrégulière (environ un partant sur six, 2,6 à 2,8 par course en attelé, jusqu'à 43 % à Caen). Elles n'existent pas au galop, en haies ni en steeple.
5. **Piste unique à suivre :** le favori du trot attelé joué au simple placé (+5 à +10 %, érosion dans le temps, non confirmé). Aucun pari de couplé n'est rentable dans les tests.

## Chronologie des modélisations

| Phase | Données | Méthodes | Résultat |
|---|---|---|---|
| **1. Premier cadrage (13/11)** | 40 courses d'attelé de Vincennes (21/11/2025 au 23/10/2026), 600 partants, 98 courses pour les compositions de top 4 | Logit conditionnel, Plackett-Luce, forêt aléatoire, paris simulés hors échantillon | La cote presse trouve environ 2 chevaux du top 4 sur 4 (0,6 au hasard), AUC 0,70 à 0,74. Aucun modèle ne la bat. Règles 1 à 28 |
| **2. Validation (14/11 matin)** | 82 courses de Vincennes (40 d'origine + 42 de novembre), 1 173 partants, historique complet des chevaux (37 782 courses passées) | 21 signaux (classe, forme, hippodrome, jockey, marché, physique), modèle probabiliste du top 3, simulation de jeu complet | Cote seule : 1,26 place sur 3 choisis ; cote + signaux : 1,21 à 1,26 ; arbres : 1,10 à 1,22. Probabilités calibrées (annoncées 45-60 % : 48 % réels). Aucun groupe de signaux n'améliore la cote |
| **3. Lecture en direct (14/11)** | 12 courses de Vincennes et Caen, relevés toutes les 20 secondes | Fiche standard par course, 3 couples prévus à T-3 (couplé placé + 2 sur 4) | −16,70 € sur 11 courses réglées. Les disqualifications expliquent beaucoup de surprises |
| **4. Collecte large (14/11 soir)** | 3 076 courses du 15/09 au 13/11/2026, toutes disciplines, avec cotes, arrivée et rapports officiels ; 2 167 exploitables | Comparaison des disciplines, fiabilité par hippodrome, profils, ROI des couples avec les vrais rapports | Voir tableaux ci-dessous |
| **5. Méthode en 3 temps (15/11)** | 1 035 courses d'attelé, 62 hippodromes, 13 448 chevaux, 5 dernières performances de chacun | Écarter les évidents, signaux faibles, départager par la cote | Les signaux n'ajoutent rien à la cote ; trier par signaux perd des places |
| **6. Protocole TURFITUP** | Documents de Hari (`references/`), Vincennes 14/11 (7 courses) et Caen 14/11 (3 courses lues à fond) | Lecture cheval par cheval : carrière complète, commentaires de fin de course, driver et entraîneur, face-à-face | 9 places sur 21 contre 11 pour les 3 premières cotes ; voir `RESULTATS_*` |

## Ce qui est établi
- La cote finale trouve 1,85 cheval du top 4 sur 4 (AUC 0,73) ; elle reste bien calibrée sur 315 courses (Vincennes et Enghien).
- **Ne jouer que les courses lisibles** : 2,15 chevaux du top 4 trouvés en course lisible contre 1,14 en course peu lisible (rho 0,44, p = 0,004).
- Ne pas jouer les outsiders à plus de 40 (0 victoire sur 100 chevaux, −79 % au placé).
- Aucun bonus pour l'expérience de la piste, la classe (Crack Series), la ferrure, le nouveau driver, la rentrée, la vitesse de fin ou le record : tout cela est déjà dans la cote.
- Petit lot (14 partants ou moins) : le gagnant a une cote inférieure à 5 dans 64 % des courses, contre 31 % en grand lot (p = 0,002).

## Pistes non confirmées (à suivre en direct)
| Piste | Preuve | Statut |
|---|---|---|
| Favori sans avis favorable de l'entraîneur : jouable ; avec avis favorable : méfiance | 26 placés pour 36 attendus, p = 0,005 (0,06 corrigé) | contredite deux fois le 14/11 : fragile |
| Baisse de la cote depuis le matin (course visée) | Rapport 0,925 par unité de baisse, p = 0,07 sur 1 026 courses | piste |
| Signal « classe » (le cheval a bien couru à une allocation supérieure ou égale) | Rapport 1,10, p = 0,013 (non corrigé sur 6 signaux) | piste |
| Fautes récentes (2 DA ou plus sur 8 courses) : 2 fois plus de disqualifications | 15 % contre 7 % sur 63 attelés à Caen | piste |
| Favori du trot attelé placé au simple | +9,7 % sur 738 courses (tiers de période : +18 %, +9 %, +6 %) | à surveiller, érosion |

## Ce qui est rejeté
- Cocher toutes les cases (forme, distance, hippodrome, driver, tandem) : le nombre de cases suit la cote (6 cases ou plus : 25 % de placés pour 29 % attendus).
- Modèle à 21 signaux, arbres, forêt aléatoire : jamais meilleurs que la cote ; forêt au gagnant −33 à −39 %.
- Graphique de type Visuturf (version approchée) : 0,91 place sur 3 contre 1,24 pour la cote (p < 0,01).
- Mélange de plusieurs cotes presse : pas d'amélioration.
- Trier les chevaux par signaux avant la cote : −0,05 à −0,25 place par course sur 1 035 courses.

## Tests à grande échelle (octobre à novembre 2026, vrais rapports)

**Disciplines (298 courses, 6 jours)**

| Type | Courses | Favori gagne | Favori dans les 3 | Disqualifiés par course |
|---|---|---|---|---|
| Trot attelé | 157 | 29 % | 63 % | 2,64 |
| Trot monté | 19 | 37 % | 53 % | 2,84 |
| Galop (plat) | 89 | 22 % | 53 % | 0 |
| Haies | 20 | 20 % | 60 % | 0 |
| Steeple-chase | 11 | 45 % | 64 % | 0 |

**Hippodromes (1 035 courses d'attelé, indicateur : places trouvées par les 3 premières cotes, moyenne 1,47)**
- Plus fiables : Krieau 2,00, Nantes 1,94, Wolvega 1,92, Avenches 1,88, Son Pardo 1,79 (petits lots d'environ 10 partants, peu de disqualifications).
- Dans la moyenne : Vincennes 1,36 (144 courses), Enghien 1,46, Cabourg 1,45.
- **Aléatoires : Caen 1,12 (4 disqualifiés par course), Graignes 1,14.**

**Jeux testés sur 2 167 courses, vrais rapports**

| Jeu | Résultat |
|---|---|
| Toutes courses, couple placé favori + 2e cote | −26 % |
| Trot attelé, favori à moins de 1,8 | −21 % |
| Trot attelé, favori entre 1,8 et 2,5 | −11 % (±17) |
| Galop, favori entre 1,8 et 2,5 | −51 % |
| Simple placé du favori au trot attelé (favori à moins de 3,5, 738 courses) | **+9,7 %** |

**Méthode en 3 temps (1 035 courses d'attelé)**
- Les 2 342 chevaux écartés (sans signal, cote méritée, pas de course visée) se placent 10,0 % du temps pour 9,5 % attendus : le tri est exact mais ne change pas le choix des 3 plus bas cotés (1,46 contre 1,47 place par course).
- Un signal de plus ne change rien au-delà de la cote (coefficient 0,0115, p = 0,48). Chaque signal pris seul non plus.
- Choisir par signaux d'abord : 1,41 place par course (au moins 2 signaux), 1,34 (au moins 3), 1,22 (le plus de signaux). Couples placés −25 %, −27 %, −35 % contre −21 % pour les 3 premières cotes.

## Protocole TURFITUP (documents de Hari)
- **Version mécanique** (`protocole_score.py` : tendance, correspondance hippodrome/distance/allocation, dernier DQ, avis, face-à-face) : Vincennes 14/11, 5 courses, 9 places sur 15, couples +6,40 € ; Caen 14/11, 6 courses, 8 places sur 18, couples −10,10 €.
- **Lecture approfondie** (carrière complète, commentaires de fin de course, driver et entraîneur, scoring qualitatif, seuil de 60 % pour retenir un cheval) : Vincennes 14/11, 7 courses, 9 places sur 21 (les 3 premières cotes : 11 sur 21), gagnant +2,1 € sur 21 €, couples −25,6 € sur 39 €. Caen 14/11, 3 courses : 4 places sur 9, gagnant −2,3 €, couples −1,4 €.
- **Ce que le protocole apporte :** les alertes de fautes (R1C3 de Vincennes : 5 des 6 disqualifiés étaient sous 50 % ; R1C5 : les 2 disqualifiés étaient à 50 % ou moins ; en revanche les mêmes alertes n'ont pas empêché deux de mes trois choix d'être disqualifiés à R1C2), la lecture du changement de classe, des commentaires de fin de course utiles (excuses, gênes). **Ce qu'il n'apporte pas encore :** un avantage sur la cote.
- **Limites :** échantillon de 10 courses, analyses faites en connaissant l'arrivée, rapports de couples à fort écart-type.

## Prochaines validations
1. Test aveugle sur Vincennes du 16/11 (protocole appliqué avant le départ, horodaté), puis 50 courses minimum.
2. Comparer chaque lecture au favori à la cote (même nombre de chevaux, mêmes paris).
3. Ajouter à la lecture les pronostics Geny, les stats officielles driver/entraîneur et la position de départ en autostart (non vérifiés à ce stade).
4. Suivre trois pistes : baisse de cote depuis le matin, signal « classe », alerte de fautes.
