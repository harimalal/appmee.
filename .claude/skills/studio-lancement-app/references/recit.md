# Le récit : du problème à la fin

Un film de lancement qui marche raconte **une transformation** : quelqu'un a un objectif et se noie dans ses outils actuels → il découvre l'app → l'app transforme son objectif en résultat visible. Le spectateur doit se reconnaître dans les 3 premières secondes et comprendre ce que fait l'app avant la 20ᵉ.

## 1. Choisir le cas de démonstration

- **Un seul cas, suivi de bout en bout** (Dropit : « Buy a house in the country by next summer »). Pas une visite de toutes les fonctions : une histoire où chaque fonction arrive au moment où le personnage en a besoin.
- **Universel et concret pour le marché visé** : un objectif que beaucoup de gens ont, avec des détails locaux crédibles (Dropit US : pré-accord de prêt, agent immobilier, ville fictive « Millbrook »). Éviter le cas qui fait passer l'app pour autre chose (un suivi de course fait passer Dropit pour une app d'habitudes).
- **Un personnage avec un prénom** dans les données de démonstration (« Let's go, Sarah! ») et quelques autres contenus autour (3 autres projets avec de vraies photos) pour que l'app ait l'air vivante.
- **Le contenu produit par l'app doit être bon** : si l'app génère un plan, une réponse, un résumé, écris-le à la main comme le meilleur résultat possible. C'est lui qu'on lit à l'écran.

## 2. Passer de la landing aux textes du film

La landing contient déjà le travail de positionnement. Le film le **montre**, il ne le réinvente pas.

| Dans la landing | Dans le film |
|---|---|
| Titre principal / promesse | Texte central de l'acte « Promesse », et voix off de cet acte |
| Contraste avec les alternatives | Formule barrée → formule surlignée (« isn't another ~~all-in-one app~~ » → « It's the path to your goals ») |
| Proposition de valeur unique | La fonctionnalité montrée en premier et le plus longuement |
| Noms des fonctionnalités | Titres en badge du récapitulatif |
| Bénéfices | Textes à l'écran de chaque scène de démo (« Always know your next move ») |
| Slogan | Dernière phrase, à l'écran et en voix |
| Appel à l'action | Adresse ou bouton de fin |

Si la landing est faible ou absente, écris ces formules avec l'utilisateur **avant** le storyboard (2 ou 3 options chacune, avec ta recommandation), puis tiens-t'en à elles partout.

Remplace « l'IA » par le nom du produit ou de son assistant (« Dropit builds the path », « Ask Dropit AI ») : on doit retenir la marque, pas la technologie.

## 3. Les actes et leur durée

| Acte | Long (≈ 100 s) | Court (60 s) | Ce qui se passe |
|---|---|---|---|
| Accroche | 0–3 s | 0–3 s | Vraie photo du cas + objectif en 2–3 mots + « Where do you even start? » |
| Problème | 3–10 s | 3–9 s | Les outils actuels arrivent de tous les bords (tableur aux cellules #REF!, boîte mail « 214 unread », tâches « 47 overdue », post-it griffonnés, icônes d'applis à pastilles rouges), tremblent, puis s'aspirent au centre : « Still no plan. » |
| Révélation | 10–13 s | 9–11 s | Le logo, animé avec l'idée de la marque (Dropit : la goutte tombe dans le trou et remonte) |
| Promesse | 13–18 s | 11–15 s | Les mots de la landing |
| Démonstration | 18–79 s | 15–49 s | 4 à 6 scènes numérotées, une fonctionnalité chacune |
| Résultat dans le temps | dans la démo | dans la démo | « 3 weeks later » : progression, points, avance sur le rythme |
| Récapitulatif | 79–96 s | 49–55 s | Trois téléphones, titres en badge ; gros plan sur chacun avec ses fonctions en bulles |
| Fin | 96–104 s | 55–61 s | Logo, slogan, adresse |

## 4. Écrire une scène de démonstration

Chaque scène suit le même mouvement, parce que l'œil a besoin d'un repère stable :
1. Le texte à gauche apparaît (numéro d'étape + bénéfice, 2 lignes, un mot surligné).
2. Le téléphone montre l'état de départ en entier.
3. L'action se passe (toucher visible, saisie lettre par lettre, contenu qui apparaît **progressivement**).
4. **Ensuite seulement**, la caméra zoome sur ce qui compte (pas pendant l'action : on perd le fil).
5. Retour au plan large, transition vers la scène suivante.

Textes à l'écran : 2 à 6 mots par ligne, 2 lignes, un seul mot surligné, en anglais simple si le marché est américain. Le texte dit le **bénéfice** (« Every task earns bonus points »), jamais le nom technique de l'écran.

## 5. La voix off

- Écrite en même temps que le storyboard, une réplique par scène, 2 à 13 mots.
- Elle **double ou complète** le texte à l'écran, jamais elle ne le contredit ; à la promesse et à la fin, elle reprend exactement les mots de la landing.
- Phrases courtes, rythme parlé, pas de liste de fonctions : « Check it off. Watch it add up. »
- Budget : environ 2,3 mots par seconde pour une voix posée (130–140 mots pour 60 s, en laissant des respirations pendant les animations fortes). `node scripts/montage.cjs montage-60s.cjs` signale les répliques trop longues pour leur place.
- Pour une voix dans une autre langue que l'anglais, réécrire la voix (pas traduire mot à mot) et refaire les textes à l'écran dans la même langue.

## 6. Le récapitulatif en trois écrans

Trois vues qui couvrent l'usage quotidien (Dropit : « Daily Brief », « Priorities by project », « Inspiration cards »). En vue d'ensemble : **seulement le titre** en grand badge blanc au-dessus de chaque téléphone (un sous-titre en plus se chevauche). En gros plan : le bénéfice apparaît sous le titre, et 3 ou 4 fonctions en bulles blanches, droites, avec une pastille de couleur. Puis une phrase de synthèse (« Every goal. One plan. Every day. »).
