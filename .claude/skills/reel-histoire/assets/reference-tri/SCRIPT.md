# Reel « histoire » — Trier 511 vidéos YouTube avec Claude in Chrome (script, sources, limites)

Format 1080×1920 (9:16), 30 fps, **116 s**, voix Google (Gemini TTS, voix Charon) + bruitages et nappe synthétisés localement. Skill : `reel-histoire` (dépôt appmee, branche `claude/skill-reel-histoire`). Source : artefact « Playbook Tri Watch Later » (https://claude.ai/artifact/B3dPBeKF3FjrDjijQjATco, 15/11/2026). Aucune image ni vidéo générée : motion design HTML rendu par Chromium ; les images de défilé sont les **17 vraies captures** du playbook.

## Le récit
1. **Problème (0–13 s)** : « Comment trier 511 vidéos YouTube avec Claude in Chrome ? En environ quinze minutes, avec mes propres critères. » puis « Ta liste déborde ? Ce n'est pas un problème de temps, c'est un problème de tri. »
2. **Situation (13–19 s)** : 585 vidéos annoncées, 511 chargées (défilé des vraies captures).
3. **Solution (19–51 s)** : mes critères (supprimer / garder), puis pourquoi l'extension Chrome.
4. **Process (51–90 s)** : six étapes, suppression une par une puis accélérée, deux pièges.
5. **Résultat (90–109 s)** : 511 → 48, ≈ 90 %, ≈ 15 min ; limites. **CTA (109–116 s)** : « Abonne-toi pour plus d'astuces IA… », puis « Et ta liste ? » qui reboucle sur le titre.

## Voix et légendes (instants mesurés)
| t (s) | scène | voix (texte lu) | légende |
|---|---|---|---|
| 0.1 | titre | Comment trier cinq cent onze vidéos YouTube avec Claude in Chrome ? | (visuel porte le texte) |
| 3.7 | titre | En environ quinze minutes, avec mes propres critères. | (visuel porte le texte) |
| 6.9 | probleme | Ta liste « À regarder plus tard » déborde ? | Ta liste « À regarder plus tard » déborde ? |
| 9.3 | probleme | Ce n'est pas un problème de temps. | Ce n'est pas un problème de temps. |
| 11.2 | probleme | C'est un problème de tri. | C'est un problème de tri. |
| 12.8 | hook | La mienne : cinq cent quatre-vingt-cinq vidéos annoncées. | (visuel porte le texte) |
| 16.0 | hook | Cinq cent onze chargées dans la page. | (visuel porte le texte) |
| 18.8 | criteres | Je lui donne mes critères. | Je lui donne mes critères. |
| 20.3 | criteres | À supprimer : les mangas, les vidéos de moins de dix minutes, tout ce qui sort de l'IA et du business. | À supprimer : les mangas, les vidéos de moins de 10 minutes, tout ce qui sort de l'IA et du business. |
| 27.1 | criteres | Les titres putaclic, les revues de personnalités, les tutos d'outils. | Les titres putaclic, les revues de personnalités, les tutos d'outils. |
| 32.1 | criteres | À garder : les formations, les startups, les SaaS, et les vidéos de plus de quarante minutes sur Claude Code. | À garder : les formations, les startups, les SaaS, et les vidéos de plus de 40 minutes sur Claude Code. |
| 39.1 | extension | Pourquoi l'extension Chrome, plutôt que Claude Code ou Claude Cowork ? | Pourquoi l'extension Chrome, plutôt que Claude Code ou Claude Cowork ? |
| 43.5 | extension | Parce que le tri se fait dans la page YouTube elle-même. | Parce que le tri se fait dans la page YouTube elle-même. |
| 46.2 | extension | L'extension travaille dans mon onglet, déjà connecté : aucun mot de passe à donner. | L'extension travaille dans mon onglet, déjà connecté : aucun mot de passe à donner. |
| 51.4 | methode | La méthode tient en six étapes : ouvrir, charger, extraire, classer, supprimer, documenter. | (visuel porte le texte) |
| 59.0 | methode | Il fait défiler toute la liste, puis relève le titre, la chaîne et la durée de chaque vidéo. | (visuel porte le texte) |
| 65.1 | methode | Il classe avec une règle pour la durée et des mots-clés pour les thèmes, et je relis ce qu’il garde. | (visuel porte le texte) |
| 70.9 | suppression | Ensuite, il supprime en boucle : le menu, puis « Supprimer de À regarder plus tard ». | (visuel porte le texte) |
| 76.4 | suppression | Un geste toutes les quatre cents millisecondes environ. Ici, accéléré. | (visuel porte le texte) |
| 80.9 | pieges | Deux pièges. Une boucle de quarante suppressions dépasse le délai de l'outil : je la lance en tâche de fond. | Deux pièges. Une boucle de 40 suppressions dépasse le délai de l’outil : je la lance en tâche de fond. |
| 86.8 | pieges | Et les très longues listes sont coupées : je les lis par petits lots. | Et les très longues listes sont coupées : je les lis par petits lots. |
| 90.4 | resultat | Résultat : de cinq cent onze à quarante-huit vidéos. | (visuel porte le texte) |
| 94.1 | resultat | Environ quatre-vingt-dix pour cent supprimées automatiquement, en une quinzaine de minutes. | (visuel porte le texte) |
| 99.7 | limites | Les limites : soixante-quatorze vidéos jamais chargées, et un classement qui reste subjectif. | Les limites : 74 vidéos jamais chargées, et un classement qui reste subjectif. |
| 105.8 | limites | Et retirer une vidéo de la liste ne la supprime pas de YouTube. | Et retirer une vidéo de la liste ne la supprime pas de YouTube. |
| 109.5 | cta | Abonne-toi pour plus d'astuces IA : sans compétences techniques, rapides, et terriblement efficaces. | (visuel porte le texte) |

## Sources de chaque nombre (page du playbook)
511 (vidéos chargées) · 585 (annoncées) · 74 (non chargées, tableau des pièges) · 48 (conservées) · ≈ 90 % (supprimées automatiquement) · ≈ 15 min · 10 min et 40 min (seuils des critères) · 6 (étapes) · 40 (suppressions par boucle) · 350 à 450 ms (pause entre gestes) · 20 à 25 (titres par lot). Les « ≈ » sont ceux de la source. Statut : tous « mesurés » dans le playbook, sauf les seuils, qui sont des règles choisies.

## Ce que la vidéo montre exactement (et ce qu'elle ne montre pas)
- **« Mes critères »** : les critères du playbook (supprimer : mangas et animés, moins de 10 minutes, hors IA et business, titres putaclic, revues de personnalités, tutos d'outils ; garder : formations, startups, SaaS, plus de 40 minutes sur Claude Code). Le playbook ne contient pas le texte exact du prompt : la carte affiche des **critères**, pas une citation. (« Interviews sur le parcours d'une personne » figure dans le playbook mais pas dans la vidéo.)
- **« Pourquoi l'extension »** : Claude Code et Claude Cowork sont indiqués « pas utilisé pour ce tri » ; seul ce que le playbook établit est dit de l'extension (travaille dans l'onglet YouTube déjà connecté, aucun mot de passe). **Aucune affirmation sur ce que Claude Code ou Cowork savent ou ne savent pas faire.**
- **Suppression accélérée** : le rythme réel est une pause de 350 à 450 ms entre deux gestes ; la vidéo le montre d'abord au rythme réel puis **accéléré**, étiqueté « accéléré » à l'écran et dit à la voix. Les lignes sont **redessinées** (aucun titre de vidéo), pas des captures.
- **Défilé** : vraies captures du playbook (432×276 px, titres de vidéos visibles, choix assumé) ; floutées par le mouvement, jamais en gros plan (trop petites).
- « ≈ 90 % supprimées automatiquement » : la liste à conserver a été relue à la main (dit dans la voix, scène méthode).
- 511 → 48 vaut pour les 511 vidéos chargées ; 74 sur 585 n'ont pas été traitées (scène limites). Retirer de la liste ne supprime pas la vidéo de YouTube.

## Points à connaître
- **CTA** : « sans compétences techniques, rapides, et terriblement efficaces » est la formulation de Hari ; « terriblement efficaces » est une promesse que ce reel ne prouve pas.
- **Logo** : étoile Claude du dépôt, pas le logo officiel de l'extension Claude in Chrome.
- **Durée** : 116 s, plus que les ≈ 80 s annoncés (instruction, pourquoi l'extension et suppression accélérée ajoutées à la demande). Coupes possibles : détail des étapes (m2, m3), pièges (g1, g2).
- Quelques phrases courtes sont ralenties de 10 à 30 % (`tempo` dans `story.json`).

## Vérifications faites / limites
Contrôle `qa.cjs` vert (zones sûres, texte déclaré, nombres autorisés, mots bannis) ; transcription inverse de chaque phrase puis du mixage final ; −14 LUFS, crête ≤ −1,5 dBTP ; H.264 High, yuv420p, faststart. **Non vérifié** : le son à l'oreille, la prononciation (« Claude in Chrome », « SaaS »), le rendu dans l'app Instagram ; zones sûres = valeurs TikTok du dépôt, non officielles pour Reels.

## Rejouer
`python3 -I tts.py <travail>` · `python3 -I plan.py` · `NODE_PATH=$(npm root -g) node qa.cjs` · `node events.cjs` · `node synth.cjs <travail>` · `node render.cjs --out out/reel-muet.mp4 --frames <images>` · `python3 -I mix.py <travail> out/reel-muet.mp4 out/reel.mp4`
