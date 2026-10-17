# Master IA — bibliothèque de ressources d'apprentissage

Tu colles un lien (ou tu demandes à Claude d'en chercher) ; la plateforme crée la fiche : **titre, catégorie, tags, description et note de pertinence /10** par rapport à ton profil d'apprentissage.

Projet Cloudflare Pages dédié : https://master-ia-qd7.pages.dev

## Ce que ça fait

| Onglet | Rôle |
|---|---|
| Bibliothèque | Recherche, filtres (catégorie, source, statut, note), tri, statut de suivi (à voir / en cours / terminé), notes perso, export JSON/CSV, « re-noter » une fiche |
| Ajouter des liens | Un lien par ligne : YouTube (vidéo/playlist), Udemy, Coursera, OpenClassrooms, ou tout autre site. Doublons détectés (`youtu.be/x` = `youtube.com/watch?v=x`, paramètres de tracking retirés) |
| Découvrir | Tu décris un besoin, tu coches les plateformes (+ sites dédiés au choix, ex. `huggingface.co`) ; Claude cherche avec `web_search` restreint à ces domaines, tu ajoutes ce que tu veux |
| Mon profil | Le texte par rapport auquel les notes sont calculées. « Re-noter toute la bibliothèque » après l'avoir modifié |

## Comment la note /10 est produite

Claude reçoit les métadonnées de la page + ton profil, et note selon une grille fixe : adéquation avec tes objectifs (40 %), profondeur/rigueur (20 %), actualité (15 %), aspect pratique (15 %), signaux de qualité (10 %). Repères : 9-10 incontournable, 5-6 utile mais généraliste, 0-2 hors sujet.

**Limite importante** : Claude n'a pas regardé la vidéo ni suivi le cours, il juge sur titre, description, chaîne, JSON-LD… Chaque fiche porte donc un indice de **confiance** ; quand il est « faible » (peu d'informations), la note est plafonnée à 7 et la fiche affiche « note peu fiable ». Prends la note comme un tri initial, pas comme un verdict.

## Mise en route

Master IA est un projet Cloudflare Pages **autonome** (dossier `master-ia/` : interface, `functions/`, `package.json`, `wrangler.toml`), indépendant du reste d'AppMétier.

