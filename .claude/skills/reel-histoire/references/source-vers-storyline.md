# De la source à la story line (méthode du reel « Créer des carrousels automatiquement »)

Dans ce document, `<skill>` désigne le dossier de ce skill. À lire **avant** d'écrire le brief : comment on passe d'un dossier de travail (playbook, journal, étude, artefact) à une histoire que la voix peut raconter. Implémentation de référence : `<skill>/assets/reference-carrousels/` ; brief rempli : `<skill>/assets/exemple-brief-carrousels-ia.md`.

Particularité de ce 3e essai : la matière n'était pas un seul playbook mais **quatre pièces** (un artefact de synthèse, un journal de production, une étude de modèles, un fichier de dépenses) et **l'angle venait de l'utilisateur**, pas de la source. La méthode ci-dessous marche aussi quand l'utilisateur dicte l'histoire.

## 1. Lire toute la source, puis la réduire à une fiche de faits
1. Lire **chaque pièce en entier** (journal, étude, fichier de chiffres, skill de production). Ne pas se fier au titre de l'artefact.
2. Pour chaque nombre candidat, noter : ce qu'il mesure, la pièce et la section où il se trouve, son statut.
3. Les statuts à distinguer : **mesuré** (renvoyé par un outil ou un fichier), **calculé** (dérivé par moi : à écrire « calcul »), **dit par l'utilisateur** (aucune source dans le dépôt), **objectif**.
4. Écarter les nombres contradictoires entre pièces et ceux que la scène ne peut pas montrer honnêtement.
5. Vérifier que **chaque nombre lu par la voix** est dans `nombres_autorises` et dans la fiche (le contrôle `qa.cjs` le vérifie).

## 2. Trier : ce que la source établit, ce que l'utilisateur apporte
Table à remplir dans le brief (voir l'exemple) :

| Idée de l'histoire | Source dans le dépôt ? | Traitement |
|---|---|---|
| établie par une pièce | oui | dite telle quelle, nombre sourcé |
| donnée par l'utilisateur (son expérience, son point de vue) | non | **je pose la question** ; ses mots sont repris tels quels, présentés à la 1re personne, et signalés « vient de l'utilisateur » dans `SCRIPT.md` |
| ni l'un ni l'autre | non | retirée, ou remplacée par un échec **sourcé** (variante proposée à l'utilisateur) |

Exemple vécu : les problèmes « outils de carrousel IA » et « Canva » n'avaient aucune source dans le dépôt. Les inventer aurait été une donnée fausse ; l'utilisateur a donné ses mots (« à la main, c'est galère » ; « personnalisation basique, rendu moyen, même sur Canva »), repris mot pour mot, avec la mention « son expérience ». Rien n'est affirmé sur les capacités réelles de ces outils.

## 3. Construire la story line
1. **Partir de l'ordre que l'utilisateur dicte**, s'il en donne un : il devient l'ossature (ici : problèmes → système → exemples → appel final). S'il n'en donne pas : le schéma de `recit.md`.
2. **Une scène = une idée = un motif** du catalogue (`motifs-et-charte.md`). On ne réutilise pas deux fois le même motif.
3. **Une phrase de voix = une idée**, 5 à 17 mots, écrite d'abord en clair pour un non-expert, puis relue avec la question : « que retient quelqu'un qui n'a jamais utilisé l'outil ? ».
4. **La preuve est en images réelles.** Le reel montre de vraies pièces du travail (ici 12 vraies slides en défilement, 2 par carrousel, sans aucune image générée pour la vidéo) ; ce que la source ne permet pas de montrer est dessiné en schéma, jamais simulé.
5. **La couverture et la phrase d'ouverture promettent seulement ce que le reel étaie.** Si une scène est retirée, relire l'ouverture et la couverture.
6. **Faire valider le texte (17 phrases facturées dans l'exemple) avant la voix** : `TEXTE_A_VALIDER.md`, légendes comprises, avec marquage `[À CONFIRMER]` sur ce qui n'est pas sourcé.

## 4. Élaguer sans casser l'histoire
Le premier montage avait 7 scènes (84,7 s) : titre, problèmes, système, **coûts**, **minimum/outils**, exemples, appel final. Sur retour de l'utilisateur, les scènes « coûts » et « minimum/outils » ont été retirées (56,7 s). Procédure :
1. Retirer l'entrée de la scène dans `story.json` **et** le bloc `scene(...)` de `story.html` ; le compteur « n/N » se recalcule seul.
2. Les phrases de voix retirées n'imposent aucune nouvelle requête de synthèse : le cache de voix est par texte, les phrases gardées sont réutilisées (copier `trim/` des phrases gardées, rejouer `plan.py`).
3. Relire les **nombres autorisés** (laisser ceux encore lus) et les **mentions de prix ou de capacité** restantes : une promesse d'ouverture (« moins d'un euro avec des images ») qui n'est plus étayée à l'écran se **signale** dans `SCRIPT.md` (ici : vrai en moyenne, 0,82 € ; deux carrousels sur six dépassent 1 €) et se propose à l'utilisateur de la qualifier (« en moyenne »).
4. Garder l'ancienne version (`out/<nom>-long.mp4`, non versionnée) : la suppression est un choix éditorial réversible.
Règle de fond : on peut retirer une scène pédagogique ou chiffrée, **jamais la scène preuve** (ici les exemples réels).

## 5. Limites à écrire dans `SCRIPT.md` (et à dire à l'utilisateur)
- Moyenne ≠ chaque cas ; part de cas qui échappent à la règle.
- Source ou usage non exercés dans le journal (ici : une vidéo comme source ; seuls des articles de blog avaient été traités).
- Ce que la vidéo ne dit pas (aucune donnée d'audience dans le journal).
- Ce qui n'a pas pu être vérifié (son non écouté, rendu sur téléphone).
- Modèle de voix de repli si le quota du modèle principal est atteint (voir `production.md`).

## 6. Résumé en 8 gestes
1. Lire toute la source. 2. Fiche de faits sourcée. 3. Trier sourcé / apporté par l'utilisateur. 4. Ossature = ordre dicté, un motif par scène. 5. Phrases en clair, une idée chacune. 6. Preuve en vraies pièces. 7. Texte validé avant la voix. 8. Élaguer par scènes entières et relire l'ouverture.
