# Exemple complet : le film de lancement Product Hunt de Dropit (octobre 2026)

Dépôt `harimalal/dropit`, dossier `MISSIONS/2026-10-13-product-hunt/livrables/` :
- `video/scene.html` — la scène complète (104 s), à lire pour le code poli de chaque type de scène.
- `scripts/capture-app.js` — captures de la vraie app anglaise avec données et IA simulées.
- `scripts/montage-60s.cjs`, `scripts/voix-off.cjs`, `scripts/rendre-video.js` — versions d'origine des scripts de ce skill.
- `video/dropit-launch-film-60s.mp4` (voix + sous-titres), `video/dropit-launch-film.mp4` (long, muet), `video/voix/` (prise et horodatage).
- `decisions.md` de la mission : tous les retours de l'utilisateur, version par version.

## Le cas
- App : Dropit, app web de productivité guidée (« tu tapes un objectif, Dropit construit le chemin »). Marché : États-Unis, anglais américain.
- Personnage : Sarah. Cas : « Buy a house in the country by next summer ». Autres projets autour : semi-marathon, voyage à Hawaï, lancer un petit business (vraies photos des tuiles de la landing).
- Slogan : « Type a goal. Dropit builds the path. You make the next move. » puis « Stop planning, focus on doing. »

## Le storyboard (film long, 104 s)
| Temps | Acte | À l'écran | Texte |
|---|---|---|---|
| 0–2,8 | Accroche | Vraie photo de maison (tuile retouchée « Buy a house », 0 %) | Buy a house. / Where do you even start? |
| 2,8–10,6 | Problème | Tableur, mails, tâches en retard, calendrier, post-it, icônes à pastilles ; effondrement | Your goals live in spreadsheets, inboxes and sticky notes, and five productivity apps. / Still no plan. |
| 10,6–13,6 | Révélation | La goutte du logo tombe dans le trou et remonte | — |
| 13,6–18,4 | Promesse | — | Dropit isn't another ~~all-in-one app~~. / It's the path to your goals. (guided, step by step) |
| 18,4–24,9 | 01 | Téléphone entre ; zoom sur la barre ; saisie lettre par lettre ; toucher Envoyer | Type what you want. |
| 24,9–36,0 | 02 | Écran de construction (goutte qui tombe en boucle) ; plan dont les étapes apparaissent une à une ; zoom objectif puis étapes ; toucher Confirmer | Dropit turns it into a real plan. / Your goal, reformulated. / Clear steps. Real time estimates. |
| 36,6–41,3 | 03 | La nouvelle tuile se pose sur l'accueil | Your project, ready. |
| 41,3–49,1 | — | Projet : prochaine action ; catégories dépliées | Always know your next move. / Every step. Every task. Timed. |
| 49,1–54,5 | — | Toucher « Done », +2 pts s'envolent, anneau sur la progression | Check it off. Watch it add up. |
| 54,5–61,3 | Résultat | « 3 weeks later » ; progression 50 %, points | Ahead of pace. Not behind. / Every task earns bonus points. |
| 61,3–74,0 | 04 | Chat : « How do I get pre-approved? » puis « What are my 80/20 priorities? » | Stuck? Ask Dropit AI how. / Ask for your 80/20 priorities. |
| 74,0–79,2 | — | 5 bulles de questions | Ask Dropit AI anything that moves you forward. |
| 79,4–95,9 | Récap | Daily Brief / Priorities by project / Inspiration cards ; gros plans avec bulles | Every goal. One plan. Every day. |
| 95,9–104 | Fin | Logo, slogan, dropitapp.io, « Free. No ads. Works in your browser. » | Type a goal. Dropit builds the path. You make the next move. / Stop planning, focus on doing. |

## La version 60 s (61 s)
16 morceaux, vitesses de ×1 (accroche) à ×2 (chat), fin ralentie à ×1,15 ; coupe franche entre « next move » et « Check it off » (cadrages trop différents). Voix : 16 répliques, 128 mots, « Justin Case » (ElevenLabs, eleven_v4, consigne `[calm, warm, confident]`), découpée grâce à Scribe ; « 80/20 » dit « eighty-twenty ».

## Les itérations (ce qui a coûté des allers-retours)
1. v1 : ouverture sur la génération du plan, illustrations, « AI builds » → refusé : ouvrir sur la photo, vraies images, « Dropit ».
2. v2 : logo trop rapide, glitch sur l'écran de construction, pas de récapitulatif → goutte entière et lente, étapes progressives puis zoom, trois téléphones zoomés un par un.
3. v3 : titres + sous-titres qui se chevauchent sur les trois téléphones, bulles trop petites et inclinées, téléphone coupé sur la miniature → titre seul en badge, bulles blanches droites, téléphone complété.
4. v4 validée, puis version 60 s avec voix et sous-titres.
