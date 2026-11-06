# JOURNAL DES DÉCISIONS — prosens-site-vente

## 2026-11-06 — Décision #1 : promesse de la page (garantie de volume ou méthode transparente)
- Tour 1 — Stratège commercial : une garantie chiffrée de rendez-vous écrase la concurrence au premier regard — preuve : Belkins affiche « 100+ guaranteed appts / year » — coût : engagement à tenir — signal : si l'utilisateur peut la tenir par contrat.
- Tour 1 — Développeur et vérificateur : on ne publie que ce qui est vérifiable ; la garantie n'est pas étayée et le même acteur la nuance sur une autre page — preuve : page appointment-setting de Belkins (« can't guarantee instant results ») — coût : promesse moins spectaculaire — signal : un chiffre contractuel fourni.
- Tour 2 : le stratège accepte de ne pas garantir un volume mais veut une promesse forte. Troisième voie : promettre le **processus** (définition écrite du rendez-vous qualifié, rendez-vous confirmés dans l'agenda, closing assuré par un commercial senior) et laisser la place à une garantie chiffrée plus tard.
- CLÔTURE : promesse de méthode et de transparence, pas de garantie de volume — motif : fiable > évident > beau, puis réversibilité.
- Écarté : garantie chiffrée de rendez-vous (non étayée), baseline générique du type « boostez votre croissance » (non différenciante).
- Réversible : oui — une section et un titre à changer.

## 2026-11-06 — Décision #2 : intensité du mouvement
- Tour 1 — Directeur artistique : des sections qui vivent partout rendent la page mémorable — preuve : pages de produit très animées — coût : poids et complexité — signal : aucun problème de performance mesuré.
- Tour 1 — Développeur : peu d'animations, bien choisies — preuve : sobriété relevée sur Stripe, Linear, Vercel ; risques de performance et de référencement notés dans les guides — coût : moins de spectacle — signal : une animation qui sert la compréhension.
- Tour 2 : le directeur artistique accepte de concentrer l'effort sur un moment fort ; le développeur accepte des mouvements discrets d'entrée de section.
- CLÔTURE : un moment fort (le parcours du rendez-vous qui se remplit dans l'agenda) et des mouvements discrets ailleurs, version sans mouvement complète pour `prefers-reduced-motion` — motif : contrainte dure (page de vente rapide) puis fiable > évident > beau.
- Écarté : bibliothèque de scroll pour toute la page ; page statique sans mouvement (contraire à la demande).
- Réversible : oui — la technique peut passer à GSAP si le résultat est trop sobre.
