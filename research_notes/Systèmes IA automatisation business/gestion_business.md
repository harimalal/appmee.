# Systèmes IA prêts à l'emploi pour automatiser la gestion d'une petite entreprise (état au 25 octobre 2026)

> Méthode : chiffres GitHub (étoiles, forks, statut archivé, date `updated_at`) relevés le **25/10/2026** via l'API de recherche GitHub. Attention, `updated_at` change aussi quand quelqu'un met une étoile : ce n'est pas la date du dernier commit. Un dépôt marqué « archivé » est en lecture seule. Les pages n8n.io et metabase.com n'ont pas pu être chargées (erreur DNS dans l'environnement). Les compteurs d'usage des templates n8n et la doc Metabot ne sont donc pas vérifiés.

## 1. Projets GitHub open source : « AI business OS », assistant exécutif, agent personnel

### Takeaway
Les agents personnels généralistes (OpenClaw, Hermes Agent) ont une traction énorme mais posent un vrai risque de sécurité et ne savent pas gérer une entreprise sans configuration. Les briques métier matures (CRM Twenty, ERP Odoo/ERPNext/Dolibarr, Inbox Zero pour l'email) sont bien plus sûres, et un « OS de chef de cabinet » prêt à l'emploi reste à l'état de kit de démarrage (clawchief, Dex, claude-chief-of-staff : moins de 1,2k étoiles, peu de commits).

### Cited Findings
**Agents personnels / assistants généralistes**
- **OpenClaw** (ex-Clawdbot) : 393 019 étoiles, 82 605 forks, 7 848 issues ouvertes, créé le 24/11/2025, actif le 25/10/2026, licence MIT. Assistant qui « fait vraiment les choses », piloté depuis WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, iMessage, Teams et « 20+ autres ». Il tourne comme un daemon (`openclaw onboard --install-daemon`, Node 24.16+) et s'étend par des skills et plugins (ClawHub). Le README demande de traiter les messages entrants comme non fiables. Par défaut, les outils tournent sur la machine hôte sans sandbox. — [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)
- **Sécurité OpenClaw/ClawHub** : Koi Security a audité 2 857 skills ClawHub et en a jugé 341 malveillantes (environ 12 %), la plupart installant le voleur macOS AMOS via de fausses étapes « prérequis ». — [incidentdatabase.ai](https://incidentdatabase.ai/reports/6951/) ; [bitdoze](https://www.bitdoze.com/openclaw-security-guide/) (le guide cite aussi la CVE-2026-25253)
  - Unit42 cite une estimation Bitdefender d'environ 17 % de skills malveillantes au début. Malgré le filtrage VirusTotal/ClawScan, Unit42 a encore trouvé 5 skills malveillantes non bloquées entre février et mai 2026. — [Unit42 Palo Alto](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)
  - Deux skills « AI assistant » sur le thème TradingView, piégées de la même façon, ont été publiées le 17/05/2026. — [Bagisto](https://bagisto.com/en/openclaw-marketplace-found-hosting-malicious-ai-skills-despite-security-scanning/amp/)
  - La campagne a été baptisée « ClawHavoc ». — [Antiy](https://www.antiy.net/p/clawhavoc-analysis-of-large-scale-poisoning-campaign-targeting-the-openclaw-skill-market-for-ai-agents/)
- **clawchief** (snarktank) : « Turn your OpenClaw into a Chief of Staff ». 1 109 étoiles, 117 forks, mais seulement 5 commits. Il fournit les skills `executive-assistant`, `business-development`, `daily-task-manager` et `daily-task-prep`, un « heartbeat orchestrator », un modèle de cron (`cron/jobs.template.json`) et l'intégration Gmail et Agenda via un guide `SETUP-GOG.md`. L'installation se fait manuellement en 7 étapes. Le README le présente comme un modèle à adapter. — [GitHub snarktank/clawchief](https://github.com/snarktank/clawchief)
- **Hermes Agent** (Nous Research) : 256 977 étoiles, 56 276 forks, « The agent that grows with you », Python, créé en 07/2025. Le compteur affiche 51 002 issues ouvertes, un chiffre anormal qui pose question sur la maintenance (ou signale du spam d'issues). — [GitHub NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **Khoj** : 37 819 étoiles, 2 530 forks, « AI second brain », auto-hébergeable. Il répond à partir du web ou de vos documents, permet de créer des agents personnalisés, de **programmer des automatisations** et de faire de la recherche approfondie, avec n'importe quel LLM local ou en ligne. — [GitHub khoj-ai/khoj](https://github.com/khoj-ai/khoj)
- **Leon** : 17 605 étoiles, 1 476 forks, « open-source personal assistant », orienté voix et hors-ligne. Utilité métier faible. — [GitHub leon-ai/leon](https://github.com/leon-ai/leon)
- **LobeHub** : 83 481 étoiles. Il se positionne maintenant en « Chief Agent Operator », qui organise des agents en opérations 24h/24 et 7j/7 (« hiring, scheduling, and reporting on your entire AI team »). — [GitHub lobehub/lobehub](https://github.com/lobehub/lobehub)
- **Open WebUI** : 156 717 étoiles, interface LLM auto-hébergée avec MCP et RAG. **AnythingLLM** : 67 534 étoiles, « local-first agent ». **mem0** : 67 781 étoiles, couche mémoire pour agents. — [open-webui](https://github.com/open-webui/open-webui) ; [anything-llm](https://github.com/Mintplex-Labs/anything-llm) ; [mem0](https://github.com/mem0ai/mem0)
- **Kits « Chief of Staff » sur Claude Code** : **Dex** (davekilleen) a 508 étoiles. Il se décrit comme « Your AI Chief of Staff — a personal operating system starter kit that adapts to your role. No coding required », avec MCP et Claude Code. **claude-chief-of-staff** (mimurchison) a 456 étoiles (« personal AI operating system built on Claude Code »). **sno-station-skills** a 825 étoiles, 31 skills et un « one-page morning brief », mais il vise le dev (Claude Code et Codex). Il a été créé le 01/10/2026 avec 595 forks pour 825 étoiles, un ratio inhabituel. — [Dex](https://github.com/davekilleen/Dex) ; [claude-chief-of-staff](https://github.com/mimurchison/claude-chief-of-staff) ; [sno-station-skills](https://github.com/sno-ai/sno-station-skills)

**Plateformes pour construire ses agents et apps IA**
- **Dify** : 159 499 étoiles, 25 208 forks, workflows agentiques et RAG, cloud, VPC ou auto-hébergé. — [langgenius/dify](https://github.com/langgenius/dify)
- **Flowise** : 55 527 étoiles, 25 082 forks. **Le dépôt est marqué `archived: true` au 25/10/2026.** C'est à vérifier, mais il ne faut pas bâtir dessus sans confirmation. — [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise)
- **Sim** (simstudioai) : 29 917 étoiles, il revendique « 100,000+ builders ». — [simstudioai/sim](https://github.com/simstudioai/sim)

**Briques métier (CRM / ERP / facturation)**
- **Twenty CRM** : 59 719 étoiles, 9 740 forks, seulement 127 issues ouvertes. Se décrit comme « The open alternative to Salesforce, designed for AI ». — [twentyhq/twenty](https://github.com/twentyhq/twenty)
- **Odoo** : 55 311 étoiles, 34 102 forks, branche par défaut 20.0. — [odoo/odoo](https://github.com/odoo/odoo)
  - Pour l'IA dans Odoo 19, je n'ai trouvé que des modules tiers. « Pronexo AI Agent » coûte 60 $ (chat sur les données Odoo + OCR). « AI Vendor Bill OCR » coûte 129 € en paiement unique, avec votre propre clé OpenAI. L'OCR natif d'Odoo (IAP) serait facturé 0,10 €/facture, selon un vendeur tiers. — [apps.odoo.com pronexo](https://apps.odoo.com/apps/modules/19.0/pronexo_ai_agent) ; [ai_vendor_bill_ocr](https://apps.odoo.com/apps/modules/19.0/ai_vendor_bill_ocr)
- **ERPNext** : 40 578 étoiles. **Frappe CRM** : 3 854 étoiles. **Frappe HRMS** : 8 961 étoiles. **Frappe Books** est **archivé**. — [erpnext](https://github.com/frappe/erpnext) ; [frappe/crm](https://github.com/frappe/crm) ; [frappe/hrms](https://github.com/frappe/hrms) ; [frappe/books](https://github.com/frappe/books)
- **Dolibarr** (ERP/CRM PHP, éditeur d'origine française) : 7 777 étoiles, 3 589 forks. **Krayin CRM** : 24 058 étoiles. **EspoCRM** : 3 520 étoiles. — [Dolibarr](https://github.com/Dolibarr/dolibarr) ; [krayin](https://github.com/krayin/laravel-crm) ; [espocrm](https://github.com/espocrm/espocrm)
- **Invoice Ninja** : 10 319 étoiles, il se dit « source-available » (pas strictement open source) et porte le tag `einvoicing`. **Akaunting** : 10 210 étoiles. **InvoiceShelf** : 1 868 étoiles. — [invoiceninja](https://github.com/invoiceninja/invoiceninja) ; [akaunting](https://github.com/akaunting/akaunting) ; [InvoiceShelf](https://github.com/InvoiceShelf/InvoiceShelf)
- **Paperless-ngx** (GED + OCR, tag `llm`) : 47 079 étoiles, utile pour classer les justificatifs. — [paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)

**Email**
- **Inbox Zero** : 12 806 étoiles, 1 632 forks, 11 698 commits. Assistant email IA pour Gmail et Outlook. Il trie la boîte, prérédige les réponses dans votre ton, applique des règles IA écrites en langage naturel, suit les réponses attendues (« Reply Zero »), désabonne et archive en masse, bloque le cold email, fournit des statistiques, prépare des briefs de réunion depuis l'email et l'agenda, classe les pièces jointes dans Drive/OneDrive, et s'intègre à Slack et Telegram. Un dossier `plugins/inbox-zero-mcp` existe. Il s'auto-héberge avec `npx @inbox-zero/cli setup` (Docker + Node 24). Il se présente comme une « open source alternative to Fyxer ». — [elie222/inbox-zero](https://github.com/elie222/inbox-zero)

**Agenda / prise de RDV**
- **Cal.com n'est plus open source** : le 15/04/2026, le code de production est passé en dépôt privé. Le code public continue sous licence MIT avec le nom **Cal.diy**. Raison invoquée : le risque de sécurité lié à l'IA. — [The New Stack](https://thenewstack.io/cal.com-codebase-security-ai/) ; [Noqta](https://www.noqta.tn/en/blog/cal-com-closed-source-ai-open-source-reckoning-2026) ; le dépôt `calcom/docker` est archivé ([GitHub](https://github.com/calcom/docker)). Je n'ai pas lu l'annonce officielle de Cal.com.
- Alternatives : **calrs** (« Like Cal.com, but written in Rust »), 327 étoiles. **someday** (prise de RDV sur Google Apps Script), 1 063 étoiles. — [calrs](https://github.com/olivierlambert/calrs) ; [someday](https://github.com/rbbydotdev/someday)

### Inferences
- Pour une TPE, l'option la plus solide aujourd'hui est un assemblage : un CRM ou ERP mature (Twenty, Odoo ou Dolibarr) + Inbox Zero + un orchestrateur (n8n) ou Claude Cowork pour la couche IA. Je n'ai trouvé aucun « AI business OS » open source à la fois mature et généraliste.
- OpenClaw a une traction gigantesque, mais avec des droits complets sur la machine et un marché de skills contaminé, il est déconseillé sur un poste qui détient les accès bancaires ou comptables. Si on l'utilise : sandbox, pas de skills ClawHub non auditées, machine dédiée.
- Les kits « Chief of Staff » (clawchief, Dex) sont de bons modèles à copier, mais ils n'ont pas de preuve d'usage au-delà des étoiles. C'est **une offre faible ou non prouvée**.

### Gaps
- Je n'ai pas pu obtenir les dates de dernier commit et de dernière release (API GitHub directe bloquée), ni confirmer officiellement l'archivage de Flowise.
- Je n'ai trouvé aucune étude de cas vérifiée de PME utilisant OpenClaw ou Khoj pour la gestion.
- Les fonctions IA natives d'Odoo 19/20 (agents, OCR) n'ont pas été confirmées sur odoo.com.

## 2. Templates n8n / Make : assistant IA, tri d'inbox, facturation, synchro CRM, rapports

### Takeaway
n8n est l'orchestrateur dominant (208k étoiles) et dispose de grandes bibliothèques de templates communautaires. Je n'ai pas pu vérifier les compteurs d'usage par template sur n8n.io.

### Cited Findings
- **n8n** : 208 556 étoiles, 61 246 forks, « fair-code » (pas OSI), plus de 400 intégrations, client et serveur MCP natifs. — [n8n-io/n8n](https://github.com/n8n-io/n8n)
- **Activepieces** (alternative MIT à n8n) : 25 215 étoiles, il revendique environ 400 serveurs MCP. **Windmill** : 18 262 étoiles. — [activepieces](https://github.com/activepieces/activepieces) ; [windmill](https://github.com/windmill-labs/windmill)
- **Zie619/n8n-workflows** : 57 080 étoiles, 7 694 forks. C'est un agrégat (« all of the workflows of n8n i could find ») : qualité variable, pas de curation. — [GitHub](https://github.com/Zie619/n8n-workflows)
- **awesome-n8n-templates** : 26 098 étoiles. Plus de 280 templates gratuits en 18 catégories (Gmail, Telegram, Slack, WhatsApp, Drive, Notion, OpenAI, agents IA, RAG, traitement de documents). — [enescingoz/awesome-n8n-templates](https://github.com/enescingoz/awesome-n8n-templates)
- Exemple de template officiel : le n°9157, « AI-Powered Email Triage and Auto-Response System with OpenAI Agents and Gmail ». Il classe les emails (Sales, Support, Internal, Finance, Promotions) et les route vers des agents dédiés. — [n8n.io/workflows/9157](https://n8n.io/workflows/9157-ai-powered-email-triage-and-auto-response-system-with-openai-agents-and-gmail/)
- Un template « Invoice Processor & Validator with OCR, AI & Google Sheets » est cité en mai 2026. — [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2026/05/everyday-ai-automation-using-n8n/)
- Des templates payants circulent sur Gumroad (ex. « Agentic Email Triage… Gmail OpenAI Pinecone »), sans preuve de traction. — [Gumroad](https://tesseractcreator.gumroad.com/l/agentic-email-triage-automated-inbox-manager-n8n-template-gmail-openai-pinecone)

### Inferences
- Les templates n8n sont des points de départ et non des systèmes clés en main. Il faut les adapter (identifiants, prompts, règles françaises). Les packs payants sur Gumroad sont à considérer comme **non prouvés**.

### Gaps
- Pas de nombre de vues ou d'utilisations par template (n8n.io inaccessible depuis l'environnement), pas de classement « most popular ».
- Je n'ai pas fait de recherche sur les templates Make.

## 3. Serveurs MCP et plugins/skills Claude Code & Cowork pour la gestion d'entreprise

### Takeaway
L'écosystème le plus « prêt à l'emploi » pour une TPE en octobre 2026 est le plugin officiel **small-business** d'Anthropic : 44 skills couvrant finance, ventes, marketing, ops et briefs, avec validation obligatoire avant chaque action. Côté France, Qonto a un connecteur MCP officiel et Pennylane en aurait un (en lecture seule).

### Cited Findings
- **anthropics/knowledge-work-plugins** : 32 888 étoiles, 3 628 forks, créé le 23/01/2026. Il contient les plugins productivity, sales, customer-support, product-management, marketing, legal, finance, data, enterprise-search, bio-research et cowork-plugin-management, plus les dossiers operations, small-business, human-resources, engineering, design et partner-built. Installation : `claude plugin marketplace add anthropics/knowledge-work-plugins`. — [GitHub](https://github.com/anthropics/knowledge-work-plugins)
  - Le plugin **productivity** gère les tâches, l'agenda et la routine quotidienne (connecteurs Slack, Notion, Asana, Linear, Jira, Monday, ClickUp, M365). Le plugin **finance** prépare les écritures, fait les rapprochements et les états financiers (connecteurs Snowflake, Databricks, BigQuery). Le plugin **sales** couvre la recherche de prospects et la revue de pipeline (connecteurs HubSpot, Close, Clay). — [README](https://github.com/anthropics/knowledge-work-plugins)
- **Plugin small-business v1.35.1** : 44 skills et un routeur `smb-router` qui comprend les demandes en langage courant. La commande « get me started » lance un onboarding de 15 minutes : connexion de deux outils, une tâche réelle, captation de la charte graphique. — [GitHub small-business](https://github.com/anthropics/knowledge-work-plugins/tree/main/small-business)
  - Skills par domaine :
    - Finance : `invoice-chase`, `cash-flow-snapshot`, `close-month`, `month-end-prep`, `pay-the-bills`, `payroll-prep`, `report-pack`, `tax-prep`
    - Ventes : `crm-autopilot`, `lead-triage`, `speed-to-lead`, `reactivate`
    - Opérations : `inbox-manager`, `inventory-planner`, `hiring-screener`
    - Briefs : `business-pulse`, `monday-brief`
  - Sécurité : rien n'est envoyé, publié, payé ou écrit sans approbation explicite. La paie est seulement préparée, pas lancée. La règle « No invented numbers » s'applique. Tout fonctionne sans connecteur, à partir de CSV ou de PDF.
  - Avertissement : le plugin ne fournit pas de conseil fiscal ou juridique. Il est orienté États-Unis (1099, payroll), donc pas de TVA ni de liasse fiscale française.
- **Plugin operations** : commandes `/status-report` (rapport de direction avec KPI, risques, actions), `/vendor-review`, `/process-doc` (SOP + RACI), `/capacity-plan`, `/runbook`. — [GitHub operations](https://github.com/anthropics/knowledge-work-plugins/tree/main/operations)
- **anthropics/skills** : 183 684 étoiles. **anthropics/claude-plugins-official** : 44 486 étoiles. **ComposioHQ/awesome-claude-skills** : 77 906 étoiles (liste communautaire). **Composio** : 30 744 étoiles, plus de 1 000 « toolkits » avec authentification gérée. — [skills](https://github.com/anthropics/skills) ; [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) ; [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) ; [composio](https://github.com/ComposioHQ/composio)
- Le répertoire de connecteurs Claude liste **plus de 950 serveurs MCP**. La spec MCP 2026-07-28 rend le cœur du protocole sans état. — [claude.com blog](https://claude.com/de/blog/bringing-mcp-2026-07-28-to-claude)
- **modelcontextprotocol/servers** (serveurs de référence) : 91 551 étoiles. — [GitHub](https://github.com/modelcontextprotocol/servers)
- **Google Workspace MCP** (taylorwilsdon) : 3 410 étoiles, 1 071 forks. Couvre Gmail, Calendar, Docs, Sheets, Slides, Chat, Forms, Tasks et Drive. — [GitHub](https://github.com/taylorwilsdon/google_workspace_mcp)
- **GongRzhe/Gmail-MCP-Server** (1 169 étoiles) est **archivé**. Il ne faut plus l'utiliser. **nspady/google-calendar-mcp** : 1 206 étoiles, 5 issues ouvertes. — [Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server) ; [google-calendar-mcp](https://github.com/nspady/google-calendar-mcp)
- **Notion MCP officiel** : 4 679 étoiles. **Stripe** (`stripe/ai`, ex-agent-toolkit) : 1 968 étoiles, MCP + SDK. — [notion-mcp-server](https://github.com/makenotion/notion-mcp-server) ; [stripe/ai](https://github.com/stripe/ai)
- **Qonto** : connecteur MCP officiel (`https://mcp.qonto.com/mcp`, OAuth), compatible Claude Desktop et claude.ai. Le connecteur personnalisé exige une offre Pro, Max, Team ou Enterprise. — [docs.qonto.com](https://docs.qonto.com/mcp/install/claude-desktop)
- **Pennylane** : un blog français affirme qu'un serveur MCP Pennylane existe depuis le 03/08/2026, avec environ 30 outils en lecture seule. Je n'ai pas pu le confirmer à la source. Des serveurs MCP Pennylane tiers existent aussi, gérés par Truto (contenu marketing). — [Tensoria](https://tensoria.fr/blog/pennylane-mcp-claude) ; [Truto](https://truto.one/blog/connect-pennylane-to-claude-manage-sales-billing-and-customers/)

### Inferences
- Pour une TPE française sous Claude Cowork, l'assemblage le plus direct serait : small-business + operations + productivity, avec les connecteurs Gmail/Calendar, Notion, Qonto (banque) et Pennylane (compta, en lecture). Il faut ensuite adapter les skills US (payroll, 1099) aux règles françaises. C'est une piste à construire, pas une solution déjà prouvée en France.
- Le skill `monday-brief` (plugin small-business) et le skill intégré « morning » couvrent le besoin de « brief du matin » sans dépendance tierce.

### Gaps
- Je n'ai trouvé aucune donnée d'adoption (installations) des plugins Anthropic, ni d'étude de cas TPE. Le contenu de `.mcp.json` / `CONNECTORS.md` du plugin small-business n'a pas été vu.
- La disponibilité officielle du MCP Pennylane reste à vérifier. Je n'ai rien trouvé sur un MCP pour Indy, Tiime, Sellsy ou Axonaut.

## 4. Gestion du temps par IA (Motion, Reclaim, Sunsama et alternatives open source)

### Takeaway
Les références SaaS restent Motion (planification automatique complète, la plus chère), Reclaim (défense de l'agenda, à partir d'environ 8–10 $/mois) et Sunsama (planification manuelle guidée, environ 20 $/mois). Côté open source, Super Productivity et Huly sont solides, mais aucun ne fait de vraie planification automatique par IA.

### Cited Findings
- **Motion** : environ 19 $ (Pro AI) et 29 $ par siège (Business AI) en annuel, selon une source. Une autre parle de 19 ou 34 $. Pas de plan gratuit, essai de 14 jours. En 2026, ajout de la transcription de réunions et des « AI Employees ». Des testeurs jugent la planification automatique « agressive ». — [dupple](https://dupple.com/compare/motion-vs-sunsama) ; [codegen](https://codegen.com/alternatives/motion/) ; [wikidocs solobizstack](https://wikidocs.net/blog/@solobizstack/25779/)
- **Reclaim** : à partir d'environ 8 $/mois selon un comparatif, 10 $/mois avec un plan gratuit selon Reclaim lui-même. Centré sur l'agenda (habitudes, temps de concentration). — [dupple](https://dupple.com/alternatives/reclaimai) ; [reclaim.ai](https://reclaim.ai/blog/motion-alternatives)
- **Sunsama** : 20 $/mois en annuel (25 $ selon une autre source), pas d'IA de planification. — [super-productivity blog](https://super-productivity.com/blog/best-sunsama-alternatives-2026/)
- **Open source** :
  - **Super Productivity** : 23 138 étoiles, timeboxing, suivi du temps, local-first.
  - **Huly** : 27 985 étoiles, « alternative to Linear, Jira, Slack, Notion, Motion ».
  - **Plane** : 61 415 étoiles, gestion de projet.
  - **AppFlowy** : 77 756 étoiles, alternative à Notion avec IA.
  - **Kimai** : 5 098 étoiles, feuilles de temps et facturation.
  — [super-productivity](https://github.com/super-productivity/super-productivity) ; [hcengineering/platform](https://github.com/hcengineering/platform) ; [makeplane/plane](https://github.com/makeplane/plane) ; [AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) ; [kimai](https://github.com/kimai/kimai)
- Vikunja a publié un billet « Vikunja stays open » en réaction à la fermeture de Cal.com. — [vikunja.io](https://vikunja.io/changelog/vikunja-stays-open)

### Inferences
- L'alternative open source la plus proche de Motion serait Huly ou Super Productivity, avec un agent (Claude + MCP agenda) qui place les blocs de temps. Aucun outil open source ne fait ça tout seul.

### Gaps
- Les prix SaaS sont contradictoires entre sources, à vérifier sur les pages tarifs. Je n'ai pas trouvé d'avis G2 chiffrés.

## 5. Automatisation des rapports (rapports KPI hebdo depuis Stripe, GA, CRM ; Metabase/Evidence + LLM)

### Takeaway
Les briques BI open source sont mûres (Metabase, Superset, Redash, Evidence, Lightdash « Agentic BI »). Le « rapport hebdo auto + commentaire LLM » reste à monter soi-même : script Stripe + Claude, n8n, ou les skills `/status-report` et `report-pack` d'Anthropic.

### Cited Findings
- **Metabase** : 49 839 étoiles. **Apache Superset** : 75 301. **Redash** : 28 852. **Evidence** (BI-as-code SQL + markdown) : 7 058. **Lightdash** (se présente comme « Agentic BI ») : 6 198. — [metabase](https://github.com/metabase/metabase) ; [superset](https://github.com/apache/superset) ; [redash](https://github.com/getredash/redash) ; [evidence](https://github.com/evidence-dev/evidence) ; [lightdash](https://github.com/lightdash/lightdash)
- Tutoriel : un script Node extrait de Stripe le chiffre d'affaires, les nouveaux abonnements, les résiliations et le MRR net, puis Claude rédige la synthèse du lundi. Attention, l'API Stripe pagine et il faut une boucle avec curseur. — [WitsCode](https://witscode.com/blogs/weekly-reporting-automation)
- Des plateformes hébergées (Toolhouse, Arahi, Improvado) proposent des agents qui interrogent Metabase le lundi et envoient les insights par email. C'est du marketing, avec des compteurs fictifs sur certaines pages : **non prouvé**. — [Toolhouse](https://toolhouse.ai/en/platform/integrations/automate-metabase-with-ai-agents) ; [Improvado](https://improvado.io/mcp/metabase)
- Les skills Anthropic `business-pulse`, `monday-brief`, `report-pack`, `growth-pulse` (small-business) et `/status-report` (operations) produisent des rapports à partir des connecteurs ou de CSV. — [small-business](https://github.com/anthropics/knowledge-work-plugins/tree/main/small-business) ; [operations](https://github.com/anthropics/knowledge-work-plugins/tree/main/operations)

### Inferences
- La pile la plus économique : Stripe MCP ou API → n8n (cron hebdo) → Claude → email/Slack, ou bien Claude Cowork avec une tâche planifiée qui exécute `monday-brief`. Metabase ou Evidence ne servent que si un tableau de bord persistant est voulu.

### Gaps
- Les fonctions et l'offre de Metabot (IA de Metabase) n'ont pas été vérifiées (site inaccessible).

## 6. Contexte France : facturation électronique 2026 (contrainte forte sur le choix d'outil de facturation)

### Takeaway
Depuis le 1er septembre 2026, toute entreprise doit pouvoir **recevoir** des factures électroniques via une plateforme agréée (PA). L'**émission** devient obligatoire pour les PME, TPE et micro-entreprises au 1er septembre 2027. Un outil de facturation open source n'est donc utilisable que s'il est relié à une PA.

### Cited Findings
- Calendrier : réception obligatoire pour toutes les entreprises au 01/09/2026, émission obligatoire pour les grandes entreprises et ETI dès 2026, et pour les PME, TPE et micro-entreprises au 01/09/2027. Il faut avoir choisi une PA avant le 01/09/2026. La liste des PA a été publiée en janvier 2026. — [Mooncard](https://www.mooncard.co/fr/blog/facturation-electronique-calendrier) ; [WebLex](https://www.weblex.fr/weblex-actualite/facturation-electronique-publication-de-la-liste-des-plateformes-agreees) ; [Sage](https://www.sage.com/fr-fr/blog/calendrier-facture-electronique/) (sources d'éditeurs, à recouper sur impots.gouv.fr)
- **Dolibarr** n'est pas une PA. Il génère du Factur-X en natif, et le module **EInvoicing** (ex-PDPConnectFR, expérimental, Dolibarr 24.0+) le relie à certaines PA. Le module serait gratuit sur DoliStore depuis le 30/07/2026, mais l'abonnement à la PA reste payant. — [wiki Dolibarr](https://wiki.dolibarr.org/index.php/Module_EInvoicing_(Generic,_FR,_...)) ; [comparatif-facture-electronique](https://www.comparatif-facture-electronique.fr/dolibarr-facturation-electronique-avis/) ; [DoliCloud](https://www.dolicloud.com/are-dolicloud-and-dolibarr-ready-for-electronic-invoicing.php)
- Bibliothèques Factur-X open source : **akretion/factur-x** (Python, 313 étoiles), **mustangproject** (Java, 485), **horstoeko/zugferd** (PHP, 440), **e-invoice-eu** (365, génère du EN16931 depuis un tableur). — [akretion/factur-x](https://github.com/akretion/factur-x) ; [mustangproject](https://github.com/ZUGFeRD/mustangproject) ; [horstoeko/zugferd](https://github.com/horstoeko/zugferd) ; [e-invoice-eu](https://github.com/gflohr/e-invoice-eu)

### Inferences
- Invoice Ninja, Akaunting, InvoiceShelf et Crater ne sont pas des PA. Sans connecteur PA documenté, ils ne conviennent pas à une TPE française à partir de septembre 2027. Pennylane, qui a un MCP et fait partie de l'écosystème des PA, ou Dolibarr + module EInvoicing sont les options les plus réalistes.

### Gaps
- Je n'ai pas vérifié l'immatriculation PA de Pennylane, Qonto ou Odoo sur la liste officielle de la DGFiP, ni l'état e-invoicing France d'Odoo et d'Invoice Ninja.

## 7. Benchmark SaaS rapide (pour comparaison)

### Takeaway
Les SaaS (Motion, Reclaim, Sunsama, Fyxer, Pennylane) offrent le meilleur rapport effort/résultat mais enferment l'utilisateur. Les packs ouverts (plugins Anthropic, n8n, Inbox Zero, Twenty) donnent la portabilité au prix d'un peu d'intégration.

### Cited Findings
- Inbox Zero se positionne contre **Fyxer** (assistant email SaaS). — [inbox-zero](https://github.com/elie222/inbox-zero)
- Prix Motion, Reclaim et Sunsama : voir la section 4. — [dupple](https://dupple.com/compare/motion-vs-sunsama)
- Flags « offre faible ou non prouvée » :
  - kits Chief of Staff à moins de 1,2k étoiles et quelques commits (clawchief, Dex, claude-chief-of-staff)
  - packs n8n payants sur Gumroad
  - agents Metabase hébergés aux compteurs fictifs
  - modules IA tiers Odoo sans avis
  - **dépôts archivés** : Flowise, Frappe Books, Maybe Finance, GongRzhe Gmail MCP, calcom/docker
  - Cal.com : n'est plus open source (Cal.diy).
  — [maybe](https://github.com/maybe-finance/maybe) ; voir les sections précédentes pour les autres

### Gaps
- Je n'ai pas consulté G2 ni Product Hunt (pas de notes ni de nombre d'avis vérifiés), ni Reddit (r/selfhosted, r/n8n, r/smallbusiness) pour les retours terrain.
