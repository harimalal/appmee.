# SCRIPT — Reel n°9 « Reel Factory » (faire des reels avec Claude)
Skill : reel-histoire (appmee, branche `claude/skill-reel-histoire`). Fichier : `out/reel-reel-factory.mp4`, rangé sous `CONTENT/REELS_INSTAGRAM/reel-instagram-reflexia-9.mp4` · couverture `couverture-reel-instagram-reflexia-9.png` · **sans musique** (`--sans-nappe`), bruitages bas (`--sfx 0.3`) · 1080×1920 · 30 i/s · **52,9 s** · −14,1 LUFS · aucune image figée · aucun texte qui en chevauche un autre.
Voix : Gemini TTS, voix Charon, modèle `gemini-3.1-flash-tts-preview` (même voix que le n°8), tempo 1,16.

## Approche (retour de Hari, 28/11/2026)
Plus d'approche « chiffres » : on part du besoin de celui qui regarde (les reels accrochent, mais c'est dur à faire : du fond, de la forme, des effets, des transitions toutes les quelques secondes, tout scripté), on montre pourquoi c'est plus simple avec Claude (il fait le script, les images, les effets, la voix ; on itère d'une phrase ; un système réglé une fois), et on illustre en plein écran avec nos vraies vidéos qui tournent. Hari : « lance tout, je fais les changements à la 1re version » (pas de validation intermédiaire du texte).

## Texte lu
1. Les reels, c'est ce qui accroche le plus. Mais en faire un, c'est un vrai casse-tête ! *(dit de Hari)*
2. Il faut du fond, sinon on décroche.
3. Et de la forme : des effets, une transition toutes les quelques secondes, tout écrit au mot près.
4. Moi, je ne fais plus le montage. C'est Claude qui s'en occupe.
5. Il écrit le script, choisit les images, place les effets et cale la voix.
6. Toi, tu valides le texte. C'est tout.
7. Un truc ne te plaît pas ? Tu le dis, il refait.
8. Le fond est trop sombre ? Le titre ne se lit pas ? Une phrase, et c'est corrigé.
9. Et le mieux, c'est que c'est un système. Tu le règles une seule fois.
10. Ta charte, ton ton, tes effets préférés.
11. Ensuite, tu demandes juste : fais-moi une nouvelle vidéo. Et elle sort en vingt minutes ! *(dit de Hari ; écran : « hors retouches »)*
12. Toutes les vidéos que tu vois là sont sorties comme ça.
13. Tu veux le même système ? Commente « reel », et je te l'envoie !

## Mise en scène (un changement toutes les 2 à 4 s, fond bleu-noir reflet de verre)
- **hook** : mur de trois colonnes de vrais reels (n°1 à 8) qui tournent et défilent ; à « casse-tête », le mur tremble et se désature.
- **craft** : un reel (n°5) plein cadre, balayé vers le haut à « décroche » ; puis le n°7 avec trois pastilles « Effets » (zoom + clic), « Transitions » (fouetté vers le n°3), « Script » (feuille de script).
- **claude** : logo Claude en 3D, huit reels en orbite ; puis quatre cartes : le script (vraies lignes `"voice"` de story.json), les images (vraies slides), les effets (reel n°5 + clic), la voix (forme d'onde animée, décorative).
- **valide** : le vrai `TEXTE_A_VALIDER.md` du n°9, bouton « Valider » cliqué.
- **refait** : la vraie demande de Hari (« Refais la couverture, qu'on voie bien le titre »), réponse « C'est refait. » ; puis deux vrais avant/après du n°8 au balayage : fond sombre → clair (proposition réelle, thème Claude) et couverture au titre illisible → lisible (corrigée le 28/11).
- **systeme** : trois réglages qui se verrouillent : charte (couleurs + police), ton (« copain »), effets (clic, zoom, swipe).
- **nouvelle** : on tape « Fais-moi une nouvelle vidéo », envoi, un reel sort.
- **montage** : les huit reels en coupes rapides (flash + zoom).
- **cta** : cinq reels qui tournent, « Commente reel ».
Les extraits : 3 s de chaque reel final (15 i/s, `assets/clips/rN/`), une image affichée par instant, décodage attendu par `render.cjs` (`window.__wait`).

## Limites
« ce qui accroche le plus » et « vingt minutes » sont des dits de Hari, non mesurés (« hors retouches » à l'écran ; avec plusieurs allers-retours, c'est plus long). La voix vient de Google (Gemini TTS) ; Claude pilote le reste (script, images, montage, contrôles). La forme d'onde de la carte « La voix » est décorative.

## Contrôles
`qa.cjs` vert · chevauchements 0 sur 529 instants · 1080×1920 / 30 i/s / 52,9 s · −14,1 LUFS · freezedetect 0 · transcription du mixage 0,994 par mots.

## Chaîne
`python3 -I tts.py /tmp/w9` → `python3 -I plan.py` → `node events.cjs` → `node qa.cjs` → `node synth.cjs /tmp/w9` → `node render.cjs --out out/reel-muet.mp4 --frames /tmp/w9/frames --workers 4` → `python3 -I mix.py /tmp/w9 out/reel-muet.mp4 out/reel-reel-factory.mp4 --sans-nappe --sfx 0.3` ; couverture `node cover.cjs`.
