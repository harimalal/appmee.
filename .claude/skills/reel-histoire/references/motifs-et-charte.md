# Motifs de scène, charte graphique, logos

Dans ce document, `<skill>` désigne le dossier de ce skill. À lire pour écrire `story.html`.

## Motifs de scène (catalogue éprouvé)

Chaque scène = une fonction `scene(id, copy, fn)` dans `story.html`, qui redessine l'état exact à l'instant `t` (aucune animation sur horloge réelle). Les motifs ci-dessous existent déjà dans `<skill>/assets/reference-seo/story.html` et `<skill>/assets/reference-tri/story.html` et `<skill>/assets/reference-carrousels/story.html` (le nom de la scène sert de repère).

| Motif | Quand l'utiliser | Scène de référence |
|---|---|---|
| Titre + logo + commande | Ouverture : nommer le sujet et l'outil, montrer l'unique consigne (un **vrai** nom de fichier) | `titre` |
| Cartes barrées → carte validée | Le renversement « ce n'est pas A ni B, c'est C » | `probleme` |
| Compteur géant + grille de carrés | Le chiffre paradoxal (N éléments dans un ensemble de M) | `hook` |
| Mots-clés flottants → catalogue | Expliquer une notion que le spectateur ne connaît pas (ici : l'indexation) | `indexation` |
| Rapport d'outil + terminal qui scanne | « Où ça se voit » + « qui a cherché la cause » | `console` |
| Navigateur à deux adresses + tampon | Un doublon, une confusion à deux versions | `slash` |
| Capture réelle surlignée + chips | Un défaut visible dans une interface réelle | `filtres` |
| Fichier avant / après + erreur géante | Un élément qui change de nom, un lien cassé | `fichier` |
| Graphe de liens qui se dessinent | Un maillage, des relations, des dépendances | `articles` |
| Liste de coches + minuteur | Le process : N étapes, durée totale | `corrections` |
| **Curseur avant / après** | Le plan signature : les mesures avant et après | `avantapres` |
| Trois cartes de résultat | Vérifié / attendu / objectif | `resultat` |
| Défilé de vraies captures | Montrer le **volume** (une liste de centaines d'éléments) ; captures basse résolution acceptables car floutées par le mouvement, jamais en gros plan | `hook` (reference-tri) |
| Critères en deux colonnes (supprimer / garder) | Montrer l'instruction donnée à un outil quand le prompt exact n'est pas dans la source : afficher des **critères**, pas une citation | `criteres` (reference-tri) |
| Trois cartes d'outils, une surlignée | « Pourquoi cet outil » (voir recit.md : ne dire que ce que la source établit) | `extension` (reference-tri) |
| Suppression successive accélérée | Une boucle répétitive montrée au rythme réel puis accélérée, **étiquetée « accéléré »** à l'écran et à la voix ; compteur qui décroît ; lignes redessinées (aucun titre réel) | `suppression` (reference-tri) |
| Cartes à pastille rouge qui s'empilent | Les problèmes du spectateur, **dits avec ses mots** (une carte = un problème), avec léger flottement pour éviter les plages figées | `probleme` (reference-carrousels) |
| Trois cartes « tu donnes / l'IA te donne / tu donnes » + puces | Expliquer un système en une scène : entrée, sortie, réglages de l'utilisateur | `systeme` (reference-carrousels) |
| Téléphone qui défile (vraies slides) puis PDF | Montrer la **preuve** : de vraies pièces qui défilent comme dans l'application (en-tête qui passe de « Instagram » à « LinkedIn · PDF »), jamais de pièces générées pour la vidéo | `exemples` (reference-carrousels) |
| CTA sur fond nuit + retour du titre | Fin et boucle | `cta` |

Un **nouveau motif** se construit avec les mêmes outils (`enter`, `put`, `P`, `eo`, `eoBack`, `io`, `hlSet`, `ev`, `circle`, `drift`, `caption`) et doit respecter la charte (ci-dessous). Ne pas réutiliser deux fois le même motif dans une vidéo.

### Charte graphique (par défaut : Reflex IA ; pour une autre marque, remplacer couleurs, police et pastille)
Un **fond pastel par scène**, jamais deux voisins identiques (`#EEECFB #FDEFF4 #ECFAF9 #E8F3FB #FBF1ED #F1EFFD #ECF4FC`), nuit `#0B1433` réservé à la dernière scène ; Inter Display 900 ; surligneur jaune `#FFD93B` ; violet `#6C5CE7` ; rouge `#E5383B` = avant / problème ; vert `#19A974` = après / validé ; encre `#0F1020`. Pastille « REFLEX•IA » en haut à gauche, compteur « n/N » en haut à droite, grand cercle translucide en coin. **Zones sûres** : haut 200, bas 380, gauche 84, droite 150 (valeurs TikTok du dépôt, non officielles pour Reels). Pas d'emoji ni d'objets décoratifs (plantes, tasses, ordinateurs).

### Logos
Uniquement des **fichiers officiels existants** (le dossier de logos du projet, ex. `CONTENT_FACTORY/carrousel/logos/` pour Reflex IA), sans modification autre que le détourage. Un logo livré sur fond blanc se détoure par canal alpha (couleur unie + masque issu de la luminance, ImageMagick) ; `mix-blend-mode` ne fonctionne pas dans un élément déjà transformé. Si le logo exact manque (mascotte de l'outil, etc.), **le dire** à l'utilisateur plutôt que de le redessiner.

---

## Motifs ajoutés au 4e essai (reference-blog-factory)
| Motif | Quand l'utiliser | Scène de référence |
|---|---|---|
| Liste d'étapes en cascade avec boucle d'audit | Présenter un système : une rangée par étape (numéro, nom, sous-titre de 3 mots), une flèche courbe rouge qui repart de l'audit vers l'étape précédente, une étiquette « < 80 : on corrige » ; une note finale non lue. Limiter les sous-titres pour rester sous `max_mots_visibles` | `etapes` (reference-blog-factory) |
| Grille de carrés qui se remplit | Donner l'échelle d'un nombre (64 articles) pendant qu'une phrase est dite, puis la remplacer par la carte du nombre ; casse aussi les plages figées | `chiffres` (reference-blog-factory) |
| Cartes + puces d'idées | Une notion (« penser le SEO ») et ses trois composantes qui arrivent au rythme de la phrase (instants calculés sur la durée de la phrase, `words[...]`) | `probleme` (reference-blog-factory) |
| Défilé de pages réelles à l'échelle mobile | Plusieurs pages (6) dans un cadre de téléphone : haut de page tenu environ 20 % du pas (titre lisible), défilement de 2 300 px, puis glissement latéral vers la page suivante ; étiquette de type de page sous le cadre (étiquettes à déclarer comme votre qualification, pas un champ de la source) | `exemples` (reference-blog-factory) |

## Motifs ajoutés au 5e essai (reference-comparatif)
| Motif | Quand l'utiliser | Scène de référence |
|---|---|---|
| Carte barrée (rouge) face à une rangée validée (coche verte) | Opposer une pratique courante et la méthode, sans test chiffré (« simple demande » / « skill + système ») | `systeme` (reference-comparatif) |
| Cartes qui apparaissent vides puis se remplissent de critères réels | Montrer que ce qui compte change d'un cas à l'autre (3 types d'outils, 4 critères chacun, tirés des en-têtes publiés) ; les cartes arrivent pendant la phrase d'accroche, les critères au rythme des phrases suivantes | `criteres` |
| Tableau réel agrandi avec balayage horizontal | Un tableau large (10 colonnes) : l'image est montée à l'échelle 1,5, on balaie les colonnes, puis on revient sur la ligne surlignée ; trois tableaux se succèdent en glissant | `tableau` |
| Fenêtre agrandie (1 000 × 1 150) | « Plus gros » : le cadre occupe presque tout l'écran, mais le texte d'en-tête du cadre reste dans les zones sûres (gauche ≥ 84, droite ≤ 930) | `tableau`, `usages`, `profils` |

## Motifs ajoutés au 6e essai (reference-site-0-euro)
| Motif | Quand l'utiliser | Scène de référence |
|---|---|---|
| **Ouverture = la vraie chose, zoom avant fort puis dézoom** (jamais un titre qui apparaît) | Dès la 1re seconde : la page réelle dans une grande fenêtre navigateur, caméra sur la toile (`camAt`) qui zoome sur le titre, puis sur un détail réel (ici l'étiquette « Limites à savoir »), puis dézoome | `ouverture` |
| **Caméra façon Prezi** sur une toile de pages réelles | Zoom, dézoom (`dip`) et glissement d'une page à l'autre au lieu d'apparitions/disparitions | `ouverture`, `pages` |
| **Pile en couches qui construit** | Présenter un « stack » : les couches (outils) s'empilent de bas en haut, puis le résultat (pages réelles) se pose dans un cadre au-dessus | `pieces` |
| **Fenêtres de pages en défilement lent + swipe** | Une page de chaque type : une fenêtre par type, défilement lent (230 unités/s), glissement horizontal vers la suivante ; la phrase dure au moins le temps du défilement (`hold`) | `pages` |
| **Deux colonnes : solutions classiques à gauche, ce dont on n'a pas besoin à droite** | Se comparer à des solutions connues **sans rien affirmer sur elles** : la gauche se grise quand la droite prend la parole | `compare` |
| **Grille de cartes qui passe au vert en vague** + compteur + contrôles | « Tout en une fois » : **schéma annoncé « illustration »** quand l'opération n'est pas réellement montrable | `masse` |
| **Poussée verticale entre scènes** | L'une monte, l'autre descend ; rien ne se superpose | `__setTime` |
| **Étiquette unique dans la bande du haut** (`swap`) | Aucun texte au-dessus d'un autre : l'ancienne sort par le haut avant que la suivante monte du bas ; `qa.cjs` vérifie l'absence de chevauchement | toutes |

## Motifs ajoutés au 7e essai (reference-comparatif-site, reel « 28 comparatifs » v6)
| Motif | Quand l'utiliser | Scène de référence |
|---|---|---|
| **Démo plein cadre façon site (sans fenêtre)** | Toute preuve par pages réelles : la page (version ordinateur 1 280 px) occupe tout l'écran 1 080 × 1 920 (échelle 1080/1280), étiquette unique sur un bandeau blanc (`scrim`) en haut ; **jamais** de barre de navigateur ni de bordure (retour de Hari : « arrête la démo dans la fenêtre, fais sans cadre ») | toutes les scènes de page |
| **Curseur + clic** | Montrer ce qu'on explique en « cliquant » dessus : flèche (`makeCursor`, positions en pixels écran projetées depuis les coordonnées de page à l'instant du clic), onde (`makeClicks`). **Plus de boîte jaune** (voir 8e essai) | `criteres`, `tableau`, `usages`, `profils` |
| **Scroll + zoom pilotés par la caméra** | `camAt` (centre, zoom, `dip`) : défilement lent, zoom sur la cible au moment où la voix la nomme | toutes |
| **Swipe** | Doigt translucide (`makeSwipes`) + glissement de caméra d'une page à l'autre (3 comparatifs côte à côte sur la toile), ou glissement horizontal d'un tableau qui défile (colonnes cachées révélées) | `criteres`, `tableau`, `profils` |
| **Plongée** | Clic sur une carte de la liste, zoom jusqu'à remplir l'écran, la page cible apparaît en dézoomant (`cvB` de 0,55 à 1) | `ouverture` |

## Motifs ajoutés au 8e essai (reference-comparatif-site v7 et reference-site-0-euro v7)
| Motif | Quand l'utiliser | Scène de référence |
|---|---|---|
| **L'élément cliqué ressort vers l'avant** (aucun cadre jaune) | Mettre en valeur une cible réelle (colonne, carte, puce, lien de menu, bloc) : `makePops(host, srcUrl, imgW, imgH, ox, oy)` crée un voile sur le reste de la page et un calque qui reprend la région de la capture, soulevé avec une ombre ; puis la caméra zoome pour qu'on lise, puis dézoome. Retour de Hari : « il vaut mieux cliquer, ne pas le mettre en jaune, mais les agrandir, dézoomer pour qu'on voie ce qui est écrit, ou que les informations ressortent vers l'avant » | `criteres`, `tableau`, `usages`, `profils` ; ouverture, menu, newsletter du site |
| **Navigation continue entre pages réelles** | Une couche plein écran par page (`lyr`), un clic par phrase vers la suivante (menu, carte, bouton), swipe/scroll entre les clics ; l'en-tête du site reste visible sous la bande d'étiquette (`camTop` : haut de page à y = 640) | `pages` du site |
| **Changement de charte en balayage** | La même page plein cadre, remplacée par sa version « océan » puis « forêt » par un balayage, plutôt que des tuiles encadrées | `charte` du site |
| **Ouverture « filtres → carte → article »** | Montrer d'emblée la matière du site : clic sur la rubrique, clic sur deux filtres de types d'outils (captures **réelles** de chaque état filtré, `assets/pc3/comparatifs-f0|f1|f2.jpg`), la **carte de comparatif** de chaque vue ressort, clic sur la carte → plongée dans l'article. Retour de Hari : ce qui doit ressortir, ce sont **les comparatifs par filtre**, pas les petits filtres ni le menu | `ouverture` du site |
| **Terminal Claude Code lisible** | Remplace le décor de barres colorées : une instruction en langage naturel **tapée** (révélation par pas de caractère, texte entier dans le DOM), puis 3 lignes de réponse cochées, mot « illustration » affiché, pastille « 0 ligne de code tapée ». Polices ≥ 35 px (mono) et 44 px (réponses) | `code` du site |
| **Étiquette au-dessus du voile** | `.lbl, .sublbl { z-index: 50 }` : un voile blanc (`.scrim`, z-index 40) posé sur la page **voile aussi** une étiquette qui le précède dans le DOM (effet « flou ») ; voile `mid` (blanc plein jusqu'à 84 %) sous la bande de texte | toutes les scènes sur page réelle |

## Motifs ajoutés aux 10e et 11e essais
| Motif | Quand l'utiliser | Scène de référence |
|---|---|---|
| **Mur d'exemples d'un même système** | Prouver « un système, plein de résultats » : rangées de vraies slides qui défilent en sens opposés, puis une visionneuse par univers (swipe, la dernière slide ressort), puis les trois côte à côte | `reference-carousel-factory` |
| **Chaîne de fichiers animée** | Montrer un système de production : fichier source → fiche → position → sorties → contrôle, chaque étape en rendu fidèle du vrai fichier, avec un clic qui fait ressortir la ligne clé | `reference-content-factory` |
| **Couverture mur 3D** | Couverture d'un reel « système » : vrais rendus en perspective, titre en deux lignes avec un mot surligné, bandeau « 1 … = / → … » | `cover.html` des deux références |

