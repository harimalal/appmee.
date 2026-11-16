# Cockpit Projets

Tableau de bord personnel de Hari, en ligne sur Cloudflare Pages (projet `cockpit-projets`).

- Adresse : https://cockpit-projets.pages.dev/cockpit/ — la racine `/` y renvoie (`_redirects` + `index.html`).
- Page : `cockpit/index.html` (une seule page, sans dépendance).
- API : `functions/api/[[route]].js` (Pages Functions), liée à la base D1 `cockpit-db` (variable `DB`, voir `wrangler.toml`).
- Schéma de la base : `cockpit/schema.sql`.
- Consignes de mise à jour par Claude : `CLAUDE.md`.

Chaque `git push` sur la branche suivie par Cloudflare Pages redéploie le site.

## Jette (`/jette/`)

App de to-do ultra simple : un champ, on y jette une idée, Claude la décortique en carte (emoji, titre à l'infinitif, thème, sous-tâches).
Les cartes se swipent, se filtrent par thème (puces au-dessus du champ) et sont gardées dans le navigateur (`localStorage`).

- Page : `jette/index.html` — API : `functions/api/jette.js` (appelle l'API Anthropic, modèle `claude-haiku-5-5`, surchargeable par `ANTHROPIC_MODEL`).
- À régler une fois dans Pages → Settings → Variables and Secrets : secret **`ANTHROPIC_API_KEY`**, puis redéployer.
- Même jeton d'accès que le cockpit (déjà saisi sur l'appareil = rien à refaire).
