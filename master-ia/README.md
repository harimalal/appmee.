# Master IA — bibliothèque de ressources d'apprentissage

Tu colles un lien (ou tu demandes à Claude d'en chercher) ; la plateforme crée la fiche : **titre, catégorie, tags, description et note de pertinence /10** par rapport à ton profil d'apprentissage.

Accessible sur `/master-ia/` une fois déployé avec le reste d'AppMétier (Cloudflare Pages).

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

Prérequis : compte Cloudflare, clé API Anthropic.

```bash
npm install
npx wrangler d1 create master-ia                 # note le database_id retourné
cp master-ia/wrangler.example.toml wrangler.toml # colle le database_id
cp .dev.vars.example .dev.vars                   # renseigne MASTER_IA_TOKEN et ANTHROPIC_API_KEY
npx wrangler d1 execute master-ia --local --file=master-ia/schema.sql
npm run master-ia:dev                            # http://localhost:8788/master-ia/
```

Production (Cloudflare Pages) :

1. `npx wrangler d1 execute master-ia --remote --file=master-ia/schema.sql`
2. Pages → Settings → **Bindings** : D1 database, variable `MASTER_IA_DB` → la base `master-ia`.
3. Pages → Settings → **Variables and Secrets** (type Secret) : `MASTER_IA_TOKEN`, `ANTHROPIC_API_KEY`, et en option `YOUTUBE_API_KEY`.
4. Déploie via Git (Cloudflare installe `@anthropic-ai/sdk` d'après `package.json` et compile `functions/`) ou avec `wrangler pages deploy`. Le glisser-déposer du dossier ne compile pas les dépendances.

`MASTER_IA_TOKEN` protège toute l'API (`/api/master-ia/*`) ; l'interface le demande une fois et le garde dans le navigateur. Sans jeton configuré, l'API refuse tout. C'est un outil mono-utilisateur : pas de comptes.

## Réglages (variables d'environnement)

| Variable | Défaut | Effet |
|---|---|---|
| `ANTHROPIC_MODEL` | `claude-opus-5-5` | Modèle des fiches et de la recherche. `claude-sonnet-5-5` ou `claude-haiku-5-5` coûtent moins cher |
| `ANTHROPIC_EFFORT` | `medium` | Profondeur de raisonnement (`low`/`medium`/`high`) |
| `YOUTUBE_API_KEY` | — | Sans elle : titre + chaîne (oEmbed). Avec : description, durée, vues, tags, date |

Coût : un appel Claude par lien ajouté, et un appel avec recherche web par recherche « Découvrir ». Quelques centimes par lien avec le modèle par défaut (estimation, non mesurée) : vérifie sur ta console Anthropic. Si le modèle décline une requête pour une raison de politique, l'API retente automatiquement sur un modèle de repli (`fallbacks: "default"`).

## Architecture

```
master-ia/                 interface (HTML/CSS/JS sans dépendance) + schema.sql (D1)
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
npm run master-ia:test
```

Couvre la normalisation d'URL, l'anti-SSRF, l'analyse HTML/JSON-LD, l'extraction JSON et la validation des fiches. Les appels réels à Claude et aux plateformes ne sont pas couverts par des tests automatiques.
