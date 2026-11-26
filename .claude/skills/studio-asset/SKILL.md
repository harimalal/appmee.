---
name: studio-asset
description: Studio de lancement d'application (web ou mobile) — crée, à partir des vraies captures de l'app et des mots de sa landing, tous les contenus pour la montrer et la lancer, à la carte ou en package complet, aux formats de chaque réseau. Film de lancement animé avec scénario, storyboard, voix off ElevenLabs et sous-titres ; vidéos de 6 s à 2 min en 16:9, 9:16, 1:1, 4:5 ; diaporamas animés avec transitions ; diaporamas statiques et carrousels (images + PDF LinkedIn) ; posts image ; galerie et vignette Product Hunt ; miniature YouTube ; image de partage ; captures de stores. Utilise ce skill dès que l'utilisateur veut montrer, présenter, promouvoir ou lancer une app ou un SaaS en images ou en vidéo — « une vidéo comme celle de Dropit », « un carrousel LinkedIn de mon app », « des visuels Instagram », « un reel », « un post pour annoncer la fonctionnalité X », « une démo animée », « tout le package réseaux » — même sans nommer le format.
---

# Studio de lancement d'application

Ce skill fabrique tout ce qui sert à **montrer une application** : du post unique au package complet de lancement, en passant par le film animé avec voix off. Il est né du lancement Product Hunt de Dropit (octobre 2026) ; l'exemple complet est dans `references/exemple-dropit.md`.

Trois idées tiennent l'ensemble :
- **Le vrai produit** : de vraies captures de l'app (jouées dans un navigateur pour une app web, fournies pour une app mobile) et de vraies photos, jamais des maquettes redessinées ni des illustrations.
- **Les mots de la landing** : promesse, valeur unique, slogan et bénéfices sont repris tels quels, pour que chaque contenu dise la même chose que la page où il envoie.
- **Tout est calculé, rien n'est filmé** : chaque visuel est une page HTML, chaque animation une fonction du temps `render(t)`, rendue image par image puis encodée avec ffmpeg. Un retour de l'utilisateur se corrige au dixième de seconde près et tout se rejoue quand l'app change.

## Prérequis
- Node + Playwright (Chromium), ffmpeg : vérifier au début (`NODE_PATH=$(npm root -g) node -e "require('playwright')"`, `ffmpeg -version`).
- Voix off et transcription : connecteur ElevenLabs (outils `creative_*`). Sans lui, tout reste faisable sans voix ; proposer de le connecter.
- Dans ce document, `<skill>` désigne le dossier de ce skill.

## 1. Le socle (commun à toutes les commandes, fait une fois par app)

Le socle vit dans un dossier versionné du projet de l'app (ex. `MISSIONS/<date>-lancement/` ou `showcase/`) :
```
brief.md        fiche d'entrée           captures/     écrans de l'app + boites.json + saisie/
storyboard.md   récit (vidéos)           medias/       photos réelles, logo, polices
sortie/         livrables, rangés par usage (video/, instagram/, linkedin/, x/, product-hunt/, web/, stores/, textes/)
```
S'il existe déjà (une commande précédente), le relire et le réutiliser : ne refais pas les captures ni le brief pour un nouveau post.

**a. Fiche d'entrée.** Copie `assets/brief-modele.md` en `brief.md` et remplis-la **toi-même d'abord** : lis la landing en entier, le dépôt, le README, les captures fournies, la conversation. Pose ensuite seulement ce qui manque, groupé (AskUserQuestion, 4 questions au plus par vague, option recommandée en premier). À confirmer presque toujours : marché et langue, personnage et cas de démonstration, fonctionnalités à montrer, formats et réseaux visés, voix. Ne demande jamais ce que la landing ou le code disent déjà : propose ta lecture et fais-la valider.

**b. Mots de la landing.** Recopie mot pour mot dans le brief : titre, sous-titre, valeur unique, slogan, contraste avec les alternatives, noms des fonctionnalités, appel à l'action, réassurance. Voir `references/recit.md` pour le passage de la landing aux textes.

