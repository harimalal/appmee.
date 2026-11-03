# Exemple : « Démo Carrousels IA » (29 octobre 2026)

https://claude.ai/artifact/5eHFmxcW2WrdrFKthYrRmN (version 2, 24 slides) : pourquoi faire des carrousels, et comment j'en ai généré 6 par l'IA (62 slides, 4,94 €). La version 1 (21 slides, la fabrique HTML en 4 formats) a été jugée « pas assez visuelle ». Planche de design : https://claude.ai/artifact/FUhc2DuQQtSdXcbywebby7

## Ce qui a été appris

### Version 2 (retour : « pas assez visuel »)

- **Montrer les vrais résultats, beaucoup.** La v1 parlait d'un gabarit et d'un seul carrousel. La v2 montre 6 carrousels générés, leurs 62 slides (mur, bande parcourue par la caméra, couvertures, avant/après) : c'est ce qui fait la vidéo.
- **Chercher l'artefact le plus riche du sujet** dans le Cockpit (collection `artifacts`) et dans les branches du dépôt, pas seulement `main` : le journal des carrousels, l'étude des modèles, les coûts réels et les visuels de référence étaient sur une branche de travail.
- **Un angle « pourquoi » chiffré** : ouvrir sur la même idée postée en texte, en image et en carrousel, avec l'engagement médian de chaque format. Les chiffres viennent d'études publiées (Buffer, Socialinsider), source citée en bas de slide, et la nuance qui dérange est dite (les Reels gagnent en portée).
- **Le tâtonnement, les modèles, l'arbitrage et les coûts** sont un récit en soi : méthodes essayées et refusées, tableau des modèles (testé, chiffré, écarté), part des crédits perdue en essais, coût par carrousel.
- **Pas de faux classement** : les « formats qui font swiper » sont présentés comme les formats que le créateur réutilise, pas comme un palmarès de performance.

### Version 1

- **La planche peut proposer la continuité.** Trois directions : le langage visuel du résultat lui-même (stabilo), la série (pastel et impact des démos précédentes), le réseau (fil Instagram). Le créateur a choisi la série : sa chaîne garde une identité d'une vidéo à l'autre.
- **Ce que le créateur a essayé, avec ses mots.** GPT Image seul : rendu superbe, mais ça dérive d'une génération à l'autre. Manus en un clic : très bon résultat, tous formats, mais 4 100 crédits consommés sans confirmation. Les SaaS de carrousels IA : toujours manuels, un outil de plus, payants, limités, templates figés. Ne rien ajouter qu'il n'a pas dit.
- **Mesurer plutôt qu'estimer.** Le script de rendu a été relancé dans une copie de travail (hors du dépôt) : 4 formats en 18 secondes, sortie réelle du terminal reprise à l'écran. Le « à la main » reste en volume (32 visuels à poser), sans durée inventée.
- **Le temps de construction vient des commits** : la fabrique a été montée entre le 23/10 au soir et le 24/10 à 11 h 30.
- **La pub peut être courte** : 2 slides (le site d'où viennent les carrousels, la newsletter) suffisent quand le produit a déjà eu sa revue complète dans une vidéo précédente.

## Le récit

Accroche (l'article et 4 cadres vides « 0 / 8 », les contraintes, « 32 visuels pour un seul article ») → titre (éventail flouté des vrais carrousels) → bénéfice (1 fichier, 32 visuels, 18 s, 0 image coupée, 0 chiffre inventé) → pourquoi des carrousels → les 4 formats à l'échelle, zones sûres en pointillé → pour qui (+ bandeau) → **pub Reflex IA** (2 slides) → un carrousel à la main (éditeur de design, menu Redimensionner) → ce que j'ai essayé → « et si mes carrousels sortaient d'un fichier ? » → la chaîne en 5 étapes → les 8 pièces → le temps, en gros → le détail : le fichier tapé à côté de la slide rendue, les 8 slides en bande, la charte stabilo, la zone sûre et le rendu ✓, rien d'inventé → teaser motion (« écris MOTION en commentaire ») → bilan.

## Techniques réutilisables

- Formats côte à côte **à la même échelle** (largeur commune, hauteurs réelles), zones sûres tracées en pointillé à partir du tableau de la fabrique.
- Zones réservées d'une app (TikTok) en hachures sur la vraie image.
- Extrait du vrai fichier source tapé ligne par ligne dans un terminal, la slide rendue qui apparaît à côté.
- PDF LinkedIn converti en image avec `pdftoppm -f 1 -l 1 -r 60 -png`.
