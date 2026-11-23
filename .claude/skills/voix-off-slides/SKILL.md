---
name: voix-off-slides
description: Transforme une présentation HTML animée (slides avec étapes au clavier) en vidéo narrée — choix de la voix, voix off lue comme un humain, slides calées sur le rythme de la voix, une seule prise continue, montage et contrôles par transcription. Utilise ce skill dès que l'utilisateur veut « mettre une voix off sur mes slides », « caler les slides sur l'audio », « faire une vidéo de ma présentation », « choisir une voix », « narrer le deck », même sans nommer le format. Pour écrire le texte lui-même, voir le skill script-video.
---

# Voix off sur slides

Ce skill fait d'une présentation HTML une vidéo narrée, **comme un présentateur humain** : il lit tout son texte d'une voix normale, puis fait défiler ses slides à ce rythme. La voix ne se cale jamais sur la vidéo ; c'est la vidéo qui suit la voix.

Né de la vidéo « lancement Product Hunt de Dropit » (octobre 2026) : 29 slides, 4 prises de voix, 1 prise vidéo, 6 min 07. Ce qui a coûté cher avant d'y arriver est listé dans « Les pièges ».

## Prérequis
- `GOOGLE_API_KEY` (Gemini) dans l'environnement ; Node + Playwright (Chromium), ffmpeg, Python 3.
- Une présentation HTML 1920×1080 qui avance au clavier (→) et expose `window.__S` (liste `[id, nombre d'étapes]`) et `window.__go(i, étape)`, comme celles du skill demo-video-youtube. Sinon, ajouter ces deux fonctions au deck avant tout.
- `<skill>` = le dossier de ce skill. Travailler dans un dossier de travail `<socle>` (scratchpad), jamais dans le dépôt pour les audios et vidéos.

## La chaîne (dans cet ordre)

### 1. Lire le deck
```bash
NODE_PATH=$(npm root -g) node <skill>/scripts/extraire-slides.js deck.html slides.json
```
→ pour chaque slide : id, nombre d'étapes, texte à l'écran, notes. C'est la base du script et des contrôles.

### 2. Le texte
Un fichier `script.txt`, un bloc par slide, **uniquement ce qui sera dit** :
```
##02 titre
Mon lancement Product Hunt, préparé en deux jours avec Claude. …
##03 benefice
…
```
La voix **appuie et développe** ce qui est écrit (l'enjeu, le pourquoi du comment) ; elle ne relit pas l'écran et ne suit pas l'ordre des animations. Pour écrire un texte qui retient, suivre le skill **script-video** (et sa simulation d'audience). Faire valider le texte **avant** toute génération.

Ne pas mettre de slide d'introduction faible : commencer sur la slide qui porte le vrai titre ou le résultat.

