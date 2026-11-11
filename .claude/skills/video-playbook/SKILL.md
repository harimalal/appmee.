---
name: video-playbook
description: À déclencher dès que l'utilisateur envoie un lien YouTube (youtube.com/watch, youtu.be), même sans autre consigne, ou colle la transcription d'une vidéo. Transforme la vidéo (masterclass, interview, podcast) en masterclass transposable : carte interactive, une page par thème, méthode en éléments à définir illustrée pour quatre métiers, schémas et logigrammes, outils classés avec prix et alternatives, hacks avec disclaimer, pièges et limites, pépites, lexique avec définitions au survol. Livrable : une page web en plusieurs pages (artefact privé), sans PDF. Moteur fourni dans assets/.
---

# Video Playbook

Statut : **valide** (format v2 validé par Hari le 11/11/2026). Trois playbooks produits avec ce process : Fountain (agents IA), Trendtrack (SaaS rentable), SEO et GEO (Paul Vengeons, ChatSEO). Registre du cockpit : table `skills`, id `video-playbook`, projet `masterai`.

Le principe : on ne résume pas la vidéo, on en tire une **masterclass déployable**. Le cas de la vidéo sert d'exemple ; chaque mécanisme est ramené à des éléments génériques et transposé à n'importe quel métier, avec ses hacks, ses pièges et ses limites.

## Contenu du skill

| Fichier | Rôle |
|---|---|
| `assets/template.body.html` | Gabarit de toutes les pages et de tous les composants (carte, niveau, matrice, canevas, cases, recettes, tableaux, hacks, pépites, FAQ). Le copier, le remplir. |
| `assets/content.example.py` | Exemple de `content.py` : métadonnées, figures SVG, glossaire, chapitres, noms à vérifier, sources. |
| `assets/build.py` | Assemble le tout. Fournit aussi les aides SVG (`box`, `ar`, `pa`, `dia`, `pill`, `band`, `chain`, `T`, `fig`). |
| `assets/engine.css`, `assets/engine.js` | Moteur commun : style sombre à dégradé vert, routage des pages, sommaires, infobulles, mémoire locale. Ne pas modifier pour un playbook ; un outil propre va dans `extra.js`. |
| `assets/check.js` | Contrôle Playwright : erreurs console, infobulles par page, débordement à 400 px, captures. |
| `references/redaction.md` | Règles de rédaction page par page, avec les exemples des trois playbooks. **À lire avant d'écrire.** |

## Ce que Hari attend (décisions prises)

- **Public :** startups, builders IA, freelances, business en ligne, profils proches des intervenants. Rien sur les projets de Hari.
- **Format :** une page web découpée en pages (`#id`), chacune avec titre, sommaire « Sur cette page », page précédente / suivante. **Pas de PDF.**
- **Style :** dark mode, ombres, dégradé vert (fourni par le moteur).
- **À ne pas faire :** pas de chronologie de la vidéo, pas d'encart « limites de la source », pas de « retiré volontairement », pas de numérotation de sections (5, 5.1…).
- **Mise en page :** paragraphes pleine largeur ; recettes et takeaways sur **fond blanc** (`.box.how`).
- **Esprit pirate assumé :** évoquer tous les hacks de la vidéo, y compris borderline (scraping, achat de liens, manipulation de clics, appels sortants…). Les présenter comme des hacks, avec la version qui reste dans les clous et un court **disclaimer** (`.box.leg` + `.disc`), sans ton moralisateur ni « à ne pas reproduire ». Seule limite : pas de mode opératoire d'intrusion (accès à un système ou une base sans autorisation).
- **Outils interactifs** quand un calcul ou un réglage est au cœur de la méthode (calculateur « objectif de MRR → créateurs nécessaires », générateur de title avec compteur…).
- **Visuels :** beaucoup de schémas, logigrammes, workflows ; 8 à 12 figures par playbook.
- **Pépites :** 5 à 10, chacune avec « Demain ».
- **Lexique :** termes et sigles surlignés avec définition au survol (automatique) + une page Lexique.

## Récupérer le titre et la transcription

1. **Titre et chaîne :** `curl -s "https://www.youtube.com/oembed?url=<lien>&format=json"` (marche aussi depuis le cloud).
2. **Transcription :** un seul essai automatique, dans cet ordre selon l'environnement :
   - navigateur disponible (Claude in Chrome, navigateur intégré) : ouvrir la vidéo, « ··· » sous la vidéo puis « Afficher la transcription », copier le texte ;
   - sinon `pip install youtube-transcript-api` puis récupérer les langues `fr` puis `en`.
3. **Depuis le cloud Claude Code, YouTube bloque l'adresse IP** (« YouTube is blocking requests from your IP », yt-dlp « Sign in to confirm you're not a bot »). Ne pas contourner : ni proxy, ni cookies de compte.
4. **Si c'est bloqué**, demander dans le même message, sans attendre : coller la transcription, ou lancer le skill depuis un environnement local (Claude Code sur la machine, Cowork, navigateur).
5. Dès que le texte est là, tout lancer **sans redemander de « go »**.
6. Dernier recours, à signaler dans le livrable : playbook reconstruit à partir de sources publiques, moins fidèle.
7. Si la description de la vidéo contient des chapitres, les reprendre tels quels pour `CH`.

## Process

