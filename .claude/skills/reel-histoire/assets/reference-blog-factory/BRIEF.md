# BRIEF v2 — Reel « histoire » : Comment j'ai publié 81 articles de blog longs (Blog Factory)
# Skill : reel-histoire (appmee, branche claude/skill-reel-histoire). Source lue en entier : artefact « Blog Factory Playbook » (https://claude.ai/artifact/2zPTT5PxXuCEKXcEfbN2Ww, 23/08/2026), croisé avec `SKILL_BLOG_FACTORY.md`, `BLOG_FACTORY_PROCESSUS.md`, `AUTOMATION/blog_cron_prompt.md` et `AUTOMATION/production_log.md`.
# Statut : v2 après les réponses de Hari (histoire dictée). EN ATTENTE D'ACCORD sur le TEXTE (`TEXTE_A_VALIDER.md`) : rien n'est produit, ni voix, ni rendu, ni son. Captures réelles déjà prises (6 articles, `assets/captures/`).

## 1. Couverture
`out/couverture.png` v2 : « Comment j'ai publié **81 articles** de blog longs » · pastille « ≈ 5 000 mots chacun » · « Analyse en profondeur, structure adaptée au sujet. » ·  · 81 carrés (un carré = un article noté du journal ; jaune = 100/100 (6), violet = 90 à 96 (53), gris-violet = 82 à 89 (22)) · « 1 CARRÉ = 1 ARTICLE · NOTE AUTO-ÉVALUÉE — Recherche réelle, rédaction cadrée, audit. »

