# BRIEF — Reel « histoire » : le site Reflex IA tourne sur GitHub + Cloudflare + Astro (v2)
# Skill : reel-histoire (appmee, branche claude/skill-reel-histoire). Source : le dépôt Reflex IA lui-même (code, `.claude/CLAUDE.md`, build local du 27/11/2026) + ce que Hari dit. Plus aucune source tierce.
# Statut : EN ATTENTE D'ACCORD. Rien n'est produit : ni voix, ni rendu, ni son.

> **Mise à jour du 27/11/2026 (v3)** : le reel a évolué après les retours de Hari (intro sur Reflex IA, stack minimum en couches, une page de chaque type en défilement lent avec swipe, comparaison avec les solutions classiques) ; la source de vérité est désormais **SCRIPT.md** (texte lu, mise en scène, statuts, limites). Le schéma ci-dessous est la version initiale.

## 1. Couverture
`out/couverture.png` : **« REFLEX·IA » en haut, centré** · **une seule grande fenêtre ordinateur qui remplit presque tout le cadre en hauteur** (le vrai site, charte actuelle) · « Mon site tourne à **0 €** » en bandeau · pastille « GitHub + Cloudflare + Astro » · ligne « UNE CHARTE CHANGE, TOUT LE SITE SUIT · HORS DOMAINE ET ABONNEMENT CLAUDE ».
**Retours de Hari intégrés** : interfaces mobiles jugées moches → **pages en version ordinateur, en pleine page** (accueil, article, comparatif, page de vente, formulaire newsletter) ; « REFLEX·IA » **en haut au milieu** (couverture, et repère fixe pendant tout le reel) ; **les pages doivent prendre quasiment toute la hauteur du cadre** (fenêtre ≈ 960 × 1 500 px sur 1 080 × 1 920, cadre minimal) ; **beaucoup de mouvement** : zoom/dézoom, apparitions, glissements, **effet Prezi**.

## 2. Angle (dicté par Hari)
> Mon système est le plus simple : GitHub, Cloudflare, Astro. La mise en ligne me coûte 0 €. Je change la charte graphique une fois, et tout le site suit. Et je n'ai pas tapé une ligne de code : Claude Code l'écrit.

**Forme (dernière consigne de Hari) : « juste un défilement des différents types de pages », et à la fin « commente *site* » : il envoie le système IA pour le répliquer « à sa sauce ».** Ouverture = le vrai site avec un fort zoom avant, jamais un titre statique.

## 3. Schéma (≈ 50–55 s, plafond 90 s)
**Principe de montage : une seule grande toile, une caméra qui la parcourt (effet Prezi).** Les pages (version ordinateur, pleine page) sont posées sur la toile ; la caméra zoome, dézoome, glisse de l'une à l'autre. Rien ne reste fixe plus d'une seconde : chaque scène enchaîne au moins un zoom ou un glissement, plus des apparitions (étiquettes, pastilles, logos) qui se posent sur la page. « REFLEX·IA » reste en haut au centre.

| Scène | Ce qu'on voit et le mouvement (aucun écran vide) | Source |
|---|---|---|
| 1. Ouverture (≈ 7 s) | la vraie page d'accueil (ordinateur) : **zoom avant fort** sur le titre, puis **dézoom** qui révèle toute la page ; la voix dit que la mise en ligne coûte 0 € | dépôt ; 0 € = dit de Hari, étayé pour Cloudflare (§4) |
| 2. Les 3 pièces (≈ 11 s) | la toile glisse vers 3 logos qui **apparaissent** l'un après l'autre : GitHub (garde le site) → Cloudflare (le met en ligne tout seul) → Astro (fabrique les pages) ; flèche animée entre eux | `CLAUDE.md` (« push sur main = déploiement automatique »), `package.json` (Astro) |
| 3. Défilement des pages (≈ 18 s) | **travelling Prezi** : accueil → article → comparatif → page de vente (**maquette**) → inscription newsletter (fenêtre) ; chaque page est défilée de haut en bas pleine page, avec son étiquette qui se pose ; compteur « 132 articles » | dépôt : `src/pages/`, `src/content/blog` (132 fichiers) |
| 4. La charte change (≈ 10 s) | **dézoom** sur les 4 pages côte à côte, puis **les couleurs basculent** sur toutes en même temps (3 chartes de suite), avec un zoom sur le formulaire et la page de vente | build de démonstration, §5 |
| 5. Pas de code (≈ 5 s) | zoom sur « Claude Code l'écrit » ; ligne « hors nom de domaine et abonnement Claude » qui glisse | dit de Hari ; exclusions : évidence |
| 6. Appel (≈ 7 s) | dézoom final sur toutes les pages, « Commente **site** » en grand | dit de Hari |

