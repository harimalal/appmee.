# BRIEF — Reel « histoire » : le SEO d'indexation avec Claude Code (EXEMPLE rempli, tel qu'il aurait dû être présenté)
# Reconstitué le 2026-11-26 d'après le reel livré (`CONTENT/2026-11-26_reel-seo-indexation/histoire/`). Sert de modèle : c'est le niveau de précision attendu avant « go ».

## 1. Couverture
`CONTENT/2026-11-26_reel-seo-indexation/histoire/out/couverture.png` (1080×1920, texte dans le carré central 1080×1080).
Titre : « Comment optimiser le SEO de ton site avec Claude Code ? » (SEO surligné, Claude Code en violet) · pastille noire « 1 seule commande » · terminal avec le vrai fichier de consigne `prompt-claude-code-indexation-reflex-ia.md` · mention : « Pas tes articles. L'indexation. » · logo Claude en haut à droite.

## 2. Angle
> Si ton site est mal vu de Google, ce n'est probablement pas la qualité de tes articles : ce sont des pages que Google n'a pas (ou mal) indexées — et on peut le corriger depuis le code, avec une seule consigne donnée à Claude Code.

## 3. Hook
| | Variante | Phrase 1 | Phrase 2 |
|---|---|---|---|
| A | promesse | « Comment optimiser le SEO de ton site avec Claude Code ? » | « Tout automatique, en une seule commande. » |
| B | chiffre paradoxal | « Sur mon blog : 285 pages non indexées. » | « Pour 132 articles. » |
| C | renversement | « Ton site n'est pas référencé sur Google ? » | « Ce n'est pas parce que tes articles sont mauvais. » |

**Recommandée : A, enchaînée sur C, puis B comme preuve.** A annonce le sujet et l'outil dès la première seconde (la v1, qui s'ouvrait sur un chiffre seul, n'était pas comprise) ; C fait le renversement qui retient ; B apporte la preuve.

## 4. Situation
> Tu as un site, mais il n'est pas référencé sur Google ? Ce n'est pas parce que tes articles sont mauvais. Ni parce que ta boutique est mal faite. C'est parce que tes pages sont mal indexées, ou pas du tout.

## 5. Schéma narratif
| Étage | En une ligne | Durée |
|---|---|---|
| Problème | Le titre, la promesse, le renversement « pas tes articles » | ≈ 15 s |
| Situation | 285 pages non indexées sur 132 articles ; mots-clés vs indexation ; ça se voit dans la Search Console, qui donne le nombre, pas la cause | ≈ 25 s |
| Solution | Trois causes « bêtes » : deux adresses par page (slash final), filtres du menu qui fabriquent de fausses pages, fichier de recherche qui change de nom (404) ; 9 articles vus mais pas indexés, reliés | ≈ 30 s |
| Process | 5 corrections, 1 commit chacun, ≈ 23 minutes | ≈ 6 s |
| Résultat | Avant/après 140→0, 23→0, 1→0, 0→27 ; site corrigé et vérifié ; réponse de Google attendue le 8 décembre ; objectif 155–160 | ≈ 20 s |

## 6. Chiffres autorisés et sources
| Nombre | Ce qu'il mesure | Source | Statut |
|---|---|---|---|
| 285 | URLs non indexées listées par la Search Console (variantes, 404 et redirections comprises) | rapport GSC du 10/11/2026 | mesuré |
| 132 | articles du blog | décompte des articles publiés | mesuré |
| 66 | URLs « Autre page avec balise canonique correcte » | rapport GSC du 10/11/2026 | mesuré |
| 140 → 0 | adresses sans slash final à corriger | mesure de build avant/après (`PLAYBOOK/2026-11-seo-indexation-gsc/`) | mesuré (build) |
| 23 → 0 | liens de filtres `?f=` | idem | mesuré (build) |
| 1 → 0 | fichier de recherche qui change de nom | idem (deux vraies mises en ligne : `0a086143` → `d7b4d2ce`) | mesuré (build) |
| 0 → 27 | liens vers les 9 articles « explorés, non indexés » | idem | mesuré (build) |
| 9 · 5 · ≈ 23 min | articles ciblés · corrections · durée du travail | playbook / journal de session | mesuré |
| 8 décembre | date où l'effet sur Google sera lisible | playbook | attendu |
| 155 à 160 | pages indexées visées | playbook | **objectif** (pas un résultat) |

Écartés (sources contradictoires) : « 10 pages canonical », « 6 liens restants ».

## 7. Ce que la vidéo n'affirmera pas
- Aucun gain d'indexation : « corrigé et vérifié » vaut pour le site (build) ; l'effet côté Google est annoncé pour le 8 décembre.
- « 285 pages » ≠ 285 articles (ce sont des URLs, variantes comprises) : le hook l'oppose à 132 articles.
- « Tout automatique, en une seule commande » vaut pour les corrections du code (un fichier de consigne, 5 commits, ≈ 23 min), pas pour l'effet Google ni la vérification.

## 8. Durée, coût, ton
- Durée cible : 95 s · 31 phrases de voix facturées (Gemini TTS ; ElevenLabs, vidIQ, Picsart : 0) · rendu local.
- Voix Google (Charon) · « tu » au spectateur, « je » pour le travail.
- À écouter : « Claude Code », « un commit chacun », « reflex-ia point com ».

## Décisions à trancher
1. Le hook recommandé (A → C → B) convient-il ?
2. Garde-t-on « Tout automatique, en une seule commande », ou une formule plus prudente (« les corrections du code en une seule commande ») ?
3. Logo : l'étoile Claude du dépôt suffit-elle, ou fournis-tu le logo Claude Code officiel ?
