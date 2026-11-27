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
