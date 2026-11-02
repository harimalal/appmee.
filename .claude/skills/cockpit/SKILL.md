---
name: cockpit
description: Enregistrer un livrable (artefact, document, page, code livré) dans le Cockpit Projets — avec explication, lien, et plan d'action quand c'est pertinent. À invoquer sur commande en langage naturel ("mets à jour le cockpit", "logue ça dans le cockpit", "ajoute ça au cockpit de <projet>") ET automatiquement juste après avoir livré quelque chose de notable (artefact publié, PR/commit poussé, document terminé) sur un projet suivi — sans attendre qu'on le demande.
---

# Cockpit — tenir le tableau de bord à jour

Le Cockpit Projets est en ligne sur Cloudflare Pages (`/cockpit/` du dépôt `harimalal/appmee.`), données dans la base D1 `cockpit-db` (id `18e5fbc0-71f2-46ea-9171-6070621d5709`). Toute écriture se fait avec `d1_database_query` (Cloudflare Developer Platform). **La page se met à jour instantanément** : elle lit la base en direct, pas besoin de redéployer. Seul un changement du code de la page (`cockpit/index.html` ou `functions/api/[[route]].js`) demande un `git push` + redeploy Cloudflare Pages.

Projets visibles aujourd'hui : `arteasy`, `reflexia`, `worthit`, `appmee`, `dropit`, `declic` (Déclic / CoachSystem). Les autres (`yoitubesum`, `lyonjarrive`, `unclassified`) sont `hidden=1`.

## Quand s'auto-déclencher (sans qu'on le demande)

Juste après avoir :
- publié un artefact (rapport, audit, maquette, deck, dashboard…) pertinent pour un projet suivi,
- terminé une étape de code (commit/push significatif, feature livrée, bug corrigé),
- produit un document de travail (cahier des charges, plan, évaluation) qui mérite d'être retrouvé plus tard,

→ écrire dans le cockpit tout de suite, sans attendre une demande explicite. Un livrable non loggé est un livrable perdu pour Hari.

## Ce qu'on écrit, et où

1. **Identifier le projet** (`project_id` parmi les projets visibles, ou en proposer un nouveau si aucun ne correspond — demander confirmation avant de créer un projet).
2. **Le livrable lui-même** → table `deliverables` :
   - `id` = l'id de l'artefact (ou `<projet>-<slug>` pour un doc/commit sans id naturel)
   - `kind` : `artefact` (claude.ai/artifact), `article` (post/blog publié), `doc` (fichier de dépôt, page, rapport technique)
   - `title` court, `url` (lien direct https ou vide), `note` = l'explication en une phrase (le POURQUOI/CE QUE ÇA RÉSOUT, pas juste le titre répété)
   - `created_at` au format `AAAA-MM-JJ`
3. **Le plan d'action, si le livrable en appelle un** (ex. : un audit qui liste des actions à faire, un correctif qui ouvre plusieurs tâches) → table `steps`, une ligne par action concrète :
   - `id` = `<projet>-<horizon>-<nn>` (prochain numéro libre pour cet horizon)
   - `horizon` (`court`|`moyen`|`long`), `axis` (`produit`|`marketing`|`vente`|`strategie`, ou un nouvel axe via `axes` si besoin)
   - `status` = `todo` (ou `doing` si déjà en cours), `ref` = lien vers le livrable si pertinent, `source` = `claude`
   - Si l'étape a elle-même un détail pas-à-pas (checklist, sous-tâches) → table `substeps`, groupées par `section`
4. **Si le livrable fait avancer ou clôture une étape existante** → `UPDATE steps SET status='done', done_at=<ISO now>, updated_at=<ISO now> WHERE id=...` (ne jamais supprimer une étape : archiver avec `status='archived'` si elle devient obsolète).
5. **Si l'objectif d'un horizon change** → `INSERT OR REPLACE INTO goals (project_id, horizon, objective, updated_at) VALUES (...)`.

## Gabarit SQL

```sql
INSERT INTO deliverables (id, project_id, kind, title, url, note, created_at)
VALUES ('<id>', '<projet>', 'artefact', 'Titre court', 'https://…', 'Explication en une phrase : pourquoi ça compte.', '2026-10-14');

INSERT INTO steps (id, project_id, horizon, axis, title, detail, status, position, ref, source, created_at, updated_at, done_at)
VALUES ('<projet>-court-07', '<projet>', 'court', 'produit', 'Action concrète à faire', 'Détail : contexte, pourquoi, comment.', 'todo', 7, 'https://…', 'claude', '<ISO now>', '<ISO now>', '');
```

Une seule instruction SQL par appel `d1_database_query` quand on utilise `params` ; pour plusieurs lignes sans `params`, un `INSERT ... VALUES (...), (...), (...)` groupé en une seule requête est préférable à N appels séparés.

## Commande en langage naturel

Hari peut dire, par exemple :
- « mets à jour le cockpit » → relire ce qui a été produit depuis la dernière synchro (comparer `deliverables.created_at` le plus récent par projet aux artefacts publiés / commits poussés depuis), combler les trous.
- « logue ça dans le cockpit », « ajoute ça au cockpit de dropit » → logger le dernier livrable produit dans la conversation, avec son plan d'action si pertinent.
- « archive cette étape », « c'est fait » → mettre à jour `steps.status`.

Dans tous les cas : écrire en D1 directement (pas de fichier intermédiaire), confirmer en une phrase ce qui a été ajouté, et signaler les cas ambigus (projet inconnu, doublon probable) plutôt que de deviner silencieusement.
