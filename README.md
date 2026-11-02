# Cockpit Projets

Tableau de bord personnel de Hari, en ligne sur Cloudflare Pages (projet `cockpit-projets`).

- Adresse : https://cockpit-projets.pages.dev/cockpit/ — la racine `/` y renvoie (`_redirects` + `index.html`).
- Page : `cockpit/index.html` (une seule page, sans dépendance).
- API : `functions/api/[[route]].js` (Pages Functions), liée à la base D1 `cockpit-db` (variable `DB`, voir `wrangler.toml`).
- Schéma de la base : `cockpit/schema.sql`.
- Consignes de mise à jour par Claude : `CLAUDE.md`.

Chaque `git push` sur la branche suivie par Cloudflare Pages redéploie le site.
