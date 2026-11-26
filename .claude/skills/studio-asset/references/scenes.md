# Catalogue des scènes types

Toutes ces scènes sont déjà en place, en version simple, dans `assets/scene-modele.html` ; le code complet et poli est dans le film Dropit (`MISSIONS/2026-10-13-product-hunt/livrables/video/scene.html` du dépôt harimalal/dropit). Chaque scène est une fonction de `t` appelée par `render(t)`.

## Table des matières
1. Outils communs
2. Accroche sur une vraie photo
3. Chaos des outils actuels
4. Révélation du logo
5. Promesse en contraste
6. Téléphone, écrans et caméra
7. Saisie lettre par lettre
8. Contenu qui apparaît ligne par ligne
9. Gestes : toucher, anneau, points qui s'envolent
10. « 3 weeks later »
11. Conversation avec l'assistant
12. Bulles de questions
13. Récapitulatif en trois téléphones
14. Fin
15. Pièges

## 1. Outils communs
- `seg(t, a, b)` : 0 avant a, 1 après b. `fade(t, a, b, c, d)` : apparaît de a à b, disparaît de c à d.
- `eio` (accélère puis freine) pour les mouvements de caméra, `eout` pour les entrées, `eback` (léger dépassement) pour ce qui « se pose ».
- Tout est en positions absolues dans l'image 1920×1080 ; ce qui est sur l'écran du téléphone vit dans `#ovs`, repère 390×844 (celui des captures et de `boites.json`), et suit donc la caméra automatiquement.

## 2. Accroche sur une vraie photo
Une photo réelle liée au cas (Dropit : la tuile « Home renovation » de la landing, retouchée en « Buy a house », 0 %). Elle entre avec une légère rotation (−3° → 0°), grandit de 5 % pendant 2 s, puis un flash blanc de 0,3 s fait la transition vers le chaos. Texte à gauche : l'objectif en très gros (96 px), puis la question en plus petit et plus clair.

## 3. Chaos des outils actuels
Des cartes HTML qui imitent les outils que le public utilise vraiment : tableur (cellules `#REF!`, `#N/A` en rouge, nom de fichier `plan_FINAL_v7(2).xlsx`), boîte mail (« Inbox · 214 unread », objets en « Re: Fwd: »), liste de tâches (« 47 overdue », mentions « late »), calendrier saturé, post-it écrits à la main (police manuscrite), icônes d'applis avec pastilles rouges (12, 31, 214…). Chaque élément arrive d'un bord (`from`), à son instant (`at`), et tremble légèrement (sinus). À la fin, `collapse` les aspire tous au centre en tournant et rétrécissant, et un gros « Still no plan. » apparaît. Les légendes de cet acte sont dans une pilule blanche en bas (`PILL`), pour rester lisibles sur le désordre.

## 4. Révélation du logo
Animer l'**idée** de la marque, pas seulement une apparition. Dropit : le logo est découpé en morceaux (gauche, droite, trou, goutte) ; la goutte apparaît au-dessus, tombe dans le trou (le trou s'écrase, une onde part), disparaît, puis remonte et se pose comme le « O » (`logoDrop(k)` dans le film Dropit). Il faut que le mouvement soit **entier et lent** (≈ 2,7 s) : l'utilisateur avait demandé une chute « bien visible ». Sans logo en morceaux : apparition avec `eback` + léger flou → net.

## 5. Promesse en contraste
Deux temps centrés : « <App> isn't another ~~all-in-one app~~. » (texte barré d'un trait épais de la couleur d'accent) puis « It's the <surligné>path to your goals</surligné>. » + une annotation manuscrite (« guided, step by step »). Les mots viennent de la landing.

## 6. Téléphone, écrans et caméra
- `ECRANS` + `SEQ` : quelle capture à quel instant, avec un fondu court (0,15 à 0,45 s) entre deux captures.
- `CAM` : liste de plans `[instant, {sx, sy, z, cx, cy}]` : le point (sx, sy) de l'écran est placé en (cx, cy) dans l'image, à l'échelle z. Deux plans identiques = arrêt sur image ; deux plans différents = mouvement. Zoom typique 1,75 à 2,4 ; durée d'un mouvement 0,7 à 1 s.
- `fit()` garde le bord gauche du téléphone zoomé à droite de 850 px, pour ne jamais couvrir la légende de gauche.
- Entrée du téléphone par le bas (cy 1700 → 540), sortie par le bas avant le récapitulatif.
- Un téléphone **entier** dès qu'il apparaît pour la première fois (jamais tronqué sur la première image ni sur une miniature).

