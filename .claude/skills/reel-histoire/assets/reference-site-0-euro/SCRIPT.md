# SCRIPT — Reel « Mon site tourne à 0 € » (v9) — GitHub + Cloudflare + Astro
Skill : reel-histoire (appmee, branche `claude/skill-reel-histoire`). Source : le dépôt Reflex IA lui-même + ce que Hari dit. Aucune source tierce.
Fichier principal : `out/reel-mon-site-0-euro.mp4`, rangé aussi sous `CONTENT/REELS_INSTAGRAM/reel-instagram-reflexia-6.mp4` (une seule version) · **sans musique** (voix + petits bruitages synchronisés ; Hari ajoute sa musique sur Instagram) · 1080×1920 · 30 i/s · **71,6 s** · −14,1 LUFS · aucune image figée · aucun texte qui en chevauche un autre.
Voix : Gemini TTS, voix Charon, **modèle `gemini-3.8-flash-tts`** (le modèle « lite » des reels précédents a atteint son plafond de 100 requêtes par jour) ; **elle diffère légèrement de celle des reels précédents.**
**Débit plus rapide (dernier retour de Hari)** : voix accélérée de **16 %** (`tempo` 1,16, hauteur conservée ; 10 % à la version précédente), silences entre phrases réduits à 0,08 s (0,14 s avant), maintiens des pages raccourcis (1,6 à 2,6 s). Le texte garde le ton « copain » de la version précédente. Une consigne de style dans la requête de voix a été essayée et abandonnée (lue à voix haute ou durée doublée).

## Texte lu (mot pour mot) — ordre : ouverture → solutions classiques → stack minimum → Claude Code → pages → charte → tous les articles → appel
**Ouverture**
1. Voilà mon site, Reflex IA, pour trouver les meilleurs outils et systèmes IA !
2. Les plus simples, les plus fiables, les plus efficaces, avec leurs vraies limites, pour ton besoin !
3. Et en plus, sa mise en ligne me coûte zéro euro !

**Face aux solutions classiques (v8 : une seule phrase)**
4. Il existe plein d'autres moyens de faire un site, mais là, on va bien plus vite ! *(« plus vite » = dit de Hari, non mesuré ici)*

**Le stack minimum, puis le rôle de chaque outil**
5. Mon système, c'est le stack minimum !
6. GitHub, il héberge le code du site.
7. Cloudflare gère les évolutions : je change un truc, et c'est en ligne, tout seul !
8. Et Astro crée les pages, à partir de mes articles !

**Claude Code pilote le tout, en langage naturel (v8)**
9. Et tout ça, c'est Claude Code qui le pilote : je lui parle normalement, j'ai pas tapé une ligne de code ! *(dit de Hari)*

**Les pages obtenues (défilement lent, swipe d'une fenêtre à l'autre)**
12. Et voilà ce qu'on obtient : la page d'accueil ! 13. Les articles. 14. Les comparatifs. 15. Les rubriques.
16. La page de vente !
17. Et le formulaire de la newsletter !

**Tout en une fois**
18. Je change la charte graphique ? Une seule fois !
19. Et toutes les pages suivent, d'un seul coup !
20. Et si je veux optimiser tous les articles ?
21. Une seule demande, et tout se fait en une fois !
22. Et rien ne casse : le site se vérifie tout seul avant d'être mis en ligne.

**Appel**
23. Tu veux le même système ? Commente « site », et je te l'envoie pour le répliquer à ta sauce !

Écran seulement (non lu) : « hors nom de domaine et abonnement Claude » · « 132 articles dans le dépôt » · « démo « océan » / « forêt » : build de démonstration » · « 0 ligne de code tapée » · « illustration : une seule demande » · « Optimise tous les articles » · « 132 articles » · « Liens vérifiés / Champs vérifiés / Build vert ».

