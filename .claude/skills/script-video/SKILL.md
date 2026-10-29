---
name: script-video
description: Écrit le script (voix off) d'une vidéo YouTube éducative ou de démonstration qui retient — accroche par la preuve, valeur avant la pub, voix qui explique le pourquoi au lieu de lire l'écran — puis le teste avant publication par une simulation de 100 spectateurs (5 profils d'agents + un analyste YouTube) et le corrige d'après la courbe de rétention simulée. Utilise ce skill dès que l'utilisateur veut « écrire le script », « la voix off », « le texte de la vidéo », « améliorer la rétention », « tester la vidéo avant de la publier », « simuler l'audience », même sans nommer le format. Pour poser la voix sur des slides, voir voix-off-slides.
---

# Script vidéo qui retient

Deux temps : **écrire** un script selon les règles ci-dessous, puis le **mettre à l'épreuve** devant 100 spectateurs simulés avant de produire quoi que ce soit de coûteux. On corrige le texte, pas le montage.

Né de la vidéo « lancement Product Hunt de Dropit » (octobre 2026) : la simulation a montré 70 % de spectateurs encore là à 30 s, 18 % à la fin, et trois fuites au début que le texte pouvait corriger. Détails : `references/exemple-dropit.md`.

## 1. Avant d'écrire
- Le public visé (un seul profil principal), ce qu'il a tapé ou vu avant de cliquer, et **la promesse du titre** : le script doit la tenir dans la première minute.
- La matière réelle : les slides (`slides.json` du skill voix-off-slides), les chiffres vrais, les captures. Ne jamais inventer un chiffre, un résultat ou une citation ; ce qui est un raisonnement de ma part, le dire à l'utilisateur.
- Le format de fichier : un bloc par slide, **uniquement ce qui sera dit** (aucune consigne de jeu : la synthèse vocale la lirait).
```
##02 titre
…texte dit…
```

## 2. Les règles d'écriture
**Les 20 premières secondes**
- Ouvrir sur **le résultat visible** (« Ça, c'est tout mon lancement : trente livrables prêts à copier-coller »), pas sur un formulaire vide ni une intro.
- Poser l'enjeu en une phrase, puis une **boucle ouverte** précise (« je te montre la demande exacte dans une minute ») — et la refermer vers 1:00–1:30.
- Dire au spectateur ce qu'il pourra en faire (« tu pourras la copier pour ton produit »).

**Le corps**
- La voix **appuie et développe** l'écran : l'enjeu, le pourquoi du comment, le piège à éviter. Elle ne lit pas ce qui est écrit et ne suit pas l'ordre des animations.
- Une idée par slide, 25 à 45 mots (≈ 8 à 15 s à 200 mots/min).
- Le contexte (« X, c'est quoi ») en **une seule slide** et seulement si le public cible l'ignore ; le reste du public décroche.
- Un **récit** plutôt qu'une liste : problème → tentative → pivot → méthode → preuve. Relancer l'attention toutes les 30 à 45 s (une question, une révélation, un avant/après, un chiffre).
- La valeur promise arrive avant 40 % de la durée.

**Les appels à l'action**
- Ni « abonne-toi » ni auto-promo avant que la valeur soit livrée. La pub de son propre produit : 15 s, après la méthode, présentée comme telle.
- Fin : une action unique et concrète (« dis-moi ce que tu lances ; le prompt est en description »), pas un résumé.

**La crédibilité**
- Chaque promesse chiffrée a sa preuve à l'écran. « 0 € » s'écrit « 0 € de budget » si un abonnement payant a servi.
- Montrer l'outil au travail (écran réel) quand le sujet est un outil.
- Dire ce qui n'est pas encore connu (le résultat du lancement) et promettre le suivi.

**La voix**
- Phrases courtes, ponctuation qui donne le rythme ; nombres écrits comme ils se disent quand c'est ambigu (« quatre-vingts vingt » plutôt que « 80/20 »).
- Une voix de synthèse est repérée vite : compenser par la preuve à l'écran dès la première seconde ; proposer la voix de l'auteur quand c'est possible.

## 3. Le banc d'essai : 100 spectateurs simulés
Protocole v2 (consigne commune des spectateurs : `references/protocole-spectateur.md` ; consigne de l'analyste et lecture : `references/simulation.md`).
1. **Dossier** : `python3 -I <skill>/scripts/dossier.py script.txt slides.json minutage.json fiche.md simu/dossier.md` — texte minuté slide par slide, écran, fiche technique (durée, voix, débit, musique, sous-titres, **titre et miniature visés**). Le dossier ne dit jamais que c'est une version corrigée ni ce qu'une simulation précédente a trouvé (à l'aveugle).
2. **Panel tiré au sort** : `python3 -I <skill>/scripts/panel.py simu/personas.json <graine>` — 5 profils × 2 panels × 10, attributs stratifiés (métier, âge, source, appareil, contexte, expertise, patience). Nouvelle graine = 100 nouveaux spectateurs ; même graine = même panel rejoué sur une autre version (comparaison plus juste).
3. **11 agents en parallèle** (outil Agent, en arrière-plan) : un par panel (`« lis protocole.md puis dossier.md, suis le protocole pour la clé "A1" de personas.json, écris panel-A1.json »`), plus 1 analyste YouTube qui ne lit que le dossier et note 12 critères fixes. Deux agents par profil : leur écart mesure l'incertitude. Chaque spectateur passe l'**impression** (aurait-il cliqué ?) puis regarde par **points de contrôle** (0:15, 0:30, 1:00, chaque slide) en citant la phrase qui le fait partir.
4. **Agrégat** : `python3 -I <skill>/scripts/agreger.py simu/ <durée> [--avant ancien/ <durée>]` — rétention en temps absolu et en % de la durée, avec intervalle à 90 % (tirage sur les panels), durée moyenne, clic, engagement, notes (dont crédibilité), profils, départs par 30 s, et comparaison à la simulation précédente.
5. **Lecture** : les causes de départ citées par plusieurs panels au même moment sont à corriger en priorité ; ce qui retient ceux qui restent est à avancer. Un écart n'est réel que si les intervalles ne se chevauchent pas ; signaler tout changement de protocole entre deux simulations.
6. **Corriger le script**, relancer (nouvelle graine pour un regard neuf, même graine pour mesurer l'effet d'une correction) et comparer.

À dire à l'utilisateur, toujours : c'est une simulation par IA, pas des données YouTube ; elle sert à trouver les faiblesses avant de publier, pas à prédire des vues. Après publication, comparer avec la vraie courbe de YouTube Studio et noter les écarts dans `references/exemple-*.md`.

## 4. Livrer
- Le script (fichier `##NN id`), le nombre de mots et la durée estimée.
- La courbe simulée avant/après correction et les 3 changements qui ont le plus d'effet.
- Titres (≤ 60 caractères) et 2 idées de miniature cohérentes avec les 20 premières secondes.
- Puis passer au skill **voix-off-slides** pour la voix et le calage.
