# Consignes pour Claude

## Cockpit Projets — le tenir à jour

Le tableau de bord de Hari est l'artefact **Cockpit Projets** : https://claude.ai/artifact/9wYVLBBGwL521kfMMgAiVu
Ses données sont dans la base de l'artefact (outil `ArtifactData`, `url` = le lien ci-dessus). Hari ne tape presque rien :
c'est à Claude de proposer et de tenir à jour les objectifs et les étapes. Hari coche, archive, supprime, et écrit des idées.

Projets affichés : `arteasy`, `reflexia`, `worthit`, `appmee`. Les autres (`dropit`, `yoitubesum`, `lyonjarrive`, `unclassified`)
ont `hidden: true` et ne s'affichent pas.

**Collections**
- `goals/<projet>__<horizon>` : `{projectId, horizon, objective, source:'claude', updated_at}` — une phrase par horizon.
- `steps/<id>` : `{projectId, horizon, domain, title, detail, status, order, ref, source:'claude', created_at, updated_at, done_at}`
  - `horizon` : `court` (2 semaines) | `moyen` (1 à 3 mois) | `long` (6 à 12 mois)
  - `domain` : `produit` | `marketing` | `vente` | `strategie`
  - `status` : `todo` | `doing` | `done` | `archived` ; `done_at` = date ISO quand `done`, sinon `""`
  - `title` : une ligne courte, lisible d'un coup d'œil. Le reste va dans `detail`. `ref` : lien https direct (artefact, doc) ou `""`.
  - id : `<projet>-<horizon>-<nn>`
- `artifacts/<id artefact>` : `{projectId, title, url, created_at (AAAA-MM-JJ), status, note}` — tous les artefacts, avec lien direct.
- `ideas/<id>` : écrites par Hari depuis la page `{projectId, text, status:'new', created_at}`.

**Quand agir, sans qu'on le demande**
- Au début d'une conversation sur un projet : lire `ideas` où `status == 'new'`, les transformer en étapes (ou ajuster les objectifs),
  puis passer l'idée en `status:'triaged'` avec une `claude_note` d'une phrase.
- Un artefact ou un article est publié → ajouter un doc `artifacts`.
- Une étape est terminée pendant la session → `status:'done'`, `done_at`.
- Hari demande « les prochaines choses à faire » ou un plan → créer ou modifier `goals` et `steps`.
Toujours passer `if_version` quand on modifie un document déjà lu. Ne jamais supprimer sans que Hari le demande (archiver à la place).
