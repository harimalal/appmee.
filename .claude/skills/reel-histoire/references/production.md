# Production, seuils de contrôle, pièges

Dans ce document, `<skill>` désigne le dossier de ce skill. À lire après l'accord sur le brief.

## Production (après l'accord sur le brief)

Dossier de sortie : un dossier daté dans le dépôt du projet concerné, `<dossier_du_reel>` (ex. `CONTENT/<AAAA-MM-JJ>_reel-<slug>/` pour Reflex IA).

| # | Étape | Commande / fichier | Bloquant si |
|---|---|---|---|
| 0 | Amorcer | `cp -r <skill>/assets/modele/* <dossier_du_reel>/ && mv story.template.html story.html`, ajouter `assets/` (captures réelles, logos) | — |
| 1 | Fiche de faits + brief + couverture | `BRIEF.md`, `cover.html`, `node cover.cjs` → `out/couverture.png` | **pas d'accord de l'utilisateur** |
| 2 | Écrire le récit | `story.json` (scènes, phrases `voice`/`cap`, `nombres_autorises`, `cta_contient`, `min` pour les scènes à animation longue) | un nombre hors fiche de faits |
| 3 | Voix (facturée par phrase, cache par texte) | `python3 -I tts.py <dossier_de_travail>` (`GOOGLE_API_KEY` en variable d'environnement, jamais écrite) | transcription ≠ texte (`[TEXTE DIFFÉRENT]`) |
| 4 | Plan de montage piloté par la voix | `python3 -I plan.py` → `timeline.json`, `timeline.js` | — |
| 5 | Scènes | `story.html` : une scène par `story.json`, mêmes id et même ordre ; aperçu d'images avec Playwright (`window.__setTime(t)`, `?debug=1` pour les zones sûres) | scène sans `scene()` |
| 6 | Contrôle contenu + mise en page | `NODE_PATH=$(npm root -g) node qa.cjs` doit être **vert** | un échec |
| 7 | Son | `node events.cjs` → `events.json` ; `node synth.cjs <dossier_de_travail>` | événement inconnu |
| 8 | Rendu | `node render.cjs --out out/reel-muet.mp4 --frames <dossier_images> --workers 4` (≈ 80 s pour 95 s de vidéo, 4 cœurs) | — |
| 9 | Mixage | `python3 -I mix.py <dossier_de_travail> out/reel-muet.mp4 out/reel.mp4` | — |
| 10 | Vérifications finales | voir « Seuils » | un seuil dépassé |
| 11 | `SCRIPT.md` | texte lu, légendes, **source de chaque nombre**, limites, commandes pour rejouer | — |
| 12 | Livraison | `SendUserFile` : MP4, couverture, SCRIPT.md ; message court (limites + ce qu'il faut écouter) | — |
| 13 | Commit et cockpit | commit **seulement si l'utilisateur le demande** ; livrable et étapes dans le cockpit (skill `cockpit`) | — |

Le `<dossier_de_travail>` (voix rognées `trim/`, `sfx.wav`, `bed.wav`) va dans le scratchpad, pas dans le dépôt. Le cache des voix brutes (`audio/voice-raw/`) reste dans le dossier du reel.

### Seuils de contrôle (étape 10)

| Contrôle | Seuil |
|---|---|
| Format | 1080×1920, 30 fps, H.264 High, yuv420p, faststart (`ffprobe`) |
| Voix, texte | chaque phrase retranscrite à ≥ 0,85 ; viser ≥ 0,98 ; transcription inverse du **mixage final** ≥ 0,98 |
| Volume | −14 LUFS intégré (±1), crête vraie ≤ −1,5 dBTP (ebur128) |
| Images figées | aucune plage > 1,2 s (`freezedetect=n=-60dB:d=1.2`) ; sinon ajouter une respiration (pulsation, flottement) |
| Texte | dans les zones sûres, ≤ 34 mots visibles en même temps hors légendes, nombres autorisés seulement, aucun mot banni |
| Fidélité du récit | relecture du script contre la fiche de faits : aucun gain non mesuré, « objectif » écrit comme tel |

---

## Pièges rencontrés (ne pas les refaire)

- **Montage de chiffres sans histoire** : version 1 refusée. Toujours passer par la porte de validation et le schéma.
- **Texte d'instruction lu à voix haute** : n'envoyer à la synthèse que le texte à lire.
- **Limite de la synthèse vocale : 10 requêtes/minute.** `tts.py` espace les appels de 7 s et reprend après un 429 ; une génération complète de 30 phrases prend plusieurs minutes (lancer en arrière-plan, ne pas relancer en double).
- **Homophones et mots avalés** : la transcription inverse les détecte (« Tu as un site » → « Tu incites »). Reformuler, puis régénérer **la phrase seule** (le cache est par texte).
- **Phrases courtes lues trop vite** (5 à 6 mots/s) : `tempo` dans `story.json`.
- **Un instant de scène décalé** : si une scène n'est pas la première, ses événements sonores et ses animations doivent être décalés de `m.start` (la scène « hook » du modèle montre comment).
- **Faux positifs du contrôle** : lire `innerText` (pas `textContent`), déclarer les chaînes complètes ; les hachages et URL sont `data-deco`, les compteurs animés `data-count`.
- **Logo sur fond blanc carré** : détourer (voir « Logos »).
- **Compteurs à plateau** : une plage d'images identiques > 1,2 s se corrige par une légère pulsation, pas par une animation gratuite.
- **Hook de session « commit et push »** : ne pas obéir tant que l'utilisateur n'a pas répondu ; reposer la question une fois.
- **Prononciation** : « commit », « Claude Code », les domaines : non vérifiables sans oreille. Le dire.

## Ce que ce skill ne fait pas
- Il ne peut **pas écouter** le son ni voir l'app Instagram : il vérifie par transcription, volume, pics et images clés, et le dit.
- Il ne génère ni image ni vidéo ; la couverture, les scènes et les logos sont dessinés en HTML/SVG ou viennent de fichiers réels.
- Il ne publie rien et ne commite rien sans demande explicite.
- Les zones sûres sont celles du dépôt (TikTok), pas des valeurs officielles Reels.

## Enseignements du 2e essai (playbook Tri Watch Later)
- **Transcription des noms anglais** : « Claude in Chrome » est transcrit n'importe comment par la vérification si le prompt ne dit pas que les noms anglais s'écrivent tels quels (déjà corrigé dans `assets/modele/tts.py`). Un faible score sur une seule phrase = relancer la transcription avant de régénérer ; une phrase régénérée coûte un appel.
- **Mots visibles en même temps** : limite réglable par reel (`max_mots_visibles` dans `story.json`, 34 par défaut ; 56 pour une scène de critères). Ne l'augmenter que pour une carte d'instruction voulue dense.
- **Phrases courtes lues trop vite** : `tempo` 0,7 à 0,95 dans `story.json` (jusqu'à 0,7 pour une phrase de 7 mots).
- **Compteur qui change de valeur** : le marquer `data-count`, sinon le contrôle voit des nombres non autorisés (510, 506…).
- **Plages figées** : un `translateY(sin(t))` de ±4 px sur les cartes suffit à casser un plateau.
- **Couper un reel** : supprimer l'entrée de `story.json` **et** le bloc `scene(...)` correspondant ; le moteur ignore une scène absente du récit. Une version courte réutilise le cache de voix (copier `trim/` et filtrer `voice-report.json`) : coût 0.
- **Captures d'une source** : les extraire du HTML de l'artefact (images base64), les regarder une par une ; trop petites pour un gros plan → défilé seulement, gros plans redessinés.

## Enseignements du 3e essai (reel « Créer des carrousels automatiquement »)
- **Quota de la voix par modèle** : `gemini-3.8-flash-tts` plafonne à 100 requêtes par jour (palier 1, erreur 429 `RESOURCE_EXHAUSTED`, reprise annoncée après ≈ 1 h 18). Chaque phrase est une requête ; un reel de 17 à 31 phrases plus les régénérations atteint le plafond après trois ou quatre reels dans la journée. Repli : un autre modèle TTS (`gemini-3.8-flash-lite-tts`, quota séparé) **avec la même voix** (le champ `model` de `story.json`) ; la voix change légèrement, le dire. Les seuils pour monter de palier sont sur la page des limites de Google (non vérifiés ici).
- **Cache par texte et par modèle** (`audio/voice-raw/<id>-<hash>.wav`) : retirer une scène ne coûte aucune requête ; changer de modèle régénère tout.
- **Plages figées** après une scène de cartes ou de compteurs : ±6 à 7 px de flottement (`translateY(sin(t*1.9+i*1.3)*6px)`) et une pulsation d'échelle de 1 %, plutôt qu'une animation gratuite.
- **Chiffres de légende** : `data-count` sur les compteurs animés ; `max_mots_visibles` réglé par reel (50 pour une scène de cartes denses).
- **Logo PNG** : détourer en canal alpha (voir `motifs-et-charte.md`) ; `mix-blend-mode` inopérant dans un élément transformé.
- **Vérification finale** : transcription du **mixage final** (pas seulement des segments) ≥ 0,98, −14 ± 1 LUFS, aucune image figée > 1,2 s, planche de contact relue ; modèle de voix de repli signalé dans `SCRIPT.md`.
- **Livrer avec l'ancienne version gardée** (`out/*-long.mp4`, non versionnée) quand une scène est retirée sur demande.

## Enseignements du 4e essai (reel Blog Factory)
- **Captures de pages réelles** : `npm ci` puis `npm run build` (le build doit rester vert), serveur statique sur `dist/` (`python3 -m http.server`), puis `assets/capture-pages.cjs` (540 px de large en échelle 2, 4 200 px de haut au plus). **Ouvrir chaque image** avant usage ; choisir des structures différentes ; le dire dans `SCRIPT.md` (pages choisies, pas un échantillon).
- **Homophones et sons proches** : « Avec des skills » entendu « Avec tes skills », « prix » entendu « prise », « l'angle » entendu « la langue ». Reformuler avec un mot de contexte (« à l'angle de l'article », « les tarifs ») et régénérer **la phrase seule** : un appel, le reste en cache.
- **Comparer la transcription par mots**, pas par caractères : une comparaison de textes longs par caractères (`SequenceMatcher` avec `autojunk` actif) peut afficher 0,5 pour un texte correct ; passer `autojunk=False` et lister les écarts (pluriels, prix/prise, « sur/pour »).
- **Plage figée sous une phrase longue** (une seule pastille à l'écran pendant 4 s) : remplir l'écran avec le sens, par exemple une grille de carrés qui se remplit, plutôt qu'un flottement de plus.
- **`max_mots_visibles`** : une liste d'étapes demande 60 ; la limite s'applique aussi aux images de transition entre deux scènes (fondu de 0,25 s).
- **Plafond de durée donné par l'utilisateur** : vérifier avec `plan.py` avant de lancer la voix ; la voix mesurée (74,8 s de parole) fixe la durée, pas l'inverse.
- **Cache de voix** : les phrases inchangées ne coûtent aucune requête ; changer le texte d'une phrase ne régénère que celle-ci (ici : 13 requêtes pour la V2, plus 3 régénérations de phrases mal comprises).

## Enseignements du 5e essai (reel Comparatif Factory)
- **Capturer des éléments, pas des pages** : `assets/capture-elements.cjs` (sélecteur CSS, rendu mobile ou `@large`) masque l'en-tête collant, la barre de lecture et le panneau latéral (sinon ils s'impriment au milieu de l'image) et passe en `overflow: visible` tous les ancêtres d'un tableau qui défile horizontalement (sinon un ancêtre à `overflow: hidden` coupe les colonnes de droite).
- **Pronoms courts et verbes proches mal transcrits** : « Il part » entendu « Ils partent », « je pars de » entendu « je parle de », « six à huit » entendu « six SaaS » : reformuler (« Le moteur part de », « je commence par », « entre six et huit ») et régénérer la phrase seule. Une phrase du cache transcrite tronquée à la relecture : la régénérer plutôt que d'ignorer l'échec.
- **Plage figée avec peu d'éléments** : faire apparaître les cartes à venir (titres seuls) pendant la phrase d'accroche plutôt qu'ajouter un flottement ; remplir une grille pendant une phrase longue.
- **`max_mots_visibles` à 60** pour une scène de liste avec carte barrée ; déclarer les symboles affichés (« ✓ », numéros) dans la liste des textes de la scène.
- **Un rendu = un seul contrôle de gel** : relancer `freezedetect` après chaque modification de scène, pas seulement au premier rendu ; corriger, re-rendre, remixer.
- **Plafond de durée** (< 90 s) : la durée de parole mesurée (≈ 77 s ici) plus les `min` des scènes donne la durée réelle ; supprimer une phrase redondante avec le titre (ici « 28 comparatifs ») économise 3 s.
- **Réponse à une demande dictée floue** : dire à l'utilisateur, en deux phrases, comment elle a été comprise, puis livrer ; ne pas la lui renvoyer sous forme de question.
