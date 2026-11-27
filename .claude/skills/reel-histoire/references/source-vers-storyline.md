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

---

## 7. Enseignements du 4e essai (reel Blog Factory : « 64 articles de blog en deux mois »)
Matière : un playbook ancien (artefact du 23/08), un dépôt qui l'a dépassé (journal, skill), et un utilisateur qui dicte l'histoire **en plusieurs vagues** (V1 : 81 articles ; V2 : « en 2 mois », le SEO, la liste des étapes, moins de 90 s). Exemple rempli : `<skill>/assets/exemple-brief-blog-factory.md` ; implémentation : `<skill>/assets/reference-blog-factory/`.

1. **Croiser le playbook avec le dépôt avant de citer un chiffre.** L'artefact annonçait 23 articles, une note moyenne de 89, 4 à 6 h par article, « 4 phases » : le journal donnait 81 articles notés, et le skill cinq étapes (0 à 4). Les chiffres périmés sont **écartés** (liste « Écartés » dans le brief), jamais corrigés de tête.
2. **Vérifier une durée annoncée par une fenêtre de dates.** « En 2 mois » : les 81 articles notés couraient sur 5 mois ; 64 seulement tombaient en août-septembre. Titre et chiffres sont recalculés sur le **sous-ensemble exact** (notes, longueur, couverture), l'utilisateur tranche entre « 64 en 2 mois », « 81 sans durée » ou les deux, et la couverture est refaite.
3. **Dire quand une note est auto-évaluée** (ici l'audit est fait par le processus lui-même) : mention **à l'écran** et dans `SCRIPT.md` ; « reproductible » n'est étayé que par l'étendue des notes.
4. **Lister un système = une étape, une phrase, une rangée.** Cinq étapes, cinq phrases, cinq rangées en cascade ; la **boucle de correction** (« sous 80, on corrige et on recommence ») est dessinée comme une boucle ; ce qui est **règle du skill** est dit comme règle (le journal ne donne pas le nombre de corrections) ; l'effet d'amélioration du système (« les audits corrigent le skill ») ne s'affirme que s'il est daté dans le skill et se montre à l'écran seulement.
5. **Budget de durée quand l'utilisateur donne un plafond** : écrire le budget par scène avant la voix (ici titre 7 s, problème 16 s, étapes 28 s, chiffres 13 s, exemples 12 s, appel 7 s = 82 s sous 90 s) ; remplacer une scène par une autre plutôt qu'en ajouter (la scène « système » est devenue la scène « étapes »).
6. **Une phrase d'accroche dictée par l'utilisateur sur le fond (SEO, intention de recherche, mots-clés, angle original) reste signalée comme la sienne** dans `SCRIPT.md` ; on n'y ajoute aucune promesse de classement.
7. **Montrer la preuve par de vraies pages** : voir `references/production.md` (captures du site construit en local, script `assets/capture-pages.cjs`).

---

## 8. Enseignements du 5e essai (reel Comparatif Factory : « 28 comparatifs »)
Matière : un moteur qui fabrique des comparatifs (artefact + skill + 28 pages publiées), un utilisateur qui dicte l'histoire en quatre vagues. Exemple rempli : `<skill>/assets/exemple-brief-comparatif-factory.md` ; implémentation : `<skill>/assets/reference-comparatif/`.

1. **« Un skill et un système » face à « une simple demande à ChatGPT ou à Claude » se dit comme le constat de l'utilisateur, jamais comme un test.** La phrase est marquée `[À CONFIRMER]` dans le texte à valider, signalée « non testé ici » dans `SCRIPT.md`, et ne dit rien sur les capacités des outils au-delà de son expérience.
2. **Le piège du critère unique se montre au lieu de s'affirmer** : trois exemples réels qui diffèrent (les en-têtes de critères lus dans trois tableaux publiés : voix IA, code, CRM) valent mieux qu'une phrase ; la voix reste courte (trois critères par type), le reste est à l'écran.
3. **Valider un contrôle avec un parseur permissif avant de l'annoncer.** « 2 tableaux sur 28 ne sont pas triés par score » est devenu « 5 sur 28 » quand le contrôle a lu toutes les formes de cellule de score ; l'annonce a été corrigée devant l'utilisateur. Un chiffre de contrôle se recompte avec une deuxième méthode.
4. **Ne pas montrer un défaut de la source** : les exemples sont choisis parmi ceux qui passent le contrôle (tableaux bien triés), et le choix est dit dans `SCRIPT.md` (« 3 comparatifs sur 28, choisis… »).
5. **Source avec un intérêt commercial** (ici des fichiers d'affiliation) : poser la question de l'endroit où le dire (à l'écran, à la voix ou seulement dans `SCRIPT.md`) ; appliquer la réponse sans la contourner ; dire une phrase neutre (« les notes viennent de mes sources, pas d'un test indépendant ») seulement si elle est validée.
6. **Quand l'utilisateur dicte par vagues** (hook gardé, partie retirée, 3 exemples, puis skill et piège) : réécrire le texte complet à chaque vague, le faire valider, ne régénérer que les phrases changées (cache), recompter la durée avant la voix.
7. **Quand la source est la synthèse d'une vidéo tierce** : **créditer l'auteur à l'écran et à la voix, et ne jamais conjuguer ses démos à « je »** ; « je » = seulement ce que l'utilisateur a fait ou dit. Les notes de qualité de l'artefact et les chiffres non sourcés d'un modèle de présentation (« 3 h vs 3 semaines ») sont écartés.
8. **Une preuve « avant / après » se reconstruit depuis l'historique git** (`git archive <commit> | tar -x`, build, captures), sans reconstitution ; on ne prétend pas que l'après est « meilleur » ou « moins IA » : c'est un jugement de goût, et rien ne prouve qu'un outil précis a servi.
