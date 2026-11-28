# SCRIPT — Reel n°7 « Carousel Factory : un système, plein de carrousels » (v1)
Skill : reel-histoire (appmee, branche `claude/skill-reel-histoire`). Source : les vrais carrousels de Hari (Reflex IA ; artefacts claude.ai « Carrousels Les Confits » et « Carrousels EndoReconversion »).
Fichier principal : `out/reel-carousel-factory.mp4`, rangé aussi sous `CONTENT/REELS_INSTAGRAM/reel-instagram-reflexia-7.mp4` · **sans musique** · 1080×1920 · 30 i/s · **57,3 s** · −14,1 LUFS · aucune image figée · aucun texte qui en chevauche un autre.
Voix : Gemini TTS, voix Charon, modèle `gemini-3.8-flash-tts`, tempo 1,16, silences 0,08 s. Texte validé par Hari (« Go »), **une seule retouche** : « un secret de fabrication » → « une fabrication pas à pas » (le mot « secret » est banni par le contrôle qualité du dépôt ; les slides, elles, gardent leur propre titre).

**Son (v1.1, retour de Hari « tous les bruits sont trop forts, transition de glissement »)** : la première version contenait **par erreur la nappe musicale** (le mixage avait été lancé sans `--sans-nappe`) ; retirée. Bruitages baissés : niveau général 0,5 → 0,3 (`mix.py --sfx 0.3`), balayage de transition entre scènes 0,6 → 0,3, swipes 0,3 → 0,2 (`synth.cjs`). Voix, image et durée inchangées.

## Texte lu (mot pour mot)
1. Un seul système, et tu fabriques des carrousels pour n'importe quel univers ! *(dit de Hari)*
2. Celui-là, c'est pour Reflex IA, les outils IA.
3. Celui-là, pour une marque de confitures.
4. Et celui-là, pour du coaching, avec sa propre charte !
5. Trois univers, trois styles, mais exactement le même système !
6. Moi, je lui donne trois choses : mes données, ma charte, et un modèle de carrousel.
7. Les données, c'est le fond : le texte, les photos, l'angle.
8. La charte, ce sont les couleurs, la police, le logo.
9. Et le modèle, c'est la structure : une liste, une fabrication pas à pas, des coulisses, une pédagogie en cinq slides.
10. Tu changes les données et la charte, le système fait le reste ! *(dit de Hari)*
11. Tu veux le même système pour ton univers ? Commente « carrousel », et je te l'envoie pour l'adapter à ta sauce !

## Mise en scène
Ouverture : mur de slides des trois univers qui défilent · Reflex IA / Confitures / Coaching : un carrousel feuilleté en swipe (doigt), clic de souris, la dernière slide **ressort vers l'avant** (voile + ombre) · Même système : les trois premières slides côte à côte · Système : trois cartes (Données, Charte avec les vraies palettes des trois univers, Modèle avec quatre vrais modèles) puis « Le système fait le reste » et trois slides · CTA : « Commente carrousel » tapé dans un commentaire. Aucun cadre jaune, fonds actuels, « REFLEX·IA » en haut au milieu.

## Sources et statuts
| Élément | Source | Statut |
|---|---|---|
| Slides Reflex IA | `CONTENT/CARROUSELS_INSTAGRAM/carrousel-instagram-reflexia-4/` (slides 1, 2, 3, 4, 6, 8) | réelles, non retouchées (redimensionnées en JPEG) |
| Slides confitures | artefact « Carrousels Les Confits », carrousels « Lire une étiquette », « L'assiette froide », « Pourquoi du citron », « Un pot bien fermé », « Trois accords », « Matinée de mise en pots » | réelles ; **seules les slides sans bandeau « à fournir par Pascal »** |
| Slides coaching | artefact « Carrousels EndoReconversion » (modèle `clair-sommeil`), slides 1, 4, 6, 7 | réelles ; **seules les slides sans tag « À vérifier »** ; rien de médical n'est dit |
| Palettes | variables `--f` / `--fc` / `--papier` des artefacts ; jaune `#FFD93B`, violet `#6C5CE7`, encre `#0F1020` de Reflex IA | réelles |
| « n'importe quel univers », « le système fait le reste » | Hari | **non prouvé ici** |

## Limites (dites à Hari)
- « Clair coaching » a été lu comme **EndoReconversion** (hypothèse retenue après « Go »).
- La page EndoReconversion dit « santé et droit : informations générales, à faire relire avant publication ; photos d'illustration » : elles sont montrées comme exemples de mise en forme, pas comme contenu à publier.
- Les slides coaching 1, 4, 6, 7 ne se suivent pas dans le carrousel d'origine (numéros 1/11, 4/11, 6/11, 7/11 visibles).
- Aucun chiffre de coût ou de temps pour confitures / coaching ; aucune donnée d'audience ; le reel ne dit pas combien de temps ni d'argent prend un carrousel.
- Curseur, clics et swipes = mise en scène sur de vraies slides, pas un enregistrement d'écran.
- Son non écouté par moi ; rendu non vu sur téléphone (planches de contact relues).

## Contrôles passés
`qa.cjs` vert · chevauchements 0 sur 573 instants · ffprobe 1080×1920 / 30 i/s / 57,3 s · −14,2 LUFS · freezedetect (n=0,0008, d=1,2 s) : 0 (une première version en avait 5 dans la scène « système » ; corrigé par un léger flottement des cartes) · transcription du mixage : similarité 0,986 par mots (« cinq » transcrit « 5 »).

## Pipeline (depuis ce dossier, `GOOGLE_API_KEY` en variable d'environnement, jamais affichée)
`python3 -I tts.py $W` → `python3 -I plan.py` → `node events.cjs` → `node qa.cjs` → `node synth.cjs $W` → `node render.cjs --out out/reel-muet.mp4 --frames $W/frames --workers 4` → `python3 -I mix.py $W out/reel-muet.mp4 out/reel-carousel-factory.mp4 --sans-nappe --sfx 0.3`
Slides : `assets/slides/` (rendues depuis les artefacts avec Playwright 1080×1350, puis JPEG).
