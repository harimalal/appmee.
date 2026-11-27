# BRIEF v2 — Reel « histoire » : créer des carrousels automatiquement (ta charte, ton point de vue, ta maquette)
# Skill : reel-histoire. Sources primaires : `CONTENT_FACTORY/carrousel/LOG_CARROUSELS_IA.md`, `ETUDE_MODELES_IMAGE.md`, `depenses-images.json`, `SKILL_CAROUSEL_FACTORY_V3.md` ; synthèse : artefact « Atelier carrousels IA ».
# Statut : EN ATTENTE D'ACCORD sur 3 points (voir « Décisions »). Rien n'est produit : ni voix, ni rendu, ni son.
# Cette version remplace la v1 (« 6 carrousels pour 4,94 € ») : nouvel angle donné par Hari.

## 1. Couverture
`out/couverture.png` : « Créer des carrousels automatiquement » (« automatiquement » surligné) · pastille « 0,051 € la slide avec image » · 62 carrés en 6 groupes (un carré = une slide réelle) · « 62 SLIDES · 6 CARROUSELS RÉELS — Ta charte, ton point de vue, ta maquette. »

## 2. Angle
> Un système qui fabrique des carrousels à la chaîne, un par article, selon **ta charte graphique, ton point de vue et ta maquette** : 0 € d'images si c'est du texte, environ 1 € avec des images. Voici le problème, le système, ce qu'il faut au minimum, puis les carrousels obtenus.

## 3. Histoire (les 7 scènes)
| # | Scène | Contenu | Sourcé ? |
|---|---|---|---|
| 1 | **Titre** | « Comment créer des carrousels automatiquement, avec ta charte, ton point de vue et ta maquette ? » + « 0 € d'images pour du texte, environ 1 € avec des images » | oui (coûts : voir §5) |
| 2 | **Les problèmes** (3 cartes barrées) | outils de carrousel IA · Canva · Claude Code sans méthode | **1 sur 3 seulement** (voir ci-dessous) |
| 3 | **Le système** | un skill qui fabrique le carrousel depuis un article ; 3 verrous : charte (bible de style), point de vue (fiche de position), maquette (modèles de référence) ; un carrousel par article | oui (SKILL V3) |
| 4 | **Les coûts** | texte seul 0 € d'images ; 0,051 € la slide avec image ; ≈ 1 € le carrousel (0,51 à 1,26 €) ; 6 carrousels = 62 slides = 4,94 € | oui |
| 5 | **Le minimum, puis les outils** | minimum : un article, ton point de vue, ta charte, un modèle d'image, un contrôle slide par slide ; outils : Claude Code, connecteur ElevenLabs (modèle `gpt-image-2.5-sunburst`), Python (Pillow, NumPy, OpenCV) pour coller les vrais logos | oui (SKILL V3, « Prérequis ») |
| 6 | **Les exemples en défilement** | vraies slides des 6 carrousels qui défilent comme dans Instagram (swipe, 1080×1350) puis comme un PDF LinkedIn | oui (62 PNG réels + PDF) |
| 7 | **CTA** | « Abonne-toi pour plus d'astuces IA… » | formule de Hari |

### Les trois « problèmes » : ce que les sources établissent
- **Claude Code sans méthode** : le premier carrousel (Shorts IA) a perdu **≈ 55 % de ses crédits en essais** (argile refusée, HTML refusé, `gpt-image-2` trop cher à 0,195 € la slide) ; la méthode écrite a ensuite ramené la perte à 0–8 % sur 3 carrousels, mais **50 % et 31 %** sur les deux autres (refontes demandées). → dit tel quel : « 0 à 55 % de pertes selon le carrousel ».
- **Outils de carrousel IA** : **aucune source dans le dépôt** (aucun de ces outils n'a été testé dans le journal). Ce qui est établi : le texte généré par une IA d'image se trompe (faux chiffres d'analytics et texte anglais sur une slide, « AdCreative,ai » sur une couverture, un « 39 » dont le 9 était inversé) et les logos sont inventés tant qu'on ne colle pas les vrais.
- **Canva** : **aucune source** (Canva n'apparaît que comme un logo dans le carrousel « pubs IA »). Je ne peux pas écrire un « problème avec Canva » sans votre formulation exacte.

## 4. Hook
A (titre : promesse) → C (les problèmes, renversement) → B (62 slides, 4,94 €, dans la scène coûts). C'est le schéma 1 du premier brief, appliqué à la nouvelle histoire.

## 5. Chiffres autorisés et sources
| Nombre | Ce qu'il mesure | Source | Statut |
|---|---|---|---|
| 0 € | images pour un carrousel **texte seul** (gabarit HTML V2, sans image) | SKILL V2/V3 | vrai pour les images ; le texte est écrit par Claude (abonnement), non chiffré |
| 0,051 € · 255,84 crédits | une slide `gpt-image-2.5-sunburst` 4:5 1K haute | ETUDE_MODELES_IMAGE.md | mesuré (0,0002 €/crédit, prix renvoyés par ElevenLabs) |
| 0,51 à 1,26 € | coût réel par carrousel de 8 à 11 slides (le moins cher : outils GEO ; le plus cher : shorts IA) | ETUDE §4 | mesuré |
| ≈ 0,56 € | 11 slides du premier coup (11 × 0,051) | **calcul** | dérivé, signalé comme tel |
| 6 · 62 · 4,94 € | carrousels · slides · dépense d'octobre | LOG, `depenses-images.json` | mesuré |
| 55 % · 8 % · 50 % · 31 % | part des crédits perdue en essais (carrousels 1, 2, 4, 5) | ETUDE §4 | mesuré |
| 0,195 € | slide `gpt-image-2` (essais, trop cher) | ETUDE | mesuré |

**« Moins d'un euro avec des images »** n'est vrai que pour 4 carrousels sur 6 (0,51 ; 0,61 ; 0,61 ; 0,82 €) ; les deux autres coûtent 1,13 et 1,26 €. Formulation proposée : « environ un euro, de 0,50 € à 1,30 € ».
**« À l'infini »** : non chiffré ; proposé : « un carrousel par article, à la chaîne ».

## 6. Ce que la vidéo n'affirmera pas
- Aucun résultat d'audience (vues, clics, abonnés) : le journal n'en contient pas.
- Rien sur les capacités de Canva ou des outils de carrousel IA tant que vous n'avez pas fourni la formulation.
- Les logos des premiers carrousels étaient des imitations ; les vrais logos viennent de l'étape de collage (dit si les slides montrées en contiennent).
- « Sans compétences techniques » (CTA) : le process montré utilise Claude Code et un peu de Python ; à concilier (voir décision 3).

## 7. Durée, coût, ton
≈ 85 s · 17 phrases de voix facturées (Gemini TTS) · rendu local · aucune image générée (les slides montrées existent déjà) · « tu » au spectateur, « je » pour le travail · voix Charon.

## Décisions (3 points bloquants)
1. **Les problèmes** : garder « outils de carrousel IA » et « Canva » avec **vos** formulations (je les écris telles quelles et je signale qu'elles viennent de vous), ou les remplacer par les échecs **sourcés** (faux chiffres et texte anglais, logos inventés, HTML plat refusé) ?
2. **Le prix** : « environ un euro (de 0,50 à 1,30 €) » (exact) ou « moins d'un euro » (vrai pour 4 carrousels sur 6) ?
3. **Le CTA** : même formule que Tri Watch Later (« sans compétences techniques, rapides, et terriblement efficaces »), alors que le process cite Claude Code et Python ?
