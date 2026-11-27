# EXEMPLE — brief rempli : reel « Créer des carrousels automatiquement » (3e essai du skill)
# Ce brief montre une histoire DICTÉE par l'utilisateur, à partir de quatre pièces (artefact de synthèse, journal, étude, fichier de dépenses). Méthode : `references/source-vers-storyline.md`. Implémentation : `assets/reference-carrousels/`.

## 1. Couverture
`out/couverture.png` : « Créer des carrousels automatiquement » (« automatiquement » surligné) · pastille « 0,051 € la slide avec image » · 62 carrés en 6 groupes (un carré = une slide réelle) · « 62 SLIDES · 6 CARROUSELS RÉELS ».

## 2. Angle
Un système qui fabrique des carrousels à la chaîne, un par article, selon **ta charte, ton point de vue et ta maquette**. Voici les problèmes, le système, puis les carrousels obtenus.

## 3. Histoire (ordre dicté par l'utilisateur ; v2 après élagage : 5 scènes, 56,7 s)
| # | Scène | Motif | Sourcé ? |
|---|---|---|---|
| 1 | Titre : « Comment créer des carrousels automatiquement… ? » + « zéro euro d'images pour du texte, moins d'un euro avec des images » | titre + logo + pastilles | oui (coûts) ; « moins d'un euro » = en moyenne |
| 2 | Problèmes : à la main · outils IA / Canva · Claude Code sans méthode | cartes à pastille rouge | **1 sur 3** : les 2 autres viennent de l'utilisateur |
| 3 | Système : tu donnes ta source (URL de blog ou vidéo) → l'IA donne angle, texte, images → tu donnes un modèle ; charte et point de vue | 3 cartes + puces | oui (skill V3) ; « vidéo » non exercée |
| 4 | Exemples : vraies slides en défilement (Instagram, puis PDF LinkedIn) | téléphone qui défile | oui (62 PNG réels) |
| 5 | Appel final (même formule que le reel précédent) | CTA nuit | formule de l'utilisateur |
Scènes retirées sur demande (v1 → v2) : « coûts » (0 €, 0,051 €, 4,94 € pour 62 slides) et « minimum / outils ».

## 4. Ce que les sources établissent / ce qui vient de l'utilisateur
| Idée | Source | Traitement |
|---|---|---|
| Claude Code sans méthode : ≈ 55 % des crédits perdus en essais (1er carrousel) | étude des modèles §4 | dite telle quelle, limitée au 1er carrousel |
| Outils de carrousel IA : personnalisation basique ; Canva : rendu moyen | **aucune** | mots de l'utilisateur, signalés « son expérience », rien sur les capacités réelles |
| À la main : galère, des heures | **aucune** | idem |
| Une vidéo comme source | non exercée (seuls des articles) | dite, signalée en limite |
| Moins d'un euro avec des images | 4,94 € ÷ 6 = 0,82 € ; 2 carrousels sur 6 > 1 € | « en moyenne » si une scène chiffrée la porte ; sinon signalé en limite |

## 5. Chiffres autorisés
0 (images d'un carrousel texte seul) · 1 · 55 (% de crédits, 1er carrousel) · 62 · 6 · 0,051 € (couverture seulement) ; tout autre nombre est refusé par `qa.cjs`.

## 6. Ce que la vidéo n'affirmera pas
Aucun résultat d'audience ; rien sur les capacités de Canva ou des outils IA ; rien sur les vidéos comme source tant qu'elles n'ont pas été exercées.

## 7. Durée, coût, ton
≈ 57 s (v2) · 11 phrases de voix · voix Charon, modèle de repli `gemini-3.8-flash-lite-tts` si le quota du principal est atteint · « tu » au spectateur, « je » pour le travail.

## Décisions posées à l'utilisateur
1. Problèmes : ses mots ou des échecs sourcés ? 2. Prix : « environ un euro » exact ou « moins d'un euro » ? 3. CTA : même formule que le reel précédent ?