## v9 — ouverture refaite (retours de Hari du 27/11) : on voit les comparatifs par type d'outils, puis un article
- **Texte, voix, durée inchangés** (71,6 s) ; seule la mise en scène des ~11 premières secondes change. Le clic sur la puce « Limites à savoir » est retiré (la phrase « vraies limites » reste dite et affichée en sous-titre).
- **Nouvelle séquence** : accueil (zoom sur le titre) → clic sur « Comparatifs » → clic sur le filtre « Image & vidéo » (les comparatifs de ce type d'outils s'affichent) → la carte « HeyGen ou ElevenLabs » ressort vers l'avant, zoom lisible → clic sur le filtre « Automatisation & agents » → clic sur la carte « Combien coûte OpenClaw ? » qui ressort → plongée dans l'article.
- Ce que fait ressortir l'écran : les **cartes de comparatifs** (pas les petits filtres ni le menu). Captures réelles du site (build local du 27/11/2026) : `assets/pc3/comparatifs-f0|f1|f2.jpg` (aucun filtre / Image & vidéo / Automatisation & agents), positions dans `assets/pc3/pages-f.json`. Le clic sur un filtre est un vrai clic fait à la capture ; le curseur et le montage sont de la mise en scène.
- Contrôles v9 : `qa.cjs` vert · chevauchements 0 sur 716 instants · 71,6 s · −14,2 LUFS · freezedetect 0.

