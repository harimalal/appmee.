# Socles techniques pour systèmes d'automatisation IA « prêts à l'emploi » (solo-entrepreneur) — état au 25 octobre 2026

> Notes de recherche. Chiffres datés quand la source le permet. Beaucoup de sources de prix sont des blogs tiers (souvent concurrents) : à revérifier sur les pages officielles avant de publier. L'accès direct à n8n.io, zapier.com, make.com et à l'API GitHub a échoué pendant la recherche (DNS / proxy) : les chiffres viennent des pages GitHub rendues, des docs officielles Claude Code et de recherches web.

## 1. Métriques d'écosystème en 2026 (n8n, MCP, marketplaces Claude, Zapier/Make, frameworks)

### Takeaway
n8n domine en communauté (~209 k étoiles, 9 000+ modèles revendiqués) ; Zapier a le plus de connecteurs (9 000+ apps) ; l'écosystème Claude (skills ~184 k étoiles, knowledge-work-plugins ~33 k, claude-plugins-official ~44,5 k) est désormais comparable en taille communautaire, mais en « briques » (skills/plugins) plutôt qu'en workflows clés en main. Le registre MCP officiel compte des dizaines de milliers de serveurs, de qualité très inégale.

### Cited Findings
**n8n**
- Dépôt n8n-io/n8n : ~208,6 k étoiles (209 k affichées), 61,2 k forks (relevé 25/10/2026) — [GitHub n8n-io/n8n](https://github.com/n8n-io/n8n)
- Le README annonce « 1500+ » intégrations et « 9,000+ » modèles de workflows ; la section About du même dépôt dit « 400+ » intégrations (contradiction interne : 400+ = nœuds natifs probablement, 1500+ = en comptant les nœuds communautaires/génériques — à vérifier) — [GitHub n8n-io/n8n](https://github.com/n8n-io/n8n)
- Licence : « Sustainable Use License » + « n8n Enterprise License » pour les fonctions entreprise ; n8n se décrit comme « fair-code » (pas open source au sens OSI) — [GitHub n8n-io/n8n](https://github.com/n8n-io/n8n)

**Marketplaces Claude Code / Cowork**
- anthropics/skills : ~183,7 k étoiles, 21,7 k forks. Skills regroupés en 4 familles : Creative & Design, Development & Technical, Enterprise & Communication, Document Skills (docx, pdf, pptx, xlsx). Contient aussi un `template` et la spécification Agent Skills. Licence : beaucoup de skills en Apache 2.0, mais docx/pdf/pptx/xlsx sont « source-available », pas open source. Installation : `/plugin marketplace add anthropics/skills` puis `/plugin install document-skills@anthropic-agent-skills` ou `example-skills@anthropic-agent-skills` — [GitHub anthropics/skills](https://github.com/anthropics/skills)
- anthropics/knowledge-work-plugins : ~32,9 k étoiles, 3,6 k forks, 1 124 commits. 11 plugins listés dans la marketplace : productivity, sales, customer-support, product-management, marketing, legal, finance, data, enterprise-search, bio-research, cowork-plugin-management. Dossiers supplémentaires hors table : engineering, design, human-resources, operations, small-business, pdf-viewer, partner-built. Installation Cowork via claude.com/plugins ; Claude Code : `claude plugin marketplace add anthropics/knowledge-work-plugins` puis `claude plugin install sales@knowledge-work-plugins` ; commandes du type `/sales:call-prep` — [GitHub anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
- anthropics/claude-plugins-official : ~44,5 k étoiles, 4,7 k forks, 4 632 commits. Deux dossiers : `/plugins` (plugins internes maintenus par Anthropic) et `/external_plugins` (partenaires/communauté, soumis à des critères de qualité et sécurité). Le nombre exact de plugins n'est pas affiché sur la page d'accueil — [GitHub anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

**MCP (Model Context Protocol)**
- Registre MCP officiel : ~30 375 serveurs uniques au 10/09/2026 (99 114 enregistrements serveur+version), contre ~9 650 en mai 2026 ; un tiers publiés par ~50 comptes — [dev.to, « The MCP registry by the numbers »](https://dev.to/amareswer/the-mcp-registry-by-the-numbers-38nc)
- Autre estimation : ~16 967 serveurs publiés au 16/07/2026 ; le registre est encore formellement en « preview », API figée en v0.1 — [Towards AI, « MCP Registries in Mid-2026 »](https://pub.towardsai.net/mcp-registries-in-mid-2026-one-upstream-won-2ce541b92036)

**Zapier / Make**
- Zapier est passé de « 8 000 » à « 9 000+ » apps dans sa communication en mai 2026 — [PricingSaaS, diff Zapier S21 2026](https://pricingsaas.com/companies/zapier/diffs/2026W21) ; [Latenode, Zapier MCP pricing](https://latenode.com/blog/zapier-mcp-pricing)
- Make : aucun chiffre fiable de nombre d'apps trouvé dans cette recherche (voir Gaps).

**Frameworks d'agents open source (étoiles GitHub, chiffres tiers)**
- CrewAI : 45,9 k (début 2026) à 57 217 (tableau d'août 2026) ; LangGraph : 39 876 (août 2026) — d'autres sources donnent 16 k–28,5 k (anciennes) — [Spheron, LangGraph vs CrewAI vs AutoGen 2026](https://www.spheron.network/blog/langgraph-vs-crewai-vs-autogen-2026/)
- Dify : 136 k–144 k étoiles selon les classements ; Flowise : 51 582 ; Agno : 39 189 (dates de relevé non précisées) — [Fungies, Top 20 GitHub AI agents 2026](https://fungies.io/top-github-repositories-ai-agent-frameworks-2026/) ; [Firecrawl, best open source agent frameworks](https://firecrawl.dev/blog/best-open-source-agent-frameworks)
- Les étoiles reflètent une adoption cumulée historique, pas la pertinence actuelle — [Spheron](https://www.spheron.network/blog/langgraph-vs-crewai-vs-autogen-2026/)

**Systèmes d'agents « tout-en-un » open source**
- OpenClaw (démon passerelle TypeScript auto-hébergé reliant un LLM aux messageries, licence MIT) : >350 k étoiles en ~5 mois, >374 k en mai 2026, >384 k selon une mise à jour ultérieure — [Elestio blog](https://blog.elest.io/openclaw-explained-how-the-fastest-growing-open-source-project-became-a-self-hosted-ai-agent-for-everyone/) ; [Fast.io review](https://fast.io/resources/openclaw-review-2026/)
- Risques : 543 CVE recensées nommant OpenClaw (décompte tiers, vendeur d'alternatives), injection de commandes et RCE via prompt-injection, centaines de paquets malveillants sur ClawHub, avis formel du CNCERT chinois sur la config par défaut — [Pinggy, alternatives OpenClaw](https://pinggy.io/blog/best_openclaw_alternatives/) ; [Towards AI, « The OpenClaw mess »](https://pub.towardsai.net/the-openclaw-mess-why-your-autonomous-agent-is-a-security-suicide-note-be0cb3bf526b)

### Inferences
- Pour un « pack » prêt à l'emploi, n8n offre la plus grande bibliothèque de workflows copiables (JSON importable) ; Claude offre des briques réutilisables (skills/plugins) qui sont agnostiques de la niche par construction (knowledge-work-plugins couvre déjà sales/marketing/finance/ops/small-business).
- Le nombre de serveurs MCP est un indicateur de vitalité mais pas de qualité : un pack sérieux doit lister les serveurs utilisés, leur éditeur (officiel vs communautaire) et leur version.
- Les marketplaces de skills communautaires (ClawHub en exemple négatif) sont un vecteur d'attaque : critère « provenance/sécurité des extensions » indispensable dans la checklist.

### Gaps
- Nombre exact de plugins dans claude-plugins-official et liste précise des skills d'anthropics/skills : non affichés sur les pages d'accueil (consulter les fichiers `marketplace.json`).
- Nombre d'apps Make en 2026 et nombre de modèles Make/Zapier : non trouvés.
- Étoiles actuelles (oct. 2026) de CrewAI, LangGraph, Agno, Dify, Flowise, OpenAI Agents SDK : l'API GitHub était bloquée ; chiffres tiers datés d'août 2026 ou non datés. OpenAI Agents SDK : aucun chiffre trouvé.
- Nombre exact de modèles n8n vérifié sur n8n.io/workflows : site injoignable.

## 2. Quelle combinaison est la plus robuste pour l'automatisation « sans surveillance » (cron, gestion d'erreurs, reprises) ?

### Takeaway
Pour des tâches déterministes répétitives (publier, synchroniser, relancer), un orchestrateur de workflows (n8n auto-hébergé ou cloud, Make, Zapier) reste le plus fiable : cron natif, « Retry On Fail » par nœud, workflows d'erreur. Claude Code en tâches planifiées cloud (ex-« routines ») est adapté au travail de jugement (rédaction, analyse, tri) mais reste en « research preview », avec un intervalle minimal d'une heure et un statut « Succeeded » qui ne garantit pas que le travail a été fait. La combinaison la plus robuste : orchestrateur = colonne vertébrale (planif + reprises + alertes) qui appelle l'IA (API LLM ou endpoint `/fire` d'une tâche Claude) pour les étapes intelligentes.

### Cited Findings
**Claude Code — trois modes de planification (doc officielle)**
- Cloud (tâches planifiées, ex-routines) : tournent sur l'infra Anthropic, ne nécessitent ni machine allumée ni session ouverte, persistent, intervalle minimum 1 heure ; Desktop : sur la machine, nécessite la machine allumée ; `/loop` : nécessite une session ouverte, intervalle 1 minute — [Claude Code docs, Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks.md)
- `/loop` et tâches de session : expiration automatique au bout de 7 jours ; pas de rattrapage des exécutions manquées ; max 50 tâches par session ; décalage (jitter) jusqu'à 30 min pour les tâches horaires ou quotidiennes — [Claude Code docs, Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks.md)
- Tâches cloud : « research preview », comportement/limites/API susceptibles de changer ; disponibles sur les plans Pro, Max, Team, Enterprise ; déclencheurs Schedule, API (POST avec jeton) et GitHub ; les expressions cron plus fréquentes qu'une fois par heure sont refusées ; cron en UTC sauf préfixe `CRON_TZ=` — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md)
- Limites horaires : 100 exécutions planifiées/heure par compte ; « Run now » + API = 30/heure par tâche ; 100 déclenchements API/heure par compte ; pas de dépassement payant sur ces limites ; les tâches consomment le quota d'abonnement comme une session interactive — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md)
- Fiabilité : « Succeeded » signifie seulement que la session s'est terminée sans échec ; requêtes réseau bloquées, outils de connecteur manquants ou travail non abouti n'apparaissent que dans la transcription. Si la connexion GitHub expire, les exécutions sont sautées jusqu'à 72 h puis la tâche se désactive — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md)
- Les exécutions démarrent en « auto mode » (un classifieur autorise/bloque) mais peuvent s'arrêter en attendant une validation humaine (règles « ask », blocages répétés) — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md)
- Endpoint `/fire` sous en-tête bêta `experimental-cc-routine-2026-04-01` ; les changements cassants passent par de nouveaux en-têtes datés, les deux versions précédentes restent acceptées — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md)
- Lancement des routines en research preview le 14/04/2026 (source tierce) — [Computingforgeeks / guides tiers](https://computingforgeeks.com/claude-code-routines-setup/)

**n8n — gestion d'erreurs**
- Trois voies de reprise : relance manuelle depuis l'onglet Executions, réglage « Retry On Fail » par nœud, workflow « Error Trigger » qui relance via « Execute Workflow » — [RapidDevelopers, retry n8n](https://www.rapidevelopers.com/md/n8n-tutorial/how-to-retry-failed-workflows-in-n8n)
- Pour les agents IA dans n8n : Error Trigger + reprises + modèles de repli (fallback) — [KodeKloud, n8n Retries and Error Handling](https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Additional-Info/Retries-and-Error-Handling/page)
- n8n peut être exposé comme serveur MCP ; il est recommandé de renvoyer des messages d'erreur explicites pour que l'agent sache s'il doit réessayer — [sipgate, MCP server with n8n](https://help.sipgate.com/en/connections-and-integrations/mcp-server-mit-n8n)
- Piège : un déclencheur par interrogation (polling) Gmail toutes les 5 min dépasse 8 600 exécutions/mois — [Activepieces, n8n pricing 2026](https://www.activepieces.com/blog/n8n-pricing-2026-plans-free-tier-costs-explained.md)

**Zapier MCP**
- Statut MCP ambigu : listé comme fonction de plan sur la page tarifs mais étiqueté bêta sur la page MCP — [Latenode, Zapier MCP pricing](https://latenode.com/blog/zapier-mcp-pricing)

**Make AI Agents**
- Le module/app Make AI Agents est en bêta ouverte depuis le 2 février 2026 ; Make prévient que la tarification peut changer — [Latenode, Make pricing](https://latenode.com/blog/make-com-pricing) ; [eesel, Make review 2026](https://www.eesel.ai/blog/make-review)

### Inferences
- Architecture recommandée « hybride » : n8n (ou Make) gère cron, files, reprises, alertes, journalisation et publication ; l'IA (API Claude/OpenAI, ou tâche Claude via `/fire`) produit le contenu ; une étape de contrôle (validation humaine ou contrôle automatique de format) précède la publication.
- Les trois couches « agentiques » (tâches Claude cloud, Zapier MCP, Make AI Agents) sont toutes en preview/bêta en oct. 2026 : risque de changements cassants à intégrer au calcul de maintenance d'un pack.
- Une tâche Claude cloud doit écrire un signal de succès vérifiable (ligne en base, fichier, message Slack) pour être surveillée, car le statut d'exécution ne suffit pas.
- Les tâches Claude Desktop ne conviennent pas au « sans surveillance » si l'ordinateur peut être éteint.

### Gaps
- Pas de doc officielle n8n consultée sur le nœud « MCP Server Trigger » et le comportement des reprises dans le nœud AI Agent (n8n.io injoignable).
- Pas de données publiques comparatives de taux de panne/uptime (n8n Cloud, Make, Zapier, tâches Claude).
- Mécanismes de reprise des scénarios Make (« incomplete executions ») et de Zapier (autoreplay) non vérifiés dans cette recherche.

## 3. Modèles de prix et coûts mensuels réalistes (hébergement + API LLM + API vidéo)

### Takeaway
Un solo-entrepreneur peut faire tourner un socle complet pour environ 30–150 €/mois hors vidéo : n8n Community auto-hébergé (VPS ~5–20 €) ou n8n Cloud Starter (~20–24 €), + API LLM (quelques euros à quelques dizaines selon volume, avec cache et batch), ou un abonnement Claude Pro/Max qui couvre aussi les tâches planifiées. La vidéo générée est le poste qui explose : 0,03 à 0,60 $/seconde, soit ~1 à 18 $ pour une vidéo de 30 s.

### Cited Findings
**n8n**
- Cloud Starter ≈ 20 €/mois (annuel) ou 24 € (mensuel), 2 500 exécutions/mois, 5 exécutions concurrentes ; Pro ≈ 50 € (annuel)/60 € (mensuel), 10 000 exécutions, 20 concurrentes ; Business : présenté soit comme licence auto-hébergée à 667 €/mois (annuel), soit comme ~800 €/mois pour 40 000 exécutions (sources discordantes) ; Community Edition gratuite, exécutions illimitées, seul le serveur est payant — [Jetadmin, n8n pricing 2026 (26/09/2026)](https://www.jetadmin.io/blog/n8n-pricing/) ; [Activepieces, n8n pricing 2026](https://www.activepieces.com/blog/n8n-pricing-2026-plans-free-tier-costs-explained.md) ; [Sliplane, n8n pricing](https://sliplane.io/blog/n8n-pricing)
- Une exécution = un run complet du workflow, quel que soit le nombre d'étapes — [Activepieces](https://www.activepieces.com/blog/n8n-pricing-2026-plans-free-tier-costs-explained.md)
- n8n a gardé ses prix cloud stables et ajouté des crédits « AI builder » — [Collab365](https://spaces.collab365.com/posts/n8n-keeps-cloud-prices-flat-and-adds-more-ai-build-Xuioxz)

**Zapier**
- MCP inclus dans tous les plans, sans frais séparés ; chaque appel d'outil réussi = 2 tâches (échecs gratuits) ; plan Free = 100 tâches/mois (soit 50 appels MCP max) ; Professional 19,99 $/mois (annuel) pour 750 tâches selon une source, 29,99 $/mois selon une autre ; palier 2 000 tâches à 49 $/mois (annuel) — [Latenode, Zapier MCP pricing](https://latenode.com/blog/zapier-mcp-pricing) ; [Tinycommand, Zapier pricing explained](https://tinycommand.com/blogs/zapier-pricing-explained)

**Make**
- Modèle à crédits : chaque déclencheur/filtre/action = 1 crédit ; une boucle sur 10 éléments multiplie d'autant. Free = 1 000 crédits/mois ; Core 9 $, Pro 16 $, Teams 29 $ (annuel) ou 10,59 / 18,82 / 34,12 $ (mensuel) selon Latenode (relevé 14/09/2026) ; un autre article Make cite Core 12 $, Pro 21 $, Teams 38 $ — [Latenode, Make pricing](https://latenode.com/blog/make-com-pricing) ; [Coworker, Make pricing](https://coworker.ai/blog/make-com-pricing)
- AI Agents : 1 crédit par opération + crédits de tokens via le fournisseur IA de Make, ou 1 crédit/opération avec sa propre clé OpenAI/Anthropic (plans payants). Table de taux d'oct. 2026 : Claude Sonnet 5 = 45 tokens d'entrée par crédit, GPT-5 nano = 18 080 — [Latenode, Make pricing](https://latenode.com/blog/make-com-pricing)

**API Claude (prix publics, sources tierces)**
- Opus 4.6/4.7 : 5 $ entrée / 25 $ sortie par million de tokens ; Sonnet 4.6 : 3 $ / 15 $ ; Haiku 4.5 : 1 $ / 5 $ ; API Batch −50 % ; lecture de cache = 0,1× le prix d'entrée, écriture de cache 5 min = 1,25× — [MorphLLM, Claude API pricing](https://www.morphllm.com/anthropic-claude-api-pricing) ; [CloudZero, Claude API pricing](https://www.cloudzero.com/blog/claude-api-pricing/) ; [Metacto](https://metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration)
- Tâches Claude Code cloud : consomment le quota de l'abonnement (Pro/Max/Team/Enterprise) ; au-delà, dépassement facturé uniquement si les crédits d'usage sont activés — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md)

**API de génération vidéo (sources tierces, mi/fin 2026)**
- Google Veo : 1080p ≈ 0,40 $/s, 4K ≈ 0,60 $/s ; Veo 3.1 Lite ≈ 0,03–0,08 $/s ; Veo 3.1 Fast ≈ 0,08 $/s (720p sans audio) — [Coverr, AI video API pricing 2026](https://coverr.co/blog/ai-video-generation-api-pricing-2026) ; [Modelslab, Veo 3.1 vs Kling 3 vs Sora 2](https://modelslab.com/blog/api/veo-3-1-vs-kling-3-sora-2-ai-video-api-cost-2026)
- Kling 3.0 : 0,08 $/s (720p sans audio), 0,13 $/s (avec audio), 0,168 $/s (1080p) — [Modelslab](https://modelslab.com/blog/api/veo-3-1-vs-kling-3-sora-2-ai-video-api-cost-2026)
- Runway : crédits à 0,01 $ ; Gen-4 Turbo ≈ 0,05 $/s, Gen-4.5 ≈ 0,12 $/s ; revend aussi Veo, Kling, Seedance — [CometAPI, AI video API pricing](https://www.cometapi.com/ai-video-api-pricing/)
- OpenAI Sora : une source affirme que l'API vidéo Sora a été retirée le 24/09/2026 ; d'autres la listent à 0,10 $/s mais « dépréciée » — [Atlas Cloud, cheapest video API 2026](https://www.atlascloud.ai/blog/cheapest-ai-video-generation-api-2026) ; [CometAPI](https://www.cometapi.com/ai-video-api-pricing/)

### Inferences
- Exemple de budget « contenu » (estimation à partir des chiffres ci-dessus) : 30 posts texte/mois + 8 vidéos courtes de 20 s en Kling 720p avec audio ≈ 8 × 20 × 0,13 ≈ 21 $ de vidéo ; texte via Sonnet ≈ quelques dollars ; n8n auto-hébergé ≈ 5–20 € de VPS ; total ≈ 30–60 €/mois. En Veo 1080p, la même vidéo coûterait ≈ 64 $.
- Le coût caché principal de Make et Zapier est la multiplication (étapes × éléments × fréquence) ; n8n facture au run complet, et l'auto-hébergement supprime ce plafond (mais ajoute la maintenance).
- Les prix d'API Claude cités concernent la génération 4.x ; des modèles plus récents (Sonnet 5, Opus 5.5) existent en oct. 2026 et peuvent avoir d'autres tarifs : vérifier la page officielle.

### Gaps
- Tarifs officiels d'oct. 2026 non vérifiés sur n8n.io, zapier.com, make.com (injoignables) ni sur la page de prix Anthropic pour les modèles 5.x.
- Prix de Zapier Agents (produit distinct de Zapier MCP) non trouvés.
- Coût réel de maintenance d'un n8n auto-hébergé (temps humain, sauvegardes, mises à jour) : pas de source chiffrée.

## 4. Limites et risques connus (quotas API, CGU d'auto-publication, licence n8n, changements cassants, RGPD, verrouillage)

### Takeaway
Les quatre risques majeurs : (1) la licence n8n « Sustainable Use » interdit de revendre l'accès à n8n ou de laisser les clients éditer les workflows ; (2) les réseaux sociaux plafonnent et auditent la publication via API (Instagram ~50–100 publications/24 h, TikTok ~15–20/jour et publication privée seulement sans audit) ; (3) les couches agentiques (tâches Claude, Zapier MCP, Make AI Agents, registre MCP) sont en preview/bêta ; (4) les agents tout-en-un auto-hébergés (OpenClaw) présentent un historique de sécurité lourd.

### Cited Findings
**Licence n8n**
- FAQ officielle : un consultant peut construire des workflows pour des clients sur sa propre instance si les clients ne peuvent ni créer ni modifier les workflows ; facturer la création, la mise en place, la maintenance, la formation et le conseil est autorisé ; héberger n8n « as a service » où les clients construisent leurs propres workflows est interdit — [n8n docs, License FAQ](https://docs.n8n.io/n8n-community-license/community-license/license-faq)
- Lecture prudente : vendre l'accès à un portail client ou facturer les workflows eux-mêmes peut sortir de « l'usage interne » ; marque blanche et revente interdites — [Activepieces, n8n license 2026](https://www.activepieces.com/blog/n8n-license-fair-code-community-enterprise-2026) ; [Hora de Codar, licença n8n](https://horadecodar.com.br/licenca-n8n/)
- Une licence « Embed » serait nécessaire pour intégrer n8n dans un produit ; ~50 000 $/an cité sur le forum (non confirmé par n8n) — [Forum n8n, consulting clients](https://community.n8n.io/t/can-i-use-n8n-cloud-to-manage-workflows-for-multiple-consulting-clients/236130?tl=en)

**Publication automatique sur les réseaux**
- Instagram : 100 publications via API sur 24 h glissantes (carrousel = 1 post) d'après la doc Content Publishing ; la référence de l'endpoint `content_publishing_limit` indique 50 conteneurs/24 h (contradiction dans la doc Meta) ; quota partagé entre tous les outils connectés au même compte — [Meta, Content Publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing) ; [Meta, IG User content_publishing_limit](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit.md)
- TikTok : ~20 posts/jour/compte et 5 partages en attente sur 24 h, et les outils non audités ne peuvent publier qu'en privé (Postly) ; ~15 posts/jour/créateur en Direct Post, partagés entre clients API (Postproxy) — non confirmé par la doc officielle TikTok — [Postly FAQ](https://postly.ai/resources/faq/publishing/publishing-23) ; [Postproxy, Social media API rules 2026](https://postproxy.dev/blog/social-media-platform-api-rules-rate-limits-media-specs/)
- Postiz (planificateur open source, AGPL-3.0, auto-hébergeable) couvre X, LinkedIn, Bluesky, Instagram, Facebook, TikTok, YouTube, Pinterest, Threads, Reddit, Mastodon, etc. et dispose d'un nœud communautaire n8n (`n8n-nodes-postiz`) — [Postiz blog, n8n](https://postiz.com/blog/use-postiz-with-n-8-n) ; [GitHub gitroomhq/postiz-n8n](https://github.com/gitroomhq/postiz-n8n) ; [NCA glossaire Postiz](https://nevercodealone.de/de/glossare/nca-glossar-open-source-projekte/postiz-open-source-social-media-scheduler-2026)

**Changements cassants / statut preview**
- Tâches Claude cloud : « research preview, behavior, limits, and the API surface may change » ; `/fire` sous en-tête bêta daté — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md)
- Registre MCP encore en preview, API figée v0.1 — [Towards AI](https://pub.towardsai.net/mcp-registries-in-mid-2026-one-upstream-won-2ce541b92036)
- Make AI Agents en bêta ouverte, tarification susceptible de changer ; Zapier MCP étiqueté bêta — [Latenode, Make](https://latenode.com/blog/make-com-pricing) ; [Latenode, Zapier MCP](https://latenode.com/blog/zapier-mcp-pricing)
- API Sora possiblement retirée (24/09/2026) : exemple de dépendance vidéo qui disparaît — [Atlas Cloud](https://www.atlascloud.ai/blog/cheapest-ai-video-generation-api-2026)

**Données / RGPD / identité**
- Tâches Claude cloud : appartiennent au compte individuel ; tout ce qu'elles font via GitHub ou les connecteurs apparaît sous l'identité de l'utilisateur ; les variables d'environnement sont visibles par quiconque utilise l'environnement (préférer les « network secrets ») ; option d'environnement auto-hébergé pour les organisations — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md)
- n8n Community auto-hébergé = données sur son propre serveur (choix de la région, ex. UE) — [Sliplane, n8n pricing](https://sliplane.io/blog/n8n-pricing)
- Postiz : aucune restriction de fonctionnalités entre version hébergée et auto-hébergée — [G2, Postiz](https://www.g2.com/sellers/postiz)

**Sécurité des agents tout-en-un**
- OpenClaw : CVE nombreuses, paquets malveillants dans la marketplace de skills, avis CNCERT — [Pinggy](https://pinggy.io/blog/best_openclaw_alternatives/) ; [Fast.io](https://fast.io/resources/openclaw-review-2026/)

### Inferences
- Pour vendre un « pack » : vendre le résultat ou des modèles (JSON n8n, plugins Claude) que le client installe sur sa propre instance/son propre compte est la voie la moins risquée côté licence n8n ; héberger un n8n multi-clients avec accès éditeur est exclu sans licence commerciale.
- Le passage par un planificateur intermédiaire (Postiz, Buffer, Blotato…) réduit le risque de CGU (applications déjà auditées par les réseaux) mais crée une dépendance supplémentaire.
- Verrouillage (lock-in) : workflows n8n = JSON exportable (portabilité moyenne : propre à n8n) ; Make/Zapier = scénarios propriétaires difficiles à migrer ; skills Claude = Markdown + scripts (format Agent Skills publié en spécification ouverte dans anthropics/skills), donc assez portables ; MCP = standard ouvert multi-clients.
- RGPD : le contrôle maximal est n8n + Postiz auto-hébergés en UE avec un LLM appelé via API (encore un transfert vers le fournisseur LLM à couvrir par DPA) ; les solutions SaaS (Zapier, Make, tâches Claude cloud) exigent de vérifier région d'hébergement et DPA.

### Gaps
- CGU LinkedIn et X pour la publication automatisée (limites, interdictions) : non trouvées dans cette recherche.
- Doc officielle TikTok Content Posting API (audit, plafonds) non consultée directement.
- Régions d'hébergement des données et DPA de n8n Cloud, Make, Zapier et Anthropic : non vérifiés ici.
- Historique des changements cassants de n8n (ex. passage de version majeure) : non documenté dans cette recherche.

## 5. Grille comparative et checklist d'évaluation d'un système/pack d'automatisation IA

### Takeaway
Aucun socle ne gagne sur tous les critères : n8n auto-hébergé = meilleur contrôle et coût à l'échelle, mais maintenance ; Zapier/Make = facilité et connecteurs, mais coût qui grimpe et lock-in ; Claude Code/Cowork = meilleur pour le travail « intelligent » et les packs agnostiques de niche (skills/plugins), mais planification encore en preview ; frameworks (CrewAI, LangGraph, Agno, OpenAI Agents SDK) = réservés aux développeurs ; Dify/Flowise = intermédiaires visuels auto-hébergeables. La checklist ci-dessous permet de noter n'importe quel pack.

### Cited Findings
Synthèse appuyée sur les sources des sections 1 à 4 (aucune nouvelle source). Points saillants :
- Planification sans surveillance : Claude cloud ≥ 1 h d'intervalle, preview, 100 runs/h — [Claude Code docs, Routines](https://code.claude.com/docs/en/routines.md) ; n8n cron + Retry On Fail + Error Trigger — [RapidDevelopers](https://www.rapidevelopers.com/md/n8n-tutorial/how-to-retry-failed-workflows-in-n8n)
- Écosystème : n8n ~209 k étoiles / 9 000+ modèles — [GitHub n8n](https://github.com/n8n-io/n8n) ; Zapier 9 000+ apps — [PricingSaaS](https://pricingsaas.com/companies/zapier/diffs/2026W21) ; skills Claude ~184 k étoiles — [GitHub anthropics/skills](https://github.com/anthropics/skills)

### Inferences
**Grille synthétique (appréciation qualitative déduite des sources ; 1 = faible, 5 = fort)**

| Critère | n8n auto-hébergé | n8n Cloud | Make | Zapier | Claude Code/Cowork (+ tâches cloud) | Dify / Flowise | Frameworks code (CrewAI, LangGraph, Agno, OpenAI Agents SDK) | Agents tout-en-un (OpenClaw) |
|---|---|---|---|---|---|---|---|---|
| Fiabilité sans surveillance | 4 (si bien maintenu) | 4 | 4 | 4 | 3 (preview, contrôle par sortie) | 3 | 3 (selon votre infra) | 2 |
| Coût à l'échelle | 5 | 3 | 3 | 2 | 3 (quota d'abonnement) | 4 | 4 | 4 |
| Facilité non-développeur | 3 | 4 | 4 | 5 | 4 (langage naturel) | 3 | 1 | 2 |
| Maintenance | 2 | 4 | 5 | 5 | 4 | 2 | 1 | 1 |
| Taille d'écosystème | 5 | 5 | 4 | 5 (connecteurs) | 4 (skills/plugins/MCP) | 4 | 3–4 | 4 (mais risqué) |
| Planification | 5 (cron libre) | 5 | 5 | 5 | 3 (≥ 1 h, preview) | 3 | dépend de l'infra | 3 |
| Publication réseaux | 4 (nœuds natifs + Postiz) | 4 | 4 | 4 | 3 (via MCP/API) | 2 | 2 | 3 |
| Contrôle données / RGPD | 5 | 3 | 3 | 2 | 3 (option auto-hébergée orga) | 5 | 5 | 4 |
| Faible lock-in | 4 | 3 | 2 | 2 | 4 (skills Markdown, MCP ouvert) | 4 | 5 | 4 |

**Checklist d'évaluation d'un pack/système (critère → comment le vérifier)**
1. *Fonctionne sans surveillance* → exige un déclencheur planifié natif (cron) ; vérifier l'intervalle minimal, l'expiration (ex. 7 j pour `/loop`), le besoin d'une machine allumée ; lancer 7 jours d'affilée et compter les runs réussis.
2. *Gestion d'erreurs* → présence de reprises automatiques (Retry On Fail, backoff), d'un workflow d'erreur, d'une alerte (email/Slack) ; tester en coupant volontairement une clé API.
3. *Preuve de résultat* → chaque run écrit une trace vérifiable (ligne en base, journal, lien publié) ; ne pas se fier au seul statut « Succeeded ».
4. *Coût total mensuel* → additionner hébergement + plan + tokens LLM + crédits vidéo/image ; simuler le volume réel (exécutions × étapes × éléments) ; vérifier existence de cache/batch et plafonds de dépense.
5. *Facilité non-dev* → temps d'installation chronométré par un non-développeur ; nombre de clés API à créer ; documentation en français ; configuration sans code.
6. *Maintenance* → fréquence des mises à jour du socle, changelog des changements cassants, statut GA vs bêta/preview de chaque brique ; qui maintient le pack (date du dernier commit, issues ouvertes).
7. *Écosystème* → étoiles/forks GitHub et date du dernier commit ; nombre de modèles et connecteurs ; taille de la communauté (forum, Discord) ; provenance des serveurs MCP/skills (officiels vs inconnus).
8. *Publication réseaux* → utilise-t-il les API officielles ou un planificateur audité (Postiz, Buffer…) ? respecte-t-il les plafonds (Instagram 50–100/24 h, TikTok ~15–20/jour) ? publication TikTok publique possible (app auditée) ?
9. *CGU et licences* → licence du socle (Sustainable Use n8n, AGPL Postiz, MIT, Apache, source-available) compatible avec la revente ; pas d'accès client à l'éditeur n8n sans licence ; respect des CGU des réseaux (pas d'automatisation d'interactions interdites).
10. *Données / RGPD* → lieu d'hébergement (UE ?), DPA disponibles chez chaque fournisseur (LLM, orchestrateur, vidéo), secrets stockés hors du code, suppression des données possible.
11. *Lock-in / portabilité* → workflows exportables (JSON, Markdown), formats ouverts (MCP, Agent Skills), possibilité de changer de modèle LLM sans tout réécrire.
12. *Sécurité* → permissions minimales des connecteurs, validation humaine avant actions irréversibles (publication, envoi d'email, paiement), aucune extension de marketplace non vérifiée, mises à jour de sécurité suivies (CVE).
13. *Agnosticité de niche* → le contexte métier (ton, offre, cible) est-il paramétrable dans un fichier unique sans toucher aux workflows ? tester en changeant de niche en moins d'une heure.

### Gaps
- La grille est une synthèse qualitative de l'auteur des notes à partir des sources ; aucune source tierce ne fournit une notation standardisée de tous ces socles sur ces critères.
- Pas de retours d'expérience Reddit consultés dans cette recherche (limite du nombre d'appels) sur la fiabilité réelle à long terme.