**c. Captures.**
- *App web* : script de capture à partir de `scripts/capture-web-modele.cjs` (vraie app au format téléphone 390×844 ×3, réseau remplacé par des données de démonstration, IA simulée avec des réponses écrites pour l'occasion, hasard fixé, saisie lettre par lettre, positions des éléments dans `captures/boites.json`).
- *App mobile native* : demander la liste exacte des captures (une par état, nommées dans l'ordre, même appareil, mêmes données de démo), les normaliser (`scripts/normaliser-captures.sh`), mesurer les zones à animer avec `scripts/quadrillage.cjs`.
- *Photos* : réelles (app, landing, banque libre de droits si le réseau le permet). *Marque* : logo (en morceaux si on l'anime), polices locales, couleurs → `medias/`.

## 2. Les commandes

L'utilisateur peut demander une seule chose (« un carrousel LinkedIn sur la fonctionnalité X ») ou tout le package. Identifie la commande, vérifie que le socle existe (sinon fais-le, en version minimale pour la commande), puis suis sa recette. Formats et durées par réseau : `references/formats.md`. Règles de composition : `references/visuels.md`.

| Commande | Outil | Sortie |
|---|---|---|
| Post image (un message, un ou plusieurs formats) | `assets/diaporama-modele.html`, 1 diapositive | `rendre.cjs --format WxH diapos` → JPEG/PNG par format |
| Carrousel (Instagram, LinkedIn) | diaporama, 5 à 10 diapositives | `diapos` → images + `--pdf` pour LinkedIn |
| Diaporama statique | diaporama, 16:9 | `diapos --pdf` |
| Diaporama animé (transitions, entrées en cascade) | diaporama | `film` → MP4 (+ `--gif`) au format voulu |
| Vidéo courte 6/15/30 s, verticale ou carrée | diaporama animé, ou montage du film long | MP4 ; sous-titres incrustés si pas de textes à l'écran |
| Film de lancement 60 s – 2 min, voix off, sous-titres | `assets/scene-modele.html` + storyboard | voir section 3 |
| Visuels uniques de tailles fixes (galerie Product Hunt, vignette GIF, miniature YouTube, image de partage, bannière de store) | `assets/planche-modele.html` | `exporter-planche.cjs` |
| Captures de store (App Store, Google Play) | diaporama aux formats des stores | `diapos` |
| **Package complet** | tout ce qui précède | arborescence de `references/visuels.md` + `index-package.cjs` |

**Recette commune aux visuels et diaporamas :**
1. Écris le contenu en texte d'abord (une ligne par diapositive : titre, phrase, capture, effet) et fais-le valider — c'est là que se jouent 80 % des retours.
2. Copie le modèle (`diaporama-modele.html` ou `planche-modele.html`) dans le socle, remplace la marque (couleurs, polices), écris les diapositives.
3. Vérifie en images fixes : `rendre.cjs … --format 1080x1350 apercu 1 4 7` ou `diapos`, assemble une planche (`ffmpeg … xstack` ou `index-package.cjs`), regarde, passe `references/qualite.md`.
4. Rends et range dans `sortie/<usage>/` ; écris les légendes des posts dans `sortie/textes/`.
5. Montre le résultat (image ou planche) et itère.

Commandes de rendu (depuis n'importe où ; `--racine` = dossier servi, qui doit contenir la page et ses images) :
```bash
R="NODE_PATH=$(npm root -g) node <skill>/scripts/rendre.cjs --racine <socle>"
$R --scene diaporama.html --format 1080x1350 --nom carrousel --sortie sortie/instagram diapos --pdf
$R --scene diaporama.html --format 1080x1920 --nom reel-15s --sortie sortie/video film 30
$R --scene diaporama.html --format 480x480 --nom vignette --gif 480 film 15
node <skill>/scripts/exporter-planche.cjs --racine <socle> --planche planche.html --sortie sortie/product-hunt
node <skill>/scripts/index-package.cjs sortie "Package <App>"
```

## 3. Le film de lancement (la commande la plus complète)

Montre le résultat des étapes marquées ★ avant de continuer : l'utilisateur juge sur images, et un retour au storyboard coûte cinq minutes, un retour après rendu une heure.

1. **Storyboard ★** — lis `references/recit.md`, écris `storyboard.md` d'après `assets/storyboard-modele.md`. Ordre : accroche sur une vraie photo → le problème (chaos des outils actuels) → révélation du logo → promesse avec les mots de la landing → démonstration, une fonctionnalité par scène numérotée, avec son bénéfice → résultat dans le temps (« 3 weeks later ») → récapitulatif en trois écrans → fin (logo, slogan, adresse). Écris la voix off en même temps, en comptant les mots (≈ 2,3 mots/s en voix posée). Fais valider le tableau avant toute capture.
2. **Scène ★** — copie `assets/scene-modele.html` en `scene.html` : il fournit le moteur (téléphone, enchaînement des écrans, caméra qui zoome sur un point de l'écran, légendes, bulles, touchers, récapitulatif, fin). **Tu écris les scènes** acte par acte avec le catalogue `references/scenes.md`. Tout se calcule depuis `t`, sans minuterie ni aléa. Vérifie avec `rendre.cjs … apercu 0.5 4 12 25 …` et la liste `references/qualite.md`.
3. **Rendu** — film long : `rendre.cjs --scene scene.html --nom film film 30`. Versions courtes : un fichier de montage par durée (`assets/montage-60s-modele.cjs` → `montage-60s.cjs`, `montage-30s.cjs`…) qui liste des morceaux du film long joués entre ×1 et ×2, puis `rendre.cjs … --montage montage-60s.cjs --nom film-60s court 30`. Coupe entre deux légendes ; fondu enchaîné sauf entre deux cadrages trop différents (marquer `'net'`). Vérifie `node <skill>/scripts/montage.cjs montage-60s.cjs` (durée, place de chaque réplique). Formats verticaux : refaire une scène 9:16 ou passer par le diaporama animé avec les mêmes captures.
4. **Voix off et sous-titres ★** — suis `references/voix-sous-titres.md` : voix ElevenLabs choisie selon le brief (dire laquelle et pourquoi), **une seule prise de tout le texte** (`voix-off.cjs --montage … --texte`), téléchargement, transcription horodatée mot par mot, puis :
   ```bash
   node <skill>/scripts/voix-off.cjs --montage montage-60s.cjs --prise voix/prise.mp3 --muet sortie/video/film-60s-court-muet.mp4 --sortie sortie/video --nom film-60s --langue en
   ```
   Le script découpe la prise réplique par réplique, la pose sur ses scènes, mixe, normalise, écrit `.srt` et `.vtt` et une piste de sous-titres activable. Si la voix déborde, ajuste les vitesses du montage plutôt que de régénérer (chaque génération coûte des crédits). Tu ne peux pas écouter : demande à l'utilisateur d'écouter avant publication.
5. **Livraison** — maître (crf 21) + web (crf 26), sous 25 Mo si le fichier est servi par Cloudflare Pages ; affiche avec téléphone entier ; texte de la voix off ; `.srt` à importer dans YouTube Studio (Product Hunt n'accepte qu'un lien YouTube).

## 4. Ranger et livrer
- Tout ce qui a servi (brief, storyboard, pages HTML, scripts adaptés, captures, prises de voix, horodatage, livrables) est commité dans le dossier du socle : l'environnement d'exécution est effacé, le dépôt fait foi. Suivre les conventions de commit du dépôt.
- Pour une revue d'ensemble : `index-package.cjs` puis montrer `sortie/index.html` (ou le publier comme page si l'outil existe).
- Donner à l'utilisateur la liste des fichiers par réseau, avec ce qui reste à faire de son côté (téléverser sur YouTube, importer les sous-titres, choisir une des prises de voix…).

## Points d'attention
- Montre des **images**, pas des descriptions, à chaque validation.
- Le **nom de la marque plutôt que « l'IA »** dans tous les textes.
- **Une image = un message ; une scène = un bénéfice.**
- La voix et les sous-titres ne contredisent jamais le texte à l'écran.
- `pkill -f <motif>` et `pgrep -f` dans une boucle se trouvent eux-mêmes : repérer le PID avec `ps`, puis `kill <pid>`.
- Le Chromium de Playwright ne lit pas le H.264 (durée nulle dans une page de test) : vérifier les MP4 avec `ffprobe`.