## v8 — retours de Hari du 27/11 (ouverture lisible, scène raccourcie, terminal Claude Code)
- **Ouverture** : les étiquettes étaient passées *sous* le voile blanc de la page (d'où l'aspect flou) ; elles sont maintenant au-dessus, le voile est plus net sous la bande de texte et le sous-titre est plus gros et plus foncé.
- **« Rien à ouvrir… » raccourci** : trois phrases → une (« Il existe plein d'autres moyens… on va bien plus vite ! ») ; à l'écran, les solutions classiques se posent vite à gauche, une carte verte « Plus rapide avec mon système » à droite. La liste « pas de serveur, pas d'extension… » est retirée.
- **Stack minimum** : « Mon système, c'est le stack minimum ! » puis directement le rôle de chaque outil (inchangé), puis Claude Code.
- **Claude Code** : le décor de barres colorées abstraites est remplacé par un terminal lisible : une instruction en langage naturel tapée (« Passe la charte du site en bleu océan, et mets-le en ligne »), trois lignes de réponse cochées, puis « 0 ligne de code tapée ». **Illustration (mot affiché à l'écran), pas un enregistrement de Claude Code** : l'instruction et les réponses sont un exemple de mise en scène.
- Contrôles v8 : `qa.cjs` vert · chevauchements 0 sur 716 instants · 1080×1920 / 30 i/s / 71,6 s · −14,2 LUFS · freezedetect 0 · transcription 0,993 · voix : 3 phrases nouvelles facturées (v1, s1, n1), le reste en cache.

## v7 — démo « souris » plein cadre (dernier retour de Hari)
Retour : « Je valide le langage, le ton, le rythme verbal. Par contre reviens sur enchaînement et séquence précédente, avec comme même effet : effet de clic avec la souris, zoom et dézoom, scroll. »
- **Inchangés** : texte lu (23 phrases, mot pour mot, cache de voix : 0 requête facturée), ton, rythme (tempo 1,16, silences 0,08 s), ordre des scènes (ouverture → solutions classiques → stack minimum → Claude Code → pages → charte → tous les articles → CTA), fonds actuels, « REFLEX·IA » en haut au milieu, aucun texte au-dessus d'un autre.
- **Changé** : les scènes `ouverture`, `pages` et `charte` n'ont plus de fenêtres encadrées. Ce sont de **vraies pages du site en version ordinateur, plein cadre**, avec **curseur de souris, ondes de clic, défilement lent, zoom/dézoom et swipes**. **Aucun cadre jaune** : l'élément cliqué **ressort vers l'avant** (calque soulevé avec ombre, reste de la page voilé), la caméra zoome pour qu'on lise, puis dézoome.
- **Ouverture** : accueil plein cadre, zoom sur le titre, clic sur la puce « Limites à savoir » (elle ressort), dézoom.
- **Pages** : navigation continue, un clic par phrase : accueil → menu « Comparatifs »/« Guides » → carte d'article → comparatif → rubrique systèmes (page de vente, voir limites) → bouton « Newsletter gratuite » qui ressort, puis le bloc newsletter.
- **Charte** : l'accueil plein cadre change de charte en balayage (océan puis forêt), puis swipes vers article, page de vente et formulaire. Les chartes alternatives sont des **builds de démonstration**, pas des versions du site.
- Captures : Playwright, pages entières en 1 280 px (échelle 1,5), positions des liens/cartes relevées sur les vraies pages (`assets/pc3/pages.json`). **Curseur, clics et swipes sont de la mise en scène** posée sur ces captures, pas un enregistrement d'écran.
- Contrôles v7 : `qa.cjs` vert · chevauchements 0 (balayage tous les 0,1 s) · 1080×1920 / 30 i/s / 71,6 s · −14,1 LUFS · freezedetect 0 · transcription 0,984.

## Retouches v6 (dernier retour de Hari)
- **CTA** : « Tu veux le même système ? Commente « site », et je te l'envoie pour le répliquer à ta sauce ! » (écran : « Commente « site » », « Tu veux le même système ? »).
- **« Maquette » retiré** : la voix dit « La page de vente ! » ; l'étiquette dit « Page de vente » ; la surbrillance jaune du bandeau « Maquette » est supprimée. **Rappel honnête** : la page `/systemes/` reste une **maquette sans paiement branché** (la capture réelle montre encore son bandeau « Maquette. Prix, vidéos et paiement simulés. ») ; la vidéo ne dit nulle part que la page encaisse. Hari a levé la consigne « dire que c'est une maquette ».
- **Musique** : fichier principal **sans nappe** (Hari la rajoute) ; variante avec nappe réduite de moitié. Pas de « musique tendance » générée : le moteur de bruitage est du JavaScript synthétique, sans droits musicaux vérifiés.
- Un mouvement léger a été ajouté en fin de scène « tous les articles » (cartes qui flottent, compteur qui bat) pour supprimer une image figée de 1,4 s.

## Mise en scène (retours de Hari appliqués ; ouverture, pages et charte : voir v7 ci-dessus, qui remplace les fenêtres encadrées)
- Ouverture : **le vrai site** (accueil, version ordinateur), **zoom avant fort** sur le titre, puis sur la table de comparaison et sur l'étiquette « Limites à savoir » de la vraie page d'accueil (liée à « leurs vraies limites »), puis dézoom. « REFLEX·IA » **en haut, au milieu**, sur toute la vidéo.
- **Stack minimum** (représentation en couches) : GitHub, Cloudflare, Astro s'empilent de bas en haut ; au moment où Astro « crée les pages », **six pages réelles** (accueil, article, comparatif, rubrique, page de vente, formulaire) se posent dans le cadre d'un site.
- **Une page de chaque type** : une fenêtre par type (accueil, articles, comparatifs, rubriques, page de vente en maquette, formulaire newsletter), **défilement lent** (230 unités/s), **swipe** horizontal pour passer à la fenêtre suivante ; pages réelles, version ordinateur, pleine page.
- **Comparaison** : **à gauche** les solutions classiques apparaissent une à une ; **à droite** ce dont je n'ai pas besoin (cartes vertes) ; la colonne de gauche s'estompe quand la droite prend la parole.
- **Tous les articles en une seule demande** (nouvelle scène) : une demande « Optimise tous les articles » se tape dans une bulle, puis **une grille de cartes d'articles passe au vert en vague**, un compteur « 132 articles » apparaît, puis trois contrôles (« liens vérifiés », « champs vérifiés », « build vert »). **C'est un schéma, annoncé « illustration » à l'écran : ce n'est pas l'enregistrement d'une vraie opération** (l'historique git de ce dépôt, tronqué au 15/09/2026, ne contient pas de lot d'articles modifié d'un coup à citer). Seuls les trois contrôles reposent sur du réel (voir « Sources »).
- **Aucun texte au-dessus d'un autre** : étiquette unique dans la bande du haut (l'ancienne sort par le haut avant que la suivante monte du bas) ; scènes enchaînées par **poussée verticale** ; règle vérifiée par `qa.cjs` et par un balayage toutes les 0,1 s.

## Sources et statuts
| Élément | Statut | Source |
|---|---|---|
| Site statique Astro ; code sur GitHub ; mise en ligne automatique sur Cloudflare Pages à chaque push sur `main` | **établi** | `package.json` (`astro ^4.16`), `astro.config.mjs` (`output: 'static'`), `.claude/CLAUDE.md` (« push sur main = déploiement automatique ») |
| « GitHub héberge le code du site » | établi **sous cette forme** : Hari a dit « hébergeur du site : GitHub » ; la vidéo dit « héberge le code », car c'est Cloudflare Pages qui sert le site (GitHub Pages n'est pas utilisé) | dépôt, `CLAUDE.md` |
| « Cloudflare gère les évolutions : chaque changement est mis en ligne » | établi | `CLAUDE.md` (déploiement automatique) |
| « Astro crée les pages à partir de mes articles » | établi | 132 fichiers Markdown dans `src/content/blog`, `src/pages/blog/[slug].astro` |
| Types de pages montrés (accueil, article, comparatif, rubrique, page de vente, formulaire) | établi | `src/pages/` (`index`, `blog/[slug]`, `[categorie]`, `systemes`), `NewsletterPopup.astro` ; le « comparatif » montré est un article de format « guide » |
| Formulaire newsletter = fonction Cloudflare → MailerLite | établi (montré, non détaillé) | `functions/api/subscribe.js` |
| « 132 articles » | **mesuré** 27/11/2026 | 132 fichiers dans `src/content/blog` |
| Page de vente = **maquette** | établi | `/systemes/` : « Maquette. Prix, vidéos et paiement simulés. », `CartDrawer` : « le paiement n'est pas encore branché » ; page `noindex` |
| « Les meilleurs outils et systèmes IA, les plus simples, fiables et efficaces, avec leurs vraies limites » | **promesse de Hari** pour son site, non mesurée ici ; l'étiquette « Limites à savoir » existe bien sur la page d'accueil | Hari |
| « La mise en ligne me coûte zéro euro » | **dit par Hari** ; **Cloudflare Pages vérifié** dans la documentation Cloudflare (27/11/2026) : offre gratuite, 500 mises en ligne par mois, 20 000 fichiers par site (ce site : 229 fichiers au build local), requêtes de pages statiques gratuites et illimitées, fonctions (le formulaire) sur le quota gratuit des Workers (100 000 requêtes par jour) ; **offre gratuite de GitHub : non vérifiée ici** | doc Cloudflare + Hari |
| « Pas de serveur à gérer » | établi (site statique ; Cloudflare héberge) | `astro.config.mjs` |
| « Pas d'extensions à mettre à jour » | établi **au sens CMS** : aucune extension de gestionnaire de contenu ; le projet a seulement 3 dépendances npm (`astro`, `@astrojs/sitemap`, `remark-heading-id`) qui, elles, se mettent à jour | `package.json` |
| « Pas d'hébergement à payer » | **dit par Hari** (0 €), voir ligne « zéro euro » ; hors nom de domaine | Hari |
| « Je n'ai rien à ouvrir, ni à manipuler » ; « je n'ai pas tapé une ligne de code ; c'est Claude Code qui l'écrit » | **dits par Hari**, aucune preuve dans le dépôt | Hari |
| « Une charte, une seule fois ; toutes les pages suivent » | **rendu réel**, mais obtenu par un script (voir ci-dessous), pas par Claude Code | build de démonstration |
| « Rien ne casse : le site se vérifie tout seul avant d'être mis en ligne » | **dit par Hari** (« sans que rien ne casse ») ; la **vérification automatique est réelle** : `npm run build` lance `scripts/check-internal-links.mjs` (liens internes morts, routes inventées, champs `format`/`usage`/`outils`, titres trop longs, doublons d'outils à 80 %) et **échoue sans mise en ligne** si un contrôle échoue (règle de `CLAUDE.md`) ; cela **réduit** le risque de casse, **ne le supprime pas** | `.claude/CLAUDE.md`, `scripts/check-internal-links.mjs` |
| « Tous les articles optimisés en une seule demande » | **parole de Hari**, jamais montrée en vrai ici ; illustration schématique ; aucun résultat, aucune durée, aucun gain annoncé | Hari |
| Colonne de gauche : page statique à la main, Wix, WordPress, « d'autres, même avec de l'IA » | **simples noms** de solutions ; « Wix » est ma lecture de « Mix » dans la dictée de Hari ; **aucune affirmation sur leurs défauts ni leurs prix** : la colonne de droite décrit seulement ce que Hari n'a pas à faire chez lui | Hari |
| « Le système IA que j'envoie » | **promesse de Hari** ; je ne sais pas quel fichier c'est (skill, playbook, dossier) ; non nommé dans la vidéo | Hari |

