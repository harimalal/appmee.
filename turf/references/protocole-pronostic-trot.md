# TURFITUP — Protocole de pronostic (déroulé course par course)

Version du 15/11/2026. Ce document est le mode opératoire : les étapes dans l'ordre, de la réception des fichiers à l'analyse après résultat. Les critères et références (hippodromes, corde, mise) sont dans `methodologie-trot.md`.

Principe directeur : la cote est un signal, pas une donnée d'entrée. Construire l'analyse d'abord, comparer à la cote ensuite.

---

## Étape 0 — Identifier ce qui a été reçu

- Fichier "Partants et Pronostics" (.mht) : tableau des partants (cote, musique, driver, entraîneur), pronostic éditorial Geny, parfois performances croisées.
- Fichiers .mht individuels par cheval : historique de carrière complet (catégorie, hippodrome, distance, résultat).
- Images de stats drivers et entraîneurs : courses, victoires, écart, réussite à la distance du jour.
- Fichiers Cosmetica Mania (_MP0*, _SYSTEME_VISUELS*) : signaler et ignorer.
- Aucun fichier partants : chercher cotes et musique sur le web (Turfomania, Equidia, Canalturf), jamais les inventer. Dire explicitement toute donnée manquante.

## Étape 1 — Exclure les données du jour (obligatoire si la course est passée)

Retirer des fichiers individuels toute entrée datée du jour de la course, sinon le résultat fuite dans l'historique. Extraction Python sur les .mht : une ligne par course passée (date, discipline, hippodrome, corde, terrain, catégorie, allocation, distance, groupe, rang). Si les mêmes fichiers sont renvoyés une seconde fois, le signaler au lieu de refaire l'analyse.

## Étape 2 — Conditions de la course du jour

Relever : départ, numéro de course, allocation, distance, nombre de partants, corde, autostart ou volté, conditions d'âge et de gains. Elles définissent les filtres de comparaison de l'étape 3. Rappeler le rang et le profil de l'hippodrome (voir classement).

## Étape 3 — Lecture croisée, cheval par cheval

1. **Musique récente** : lue de gauche (récent) à droite (ancien), tendance et non dernier caractère. (25) ou (24) marque une fin de saison.
2. **Correspondance exacte** hippodrome, catégorie, distance. Trois dimensions = preuve forte, une seule = preuve partielle (à dire).
3. **Chrono comparé** à même distance, via la liste "plus rapides sur le parcours", croisée avec les non-partants (la vitesse brute se reporte sur la vague suivante).
4. **Driver et entraîneur séparément** : courses, victoires, écart, réussite. Écart bas et bon % = signal fort. Ne jamais fusionner cheval, driver et entraîneur.
5. **Commentaires de fin de course** (Equidia, Geny, Canalturf) : "a bien terminé", "a faibli", "gêné au départ".
6. **Face-à-face direct** entre chevaux du jour : preuve la plus forte, plus fiable qu'une comparaison indirecte.
7. **Carrière étendue** pour les chevaux à longue carrière : chercher toutes les apparitions sur l'hippodrome exact du jour, pas seulement les 5 dernières lignes.
8. **Rentrée** : vérifier le flag en Zone Infos (proxy de la saisonnalité).

## Étape 3bis — Checklist avant rédaction

- [ ] Musique récente lue (tendance)
- [ ] Historique étendu (10-15 courses) pour les carrières longues
- [ ] Correspondance classe, distance, hippodrome cherchée
- [ ] Driver et entraîneur séparés (écart et réussite)
- [ ] Liste "plus rapides sur le parcours" extraite si présente
- [ ] Croisement avec les non-partants
- [ ] Face-à-face direct cherché
- [ ] Flag Rentrée vérifié
- [ ] Commentaires de fin de course cherchés

Toute case non vérifiée est signalée dans la réponse ("je n'ai pas vérifié X").

## Étape 4 — Signaux