## 7. Saisie lettre par lettre
Web : le script de capture photographie la vraie barre de saisie après chaque lettre (`captures/saisie/NN.png`) ; la scène superpose l'image n° `round(seg(t, a, b) × longueur)` à la position de la barre, pendant que la caméra est zoomée dessus (z ≈ 2,3). Puis un toucher sur le bouton d'envoi.
Mobile sans captures par lettre : superposer un `<div>` à la position du champ, avec la police de l'app, qui affiche `texte.slice(0, n)` + un curseur clignotant (`Math.floor(t * 2) % 2`).

## 8. Contenu qui apparaît ligne par ligne
Quand l'app produit un résultat (plan, liste, réponse), le montrer **se construire** : des caches de la couleur du fond posés sur chaque ligne (positions depuis `boites.json`), qui s'effacent l'un après l'autre (toutes les 0,4 s), téléphone entier ; puis seulement le zoom sur l'objectif reformulé, puis sur les étapes. L'utilisateur avait demandé : « la goutte entière, sans glitch, puis les étapes apparaissent progressivement, ensuite seulement le zoom ».
Écran d'attente (génération) : s'il contient une animation, la recréer proprement par-dessus la capture (Dropit : le trou de la capture est effacé et redessiné, une goutte entière tombe dedans en boucle).

## 9. Gestes
- **Toucher** : `ripple(r, t, instant, x, y)` — disque gris translucide qui grandit et s'efface en 0,5 s, au point touché (repère 390×844). Toujours un toucher avant un changement d'écran provoqué par l'utilisateur.
- **Anneau** : `ringOn(t, BOX.zone, a, d)` — cadre de la couleur d'accent autour d'un élément (progression, points), pendant 2 s.
- **Points qui s'envolent** : pastille « +2 pts » qui monte de 120 px en grossissant (`eback`) puis s'efface.
- **Éclat** : petite étoile qui tourne à côté d'un compteur de points.
- **Tuile qui se pose** : découper la zone de la nouvelle tuile dans la capture et la faire passer de l'échelle 0,6 à 1 avec `eback`, puis un halo de couleur autour.

## 10. « 3 weeks later »
Pilule sombre centrée (« 3 weeks later ») qui apparaît 0,8 s pendant le changement d'écran, puis capture du même projet avancé (progression à 50 %, « ahead of pace »), anneau sur la barre de progression, zoom sur les points.

## 11. Conversation avec l'assistant
Toucher l'onglet → capture du chat vide → question tapée (capture avec le champ rempli) → toucher Envoyer → capture « en attente » 0,8 s → réponse. Zoomer sur la réponse **après** qu'elle soit apparue. Les réponses sont écrites à la main, courtes, avec des titres et du gras : c'est la preuve de valeur. Légende : « Stuck? Ask <App> AI how. » puis « Ask for your 80/20 priorities. »

## 12. Bulles de questions
4 ou 5 questions qu'on pourrait poser à l'assistant, en bulles blanches de conversation (coin bas gauche moins arrondi), mot clé en couleur d'accent, légèrement inclinées (±2°), qui arrivent l'une après l'autre (toutes les 0,45 s) sous une légende « Ask <App> AI anything that moves you forward. »

## 13. Récapitulatif en trois téléphones
Trois mini-téléphones (300×649) en ligne, chacun avec **seulement son titre** en grand badge blanc au-dessus. Puis gros plan sur chacun à tour de rôle (échelle 1,55, côté alterné) : le titre reste et grandit, le bénéfice apparaît dessous, les fonctions arrivent en bulles blanches **droites** (pas inclinées), texte foncé, pastille de couleur. Dézoom, phrase de synthèse en bas (y ≈ 972), sortie.

## 14. Fin
Logo (même animation qu'à la révélation, en plus petit), qui monte ; slogan de la landing en deux lignes (la première plus claire, la seconde en gros avec un mot en couleur) ; adresse dans une pilule de la couleur d'accent ; une ligne de réassurance (« Free. No ads. Works in your browser. »). Garder 1,5 s d'image fixe à la fin.

## 15. Pièges
- Mesurer les positions dans `boites.json` plutôt que de les estimer : un anneau décalé de 4 px se voit.
- Un élément qui doit disparaître doit avoir `opacity = 0` explicitement à chaque image (la scène ne garde aucun état entre deux appels de `render`, et un rendu peut sauter dans le temps).
- `offsetWidth` d'un texte n'est juste qu'une fois les polices chargées : c'est pour ça que `window.ready` attend `document.fonts.ready`.
- Les captures en PNG 1170×2532 pèsent lourd : 15 à 20 captures restent fluides ; au-delà, passer en WebP.
