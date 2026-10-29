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
Protocole complet et consignes des agents : `references/simulation.md`.
1. **Dossier** : `python3 -I <skill>/scripts/dossier.py script.txt slides.json minutage.json fiche.md dossier.md` — texte minuté slide par slide, écran, fiche technique (durée, voix, débit, musique, sous-titres, titre visé).
2. **6 agents en parallèle** (outil Agent, en arrière-plan), sur ce seul dossier : 5 profils × 20 spectateurs (makers, curieux du sujet, tout-venant, experts sceptiques, débutants — à adapter au sujet) et 1 analyste YouTube qui ne voit pas les spectateurs. Chaque agent écrit un JSON dans `simu/`.
3. **Agrégat** : `python3 -I <skill>/scripts/agreger.py simu/ <durée en s>` — rétention à 5 s, 15 s, 30 s, 1 min… fin, durée moyenne, engagement, résultats par profil, départs par tranche de 30 s.
4. **Lecture** : les causes de départ citées par plusieurs profils au même moment sont à corriger en priorité ; ce qui retient ceux qui restent est à avancer dans la vidéo.
5. **Corriger le script**, relancer la simulation (même protocole) et comparer les deux courbes.

À dire à l'utilisateur, toujours : c'est une simulation par IA, pas des données YouTube ; elle sert à trouver les faiblesses avant de publier, pas à prédire des vues. Après publication, comparer avec la vraie courbe de YouTube Studio et noter les écarts dans `references/exemple-*.md`.

## 4. Livrer
- Le script (fichier `##NN id`), le nombre de mots et la durée estimée.
- La courbe simulée avant/après correction et les 3 changements qui ont le plus d'effet.
- Titres (≤ 60 caractères) et 2 idées de miniature cohérentes avec les 20 premières secondes.
- Puis passer au skill **voix-off-slides** pour la voix et le calage.
