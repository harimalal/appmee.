# Systèmes IA prêts à l'emploi : création de contenu + montage + publication de vidéos courtes (Shorts / Reels / TikTok)

*Notes rédigées le 25 octobre 2026. Les chiffres GitHub (étoiles, forks, issues ouvertes, dernier push) ont été relevés le 25/10/2026 via l'API de recherche GitHub. Avertissement sur la méthode : n8n.io et api.n8n.io étaient inaccessibles depuis cette session (DNS / proxy refusé), donc aucun compteur de vues des modèles n8n n'a pu être relevé. Reddit, G2 et Trustpilot n'ont pas été consultés directement.*

## 1. Dépôts GitHub open source : génération de vidéos faceless/courtes et mise en ligne automatique de bout en bout

### Takeaway
Sur GitHub, **aucun dépôt très suivi ne couvre la chaîne entière de façon fiable**, publication comprise. MoneyPrinterTurbo (135k ★, actif) est le générateur « sujet → vidéo » le plus solide. Son README évoque une mise en ligne auto, mais sans en documenter la configuration. Les nouveaux venus « agentiques » (OpenMontage, HyperFrames, skills Remotion) font tourner un agent de code (Claude Code…) comme studio de montage, mais aucun ne publie sur les réseaux. ShortGPT et short-video-maker (MCP) sont quasi à l'arrêt.

### Cited Findings

**Tableau de traction (relevé GitHub du 25/10/2026)**

| Dépôt | ★ | Forks | Issues ouvertes | Dernier push | Licence | Ce qu'il fait vraiment |
|---|---|---|---|---|---|---|
| harry0703/MoneyPrinterTurbo | 135 035 | 21 390 | 78 | 25/10/2026 | MIT | Sujet/mot-clé → script LLM → voix → rushes → sous-titres → musique → MP4 |
| heygen-com/hyperframes | 71 931 | 6 497 | 285 | 25/10/2026 | Apache-2.0 | « Write HTML. Render video. Built for agents. » Framework de rendu |
| calesthio/OpenMontage | 71 805 | 9 315 | 410 | 24/10/2026 | AGPL-3.0 | Système de production vidéo agentique pour assistants de code |
| remotion-dev/remotion | 67 351 | 5 438 | 206 | 25/10/2026 | licence propre (NOASSERTION) | Vidéo programmatique en React |
| FujiwaraChoki/MoneyPrinterV2 | 32 188 | 3 454 | 91 | 15/09/2026 | AGPL-3.0 | « Automate the process of making money online » |
| FujiwaraChoki/MoneyPrinter (v1) | 14 089 | 1 836 | 19 | 26/03/2026 | MIT | Création de YouTube Shorts avec MoviePy |
| RayVentura/ShortGPT | 8 070 | 1 168 | 85 | **10/02/2025** | MIT | « Experimental » : automatisation de chaînes Shorts/TikTok |
| remotion-dev/skills | 5 688 | 631 | 22 | 22/10/2026 | — | Skills d'agent officiels Remotion |
| Anil-matcha/AI-Youtube-Shorts-Generator | 5 594 | 1 018 | 25 | maj 25/10/2026 | — | Vidéo longue → clips 9:16 (alternative open source à Opus Clip) |
| inovector/mixpost | 3 864 | 582 | 35 | 16/03/2026 | MIT | Planificateur social auto-hébergé |
| digitalsamba/claude-code-video-toolkit | 2 339 | 396 | 3 | 21/10/2026 | MIT | Boîte à outils de production vidéo pour Claude Code |
| elevenlabs/elevenlabs-mcp | 1 538 | 259 | 0 | 20/08/2026 | MIT | Serveur MCP officiel ElevenLabs |
| gyoridavid/short-video-maker | 1 431 | 441 | 29 | **21/06/2025** | MIT | Vidéos courtes via MCP + REST |
| IgorShadurin/app.yumcut.com | 895 | 143 | 4 | maj 24/10/2026 (créé 13/02/2026) | — | Prompt → vidéo verticale (script, scènes, voix, sous-titres) |
| SamurAIGPT/AI-Faceless-Video-Generator | 523 | 107 | 2 | maj 25/10/2026 | — | Script + voix + visage parlant IA (notebook Jupyter) |