### 3. Le choix de la voix (casting)
Toujours sur le **même extrait** (les 2 premiers paragraphes), en une passe :
```bash
python3 -I <skill>/scripts/voix.py casting extrait.txt casting/ --voix Puck,Achird,Iapetus,Umbriel,Orus,Zubenelgenubi
```
- Proposer 4 à 6 voix **contrastées** à la fois (timbre, énergie), les nommer avec leur caractère, laisser l'utilisateur écouter et choisir. Je ne peux pas écouter : ne jamais prétendre qu'une voix « sonne » bien.
- Affiner par élimination avec ses mots (« homme, pas grave, médium, reconnaissable, pas d'accent, naturel, pas podcast »). Ce qui a été retenu pour Dropit : **Achird**, voix d'homme au timbre médium.
- Puis comparer le même extrait sur 2 ou 3 **modèles** (`--modele`) : le timbre change d'un modèle à l'autre. Retenu : `gemini-2.5-flash-preview-tts`.
- Le style se règle en choisissant la voix et en **écrivant** le texte (ponctuation, phrases courtes), jamais par une consigne (voir les pièges).

### 4. Les prises
```bash
python3 -I <skill>/scripts/voix.py prises script.txt prises/ --voix Achird --modele gemini-2.5-flash-preview-tts
```
Le texte est coupé en prises d'environ 300 mots **entre deux slides** (≈ 1 min 30 chacune), générées en parallèle, chacune transcrite et comparée au texte. Débit attendu : 170 à 210 mots/min. Ne jamais accélérer l'audio.

### 5. Les repères
```bash
python3 -I <skill>/scripts/reperes.py script.txt prises/ reperes.json
```
Pour chaque slide : instant où commence son texte. Estimation par la part de mots déjà lus, recalée sur la plus longue pause voisine, puis **vérifiée** en transcrivant 2,5 s à cet endroit (le début du paragraphe doit s'y entendre) ; sinon les pauses voisines sont essayées. Tout repère non vérifié est signalé : l'écouter ou le transcrire avant de continuer.

### 6. Le minutage et la prise vidéo
```bash
python3 -I <skill>/scripts/minutage.py reperes.json slides.json minutage.json
NODE_PATH=$(npm root -g) node <skill>/scripts/presenter.js deck.html minutage.json prise/
```
- Chaque slide dure de son repère au suivant ; ses étapes se répartissent sur sa durée (8 % → 88 %, au moins 0,8 s entre deux).
- **Une seule prise continue**, fenêtre 1952×1080 (le deck se met à l'échelle 1 et le cadre est recadré à 1920×1080) : les vraies transitions entre slides, comme un présentateur. L'enregistrement du navigateur ne capte pas le son : l'instant réel de chaque changement est noté dans `prise/journal.json`.

### 7. Le montage et les contrôles
```bash
python3 -I <skill>/scripts/monter.py prise/journal.json prises/ video.mp4
```
- La voix complète est posée 0,4 s après le premier changement de slide ; la vidéo est coupée et encodée (H.264, CRF 23).
- Le script affiche l'écart entre le plan et la prise (attendu : moins de 0,1 s), transcrit 4 s après 4 changements de slide et extrait leurs images : **vérifier que la voix dit bien le début de la slide montrée**, et regarder les images.
- Livrer la vidéo, dire ce qui a été vérifié et ce qui ne l'a pas été (je n'écoute pas le rendu).

Corriger une seule slide : modifier son paragraphe, regénérer **sa prise** seulement, relancer repères → minutage → prise → montage (quelques minutes, 1 appel de voix).

## Les pièges (chacun a coûté cher)
- **La consigne est lue à voix haute.** Avec les modèles TTS Gemini, tout texte envoyé est dit : « Dis ce texte comme… » se retrouve au début de chaque clip (≈ 30 s de consigne avant le contenu). `systemInstruction` est refusé (400). → Envoyer **le texte seul**. Et toujours transcrire chaque audio produit avant de le livrer.
- **Une phrase par appel étire la voix** (≈ 40 s pour 20 mots), **une prise unique de 8 min l'accélère** (≈ 270 mots/min). → Prises d'environ 300 mots.
- **Format de sortie** : `gemini-3.8-flash-tts` renvoie un WAV complet (ne pas rajouter d'en-tête, sinon claquement) ; `gemini-2.5-flash-preview-tts` et `gemini-3.1-flash-tts-preview` renvoient du PCM 24 kHz brut à envelopper. `voix.py` gère les deux.
- **Quotas** : plafond **journalier par modèle** selon le palier du compte, même payant (Tier 1 : 100 requêtes/jour sur `gemini-3.8-flash-tts`). Lire le message 429 (`quotaId`, `retryDelay`). Ne pas dépenser le quota en essais : casting sur un extrait, prises longues, une génération par slide corrigée seulement.
- **Repères donnés par Gemini** (« à quelle seconde commence ce paragraphe ») : faux au-delà de la première minute (instants après la fin de l'audio). → Proportion de mots + pauses + vérification.
- **Ne pas filmer slide par slide** avec rechargement : plus lent, pas de transitions, et chaque slide étirée sur sa voix. Une prise continue suffit.
- **Une voix qui énumère l'écran** est jugée « nulle » : elle doit expliquer l'enjeu, pas décrire.
- Le panneau du deck (`#ui`) se cache seul après 2,2 s sans souris : ne pas bouger la souris pendant la prise.

## Coût d'une vidéo de 6 min
1 casting (6 appels), 4 prises, ≈ 35 petites transcriptions de contrôle, 1 prise vidéo en temps réel (≈ durée de la vidéo + 10 s), 1 encodage.
