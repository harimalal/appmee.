# Exemple : « Démo Lancement Product Hunt » (29 octobre 2026)

https://claude.ai/artifact/7b5nNfWtk62rr6b4FmxdaC : comment le créateur a préparé le lancement Product Hunt de Dropit avec Claude. 30 livrables en 2 jours, zéro euro. 30 slides, thème pastel. Planche de design : https://claude.ai/artifact/FE8tEkFnMt8ig8EFYFxGFb

## Ce qui a été appris

- **Le style dépend du sujet.** Le thème sombre du modèle a été refusé (« trop basique »). Une planche de 3 directions a été montrée sur les mêmes 4 slides. Le choix : **pastel produit**, dans la continuité visuelle de l'app lancée (ses dégradés, son corail), avec l'impact des titres de la v1 (`assets/theme-pastel.css`). Pour un autre sujet, refais une planche : la direction se tire de l'univers du sujet (couleurs du produit, de la marque, du milieu), pas d'une démo précédente.
- **Expliquer le contexte avant le travail.** Le créateur a demandé d'ajouter ce qu'est Product Hunt, les références qui y ont lancé, pourquoi c'est incontournable (avis, bêta-testeurs, prendre la température, valider le concept et la valeur), et ses objectifs chiffrés. Quand le sujet tourne autour d'une plateforme ou d'une notion que le public ne connaît pas forcément, prévois ces slides après le bénéfice.
- **Montrer tout ce qui a été livré.** Une slide « inventaire » avec chaque livrable numéroté (30) et un compteur, puis le détail livrable par livrable. C'est ce qui impressionne.
- **Une pub du produit, intégrée au récit** : 3 ou 4 slides avec des exemples concrets (un vrai cas d'usage, de vrais écrans, la vraie landing qui défile), sur un fond plein différent pour qu'on voie que c'est une pub. Placée là où le spectateur se demande « mais c'est quoi, ce produit ? », juste après « Pour qui ».
- **Ce qui n'a pas été essayé avant** se raconte aussi : « je ne savais pas par où commencer ni comment bien le faire », puis « j'ai demandé à Claude d'étudier les meilleurs ».
- **Les sujets annexes deviennent des teasers** : le passage de l'app en anglais tient en une slide, avec « une prochaine vidéo ».
- **Les vraies sources visuelles** : galerie et vidéo lues dans les fichiers publiés de l'artefact (`Artifact` read avec `paths`), images extraites du film avec ffmpeg, et la landing rendue depuis le dépôt du produit quand le site n'est pas joignable (serveur local + `capturer-page.cjs --defiler`).

## Le récit

Accroche (le formulaire Product Hunt vide, la liste de tout ce qu'il faut, « Par où je commence ? ») → titre (mosaïque floutée de la galerie) → bénéfice (« 30 livrables. 2 jours. 0 € ») → Product Hunt, c'est quoi → pourquoi c'est incontournable → un seul jour pour réussir → mes objectifs → tout pour le jour J → pour qui (+ bandeau) → **pub Dropit** (4 slides) → tout faire soi-même → les solutions à la mode → « j'ai demandé à Claude d'étudier les meilleurs » → de la recherche au kit (chaîne de travail) → l'inventaire (30) → ce que ça facilite → le détail : l'anglais, la recherche, la fiche, la galerie, le film, ses 4 versions, un visuel par format, le jour J, les objections, le vrai kit → bilan et appel à l'action.

## Techniques réutilisables

- `integrer-images.py --libre` pour les visuels qui gardent leurs proportions (story, carré, galerie en grand).
- `capturer-page.cjs … --defiler` pour les pages qui se révèlent au défilement.
- Une landing qui **défile** dans une fenêtre de navigateur : `<img>` dans un cadre `overflow:hidden`, animation `translateY` lente en aller-retour.
- Une **bande** d'images parcourue par la caméra : images posées tous les 1350 px, une étape par image, puis un dézoom final.
- Le formulaire de la plateforme **redessiné vide en accroche, puis rempli** dans le détail (texte tapé, compteurs de caractères) : la boucle se referme.
