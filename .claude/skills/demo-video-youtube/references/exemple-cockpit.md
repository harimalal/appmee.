# Exemple : « Démo Cockpit Projets » (28 octobre 2026, v3)

https://claude.ai/artifact/TE6Q2c1W7WgZq2yo4J3YkV : comment le créateur pilote 7 projets avec un cockpit que Claude tient à jour. 23 slides, puis 5 slides en réserve. C'est le deuxième exemple après « Démo Veille YouTube ». Il montre surtout **comment adapter le récit** au lieu de recopier le premier.

## Ce que les retours ont appris (v1 → v3)

- La v1 reprenait les 20 slides de la démo Veille, dans le même ordre. Retour : « trop le même framework ». La v2 a repris le récit depuis le problème, avec ses propres animations.
- L'ouverture qui marche : **accroche sur le problème** (la liste des conversations qui défile, « On en était où sur Dropit ? »), puis le **titre** avec la solution redessinée et floutée en fond, puis le **bénéfice** (« Zéro saisie. Rien à payer en plus. »).
- Raconter au **« je »** ce que le créateur a vraiment essayé. Ici Notion branché à Claude : plus une vraie base mise à jour par Claude ; moins il faut aller sur Notion pour voir, chaque consultation coûte des tokens, rien pour ranger les artefacts. On l'apprend en le lui demandant.
- Appel à l'action : un **petit bandeau en bas**, après « Pour qui », jamais en entrée.
- Les slides retirées passent **en réserve**. Le créateur en a ensuite réinséré 7 : garder les anciennes slides a servi.

## Le récit (v3)

Accroche → titre → bénéfice → à quoi ça sert (3 questions, projecteur sur la zone qui répond) → le coût de la reprise (boucle des projets) → trop de projets, une seule tête (5 bénéfices) → pour qui (+ bandeau) → une liste n'est pas un cap → le tableur à la main → Notion branché à Claude → les outils à la mode → et si Claude tenait le tableau ? → la boucle de la solution → pourquoi ça tient → 5 choses qu'il facilite → le prompt → l'inventaire → la structure → l'avancement (top 3) → la mise à jour en direct → le vrai cockpit encart par encart → avant / après → bilan et appel à l'action.

## Techniques réutilisables

- **Capturer un artefact qui a une base de données** : il ne s'affiche pas hors de claude.ai. Lis ses collections avec ArtifactData (`list` avec `out_dir`) et son HTML (`Artifact` read avec `path: "index.html"`), puis `scripts/simuler-base.py` injecte une base simulée avec les vraies données. Fixe l'état voulu (onglet, étape dépliée) avec `--etat`, puis capture avec `capturer-page.cjs`.
- **Interface redessinée en HTML** (classe `.mk`, 900 × 760, positions fixes), plus lisible en vidéo que la capture. Elle sert en fond flouté pour le titre et comme support des projecteurs. La vraie capture sert pour le bénéfice et le détail.
- **Projecteur** `.hl` : un cadre jaune avec une ombre de 2000 px qui assombrit le reste. Un par étape (`data-s` et `data-x`), avec une pastille numérotée qui renvoie à la question.
- **Boucle** : nœuds autour d'un artefact central, flèches en pointillés animées (`.flow`), un nœud par étape.
- **Barres d'avancement** qui se remplissent : classe `.a-sx` (scaleX de 0 à 1).
- **Scène réelle rejouée** : la vraie demande de la conversation, les appels d'outils, puis les lignes qui arrivent dans l'artefact, avec un compteur qui passe de 6 à 10.
- **Vrais chiffres** tirés de la base : 240 étapes, 233 écrites par Claude, 21 objectifs, 133 artefacts, avancements 57 / 52 / 43 %.