## La preuve « une charte, tout le site » : ce qu'elle montre et ne montre pas
- Copie du site (`git archive HEAD`), **une seule table de correspondance de 11 couleurs** appliquée à 15 fichiers (couleurs et ombres teintées), build Astro, captures Playwright en 1 280 px de large. Deux chartes de démonstration (« océan », « forêt ») + la charte actuelle ; **rien n'est publié**.
- Sur les **seules variables globales** de `global.css`, très peu de chose bougeait : de nombreuses couleurs sont écrites en dur dans les pages (ex. `index.astro`). L'effet « tout le site » vient donc d'un **remplacement dans tout le code**, que j'ai fait par script ; la vidéo ne prétend pas que Claude Code l'ait fait (c'est Hari qui le dit, phrase 11).
- Accueil, article, comparatif, page de vente (maquette) et formulaire newsletter changent ; la page contact change à peine (peu de couleur). Aucune promesse de qualité visuelle (goût).

## Limites (dites à Hari)
- **0 €** = mise en ligne / hébergement. Nom de domaine et abonnement Claude **ne sont pas gratuits** : affichés à l'écran. Offre GitHub non vérifiée ; l'offre Cloudflare est celle de la doc du 27/11/2026 (peut changer).
- **Comparaison avec les solutions classiques** : la vidéo ne dit rien de précis sur Wix, WordPress ou les outils avec IA ; elle les nomme à gauche, et dit à droite ce que Hari n'a pas à faire. Aucun test, aucun prix, aucune donnée sur ces outils.
- **Scène « tous les articles »** : schéma, pas une démonstration. Rien n'est affirmé sur le nombre d'articles réellement modifiés, ni sur la fiabilité d'une modification de masse ; « rien ne casse » est dit par Hari et appuyé seulement par les contrôles du build (qui peuvent échouer).
- Pas de donnée d'audience, de vitesse ou de gain de temps ; aucun prix autre que « 0 € ».
- « Sans code », « rien à ouvrir ni à manipuler », « meilleurs, simples, fiables, efficaces » et « le système IA » sont des paroles de Hari, non prouvées ici.
- « Reflex IA » : la voix prononce « Reflex » à la française (« réflexe »), ce qui est l'usage ; la transcription du mixage l'a écrit « Réflexe IA » (même prononciation).
- Phrase 11 (ancienne phrase « Claude Code l'écrit ») : plusieurs reformulations successives (« c'est Claude Code qui l'écrit », puis « qui écrit tout ») avaient été comprises à tort au passé (« l'a écrit ») par la transcription ; la version retenue (« Claude Code, il s'en charge sur mes instructions ») est comprise correctement dans le mixage final. Phrase 19 : « Et hop, toutes les pages suivent » était comprise « tout de suite » ; reformulée (« Et toutes les pages suivent, d'un seul coup »).
- Durée : 71,6 s, sous le plafond de 90 s ; durées de maintien (« hold ») dans `story.json` pour laisser défiler chaque page.
- Son non écouté par moi ; rendu non vu sur téléphone (vérifié par planches de contact et images isolées).
- La fin « Commente site » **remplace** le « Abonne-toi pour plus d'astuces IA… » des reels précédents (hypothèse retenue : décision non tranchée explicitement par Hari).
- Captures : article et comparatif coupés à leurs 4 200 / 4 800 premiers pixels de hauteur CSS, rubrique à 3 200 (poids).

## Contrôles passés
`qa.cjs` vert (plusieurs dizaines d'instants : nombres autorisés `0` et `132`, zones sûres, texte déclaré, CTA « Commente ») · chevauchements : 0 sur 761 instants · ffprobe 1080×1920 / 30 i/s / 71,6 s · −14,1 LUFS · freezedetect (n=0,0008, d=1,2 s) : 0 · transcription du mixage final comparée par mots : **0,988**.

## Pipeline (depuis ce dossier, `GOOGLE_API_KEY` en variable d'environnement, jamais affichée)
`python3 -I tts.py $W` → `python3 -I plan.py` → `node events.cjs` → `node qa.cjs` → `node synth.cjs $W` → `node render.cjs --out out/reel-muet.mp4 --frames $W/frames --workers 4` → `python3 -I mix.py $W out/reel-muet.mp4 out/reel-mon-site-0-euro.mp4`
Captures : `assets/charte-pc/` (3 chartes × accueil, article, comparatif, page de vente, newsletter ; + rubrique en charte actuelle). Couverture : `cover.html` → `node cover.cjs`.
`story.json` accepte un champ `hold` (durée mini d'une phrase à l'image) lu par `plan.py`.