## 2. Angle
> Faire écrire un article par une IA, ce n'est pas lui dire « écris-moi un article » : c'est lui imposer un processus (chercher les vraies questions, récupérer de vraies données sourcées, rédiger avec une structure fixe, s'auditer) et lui interdire d'inventer un chiffre. Voici le processus, et ce qu'il a produit sur mon blog.

## 3. Hook (les 2 premières phrases, mot pour mot)
| | Variante | Phrase 1 | Phrase 2 |
|---|---|---|---|
| A | promesse | « Comment faire écrire ton blog par Claude Code, sans qu'il invente un seul chiffre ? » | « Avec un processus fixe, en cinq étapes. » |
| B | chiffre | « Quatre-vingt-un articles notés sur mon blog. » | « Tous écrits par Claude Code, avec le même processus. » |
| C | renversement | « Demander un article à une IA, c'est facile. » | « Le problème, c'est qu'elle invente. » |

**Recommandée : C → A → B** (le renversement parle au spectateur, A nomme le sujet et l'outil, B apporte la preuve).

## 4. Situation (le spectateur, à la 2e personne)
> Tu demandes un article à une IA ? Il sort lisse et générique, avec des chiffres que personne ne peut vérifier.

(Tournure rhétorique, pas un fait mesuré : à garder, adoucir ou retirer.)

## 5. Schéma narratif (≈ 80 s)
| Étage | En une ligne | Durée |
|---|---|---|
| Problème | L'IA écrit vite mais invente ; un blog demande des dizaines d'articles cohérents | ≈ 15 s |
| Situation | Ce que ça change : prix, notes, retours terrain doivent venir de sources réelles | ≈ 10 s |
| Solution | Un processus fixe en étapes 0 à 4 : questions réelles → recherche web réelle → rédaction cadrée (structure fixe de composants) → audit (note ≥ 80/100) → publication | ≈ 30 s |
| Process | Quatre skills qui encadrent l'IA (recherche, structure, voix humaine, SEO) ; un build qui doit passer avant toute mise en ligne ; une production planifiée de 2 articles par jour | ≈ 15 s |
| Résultat | 81 articles notés de 82 à 100, moyenne 91,3 ; **limites** : notes auto-évaluées, aucun résultat d'audience ; production ≠ indexation (285 pages non indexées sur 132 articles, reel précédent) | ≈ 15 s |

Motifs de scène proposés (catalogue du skill, aucun motif répété) : titre + logo ; cartes à pastille rouge (les problèmes) ; liste de coches en cascade (les étapes) ; trois cartes (les 4 skills) ; compteur + grille de 81 carrés par note (résultat) ; trois cartes vérifié / attendu / limite ; CTA.

## 6. Chiffres autorisés et sources
| Nombre | Ce qu'il mesure | Source | Statut |
|---|---|---|---|
| 81 | articles ayant une ligne « Publié — NN/100 » dans le journal | `AUTOMATION/production_log.md` (comptage) | mesuré par comptage |
| 82 à 100 · 91,3 | étendue et moyenne de ces notes | `production_log.md` (calcul) | **calcul** ; notes **auto-évaluées** (11 lignes l'indiquent explicitement, les autres n'ont pas de mention contraire) |
| 6 | articles à 100/100 | `production_log.md` | mesuré |
| 80 | seuil d'audit : en dessous, on corrige | `SKILL_BLOG_FACTORY.md` | règle |
| 5 000 mots | longueur visée par article | `SKILL_BLOG_FACTORY.md` (l. 158, 485), cron | règle, **pas une mesure** |
| 2 | articles par jour planifiés | `AUTOMATION/blog_cron_prompt.md`, `CLAUDE.md` | règle du cron, pas un résultat |
| 4 | skills (recherche, structure, voix, SEO) | artefact + `BLOG_FACTORY_SKILLS/` | mesuré |
| 132 | fichiers dans `src/content/blog/` (99 `blog_`, 28 `compare_`, 5 `article_`) | comptage du dépôt | mesuré ; inclut les comparatifs d'une autre fabrique |
| 285 sur 132 | pages non indexées sur articles (limite honnête) | reel SEO d'indexation (Search Console) | mesuré, source du reel précédent |

**Écartés** (contradictions entre sources) : « 23 articles, score moyen 89, 3 à 100/100, 5 clusters » (artefact figé au 23/08, remplacé par les chiffres du journal) ; « 4-6 h par article » et « ~45 k tokens » (artefact seul, incompatible avec 2 articles par jour) ; « 4 000+ mots » (artefact) face à « 5 000+ » (skill actuel).

## 7. Ce que la vidéo n'affirmera pas
- « Sans rien inventer » est une **règle imposée au processus** (phase 1 : pas de donnée non retrouvée), pas une garantie vérifiée article par article : dit comme règle, jamais comme résultat.
- Les notes sont **auto-évaluées** par Claude pendant la phase d'audit, pas par un lecteur ni par Google. Dit à l'écran.
- Aucune affirmation de trafic, de classement ou de revenus (le journal n'en contient pas).
- « Zéro intervention » : non repris (le document de processus prévoit des validations, l'artefact dit qu'elles sont supprimées depuis août : sources divergentes).
- Le nombre de phases : l'artefact écrit « 4 phases » mais décrit les phases 0 à 4, donc cinq étapes (la 3 et la 4 sont regroupées sur son schéma). La vidéo dira « cinq étapes ».

## 8. Durée, coût, ton
≈ 80 s · ≈ 20 phrases de voix facturées (Gemini TTS, modèle lite si le quota du principal est atteint) · rendu local · aucune image générée · « tu » au spectateur, « je » pour le travail · voix Charon · à écouter après production : « Claude Code », « Reddit », « G2 », « Capterra ».
Visuels réels disponibles : la structure du processus ; **pas de capture d'article** prévue sauf si tu en fournis (la grille de 81 carrés vient du journal).

## Décisions à trancher
1. **Quel playbook ?** J'ai pris « Blog Factory Playbook » (23/08/2026). Les artefacts « Blog Factory » et « Workflow Blog Factory » (23/10/2026) sont plus récents : veux-tu l'un d'eux à la place ?
2. **Hook** : C → A → B (recommandé), A d'abord, ou B d'abord ?
3. **Résultat** : « 81 articles notés, moyenne 91 » avec la mention « notes auto-évaluées » à l'écran (recommandé), ou on retire les notes et on ne garde que le processus ?
4. **La limite** (« production ≠ indexation, 285 pages non indexées ») : la garder pour la fin, ou ne pas en parler ?
5. **CTA** : même formule que les deux reels précédents (« Abonne-toi pour plus d'astuces IA : sans compétences techniques, rapides, et terriblement efficaces »), ou un autre appel ?
6. **Titre de la couverture** : « Un blog écrit par Claude Code, sans rien inventer » te convient-il ?

---
## v2 — Ce que Hari a décidé (réponses dictées)
- Playbook : « Blog Factory Playbook » (23/08/2026).
- Histoire : titre « Comment j'ai publié 81 articles de blog longs » → problème (sujet, angle, contenu, références ; des jours à la main ; une IA donne un texte moyen) → système (skills + système complet : professionnel, complet, valeur profonde, **reproductible d'un article à l'autre**, structure adaptable) → **chiffres puis exemples** (vraies captures de pages qui défilent) → appel.
- Hook : ouvrir par le titre (il a écarté les variantes A/B/C du brief v1). CTA non précisé : même formule que les reels précédents (à confirmer).
- Non repris à l'écran : la limite d'indexation (reste dans SCRIPT.md).

## v2 — Captures réelles (aucune image générée)
Site construit en local (`npm run build` vert, 164 pages), 6 articles notés 96 à 100/100, 540 px de large (rendu mobile), 4 200 px de haut chacun : Runway vs Kling vs Veo 3 (100), Make vs n8n (96), Taskade pour freelances (100), Surfer SEO vs Frase vs MarketMuse (96), Make AI Agents (100), Writesonic meta descriptions en masse (100). Les 6 pages ont été relues : titres, chapô et corps réels.

## v2 — Chiffres autorisés
81 · ≈ 5 000 mots (comptage approximatif) · 82 et 100 (étendue des notes auto-évaluées) · 5 « cinq mille ». Écartés : 23 / 89 / 4-6 h (artefact du 23/08), 132 (fichiers, comparatifs inclus), « zéro intervention ».

---
## v3 — Demandes suivantes de Hari
Titre « Comment j'ai publié **64 articles de blog en deux mois** » (août-septembre, mesuré ; les 81 notés courent sur 5 mois) ; le SEO (ce que cherche l'utilisateur, mots-clés, angle original) entre dans le problème ; la scène « système » devient la liste des cinq étapes avec audit et boucle de correction ; durée < 90 s (82,1 s). Texte validé : `TEXTE_A_VALIDER.md` ; sources et limites : `SCRIPT.md`. Chiffres autorisés : 64, ≈ 5 200, 85 à 100 ; plus de 81.
