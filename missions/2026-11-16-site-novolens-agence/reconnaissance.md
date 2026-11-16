# Reconnaissance — site NOVOLENS (2026-11-16)

## Ce qui existe et se réutilise
- V1 (artefact privé XrX63oaT9QkR8Czv5SqjBL) et V2 (Wa6PwbDi2TBJ4L5hnhFJvz) : site multi-pages (accueil, pourquoi nous, comment ça marche, résultats, tarifs, FAQ, contact), 4 parcours animés (calibrage, prospection, qualification, rendez-vous), hero photo, fonds alternés (V2), titres serif gras avec surlignage jaune.
- Sources reproductibles dans `scratchpad/novolens/src` (build.py, story.py, ucards.py, style.css, app.js, style_v2.css, img/). Elles sont dans un dossier de session éphémère : la mission les recopie dans `livrables/site-src/` pour les pérenniser.
- Visuel de départ fourni par l'utilisateur (concept NOVOLENS) : charte violet/blanc, sections réalité, approche, livraison, témoignages, appel à l'action.
- Inspiration demandée : hatmada.io (animations, structure). Le site n'a pas pu être lu depuis cette session (aucune page trouvée par recherche) : on s'inspire des principes, on ne copie rien.

## Contraintes dures
- Français, thème clair uniquement, jamais sombre.
- Artefact Claude : scripts uniquement depuis cdnjs/jsdelivr/unpkg, polices Google Fonts, pas d'image externe (images embarquées comme fichiers), pas d'envoi réel de formulaire.
- Réseau : images.unsplash.com autorisé (ajouté à l'environnement). Vidéo générée, ElevenLabs et HeyGen non utilisables dans cette session (outils déconnectés ou désactivés).
- V1 et V2 ne sont jamais écrasées : la V3 est un nouvel artefact.

## Ce qu'on ignore
- Vrais chiffres, tarifs, témoignages, cas clients, nom légal, domaine, adresse e-mail.
- Pile d'hébergement visée (Cloudflare Pages est celle du dépôt, à confirmer).
- Ce que la référence hatmada.io propose réellement.

## Repères externes (recherche web, valeurs indicatives et à ne pas citer comme faits)
- Pages B2B : un objectif unique par page, formulaires courts (5 champs ou moins), cas détaillés plutôt que témoignages vagues, cohérence promesse/titre. Sources de blogs d'agences, sans méthodologie publiée.
- Prix agence : discovery séparée, contenu et photo/vidéo souvent exclus, 90 jours de support au niveau haut. Aucune source euro fiable trouvée.
