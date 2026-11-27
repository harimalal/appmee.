# SCRIPT — Reel n°8 « Content Factory : un article → tous tes posts » (v1)
Skill : reel-histoire (appmee, branche `claude/skill-reel-histoire`). Source : la chaîne réelle du dépôt pour l'article « Combien coûte OpenClaw ? » (`CONTENT/2026-10-23_combien-coute-openclaw-prix-reel-alternatives-2026/`).
Fichier principal : `out/reel-content-factory.mp4`, rangé aussi sous `CONTENT/REELS_INSTAGRAM/reel-instagram-reflexia-8.mp4` · couverture `couverture-reel-instagram-reflexia-8.png` · **sans musique** (`--sans-nappe`), bruitages bas (`--sfx 0.3`) · 1080×1920 · 30 i/s · **55,9 s** · −14,1 LUFS · aucune image figée · aucun texte qui en chevauche un autre.
Voix : Gemini TTS, voix Charon, **modèle `gemini-3.1-flash-tts-preview`** : le 27/11/2026, les quotas journaliers (100 requêtes) de `gemini-3.8-flash-tts` (voix des reels 5 à 7) et de `gemini-3.8-flash-lite-tts` étaient atteints. **La voix peut donc différer légèrement de celle des reels 5 à 7.** Toutes les phrases viennent du même modèle (voix homogène dans la vidéo). Pour la refaire avec la voix des reels 5 à 7 : remettre `"model": "gemini-3.8-flash-tts"` dans `story.json` et relancer la chaîne (11 requêtes) après la remise à zéro du quota.
`tts.py` accepte maintenant les modèles qui renvoient du PCM brut (`audio/l16`) : l'en-tête WAV est ajouté.

## Texte lu (validé par Hari, « Go »)
1. Un seul article de blog, et tous tes posts sortent d'un coup ! *(dit de Hari : le système produit les fichiers, pas la publication)*
2. Moi, je pars d'un article : le coût réel d'OpenClaw.
3. Le système en sort d'abord une fiche : les faits de l'article, chaque chiffre avec sa source.
4. Ensuite, il me propose une position, et c'est moi qui la valide.
5. Et de là, trois fabriques : un post LinkedIn, un fil X, et un carrousel !
6. Le post LinkedIn, avec le verdict pour chaque profil.
7. Le fil X, en six posts.
8. Et le carrousel : sept slides, prêtes pour Instagram, LinkedIn, Pinterest et TikTok.
9. Avant de publier, un contrôle : un chiffre qui n'est pas dans la fiche, il est refusé !
10. Résultat : des posts fidèles à l'article, sans chiffre inventé.
11. Tu veux le même système pour tes articles ? Commente « contenu », et je te l'envoie pour l'adapter à ta sauce !

## Mise en scène (vraie matière, démo plein cadre)
- **Ouverture** : la vraie page de l'article ; trois vrais rendus en jaillissent (post LinkedIn, slide 1 du carrousel, fil X) ; zoom sur le titre, clic, il ressort.
- **Fiche** : rendu fidèle de `atomes.md` (A1, A2, A6, A8, A12, A14 : fait, statut, source, lus dans le fichier) ; les lignes apparaissent une à une ; clic sur A6 qui ressort.
- **Position** : rendu de `positions.md` (statut « position proposée par Claude… à valider ou renverser par Hari », thèse, verdicts) ; le statut ressort ; bouton « Valider » cliqué → « Validée » (**mise en scène de l'étape de Hari**, pas une capture d'outil).
- **Fabriques** : trois tuiles ; le vrai post `LI-1` (le bloc « Pour qui ça vaut la peine » ressort) ; le vrai fil `X-FIL-1` (6 posts, défilement) ; les 7 vraies slides du carrousel en swipe, la dernière ressort.
- **Contrôle** : la **sortie réelle** de `node scripts/content-qa.mjs …` (relancée le 27/11/2026 : « ✓ VERT — 0 erreur(s), 0 avertissement(s) »), tapée ligne par ligne ; la ligne verte ressort.
- **CTA** : « Commente contenu » tapé dans un commentaire.
Les rendus sont générés par `cards.py` (lit les fichiers, ne réécrit aucun texte) puis `cards.cjs` (captures Playwright, `assets/cards/`).

## Sources et statuts
| Élément | Source | Statut |
|---|---|---|
| 14 faits, statuts, sources | `atomes.md` | fichier réel ; faits « compilés » de l'article, non mesurés |
| Position | `positions.md` | fichier réel, « à valider ou renverser par Hari » |
| Post LinkedIn, fil X | `linkedin.md` (LI-1, 1 386 caractères), `x.md` (X-FIL-1 : 6 posts) | fichiers réels |
| Carrousel | `carrousel/instagram/slide-01…07.png` ; exports Instagram, LinkedIn PDF, Pinterest, TikTok présents dans `carrousel/` | fichiers réels |
| Contrôle | `scripts/content-qa.mjs` ; règle « un chiffre absent de atomes.md est refusé » (`SKILL_CONTENT_FACTORY.md`) | sortie réelle |
| « tous tes posts sortent d'un coup », « c'est moi qui la valide » | Hari | non prouvé ici |

## Limites (dites à Hari)
- Le contrôle vérifie que **chaque chiffre vient de la fiche**, pas qu'il est exact : les chiffres de l'article restent « compilés ».
- « Tous tes posts » = LinkedIn, X et carrousel (pas de vidéo) ; le système produit les fichiers, la publication reste à faire.
- Le bouton « Valider » est une mise en scène ; on ne sait pas, dans le dépôt, si cette position a été validée telle quelle.
- Voix d'un autre modèle que les reels 5 à 7 (quotas). Son non écouté ; rendu non vu sur téléphone.

## Contrôles passés
`qa.cjs` vert · chevauchements 0 sur 559 instants · 1080×1920 / 30 i/s / 55,9 s · −14,1 LUFS · freezedetect 0 (une image figée sur la slide finale corrigée par un léger flottement) · transcription du mixage 0,972 par mots (« trois/six/sept » transcrits en chiffres ; « OpenClaw » bien entendu).

## Pipeline (depuis ce dossier, `GOOGLE_API_KEY` en variable d'environnement, jamais affichée)
`node ../../scripts/content-qa.mjs ../2026-10-23_combien-coute-openclaw-prix-reel-alternatives-2026 > /tmp/cqa.txt` → `python3 -I cards.py /tmp/cqa.txt` → `node cards.cjs` → `python3 -I tts.py $W` → `python3 -I plan.py` → `node events.cjs` → `node qa.cjs` → `node synth.cjs $W` → `node render.cjs --out out/reel-muet.mp4 --frames $W/frames --workers 4` → `python3 -I mix.py $W out/reel-muet.mp4 out/reel-content-factory.mp4 --sans-nappe --sfx 0.3` · couverture : `node cover.cjs`.
