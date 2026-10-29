---
name: demo-video-youtube
description: Transforme un résultat construit avec Claude (veille YouTube, tableau de bord, outil, automatisation, app, document) en support de vidéo YouTube, un diaporama animé 16:9 qui démontre comment on l'obtient. On ouvre sur le résultat ou le blocage, puis la façon fastidieuse et les outils existants avec leurs limites, puis les étapes avec Claude (prompt, outil, calcul, rendu). Interfaces reproduites au plus près (Chrome, YouTube, tableur, Claude Desktop, terminal), vraies captures et images, texte tapé, zooms et caméra, compteurs, pointeur, appels à l'action S'abonner / J'aime / Commenter, notes d'oral, export MP4. Utilise ce skill dès que l'utilisateur veut une vidéo, une démo, un tuto animé ou un support de tournage YouTube à partir de ce qu'on a construit (« fais-en une vidéo », « explique en slideshow comment on a construit ça »), même sans dire « diaporama ». Pour lancer une app (film de lancement, posts réseaux), préférer studio-lancement-app.
---

# Démo vidéo YouTube

Version : 2026-10-29 (v6, après la démo Carrousels IA).

Né le 28 octobre 2026 avec « Démo Veille YouTube » (20 slides, 94 étapes) : comment on a construit l'analyseur de vidéos YouTube avec Claude. Le modèle `assets/demo-modele.html` **est** cette démo, sans ses images. Elle tourne telle quelle et sert de point de départ à toute nouvelle démo.

Trois idées :
- **Le problème d'abord.** On ouvre sur le problème vécu, puis le titre (la solution illustrée, floutée en fond), puis le bénéfice immédiat, avant de montrer comment.
- **Le vrai.** Vraies captures du résultat, vraies images, vrais chiffres de la conversation. Interfaces reproduites au plus près ; logos laissés en repères.
- **L'oral explique, l'écran montre.** Un titre, une structure par slide, une note d'oral par slide.

`<skill>` désigne le dossier de ce skill.

## Déroulé

1. **Rassemble la matière** sans rien demander d'abord : la conversation (ce qui a été construit, les étapes réelles, le prompt, les chiffres), le ou les artefacts du résultat (relis-les), les images disponibles (miniatures, captures). Ne pose ensuite que ce qui manque (chaîne, ton, durée visée), groupé, avec une option recommandée.
2. **Écris le déroulé** en texte, une ligne par slide : titre, ce qu'on voit (structure et animation), phrase d'oral. Les trois premières slides sont fixes (accroche-problème, titre, bénéfice) ; le reste se compose pour ce sujet à partir des sections de `references/narration.md`, sans recopier le plan ni les animations du modèle. **Montre-le et fais-le valider avant de coder.**
3. **Pars du modèle** `assets/demo-modele.html` pour le moteur, le style et le kit d'interfaces, puis écris tes propres slides : textes, données (`assets`), notes (`NOTES`), caméras, et les animations propres au sujet. Vocabulaire des animations : `references/moteur.md`. Interfaces et règles sur les logos et les images : `references/interfaces.md`.
4. **Fais la planche de design** (voir `references/narration.md`), publie-la, fais choisir. Puis **capture le vrai résultat** :
   ```
   NODE_PATH=$(npm root -g) node <skill>/scripts/capturer-page.cjs <page-du-résultat.html|url> capture.jpg --boites boites.json
   python3 -I <skill>/scripts/integrer-images.py demo.html --img page=capture.jpg --geo capture.geo.json \
       --img t_n1=miniatures/<id>.jpg … --mur miniatures/ --json donnees.json
   ```
   Un artefact claude.ai : relis-le (`Artifact` read avec `path: "index.html"`), garde son HTML en local, capture ce fichier. S'il lit sa base de données (capacité db), il ne s'affiche pas hors de claude.ai : lis ses collections avec ArtifactData (`list` avec `out_dir`), puis `python3 -I <skill>/scripts/simuler-base.py page.html donnees/ capturable.html --etat "…"` avant de capturer.
   Une interface **redessinée** en HTML (plus lisible) peut compléter la capture, en particulier pour le fond flouté du titre et pour les projecteurs (voir `references/exemple-cockpit.md`).
5. **Vérifie** chaque étape en headless (`window.__S`, `window.__go(i, étape)`) : zéro erreur console, captures de la première et de la dernière étape de chaque slide et de chaque zoom, regarde-les. Vérifie aussi le mobile.
6. **Publie** en artefact (ou rends le fichier), et si demandé, **enregistre** :
   ```
   NODE_PATH=$(npm root -g) node <skill>/scripts/enregistrer.cjs demo.html demo.mp4 --temps temps.json
   ```
