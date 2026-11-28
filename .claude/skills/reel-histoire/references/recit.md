# Le récit : schéma narratif, adaptation, fiche de faits, voix

Dans ce document, `<skill>` désigne le dossier de ce skill. À lire pour écrire le brief puis `story.json`. **Pour passer d'une source (playbook, journal, étude) à l'histoire, et quand l'utilisateur dicte l'ordre de l'histoire : `<skill>/references/source-vers-storyline.md`** (fiche de faits, tri « sourcé / apporté par l'utilisateur », élagage de scènes).

## Le schéma narratif

Cinq étages, toujours dans cet ordre. Chaque étage répond à **une** question du spectateur.

| Étage | Question du spectateur | Part du temps | Dans le reel SEO |
|---|---|---|---|
| **1. Problème** (le renversement) | « Est-ce que ça me concerne ? » | ≈ 15 % | Titre (« Comment optimiser le SEO de ton site avec Claude Code ? ») puis « Ce n'est pas tes articles, ni ta boutique : c'est l'indexation » |
| **2. Situation** (la preuve + la notion inconnue) | « De quoi on parle, concrètement ? » | ≈ 25 % | 285 pages non indexées sur 132 articles ; mots-clés vs indexation ; où ça se voit (Search Console) |
| **3. Solution** (les causes trouvées) | « Qu'est-ce qui ne va pas ? » | ≈ 25 % | Trois causes « bêtes », une scène chacune, puis les articles oubliés |
| **4. Process** (la méthode) | « Comment ils s'y sont pris ? » | ≈ 10 % | 5 corrections, 1 commit chacun, ≈ 23 minutes |
| **5. Résultat** (avant/après, honnête) | « Qu'est-ce que ça a donné ? » | ≈ 25 % | 140→0, 23→0, 1→0, 0→27 ; site corrigé et vérifié ; réponse de Google attendue le 8 décembre ; objectif ≠ résultat |

