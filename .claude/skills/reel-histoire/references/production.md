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

## Enseignements du 6e essai (reel « Mon site tourne à 0 € »)
- **Retours visuels de Hari, à appliquer d'office** : pages en **version ordinateur, pleine page**, dans une fenêtre qui occupe presque toute la hauteur (≈ 960 × 1 180 sur 1 080 × 1 920) — les captures mobiles sont jugées moches ; **marque en haut au milieu** ; **aucun texte au-dessus d'un autre** ; **mouvement de caméra (zoom, dézoom, glissement)** plutôt qu'apparition/disparition.
- **Règle vérifiable « pas de chevauchement »** : `qa.cjs` compare les boîtes de tous les textes visibles à chaque instant (marge 4 px) ; ignorer ce qui est hors cadre (scène qui entre ou sort) ; en plus, balayer toutes les 0,1 s (script `overlap.cjs` du scratchpad) : un seul chevauchement à 29,5 s a été trouvé ainsi (décalage d'entrée trop grand), corrigé en réduisant l'amplitude de l'étiquette.
- **Plafond de voix atteint en cours de journée** : `gemini-3.8-flash-lite-tts` (100 requêtes/jour) épuisé → basculer **tout** le reel sur `gemini-3.8-flash-tts` (le cache est lié au modèle : toutes les phrases sont régénérées, ≈ 20 requêtes) pour garder une voix homogène ; le dire à l'utilisateur.
- **Retour sur la voix « plus pêche »** : `tempo` global dans `story.json` (lu par `tts.py`) + `gap_sentence` à 0,08 s ; les instants de scène sont calculés sur la **durée parlée réelle** (`dv(phrase)`) et non plus sur des secondes fixes, pour que les images suivent le nouveau débit.
- **`hold`** (durée mini d'une phrase à l'image) lu par `plan.py` : laisse défiler une page pendant une phrase de 1 s.
- **Précharger les images** : `window.__ready` (images décodées) attendu par `render.cjs`, sinon des captures du début de rendu sont vides.
- **Image figée en fin de scène** : une scène qui a tout fait apparaître gèle ; ajouter un flottement léger (±3 à 7 px, compteur qui bat) dans les dernières secondes.
- **Sans musique (choix de Hari)** : `mix.py --sans-nappe` (voix + bruitages synchronisés) en fichier principal ; `--nappe 0.5` en variante. Ne pas synthétiser une « musique tendance » avec le moteur JS : sans droits vérifiés et peu convaincant ; l'utilisateur ajoute la sienne sur Instagram.
- **Dictée en vagues** : une retouche (CTA, mot retiré) ne régénère que les phrases changées (cache) ; relire l'ordre des scènes à chaque vague et recompter la durée.
- **Une mention de limite peut être levée par l'utilisateur** (« on s'en fous » pour « maquette ») : l'appliquer, **la garder dans `SCRIPT.md`** et la rappeler dans le message de livraison ; la vidéo ne doit simplement pas dire le contraire.

