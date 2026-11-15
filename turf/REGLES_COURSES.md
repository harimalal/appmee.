# Règles de sélection : trot attelé à Vincennes

Source : open-pmu-api + letrot.com (usage privé, non partagé), 40 courses de Vincennes avec le lot complet (21/11/2025 au 23/10/2026), 600 partants.
Méthodes : logit conditionnel, Plackett-Luce, forêt aléatoire, paris simulés hors échantillon.
Statut de chaque règle :
- **établi** : significatif et confirmé hors échantillon ;
- **piste** : signal non significatif, à confirmer ;
- **rejeté** : testé, sans effet ou perdant.

## À suivre

| # | Règle | Statut | Preuve |
|---|---|---|---|
| 1 | **La cote presse est la base.** Elle trouve environ 2 chevaux du top 4 sur 4, contre 0,6 au hasard. | établi | AUC 0,70–0,74. Aucun modèle ne la bat hors échantillon. |
| 2 | **Ne jouer que les courses lisibles.** Lisibilité = cote concentrée, favori net, journaux d'accord sur leurs 5 premiers. Écarter le tiers des courses les moins lisibles. | établi | Top 4 trouvés : 2,15 en course lisible contre 1,14 en course peu lisible (rho 0,44, p = 0,004). |
| 3 | **Le consensus de la presse complète la cote** : nombre de journaux qui citent le cheval, rang moyen dans les pronostics. | établi (pour classer) | C'est le seul bloc utile après la cote (−0,11 d'AUC quand on le retire). Il n'améliore pas significativement la prédiction finale. |
| 4 | **Au gagnant, privilégier le favori presse.** Il gagne 31 % des courses alors que sa cote lui en donne 20 % (favoris sous-cotés). | piste | Rendement +5 % au gagnant (fourchette −42 % à +56 %, 40 courses). |
| 5 | **Au placé, seul le favori en course lisible approche l'équilibre** (barème : −6 % au milieu, +8 % en haut). | piste | 13 paris. |
| 6 | **Chez les non-favoris, deux signaux faibles :** cheval annoncé déferré, et au moins 2 victoires sur les 5 dernières courses. Ils se placent environ 1,4 fois plus que ce que prévoit la cote. | piste | p = 0,23–0,25. Il faut 200 à 300 cas pour trancher. |

| 6b | **Non-favoris montés par un driver très performant à Vincennes** (quart supérieur en taux de top 3, calculé sur ses vraies montes) : ils se placent 1,3 fois plus que ce que prévoit la cote. | piste | 111 chevaux, p = 0,17. |
| 6c | **Non-favoris déjà dans les 3 premiers à Vincennes** (affinité réelle pour la piste) : ils se placent 1,4 fois plus que ce que prévoit la cote. | piste | 43 chevaux, p = 0,30. |

