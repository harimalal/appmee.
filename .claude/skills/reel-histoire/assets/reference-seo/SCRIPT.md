# Reel « histoire » — script, sources, limites

Format 1080×1920 (9:16), 30 fps, **95 s**, voix Google (Gemini TTS, voix Charon) + bruitages et nappe synthétisés localement. Aucune image ni vidéo générée : motion design HTML/CSS/JS rendu par Chromium (`story.html`), voix pilotant le montage (`plan.py` → `timeline.json`).

## Le récit (réponse au retour : « on ne comprend rien, il faut raconter une histoire »)
0. **Ouverture (0–15 s)** : le titre « Comment optimiser le SEO de ton site avec Claude Code ? » (logo Claude, trait de tutoiement), « Tout automatique, en une seule commande » (le fichier de consigne réellement utilisé, `prompt-claude-code-indexation-reflex-ia.md`), puis le renversement : « Ton site n'est pas référencé sur Google ? Ce n'est pas parce que tes articles sont mauvais, ni parce que ta boutique est mal faite : c'est parce que tes pages sont mal indexées, ou pas du tout. »
1. **Situation (15–29 s)** : « Sur mon blog : 285 pages non indexées, pour 132 articles » → tout le monde parle de mots-clés, personne de l'**indexation** (le catalogue de Google) → ça se voit dans la Search Console.
2. **Enquête (29–63 s)** : la Search Console donne le nombre, pas la cause → Claude Code lit le code → trois causes « bêtes » (deux adresses pour la même page ; filtres du menu qui fabriquent de fausses pages ; fichier de recherche qui change de nom et renvoie une 404) → 9 articles « vus mais pas indexés » reliés par 27 liens.
3. **Méthode (63–69 s)** : 5 corrections, 1 commit chacun, ≈ 23 minutes.
4. **Avant / après (69–81 s)** : curseur qui balaie l'écran, 4 mesures.
5. **Résultat honnête (66–75 s)** : site corrigé et vérifié ; réponse de Google attendue le 8 décembre ; objectif 155 à 160 pages indexées.
6. **CTA (91–95 s)** : reflex-ia.com, puis « Et ton site ? » (la fin reboucle sur le titre du début).

## Voix et légendes (instants mesurés)
| t (s) | scène | voix (texte lu) | légende à l'écran |
|---|---|---|---|
| 0.1 | titre | Comment optimiser le SEO de ton site avec Claude Code ? | (pas de légende : le visuel porte le texte) |
| 3.0 | titre | Tout automatique, en une seule commande. | (pas de légende : le visuel porte le texte) |
| 6.7 | probleme | Ton site n'est pas référencé sur Google ? | Ton site n'est pas référencé sur Google ? |
| 8.7 | probleme | Ce n'est pas parce que tes articles sont mauvais. | Ce n'est pas parce que tes articles sont mauvais. |
| 11.0 | probleme | Ni parce que ta boutique est mal faite. | Ni parce que ta boutique est mal faite. |
| 13.0 | probleme | C'est parce que tes pages sont mal indexées, ou pas du tout. | C'est parce que tes pages sont mal indexées, ou pas du tout. |
| 16.2 | hook | Sur mon blog : deux cent quatre-vingt-cinq pages non indexées. | (pas de légende : le visuel porte le texte) |
| 19.2 | hook | Pour cent trente-deux articles. | (pas de légende : le visuel porte le texte) |
| 21.8 | indexation | En SEO, on parle de mots-clés. | En SEO, on parle de mots-clés. |
| 23.7 | indexation | Mais avant, il faut que Google connaisse la page : c'est l'indexation. | Mais avant, il faut que Google connaisse la page : c'est l'indexation. |
| 27.7 | indexation | Sinon, elle n'apparaît jamais dans les résultats. | Sinon, elle n'apparaît jamais dans les résultats. |
| 30.3 | console | Le chiffre s'affiche dans la Google Search Console. | Le chiffre s'affiche dans la Google Search Console. |
| 33.4 | console | Elle donne le nombre, pas la cause. | Elle donne le nombre, pas la cause. |
| 35.8 | console | Claude Code a lu le code du site. | Claude Code a lu le code du site. |
| 38.4 | console | Les causes étaient bêtes. | Les causes étaient bêtes. |
| 40.4 | slash | Une même page existait sous deux adresses : avec un slash à la fin, et sans. | Une même page existait sous deux adresses : avec un slash à la fin, et sans. |
| 44.8 | slash | Pour Google, c'est deux pages : un doublon. | Pour Google, c'est deux pages : un doublon. |
| 47.5 | filtres | Les filtres du menu fabriquaient de fausses pages. | Les filtres du menu fabriquaient de fausses pages. |
| 50.4 | filtres | Soixante-six rangées en doublon par Google. | 66 rangées en doublon par Google. |
| 52.9 | fichier | Un fichier changeait de nom à chaque mise en ligne. | Un fichier changeait de nom à chaque mise en ligne. |
| 55.4 | fichier | Google le cherchait, et tombait sur une erreur quatre cent quatre. | Google le cherchait, et tombait sur une erreur 404. |
| 59.0 | articles | Neuf articles vus mais pas indexés : j'y ai ajouté des liens. | 9 articles vus mais pas indexés : j'y ai ajouté des liens. |
| 64.5 | corrections | Cinq corrections. Un commit chacun. Vingt-trois minutes. | (pas de légende : le visuel porte le texte) |
| 69.8 | avantapres | Avant, après : cent quarante adresses à corriger, zéro. | (pas de légende : le visuel porte le texte) |
| 73.9 | avantapres | Vingt-trois liens de filtres, zéro. | (pas de légende : le visuel porte le texte) |
| 76.5 | avantapres | Un fichier qui change de nom, zéro. | (pas de légende : le visuel porte le texte) |
| 79.4 | avantapres | Vingt-sept liens vers les articles oubliés. | (pas de légende : le visuel porte le texte) |
| 82.3 | resultat | Côté site, tout est corrigé et vérifié. | Côté site, tout est corrigé et vérifié. |
| 85.0 | resultat | Côté Google, la réponse arrive le huit décembre. | Côté Google, la réponse arrive le 8 décembre. |
| 87.7 | resultat | L'objectif : cent cinquante-cinq à cent soixante pages indexées. | L'objectif : 155 à 160 pages indexées. |
| 91.7 | cta | La méthode complète, sur Reflex IA point com. | (pas de légende : le visuel porte le texte) |

