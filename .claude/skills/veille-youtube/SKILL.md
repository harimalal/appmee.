---
name: veille-youtube
description: Veille YouTube par sujet. Trouve les vidéos longues qui performent vraiment, rapportées à la taille de la chaîne (vues ÷ abonnés) et à leur âge (vues par mois), pas aux vues brutes. Classe le top 15, regarde les miniatures du top 5, explique pourquoi elles marchent et livre de quoi tourner : un angle, 3 titres, une miniature signature avec son prompt, le pattern à reproduire. Chaque recherche s'ajoute à la page « Veille YouTube », un artefact qui garde toutes les recherches et la vue d'ensemble. Utilise ce skill dès que l'utilisateur donne un sujet à analyser sur YouTube, ou dit « nouvelle recherche : … », « quelles vidéos marchent sur … », « fais la veille sur … », « quel angle pour une vidéo sur … », « analyse la concurrence YouTube de … », même sans dire « veille ».
---

# Veille YouTube

Version : 2026-10-28.

Né le 28 octobre 2026 (sept recherches : JEV, générateurs vidéo IA, plateformes vidéo et image, Claude Code motion, agents IA, business IA, Higgsfield). La page de référence : `assets/veille-youtube-modele.html`, avec le rapport JEV comme exemple.

L'idée : **les vues brutes mentent**. 707 986 vues pour 150 000 abonnés (4,7 ×), c'est moins fort que 8 576 vues pour 336 abonnés (25,5 ×). On classe donc par vues ÷ abonnés, puis par vues par mois, avec des filtres fixes. Ensuite on explique, chiffres à l'appui, et on transforme en vidéo à tourner.

`<skill>` désigne le dossier de ce skill.

## Déroulé pour un sujet

1. **Requêtes.** 3 à 5 requêtes qui couvrent les intentions (nom seul, avis, test, tutoriel, vs, alternative ; une variante dans l'autre langue si utile). Ne demande pas de validation : lance.
2. **Collecte.** Script ou navigateur, voir `references/methode.md` § 2. Respecte le rythme et **arrête-toi si YouTube demande une vérification** : ne la contourne jamais. Dis ce qui manque et propose de reprendre plus tard ou au navigateur.
3. **Filtres et calculs.** Ceux de `references/methode.md` §§ 3-4, sans exception silencieuse. Écarte à la main les vidéos hors sujet et note-le.
4. **Relis le classement** (`top.md`) : les chiffres sont-ils plausibles ? une chaîne à 17 abonnés avec 400 vues est-elle un vrai signal ou du bruit ? Dis-le dans la remarque de la ligne.
5. **Regarde les miniatures du top 5** (ouvre les images). Note ce qui revient et ce qui distingue.
6. **Analyse** selon `references/analyse.md` : 4 à 6 mécanismes (constat, à reprendre, déclinaisons), le pattern, la synthèse (angle, 3 titres, miniature signature décrite + prompt), une remarque par vidéo du top 15.
7. **Rapport.** Écris le JSON (`references/format-rapport.md`), puis :
   ```
   python3 -I <skill>/scripts/rapport.py <page.html> <rapport.json> --miniatures <dossier>/miniatures
   ```
   La première fois, `<page.html>` est une copie de `assets/veille-youtube-modele.html` (passe `--retirer r1` pour enlever l'exemple JEV si l'utilisateur ne le veut pas).
8. **Vérifie la page** dans un navigateur headless (aucune erreur console, le rapport s'affiche, les miniatures sont là), puis **publie** : mets à jour l'artefact « Veille YouTube » existant (même URL : relis-le d'abord, ajoute le rapport à sa version en ligne) plutôt que d'en créer un nouveau. Hors claude.ai, garde la page dans le dépôt ou envoie le fichier.
9. **Réponds** court : le top 3 (titre, chaîne, ratio, lien), l'angle recommandé, ce qui a été approximé ou écarté, le lien de la page. Termine par « Quel est le prochain sujet ? ».

Quand l'utilisateur tient un tableau de suivi (Projet · Tâche · Description · Commentaire), rends le compte rendu sous cette forme.

## Ce qu'on livre par vidéo du top 15

Titre, lien, miniature (décrite si on la montre en texte), vues, abonnés, date de publication, âge, durée, **ratio vues/abonnés**, **vues par mois**, rang, tranche, une remarque.

## Règles

- Jamais de chiffre inventé ni « estimé » sans le dire. Une donnée manquante reste manquante.
- Les dates « il y a N mois » sont approximatives : `approx: true`.
- Les miniatures appartiennent aux créateurs : on les montre pour les analyser, on cite les chaînes.
- La charte de miniature signature (`sig`) est commune à toutes les recherches. Ne la change que sur demande.
- Une recherche = un rapport. Une nouvelle recherche sur le même sujet remplace l'ancien rapport si l'utilisateur le demande, sinon elle s'ajoute avec sa date.

## Pour en faire une vidéo

Le skill `demo-video-youtube` transforme une recherche (ou n'importe quel résultat construit ensemble) en diaporama animé 16:9 pour une vidéo YouTube : résultat d'abord, blocage, méthode manuelle, outils et limites, démonstration avec Claude, rendu final, appels à l'action.

## Prompt type

Avec ce skill installé, une ligne suffit : « Nouvelle recherche : <sujet> ». Sans le skill, le prompt complet :

> Je vais te donner des sujets YouTube. Pour chacun, trouve les vidéos longues (pas de Shorts) qui performent le plus par rapport à la taille de la chaîne : vues ÷ abonnés, puis vues par mois. Filtres : plus de 4 min, plus de 500 vues, de 2 jours à 12 mois. Donne le top 15, du meilleur au moins bon : titre, lien, miniature, vues, abonnés, date. Regarde les miniatures du top 5 et explique pourquoi elles marchent (constat, à reprendre, déclinaisons), puis donne 1 angle pour ma vidéo, 3 titres, 1 miniature dans ma charte avec son prompt, et le pattern à reproduire. Ajoute chaque recherche à l'artefact « Veille YouTube ». Premier sujet : <sujet>.