| 16 | **Petits lots (14 partants ou moins) : jouer le favori.** Il gagne 2 fois plus souvent que dans les grands lots, et plus que sa cote ne l'annonce. | piste forte | 100 courses : un gagnant à cote < 5 dans 64 % des petits lots, contre 31 % des grands (Fisher p = 0,002). 40 courses : le favori presse gagne 8 fois sur 16, pour 22 % attendus (p = 0,013). Rendement gagnant +45 %, placé +20 % au barème moyen (16 courses). |
| 17 | **Pour les jeux combinés, prévoir des outsiders.** Le top 4 compte en moyenne 0,8 cote < 5, 1 cote de 5 à 10, 1,15 cote de 10 à 20 et 1,07 cote de 20 ou plus. | établi (descriptif) | 80 % des courses ont au moins une cote ≥ 20 dans le top 4, et 76 % au moins deux cotes ≥ 10. Motif le plus fréquent : une cote de chaque tranche (13 %). |
| 18 | **Grands lots (15 partants ou plus) : élargir aux outsiders.** Le top 4 y contient 1,4 fois plus de cotes ≥ 10. | piste forte | Poisson p = 0,04, résultat stable sur les deux moitiés de la période (1,8 contre 2,5 cotes ≥ 10). Une partie de l'écart est mécanique : plus de partants, donc plus de grosses cotes. |
| 19 | **Courses de femelles et de jeunes chevaux (6 ans ou moins) : se méfier du favori.** | piste | Gagnant à cote < 5 : 13 % (femelles) et 21 % (jeunes), contre 47 à 51 % ailleurs. Cohérent avec l'analyse au niveau course (femelles : p = 0,003). |
| 23 | **Utiliser la cote PMU finale (letrot.com) plutôt que la cote presse.** Elle existe pour tous les partants. | piste forte | Top 4 trouvés : 1,85 contre 1,78 ; AUC 0,73 contre 0,70 (40 courses). Corrélation 0,88 entre les deux. |
| 24 | **Favori PMU dont l'entraîneur n'a pas donné d'avis favorable : le jouer.** Favori avec avis favorable : s'en méfier. | piste forte | Les chevaux à avis favorable (« 1 ») se placent 0,71 fois l'attendu (26 placés pour 36, p = 0,005 ; 0,06 après correction). Stable sur les deux moitiés. Favori sans avis favorable : 10 gagnants sur 19, gagnant +89 %. Avec avis favorable : 5 sur 21, −34 %. Le public surjoue les chevaux annoncés confiants. |
| 25 | **Crack Series (letrot) : utile pour repérer un outsider sous-coté, pas pour parier seul.** Non-favori (4e cote PMU ou au-delà) classé dans les 3 meilleurs Crack Series du lot. | piste | Il se place 1,55 fois l'attendu (21 pour 13,6, p = 0,04, stable sur les deux moitiés). Mais au placé, le barème ne compense pas (−17 % au milieu). |
| 26 | **Affiner les règles 16 et 20 par profil :** avec la cote PMU, le favori est jouable en petit lot (tous profils) et en grand lot mixte d'âges. À éviter en grand lot de jeunes ou de femelles. | piste | Favori PMU : petit lot mixte +52 % gagnant, +57 % placé ; grand lot mixte +44 % / +14 % (16 courses) ; grand lot jeunes ou femelles : 0 gagnant et 0 placé sur 8. |

## À éviter

| # | Règle | Statut | Preuve |
|---|---|---|---|
| 7 | **Ne pas jouer les courses peu lisibles** : la cote y fait à peine mieux que le hasard. | établi | Voir la règle 2. Favori placé : −22 % en course peu lisible. |
| 8 | **Ne pas jouer les gros outsiders** (cote de plus de 40). | établi | 0 victoire sur 100 chevaux, rendement placé de −79 %. |
| 9 | **Ne pas chercher la « valeur » chez les outsiders au placé**, même avec des signaux : les rapports ne compensent pas. | établi | Non-favoris avec signaux : −25 % à −52 %. |
| 10 | **Ne pas surpondérer la forme, le record, l'âge, le sexe, les gains, l'entraîneur ou le numéro de départ** : déjà intégrés dans la cote. | établi | Aucun apport au-delà de la cote. Ils dégradent le modèle complet. |
| 11 | **Ne pas se fier aux modèles « boîte noire »** (forêt aléatoire pour chercher de la valeur). | établi | Forêt aléatoire au gagnant : −33 % à −39 %. |
| 12 | **« Engagement favorable » dans le commentaire** : pas de bonus. | rejeté (petit échantillon) | 2 placés pour 3 attendus. |
| 13 | **Ne pas pénaliser un cheval fautif plus que la cote ne le fait déjà** : les fautes (musique, commentaire) sont déjà intégrées dans la cote. | établi | Disqualification récente : 0,94 fois l'attendu (p = 0,64). Fautif selon le texte : 1,14 fois (p = 0,68). |
| 14 | **Le record kilométrique n'est pas un critère de vitesse utile** au-delà de la cote. | établi | Meilleurs records du lot : 1,02 fois l'attendu (p = 1,0). |
| 20 | **Ne pas jouer le favori dans les grands lots** (15 partants ou plus). | piste forte | Favori presse : gagne 21 %, rendement gagnant −22 %, placé −25 % (24 courses). |
| 21 | **Ne pas mélanger les cotes de plusieurs sources** (Paris-Turf, Tiercé Magazine, consensus des journaux) : Paris-Turf seul fait aussi bien ou mieux. Tiercé Magazine seul est moins bon. | établi | Mélanges à poids fixes ou ajustés : pas d'amélioration. Tiercé Magazine seul : −0,20 en log-vraisemblance par course (p = 0,01). Sources corrélées à 0,99 (Paris-Turf / Tiercé Magazine). Des poids qui varient selon la configuration donnent +0,18 (p = 0,09) : piste faible. |
| 22 | **La distance et l'allocation ne changent pas la composition du top 4.** | établi | Chi² p = 0,98 (distance) et 0,55 (allocation). |
| 27 | **Ne pas classer les chevaux au Crack Series à la place de la cote.** Il mesure la classe, déjà dans la cote. | établi | Seul : AUC 0,63 contre 0,73 pour la cote (p = 0,025). Ajouté à la cote : +0,07, non significatif (p = 0,31). Effet au-delà de la cote : p = 0,42. |
| 28 | **Ferrure (déferré des 4 pieds, changement de ferrure), nouveau driver, rentrée, course rapprochée, changement d'entraîneur : pas de bonus.** | établi (40 courses) | Aucun écart à la cote (p de 0,17 à 0,91). La piste « déferré » de la règle 6 n'est pas confirmée avec la ferrure officielle. |
| 15 | **Ne pas surpondérer la vitesse de fin des courses précédentes** (derniers 500 m et 1 000 m comparés au peloton) : la cote l'intègre déjà. | établi (palier 1) | Mesurée sur la dernière course chronométrée de 414 partants (letrot.com, Vincennes, Enghien et 2 autres pistes). Corrélée à la cote (0,36). Meilleur finisseur du lot : 12 placés pour 11,9 attendus. 3 meilleurs finisseurs : 33 pour 35,5. Aucun effet après correction (p ≥ 0,22). Piste faible à surveiller : non-favori à cote ≤ 20 parmi les 3 meilleurs finisseurs (5 gagnants sur 34, placé −1 % au milieu du barème). |

