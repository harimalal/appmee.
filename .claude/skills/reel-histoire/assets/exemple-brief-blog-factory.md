# EXEMPLE — brief rempli : reel « Comment j'ai publié 64 articles de blog en deux mois » (4e essai du skill)
# Playbook ancien + dépôt plus récent + utilisateur qui dicte l'histoire en plusieurs vagues. Méthode : `references/source-vers-storyline.md` (section 7). Implémentation : `assets/reference-blog-factory/`.

## 1. Couverture
« Comment j'ai publié **64 articles** de blog en deux mois » · pastille « ≈ 5 200 mots chacun » · 64 carrés (un carré = un article noté du journal ; jaune = 100/100, violet = 90 à 99, gris-violet = 85 à 89) · « Pensés pour le SEO : intention, mots-clés, angle original. » Refaite à chaque changement de titre ou de chiffre.

## 2. Angle
Écrire un article de blog avec une IA, ce n'est pas lui demander « écris un article » : c'est penser le SEO (ce que cherche l'utilisateur, la stratégie de mots-clés, un angle original) et lui faire suivre un système en étapes avec un audit et une boucle de correction.

## 3. Histoire (ordre dicté ; 82 s, plafond 90 s)
| Scène | Contenu | Motif | Sourcé ? |
|---|---|---|---|
| titre | « Comment j'ai publié 64 articles de blog en deux mois ? » + « articles longs, pensés pour le SEO » | titre + logo + pastilles | 64 : journal (1er août au 30 septembre) |
| problème | Penser le SEO (intention, mots-clés, angle original), à la main : des jours, une IA : un texte moyen | cartes + puces | **dit par l'utilisateur** |
| étapes | 5 étapes : questions réelles, recherche web réelle, rédaction, audit (< 80 : on corrige), publication (si le build passe) | liste en cascade + boucle | `SKILL_BLOG_FACTORY.md` (règles) |
| chiffres | même processus ; 64 articles ; ≈ 5 200 mots ; notes 85 à 100 **auto-évaluées** | grille de carrés + cartes | journal, comptage de mots |
| exemples | 6 vraies pages du blog qui défilent | défilé de pages réelles | captures du site construit en local |
| appel | formule de l'utilisateur | CTA nuit | — |

## 4. Ce que les sources établissent / ce qui vient de l'utilisateur
| Idée | Source | Traitement |
|---|---|---|
| 64 articles du 01/08 au 30/09 (sur 81 notés, de mai à octobre) | journal, comptage par dates | « en deux mois » = ces 64 ; recalculer notes et mots sur eux |
| Cinq étapes, cinq critères, seuil 80, boucle de correction | skill | dit comme **règle** |
| Notes 85 à 100 | journal | **auto-évaluées** (mention à l'écran) |
| Le SEO se pense d'abord ; des jours à la main ; texte moyen d'une IA | aucune | mots de l'utilisateur, signalés |
| « Les audits ont corrigé le skill » | corrections datées dans le skill | écran seulement, sans nombre |

## 5. Écartés
23 articles, moyenne 89, 4-6 h, ~45 000 tokens (artefact figé au 23/08) ; 81 articles (5 mois) ; 132 fichiers (comparatifs inclus) ; « zéro intervention ».

## 6. Ce que la vidéo n'affirmera pas
Aucune donnée d'audience ni de classement ; production ≠ indexation (285 pages non indexées, reel SEO) ; la boucle d'audit est une règle (pas de nombre de corrections) ; les 6 pages sont choisies parmi les mieux notées.

## 7. Durée, coût, ton
82,1 s · 18 phrases (13 générées pour la V2, 5 reprises du cache, 3 régénérées après la transcription de contrôle) · voix Charon, modèle lite · « tu » au spectateur, « je » pour le travail.

## Décisions posées à l'utilisateur
1. Quel playbook ? 2. Hook : ouvrir par le titre. 3. « En 2 mois » : 64 articles (recommandé), 81 sans durée, ou les deux. 4. Texte validé avant la voix (deux fois : V1 et V2).
