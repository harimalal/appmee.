---
name: video-playbook
description: À déclencher dès que l'utilisateur envoie un lien YouTube (youtube.com/watch, youtu.be), même sans autre consigne, ou colle la transcription d'une vidéo. Transforme la vidéo (masterclass, interview, podcast) en masterclass transposable : carte interactive, une page par thème, méthode en éléments à définir illustrée pour quatre métiers, schémas et logigrammes, outils classés avec prix et alternatives, pièges et limites, pépites, lexique avec définitions au survol. Livrable : une page web en plusieurs pages (artefact privé), sans PDF.
---

# Video Playbook

Statut du process : **draft** ; le format v2 a été validé par Hari le 11/11/2026 (« excellent »). Passer en `valide` après le deuxième playbook. Registre : table `skills` du cockpit, id `video-playbook`, projet `masterai`.

## Ce que Hari attend (décisions prises, v2 du 11/11/2026)

- **But :** passer d'une restitution à une **masterclass déployable**. Le cas de la vidéo sert d'exemple ; chaque mécanisme doit pouvoir être transposé à n'importe quel métier, objectif ou structure, avec ses pièges et ses limites.
- **Public :** startups, builders IA, freelances, business en ligne, profils proches des intervenants. Rien sur les projets de Hari.
- **Format :** une page web découpée en **pages** (routage par `#nom`), chacune avec son titre, un sommaire « Sur cette page », et des liens page précédente / suivante. **Pas de PDF.**
- **Accueil :** une introduction qui va droit au but et dit ce que le lecteur va apprendre. Ensuite une **vraie carte** : tous les thèmes en cartes groupées, chacune avec un résumé, un aperçu au survol, et un clic qui ouvre la page.
- **« Comment lire » :** seulement la légende des étiquettes, sans avertissements.
- **« Pour qui et à quel niveau » :** un public adapté au contenu, et un graphique de niveau sur 10 (stratégie, business, mindset, technique, organisation, ou d'autres axes pertinents). Critères explicites et une annotation par axe.
- **À ne pas faire :** pas de chronologie, pas d'encart « limites de la source », pas de « retiré volontairement », pas de numérotation (5, 5.1…).
- **Mise en page :** paragraphes sur toute la largeur. Encarts recette ou takeaway sur **fond blanc**.
- **Page « méthode transposable » :** les éléments génériques à définir (ex. objectif, signaux, machines, agents, gates humaines, mémoire, mesures, budget et rituel). Pour chacun, la question à se poser et des exemples dans quatre métiers types (freelance, e-commerce, startup SaaS, formation en ligne). Y ajouter une matrice de priorité et un canevas à remplir.
- **Chaque page thématique :** ce que fait le cas étudié, des schémas, une recette sur fond blanc, un tableau « Transposer à votre métier », les outils, et « Pièges et limites ».
- **Outils et alternatives :** les classer par famille et dire en langage courant à quoi sert chaque famille et chaque outil.
- **Termes techniques et acronymes :** surlignés, avec la définition au survol, générée automatiquement à partir du lexique. Il faut aussi une page Lexique.
- **Pépites :** 5 à 10 maximum, chacune avec un « à faire demain ».
- **Visuels :** schémas, logigrammes, illustrations et workflows visuels dès qu'un mécanisme se montre mieux qu'il ne se dit.
- **Style :** dark mode, ombres, dégradé vert.

## Récupérer le titre et la transcription

1. **Titre et chaîne : automatique.** `curl "https://www.youtube.com/oembed?url=<lien>&format=json"` fonctionne depuis le cloud.
2. **Transcription : un seul essai automatique**, avec `python3.13` et `youtube-transcript-api` (langues `fr` puis `en`). En cas d'échec, ne pas insister.
3. **Constat du 11/11/2026 :** depuis le cloud Claude Code, YouTube bloque l'adresse IP. La bibliothèque répond « YouTube is blocking requests from your IP » et yt-dlp « Sign in to confirm you're not a bot ». Ne pas contourner : ni proxy, ni cookies de compte.
4. **Si c'est bloqué**, demander dans le même message, sans attendre :
   - soit de coller la transcription (sous la vidéo : « ··· » puis « Afficher la transcription ») ;
   - soit de lancer le skill dans une session Claude Code sur la machine de Hari, où YouTube répond normalement.
5. Dès que le texte est là, lancer tout le process **sans redemander de « go »**. Le format est validé (v2).
6. **Dernier recours**, à signaler dans le livrable : un playbook reconstruit à partir de sources publiques seulement, donc moins fidèle.

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
9. **Construire** : un fichier de contenu (pages), une feuille de style, un script (routage, sommaires, infobulles, mémoire locale), et un script d'assemblage qui produit le fragment pour l'artefact et un HTML complet.
10. **Contrôler** : un coup d'œil au rendu (carte, une page, infobulle), puis console sans erreur et pas de débordement à 400 px sur chaque page.
11. **Publier** l'artefact en privé, puis l'enregistrer dans le cockpit (livrable, étapes de suite).

## Pièges techniques déjà rencontrés

- **Ne pas committer le playbook dans le dépôt.** `wrangler.toml` publie tout le dépôt (`pages_build_output_dir = "."`) : le HTML et le PDF dérivés d'un podcast deviendraient publics. Garder le livrable dans un artefact privé et en fichiers non suivis ; ne committer que ce skill.
- Playwright : module dans `/opt/node-tools/node_modules` (`NODE_PATH=/opt/node-tools/node_modules node script.js`). Chromium déjà installé.
- Dans les commandes Bash, éviter `${…}` (littéraux JavaScript) et les gros heredocs contenant du JavaScript : le contrôle de sécurité les prend pour des suppressions. Écrire le script avec l'outil d'écriture, puis l'exécuter.
- `pip install` installe pour `python3.13` ; `python3` est la 3.11.
- Script de page : appeler l'affichage de la première page **après** avoir défini le moteur d'infobulles, sinon il plante.
- Barres ou étiquettes avec `padding` en pourcentage : risque de débordement sur mobile ; tester à 400 px.

## Fin de tâche

- Cockpit : livrable ajouté (`deliverables`), étapes de suite (`steps`), tâche passée en `done`.
- Dire en deux phrases ce qui a été fait et ce qui reste à valider.
