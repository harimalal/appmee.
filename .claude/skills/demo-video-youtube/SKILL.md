---
name: demo-video-youtube
description: Transforme un résultat construit avec Claude (veille YouTube, tableau de bord, outil, automatisation, app, document) en support de vidéo YouTube, un diaporama animé 16:9 qui démontre comment on l'obtient. On ouvre sur le résultat ou le blocage, puis la façon fastidieuse et les outils existants avec leurs limites, puis les étapes avec Claude (prompt, outil, calcul, rendu). Interfaces reproduites au plus près (Chrome, YouTube, tableur, Claude Desktop, terminal), vraies captures et images, texte tapé, zooms et caméra, compteurs, pointeur, appels à l'action S'abonner / J'aime / Commenter, notes d'oral, export MP4. Utilise ce skill dès que l'utilisateur veut une vidéo, une démo, un tuto animé ou un support de tournage YouTube à partir de ce qu'on a construit (« fais-en une vidéo », « explique en slideshow comment on a construit ça »), même sans dire « diaporama ». Pour lancer une app (film de lancement, posts réseaux), préférer studio-lancement-app.
---

# Démo vidéo YouTube

Version : 2026-10-28.

Né le 28 octobre 2026 avec « Démo Veille YouTube » (20 slides, 94 étapes) : comment on a construit l'analyseur de vidéos YouTube avec Claude. Le modèle `assets/demo-modele.html` **est** cette démo, sans ses images. Elle tourne telle quelle et sert de point de départ à toute nouvelle démo.

Trois idées :
- **Le résultat d'abord.** On montre ce qu'on obtient (ou le blocage, ou la corvée) avant de montrer comment.
- **Le vrai.** Vraies captures du résultat, vraies images, vrais chiffres de la conversation. Interfaces reproduites au plus près ; logos laissés en repères.
- **L'oral explique, l'écran montre.** Un titre, une structure par slide, une note d'oral par slide.

`<skill>` désigne le dossier de ce skill.

## Déroulé

1. **Rassemble la matière** sans rien demander d'abord : la conversation (ce qui a été construit, les étapes réelles, le prompt, les chiffres), le ou les artefacts du résultat (relis-les), les images disponibles (miniatures, captures). Ne pose ensuite que ce qui manque (chaîne, ton, durée visée), groupé, avec une option recommandée.
2. **Écris le déroulé** en texte, une ligne par slide : titre, structure, effets, phrase d'oral. Suis l'arc de `references/narration.md` (résultat → blocage → piège → bénéfices → pour qui → à la main → autres solutions → pivot → outil → étapes → résultat détaillé → bilan → appel à l'action), adapté au sujet. Montre-le avant de coder si la vidéo est longue ou si le sujet est nouveau.
3. **Copie le modèle** `assets/demo-modele.html` et réécris les slides : textes, données (`assets`), notes (`NOTES`), caméras. Vocabulaire des animations : `references/moteur.md`. Interfaces et règles sur les logos et les images : `references/interfaces.md`.
4. **Capture le vrai résultat** :
   ```
   NODE_PATH=$(npm root -g) node <skill>/scripts/capturer-page.cjs <page-du-résultat.html|url> capture.jpg --boites boites.json
   python3 -I <skill>/scripts/integrer-images.py demo.html --img page=capture.jpg --geo capture.geo.json \
       --img t_n1=miniatures/<id>.jpg … --mur miniatures/ --json donnees.json
   ```
   Un artefact claude.ai : relis-le (`Artifact` read), garde son HTML en local, capture ce fichier.
5. **Vérifie** chaque étape en headless (`window.__S`, `window.__go(i, étape)`) : zéro erreur console, captures de la première et de la dernière étape de chaque slide et de chaque zoom, regarde-les. Vérifie aussi le mobile.
6. **Publie** en artefact (ou rends le fichier), et si demandé, **enregistre** :
   ```
   NODE_PATH=$(npm root -g) node <skill>/scripts/enregistrer.cjs demo.html demo.mp4 --temps temps.json
   ```
7. **Livre** : lien, nombre de slides, commandes de tournage (→ ← R F H N), liste des repères de logos à remplacer au montage, rappel sur les miniatures des créateurs, et le prompt complet à coller dans la description de la vidéo si la démo y renvoie.

## Règles

- Un titre et une structure par slide. Pas de graphique pour comparer des outils : une liste avec les limites en rouge.
- Appels à l'action en slide 2 et en dernière slide (s'abonner, liker, commenter avec un sujet).
- Méthode manuelle : au moins 10 lignes remplies, les premières tapées lentement avec zoom.
- Zooms sur ce qui compte : l'encart de calcul, le classement, le top 3, chaque encart du rendu final.
- Estimations écrites comme telles, pas de prix d'outils, pas de logo redessiné, pas de chiffre inventé.
- Pendant un zoom, masquer le titre (`data-hudoff`).
- Garder un seul fichier HTML autonome sous 15 Mo.

## Exemple

`Démo Veille YouTube` : https://claude.ai/artifact/Pn2hNDHRa2NmW8LKDM9p62 (avec ses images). La recherche qu'elle met en scène vient du skill `veille-youtube`.

## Prompt type

> Fais une vidéo YouTube de <ce qu'on a construit / l'artefact « … »> : un diaporama animé 16:9 qui montre comment on obtient ce résultat. Ouvre sur le résultat, puis le blocage et la façon fastidieuse (méthode manuelle avec au moins 10 lignes, outils gratuits et payants avec leurs limites), puis les étapes avec Claude (outil, prompt, collecte, calcul, rendu final), avec zooms sur le calcul, le classement, le top 3 et chaque encart du rendu. Un titre et une structure par slide, l'oral dira le reste (notes par slide). Vraies captures et vraies images, interfaces reproduites au plus près, logos en repères. Appels à l'action s'abonner / liker / commenter en slide 2 et à la fin.