**À rétrograder, jamais à exclure sur un seul signal**
- DQ à la dernière sortie : descendre d'un cran. Atténuant si la DQ date d'une classe plus dure, aggravant si même niveau ou plus facile.
- Changement de discipline (attelé et monté) : la perf dans l'autre discipline ne prouve rien.
- Écart driver ou entraîneur supérieur à 20-25 : signal négatif indépendant, jamais éliminatoire seul. Toujours croiser avec la correspondance classe, distance, hippodrome (cas Jazz In Montreux : écart driver 50, gagnant).

**À chercher activement**
- Écart bas (0-3) chez driver et entraîneur à la fois.
- Victoires ou places répétées aux conditions exactes du jour.
- Progression sur 3 courses.
- Flags Zone Infos : première ferrure ou déferrure, changement d'entraîneur ou de driver.
- Sous-cotation ou sur-cotation : dossier solide avec cote nettement plus large qu'un favori à signaler explicitement.

## Étape 5 — Difficulté de lecture

Niveau explicite avec raison factuelle :
- **Facile** : forte convergence (éditorial, musique, driver, classe) vers 1-2 noms, aucun signal contradictoire majeur.
- **Modérée** : un bon favori se dégage mais 2-3 dossiers tiennent à cote proche, ou la correspondance de classe manque.
- **Difficile** : favori avec signal négatif propre, ou plusieurs dossiers équivalents sans hiérarchie, ou éditorial qui parle d'une course ouverte.

## Étape 6 — Synthèse et notation

Ordre obligatoire : chevaux de base retenus par priorité, puis non retenus avec la raison en une ligne. Jamais dans un seul tableau plat.

Deux profils de base : dossier complet (toutes les cases cochées, sans contradiction) ou dossier à signaux faibles cumulés (surprise potentielle, cote souvent plus large).

**Grille en % (jugement qualitatif, jamais présenté comme probabilité)**

| Score | Signification |
|---|---|
| 85-95 % | Dossier complet, aucune contradiction |
| 65-84 % | Solide, une réserve mineure déjà rétrogradée |
| 40-64 % | Incertitudes réelles ou données manquantes : couverture large, pas en base |
| Moins de 40 % | Contradiction significative non expliquée |

Règles de qualité :
- Seuil de 60 % pour retenir un cheval en base. En dessous : pas de médaille, il figure dans les non-retenus avec son score.
- Ne jamais forcer le nombre de bases : il reflète le nombre de dossiers au-dessus du seuil.
- Aucun cheval au-dessus de 60 % : conclure qu'il faut passer la course, c'est un résultat en soi.
- Trio seulement si 3 dossiers dépassent 60 % : difficile = favori (cote < 5) + moyen (< 10) + outsider (15-25) ; facile = 2 favoris + 1 moyen ou 1 outsider.

## Étape 6bis — Structure de pari (si demandée)

1 base plus 3 chevaux moins certains, mise décroissante, en unités. Pas de montant en euros, rappeler l'absence de conseil financier, préciser que les cotes combinées ne se calculent pas à partir des cotes simples.

## Étape 7 — Après le résultat

Comparer honnêtement le pronostic au résultat. Ne jamais justifier un raté par une explication absente des données d'origine : dire "aucune donnée que j'avais n'annonçait ce résultat" quand c'est le cas. Chaque écart sert à identifier un motif à ajouter au protocole.

## Étape 8 — Pistes professionnelles (quand la donnée existe)

- Position de départ et taux de réussite par corde sur l'hippodrome.
- Association driver-cheval spécifique (X courses ensemble, Y %).
- Convergence entre sources indépendantes (Geny, Turfomania, Equidia, Canalturf, PMU) : signal de robustesse, utile pour départager.
- Pedigree pour un cheval sans historique exploitable.

Volontairement exclus du systématique : rythme probable de course (inconnu avant le départ), poids porté (sauf trot monté) et type de terrain (sauf variation réelle).

---

## Règle d'évolution

Toute nouvelle règle générale formulée en session ("à partir de maintenant, fais toujours X") est ajoutée à ce protocole ou au référentiel, pas gardée seulement en conversation.