## Combinaisons de cotes par profil de course
Source : 98 courses d'attelé, cote PMU finale des 4 premiers. Fourchette = moitié centrale des cas (25e à 75e centile). Plafond 90 % = la cote est en dessous 9 fois sur 10.

| Profil | Jouable ? | Gagnant | 2e | 3e | 4e | Couverture trio (3 premiers tous dans le plafond) |
|---|---|---|---|---|---|---|
| **A. Petit lot (14 ou moins), mixte, chevaux de plus de 6 ans** (23 courses) | **Oui : profil n°1** | cote < 5 dans 70 % des courses ; fourchette 2,2 à 6,3 ; toujours ≤ 20 | 5,2 à 9,9 | 7 à 20 | 8 à 26 | cotes ≤ 20 : 61 % ; ≤ 30 : 70 % ; ≤ 50 : 96 % |
| **B. Petit lot, jeunes ou femelles** (10 courses) | Oui, avec prudence (trop peu de courses) | cote < 5 dans 50 % ; fourchette 4 à 14 ; toujours ≤ 20 | 4,4 à 9,2 | 6 à 18 | 9 à 19 | ≤ 20 : 60 % ; ≤ 30 : 80 % |
| **C. Grand lot (15 ou plus), mixte, chevaux de plus de 6 ans** (41 courses) | En jeux combinés seulement, pas le favori en simple | cote < 5 dans 41 % ; fourchette 3,7 à 11 | 6,7 à 18 | 6 à 27 | 10 à 27 | ≤ 20 : 34 % ; ≤ 30 : 59 % ; ≤ 50 : 80 % |
| **D. Grand lot, jeunes ou femelles** (24 courses) | **Non** | cote < 5 dans 12 % seulement ; fourchette 8 à 16 | 9 à 23 | 9 à 38 | 12 à 28 | ≤ 30 : 58 % ; au moins un cheval > 40 dans le top 4 dans 42 % des courses |

**Combinaisons types :**
- **A :** favori < 5 en base, puis cotes de 5 à 20 (environ 7 chevaux). Ajouter 1 ou 2 chevaux de 20 à 40 pour le quarté : il y en a un dans le top 4 une fois sur deux.
- **B :** même schéma que A, en élargissant aux cotes de 20 à 30.
- **C :** pas de base favori. Couvrir les cotes de 4 à 30, et prévoir 1 cheval de 20 à 40 (présent dans 61 % des courses).
- **D :** à éviter. Le gagnant est le plus souvent entre 8 et 16, sans favori fiable, et le top 4 inclut souvent un cheval à plus de 40.

