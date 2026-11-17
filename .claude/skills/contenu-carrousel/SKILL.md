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
2. **Choisir le template** qui correspond au pilier du sujet. Si aucun ne convient, en proposer un nouveau à valider.
3. **Rédiger** `carrousels/<slug>/carrousel.json` : une idée par slide, 35 mots maximum de texte courant, voix de `marque.md`.
   - Types de slide : `cover`, `texte`, `liste`, `etape`, `chiffre`, `photo`, `cta`.
   - `fruit` (ou la clé de palette du client) choisit la couleur du carrousel.
4. **Contrôler** : chaque fait vient de `thematiques.md`, sinon il est écrit `[[à compléter : ce qu'il faut]]`. Relire `verrous.md` ligne par ligne.
5. **Rendre** : `node studio-contenu/moteur/carrousel/render.mjs studio-contenu/clients/<client> <slug>` → `out/slide-NN.png` et `out/carrousel.pdf`.
6. **Aperçu** : `node studio-contenu/moteur/carrousel/apercu.mjs studio-contenu/clients/<client> <fichier.html>`.
7. **Livrer en brouillon** : rien n'est publié sans la validation du client.

## Nouveau client
Créer `studio-contenu/clients/<slug>/` avec les mêmes fichiers. Partir de ses vrais contenus (site, posts) pour la voix, jamais d'une description générique. Marquer le pack « provisoire » tant que le client n'a pas validé.