Sources : [recherche GitHub API, dépôts listés](https://github.com/harry0703/MoneyPrinterTurbo) ; [Anil-matcha/AI-Youtube-Shorts-Generator](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator) ; [IgorShadurin/app.yumcut.com](https://github.com/IgorShadurin/app.yumcut.com) ; [SamurAIGPT/AI-Faceless-Video-Generator](https://github.com/SamurAIGPT/AI-Faceless-Video-Generator). Pour les deux derniers et Anil-matcha, l'API n'a donné que `updated_at`, pas `pushed_at`.

**MoneyPrinterTurbo (lecture du README)** — [README](https://github.com/harry0703/MoneyPrinterTurbo)
- Chaîne : sujet ou mot-clé → script IA multilingue (ou script fourni) → voix off → rushes → sous-titres → musique de fond → vidéo finale.
- LLM pris en charge : OpenAI, Claude, Gemini, DeepSeek, Qwen, Kimi, Azure, Grok, MiniMax, etc., ainsi que OpenRouter, LiteLLM et Ollama en local.
- TTS : Edge TTS (gratuit, sans clé), Azure, ElevenLabs, Gemini, Fish Audio, Kokoro, Chatterbox, VoxCPM, MiniMax, etc.
- Visuels : banques Pexels, Pixabay et Coverr, médias locaux, ou générateurs IA (MiniMax, Seedance, WaveSpeed…), plus du texte → image → clip.
- Sous-titres : `edge` (timestamps TTS, sans GPU) ou `whisper` (faster-whisper en local).
- Formats : 9:16 en 1080×1920, 16:9 et 1:1.
- Lots : la CLI accepte `--batch-file` (jusqu'à 100 tâches). Une tâche en échec n'arrête pas les autres.
- Interfaces : WebUI, API REST, CLI, et « AI Agent via un document Skill ». Installation via PyPI `mpt`, Docker, paquet Windows en un clic ou Colab. Le README signale qu'un paquet PyPI nommé `MoneyPrinterTurbo` est tiers.
- Matériel : au minimum 4 cœurs et 4 Go de RAM. Pas de GPU requis.
- **Publication :** le README affirme une mise en ligne auto vers TikTok, Instagram et YouTube Shorts, mais **ne décrit ni la configuration ni les identifiants**. Cette affirmation n'est pas vérifiée.
- Problèmes connus (FAQ) : ffmpeg introuvable, « too many open files », échecs de téléchargement des modèles Whisper (large-v3 ≈ 3 Go), chemins Windows à caractères spéciaux.

**short-video-maker (gyoridavid)** — [README](https://github.com/gyoridavid/short-video-maker)
- Entrée : une liste de scènes (texte de narration + `searchTerms`).
- Voix : Kokoro, **anglais uniquement**. Sous-titres : whisper.cpp. Rushes : **Pexels uniquement**. Rendu : Remotion + FFmpeg (gourmand en CPU).
- Outils MCP : `create-short-video` et `get-video-status`, plus une API REST. Des exemples n8n sont fournis dans un dépôt séparé.
- **Aucune publication** : le résultat est un fichier.
- Pas de Windows. Il faut au moins 3 Go de RAM.
- Dernier push le 21/06/2025 : projet de fait **non maintenu**.

**OpenMontage** — [README](https://github.com/calesthio/OpenMontage)
- Pas d'orchestrateur en code : l'agent (Claude Code, Cursor, Copilot, Codex, Windsurf) suit des manifestes YAML et des skills Markdown.
- Rendu via Remotion ou HyperFrames, puis FFmpeg.
- Pipelines (11 dans le tableau, alors que la description en annonce 12 : incohérence) : explainer animé, avatar porte-parole, cinématique, Clip Factory, documentaire, localisation/doublage, podcast repurpose, screen demo, talking head…
- Un chemin « zéro clé » existe (Piper TTS, banques libres). Coûts annoncés : environ 0,15 à 1,50 $ par vidéo avec un fournisseur image/vidéo, 1 à 3 $ en configuration complète, plafond de budget de 10 $ par défaut.
- **Pas d'intégration de publication sociale** : il n'y a qu'une étape d'approbation « publish ».
- Un LLM cloud est obligatoire (le support local est « coming soon »).
- La traction (71,8k ★) mesure l'intérêt, pas l'usage en production. Les vidéos vitrines sont celles des mainteneurs.

**HyperFrames (HeyGen)** — [dépôt](https://github.com/heygen-com/hyperframes)
- Framework HTML/GSAP → vidéo (MP4, WebM, MOV).
- Dans un agent CLI (Claude Code), on l'utilise via des skills locales (`npx skills add heygen-com/hyperframes`), qui ajoutent les commandes `/hyperframes`, `/hyperframes-cli` (init, lint, preview, render) et `/hyperframes-media` (TTS, transcription, détourage).
- Il existe aussi un MCP hébergé (compose, render_video) pour les clients chat. D'après les instructions du serveur MCP, ces deux outils sont désactivés depuis Claude Code.
- Pas de publication sociale.

### Inferences
- Pour un système « adaptable à n'importe quelle niche », **MoneyPrinterTurbo** reste la base la plus robuste côté génération : multi-LLM, multilingue, WebUI, API et traitement par lots. Il doit être couplé à une couche de publication séparée (Postiz, Upload-Post, Blotato…).
- **OpenMontage, HyperFrames et les skills Remotion** visent une qualité « motion design » pilotée par un agent plutôt que la production de masse. Ils conviennent mieux au contenu de marque qu'aux fermes de Shorts.
- **Signaux faibles :** ShortGPT (« experimental », plus de push depuis février 2025) et short-video-maker (plus de push depuis juin 2025) sont à éviter pour un système neuf. yumcut est récent (février 2026) et a peu de recul.
- La croissance très rapide d'OpenMontage (≈72k ★ en 2026) est à prendre avec prudence : les étoiles ne valent pas des cas d'usage.

### Gaps
- MoneyPrinterV2 : le README n'a pas pu être relu dans cette session. Son mécanisme de mise en ligne YouTube et ses modules (Twitter, affiliation) ne sont **pas vérifiés**.
- Aucun cas réel chiffré (vues, revenus) n'a été trouvé pour une chaîne produite avec ces dépôts.
- AutoShorts et mutonby/openshorts n'ont pas été vérifiés (non trouvés par la recherche).

## 2. Modèles n8n / Make pour les pipelines de contenu et de vidéos courtes avec publication

### Takeaway
L'écosystème n8n est dense mais **dominé par les vendeurs d'API**. La pile typique est la suivante : LLM pour le script, ElevenLabs pour la voix, un moteur de rendu (Creatomate, Shotstack, JSON2Video), puis Blotato ou Upload-Post pour la publication. Les « packs » vendus sur Gumroad ou Etsy n'ont aucune preuve de traction vérifiable. Les compteurs de vues de n8n.io n'ont pas pu être relevés.

### Cited Findings
- Modèles officiels de la galerie n8n repérés :
  - n°6014, « Create faceless videos with Gemini, ElevenLabs, Leonardo AI & Shotstack » — [n8n.io](https://n8n.io/workflows/6014-create-faceless-videos-with-gemini-elevenlabs-leonardo-ai-and-shotstack/)
  - n°14985, « Generate AI music and publish YouTube videos automatically with Blotato, OpenAI, ElevenLabs, and Shotstack » — [n8n.io](https://n8n.io/workflows/14985-generate-ai-music-and-publish-youtube-videos-automatically-with-blotato-openai-elevenlabs-and-shotstack/)
  - n°5100, « GPT-4o, RunwayML, ElevenLabs for Social Media » — [n8n.io](https://n8n.io/workflows/5100-gpt-4o-runwayml-elevenlabs-for-social-media/)
- Blotato publie son propre système d'agent n8n/Make « faceless videos → toutes plateformes ». Son nœud n8n exige d'activer les *verified community nodes*. — [Blotato help](https://help.blotato.com/api/n8n/n8n-faceless-videos) ; [Blotato blog](https://help.blotato.com/blog/automate-faceless-ai-videos-tiktok-reels)
- Tutoriels éditeurs proposant la pile ChatGPT + ElevenLabs + Creatomate pour des Shorts faceless — [Creatomate](https://creatomate.com/blog/how-to-auto-generate-faceless-shorts-with-chatgpt-and-n8n) ; [Orshot](https://orshot.com/blog/how-to-make-faceless-videos-with-n8n)
- Un guide déconseille l'automatisation totale dès le premier jour, car les plateformes surveillent le spam automatisé. Il recommande de relire les premières semaines et d'espacer les uploads — [Orshot](https://orshot.com/blog/how-to-make-faceless-videos-with-n8n)
- Packs vendus par des tiers (Etsy, Gumroad) promettant par exemple « moins de 1 $ par vidéo » : ce sont des affirmations marketing, sans compteur de ventes vérifié — [Etsy](https://www.etsy.com/listing/4356725968) ; [Gumroad kjetilfuras](https://kjetilfuras.gumroad.com/l/tqyib) ; [Gumroad josephcodes](https://josephcodes.gumroad.com/l/fqtdyd) ; [Gumroad mjekster](https://mjekster.gumroad.com/l/auto-content-creator)
- short-video-maker (MCP/REST) s'intègre à n8n, avec des exemples dans un dépôt séparé — [README](https://github.com/gyoridavid/short-video-maker)
- Postiz propose un nœud n8n personnalisé et une app Make — [README Postiz](https://github.com/gitroomhq/postiz-app)

### Inferences
- Sur n8n, la valeur réside dans l'orchestration. Le coût réel se trouve dans les API appelées (rendu, voix, publication), d'où le nombre de modèles écrits par les éditeurs eux-mêmes (Blotato, Creatomate, Shotstack).
- **Offres faibles :** les packs Gumroad/Etsy « viral shorts machine » n'ont ni avis vérifiés ni compteur public. Mieux vaut partir des modèles gratuits de n8n.io ou du dépôt d'exemples de short-video-maker.

### Gaps
- Pas de compteur de vues ou d'installations sur n8n.io (site inaccessible depuis la session).
- Galerie Make non consultée.
- Pas de données Reddit (r/n8n, r/automation) sur des résultats réels.

## 3. Serveurs MCP et skills/plugins Claude Code pour la vidéo et la publication sociale

### Takeaway
La pile « agent » est mature côté création : skills Remotion (5,7k ★), HyperFrames (72k ★), MCP officiel ElevenLabs, claude-code-video-toolkit. Côté publication, les options sont un **MCP hébergé payant** (Blotato, Upload-Post, Ayrshare) ou le MCP de Postiz (gratuit en auto-hébergé, sous réserve de ses propres apps validées).

### Cited Findings
- **remotion-dev/skills** : skills d'agent officiels, 5 688 ★, push le 22/10/2026 — [GitHub](https://github.com/remotion-dev/skills)
- **HyperFrames** : skills locales pour Claude Code, plus un MCP hébergé (compose, render) pour les clients chat — [GitHub](https://github.com/heygen-com/hyperframes)
- **elevenlabs/elevenlabs-mcp** : MCP officiel (TTS, transcription…), 1 538 ★, 0 issue ouverte, push le 20/08/2026 — [GitHub](https://github.com/elevenlabs/elevenlabs-mcp)
- **digitalsamba/claude-code-video-toolkit** : boîte à outils de production vidéo « AI-native » pour Claude Code, 2 339 ★, push le 21/10/2026 — [GitHub](https://github.com/digitalsamba/claude-code-video-toolkit)
- **OpenMontage** : configurations fournies pour Claude Code, Cursor, Copilot, Codex et Windsurf — [GitHub](https://github.com/calesthio/OpenMontage)
- **Blotato MCP** (source : marketing Blotato) :
  - Endpoint hébergé `https://mcp.blotato.com/mcp`, ajout par `claude mcp add --transport http Blotato https://mcp.blotato.com/mcp`.
  - 9 plateformes : X, LinkedIn, Facebook, Instagram, TikTok, YouTube, Threads, Bluesky, Pinterest.
  - Inclus dans les plans payants (29, 97 ou 499 $/mois). Pas d'API/MCP pendant l'essai.
  - [Blotato MCP](https://www.blotato.com/mcp) ; [Blotato Claude Code](https://www.blotato.com/ai-agent/claude-code)
- **Upload-Post MCP** : dépôt `Upload-Post/upload-post-mcp` listé dans un annuaire MCP — [claudemarket](https://www.claudemarket.ai/mcp/Upload-Post/upload-post-mcp/related-servers). Les « 40 outils » (publication, planification, analytics, commentaires, DM) sont une affirmation d'un concurrent (Blotato) — [Blotato blog](https://www.blotato.com/blog/postproxy-alternatives)
- **Postiz** : connecteurs agents MCP + CLI (Claude, ChatGPT, Codex, Cursor), MCP hébergé pour le cloud, MCP/CLI pointable vers une instance auto-hébergée — [README Postiz](https://github.com/gitroomhq/postiz-app)

### Inferences
- Pile Claude Code cohérente et peu chère : script et orchestration dans Claude Code, voix via le MCP ElevenLabs, montage via skills Remotion ou HyperFrames (ou rendu MoneyPrinterTurbo via son API), publication via le MCP Postiz auto-hébergé (gratuit, mais validation des apps à prévoir) ou via Upload-Post / Blotato (payants, apps pré-auditées).

### Gaps
- Nombre d'étoiles d'Upload-Post MCP non relevé.
- Existence et maturité d'un MCP Ayrshare non confirmées.

## 4. Planificateurs sociaux open source avec API (Postiz, Mixpost) et limites d'API TikTok, Instagram et YouTube, risques de ban

### Takeaway
**Postiz** (37,8k ★, AGPL, très actif, 14 plateformes, MCP, n8n, Make) est le choix open source de référence. **Mixpost** (3,9k ★, MIT) est moins actif (dernier push en mars 2026). Le vrai goulot n'est pas l'outil mais **l'approbation des API par les plateformes** : un client TikTok non audité ne peut publier qu'en privé. Côté YouTube, la politique de juillet 2025 sur le « contenu inauthentique » cible les chaînes faceless produites en masse.

### Cited Findings
- **Postiz** : 37 765 ★, 7 377 forks, 220 issues ouvertes, push le 24/10/2026, AGPL-3.0 — [GitHub](https://github.com/gitroomhq/postiz-app)
  - 14 plateformes : Instagram, YouTube, Dribbble, LinkedIn, Reddit, TikTok, Facebook, Pinterest, Threads, X, Slack, Discord, Mastodon, Bluesky.
  - Fonctions : API publique + webhooks, SDK Node, publication auto depuis un flux RSS.
  - Auto-hébergement : Docker, Coolify ou Railway, avec PostgreSQL, Redis et Temporal.
  - Le cloud fournit des apps pré-approuvées. En auto-hébergé, il faut créer ses propres apps développeur, et l'approbation « Meta, YouTube, TikTok can take weeks ».
- **Mixpost** : 3 864 ★, 582 forks, 35 issues ouvertes, dernier push le 16/03/2026, MIT. Se présente comme une « alternative à Buffer » auto-hébergée — [GitHub](https://github.com/inovector/mixpost)
- **TikTok (documentation officielle)** :
  - Tout contenu publié par un client non audité est limité à la visibilité privée. Il faut un audit de conformité pour lever cette restriction.
  - Une tentative de publication vers un compte public est bloquée avec l'erreur `unaudited_client_can_only_post_to_private_accounts`.
  - [TikTok Direct Post](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post) ; [Get started](https://developers.tiktok.com/doc/content-posting-api-get-started)
- **TikTok (sources secondaires, non confirmées par TikTok)** : la documentation Postiz évoque au plus 5 utilisateurs postant par 24 h pour les apps non auditées, avec `privacy_level` forcé à SELF_ONLY — [Postiz docs](https://docs.postiz.com/providers/tiktok.md). Une agence évoque un audit de 2 à 6 semaines et environ 15 posts par jour et par compte — [rapidevelopers](https://rapidevelopers.com/api-automations/how-to-automate-tiktok-video-posting-using-the-api)
- **Instagram (Meta, officiel)** : 50 conteneurs publiés par période glissante de 24 h, vérifiables via l'endpoint `content_publishing_limit` — [Meta](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit). Blotato annonce 100, en contradiction avec la source Meta — [Blotato](https://www.blotato.com/blog/social-media-api-rate-limits)
- **YouTube** : le coût de 1 600 unités par upload et le quota de 10 000 unités par jour n'ont **pas** pu être confirmés dans cette session. Blotato parle de 100 appels `videos.insert` par jour, et Metricool d'une limite « interne » — [Blotato](https://www.blotato.com/blog/social-media-api-rate-limits) ; [Metricool](https://help.metricool.com/daily-posting-limits-on-social-media-sh58j)
- **Risque de démonétisation ou de ban (YouTube)** :
  - Mise à jour du YPP appliquée depuis le 15/07/2025 contre le contenu « mass-produced and repetitious ».
  - L'application se fait au niveau de la chaîne : démonétisation, exclusion du YPP, voire suspension.
  - Le faceless n'est pas pénalisé automatiquement.
  - [Plagiarism Today](https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/) ; [Gulf News](https://gulfnews.com/technology/youtube-updates-monetisation-policies-ai-and-repetitive-content-ban-begins-july-15-1.500192660)
  - Une vague de janvier 2026 aurait supprimé 16 chaînes cumulant 35 M d'abonnés et 4,7 Md de vues (source secondaire) — [AIR Media-Tech](https://air.io/en/news-air/how-youtube-treats-ai-in-2026-new-update)

### Inferences
- Pour publier publiquement sur TikTok sans passer soi-même l'audit, il faut soit Postiz Cloud, soit un service pré-audité (Upload-Post, Blotato, Ayrshare). Postiz auto-hébergé reste « gratuit » mais suppose des semaines de validation des apps.
- Un pipeline 100 % automatique du sujet à la publication, à haut volume et sans variation éditoriale, est exactement le profil visé par la politique YouTube. Il faut prévoir une validation humaine, une voix ou personnalité distincte et des cadences modérées.

### Gaps
- Quotas officiels de l'API YouTube Data non revérifiés.
- Pas de témoignages Reddit chiffrés sur des bans liés aux outils d'automatisation.

## 5. Benchmark SaaS (pour comparaison uniquement) et API de publication payantes

### Takeaway
Les SaaS de clipping (Opus Clip, Submagic, Vizard) coûtent environ 12 à 20 $/mois et partent d'une vidéo longue, alors que la cible ici est la création ex nihilo. Côté publication, **Upload-Post** (formule gratuite, puis 16 à 24 $/mois) est nettement moins cher qu'**Ayrshare** (à partir de 149 $/mois). **Blotato** (29 à 499 $/mois) combine création et publication.

### Cited Findings
- **OpusClip** : environ 15 $/mois pour 150 min, formule gratuite de 60 min/mois, crédits à la minute de source (blog comparatif, pas de page tarifaire officielle) — [Castmagic](https://www.castmagic.io/blog/opus-clip-alternatives)
- **Submagic** : environ 12 $/mois en annuel, plus un module de clipping à 12 $/mois. Note Trustpilot 4,8/5 **autodéclarée** par Submagic — [Castmagic](https://www.castmagic.io/blog/opus-clip-alternatives) ; [Submagic](https://www.submagic.co/vs/vizard-vs-opus-pro)
- **Vizard** : formule gratuite de 60 min/mois en 720p avec filigrane, Capterra 4,9 (446 avis). Les prix payants cités (14,50 et 19,50 $) proviennent d'un concurrent — [Submagic](https://www.submagic.co/vs/vizard-vs-opus-pro) ; [Capterra](https://www.capterra.com/p/10009489/submagic/)
- **Upload-Post** : formule gratuite de 10 uploads/mois (sans TikTok), plans payants à partir de 24 $/mois (16 $ en annuel), posts illimités, API incluse. 12 plateformes : TikTok, IG, YT, LinkedIn, FB, X, Threads, Pinterest, Reddit, Bluesky, Discord, Telegram. Source : éditeur — [Upload-Post](https://www.upload-post.com/pricing-comparison)
- **Ayrshare** : à partir de 149 $/mois pour un profil, module Max Pack à 300 $/mois, 13 réseaux dont Snapchat et Google Business — [Upload-Post comparison](https://www.upload-post.com/pricing-comparison) ; [Ayrshare](https://www.ayrshare.com/compare/upload-post-api-alternative/)
- **Blotato** : 29, 97 ou 499 $/mois, essai de 7 jours sans API. App TikTok pré-auditée, donc posts publics dès le premier appel (affirmation de l'éditeur) — [Blotato TikTok API](https://www.blotato.com/api/tiktok) ; [Blotato MCP](https://www.blotato.com/mcp)
- Alternative open source à Opus Clip : Anil-matcha/AI-Youtube-Shorts-Generator (5,6k ★), qui combine détection des moments forts par LLM, Whisper et recadrage vertical — [GitHub](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator)

### Inferences
- Toutes les comparaisons de prix trouvées sont **rédigées par des concurrents** (Upload-Post contre Blotato, Ayrshare contre Upload-Post). Il faut revérifier sur les pages tarifaires officielles avant de décider.

### Gaps
- Revid et Faceless.video : aucune donnée trouvée (prix, avis).
- Notes Trustpilot et G2 indépendantes non relevées.

## 6. Systèmes de génération de contenu texte (blog, LinkedIn, newsletter) indépendants de la niche

### Takeaway
Ce volet a été **peu couvert** dans cette session (budget d'appels atteint). Les seuls éléments vérifiés sont les briques de publication texte multiplateformes : Postiz avec publication auto depuis RSS, IA Copilot, LinkedIn, X, Threads, Bluesky, Mastodon, et Blotato/Upload-Post, qui couvrent LinkedIn et X.

### Cited Findings
- Postiz publie automatiquement depuis un flux RSS et intègre un AI Copilot et un « Smart Agent ». Il gère LinkedIn, X, Threads, Bluesky, Mastodon et Reddit — [README Postiz](https://github.com/gitroomhq/postiz-app)
- Blotato vend un « Repurpose Engine » et des Claude Skills (« Top 100 Viral Hooks ») pour décliner un contenu vers plusieurs réseaux. C'est du marketing éditeur, sans traction vérifiée — [Blotato](https://www.blotato.com/blog/claude-routines-social-media)
- Blotato annonce aussi la publication de carrousels Instagram et de diaporamas TikTok via n8n — [Blotato blog](https://www.blotato.com/blog/category/ai-automation)

### Inferences
- Schéma simple et indépendant de la niche : un agent (Claude Code ou n8n) rédige le blog, l'article est publié avec un flux RSS, puis Postiz republie automatiquement sur LinkedIn et X. On évite ainsi tout SaaS de rédaction.

### Gaps
- Dépôts open source de rédaction multicanal (gpt-researcher, STORM, générateurs de posts LinkedIn) non vérifiés : la recherche GitHub n'a rien renvoyé avec les requêtes tentées.
- Modèles n8n de newsletter ou de blog et leurs compteurs non relevés.