## Constats sûrs à conserver
Ce qui est confirmé et qu'on ne remet pas en cause sans 300 courses de plus.

| # | Constat | Statut | Preuve |
|---|---|---|---|
| 29 | **Les chevaux qui ont déjà couru à Vincennes se placent exactement comme la cote le prévoit.** Aucun bonus et aucun malus pour l'expérience de la piste. | établi (82 courses, historique complet) | 1 à 2 courses : 0,99 fois l'attendu ; 3 à 6 : 0,94 ; 7 et plus : 0,97. Les chevaux qui n'ont jamais couru à Vincennes ne sont pas rares dans les 3 premiers : 14 % des 3 premiers pour 11 % attendus ; 28 % se placent contre 22 % attendus (p = 0,12). Ne pas écarter un cheval pour cette seule raison. |
| 30 | **Cocher toutes les cases ne bat pas la cote** (déjà couru à Vincennes, bon taux de places, niveau de course, forme, driver, temps au km, tendance). Le nombre de cases cochées suit la cote. | établi (82 courses) | 6 cases ou plus : 25 % de placés pour 29 % attendus (p = 0,31). Chaque case de plus : 0,93 fois (p = 0,14). |
| 31 | **Un modèle à 21 signaux (classe, forme, hippodrome, jockey, marché, physique) ne bat pas la cote** pour trouver les 3 premiers. Ses probabilités sont fiables. | établi (validation croisée, 82 courses) | 1,21 place sur 3 choisis contre 1,26 pour la cote seule. Aucun groupe de signaux ne l'améliore. Probabilités annoncées 45-60 % : 48 % réels. |
| 32 | **Graphique de type Visuturf (version approchée) : ne bat pas la cote.** Seule piste : la zone jaune (bon jockey, cheval moyen) en course moyennement lisible. | rejeté en l'état ; piste sur la zone jaune | Les 3 meilleurs du graphique : 0,91 sur 3 contre 1,24 pour la cote (p < 0,01). Zone jaune : 8 sur 21 dans les 3 pour 5 attendus. |
| 33 | **Mouvements de cote avant le départ : à valider en direct.** Parmi les arrivés, les chevaux dont la cote raccourcit finissent plus souvent dans les 3 (62 % contre 34 % pour ceux dont la cote dérive). | piste | Échantillon biaisé (arrivés seulement), p = 0,18. Relevés de toutes les cotes en direct à Vincennes depuis le 14/11/2026. |

## Tendances de Vincennes (observées, pas des règles)
Une tendance est un profil d'arrivée qui se retrouve dans deux échantillons indépendants (40 courses d'origine, puis 39 à 42 courses de novembre 2026). Elle décrit comment les courses se déroulent ; elle ne sert pas seule à décider d'un pari. Les écarts avec la cote ne sont pas traités comme des anomalies : ils sont suivis et pourront devenir des règles quand le nombre de courses le permettra.