## Enseignements du 7e essai (reel « 28 comparatifs » v6)
- **Une consigne dictée du type « oublie l'instruction précédente, je préfère la version précédente » : demander de quelle vidéo et de quelle version on parle** avant de produire (ici : la v4 des comparatifs, supprimée par la règle « ne garde pas les anciennes versions »). Une version supprimée se reconstruit depuis git + le cache de voix, mais il vaut mieux **ne jamais écraser ni supprimer sans accord explicite** ; ranger les vidéos finales dans un dossier unique (`CONTENT/REELS_INSTAGRAM/`, noms standard `reel-instagram-reflexia-N.mp4`, `INDEX.md`).
- **Captures pour une démo plein cadre** : pages **entières** en version ordinateur (viewport 1 280 px, échelle 1,5, ≈ 10 000 px de haut : sous la limite de 16 384 px du navigateur), plus le **relevé des positions réelles** (en-têtes de colonnes, lignes, cartes, grilles : `getBoundingClientRect` + `scrollY`) dans un JSON qui pilote caméra, curseur et surbrillances. **Piège** : un tableau large défile horizontalement dans la page (colonnes cachées) ; pour le montrer, superposer une capture du tableau déplié dans un conteneur `overflow: hidden` qui glisse (swipe) au lieu de relever des colonnes invisibles.
- **Choisir la bonne rubrique** : les comparatifs (`format: "guide"`) sont dans `/guides/`, pas dans `/comparatifs/` (qui liste les autres articles).
- **Poids** : trois pages de 1 920 × 10 000 px, 4 workers : rendu ≈ 2,5 min pour 76 s ; fichier final ≈ 32 Mo (le double d'un reel à fenêtres) ; vérifier que le dépôt peut le porter.
- **Anti-gel** : un passage où la caméra est immobile entre deux clics est détecté comme image figée (curseur trop discret) : ajouter une légère dérive de caméra (zoom +0,05, glissement +40 px) entre les mêmes cibles.
- **Lisibilité** : l'étiquette sur page réelle exige un bandeau blanc **opaque** sur les ≈ 460 px du haut (le texte de la page passe derrière sinon) ; réduire la taille (44 px) des étiquettes longues pour qu'elles tiennent sur une ligne ; garder un bandeau doux seulement pour l'ouverture (zoom sur le titre de la page).
- **Registre** : voir `recit.md` (ton « ami », tempo 1,16, CTA à mot-clé) ; la v6 reprend le contenu de la v4 en le réécrivant, sans toucher aux affirmations.

## Enseignements du 8e essai (reels « 28 comparatifs » et « Mon site » v7)
- **Plus aucune surbrillance jaune** : l'élément cliqué **ressort vers l'avant** (`makePops` : calque soulevé + ombre + voile), la caméra zoome pour la lecture puis dézoome. Le jaune ne sert plus qu'au surligneur de texte des scènes graphiques.
- **Navigation continue** : pour une série de pages (accueil, article, comparatif, rubrique, page de vente, newsletter), une couche par page et **un clic par phrase** (menu, carte, bouton) plutôt qu'une fenêtre par type. L'en-tête réel (`Newsletter gratuite` sur l'accueil, `S'abonner →` ailleurs) reste visible sous la bande d'étiquette.
- **Les fonds ne se proposent pas sans demande** : Hari a rejeté six variantes de fond (« les fonds sont pourris, utilise les fonds actuels, on verra plus tard »). Garder les fonds du moteur ; n'en proposer d'autres que s'il le demande.
- **« Reviens sur la séquence précédente » = garder texte, ton, rythme et ordre des scènes, changer uniquement la mise en scène.** Le cache de voix permet alors un rendu à 0 requête facturée ; vérifier le compte dans `voice-report.json`.
- **Quota de voix** : le modèle « lite » plafonne à 100 requêtes par jour ; basculer sur `gemini-3.8-flash-tts` change légèrement la voix, le dire.
- **Transcription** : une formulation lue au passé par erreur (« l'écrit » → « l'a écrit ») se corrige par reformulation (« s'en charge sur mes instructions »), pas par relecture.
- **Une scène d'un reel « souris » non faisable proprement** (formulaire qui ne s'ouvre pas à la capture) : le dire et garder la scène graphique plutôt que livrer un montage bancal.

## Enseignements du 9e essai (reel « Mon site tourne à 0 € » v8 et v9)
- **Texte « flou » = étiquette sous le voile.** Quand une étiquette paraît grisée ou floue sur une page réelle, vérifier d'abord l'ordre d'empilement (`z-index`) avant de changer les polices : le voile blanc la recouvrait. Ensuite seulement : voile plus net sous la bande, sous-titre plus gros et plus foncé.
- **Une scène « autres solutions » se dit en une phrase** (« Il existe plein d'autres moyens de faire un site, mais là, on va bien plus vite ! ») : énumérer ce qu'on n'a pas à faire (serveur, extensions, hébergement…) a été jugé trop long. Cartes de gauche vite posées, une seule carte verte à droite. Règle : ne pas lister l'inventaire d'une comparaison, donner le sens.
- **Ordre du récit d'outils** : nommer le système (« le stack minimum »), puis **directement** le rôle de chaque outil, puis « et tout ça, c'est <outil de pilotage> qui le pilote, je lui parle normalement ». Ne pas énumérer les noms avant d'en donner le rôle.
- **Pas de décor abstrait pour un outil qu'on veut faire comprendre** : le terminal doit montrer du texte réel lisible (instruction naturelle + réponses), marqué « illustration » s'il s'agit d'un exemple et non d'un enregistrement.
- **Captures filtrées** : pour montrer qu'un filtre change le contenu, capturer **chaque état** par un vrai clic Playwright (`getByText(label, { exact: true }).click()`, attente 700 ms, capture pleine page recadrée) ; relever la position des filtres et de la première carte. Choisir le filtre dont la première carte mène à l'article déjà capturé (cohérence du clic final).
- **Couches qui se superposent pendant un zoom** : quand la caméra d'une page zoome et laisse un vide sur le côté, les couches précédentes réapparaissent. Les masquer (`opacity` à 0) dès que la couche du dessus est entièrement opaque ; raccourcir les fondus entre états filtrés (≈ 0,15 s) pour éviter le texte fantôme.
- **Dictée ambiguë et réponse courte** : « va rien changer, juste le début » = ne toucher qu'à la mise en scène d'une zone ; un message envoyé en cours de travail précise souvent *ce qui doit ressortir* (ici : les comparatifs par filtre). Quand deux fragments restent incompréhensibles, le dire et demander plutôt que de deviner.
- **Voix** : changer 3 phrases sur 23 = 3 requêtes facturées, le reste vient du cache ; prévoir de garder au maximum les phrases déjà validées.

## Enseignements des 10e et 11e essais (reels « Carousel Factory » et « Content Factory »)
- **Toujours mixer avec `--sans-nappe`** : le 1er envoi du reel n°7 contenait la nappe par oubli de l'option ; Hari l'a entendue (« tous les bruits sont trop forts »). Bruitages bas par défaut : `mix.py --sfx 0.3`, balayages de transition 0,3, swipes 0,2 (`synth.cjs`).
- **Montrer un système par ses vrais fichiers** : rendre fidèlement les fichiers de la chaîne (fiche, position, posts, sortie du contrôle) avec un générateur qui **lit** les fichiers et n'en réécrit aucun texte (`cards.py` + `cards.cjs`), puis animer ces rendus (lignes qui apparaissent, zoom, l'élément cliqué ressort). Le texte dans une image échappe au contrôle de mots : relire chaque rendu à l'œil.
- **Exemples hors dépôt** : des carrousels peuvent vivre dans des artefacts claude.ai (`Artifact list`/`read`) ; les rendre en PNG 1080×1350 avec Playwright, ne montrer que les slides sans bandeau « à fournir » ni tag « À vérifier ».
- **Zooms sur une carte pleine largeur** : au-delà de ×1,1 le texte sort du cadre à gauche ; préférer un zoom ×1,08-1,12 recentré, le « ressort » fait le reste.
- **Libellé en flex + surlignage** : un `<span class="hl">` dans une étiquette longue la coupe en colonnes ; garder l'étiquette courte (une ligne).
- **Mot banni « secret »** (contrôle qualité) : reformuler même un nom de modèle (« secret de fabrication » → « fabrication pas à pas ») et le dire.
- **Quotas voix** : 100 requêtes/jour par modèle (`gemini-3.8-flash-tts`, `gemini-3.8-flash-lite-tts`). Si les deux sont épuisés, générer **toute** la vidéo avec un même autre modèle (`gemini-3.1-flash-tts-preview`, qui renvoie du PCM brut `audio/l16` : `tts.py` ajoute l'en-tête WAV) plutôt que mélanger deux voix ; le dire à l'utilisateur.
- **Couverture « limite 3D »** : mur de vrais rendus en perspective CSS (`perspective`, `rotateX/Y`, `translateZ`), titre en haut sur fond net, bandeau sombre ; contrôler les recadrages 3:4 et 1:1.

