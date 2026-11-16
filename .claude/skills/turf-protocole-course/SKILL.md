---
name: turf-protocole-course
description: Lire une course de trot cheval par cheval selon le protocole TURFITUP de Hari (carrière complète, commentaires de fin de course, chrono, driver et entraîneur, face-à-face), noter chaque cheval, juger la lisibilité et donner les 3 chevaux qui sortent du lot avec leur cote et la projection pour 1 euro. À invoquer quand Hari dit « analyse la course », « lis Vincennes R1C3 », « refais Caen avec le protocole », « donne-moi les 3 chevaux », « lecture cheval par cheval », ou donne un hippodrome et un numéro de course.
---

# Lecture d'une course de trot cheval par cheval (protocole TURFITUP)

Référence : `turf/references/protocole-pronostic-trot.md` (déroulé) et `turf/references/methodologie-trot.md` (critères). Ne pas improviser ni raccourcir : appliquer le protocole tel que Hari l'a écrit. Workflow complet : `turf/WORKFLOWS.md` (W2). Aucune mise réelle, aucun conseil financier : tous les gains sont des projections ou des simulations.

## Avant de commencer
1. Identifier la course : hippodrome, réunion, numéro (ex. Vincennes R1C3) et la date. Vincennes = code letrot 7500, Caen = 1400 (autres codes dans la page `https://www.letrot.com/courses/<AAAA-MM-JJ>`).
2. Vérifier que la course n'est pas déjà courue si le test doit être aveugle ; sinon le dire à Hari (lecture « après coup »).
3. Lire les idées et tâches `new` du cockpit pour ce projet (règle du dépôt).

## Déroulé
1. **Collecter** (rythme lent, voir `turf-collecte-donnees`) : page course letrot, carrière complète de chaque partant, commentaires des 5 dernières courses de chacun.
2. **Dossiers** : `dossier_cheval.py` (8 dernières courses de chaque cheval avec place, cote, chrono, driver, ferrure, commentaire) et `stats_course.py` (conditions, Equidia, stats driver, entraîneur, tandem, cotes).
3. **Lecture manuelle**, cheval par cheval, dans cet ordre : musique et tendance ; correspondance exacte hippodrome, catégorie, distance (trois dimensions = preuve forte) ; chrono à distance équivalente ; driver et entraîneur séparément (volume minimum 30 courses) ; commentaires de fin de course (excuses, gênes, faiblesses) ; face-à-face direct ; rentrée ; flags avant course (première ferrure, changement d'entraîneur ou de driver, premier autostart).
4. **Alertes de fautes** (à rétrograder d'un cran, jamais exclure sur un seul signal) : DA à la dernière sortie, 2 DA ou plus sur 8 courses, jockey à plus de 30 % de disqualifications. En monté, 30 % des partants sont disqualifiés à Vincennes ; à Caen 43 % en attelé.
5. **Notation en %** : 85-95 dossier complet, 65-84 solide, 40-64 incertain, moins de 40 contradiction. Seuil de 60 % pour retenir un cheval. Trio seulement si 3 dossiers dépassent 60 % ; sinon 2 bases plus un 3e en couverture ; si aucun cheval n'atteint 60 %, conclure qu'il faut passer la course.
6. **Lisibilité** : facile (convergence vers 1-2 noms), modérée (un bon dossier mais 2-3 proches), difficile (plusieurs dossiers équivalents ou favori avec signal négatif), avec la raison factuelle.
7. **Sortie** (format structuré, voir `turf-bilan-reunion`) : configuration de la course, tableau d'analyse (N°, cheval et jockey, cote, lecture, score), les 3 chevaux retenus avec leur cote, projection pour 1 euro gagnant, couplé placé et 2 sur 4 (les rapports des couples sont des estimations : en moyenne 14 € pour un couple placé à 13 partants ou plus à Vincennes, 6 € pour un 2 sur 4), chance de réussite honnête (environ 1 sur 3 d'avoir au moins 2 de ses 3 chevaux dans les 3 à 13 partants ou plus).

## Garde-fous
- Dire ce qui n'est pas vérifié : Geny, stats officielles driver et entraîneur, position de départ en autostart.
- Le protocole n'a pas battu la cote sur les tests (9 places sur 21 contre 11 pour les 3 premières cotes à Vincennes). Le dire sans détour si Hari demande « ça marche ? ». Ne jamais présenter les scores comme des probabilités.
- Un cheval sans aucune carrière lisible (étranger, débutant) : le signaler et ne pas inventer.
- Ne jamais utiliser le résultat d'une course dans l'analyse de cette course.
- Après la course, comparer à l'arrivée avec les vrais rapports (skill `turf-bilan-reunion`) et enregistrer dans le cockpit (skill `cockpit`).
