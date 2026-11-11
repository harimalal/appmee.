---
name: video-playbook
description: Transformer une vidéo YouTube dense (masterclass, interview, podcast) en playbook de type livre à reproduire : vue d'ensemble d'abord, sections thématiques, schémas et logigrammes, "comment faire", outils, prix et alternatives recherchés, questions de l'audience, pépites, lexique, plan d'action. Livrables : page web (artefact privé) et PDF. À utiliser quand l'utilisateur donne un lien YouTube et dit "fais-en un playbook", "deep dive", "reproductible", "résume en playbook", ou colle une transcription pour la même fin.
---

# Video Playbook

Statut du process : **draft** (à faire valider par Hari après un deuxième essai). Registre : table `skills` du cockpit, id `video-playbook`, projet `masterai`.

## Ce que Hari attend (décisions déjà prises)

- **Entrée :** une vidéo YouTube, sans que Hari la transcrive. Le texte doit être récupéré par Claude (voir ci-dessous).
- **Public visé :** startups, builders IA, freelances, business en ligne, profils proches de ceux des intervenants. **Rien à voir avec les projets de Hari** : ne pas ajouter d'encadrés « application à Reflexia / Dropit… » sauf demande explicite.
- **Fond :** rester fidèle au contenu de la vidéo, retirer l'inutile (sponsor, blagues, anecdotes sans valeur), et **approfondir ce qui est survolé** (comment faire, cas d'usage, outils, prix, alternatives, retours d'utilisateurs, ce qui aide à décider).
- **Structure :** toujours partir de la vue d'ensemble (carte), puis une partie par thème, en expliquant les liens entre thèmes. Vidéos longues ou morcelées : reconstruire l'arbre complet.
- **Répondre aux questions que l'audience se pose** (section FAQ).
- **Pépites :** 5 à 10 maximum, chacune avec un « à faire demain ».
- **Visuels :** schémas, logigrammes, illustrations, workflows visuels, au moins un par partie quand un mécanisme se montre mieux qu'il ne se dit.
- **Lexique :** un lexique des acronymes et un du jargon, définitions en une ligne, avec la partie où le terme apparaît.
- **Style (direction donnée, à ajuster) :** dark mode, ombres, dégradé vert. Sommaire latéral fixe, chapitres, mise en page de livre.
- **Format final :** page web (artefact privé) **et** PDF de la même mise en page.

## Récupérer la transcription (ordre à suivre)

1. Essayer depuis l'environnement : `youtube-transcript-api` (installé pour `python3.13`, pas `python3`) et `yt-dlp`. Les langues `fr` puis `en`.
2. **Constat du 11/11/2026 :** depuis le cloud Claude Code, YouTube répond 403 (adresse de datacenter). L'oEmbed (`/oembed?url=…`) répond bien et donne titre et chaîne. Ne pas contourner le refus.
3. Si 403 : demander à Hari de **coller la transcription** (sous la vidéo : « ··· » puis « Afficher la transcription »), ou de lancer le workflow dans une **session locale** où YouTube répond.
4. Piste à évaluer plus tard (non testée) : un petit Worker Cloudflare comme relais de transcription ; YouTube bloque aussi souvent ces IP, à vérifier avant d'y investir.
5. Dernier recours, à signaler clairement dans le livrable : playbook reconstruit à partir de sources publiques seulement (moins fidèle).

## Process

1. **Reformuler** (hub) : objectif, livrable, critère de fin ; projet `masterai`, skill `video-playbook` ; attendre un « go » sauf si tout est déjà cadré.
2. **Nettoyer la transcription :** séparer les voix, repérer les chapitres, lister les noms mal transcrits (annexe « à vérifier »), noter les passages inaudibles.
3. **Extraire** par thème : affirmations, chiffres, exemples, étapes. Tout est étiqueté par provenance :
   - `VIDÉO` dit dans la vidéo (avec horodatage cliquable `&t=…s`)
   - `APPROFONDI` ajouté par recherche web, avec sources et date de relevé
   - `AVIS` lecture de Claude
   - `À VÉRIFIER` incertain, contradictoire ou mal transcrit
4. **Choisir 5 à 8 sujets décisifs** et les rechercher (WebSearch « standard », en parallèle) : prix actuels, alternatives, retours d'utilisateurs, conformité si pertinent. Les prix des comparateurs divergent souvent : le dire, ne pas trancher.
5. **Plan du playbook :** vue d'ensemble (carte + tableau « qui alimente quoi »), contexte, une partie par thème (module : ce que dit la vidéo, comment le faire, schéma, outils et prix, pièges, FAQ de la partie), pépites, FAQ, plan 30/60/90, lexique, annexes (chapitrage, noms à vérifier, retiré volontairement, sources).
6. **Vérifier les chiffres entre eux** (ex. un revenu annoncé plus grand que le total) et signaler les incohérences plutôt que les lisser.
7. **Écrire** : ne jamais deviner le genre d'une personne (tournures neutres) ; ne pas inventer ce que la vidéo ne dit pas (ex. une réponse laissée sans réponse reste signalée comme telle).
8. **Schémas :** SVG en ligne, étiquettes sur les flèches, numérotation des figures automatique (compteur CSS). Logigramme quand il y a des décisions, chronologie pour un calendrier, couches pour une architecture.
9. **Construire** : un fichier source unique (gabarit), un script qui produit (a) le fragment pour l'artefact, (b) un HTML complet, (c) le PDF.
10. **Contrôler** : un coup d'œil au rendu (desktop sombre, mobile 400 px, PDF), débordements, console.
11. **Publier** l'artefact en privé, envoyer le PDF, enregistrer dans le cockpit (livrable, étapes de suite).

## Pièges techniques déjà rencontrés

- **Ne pas committer le playbook dans le dépôt.** `wrangler.toml` publie tout le dépôt (`pages_build_output_dir = "."`) : le HTML et le PDF dérivés d'un podcast deviendraient publics. Garder le livrable dans un artefact privé et en fichiers non suivis ; ne committer que ce skill.
- Playwright : module dans `/opt/node-tools/node_modules` (`NODE_PATH=/opt/node-tools/node_modules node script.js`). Chromium déjà installé.
- Dans les commandes Bash, éviter `${…}` (littéraux JavaScript) et les gros heredocs contenant du JavaScript : le contrôle de sécurité les prend pour des suppressions. Écrire le script avec l'outil d'écriture, puis l'exécuter.
- `pip install` installe pour `python3.13` ; `python3` est la 3.11.
- PDF : émuler le média `print`, ouvrir tous les `<details>`, `printBackground: true`, gabarit clair même si la page est sombre.
- Barres ou étiquettes avec `padding` en pourcentage : risque de débordement sur mobile ; tester à 400 px.

## Fin de tâche

- Cockpit : livrable ajouté (`deliverables`), étapes de suite (`steps`), tâche passée en `done`.
- Dire en deux phrases ce qui a été fait et ce qui reste à valider.
