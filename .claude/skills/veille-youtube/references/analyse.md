# Analyse : de la liste classée à la vidéo à tourner

Le classement dit *quoi* marche. L'analyse dit *pourquoi*, et ce qu'il faut en faire. C'est la partie qui a de la valeur : ne la saute jamais, et appuie chaque phrase sur des vidéos nommées avec leur chiffre.

Matière première : le top 15 (titres, chaînes, ratios, dates, durées) et **les miniatures du top 5, regardées une par une** (lis les images, ne devine pas à partir du titre).

## 1. Pourquoi elles performent (`why`)

- `defs` : une phrase de cadrage, toujours la même idée : « Constats tirés des N vidéos longues relevées. L'échantillon est petit et une corrélation n'est pas une cause : ce sont des hypothèses solides, pas des lois. »
- `cards` : **4 à 6 mécanismes**, du plus fort au plus faible. Chacun :
  - `h` : « 1. Le nom du mécanisme » (court, concret : « La fenêtre de lancement », « L'angle de vérification », « Le logo vert comme signature »).
  - `html`, trois paragraphes, dans cet ordre :
    - `<p><b>Constat.</b> …</p>` : les faits, avec chaînes, ratios, vues, dates. Compare : ce qui marche contre ce qui ne marche pas.
    - `<p><b>À reprendre.</b> …</p>` : la règle actionnable qu'on en tire.
    - `<p><b>Déclinaisons.</b></p><ul><li>…</li></ul>` : 3 formules à trous, réutilisables (`[Outil] : [promesse]… vrai ou truqué ?`).

Familles de mécanismes à chercher : timing (fenêtre après une annonce), angle (doute, vérification, alternative, clone, prix), croisement avec une niche, preuve chiffrée dans le titre, format (liste, tuto complet, duel), durée, signature visuelle de la miniature (logo, couleur, visage, objet), taille de chaîne (les petites chaînes qui sur-performent).

## 2. Le pattern (`pattern`)

- `formulas` : 3 à 4 lignes « Titre : […] », « Croisement : […] », « Miniature : […] », « Vidéo : durée, moment de publication, structure ».
- `checklist` : 5 vérifications avant publication, chacune vérifiable par oui ou non.
- `examples` : 3 à 4 applications à d'autres situations, sous la forme `<b>Situation</b> : titre à trous`.

## 3. La synthèse pour ta vidéo (`synth`)

- `angle` : `<b>Une phrase d'angle.</b>` puis 3 à 4 phrases : quoi tourner, pour qui, pourquoi ça combine les mécanismes les plus forts. Retwiste vers la niche de l'utilisateur quand on la connaît (ses projets, son métier). Les chiffres à ajuster vont entre crochets `[500]`.
- `titles` : 3 titres `{t, w}`. `t` = le titre prêt à copier ; `w` = la logique + les vidéos modèles avec leur chiffre + pour quoi il est recommandé (portée ou ratio).
- `struct` : la structure de miniature choisie, une lettre de A à E (voir § 4), adaptée au thème.
- `els` : 3 à 4 éléments repris des miniatures du top 5, `{o: rang, el: "ce qui est repris (chaîne, ratio)"}`, plus un élément différenciant marqué `"d": true`.
- `thumb` : `<p><b>Description.</b> …</p><p><b>Variante.</b> …</p>` : la miniature décrite pour un humain (placement, expression, texte exact, mot en jaune).
- `prompt` : le bloc signature `sig.block` copié tel quel, une ligne vide, puis la scène en anglais : `STRUCTURE X (…). …` avec personne, expression hyper réaliste, logos officiels nommés et décrits (forme, couleurs), `TEXT:` exact.

## 4. Miniature signature (bloc `sig` de la page)

La charte est commune à toutes les miniatures de la chaîne et vit dans `sig` (règles, structures, `block`). Ne la modifie que si l'utilisateur le demande (autres couleurs, vrai logo à la place du carré). Par miniature, **trois choses seulement changent** : la structure, l'émotion du visage, un objet propre au sujet.

| Structure | Quand |
|---|---|
| A · Visage + logo | Test ou avis sur un outil |
| B · Duel | Versus, prix, alternative |
| C · Grille de logos | Comparatif, classement |
| D · Logo + mot massif | Annonce, thèse |
| E · Écran + flèche | Tutoriel, démo |

À rappeler sous chaque prompt : les générateurs épellent mal les textes et approchent les logos. Si le rendu est imparfait, générer sans texte, puis poser le texte et les fichiers officiels des logos dans Canva ou Photoshop.

## 5. Remarque par vidéo (`rows[].r`)

Une phrase pour chaque vidéo du top 15, au moins : ce qui explique son rang (« Très petite chaîne, 8 fois ses abonnés. Publiée à J+3 après l'annonce. »). Pour les autres, une remarque seulement si elle apprend quelque chose.

## 6. En-tête du rapport

- `name` et `h1` : le sujet, court (« JEV, l'IA plus rapide »).
- `tags` : 1 à 2 thèmes réutilisés d'une recherche à l'autre (« Modèles IA », « Vidéo IA », « Agents IA », « Business IA »…), pour filtrer la vue d'ensemble.
- `note` : ce qui a été écarté ou approximé. `method` : la méthode en une ligne, inchangée sauf exception.
