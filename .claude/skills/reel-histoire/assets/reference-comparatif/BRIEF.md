# BRIEF — Reel « histoire » : Comment j'ai comparé les outils IA en 28 comparatifs (Comparatif Factory)
# Skill : reel-histoire (appmee, branche claude/skill-reel-histoire). Source lue en entier : artefact « Comparatif Factory » (https://claude.ai/artifact/KFxadDZ34RkUBiB6nQkPRm, 04/10/2026), croisé avec `SKILL_COMPARATIF_FACTORY.md`, `Comparatif Outils/PUBLISH_QUEUE_COMPARATIFS.md` et les 28 fichiers `src/content/blog/compare_*.md`.
# Statut : EN ATTENTE D'ACCORD. Rien n'est produit : ni voix, ni rendu, ni son.

## 1. Couverture
`out/couverture.png` : « Comment j'ai comparé les outils IA en **28 comparatifs** » · pastille « 6 cas d'usage chacun » · 28 carrés (un carré = un comparatif publié ; clair = août (17), violet = septembre (5), jaune = octobre (6)) · « Un tableau noté, des cas d'usage, des profils. »

## 2. Angle
> Choisir un outil IA, ce n'est pas lire dix sites qui se disent tous les meilleurs : c'est un tableau noté sur les mêmes critères, ce que les gens font vraiment avec chaque outil, et quel outil pour quel profil. Voici comment ces comparatifs sont fabriqués, et à quoi ils ressemblent.

## 3. Hook (les 2 premières phrases, mot pour mot)
| | Variante | Phrase 1 | Phrase 2 |
|---|---|---|---|
| A | promesse | « Comment choisir un outil IA sans lire dix sites ? » | « J'ai fait vingt-huit comparatifs, avec un tableau noté pour chacun. » |
| B | chiffre | « Vingt-huit comparatifs d'outils IA. » | « Chacun avec un tableau, six cas d'usage et des profils. » |
| C | renversement | « Chaque outil IA se dit le meilleur. » | « Le tableau, lui, les note tous sur les mêmes critères. » |

**Recommandée : C → A → B.** Le renversement parle au spectateur, A nomme le sujet, B apporte la preuve chiffrée. (C affirme « les mêmes critères » : vrai pour un comparatif donné, 4 critères de notation par comparatif ; pas d'un comparatif à l'autre.)

## 4. Situation (le spectateur, à la 2e personne)
> Tu cherches un outil IA ? Chaque site se dit le meilleur, et tu ne sais pas lequel est fait pour ton cas.

(Tournure rhétorique, pas un fait mesuré : à garder, adoucir ou retirer.)

## 5. Schéma narratif (≈ 80 s, plafond 90 s)
| Étage | En une ligne | Durée |
|---|---|---|
| Problème | Chaque outil se dit le meilleur ; dix sites à lire pour choisir | ≈ 12 s |
| Système | Un moteur : une source déjà notée (4 critères, score sur 20, prix, avis), reformatée en 10 sections, QA, build vert avant mise en ligne ; jamais de donnée inventée (règle) | ≈ 15 s |
| Tableau | Vraie capture : outils classés par score, prix, avis, verdict | ≈ 12 s |
| Cas d'usage | Vraie capture : « ce que créent les utilisateurs », 6 cartes par comparatif | ≈ 10 s |
| Profils | Vraie capture : « recommandations par profil », 6 à 8 profils (freelance, agence, équipe sales…) | ≈ 10 s |
| Chiffres + limites | 28 comparatifs, 6 cas d'usage et 6 à 8 profils chacun ; scores = notation de la source, pas un test indépendant | ≈ 12 s |
| Appel | formule des reels précédents | ≈ 7 s |

Motifs (catalogue du skill, sans répétition) : titre + logo ; cartes (problème) ; liste d'étapes (système) ; défilé de captures réelles par élément (tableau, cas d'usage, profils) ; grille de carrés + compteurs ; CTA.

## 6. Chiffres autorisés et sources
| Nombre | Ce qu'il mesure | Source | Statut |
|---|---|---|---|
| 28 | comparatifs publiés (tous `compare_*`, tous `format: "guide"`, du 02/08 au 23/10/2026 ; 17 en août, 5 en septembre, 6 en octobre) | comptage de `src/content/blog/` | mesuré |
| 6 | cas d'usage par comparatif (cartes `cmp-content-card`) = 168 | comptage par motif HTML | mesuré, identique dans les 28 |
| 6 à 8 | profils par comparatif (cartes `cmp-profile-card`) = 178 | comptage par motif HTML | mesuré |
| 6 à 20 | outils par tableau (228 lignes d'outils en tout) | comptage par motif HTML | mesuré ; un outil peut revenir dans plusieurs comparatifs |
| plus de 200 | outils différents nommés (213 dans le champ `outils` des 28 fichiers) | frontmatter | mesuré, à arrondir (« plus de deux cents ») ; noms non dédoublonnés à la main |
| 4 critères · score sur 20 | notation d'un comparatif | `SKILL_COMPARATIF_FACTORY.md`, captures | règle / mesuré par comparatif |
| 10 | sections de reformatage | skill | règle |

**Écartés (contradictions entre sources)** : « 1 comparatif par jour » (artefact) face à « 2 par jour, 18 h et 19 h » (en-tête de la file) : la cadence réelle est de 28 comparatifs en 82 jours, aucune des deux n'est reprise ; 25 « Publié le » dans la file (28 fichiers : certains viennent d'autres sources) ; « 80 % d'outils en commun = échec du build » (règle technique, non utile).

## 7. Ce que la vidéo n'affirmera pas
- Les **scores viennent de la notation des comparatifs sources** de Reflex IA (recherche web : notes G2/Capterra, prix, avis), **pas d'un test indépendant** des outils : dit en une phrase.
- **Affiliation** : les sources s'appellent `comparatif_affiliation_*` et 6 des 28 articles mentionnent des programmes d'affiliation (ex. une commission). Décision demandée : le dire à l'écran, ou seulement dans `SCRIPT.md`.
- Les prix et notes sont **datés d'août à octobre 2026** et peuvent avoir changé.
- Aucun résultat d'audience, de clics ou de revenus (le dépôt n'en contient pas).
- « Jamais de donnée inventée » est une **règle du moteur**, pas une garantie vérifiée ligne par ligne.

## 8. Durée, coût, ton
≈ 80 s · ≈ 16 phrases de voix facturées (Gemini TTS, modèle lite) · rendu local · aucune image générée (3 captures réelles par élément) · « tu » au spectateur, « je » pour le travail · voix Charon.
Captures prévues : le tableau comparatif, la grille « ce que créent les utilisateurs » et la grille « recommandations par profil » de 3 comparatifs de catégories différentes, prises sur le site construit en local ; regardées une par une avant usage.

## Décisions à trancher
1. **Playbook** : « Comparatif Factory » (retenu, lu en entier) ou « Le Grand Comparatif » / « Variantes format comparatif » (non lus) ?
2. **Hook** : C → A → B (recommandé), A d'abord ou B d'abord ?
3. **Affiliation** : la dire à l'écran (recommandé : une ligne dans la scène des limites) ou seulement dans SCRIPT.md ?
4. **« Par métier »** : les profils des comparatifs mêlent métiers et situations (freelance, agence, équipe sales, budget serré) : ton « par métier » = ces profils, ou veux-tu que je ne montre que les profils de type métier ?
5. **CTA** : même formule que les reels précédents ?