1. **Cadrer en une ligne** (mode hub) : objectif, livrable, critère de fin ; projet `masterai`, skill `video-playbook`. Pas de « go » à attendre : le format est validé.
2. **Lire et nettoyer la transcription :** séparer les voix, repérer les chapitres, relever avec leur horodatage les affirmations, chiffres, exemples, étapes, outils, hacks. Lister les noms mal transcrits (`VERIFY`).
3. **Étiqueter chaque information** par provenance :
   - `{V}` VIDÉO : dit dans la vidéo, toujours avec un horodatage `[[mm:ss]]` ou `[[h:mm:ss]]` ;
   - `{A}` APPROFONDI : ajouté par recherche web, avec la source dans `SRC` ;
   - `{O}` AVIS : analyse, exemple ou transposition construits pour le playbook ;
   - `{Q}` À VÉRIFIER : incertain, contradictoire, mal transcrit.
4. **Rechercher 5 à 8 sujets décisifs** (WebSearch, en parallèle) : prix actuels des outils cités, alternatives, chiffres ou études avancés dans la vidéo, cadre légal des hacks, identité des noms mal transcrits. Les prix des comparateurs divergent : donner la fourchette et `{Q}`, ne pas trancher.
5. **Vérifier les chiffres entre eux** (un revenu plus grand que le total, un pourcentage qui change en cours d'échange…) et signaler l'incohérence plutôt que la lisser.
6. **Plan :** 4 à 8 pages thématiques regroupées en 2 à 4 groupes (ex. « Comprendre », « Construire », « Accélérer »), plus les pages fixes (voir l'ordre ci-dessous). Une page par thème décisif, pas par chapitre de la vidéo.
7. **Écrire** dans un dossier de travail (dossier temporaire ou de brouillon, jamais un dossier publié) :
   - `body.html` copié depuis `assets/template.body.html` ;
   - `content.py` copié depuis `assets/content.example.py` ;
   - `extra.js` si un outil interactif est utile.
   Suivre `references/redaction.md`.
8. **Figures** dans `FIGURES()` : SVG en ligne avec les aides de `build.py`, un identifiant de marqueur unique par figure (`m = "s1"`, `"s2"`…), une description complète en `label`, une légende avec étiquette et horodatage. Logigramme quand il y a des décisions, chaîne pour un funnel ou un rituel, couches ou arbre pour une architecture, courbe « illustrative » pour une dynamique dans le temps (le dire dans la légende).
9. **Assembler :** `python3 assets/build.py <dossier>` → `playbook.artifact.html` (à publier) et `playbook.full.html` (à contrôler). Le script refuse de finir s'il reste un marqueur non remplacé, une figure manquante ou un texte du gabarit oublié (« … », « mois année », `VIDEO_ID`, « Titre… » : c'est arrivé sur le playbook Apify).
10. **Contrôler :** `node assets/check.js <dossier>` (Playwright ; en cloud Claude Code : `NODE_PATH=/opt/node-tools/node_modules`). Attendu : `erreurs []`, `debordement mobile {}`. Regarder la carte, deux figures et l'outil interactif sur les captures ; corriger les textes qui débordent des boîtes. Sans Playwright : ouvrir `playbook.full.html`, console sans erreur, largeur 400 px sans défilement horizontal.
11. **Publier** `playbook.artifact.html` en artefact privé (nouvel artefact par vidéo, icône d'un mot, description en une phrase).
12. **Cockpit** (`cockpit-db`) : `INSERT OR REPLACE INTO deliverables` (kind `artefact`, projet `masterai`, id = id de l'artefact) et une ligne `tasks` en `done` (`skill_id='video-playbook'`).
13. **Répondre à Hari en français**, court : le lien, le contenu (pages, figures, outil), les hacks traités, les points à vérifier.

## Ordre des pages

1. `accueil` : intro « ce que vous allez apprendre », carte interactive, « Comment lire » (légende seule), « Pour qui, et à quel niveau » avec graphique de niveau sur 10, ligne source.
2. Groupe **Déployer chez vous** : `methode` (méthode transposable), `plan` (30/60/90, rituel, cases à cocher).
3. Groupe **Comprendre** : `cas` (l'intervenant, le produit, outils et alternatives, ce qui se transpose ou non), éventuellement une page de stratégie.
4. Groupes thématiques : une page par thème décisif.
5. Groupe **Retenir** : `pepites`, `faq`, `lexique`, `sources`.

## Pièges techniques déjà rencontrés

- **Ne pas committer un playbook dans ce dépôt :** `wrangler.toml` publie tout le dépôt (`pages_build_output_dir = "."`). Le livrable reste dans un artefact privé et des fichiers non suivis (`playbooks/` est dans `.gitignore`). Seul le skill est commité.
- Dans Bash, éviter `${…}` et les gros heredocs contenant du JavaScript (le contrôle de sécurité les prend pour des suppressions) : écrire le fichier avec l'outil d'écriture, puis l'exécuter.
- Cloud Claude Code : `pip install` installe pour `python3.13` ; Playwright est dans `/opt/node-tools/node_modules`, Chromium déjà installé.
- Le moteur affiche la première page **après** avoir défini les infobulles ; si on modifie `engine.js`, garder l'appel `show()` à la fin.
- Pas de `padding` en pourcentage dans les barres ou étiquettes : débordement sur mobile.
- Les infobulles ne s'appliquent pas aux titres, liens, libellés de cases, cartes de la carte, ni aux sorties d'outil (`.calc-out`) : c'est voulu.
- Boîtes SVG : ≤ 22 caractères par ligne pour une boîte de 156 px, sinon le texte déborde. Vérifier sur les captures.
- Les commentaires HTML de `body.html` sont retirés à l'assemblage ; on peut y laisser des notes.
- Une f-string Python ne peut pas contenir de barre oblique inverse ni d'apostrophe du même type que ses guillemets : utiliser des guillemets doubles pour le français.

## Fin de tâche

- Cockpit : livrable ajouté, tâche en `done`, étapes de suite si Hari en demande.
- Deux phrases : ce qui a été fait, ce qui reste à vérifier.