| # | Tendance | Origine (40) | Novembre (39) |
|---|---|---|---|
| T1 | **Le top 4 contient en moyenne 2 à 3 chevaux des 5 premières cotes** (2 ou 3 dans 3 courses sur 4). | 2,33 ; 75 % | 2,46 ; 74 % |
| T2 | **Le reste du top 4 vient surtout des cotes 6 à 10** (environ 1,2 cheval), rarement des cotes 11 et plus. | 6-10 : 1,23 ; 11+ : 0,45 | 6-10 : 1,23 ; 11+ : 0,31 |
| T3 | **Les 5 premières cotes placent un peu moins de chevaux que la cote ne le prévoit**, et les cotes 6 à 10 un peu plus. Le gagnant reste dans les 5 premières cotes 4 fois sur 5. | 2,33 contre 2,62 attendu ; gagnant dans le top 5 : 82 % | 2,46 contre 2,87 attendu ; gagnant dans le top 5 : 82 % |
| T4 | **Les 3 premiers sont rarement tous dans les 5 premières cotes** : un outsider s'invite presque toujours. | 20 % (33 % attendu) | 23 % (38 % attendu) |
| T5 | **Le favori est dans le top 4 plus souvent en petit lot qu'en grand lot.** | 77 % contre 48 % | 83 % contre 56 % |
| T6 | **En novembre, la 2e cote s'est mal placée** (11 places pour 23 attendues), le 5e se place plus que prévu (14 pour 10,5). Dans l'échantillon d'origine, la 2e cote est aussi en dessous (0,77 fois l'attendu). | 2e cote : 0,77 fois l'attendu | 2e cote : 0,48 fois l'attendu |
| T7 | **Les trios et quartés fermés sur les 10 premières cotes touchent moins souvent que ne le prévoit la cote** (test des tendances : 77 courses, sans filtre). Trio 3 des 5 premières cotes : 0,61 fois l'attendu (p = 0,02). Trio « 2 des cotes 1-5 + 1 des cotes 6-10 » : 0,91 (p = 0,61). Quarté « 3 des cotes 1-5 + 1 des cotes 6-10 » : 0,61 (p = 0,01). | trio 3 des cotes 1-5 : 0,73 | 0,52 |
| T8 | **Le filtre de course fait la différence, pas les signaux du cheval.** Courses gardées (lisibles, hors profil D) : la cote y trouve 2,14 chevaux du top 4 contre 1,57 dans les écartées. Avec 3 chevaux choisis par la cote, au moins un couple placé touche dans 48 % des courses gardées contre 25 % des écartées (origine 47 % / 28 %, novembre 48 % / 22 %). Un modèle avec classe, forme, appétence Vincennes, expérience et avis n'apporte rien hors échantillon (gain de vraisemblance 0,000, p = 0,65). | 47 % contre 28 % | 48 % contre 22 % |

Mise à jour sur T3 et T7 : sur 82 courses, la cote ressortait un peu trop concentrée sur les premiers choix pour prévoir les places. Sur 315 courses (Vincennes et Enghien), la cote est bien calibrée pour le top 3 (pente 1,07 à 1,10, soit environ 1). T3 et T7 relèvent donc probablement du petit échantillon : à ne pas considérer comme établies.

T9 : **la classe (Crack Series) n'apporte rien au-delà de la cote pour finir dans les 3** (315 courses, 4 190 partants : coefficient +0,06, IC95 de −0,04 à +0,15, p = 0,23). Non-favoris dans les 3 meilleures classes du lot : 103 placés pour 107 attendus. Un modèle de probabilité à 14 signaux (forme, appétence, avis, âge, ferrure, record, etc.) ne repère pas mieux les 3 premiers que la cote seule (82 courses, validation croisée).

Lecture : un top 4 type de Vincennes = 2 chevaux parmi les 5 premières cotes + 1 ou 2 chevaux de cote 6 à 10 (+ parfois un cheval de cote 11 et plus). T1, T2 et T5 sont les plus stables.

## Limites
- 40 courses, un seul hippodrome, une seule discipline (attelé).
- Les rapports placés viennent du barème de Hari, pas des vrais rapports PMU.
- On suppose que la cote PMU est un rapport pour 1 € mise incluse, et que la dernière cote publiée est la cote finale.
- Règle de mise à jour : quand une piste est confirmée sur au moins 300 courses, elle passe en « établi ».

## Journée du 14/11/2026 (lecture en direct, 12 courses, hors échantillon)
Détail : data/fiches/BILAN_2026-11-14.md. Aucune règle n'est modifiée par cette journée.
- Les 3 couples prévus à T-3 min (couplé placé + 2 sur 4) : -16,70 euros sur 11 courses réglées ; Vincennes R1C9 gagnant sur les 3 couples (rapports à chiffrer).
- R24 (avis favorable du favori) : contredite deux fois (Vincennes R1C7 et R1C5). A surveiller.
- R33 (mouvements de cote) : 4 cas favorables, 2 contraires. Reste une piste.
- T10 (nouvelle tendance) : les disqualifications pour allure irrégulière touchent presque toutes les courses (jusqu'à 6 partants sur 15), ce qui explique une grande part des surprises.
