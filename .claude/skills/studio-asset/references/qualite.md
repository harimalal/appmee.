# Liste de contrôle avant de montrer des images

Chaque point vient d'un retour réel de l'utilisateur sur le film Dropit (4 versions) ou d'une panne rencontrée. Passe-la sur une planche d'aperçus (un instant par scène) **avant** de montrer quoi que ce soit.

## Ce que l'utilisateur a fait corriger
- [ ] **Vraies images, pas d'illustrations.** Photos réelles dans les tuiles, l'accroche, les écrans de démo. Les illustrations maison ont été refusées.
- [ ] **Le film ne s'ouvre pas sur la démo.** Il s'ouvre sur l'objectif ou la douleur (vraie photo), puis le problème.
- [ ] **Le nom de la marque, pas « AI ».** « Dropit builds the path », « Ask Dropit AI ».
- [ ] **Téléphone entier** sur la première image, la miniature et l'affiche : jamais coupé en bas ou sur le côté. Si la capture d'origine est coupée, la compléter.
- [ ] **Aucun texte qui en chevauche un autre** : vérifier chaque instant où deux légendes, un badge et un téléphone coexistent. Au récapitulatif : seulement le titre en vue d'ensemble.
- [ ] **Badges et bulles lisibles** : grands (38–44 px), fond blanc, texte foncé, **droits** (pas inclinés), ombre douce.
- [ ] **Les titres restent pendant le gros plan** (ils grandissent, le bénéfice s'ajoute dessous).
- [ ] **Les animations de marque sont entières et lisibles** (la goutte tombe vraiment dans le trou et ressort), pas des mouvements de 0,2 s.
- [ ] **Pas de « glitch »** : un résultat qui apparaît se construit progressivement, sans saut ni clignotement ; le zoom vient après.
- [ ] **Le texte tapé est aligné** sur le visuel qu'il décrit.
- [ ] **Les textes du film reprennent ceux de la landing** (promesse, slogan, fin).
- [ ] **Les écrans de démo de l'accueil montrent un contenu vivant** (autres projets avec photos, prénom dans la salutation, ponctuation correcte : « Let's go, Sarah! »).

## Raccords et montage
- [ ] Coupes de la version courte entre deux légendes, jamais au milieu.
- [ ] Fondu enchaîné seulement entre deux images proches ; sinon coupe franche (`'net'`) — un fondu entre deux cadrages différents donne une double image floue.
- [ ] La voix ne dépasse pas la fin ; 1 s d'image fixe au moins après la dernière réplique.

## Technique
- [ ] `ERREUR dans la scène` et `MANQUANT` absents de la sortie de `rendre.cjs`.
- [ ] Maître < 25 Mo si hébergé sur Cloudflare Pages (sinon crf 23).
- [ ] `ffprobe` : h264 + aac (+ mov_text), durées égales à ±0,1 s.
- [ ] Les MP4, sources, scripts, prise de voix et horodatage sont rangés dans le dépôt (le bac à sable est effacé à la fin de la session).

## Pannes déjà rencontrées
- Banques d'images (Pexels, Unsplash) et huggingface.co bloquées par le réseau de l'environnement cloud : utiliser les photos de la landing, ou faire autoriser les domaines dans les réglages de l'environnement (effet à la session suivante).
- `pkill -f motif` tue le shell qui le lance si le motif est dans sa propre ligne de commande (code 144) : utiliser `ps` + `kill <pid>`. Même piège avec `pgrep -f` dans une boucle d'attente.
- Deux rendus en même temps sur le même port : `rendre.cjs` prend un port libre, mais ne lance pas deux rendus dans le même dossier d'images (`--images`).
- Un état d'app qui change d'une capture à l'autre (couleur d'un projet, émoji) : fixer `Math.random` et réutiliser les identifiants créés.
- Un bandeau ou une carte d'aide qui s'ouvre au chargement : le masquer par CSS injecté ou marquer l'état « déjà vu » dans `localStorage` avant le chargement.
