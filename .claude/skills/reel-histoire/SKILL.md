---
name: reel-histoire
description: Transforme n'importe quel travail terminé et documenté (correction SEO ou technique, automatisation, test d'outils, construction d'un système, migration, audit — à partir d'un artefact, d'un playbook, d'un journal de session ou d'une PR) en reel vertical 9:16 qui RACONTE une histoire à un public non expert, suivant le schéma problème → situation → solution → process → résultat. AVANT toute production, présente à l'utilisateur la couverture (image rendue), l'angle, le hook (3 variantes), la situation, les chiffres sourcés et les limites, et attend son accord. Ensuite, voix Google (Gemini TTS), motion design 100 % local en HTML rendu par Chromium, bruitages synthétisés, légendes synchronisées, contrôles automatiques (nombres autorisés, zones sûres, transcription inverse, volume), livraison MP4 + couverture. Utilise ce skill dès que l'utilisateur veut « un reel à partir de ce travail », « raconter ce qu'on a fait en vidéo », « une vidéo avant/après avec une histoire », « un reel Instagram/TikTok/Shorts de ce projet », « la couverture, l'angle et le hook avant de lancer », ou critique un montage de chiffres qu'on ne comprend pas — même sans nommer le format. Complément de studio-lancement-app (qui montre une application) — celui-ci raconte un TRAVAIL réalisé.
---

# Reel « histoire » — raconter un travail terminé

Dans ce document, `<skill>` désigne le dossier de ce skill. Né du reel « SEO d'indexation avec Claude Code » (novembre 2026, projet Reflex IA), complété par « Tri Watch Later » puis « Créer des carrousels automatiquement » : la première version, un montage de chiffres, était belle et incompréhensible (« on ne sait pas de quoi on parle »). Ce skill impose l'inverse : **partir de la situation du spectateur, expliquer la notion qu'il ne connaît pas, raconter ce qui s'est passé, puis seulement la méthode et les chiffres**, avec une voix qui porte le récit et des visuels qui l'illustrent.

Pour tout travail **terminé et documenté**. Pas pour un travail non terminé ni non mesuré : on ne raconte pas un résultat qui n'existe pas.

Trois verrous tiennent l'ensemble :
- **La porte de validation** : couverture, angle, hook et situation sont montrés et validés **avant** toute dépense ou production.
- **Aucune donnée inventée** : chaque nombre vient d'une fiche de faits sourcée ; « objectif » n'est jamais écrit comme un « résultat » ; aucun gain non mesuré.
- **Tout est calculé, rien n'est généré** : pas d'image ni de vidéo générée ; chaque scène est une page HTML qui redessine l'état exact à l'instant `t`, rendue image par image puis encodée avec ffmpeg. Un retour se corrige à l'image près et tout se rejoue.