## 4. Ce que le dépôt établit, ce qu'apporte Hari
| Idée | Source ? | Traitement |
|---|---|---|
| Site statique Astro, déployé sur Cloudflare Pages à chaque push sur `main`, code sur GitHub | oui (`package.json`, `astro.config.mjs`, `.claude/CLAUDE.md`) | dit tel quel |
| Formulaire newsletter = une fonction Cloudflare qui écrit chez MailerLite | oui (`functions/api/subscribe.js`) | montré, pas détaillé |
| « 132 articles » | oui (132 fichiers dans `src/content/blog`, mesuré le 27/11/2026) | à l'écran seulement |
| « La mise en ligne me coûte 0 € » | **dit par Hari** ; Cloudflare Pages : offre gratuite confirmée dans la doc Cloudflare consultée le 27/11/2026 (500 mises en ligne/mois, 20 000 fichiers/site, pages statiques gratuites et illimitées ; ce site : 229 fichiers au build local) ; **GitHub : non vérifié ici** | « mise en ligne = 0 € » ; **nom de domaine et abonnement Claude affichés comme hors périmètre** |
| « Pas de serveur à gérer » | oui (site statique ; Cloudflare héberge) | dit ainsi, pas « sans hébergeur » (Cloudflare EST l'hébergeur) |
| « Je n'ai pas tapé une ligne de code, Claude Code l'écrit » | **dit par Hari**, rien ne le prouve dans le dépôt | signalé `[À CONFIRMER]` ; formulé à la 1re personne |
| « Une seule charte change tout le site » | **rendu réel** (§5) | montré ; précisé « build de démonstration » |
| « Tunnel de vente » | la page AI Factory est une **maquette** (paiement non branché) | dit « page de vente en maquette » |
| « Le système IA que j'envoie » | promesse de Hari ; **je ne sais pas quel fichier c'est** | dit comme sa promesse ; à confirmer |

## 5. La preuve « une charte, tout le site » (faite, captures dans `assets/charte-pc/`)
- Méthode : copie du site (`git archive`), **une seule table de correspondance de 11 couleurs** appliquée à 15 fichiers, build Astro, captures Playwright **en version ordinateur** (1 280 px de large, pleine page ; l'article et le comparatif sont coupés à leurs 4 200 et 4 800 premiers pixels de hauteur CSS). Deux chartes de démonstration (« océan » bleu, « forêt » vert) + la charte actuelle ; **rien n'est publié**.
- **Résultat vu sur les captures** : accueil, article, comparatif, page de vente (maquette) et formulaire newsletter changent tous ; la page contact est quasi neutre (peu de couleur). Sur les **variables globales seules** (`global.css`), peu de choses bougeaient : des couleurs sont aussi écrites en dur dans les pages. **Donc « une charte, tout le site » demande une vraie opération sur le code, que je fais ici par script, pas par Claude Code** : « Claude Code l'écrit » reste le dit de Hari.
- Pas de promesse sur la qualité du résultat (goût).

## 6. Ce que la vidéo n'affirmera pas
- Aucune donnée d'audience, de vitesse, de gain de temps ou de rang. Aucun prix autre que « 0 € de mise en ligne ».
- Rien sur les offres de GitHub (non vérifiées). Rien sur la durée d'une mise en ligne.
- « Simple à répéter » n'est pas affirmé comme un fait mesuré : il est porté par la promesse d'envoyer le système.
- Chartes alternatives = builds de démonstration, pas des versions du site.

## 7. Durée, coût, ton
≈ 12 phrases de voix facturées (Gemini TTS lite, Charon) ; ≈ 50–55 s ; rendu local ; aucune image générée (captures réelles) ; « tu » au spectateur, « je » = Hari.

## Décisions à trancher
1. **Fin** : « Commente *site* et je t'envoie le système IA pour le répliquer à ta sauce » remplace le « Abonne-toi pour plus d'astuces… » des reels précédents. OK, ou on garde les deux ?
2. **0 €** : « la mise en ligne me coûte zéro euro » dit à la voix, exclusions (domaine, abonnement Claude) affichées à l'écran. OK ?
3. **Le système à envoyer** : quel est-il (le skill, le playbook, un dossier) ? Je ne le nomme pas dans la vidéo.
