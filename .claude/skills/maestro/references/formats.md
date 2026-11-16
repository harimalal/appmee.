# Routeur de livrables : n'importe quel format

Pour chaque livrable du brief : son **type**, sa **méthode de production**, sa **vérification** (voir `quality-gates.md`) et son **canal de livraison**. Tout livrable est d'abord un fichier de `livrables/` dans le dépôt, commité et poussé ; le canal ajoute une livraison complémentaire si le brief la demande.

Avant de produire avec un outil : vérifier qu'il est disponible (`tooling.md`). Les skills cités sont ceux de la session ; s'ils manquent, prendre le plan B de `TOOLING.md`.

| Type | Production | Grille | Livraison |
|---|---|---|---|
| **Texte, article, note, script, séquence** | Écrire en Markdown ou en texte brut | Contenu | Fichier `.md` dans `livrables/` |
| **Document formel (rapport, procédure, proposition)** | Markdown puis conversion, ou skill `docx` si Word demandé ; document éditable partagé (connecteur Docs) seulement si le brief ou l'utilisateur le demande | Document formel | Fichier `.docx` ou `.md` ; lien du doc si créé |
| **PDF** | Skill `pdf` (ou conversion depuis le Markdown ou le docx) | Document formel | Fichier `.pdf` |
| **Tableur, budget, modèle chiffré** | Skill `xlsx` | Données | Fichier `.xlsx` ou `.csv` |
| **Présentation, deck** | Type d'artefact "Slides" (démarrage via `Artifact` quickstart), ou skill `pptx` si .pptx demandé | Présentation | Lien d'artefact privé ou fichier `.pptx` |
| **Page web, outil interactif, mini-app** | Artefact HTML privé (guides `artifact-design`, `artifact-capabilities`) ; ou fichiers dans le dépôt pour un site | Produit | Lien d'artefact privé. Publier un site ou rendre public = ligne rouge |
| **Tableau de bord, visualisation** | Skill `dataviz`, type d'artefact "Dashboard" | Données | Lien d'artefact privé ou image dans `livrables/` |
| **Code, script, automatisation** | Écrire dans le dépôt cible avec tests ; workflow n8n en JSON exportable | Code | Commits sur la branche de travail ; pas de PR sans demande |
| **Base de données, schéma** | Fichiers SQL de migration dans le dépôt | Code | Fichiers `.sql` ; exécution sur une base live = ligne rouge |
| **Vidéo, diaporama animé, contenu de lancement d'app** | Skill `studio-lancement-app` ; HyperFrames pour les vidéos HTML | Créatif | Fichiers dans `livrables/` ; génération de crédits = dépense |
| **Voix off, audio** | Connecteur ElevenLabs (génération de parole) | Créatif | Fichier audio ; crédits = dépense, accord avant |
| **Image, visuel, photo** | Photos libres via Unsplash (licence à noter), SVG ou HTML/Canvas, génération via ElevenLabs si connecteur complet | Créatif | Fichier dans `livrables/` ; génération = dépense |
| **Email, newsletter, séquence d'emails** | Rédiger en Markdown ; brouillon dans Gmail ou campagne en brouillon dans MailerLite | Contenu | Brouillon uniquement ; **envoi interdit sans feu vert** |
| **Page ou base de connaissances** | Page Notion privée (brouillon) ou Markdown dans le dépôt | Document formel | Lien du brouillon ; partage = ligne rouge |
| **Recherche, synthèse, benchmark** | Skill `deep-research` ou recherche menée directement | Document formel | Rapport `.md` avec sources |
| **Plan d'action, stratégie, feuille de route** | Markdown structuré (qui, quoi, quand, outil) | Stratégie | Fichier `.md` |
| **Process, playbook, checklist** | Markdown avec critères de "fait" | Système | Fichier `.md` |
| **Calendrier, planning** | Fichier `.ics` ou tableau ; événement réel avec invités = envoi | Document formel | Fichier ; pas d'invitation envoyée |
| **Livrable non listé** | Procédure ci-dessous | Ad hoc | Selon le brief |

## Livrable non listé : procédure

1. Décrire en une phrase ce qu'est le livrable, qui l'utilise et comment il est ouvert.
2. Chercher l'outil : natifs, skills (`SearchSkills`), connecteurs (`ListConnectors`, `ToolSearch`).
3. Si aucun outil ne le produit proprement : produire la meilleure forme textuelle ou fichier possible, dire précisément ce qui manque et ce que l'utilisateur doit connecter. Ne pas simuler un résultat.
4. Construire la grille ad hoc de 4 à 6 critères (voir `quality-gates.md`) et l'écrire dans `brief.md` **avant** le GO.
5. Choisir une vérification concrète du format et l'écrire de la même façon.

## Règles transverses de livraison

- **Une seule langue par livrable**, celle du brief (français par défaut).
- **Formats finaux** : extension, encodage, noms de fichiers lisibles, pas de fichier temporaire dans `livrables/`.
- **Pas de lien `file://`** : chemin relatif au dépôt ou lien d'artefact.
- **Artefacts** : toujours privés ; l'utilisateur décide du partage.
- **Gros fichiers** : garder sous quelques dizaines de Mo ; au-delà, lien ou découpage, et le dire.
- **Aucune donnée sensible** (clés, jetons, données personnelles inutiles) dans un livrable.
