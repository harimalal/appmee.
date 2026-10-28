# Narration : la démo qui mène à un résultat

Ce n'est pas un « how to ». C'est une démonstration qui part d'un **résultat recherché** et montre comment on l'obtient, avec le contraste entre la façon fastidieuse et la façon Claude. L'oral porte l'explication : à l'écran, **un titre et une structure par slide**, le reste se voit.

## Ouverture : trois portes possibles

Toujours commencer par l'une des trois, jamais par une présentation :
1. **Le résultat** (effet « waouh ») : la vraie page finale, zoom sur le détail le plus fort (le point n°1, le chiffre clé), puis recul sur l'ensemble. Titre : ce que ça fait, en une ligne, et ce que ça évite (« 51 vidéos classées. Zéro copier-coller. »).
2. **La façon fastidieuse** : l'interface à la main, la répétition, le temps qui passe.
3. **Le blocage** : la question sans réponse (« Quelle vidéo faire ? »), l'écran plein de choix.

Le résultat est l'ouverture la plus forte quand il existe vraiment : prends-la par défaut.

## L'arc type (20 slides, ≈ 8 à 12 min d'oral)

| # | Slide | Rôle | Effets typiques |
|---|---|---|---|
| 1 | Résultat | Accroche | Vraie capture, zoom sur le n°1 puis recul |
| 2 | Appel à l'action | Abonne-toi, like, commente ton sujet | Pointeur qui clique, bouton qui bascule, commentaire tapé |
| 3 | Blocage | La question de départ | Recherche tapée dans la vraie interface, résultats qui tombent, zoom |
| 4 | Le piège | L'idée reçue qui trompe (vues brutes) | Deux cartes face à face, compteurs, verdict qui se renverse |
| 5 | Pourquoi | Les bénéfices clés (la jungle) | Mur de vraies images en fond, 5 bénéfices un par un |
| 6 | Pour qui | 3 profils | 3 cartes, une phrase chacune |
| 7 | À la main | La méthode classique, **au moins 10 lignes** remplies | Saisie lente des 2 premières lignes avec zoom, puis rapide ; formule tapée ; temps estimé ; tampon « et toujours aucune analyse » |
| 8 | Les autres solutions | Outils gratuits et payants **en liste**, chacun avec ses limites en rouge | Apparition ligne par ligne ; **pas de graphique** ; conclusion « Il manque : … » |
| 9 | Pivot | « Et si on donnait la mission à Claude ? » | Titre en flou → net, la demande tapée |
| 10 | L'outil | Claude Desktop + extension Claude in Chrome (ou Claude Code) | Deux fenêtres, liseré orange, flux animé, pointeur |
| 11 | Étape 1 : le prompt | Écrit une fois, puis une ligne par sujet | Saisie dans la vraie interface, étiquettes « le filtre / l'indicateur / le livrable » |
| 12 | Étape 2 : collecte | Ce que fait Claude | Onglet piloté, appels d'outils qui s'empilent, compteur |
| 13 | Étape 3 : calcul | Les règles fixes, un exemple | **Zoom sur l'encart de calcul**, compteur jusqu'au chiffre |
| 14 | Étape 4 : classement | L'ordre qui se renverse | Tri animé, **zoom sur le top 3**, gros plan final |
| 15 | Pourquoi ça marche | Les vraies miniatures du top 5, l'élément repris de chacune, 3 mécanismes | Zoom sur une miniature |
| 16 | Ce que l'outil donne | L'analyse dans la vraie page | Zooms dans la capture : un mécanisme, le pattern |
| 17 | Rendu final | La vraie page défile | Caméra qui descend, étiquettes par zone |
| 18 | Les encarts | Encart par encart, tel qu'il est dans l'artefact | Zoom sur chaque encart |
| 19 | Avant / après | Le bilan | Deux colonnes qui se remplissent en miroir |
| 20 | À toi + appel à l'action | Donne-lui un sujet ; abonne-toi, like, commente | Sujets qui se tapent en boucle, boutons, « le prompt est dans la description » |

Adapter à un autre sujet : garde l'ordre **résultat → blocage → piège → bénéfices → pour qui → à la main → autres solutions → pivot → outil → étapes → résultat détaillé → bilan → appel à l'action**. Les étapes Claude (11 à 14) deviennent les vraies étapes du sujet (3 à 6), dans l'ordre où elles se sont passées dans la conversation.

## Règles d'écriture

- **Un titre par slide**, court, en majuscules condensées, un seul mot en couleur d'accent. Un surtitre (« Étape 3 », « Le piège ») au-dessus.
- **Une structure par slide** : deux cartes, une liste, une interface, un tableau. Pas de mélange.
- **L'oral dit le reste** : chaque slide a sa note (touche N) de 1 à 3 phrases, écrite pour être dite.
- **Vrais chiffres, vraies images** : ceux de la conversation et de l'artefact. Une estimation est écrite comme telle à l'écran (« ≈ 2 min × 51 vidéos (estimation) »).
- **Pas de prix d'outils** : ils changent. Classe en gratuit, freemium, payant.
- **Appels à l'action** : en slide 2 (tôt, sans attendre la fin) et en dernière slide. Le commentaire demandé est utile (« donne ton sujet »), pas un « like si tu aimes ».
- **Bénéfices avant méthode** : on dit à quoi ça sert et pour qui avant de montrer comment.
- Pendant un zoom, masque le titre (`data-hudoff`) pour ne pas recouvrir l'interface.

## Le script

Pour une démo longue, écris d'abord le **déroulé en texte** (une ligne par slide : titre, structure, effets, phrase d'oral) et fais-le valider. C'est là que se jouent les retours. Ensuite seulement, code.
