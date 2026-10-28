# Systèmes IA prêts à l'emploi pour la prospection et la vente (état au 25 octobre 2026)

Note méthodo : chiffres GitHub relevés le 2026-10-25 via l'API de recherche GitHub (étoiles, forks, date du dernier push « pushed_at »). Les README ont été lus directement sur github.com. n8n.io et api.n8n.io étaient inaccessibles depuis cet environnement (DNS / proxy refusé) : aucun compteur de vues n8n officiel n'a pu être relevé. Beaucoup de sources SaaS sont des blogs de concurrents, signalé à chaque fois.

## 1. Agents open source GitHub (AI SDR, outreach, scrapers de leads) : étoiles, activité, utilisabilité réelle

### Takeaway
En 2026, la nouvelle génération d'AI SDR open source « tourne sur l'abonnement Claude Code / Codex » (Harvey, Franco) ou sur une base de données licenciée (OpenOutreach). Ces outils couvrent toute la chaîne : sourcing, e-mail, relances, gestion des réponses. Aucun ne publie de résultat chiffré (taux de réponse, RDV, CA). SalesGPT, la référence historique, est à l'arrêt depuis septembre 2024.

### Cited Findings
**Harvey (ethanplusai/harvey)**
- 2 514 étoiles, 524 forks, créé le 2026-03-12, dernier push le 2026-10-24, licence MIT. Il se présente comme un « Autonomous AI sales agent powered by Claude Code or Codex. Finds prospects, writes cold emails, sends campaigns, handles replies, books meetings ». — [GitHub API search](https://github.com/ethanplusai/harvey)
- Ce que fait vraiment le README :
  - Sourcing : entreprises via OpenStreetMap (gratuit), DataForSEO (0,372 $/1 000 fiches) ou Serper (environ 0,30 à 1 $/1 000).
  - Profilage du site en HTTP simple. Recherche du dirigeant sur le site de l'entreprise. Déduction du format d'e-mail, avec un statut verified/risky/guess/invalid.
  - Séquences de 3 e-mails écrites par le LLM à partir de « skills » Markdown modifiables.
  - Envoi par Gmail, M365, SMTP ou Instantly, avec montée en charge progressive (warmup), plafond quotidien et kill switch.
  - Classification des réponses par intention, arrêt de la séquence en cas de réponse ou de rebond.
  - Par défaut, chaque e-mail attend une validation humaine (Outbox), sauf si l'on active l'« autopilot ». — [README Harvey](https://github.com/ethanplusai/harvey)
- La prise de RDV automatique est seulement listée en « Next » dans la roadmap : elle n'est pas livrée, contrairement à ce que dit la description. — [README Harvey](https://github.com/ethanplusai/harvey)
- L'automatisation LinkedIn est désactivée par défaut, « violates LinkedIn's ToS ». Le README insiste sur CAN-SPAM, RGPD/PECR, un domaine secondaire dédié et 2 à 4 semaines de warmup. — [README Harvey](https://github.com/ethanplusai/harvey)
- Aucune preuve de résultat : la démo utilise des données inventées (« Bookwell », domaines .test). On compte 303 commits et 242 tests. — [README Harvey](https://github.com/ethanplusai/harvey)

**Franco (GortexAI/franco)**
- 715 étoiles et 261 forks, alors que le dépôt a été créé le 2026-10-15 (10 jours). MIT. — [GitHub](https://github.com/GortexAI/franco)
- Agent outbound auto-hébergé, tournant sur Claude Code (Pro/Max) ou Codex. Trois modes :
  - « generated » : le LLM rédige.
  - « templates » : il envoie mot pour mot une copie déjà validée.
  - « Raad » : un entonnoir narratif inspiré de Raad Mobrem (Intro).
- Fonctions : dashboard local, liste de suppression, Gmail OAuth/SMTP/Instantly. Un vérificateur d'e-mail est requis (Reoon, ZeroBounce, Hunter). Le code est dérivé d'un projet MIT dont le nom n'est pas cité dans le README. Aucune métrique ni étude de cas. — [README Franco](https://github.com/GortexAI/franco)

**OpenOutreach (eracle/OpenOutreach)**
- 3 409 étoiles, 618 forks, dernier push le 2026-10-23, GPL-3.0, environ 1 065 commits. — [GitHub](https://github.com/eracle/OpenOutreach)
- Fonctionnement : CLI `uv tool install openoutreach`. On décrit son produit, et les leads sont trouvés via BetterContact Lead Finder (source « licenciée »). Le LLM justifie chaque lead retenu. L'e-mail est trouvé via BetterContact (1 crédit par e-mail vérifié, 40 crédits gratuits) puis envoyé en SMTP depuis votre boîte. Plugin Claude Code et image Docker disponibles. — [README OpenOutreach](https://github.com/eracle/OpenOutreach)
- Signaux de prudence :
  - Le lien BetterContact est affilié.
  - Une offre hébergée est proposée à 2 $/lead.
  - L'auteur admet que la composante d'apprentissage n'est « not yet shown to beat picking at random ».
  - Aucune liste d'utilisateurs ni chiffre de résultats.
  - Historiquement, le projet était un bot d'automatisation LinkedIn. Il se dit aujourd'hui « browserless, no scraping », mais sort toujours une colonne `linkedin_url`. — [README OpenOutreach](https://github.com/eracle/OpenOutreach)

**SalesGPT (filip-michalsky/SalesGPT)**
- 2 794 étoiles, 613 forks, mais dernier push le 2024-09-17 : projet de fait abandonné. Description : « Context-aware AI Sales Agent to automate sales outreach ». — [GitHub](https://github.com/filip-michalsky/SalesGPT)

**ai-sales-team-claude (zubair-trabzada)**
- 1 468 étoiles, 376 forks, dernier push le 2026-03-27, MIT. Ce sont des skills Claude Code (`prospect`, `qualify` BANT+MEDDIC, `contacts`, `outreach`, `followup`, `proposal`, `report-pdf`, etc.). L'outil génère des fichiers Markdown/PDF et n'envoie rien. Le README renvoie vers une communauté Skool (« aiworkshop »), un probable entonnoir d'upsell. — [README](https://github.com/zubair-trabzada/ai-sales-team-claude)

**Autres briques**
- warmbly/warmbly : 484 étoiles, 106 forks, Go. « The largest open-source B2B cold outreach and email warmup service ». — [GitHub](https://github.com/warmbly/warmbly)
- Knotie-AI : 163 étoiles. Agent vocal/texte inbound/outbound, adoption faible. — [GitHub](https://github.com/avijeett007/Knotie-AI)
- growchief/growchief : 3 495 étoiles, outil d'automatisation « outreach » des réseaux sociaux, mais dernier push le 2025-10-13 (inactif depuis un an). — [GitHub](https://github.com/growchief/growchief)
- omkarcloud/google-maps-scraper : 3 808 étoiles, 550 forks, push le 2026-10-19. « Google Maps Scraper & Lead Generation Tool. Extract 50+ data points including business emails, phone numbers ». — [GitHub](https://github.com/omkarcloud/google-maps-scraper)
- Mahanaicoach/google-maps-scraper-kit : 1 881 étoiles, push le 2026-10-13. Scraper Google Maps local en Docker, sans clé API, export CSV. — [GitHub](https://github.com/Mahanaicoach/google-maps-scraper-kit)
- Bruit dans les recherches : MoneyPrinterV2 (32 188 étoiles, « Automate the process of making money online ») ressort sur « outreach », mais ce n'est pas un outil SDR sérieux. — [GitHub](https://github.com/FujiwaraChoki/MoneyPrinterV2)

### Inferences
- Pour Hari (France, toutes niches), le meilleur candidat « pack » est Harvey ou Franco en mode validation humaine, avec un domaine secondaire. Ils sont agnostiques de la niche, car le sourcing se fait par Maps/OSM/SERP, ce qui convient très bien aux TPE/PME locales, moins aux grands comptes. Le coût marginal est quasi nul hors abonnement Claude.
- Franco cumule 715 étoiles et 261 forks en 10 jours, avec un ratio forks/étoiles inhabituellement élevé. Il faut attendre avant de s'y fier : buzz, ou possible gonflement artificiel.
- Les étoiles GitHub mesurent l'intérêt, pas le chiffre d'affaires. Aucun de ces dépôts ne fournit de preuve d'efficacité commerciale.
- Le sourcing via Google Maps est très efficace pour les niches locales. En revanche, scraper des e-mails nominatifs puis les deviner relève du cadre CNIL sur la « reconstitution d'adresses » (voir section 4).

### Gaps
- Pas de nombre d'utilisateurs actifs ni de taux de réponse publiés pour aucun de ces dépôts.
- Les exemples CrewAI/LangGraph « sales agents » (tutoriels) n'ont pas été mesurés individuellement : ce sont surtout des démos sans envoi réel.
- Aucune alternative open source mature à Clay ou Apollo (base de contacts B2B) n'a été trouvée. Les données restent payantes (BetterContact, DataForSEO, Apollo).

## 2. Templates n8n / Make pour lead gen et outreach : usages, avis

### Takeaway
L'écosystème n8n est abondant mais peu vérifiable. Les templates de prospection (Apollo → GPT → Gmail/Sheets/Airtable, LinkedIn via Apify/PhantomBuster) sont nombreux et souvent gratuits. Les packs payants Gumroad (20 à 49 $) n'affichent quasiment aucun avis, et je n'ai obtenu aucun compteur d'usage officiel.

### Cited Findings
- enescingoz/awesome-n8n-templates : 26 098 étoiles, 6 574 forks, « 280+ free n8n automation templates », mise à jour en octobre 2026. C'est une collection générale, pas spécifique à la vente. — [GitHub](https://github.com/enescingoz/awesome-n8n-templates)
- Templates gratuits hébergés par growwstacks.com :
  - Airtable + Jina AI + agents OpenAI (enrichissement, recherche du décideur, e-mail, contrôle qualité). — [growwstacks](https://growwstacks.com/workflows/generate-sales-leads-and-personalized-outreach-emails-using-jina-ai-and-openai-agents)
  - Leads locaux Apify + Hunter avec scoring. — [growwstacks](https://growwstacks.com/workflows/extract-and-qualify-local-business-leads-and-draft-cold-emails-with-openai-apify-and-hunter/)
  - Multi-agents o3 + GPT-4.1. — [growwstacks](https://growwstacks.com/workflows/multi-agent-cold-email-campaign-generator-with-o3-director-and-gpt-41-specialists)
  - Demandes de connexion LinkedIn Apollo + Apify + PhantomBuster. — [growwstacks](https://growwstacks.com/workflows/personalized-linkedin-connection-requests-with-apollo-gpt-4-apify-and-phantombuster/)
- Packs payants :
  - « Apollo lead gen » à 20 $ : messages LinkedIn et 4 e-mails. — [Gumroad](https://gainflowai.gumroad.com/l/apollo-lead-gen)
  - Pipeline Apollo → Airtable → Gmail à 49 $, seulement 2 notes. — [Gumroad](https://dneale03.gumroad.com/l/ibichu)
  - « 6000 n8n workflow » en vrac. — [Gumroad](https://aipromptsworld.gumroad.com/l/6000-n8n-workflow-automation-template)
- Un playbook propose de scraper les pages de résultats Apollo via Apify au lieu d'exporter, car l'export est jugé « très cher ». Cela pose un problème de CGU. — [Jeff Bullas playbook](https://www.jeffbullas.com/playbooks/building-your-automated-ai-linkedin-outreach-system-in-n8n/)
- Guide gratuit d'enrichissement n8n + Apollo, avec workflow importable. — [Substack](https://angelsant.substack.com/p/lead-enrichment-with-n8n-apolloio?r=5o9a5d)

### Inferences
- Les packs Gumroad de « 6000 workflows » sont à considérer comme du contenu de faible valeur, souvent repackagé depuis des collections gratuites. À éviter.
- Les templates n8n LinkedIn qui s'appuient sur PhantomBuster ou Apify pour envoyer des invitations exposent au risque de restriction du compte LinkedIn (section 4).
- n8n reste intéressant comme « colle » auto-hébergée entre une source (Maps, Apollo MCP/API), un LLM et un envoi via Instantly, lemlist ou Gmail.

### Gaps
- Compteurs de vues/usages et classement par popularité de n8n.io/workflows : non obtenus (site bloqué depuis l'environnement).
- Templates Make : non couverts.
- Avis vérifiés sur les packs de créateurs : quasi inexistants.

## 3. Serveurs MCP / plugins Claude Code pour la vente

### Takeaway
Les connecteurs officiels sont désormais la voie la plus solide et la moins risquée. Apollo (MCP officiel depuis le 24 février 2026), HubSpot (connecteur officiel gratuit) et le plugin `sales` d'Anthropic (36 skills, connecteurs CRM/enrichissement/agenda) tournent tous dans une conversation lancée par l'utilisateur. Le MCP LinkedIn communautaire le plus populaire repose sur du scraping de session.

### Cited Findings
- Plugin Anthropic `sales` (anthropics/knowledge-work-plugins), conçu pour Cowork et compatible Claude Code.
  - Installation : `claude plugin marketplace add anthropics/knowledge-work-plugins` puis `claude plugin install sales@knowledge-work-plugins`.
  - 36 skills, dont `account-research`, `draft-outreach`, `lead-triage`, `call-prep`, `call-summary`, `schedule-meeting`, `pipeline-review` et `forecast`.
  - Connecteurs listés : HubSpot, Close, Salesforce, Gmail, Google Calendar, Calendly, M365, Gong, Fireflies, Clay, ZoomInfo, Apollo, Lusha, Crunchbase, Slack.
  - Les skills peuvent « create email drafts or send email… book meetings ». Anthropic recommande de régler l'envoi sur « ask » pour les exécutions planifiées. — [GitHub anthropics/knowledge-work-plugins/sales](https://github.com/anthropics/knowledge-work-plugins/tree/main/sales)
- Apollo MCP officiel : bêta dans l'annuaire des connecteurs Claude depuis le 24 février 2026.
  - Fonctions : recherche de leads, détails d'entreprise, enrichissement (consomme des crédits Apollo), création et mise à jour de contacts, ajout et retrait de séquences.
  - Authentification OAuth, sans clé API. — [Apollo newsroom](https://www.apollo.io/newsroom/announcements/apollo-delivers-gtm-outbound-execution-to-claude) ; [Apollo MCP](https://www.apollo.io/product/mcp)
  - Apollo indique que tous les plans, y compris le gratuit, y ont accès. Un guide tiers parle au contraire de plans payants : contradiction non résolue. — [lagrowthmachine.com/apollo-mcp](https://lagrowthmachine.com/apollo-mcp/)
  - Le connecteur ne fonctionne que dans une conversation lancée par l'utilisateur, sans prospection autonome. — [usecarly](https://www.usecarly.com/blog/claude-apollo-integration/)
- HubSpot : connecteur Claude officiel, développé par HubSpot, gratuit sur tous les tiers, OAuth. HubSpot évoque aussi un « HubSpot Sales Plugin » (connecteur + skills). — [hubspot.com/claude](https://www.hubspot.com/claude?webview=1)
- stickerdaniel/linkedin-mcp-server : 4 010 étoiles, 708 forks, 197 issues ouvertes, actif en octobre 2026. Accès aux profils, entreprises, offres d'emploi et messages. Les topics incluent « linkedin-scraper ». — [GitHub](https://github.com/stickerdaniel/linkedin-mcp-server)
- eliasbiondo/linkedin-mcp-server : 201 étoiles, recherche et scraping de profils. — [GitHub](https://github.com/eliasbiondo/linkedin-mcp-server)
- MailerLite et Gmail disposent de connecteurs MCP (déjà disponibles dans l'environnement de Hari). MailerLite est fait pour des listes opt-in : ses CGU interdisent en général les listes achetées ou froides. Ce dernier point est une inférence, non vérifiée ici.

### Inferences
- La pile la plus « propre » pour Hari en France : plugin `sales` + Apollo MCP (sourcing et enrichissement) + Gmail/Calendar (brouillons et RDV) + HubSpot gratuit (CRM). Le tout reste semi-automatique, avec validation humaine.
- Les MCP LinkedIn communautaires utilisent un cookie de session : à réserver à la lecture ponctuelle, jamais à l'envoi en masse.

### Gaps
- Contenu exact de `.mcp.json` et `CONNECTORS.md` du plugin `sales` : non lus.
- MCP officiel Clay : non confirmé.
- Nombre d'étoiles du dépôt knowledge-work-plugins : non relevé.

## 4. Benchmark SaaS (lemlist, La Growth Machine, Instantly, Smartlead, Clay, Apollo, 11x, Artisan) et conformité

### Takeaway
Pour l'outbound « classique », les outils d'envoi coûtent de 37 à 110 $/mois. LGM est français et multicanal LinkedIn + e-mail dès 50 à 60 €/mois. Clay coûte au moins 185 $/mois (Launch), avec une courbe d'apprentissage lourde. Les « AI SDR » autonomes haut de gamme (11x, Artisan) ont une réputation abîmée : churn élevé, accusations contre 11x.

### Cited Findings
- Instantly : à partir de 37 $/mois (LGM) ou 47 $/mois en Growth mensuel (SmartReach, prix d'août 2026). Boîtes d'envoi et warmup illimités, pas de LinkedIn. — [LGM comparatif](https://lagrowthmachine.com/lemlist-vs-instantly-vs-lgm/) ; [SmartReach](https://smartreach.io/blog/instantly-vs-smartlead-vs-lemlist/)
- Smartlead : environ 39 $/mois, +29 $ par client pour les agences. — [SmartReach](https://smartreach.io/blog/instantly-vs-smartlead-vs-lemlist/)
- lemlist (français) : 69 $ (Email) ou 109 $/utilisateur (Multichannel) selon SmartReach. G2 indique 87 $/mois pour Multichannel Expert. Les sources divergent. — [SmartReach](https://smartreach.io/blog/instantly-vs-smartlead-vs-lemlist/) ; [G2](https://www.g2.com/compare/la-growth-machine-vs-lemlist)
- La Growth Machine (français) : Basic à 60 €/mois (50 € en annuel), LinkedIn + e-mail, enrichissement en cascade, essai de 14 jours. Source : LGM elle-même. — [LGM](https://lagrowthmachine.com/lemlist-vs-instantly-vs-lgm/)
- Clay (refonte de mars 2026) :
  - Plans : Free ; Launch à 185 $/mois (2 500 Data Credits et 15 000 Actions) ; Growth à 495 $/mois ; Enterprise sur devis. — [Crustdata, vérifié le 16/10/2026](https://crustdata.com/reviews/clay)
  - Note G2 de 4,7/5 sur environ 189 avis. — [Enrich.so](https://enrich.so/blog/clay-review)
  - Premier workflow en production en 20 à 40 h. — [Gojiberry](https://blog.gojiberry.ai/blog/clay-pricing)
  - Le Growth est passé de 349 à 446 $ avec 40 % de crédits en moins. — [SyncGTM](https://www.syncgtm.com/blog/clay-pricing-change)
  - Sources majoritairement concurrentes.
- Apollo : sa page LinkedIn a été retirée en mars 2025, sans motif officiel, puis rétablie (« live again in July 2026 »). L'interdiction LinkedIn du scraping et de l'accès automatisé reste en vigueur. — [Salesmotion](https://salesmotion.io/blog/linkedin-removed-apollo-brand-page-2025-alternatives) ; [LeadGenius 2026](https://www.leadgenius.com/resources/linkedins-b2b-data-crackdown-what-changed-by-2026)
- 11x :
  - Des sources (investisseurs, ex-employés) rapportées par TechCrunch font état de churn élevé, de métriques gonflées et de logos clients non autorisés (ZoomInfo, client un mois seulement, aurait été affiché pendant environ 12 mois).
  - Des ex-employés parlent de 70 à 80 % de churn ; 11x revendique 79 % de rétention. — [Tech Rundown (résumé TechCrunch)](https://tech-rundown.beehiiv.com/p/fraud-charges-surface-11x-accused-of-overstating-revenue-and-misusing-logos) ; [Salesmotion](https://salesmotion.io/blog/turns-out-ai-sdrs-are-too-good-to-be-true-11x-might-face-legal-action)
- Artisan : levée de 25 M$ (avril 2025). Le cofondateur reconnaît un « relatively high churn » pour la première génération d'AI SDR et des hallucinations « mostly fixed ». — [TechCrunch](https://techcrunch.com/2025/04/09/artisan-the-stop-hiring-humans-ai-agent-startup-raises-25m-and-is-still-hiring-humans)
- Conformité en France (sources secondaires, pas la CNIL directement) :
  - B2C : opt-in obligatoire (art. L.34-5 CPCE).
  - B2B : opt-out admis si le message concerne la fonction du destinataire, avec information et droit d'opposition. L'adresse prenom.nom@societe.fr reste une donnée personnelle. — [donneespersonnelles.fr](https://www.donneespersonnelles.fr/prospection-commerciale-rgpd)
  - La CNIL aurait réorganisé ses fiches en juin 2026 et publié un cadre sur la reconstitution d'adresses e-mail pro ainsi que sur les appels à froid (fin 2026). Dates à vérifier sur cnil.fr. — [Leptidigital](https://www.leptidigital.fr/growth-hacking/appels-a-froid-e-mails-pro-devines-cnil-encadre-deux-pratiques-courantes-prospection-commerciale-92263/)
  - Le régime de consentement pour la prospection téléphonique serait entré en vigueur en août 2026, selon des blogs. — [mntd.fr PDF](https://www.mntd.fr/app/uploads/2026/02/Prospection-commerciale-RGPD-quelles-sont-les-regles-en-2026.pdf)
  - Sanctions citées : Hubside 525 000 € (2024), Canal+ 600 000 € (2023). — [donneespersonnelles.fr sanctions](https://donneespersonnelles.fr/prospection-commerciale-rgpd-sanctions)

### Inferences
- Pour Hari, en France et avec un budget serré, la meilleure combinaison est un agent open source (Harvey/Franco) qui envoie via Gmail ou Instantly (37 à 47 $). LGM sert si LinkedIn est indispensable, car il fait ce canal de façon industrialisée mais reste exposé aux CGU LinkedIn.
- 11x et Artisan sont à éviter pour un solo ou une petite structure : prix élevés (non vérifiés ici), churn, controverses.
- Deviner des e-mails (« pattern learning » de Harvey, Franco ou Hunter) est précisément la pratique que la CNIL encadre. Il faut documenter l'intérêt légitime, informer dès le premier message, prévoir un opt-out et une liste de suppression.

### Gaps
- Prix publics actuels de 11x et Artisan : non vérifiés.
- Pages primaires de la CNIL : non consultées. Les dates de 2026 viennent de blogs.
- Notes Trustpilot/G2 détaillées de lemlist, LGM, Instantly et Smartlead : non relevées.

## 5. Preuves de génération de revenu et modes d'échec courants

### Takeaway
Il n'existe pas de preuve indépendante solide de CA généré par les agents open source. Les seuls repères chiffrés sont des benchmarks de vendeurs : environ 3 % de taux de réponse moyen en cold e-mail en 2026, 85 à 95 % de placement en boîte de réception. Les échecs récurrents sont la délivrabilité, les hallucinations ou la personnalisation creuse, le churn des AI SDR après 1 à 3 mois et les restrictions LinkedIn.

### Cited Findings
- Taux de réponse moyen en cold e-mail 2026 : 3,43 %, 5,5 % pour le quartile supérieur (benchmark Instantly). Woodpecker : 3,1 %, et 1,7 % sans personnalisation. Boomerang : 1,4 % (estimation modélisée). — [Instantly](https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/) ; [lemlist benchmarks](https://lemlist.com/blog/cold-email-benchmarks/) ; [Boomerang](https://www.getboomerang.ai/glossaries/cold-email-reply-rate-benchmarks-2026)
- Placement en boîte de réception moyen : environ 85 %, avec environ 12 % en spam (rapport Instantly cité par un résumé). Le seuil de plaintes spam à viser est inférieur à 0,3 % selon lemlist (non confirmé par une source Google/Yahoo primaire dans cette recherche). — [searchlab.nl](https://searchlab.nl/en/statistics/cold-email-statistics-2026) ; [lemlist](https://lemlist.com/blog/cold-email-benchmarks/)
- Échecs des AI SDR : hallucinations, problèmes fonctionnels, churn de 70 à 80 % selon d'ex-employés de 11x. Un blog concurrent décrit un retour vers des SDR humains assistés par l'IA fin 2025, ce qui est peu fiable. — [Tech Rundown](https://tech-rundown.beehiiv.com/p/fraud-charges-surface-11x-accused-of-overstating-revenue-and-misusing-logos) ; [leadgen-economy](https://leadgen-economy.com/blog/ai-sdr-cancellation-wave-failure-forensics/) ; [naoma.ai](https://naoma.ai/articles/ai-sdr-dying-2026)
- Liste de vérifications côté acheteur face aux promesses des AI SDR. — [Salesmotion](https://salesmotion.io/blog/ai-sdr-claims-scrutiny-what-buyers-should-verify)
- Les dépôts eux-mêmes reconnaissent leurs limites :
  - Harvey : risque d'injection de prompt via les sites et les réponses, d'où une rétention pour revue. — [README Harvey](https://github.com/ethanplusai/harvey)
  - OpenOutreach : son apprentissage ne bat pas encore le hasard. — [README OpenOutreach](https://github.com/eracle/OpenOutreach)

### Inferences
- Ordre de grandeur pour 1 000 prospects contactés : environ 30 réponses, dont une fraction en RDV. La rentabilité dépend donc surtout de l'offre et du ciblage, pas de l'outil.
- Échecs typiques à prévenir :
  1. Envoi depuis le domaine principal ou sans SPF/DKIM/DMARC.
  2. Volume trop rapide sans warmup.
  3. E-mails « devinés » non vérifiés, donc rebonds.
  4. Personnalisation générique par le LLM.
  5. Automatisation LinkedIn, avec restriction du compte.
  6. Autopilot sans revue, d'où des hallucinations et un risque juridique.
  7. Pas de liste d'opposition (RGPD).
- Les « packs » vendus avec promesse de revenu (Gumroad, Skool, MoneyPrinter) sont non prouvés.

### Gaps
- Aucune étude de cas indépendante avec CA attribuable à Harvey, Franco, OpenOutreach ou un template n8n.
- Pas de données vérifiées sur le taux de restriction des comptes LinkedIn selon l'outil.
- Fils Reddit (r/coldemail, r/n8n, r/sales) : non lus directement dans cette passe.