Déjà en place sur le compte Cloudflare : projet Pages `master-ia` (https://master-ia-qd7.pages.dev), base D1 `master-ia-db` avec le schéma appliqué, secret `MASTER_IA_TOKEN`.

**Reste à faire une fois : la clé Anthropic** (sans elle, ajout et recherche répondent « ANTHROPIC_API_KEY manquante ») :

```bash
cd master-ia
npx wrangler pages secret put ANTHROPIC_API_KEY --project-name=master-ia
# optionnel : npx wrangler pages secret put YOUTUBE_API_KEY --project-name=master-ia
```

(ou Cloudflare → Workers & Pages → master-ia → Settings → Variables and Secrets). Les secrets s'appliquent au déploiement suivant : relance `npm run deploy`.

Redéployer après une modification : `cd master-ia && npm install && npm run deploy` (nécessite `CLOUDFLARE_API_TOKEN` et `CLOUDFLARE_ACCOUNT_ID`).

Développement local :

```bash
cd master-ia && npm install
cp .dev.vars.example .dev.vars          # MASTER_IA_TOKEN, ANTHROPIC_API_KEY
npm run migrate:local && npm run dev    # http://localhost:8788/
```

Créer l'environnement sur un autre compte : `npx wrangler d1 create master-ia-db`, reporter le `database_id` dans `wrangler.toml`, `npm run migrate:remote`, `npx wrangler pages project create master-ia`, les secrets, puis `npm run deploy`.

`MASTER_IA_TOKEN` protège toute l'API (`/api/master-ia/*`) ; l'interface le demande une fois et le garde dans le navigateur. Sans jeton configuré, l'API refuse tout. Outil mono-utilisateur : pas de comptes.

## Réglages (variables d'environnement)

| Variable | Défaut | Effet |
|---|---|---|
| `ANTHROPIC_MODEL` | `claude-opus-5-5` | Modèle des fiches et de la recherche. `claude-sonnet-5-5` ou `claude-haiku-5-5` coûtent moins cher |
| `ANTHROPIC_EFFORT` | `medium` | Profondeur de raisonnement (`low`/`medium`/`high`) |
| `YOUTUBE_API_KEY` | — | Sans elle : titre + chaîne (oEmbed). Avec : description, durée, vues, tags, date |

Coût : un appel Claude par lien ajouté, et un appel avec recherche web par recherche « Découvrir ». Quelques centimes par lien avec le modèle par défaut (estimation, non mesurée) : vérifie sur ta console Anthropic. Si le modèle décline une requête pour une raison de politique, l'API retente automatiquement sur un modèle de repli (`fallbacks: "default"`).

## Architecture

```
index.html, css/, js/      interface (HTML/CSS/JS sans dépendance) · schema.sql (D1)
functions/api/master-ia/   API (Cloudflare Pages Functions)
  resources/               GET liste+filtres · POST ajout · [id] PATCH/DELETE · [id]/rescore
  discover.js              recherche Claude + web_search
  settings.js              profil + taxonomie
functions/_lib/master-ia/  sources.js (URL, oEmbed/API YouTube, Open Graph, JSON-LD) · claude.js · db.js
```

Métadonnées, dans l'ordre : YouTube → oEmbed (+ API Data si clé) ; autres sites → balises Open Graph et JSON-LD ; si la plateforme bloque la requête serveur (fréquent sur Udemy, Coursera, OpenClassrooms), Claude lit la page avec l'outil `web_fetch`. Pas de scraping massif.

Les catégories viennent d'une liste fixe (`functions/_lib/master-ia/taxonomy.js`) pour rester stables ; adapte-la à ton programme.

## Faut-il le construire, ou ça existe déjà ?

**Déjà disponible — ne pas reconstruire :** enregistrer, ranger, chercher et tagger des liens avec une IA.
- [Karakeep](https://github.com/karakeep-app/karakeep) (open source, auto-hébergé) : tags et résumés automatiques par IA (OpenAI ou modèles locaux via Ollama), recherche plein texte, extensions navigateur, API REST. Je n'ai rien trouvé indiquant qu'il analyse le contenu des vidéos YouTube.
- [Raindrop.io](https://raindrop.io) : stockage gratuit ; l'assistant IA (tags suggérés, recherche en langage naturel) est dans l'offre Pro, environ 3 $/mois selon des sources secondaires (à vérifier sur leur site).
- Notion (web clipper + propriétés remplies par IA) si tu y travailles déjà.

**Pas trouvé tel quel :** une note de pertinence /10 calculée par rapport à *tes* objectifs de Master, et une recherche de ressources limitée aux plateformes de ton choix. C'est ce que couvre cette app, et la seule raison de la garder.

**Accès aux plateformes (état de mes recherches, à vérifier avant de t'y appuyer) :**
- YouTube : API officielle gratuite (clé requise) → utilisée en option.
- Udemy : une API « Affiliate » existe (clés à demander) → non utilisée ; la recherche passe par le web.
- Coursera : pas d'API publique ouverte à tous d'après un blog secondaire (catalogue pour partenaires/affiliés).
- OpenClassrooms : rien trouvé sur une API publique.

D'où `web_search` / `web_fetch` plutôt qu'un scraping fragile et contraire aux conditions d'usage de ces sites.

**Recommandation :** si tu veux seulement une bibliothèque taguée, installe Karakeep ou prends Raindrop Pro. Garde cette app si la note de pertinence et la découverte guidée te servent vraiment ; ne l'étends pas en gestionnaire de favoris complet, ce serait refaire Karakeep.

## Tests

```bash
cd master-ia && npm test
```

Couvre la normalisation d'URL, l'anti-SSRF, l'analyse HTML/JSON-LD, l'extraction JSON et la validation des fiches. Les appels réels à Claude et aux plateformes ne sont pas couverts par des tests automatiques.
