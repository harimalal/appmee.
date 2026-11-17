---
name: contenu-carrousel
description: Produire un carrousel (images 1080x1350 + PDF) pour un client, avec son pack (voix, design, thématiques, verrous, templates). À utiliser pour « fais un carrousel pour <client> sur <sujet> ». Le moteur est commun, le pack client change tout.
---

# Carrousel : moteur commun, pack client

Moteur : `studio-contenu/moteur/carrousel/` (ne change pas d'un client à l'autre).
Pack client : `studio-contenu/clients/<client>/` (change d'un client à l'autre).

Commande : `carrousel client=<slug> sujet=<sujet>`

## Flow
1. **Charger** le pack du client : `marque.md`, `design.json`, `thematiques.md`, `verrous.md`, `templates/`. Ne rien lire d'un autre client.
2. **Partir d'un template** (`templates/<nom>.json`) qui correspond au pilier du sujet : il fixe la suite des slides et leur layout. Si aucun ne convient, en proposer un nouveau à valider.
   - Layouts : `cover-photo` (photo plein cadre, titre géant), `plein` (photo + titre + légende), `arche` (photo en arche + texte), `bande` (photo en bandeau + liste), `duo` (photo teintée + titre géant, pour la clôture), `chiffre` (donnée géante, sans photo).
   - Autres layouts : `carte` (carte de texte posée sur la photo), `liste-carte` (la carte porte une liste), `haut-texte` (texte en haut, photo inclinée en bas), `moitie` (photo sur une moitié, bloc de couleur sur l'autre), `cercle` (coupole de photo en bas).
   - **Varier d'un carrousel à l'autre** : le template donne la suite par défaut, mais chaque carrousel doit avoir sa propre personnalité. Changer `marque` au niveau du carrousel (`surligne`, `souligne`, `contour`, `pastille`, `blanc`) et, par slide, `layout`, `pos` (`bas`, `haut`, `centre`), `align` (`gauche`, `centre`, `droite`) et `encart` (bande : `bloc`, `etiquette`, `contre`, `libre` ; carte : `rotee`). Deux carrousels d'un même client ne doivent pas avoir la même combinaison.
3. **Choisir les photos** : le carrousel se construit autour d'elles. Utiliser en priorité les vraies photos du client (`assets/`). À défaut, chercher sur Unsplash (outils `search_photos` puis `download_asset`), enregistrer dans `assets/unsplash/` (1200 px de large) et noter l'auteur dans `credits.json`. Ne jamais garder une photo où figure la marque d'un tiers. Les photos d'illustration ne représentent pas le client : le dire.
4. **Rédiger** `carrousels/<slug>/carrousel.json` : titres courts et percutants, un mot mis en valeur avec `*mot*`, 35 mots maximum de texte courant, voix de `marque.md`. Chaque slide donne `image: {fichier, pos}` selon son layout. `fruit` (ou la clé de palette du client) choisit la couleur du carrousel.
5. **Contrôler** : chaque fait vient de `thematiques.md`, sinon il est écrit `[[à compléter : ce qu'il faut]]`. Relire `verrous.md` ligne par ligne.
6. **Rendre** : `node studio-contenu/moteur/carrousel/render.mjs studio-contenu/clients/<client> <slug>` → `out/slide-NN.png` et `out/carrousel.pdf`.
7. **Aperçu** : `node studio-contenu/moteur/carrousel/apercu.mjs studio-contenu/clients/<client> <fichier.html>`.
8. **Livrer en brouillon** : rien n'est publié sans la validation du client.

## Nouveau client
Créer `studio-contenu/clients/<slug>/` avec les mêmes fichiers. Partir de ses vrais contenus (site, posts) pour la voix, jamais d'une description générique. Marquer le pack « provisoire » tant que le client n'a pas validé.
