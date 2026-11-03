# Le moteur du diaporama (`assets/demo-modele.html`)

Une scène fixe de 1920×1080 (`#stage`), mise à l'échelle de la fenêtre. Chaque `<section class="slide" id="…">` est une slide ; on avance **étape par étape** (flèche droite, espace, clic). Tout est en attributs : pas de code à écrire pour une animation simple.

## Structure d'une slide

```html
<section class="slide" id="calcul" data-hudoff="3,4" data-cam='[[1,960,540],[1.45,1420,640]]'>
  <div class="hud"><div class="eyebrow">Étape 3</div><div class="title">Le <em>calcul</em></div></div>
  <div class="cam"> … tout ce qui bouge avec la caméra … </div>
</section>
```
- `.hud` : surtitre + titre, fixes (hors caméra). `<em>` = le mot en couleur d'accent. `.bar` = barre d'accent.
- `.cam` : le plan filmé ; la caméra zoome et se déplace dessus.

## Attributs d'étape

| Attribut | Effet |
|---|---|
| `data-s="2"` | L'élément apparaît à l'étape 2 (0 = dès l'arrivée sur la slide) |
| `data-x="4"` | …et disparaît à l'étape 4 |
| `data-d="300"` | Délai en ms à l'apparition (pour les cascades) |
| classes d'entrée | `a-up` `a-down` `a-l` `a-r` (glissé), `a-pop` (rebond), `a-zoom` (arrive de plus grand), `a-blur` (flou → net) |
| `class="type" data-text="…" data-s2="1"` | Texte **tapé** lettre à lettre à l'étape 1 ; `data-speed` (ms/lettre, 45 par défaut), `data-td` (délai), `data-caret="1"` (curseur qui reste), `data-x2` (disparaît à l'étape) |
| `class="count" data-to="707986" data-s2="1"` | **Compteur** qui défile jusqu'à la valeur ; `data-dec="1"` pour une décimale |
| `data-cam='[[échelle,x,y], …]'` | **Caméra** par étape : zoom `échelle` centré sur le point (x, y) de la scène. `[1,960,540]` = plan large |
| `data-hudoff="1,2"` | Masque le titre aux étapes listées (pendant les zooms) |
| `<svg class="ptr" data-path='[[x,y], …]'>` | **Pointeur de souris** : position par étape ; ajoute `.click` pour l'effet de clic |

Le nombre d'étapes d'une slide = le plus grand `data-s` / `data-s2` / index de caméra.

## Code par slide (quand les attributs ne suffisent pas)

`HOOK[idSlide] = function(étape, animé, slide){ … }` est appelé à chaque étape : tri animé d'un tableau (`classement`), sujets tapés en boucle (`atoi`). Les éléments générés en JS (lignes de tableau, résultats YouTube, mur) lisent leurs données dans `A`.

## Données et images : le bloc `assets`

`<script id="assets" type="application/json">{…}</script>` contient tout ce qui varie : miniatures (`t_xxx`), mur (`wall`), capture de la vraie page (`page`, `apercu`), lignes du tableur (`sheet`), géométrie des encarts (`geo`). Une image vide est remplacée par un repère gris : le modèle tourne sans ses images.
- Remplir : `scripts/integrer-images.py`.
- Capturer la vraie page et ses encarts : `scripts/capturer-page.cjs` → `page` + `geo`. Les caméras des slides « résultat », « sortie », « rendu », « encarts » sont calculées depuis `geo` (fonction `C(boîte, échelle, décalage)`), donc elles suivent la capture si la page change.

## Commandes au tournage

→ / espace / clic : étape suivante · ← : retour · R : rejouer la slide · F : plein écran · H : masquer la barre · N : notes d'oral. La souris et la barre disparaissent après 2 s d'immobilité. L'URL garde la slide (`#calcul`).

## Vérifier

- Parcours complet sans erreur : `window.__S` (liste `[id, nbÉtapes]`) et `window.__go(slide, étape)` permettent de visiter chaque étape en headless (Playwright) et de faire des captures.
- Regarde au moins : la première étape et la dernière de chaque slide, chaque zoom, et l'affichage sur mobile (le cadre doit rester entier).
