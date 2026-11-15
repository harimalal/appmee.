# TURFITUP — Méthodologie (référentiel de critères)

Version du 15/11/2026. Ce document est le référentiel : quels critères comptent, lesquels écarter, et comment lire hippodrome, corde, distance et mise. Le déroulé d'analyse course par course est dans `protocole-pronostic-trot.md`.

Principe directeur : la cote est un signal, pas une donnée d'entrée. On analyse d'abord forme, classe, driver et correspondance de conditions, puis on compare à la cote. L'écart révèle les chevaux sous-cotés ou sur-cotés.

---

## 1. Hippodrome et tracé

- **Sens de rotation** : certains chevaux ont une préférence nette (main droite ou gauche). Vérifier la cohérence dans l'historique, pas seulement le nom de l'hippodrome.
- **Taille de piste** : petite piste = virages serrés, placement à la corde crucial, remontée difficile. Grande piste = course ouverte, l'arrière-garde peut remonter.
- **Dénivelé** : un faux-plat montant en fin de parcours (Vincennes, Saint-Cloud, Lyon-Parilly) avantage les puissants et endurants, pénalise les purs vitesse.
- **Surface** : cendrée ou sable (Vincennes, Enghien, Cabourg), impact modéré.
- **Spécialistes de piste** : un cheval peut briller sur un tracé et être nul ailleurs. Toujours vérifier le bilan sur le tracé du jour, jamais le bilan général.
- **Province** : moins de couverture, cotes parfois plus généreuses sur les spécialistes locaux.

### Classement par rapport moyen (Simple Gagnant)

Source : Boturfers, 128 hippodromes (France et étranger accessible au PMU), vérifié le 20/07/2026.

Lecture : un rapport moyen élevé signifie que les favoris dominent moins, donc marché moins efficient et course plus ouverte. Ce n'est ni une note de qualité ni une garantie de rentabilité.

| Hippodrome | Rang | Rapport moyen | Courses/an |
|---|---|---|---|
| Lisieux | 5 | 12,2 € | 48 |
| Cavaillon | 6 | 12,1 € | 16 |
| Argentan | 7 | 12,0 € | 85 |
| Vire | 8 | 11,8 € | 32 |
| Amiens | 9 | 11,2 € | 100 |
| Cabourg | 11 | 10,1 € | 208 |
| Deauville | 13 | 10,1 € | 433 |
| Longchamp | 16 | 9,6 € | 242 |
| Chantilly | 23 | 9,4 € | 422 |
| Auteuil | 29 | 9,0 € | 284 |
| Vincennes | 32 | 8,9 € | 1225 |
| Saint-Cloud | 35 | 8,8 € | 252 |
| Enghien-Soisy | 39 | 8,5 € | 337 |
| Saint-Galmier | 49 | 8,2 € | 71 |

Constats : Vincennes est 1er en volume mais seulement 32e en rapport. Les sommets sont des trots normands ou provinciaux (Lisieux, Argentan, Vire, Amiens). Maisons-Laffitte est absent de la source. Classement complet dans `classement-hippodromes.md`.

Trois profils à annoncer à chaque course : facile et bien payé, facile mais peu généreux, difficile mais généreux.

---

## 2. Corde et mode de départ

- Impact de la corde : pas de règle universelle, à vérifier hippodrome par hippodrome. Corde intérieure avantagée sur virage serré et distance courte, extérieure avantagée si meilleur débouché en ligne droite.
- Quand un tableau "taux de réussite par position" existe (Geny, LeTrot), l'utiliser systématiquement.
- **Autostart** : départ lancé, favorise les rapides bien placés, distance effective égale à la distance nominale.
- **Volte avec recul** : départ arrêté, recul par tranche de 25 m. Les reculés courent physiquement plus loin que la distance affichée.
- Le mode de départ est à vérifier sur la fiche course, il est parfois absent.

---

## 3. Critères fiables et critères à écarter

### Fiables (toujours contextualisés)

| Critère | Pourquoi |
|---|---|
| Strike rate sur 5 à 10 dernières sorties | Plus révélateur que la carrière globale |
| Performance par distance | Un cheval peut être spécialiste d'un format |
| Performance par terrain | Un terrain différent peut inverser une hiérarchie |
| Musique croisée avec le niveau de course | Un 1 en réclamer n'est pas un 1 en Listed |
| Stats driver et entraîneur filtrées | Le taux brut mélange trop de contextes |
| Tandem driver-entraîneur | Fort quand le duo dépasse chaque moyenne individuelle |
| Taux de réussite des favoris par type d'épreuve | Mesure la lisibilité de la course |
| Nombre de non-partants | Redistribue la hiérarchie et les rapports |
| RK à distance équivalente | Seul outil valable pour comparer l'aptitude à la distance |
| Changement de distance décidé par l'entraîneur | Allongement après forte fin = positif, va-et-vient répétés = négatif |

### À écarter (biais et bruit)

| Critère | Pourquoi |
|---|---|
| Stats de carrière globales sans filtre | Mélange années, terrains, distances, niveaux |
| Systèmes mono-variable (numéro, jour) | Corrélation fantôme sans causalité |
| Séries chaudes ou froides | Chaque course est indépendante |
| Robe, couleur, nom | Bruit statistique |

### Règle de volume

En dessous de 20-30 courses, une statistique n'est pas fiable, même à 100 %. Plus le filtre est fin (un driver sur un seul hippodrome), plus il faut de volume.

---

## 4. Distance et aptitude

- RK (réduction kilométrique) : temps moyen au km, comparable uniquement à distance équivalente.
- 2100 m : vitesse pure. 2700-3000 m : équilibre vitesse et tenue. 3500 m et plus : endurance et gestion de l'effort (risque de faute).
- En attelé, le driver gère le rythme : avantage au couple expérimenté sur longue distance.
- Deux essais minimum sur une distance avant de conclure à une inaptitude.

---

## 5. Structuration de la mise

Toujours en unités, jamais en euros réels. Aucun conseil financier.

### Quinté+ (bases, associés, Flexi)
- Coût combinatoire C(N,5) : passer de 7 à 9 chevaux multiplie le coût par 6.
- Une base qui saute fait tomber toute la combinaison : mieux vaut une base de moins qu'une de trop.
- Équilibre courant : 2-3 bases plus des associés.
- Le Flexi ajuste le budget, jamais la qualité de la sélection.
- En trot attelé, les courses sont plus ouvertes (disqualifications, incidents) : structure un peu plus large qu'en galop.

### Jeu simple multiple (méthode des 42 unités)
- Répartir sur 2 à 4 chevaux en simple gagnant, cotes idéalement entre 3/1 et 8/1, barème dégressif (plus la cote est basse, plus la mise est élevée).
- Plafond de 42 unités, au-delà passer la course.
- Si aucun cheval choisi ne gagne, la perte est totale : ce n'est pas un arbitrage sans risque.
- Course idéale : 9 à 13 partants (moins de 8 trop restreint, plus de 14 trop de variables).

### Structure de pari avec une base
1 cheval de base (le plus fiable analytiquement) combiné à 3 autres moins certains, mise décroissante. Les cotes des paris combinés ne se déduisent pas des cotes simples (pari mutuel).

---

## 6. Points ouverts

- Classement des hippodromes par rendement réel (le classement actuel est par rapport moyen).
- Confirmation du mode de départ sur les fiches courses futures.