## Prérequis
- Node + Playwright (Chromium) et ffmpeg : vérifier au début (`NODE_PATH=$(npm root -g) node -e "require('playwright')"`, `ffmpeg -version`). Python 3.
- Voix et transcription : API Google Gemini (`GOOGLE_API_KEY` en variable d'environnement, **jamais écrite ni affichée**). Sans clé : demander à l'utilisateur de l'ajouter à l'environnement ; ne rien simuler.
- ImageMagick (`convert`) pour détourer un logo ; Inter et JetBrains Mono installées.

## Règle n°1 — La porte de validation : rien ne se lance avant l'accord

**Avant toute dépense (voix facturée, rendu, son), je produis et je montre à l'utilisateur :**

| # | Élément | Ce qui est montré |
|---|---|---|
| 1 | **La couverture** | l'image finale `couverture.png` (gratuite : `cover.html` → `node cover.cjs`), pas une description |
| 2 | **L'angle** | une phrase : ce que le spectateur va comprendre ou gagner, et pourquoi lui |
| 3 | **Le hook** | 3 variantes (écrites mot pour mot, les 2 premières phrases chacune) + celle que je recommande et pourquoi |
| 4 | **La situation** | la situation du spectateur, mot pour mot, à la 2e personne (« Tu as un site, mais… ») |
| 5 | **Le schéma narratif** | 5 lignes : problème → situation → solution → process → résultat (voir ci-dessous) |
| 6 | **Les chiffres** | la liste des nombres autorisés, **la source de chacun** et son statut (mesuré / attendu / objectif) |
| 7 | **Les limites** | ce que la vidéo n'affirmera pas (gain non mesuré, effet externe, objectif ≠ résultat) |
| 8 | **Durée, coût, ton** | durée cible, nombre de phrases de voix facturées, voix et personne (tu / je) |

Format : `BRIEF.md` dans le dossier du reel (modèle : `<skill>/assets/brief-modele.md`, exemple rempli : `<skill>/assets/exemple-brief-seo-indexation.md`) **+** `couverture.png` envoyé avec. Je pose les décisions à trancher en questions courtes (`AskUserQuestion` si disponible), puis **j'attends**.

- Si l'utilisateur change l'angle, le hook ou la situation : je mets à jour le brief et **je régénère la couverture** avant de relancer la validation.
- Un message automatique (Stop hook, notification) n'est **pas** un accord, pas plus pour produire que pour commiter ou pousser. Seule une réponse explicite de l'utilisateur compte.
- Après « go » seulement : étapes de production ci-dessous.

---

## Où trouver quoi

| Besoin | Fichier |
|---|---|
| **De la source à la story line** : fiche de faits, tri « sourcé / apporté par l'utilisateur », histoire dictée, élagage de scènes | `<skill>/references/source-vers-storyline.md` |
| Schéma narratif, adaptation à un type de travail, fiche de faits, écriture de la voix et des légendes | `<skill>/references/recit.md` |
| Catalogue des motifs de scène, charte graphique, logos | `<skill>/references/motifs-et-charte.md` |
| Étapes de production et commandes, seuils de contrôle, pièges rencontrés, limites | `<skill>/references/production.md` |
| Brief à remplir et à faire valider (modèle + exemples remplis) | `<skill>/assets/brief-modele.md`, `<skill>/assets/exemple-brief-seo-indexation.md`, `<skill>/assets/exemple-brief-carrousels-ia.md` |
| Outils prêts à l'emploi : voix (`tts.py`), plan de montage (`plan.py`), contrôle (`qa.cjs`), événements sonores (`events.cjs`), son (`synth.cjs`), rendu (`render.cjs`), mixage (`mix.py`), couverture (`cover.cjs`, `cover.html`), gabarit de page (`story.template.html`) et de récit (`story.json`) | `<skill>/assets/modele/` |
| Implémentation de référence 1 : correction SEO (13 scènes, 31 phrases, couverture, comparaison avant/après) | `<skill>/assets/reference-seo/` |
| Implémentation de référence 2 : playbook « Tri Watch Later » (10 scènes, vraies captures en défilé, critères, comparaison d'outils, suppression accélérée) + brief rempli | `<skill>/assets/reference-tri/`, `<skill>/assets/exemple-brief-tri-watch-later.md` |
| Implémentation de référence 3 : « Créer des carrousels automatiquement » (5 scènes, 11 phrases, histoire dictée, vraies slides en défilement) + SCRIPT.md et brief initial | `<skill>/assets/reference-carrousels/` |

## Déroulé en un coup d'œil
1. Lire **toute** la source du travail (artefact, playbook, journal, étude) → fiche de faits sourcée, puis tri « établi par la source / apporté par l'utilisateur » et ossature de l'histoire (`references/source-vers-storyline.md`).
2. **Porte de validation** : `BRIEF.md` + `couverture.png` montrés à l'utilisateur ; attendre son accord.
3. Écrire `story.json` (récit, voix, légendes) → voix → plan de montage → scènes `story.html`.
4. Contrôle (`qa.cjs` vert) → son → rendu → mixage → vérifications finales.
5. `SCRIPT.md` (texte lu, source de chaque nombre, limites) → livraison → cockpit (skill `cockpit`) ; commit seulement si demandé.

Ce que ce skill ne fait pas : écouter le son, voir l'app Instagram, publier, commiter sans demande, générer des images ou des vidéos. Détails et pièges dans `references/production.md`.