Durée cible **60 à 95 s** (le reel SEO : 95 s, c'est le haut de la fourchette ; au-delà, couper une cause ou le détail du process).

Règles de l'enchaînement :
1. **Le premier plan dit de quoi on parle et pour qui.** Jamais un chiffre seul en ouverture (c'est l'erreur de la v1).
2. **On parle au spectateur (« tu »)** pour le problème, **à la 1re personne (« j'ai », « sur mon blog »)** pour le travail et la preuve. Jamais « vous ».
3. **La notion inconnue se définit en une à trois phrases**, avant d'être utilisée (« indexation = que Google connaisse la page »).
4. **Une idée par scène**, une scène par cause. Si deux causes se ressemblent, n'en garder qu'une et la dire dans le process.
5. **Les chiffres arrivent après l'histoire**, sauf le chiffre paradoxal du hook qui sert de preuve (285 pour 132).
6. **Le résultat sépare toujours** ce qui est vérifié (côté site), ce qui est attendu (côté externe, avec la date) et l'objectif (écrit « objectif »).
7. **La fin reboucle sur le début** (même texte, même fond que le titre) pour le re-visionnage.

### Adapter à un autre type de travail

| Type de travail | Problème (côté spectateur) | « Causes » = | Avant / après | Résultat honnête |
|---|---|---|---|---|
| Correction technique / SEO | « Ton site n'est pas bien vu… et ce n'est pas ce que tu crois » | les défauts trouvés dans le code | compteurs de défauts → 0 | corrigé et vérifié côté site ; effet externe attendu à une date |
| Automatisation (n8n, Make…) | « Tu refais chaque semaine la même tâche à la main » | les étapes manuelles et leur coût | temps / nombre d'actions par semaine avant → après | temps gagné **mesuré sur N exécutions**, pas projeté |
| Test ou comparatif d'outils | « Tu hésites entre X et Y » | les critères qui départagent | scores ou coûts côte à côte | verdict par profil, avec la limite du test |
| Construction d'un système IA | « Tu veux un agent qui fasse Z, mais tout casse » | les échecs rencontrés et la règle ajoutée | version 1 → version finale | ce qui marche, ce qui coince encore |
| Migration / refonte | « Tu as peur de perdre ton trafic en changeant » | les risques identifiés | liste de risques → vérifs passées | ce qui est vérifié, ce qui reste à surveiller |
| Audit | « Tu ne sais pas où ça coince » | les constats classés | état initial → plan | recommandations, sans résultat inventé |

Si le travail n'a **pas d'avant/après chiffré**, supprimer l'étage « curseur » et finir sur la liste des vérifications faites. Ne jamais fabriquer un avant/après.

---

## La fiche de faits (avant de rédiger quoi que ce soit)

Extraire du travail documenté, dans `story.json` (champ `nombres_autorises`) et dans `BRIEF.md` :
- chaque **nombre** utilisable, sa **source** (fichier, section, mesure) et son **statut** : mesuré / attendu / objectif ;
- les nombres **contradictoires entre sources** : on ne les utilise pas (dans le reel SEO : « 10 pages canonical » et « 6 liens restants » écartés) ;
- ce qu'on **n'affirme pas** (gain d'indexation, trafic, classement) tant que ce n'est pas mesuré ;
- les noms réels à montrer (fichiers, pages, URL) : **uniquement des éléments existants** (les hachages `search-index.0a086143.json` → `d7b4d2ce.json` étaient de vraies mises en ligne).

Aucune donnée inventée, aucune commande ou capture factice : si un élément n'est pas réel, on le remplace par un schéma abstrait.

---

## Écrire la voix et les légendes

Chaque phrase de `story.json` a **deux textes** :
- `voice` : le texte lu. Nombres en toutes lettres (« deux cent quatre-vingt-cinq »), jamais de chiffre ni de signe, marque écrite comme elle se prononce (« Reflex IA point com »).
- `cap` : la légende affichée, avec les chiffres.

Règles :
- 5 à 12 mots par phrase, une idée par phrase. Ouvrir par une **question** quand c'est le problème du spectateur.
- **Débit ≤ 4,5 mots/s** (contrôlé). La synthèse lit parfois les phrases courtes trop vite : ajouter `"tempo": 0.8–0.95` à la phrase (ralentissement sans changer la hauteur), plutôt que de rallonger le texte.
- Style : preuve avant promesse, le « mais », une limite (pour Reflex IA : `SKILL_STYLE_ECRITURE.md` et `SKILL_VOIX_REFLEXIA.md` du dépôt reflex-ia). Mots bannis : révolutionnaire, game changer, incroyable, magique, ultime, 10x, « secret », « fait tout à votre place ». Pas d'emoji.
- **Registre : écrire comme on parle à un ami (retour de Hari, 6e essai).** Quand l'utilisateur le demande (ou que le reel est un « raconte-moi » à la première personne) : tutoiement, contractions orales (« y a plein de solutions », « j'ai rien à ouvrir », « je change un truc »), phrases courtes, exclamations, une pointe de « tranquille ! ». **Le registre passe par le texte et le débit, pas par une consigne dans la requête de voix** : « dis ça avec énergie… » est lu à voix haute en français et double la durée en anglais ; on règle `tempo` global (1,1 à 1,16) et `gap_sentence` (0,08 s) dans `story.json`. Ne pas durcir les affirmations : le ton change, pas le fond (« je n'ai pas tapé de code » reste signalé comme une parole de l'utilisateur).
- **CTA à mot-clé unique (6e essai, choix de Hari).** Formule : « **Tu veux le même système ? Commente « <mot-clé> », et je te l'envoie pour l'adapter à ta sauce.** » Le mot-clé est **un seul mot qui nomme le sujet du reel** (« site » pour le reel site, « comparatif » pour le reel comparatifs ; pour un autre sujet, le mot du sujet) ; l'écran montre le mot en grand et une bulle où il se tape. `cta_contient` = « Commente ». C'est **la promesse de l'utilisateur** (il envoie un système) : la signaler dans `SCRIPT.md`, ne pas nommer le fichier envoyé dans la vidéo si on ne le connaît pas. L'ancien CTA « Abonne-toi… » reste valable quand l'utilisateur le demande.
- **Pas d'appât d'engagement par défaut** (« commente X » sans promesse précise). Le CTA est **unique et choisi par l'utilisateur** (domaine du projet, abonnement, lien du playbook ; réglé par `cta_contient` dans `story.json`). Si la formule contient une promesse que le reel ne prouve pas (« terriblement efficaces »), la signaler à l'utilisateur dans le message de livraison ; c'est son choix éditorial. Pour Reflex IA : domaine **reflex-ia.com**, jamais `reflexi-ai.com`.
- Prononciations à écouter par l'utilisateur et à signaler : noms d'outils, « commit », sigles, domaines.

---

### Phrases qui ne sont pas lues
Une liste affichée (les 6 étapes, les critères) n'a pas à être lue en entier : supprimer la phrase de voix qui l'énumère et laisser la voix décrire **ce qui se passe**. La scène (cascade de coches) se cale alors sur la 1re phrase conservée (`const [m2, m3] = m.sent, m1 = m2`).

### Comparer des outils : ne dire que ce que la source établit
Une scène « pourquoi cet outil plutôt que X ou Y » n'affirme **rien** sur les capacités de X et Y (« pas utilisé pour ce tri ») et donne la raison positive tirée de la source (ex. « travaille dans mon onglet déjà connecté, aucun mot de passe »). Le texte de cette scène est montré à l'utilisateur **avant** la voix.

### Quand l'utilisateur dicte l'histoire
Si l'utilisateur donne l'ordre des scènes (problèmes → système → exemples → appel), cet ordre **remplace** le tableau des 5 étages : on garde seulement les règles d'enchaînement (premier plan = de quoi on parle ; « tu » pour le problème, « je » pour le travail ; une idée par scène ; chiffres après l'histoire ; fin qui reboucle). Ses propres mots pour les problèmes sont repris tels quels et signalés comme siens dans `SCRIPT.md` (voir `source-vers-storyline.md`).

## Vidéo « pub » d'un système (retour de Hari sur le reel n°8)
- **Les avantages d'abord, le process en une phrase** : hook = le bénéfice (« une seule source, tout ton contenu »), puis 3 ou 4 avantages concrets (une fois, tous les réseaux, trente jours prêts, zéro outil en plus), puis l'anatomie du système en **une** phrase, puis ce que ça apporte, puis le CTA à mot-clé.
- **Promesse non prouvée = limite affichée** : quand l'utilisateur veut dire « automatique », « 30 jours », « 0 € », garder sa phrase (signalée comme son dit) et poser la limite en sous-titre à l'écran (« production automatique · publication par toi », « prêts, pas encore publiés », « hors abonnement Claude »).



## Approche besoin (retour de Hari sur le reel n°9, 28/11/2026)
- **Partir du besoin de celui qui regarde, pas des chiffres.** Exemple n°9 : « les reels accrochent, mais en faire un est un casse-tête : du fond, de la forme, des effets, une transition toutes les quelques secondes, tout écrit au mot près ». Puis : pourquoi c'est plus simple avec le système (Claude écrit le script, choisit les images, place les effets, cale la voix ; toi tu valides le texte), l'itération (« tu le dis, il refait », avec de VRAIS avant/après), le système réglé une fois (charte, ton, effets), et « tu demandes juste une nouvelle vidéo ».
- **Illustrer en plein espace avec ce qu'on a vraiment fait**, qui tourne : extraits de vraies vidéos, vrais écrans, vrais fichiers. Le montage final de nos réalisations vaut toutes les démonstrations.
- **Arrêter l'approche mathématique** : pas de chiffres empilés ; un nombre seulement s'il sert le récit et qu'il est sourcé. Parler au niveau du spectateur.
- Rythme : un changement visuel toutes les 2 à 4 s, une seule étiquette à la fois.
- Les affirmations de Hari (« ce qui accroche le plus », « en vingt minutes ») restent marquées comme ses dits, avec une limite à l'écran (« hors retouches »).

## Enseignements du reel n°8 « Content Factory » (v1 → v3)
- Les **avantages d'abord**, le process ensuite : une source → tout ton contenu, tous les réseaux, du contenu prêt à l'avance, sans outil en plus.
- Quand un outil est nommé (Claude), son **logo en 3D léger** apparaît au mot près ; il coiffe le « système » qu'on explique.
- **Expliquer un système pièce par pièce** : une phrase par pièce, tirée de son vrai fichier ; titre et ligne d'explication changent au même instant.
- Retirer une phrase dès que Hari la juge en trop (ex. « rien d'inventé »), même vraie.
- Fond : Hari n'aime plus les fonds clairs à ronds de couleur → **bleu-noir reflet de verre**, sans ronds, éléments agrandis pour remplir l'écran.
- Couverture : le titre doit se lire au premier coup d'œil sur fond sombre (blanc + jaune plein, grand), jamais de texte sombre sur fond sombre.

## Quand Hari raconte un épisode passé (reel n°10, charte)
- Retrouver l'épisode dans l'historique (`git log -i --grep`, valeurs CSS par commit) avant d'écrire : l'avant et l'après doivent être de vraies captures.
- Ce que Hari ajoute et que le dépôt n'a pas (ex. « cinq ou six maquettes GPT Image ») : dit de Hari ; à l'écran, cadres neutres + la seule pièce réelle ; le noter dans SCRIPT.md et proposer de remplacer par ses images.