7. **Livre** : lien, nombre de slides, commandes de tournage (→ ← R F H N), liste des repères de logos à remplacer au montage, rappel sur les miniatures des créateurs, et le prompt complet à coller dans la description de la vidéo si la démo y renvoie.

## Règles

- Un récit propre à chaque sujet : pas de copie du plan, des titres ni des animations d'une démo précédente.
- **Un style propre à chaque sujet** : après le déroulé, une planche de 2 ou 3 directions de design sur 4 slides, tirées de l'univers du sujet (couleurs du produit ou de la marque). Fais choisir avant de construire. Jamais le thème sombre du modèle par défaut.
- Si le sujet tourne autour d'une plateforme ou d'une notion peu connue : l'expliquer (c'est quoi, références, pourquoi c'est important, objectifs) avant la méthode.
- **Une vidéo, un sujet.** Ce qui relève d'un autre chantier (monter le site, traduire l'app, décliner en posts) devient une slide teaser, avec un appel au commentaire précis (« écris SITE en commentaire si tu veux cette vidéo »), repris dans le bilan.
- **Le temps, en gros** : à la main (durées du process × volume, écrit « estimation ») face au temps réel, sur le seul périmètre de la vidéo. Puis la croissance, tirée des vraies dates.
- **Mesurer plutôt qu'estimer** : si l'outil se relance (un script de rendu, un build), relance-le dans une copie de travail, chronomètre-le et montre sa vraie sortie à l'écran.
- Montrer **tout ce qui a été livré** : une slide inventaire numérotée, puis le détail.
- Si le créateur a un produit : une courte pub de 3 ou 4 slides avec de vrais exemples, sur un fond distinct, après « Pour qui ».
- Ouverture : accroche sur le problème, titre avec la solution illustrée et floutée en fond, bénéfice immédiat.
- Un titre et une structure par slide. Pas de graphique pour comparer des outils : une liste avec leurs plus en vert et leurs moins en rouge.
- Appel à l'action jamais en entrée : petit bandeau en bas après « Pour qui », puis complet à la fin.
- Raconter au « je » ce que le créateur a vraiment essayé : demande-le.
- Méthode manuelle : au moins 10 lignes remplies, les premières tapées lentement avec zoom.
- Zooms sur ce qui compte dans le vrai résultat.
- Une nouvelle version garde les slides retirées en réserve, après la fin.
- Estimations écrites comme telles, pas de prix d'outils, pas de logo redessiné, pas de chiffre inventé.
- Pendant un zoom, masquer le titre (`data-hudoff`).
- Garder un seul fichier HTML autonome sous 15 Mo.

## Exemples

- `Démo Veille YouTube` : https://claude.ai/artifact/Pn2hNDHRa2NmW8LKDM9p62 (avec ses images). La recherche qu'elle met en scène vient du skill `veille-youtube`.
- `Démo Cockpit Projets` : https://claude.ai/artifact/TE6Q2c1W7WgZq2yo4J3YkV. Récit adapté, au « je », base de données simulée pour la capture, interface redessinée, projecteurs : voir `references/exemple-cockpit.md`.
- `Démo Lancement Product Hunt` : https://claude.ai/artifact/7b5nNfWtk62rr6b4FmxdaC. Planche de design puis thème pastel, contexte de la plateforme, inventaire de 30 livrables, pub du produit avec la landing qui défile : voir `references/exemple-product-hunt.md`.
- `Démo Blog Factory` : https://claude.ai/artifact/TiVRxcMY6qtqaNoSsTz4iN. Même thème pastel, violet pâle en couleur secondaire ; pub = revue du site (fiches d'articles, diversité, angle, newsletter) ; le temps en gros et la croissance ; le site renvoyé à une autre vidéo par un appel au commentaire : voir `references/exemple-blog-factory.md`.
- `Démo Carrousels IA` : https://claude.ai/artifact/5eHFmxcW2WrdrFKthYrRmN. La série pastel choisie sur planche ; ce que le créateur a essayé (GPT Image, Manus, SaaS) ; le rendu relancé et chronométré (18 s) ; une bande des 8 slides parcourue par la caméra : voir `references/exemple-carrousels.md`.

## Prompt type

> Fais une vidéo YouTube de <ce qu'on a construit / l'artefact « … »> : un diaporama animé 16:9 qui montre comment j'obtiens ce résultat. Commence par me proposer le déroulé. Ouvre sur le problème, puis le titre avec la solution floutée en fond, puis le bénéfice. Ensuite, dans l'ordre qui sert le sujet : à quoi ça sert, pourquoi, pour qui, les méthodes fastidieuses et à la mode avec leurs plus et leurs moins (dont ce que j'ai essayé, au « je »), la solution, ce qu'elle facilite, puis le détail avec de vraies captures et des zooms. Un titre et une structure par slide, l'oral dira le reste. Appel à l'action en petit bandeau après « Pour qui », et complet à la fin.