Les légendes surlignent le mot dit ; les instants de mots sont **proportionnels à la longueur des mots** (aucun horodatage de mot fourni par la synthèse) : approximation, pas un alignement exact.

## Sources de chaque chiffre
Tous viennent du travail documenté dans `PLAYBOOK/2026-11-seo-indexation-gsc/` et de l'artefact « Atelier indexation SEO » :
285 (pages non indexées, rapport Search Console du 10/11/2026) · 132 (articles du blog) · 66 (ligne « Autre page avec balise canonique correcte ») · 140 → 0 (adresses sans slash final à corriger) · 23 → 0 (liens de filtres `?f=`) · 1 → 0 (fichier de recherche qui change de nom : `search-index.0a086143.json` puis `search-index.d7b4d2ce.json`, deux mises en ligne réelles) · 0 → 27 (liens vers les 9 articles oubliés) · 9 · 5 · 23 minutes · 8 décembre · 155 à 160.

## Couverture
`out/couverture.png` (1080×1920) : titre, logo Claude, « 1 seule commande », le fichier de consigne et « Pas tes articles. L'indexation. ». Tout le texte tient dans le carré central 1080×1080 (aperçu `out/couverture-carre.png`) pour la grille de profil. Source : `cover.html` (`node cover.cjs`).

## Garde-fous respectés
- **« Tout automatique, en une seule commande »** est exact pour les corrections du code (un fichier de consigne lancé une fois ; 5 commits, ≈ 23 min). Ça ne couvre ni l'effet côté Google, ni la vérification et la mise en ligne, faites ensuite.
- **Logo** : le logo Claude (étoile orange) vient du dépôt (`carrousel-ia/logos/claude.png`), détouré sans modification ; ce n'est pas la mascotte Claude Code, absente du dépôt.
- **Aucun gain d'indexation annoncé** : « corrigé et vérifié » porte sur le site (mesures de build) ; l'effet côté Google est annoncé pour le 8 décembre ; **155 à 160 est un objectif**, écrit « objectif » à l'écran et dans la voix.
- « 285 pages » = URLs listées par la Search Console (variantes, 404 et redirections comprises), pas 285 articles : c'est pourquoi le hook oppose 285 à 132 articles.
- Voix à la 1re personne (« j'ai ajouté des liens »), comme demandé ; aucun mot banni, aucun emoji, domaine reflex-ia.com ; `node qa.cjs` vert (126 instants rendus contrôlés : zones sûres, texte déclaré, nombres autorisés, ≤ 34 mots visibles hors légendes).

## Vérifications faites / limites
- Faites : transcription inverse de chaque phrase (similarité ≥ 0,98) et du **mixage final** (0,993) ; −14,1 LUFS intégré, crête −1,2 dBFS ; H.264 High, yuv420p, faststart ; une seule image fixe > 1,2 s (1,5 s, vers 90 s).
- Quelques phrases courtes sont ralenties de 6 à 20 % (`tempo` dans `story.json`) parce que la synthèse les lisait à plus de 5 mots/s.
- **Non faites (je ne peux pas écouter ni voir l'app Instagram)** : le rendu dans Instagram, le goût de la voix et de la nappe, la prononciation de « Claude Code » et de « reflex-ia point com » (à écouter). Zones sûres = valeurs TikTok du dépôt, non officielles pour Reels.

## Rejouer
```
python3 -I tts.py <dossier_de_travail>      # voix (cache par phrase) + vérification par transcription
python3 -I plan.py                          # timeline.json / timeline.js
NODE_PATH=$(npm root -g) node qa.cjs        # contrôle
NODE_PATH=$(npm root -g) node events.cjs && node synth.cjs <dossier_de_travail>
NODE_PATH=$(npm root -g) node render.cjs --out out/reel-histoire-muet.mp4 --frames <dossier_images>
python3 -I mix.py <dossier_de_travail> out/reel-histoire-muet.mp4 out/reel-histoire.mp4
```
