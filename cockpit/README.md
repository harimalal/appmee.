# Cockpit projets

Tableau de bord de suivi de tous les projets, servi par Cloudflare Pages à l'adresse `/cockpit/`.

- **Onglets** : « Vue d'ensemble » + un onglet par projet.
- **Dans chaque projet** : *Plan d'action* (thématiques dépliables → tâches → sous-tâches, idées), *Historique* (tout ce qui a été fait, jour par jour), *Livrables* (artefacts, articles, docs).
- **Tout s'édite** : clic sur un titre pour le renommer, ✓ pour terminer, ◐ statut, ⚑ priorité, ＋ sous-tâche, ⋯ détails (notes, lien, déplacer vers un autre projet/thème, supprimer). Glisser-déposer avec la poignée ⋮⋮ (tâches entre thématiques, dans une sous-liste, thématiques entre elles, cartes projets).
- **Ajout rapide** : barre du haut (Tâche / Idée + thématique), ou le champ en bas de chaque thématique (commencer par `?` pour une idée).
- Rafraîchissement automatique toutes les 20 s : ce que Claude ajoute apparaît tout seul.

## Architecture

| Élément | Où |
|---|---|
| Interface | `cockpit/index.html`, `app.css`, `app.js`, `vendor/Sortable.min.js` |
| API | `functions/api/[[route]].js` (Pages Functions) |
| Base | D1 `cockpit-db` (`6c0e61f0-271c-43bc-998e-d01e6e4485f0`), schéma `cockpit/schema.sql` |
| Accès | jeton Bearer ; seul son SHA-256 est stocké (`settings.token_hash`) |

API (toutes les routes exigent `Authorization: Bearer <jeton>`) :
`GET /api/state` · `POST /api/{projects|themes|items}` · `PATCH|DELETE /api/{table}/{id}` · `POST /api/reorder {table, moves:[{id, position, theme_id?, parent_id?}]}`.

## Mise en ligne (une seule fois)

1. Cloudflare → **Workers & Pages** → le projet Pages relié à ce dépôt → **Settings → Bindings → Add → D1 database**.
   Nom de variable : `DB` — base : `cockpit-db`. Enregistrer.
2. **Deployments** → relancer le dernier déploiement (ou pousser un commit).
3. Ouvrir `https://<projet>.pages.dev/cockpit/` et entrer le jeton.

Sans l'étape 1, l'API répond « Liaison D1 "DB" absente » et l'interface l'affiche.

## Changer le jeton

```sql
-- remplacer <sha256> par le SHA-256 hexadécimal du nouveau jeton (ex. : printf '%s' 'nouveau-jeton' | sha256sum)
UPDATE settings SET value = '<sha256>' WHERE key = 'token_hash';
```

## Mise à jour automatique par Claude

Voir `CLAUDE.md` à la racine : les sessions Claude écrivent directement dans D1 (outil Cloudflare `d1_database_query`)
quand un artefact/article est publié, qu'une tâche est finie, ou qu'un plan d'action est demandé.
Pour que ça marche aussi dans les conversations hors de ce dépôt, recopier ce paragraphe dans les préférences Claude
(claude.ai → Paramètres → Profil) :

> Après chaque artefact ou article publié, chaque tâche terminée, et chaque plan d'action ou idée que je te donne,
> mets à jour mon cockpit : base Cloudflare D1 `cockpit-db` (id 6c0e61f0-271c-43bc-998e-d01e6e4485f0), tables
> projects / themes / items / activity, `source='claude'`. Les consignes SQL sont dans le CLAUDE.md du dépôt harimalal/appmee.
