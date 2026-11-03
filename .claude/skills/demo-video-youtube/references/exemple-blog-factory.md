# Exemple : « Démo Blog Factory » (29 octobre 2026)

https://claude.ai/artifact/TiVRxcMY6qtqaNoSsTz4iN : comment le créateur publie jusqu'à 2 articles par jour sur Reflex IA (reflexi-ai.com) avec une usine à articles construite avec Claude. 132 articles, 615 000 mots, score qualité moyen 91/100. 23 slides, thème pastel avec du violet pâle en secondaire. Planche de design : https://claude.ai/artifact/GJiiVPVxaH1xnu7XFByv8x

## Ce qui a été appris

- **Une vidéo, un sujet.** La première version mélangeait la mise en place du site et la génération des articles. Le créateur a demandé de séparer : cette vidéo ne parle que du contenu. Le site devient une slide teaser et un appel au commentaire (« écris SITE en commentaire si tu veux la vidéo pour créer et déployer ce site avec Claude »), repris dans le bilan.
- **« Même style, mais… »** : quand le créateur veut le style de la démo précédente avec une autre couleur, on décline le thème pastel (`--vio`, fond de la pub) au lieu de refaire une planche.
- **La pub, c'est une revue du produit** : la page d'accueil qui défile, de vrais articles présentés en fiches (usage, sujet, titre, date), le nombre d'articles et leur diversité (barre par usage), l'angle et la valeur ajoutée, puis la newsletter avec un champ e-mail tapé.
- **Le temps, en gros** : à la main, les durées écrites dans le process (5 à 8 h par article) × 132 articles ≈ 660 à 1 050 h, écrit « estimation » ; avec la Blog Factory, 47 jours de publication. Rien sur le site, hors du périmètre.
- **La croissance vient des vraies dates** : la date de publication dans les métadonnées des 132 articles, cumulée par mois (3, 17, 17, 23, 75, 115, 132). Une courbe qui se dessine, puis un repère sur le décollage d'août.
- **Les données du dépôt plutôt que la mémoire** : composants, phases et durées, critères d'audit et leur poids lus dans le process (`SKILL_BLOG_FACTORY.md`), extraits réels du journal de production, sortie réelle de `npm run build`.

## Le récit

Accroche (la page blanche « Article n°1 sur 132 » et la liste de tout ce qu'il faut, « Et ça, 2 fois par jour ? ») → titre (le schéma du système flouté) → bénéfice (132 articles, 91/100) → pourquoi un blog en 2026 (mur des vrais titres) → les 16 composants → pour qui (+ bandeau) → **pub Reflex IA** (4 slides : le site, les fiches, l'angle, la newsletter) → un article à la main (tableur des 5 phases) → les solutions à la mode → « et si Claude suivait mon process ? » → la chaîne en 5 phases avec la boucle « sous 80, retour en rédaction » → les 12 pièces du système → le temps, en gros (+ teaser SITE) → la croissance → le détail : la recherche sans donnée inventée, un vrai article composant par composant, l'audit, le build → la suite (Content Factory, une prochaine vidéo) → bilan et appels à l'action.

## Techniques réutilisables

- Les données d'un site de contenu se tirent du frontmatter (titre, catégorie, sujet, usage, date) avec un petit script Python, injectées dans le JS comme `FICHES`, `USAGE`, `TITLES`.
- Courbe qui se dessine : chemin SVG avec `stroke-dasharray` et `stroke-dashoffset` qui passe à 0 quand l'élément reçoit `.on`.
- Caméra dans un long article capturé, le contenu à gauche et l'étiquette à droite : `[s, PX+x+w/2+340/s, y+400/s]`.
- Bulle de commentaire YouTube (`.ytc`) pour un appel au commentaire précis.
