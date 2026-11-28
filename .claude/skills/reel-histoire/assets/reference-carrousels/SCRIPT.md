# SCRIPT — Reel « Créer des carrousels automatiquement » (v2, 56,7 s, 1080×1920, 30 fps)

Version 2 : les scènes « coûts » et « minimum / outils » (6 phrases) ont été retirées sur demande de Hari ; la version longue (84,7 s) est gardée localement (`out/reel-carrousels-ia-long.mp4`, non versionnée).

Skill : reel-histoire. Voix : Google Gemini TTS, voix Charon, modèle `gemini-3.8-flash-lite-tts` (le modèle `gemini-3.8-flash-tts` avait atteint son quota du jour). Rendu 100 % local, aucune image générée pour la vidéo.

## Texte lu (11 phrases)
t1 Comment créer des carrousels automatiquement, avec ta charte, ton point de vue et ta maquette ?
t2 Zéro euro d'images pour du texte, moins d'un euro avec des images.
p1 Faire un carrousel à la main, c'est galère : ça prend des heures.
p2 Avec les outils IA, la personnalisation est basique et le rendu moyen, même sur Canva.
p3 Et Claude Code sans méthode, ce sont des essais à répétition : cinquante-cinq pour cent de mes crédits partis en essais sur le premier carrousel.
s1 Avec ce système, c'est simple : tu donnes ta source, une URL de blog ou une vidéo.
s2 L'IA te donne l'angle, le texte et les images.
s3 Tu donnes un modèle de carrousel que tu aimes, et ta charte et ton point de vue font le reste.
e1 Voilà ce que ça donne, comme ça défile sur Instagram.
e2 Et sur LinkedIn, en PDF.
k1 Abonne-toi pour plus d'astuces IA : sans compétences techniques, rapides, et terriblement efficaces.

## Sources des nombres
| Nombre | Source | Statut |
|---|---|---|
| 0 € d'images (texte seul), phrase t2 | `SKILL_CAROUSEL_FACTORY_V2/V3` (gabarit HTML sans image) | vrai pour les images ; le texte est écrit par Claude, non chiffré |
| « moins d'un euro avec des images » (t2, sans « en moyenne » ; plus de scène coûts à l'écran) | 4,94 € ÷ 6 = 0,82 € (`depenses-images.json`) | **calcul, vrai en moyenne seulement** ; 2 carrousels sur 6 dépassent 1 € (1,13 et 1,26 €), 4 sont sous 1 € (0,51 ; 0,61 ; 0,61 ; 0,82) |
| 0,051 € la slide (pastille de la couverture, non lue) | `ETUDE_MODELES_IMAGE.md` : 255,84 crédits × 0,0002 € | mesuré |
| 62 slides, 6 carrousels (carrés de la couverture) | `LOG_CARROUSELS_IA.md` | mesuré |
| 55 % des crédits perdus en essais | `ETUDE_MODELES_IMAGE.md` §4 (premier carrousel) | mesuré, vaut pour le 1er carrousel seulement (les autres : 0–8 %, 50 %, 31 %) |

## Ce qui vient de Hari, non sourcé dans le dépôt
- « À la main, c'est galère, ça prend des heures » ; « outils IA : personnalisation basique, rendu moyen, même sur Canva » : son expérience, aucun test de ces outils n'est dans le journal.
- « Une vidéo » comme source : seuls des articles de blog ont été exercés dans le journal.
- « Moins d'un euro » : tenu uniquement en moyenne (voir ci-dessus).
- CTA « sans compétences techniques, rapides, et terriblement efficaces » : formule de Hari.
- « Zéro euro / moins d'un euro » conservé dans la phrase d'ouverture sur décision de Hari : la scène qui l'étayait a été retirée (voir limites).

## Contrôles
QA contenu/mise en page : vert · −14,2 LUFS (crête −1,3 dBFS) · 0 image figée > 1,2 s · transcription du mixage final : similarité 0,977 par mots (écarts : « d'images » non entendu dans t2 par la transcription, singuliers/pluriels) · aucune requête de synthèse vocale nouvelle (cache).

## Limites
- Son non écouté par moi ; à vérifier : « Canva », « Claude Code », « LinkedIn ».
- Rendu Instagram non testé sur le téléphone.
- **« Moins d'un euro avec des images » n'est plus étayé à l'écran** : vrai en moyenne (0,82 €), 2 carrousels sur 6 coûtent 1,13 et 1,26 €. Option : ajouter « en moyenne » à t2 (1 phrase à régénérer).
- Les slides montrées sont les vraies (2 par carrousel, 12 au total), pas les 62.
- Aucune donnée d'audience (vues, clics) : le journal n'en contient pas.
