# L04 — Guide d'intégration du site NOVOLENS V3

Pour qui : la personne qui remplace les photos et les données, branche le formulaire et met le site en ligne. Tous les chemins sont relatifs à `missions/2026-11-16-site-novolens-agence/livrables/`. Le contenu à valider est listé dans `L03-contenu.md`.

## a) Structure des dossiers et reconstruction

```
livrables/
├── site/                  sortie générée (ne jamais la modifier à la main)
│   ├── index.html, pourquoi-nous.html, comment-ca-marche.html, resultats.html,
│   │   cas-client.html, tarifs.html, faq.html, contact.html, 404.html
│   ├── style.css, app.js, robots.txt, sitemap.xml
│   └── img/               12 photos JPEG
├── site-src/              sources
│   ├── build.py           assemble les pages, le pied de page, la FAQ, le formulaire
│   ├── story.py           parcours en 4 ou 5 étapes (textes + animations SVG)
│   ├── ucards.py          les 4 encarts « action et moyen »
│   ├── v3_extra.py        cas client, page 404, sitemap, robots, design system
│   ├── style.css, style_v2.css, style_v3.css   feuilles concaténées dans site/style.css
│   ├── app.js             animations, hero, formulaire, simulateur
│   └── img/               photos sources (copiées dans site/img)
├── audit/audit.js         audit automatique
├── L02-design-system.html, L03-contenu.md, L04-guide.md, L05-rapport-audit.md
```

Reconstruire :

```bash
cd livrables/site-src
V2=1 V3=1 python3 build.py     # écrit dans livrables/site
```

| Point | Détail |
|---|---|
| Prérequis | Python 3 et Pillow (`pip install pillow`) ; Pillow lit la taille des images pour écrire `width` et `height` |
| Les deux variables | `V2=1` active les photos et le style des cartes, `V3=1` active la version finale (cas client, 404, sitemap, robots) ; sans les deux, le rendu est incomplet |
| Le dossier `site/` est effacé | `build.py` supprime puis recrée `site/` à chaque exécution : tout fichier ajouté à la main dans `site/` disparaît. Mettre les fichiers à ajouter dans `site-src/` et les copier depuis `build.py` (exemple en section e) |
| Effet de bord | La reconstruction réécrit aussi `L02-design-system.html` |
| Vérifier | La dernière ligne affichée est `ok [...]` avec la liste des fichiers ; ouvrir `site/index.html` dans un navigateur |
| Règle d'or | On modifie `site-src/`, on reconstruit, on relance l'audit (section h) |

## b) Remplacer les photos

Remplacer le fichier dans `site-src/img/` en gardant le même nom, puis reconstruire. Ne pas écrire dans `site/img/` (effacé à la reconstruction).

| Fichier | Taille actuelle | Où il apparaît | Où changer le texte alternatif |
|---|---|---|---|
| `hero-bg.jpg` | 2000 × 1125, 197 Ko | Photo du hero de l'accueil, en fond (cadrage 78 % / 35 %, voile blanc dégradé à gauche pour lire le texte). Préchargée dans `<head>` | `build.py` · `build_index()`, attribut `aria-label` du `div.hero-bg` |
| `cta-bg.jpg` | 1600 × 900, 198 Ko | Bandeau d'appel à l'action en bas de chaque page (à 60 % d'opacité, fondu vers la gauche) et photo de l'en-tête de Résultats | décoratif ; en-tête : `aria-label` dans `v2body()` |
| `card-1.jpg` | 1100 × 825, 152 Ko | Encart 1 « Calibrage » ; en-tête de Pourquoi nous | décoratif (`aria-hidden`) |
| `card-2.jpg` | 1100 × 734, 124 Ko | Encart 2 « Prospection » ; en-tête de Comment ça marche | idem |
| `card-3.jpg` | 1100 × 825, 169 Ko | Encart 3 « Qualification » | idem |
| `card-4.jpg` | 900 × 1200 (portrait), 131 Ko | Encart 4 « Rendez-vous » ; en-tête de Tarifs | idem |
| `sans.jpg` | 1000 × 563, 85 Ko | Duo « Sans NOVOLENS », affiché en noir et blanc (accueil, Pourquoi nous, cas client) | `build.py` · constante `DUO` |
| `avec.jpg` | 1000 × 563, 52 Ko | Duo « Avec NOVOLENS » | `build.py` · constante `DUO` |
| `pme.jpg` | 900 × 506, 55 Ko | Carte « PME en croissance » (accueil) ; en-tête de la FAQ | décorative (`alt` vide) |
| `eti.jpg` | 900 × 506, 60 Ko | Carte « ETI » (accueil) | décorative |
| `grand.jpg` | 900 × 506, 111 Ko | Carte « Grands groupes » (accueil) | décorative |
| `livraison.jpg` | 1000 × 563, 65 Ko | Photo sous la liste de livraison (accueil, Comment ça marche) ; en-tête de Contact | `build.py` · `delivery()` |
| `etape-1.jpg` à `etape-5.jpg` | absentes (facultatives) | Remplacent l'animation de l'étape correspondante : 1 à 4 sur l'accueil, 1 à 5 sur Comment ça marche. `app.js` les charge si elles existent. Ratio 5/4 recommandé (1250 × 1000 px) | `story.py` · `story()` (alt vide) |

Les en-têtes de page reçoivent leur photo par la table `PH` de `build.py` (page → fichier) : changer le nom de fichier dans `PH` pour réaffecter une photo, par exemple `"faq.html": "pme"`.

Règles et recette :
- Poids : 250 Ko au plus par image (critère du brief) ; hero et fond de bandeau : 1600 à 2000 px de large.
- Cadrage : les cartes et les en-têtes sont recadrés en `cover` ; garder le sujet au centre. Le hero est recadré à droite : le sujet doit être à droite de l'image.
- Compression :

```bash
python3 -c "
from PIL import Image
i = Image.open('nouvelle-photo.jpg').convert('RGB')
i.thumbnail((2000, 2000))
i.save('site-src/img/hero-bg.jpg', quality=80, optimize=True, progressive=True)"
```

- Droits : les photos actuelles viennent d'Unsplash (licence libre, usage commercial autorisé). Pour des photos de l'entreprise, conserver l'accord des personnes visibles. Noter dans un fichier de crédits l'adresse source de chaque image.
- Texte alternatif : décrire la scène en une phrase pour les photos porteuses de sens (hero, duo) ; les photos d'ambiance restent décoratives.

## c) Modifier chiffres, tarifs, témoignages, e-mail

| Quoi | Où | Remarque |
|---|---|---|
| « +70 % de rendez-vous qualifiés » | `build.py` · `build_index()` (bloc `.stats`, attributs `data-count="70"`, `data-pre`, `data-suf` et texte) ; `build_resultats()` (`kp`) | Changer la valeur dans l'attribut et dans le texte. Voir reformulations P1 de L03 |
| « < 1 mois » | `build.py` (`build_index`, `build_pourquoi`, `build_methode`, `build_resultats`, liste `FAQ`) | Chercher : `grep -n "1 mois" site-src/*.py` |
| Chiffres d'exemple 128 / 86 / 24 / 8 et taux 67 / 28 / 33 % | `funnel()` (liste `rows`), `laptop()` (attributs `data-count`), `build_resultats()`, `v3_extra.py` · `build_cas()`, `story.py` · `il5()`, `ucards.py` · `u3()` et `u4()` | Chercher : `grep -nE "128|\b86\b|\b24\b" site-src/*.py` |
| Courbe hebdomadaire | `build.py` · `laptop()` et `build_resultats()` (listes de valeurs), `story.py` · `il5()` | Les trois listes doivent rester cohérentes entre elles et avec l'entonnoir |
| Tarifs et formules | `build.py` · `build_tarifs()` : appels `plan(nom, accroche, description, [liste], hot=...)` | Le prix est écrit « Sur devis » dans `<div class="price">` de `plan()` : le remplacer par votre prix ou « À partir de … » une fois validé |
| Badge de la formule mise en avant | `plan(..., hot=True)` et texte « Le plus choisi » | Voir P9 de L03 |
| Simulateur (valeurs de départ) | `build_tarifs()` : attributs `value="20000"`, `value="20"`, `value="8"` ; calcul dans `app.js` bloc « V3 : rotateur, simulateur » | Garder la mention « Valeurs d'exemple » |
| Témoignages | `build.py` · `proof_wall()` : une ligne `tcard(citation, nom, fonction, initials=...)` par carte ; `draft=False` retire la pastille « Texte provisoire » ; supprimer les trois lignes `tcard("", "Nom du client", ...)` quand il y a assez de vrais avis | Retirer aussi le sous-titre « Textes provisoires… » dans `build_index()` (`preuves`). Citation du cas client : `v3_extra.py` · `build_cas()` |
| Témoignage vidéo | `build.py` · `build_resultats()` (bloc `vid`) : remplacer le cadre `vid-frame` par une balise `<video controls>` ou un lien | Un lecteur tiers (YouTube) ajoute des cookies : préférer un fichier hébergé avec le site |
| Cas clients | `build_resultats()` (`cas`) ; page modèle : `v3_extra.py` · `build_cas()` | Voir le tableau « Mentions internes » de L03 |
| FAQ | `build.py` · liste `FAQ` (question, réponse) | Une seule modification met à jour la page et les données structurées `FAQPage` |
| E-mail de contact | `build.py` · `footer()` et `build_contact()` (bloc `side`) | Chercher : `grep -n "contact@novolens.fr" site-src/*.py`. Pour rendre l'adresse cliquable, entourer de `<a href="mailto:adresse">…</a>` |
| Raison sociale et URL dans les données structurées | `build.py` · constante `ORG` | Ajouter `"url"`, `"email"`, `"logo"` quand ils sont confirmés |
| Créneaux affichés | `build_contact()` (liste `days`) | Dates figées : à retirer ou à remplacer par un agenda en ligne (section d) |
| Notifications du hero et fonctions du rotateur | `app.js` bloc « Hero : liste de rendez-vous » ; constante `ROT` dans `build.py` | Garder la mention « exemple » |
| Titres et descriptions SEO | dernier appel `page(...)` de chaque `build_*()` | Propositions dans L03 |

## d) Brancher le formulaire de contact

État actuel : la validation des champs obligatoires et de l'e-mail se fait dans le navigateur, puis `app.js` (bloc « Contact : choix de créneau + envoi simulé ») affiche le message de réussite sans rien envoyer. Les champs ont un attribut `name` : `prenom`, `nom`, `email`, `tel`, `societe`, `poste`, `taille`, `objectif`. Le créneau choisi est gardé dans la variable `chosen` mais n'est pas dans un champ.

| Option | Principe | Avantages | Limites |
|---|---|---|---|
| 1. Service de formulaires (par exemple Formspree, Basin, Getform, Web3Forms) | Créer un formulaire dans le service ; il fournit une adresse d'envoi (URL) à laquelle le site envoie les données | Aucun code serveur, réception par e-mail, anti-spam inclus | Un tiers traite les données : l'indiquer dans la politique de confidentialité ; quota gratuit limité |
| 2. Fonction serverless Cloudflare Pages | Un fichier `functions/api/contact.js` reçoit le formulaire et le transmet à un service d'envoi d'e-mails ou l'enregistre dans D1 | Données maîtrisées, même hébergeur, ajout possible de Cloudflare Turnstile contre le spam | Demande un compte du service d'e-mail choisi ; clé à stocker comme secret |
| 3. Messagerie ou agenda | `mailto:adresse` (aucune donnée collectée) ou lien vers un agenda de prise de rendez-vous (Cal.com, Calendly, Microsoft Bookings, Google Agenda) à la place du choix de créneau | Mise en place immédiate ; l'agenda règle le problème des dates figées | Un lien externe vaut mieux qu'un `<iframe>` (pas de traceurs sur votre page) |

Aucun identifiant n'est fourni dans ce dépôt : l'URL du service, la clé d'envoi et l'adresse de réception viennent du compte que vous créez.

Branchement front, option 1 ou 2 :

1. Dans `build.py` · `build_contact()`, ajouter l'adresse d'envoi à la balise du formulaire : `<form id="contact-form" novalidate data-endpoint="<URL fournie par le service>">`.
2. Ajouter un champ caché pour le créneau et un message d'erreur : `<input type="hidden" name="creneau" id="creneau">` et `<p class="err" id="form-error" role="alert"></p>` avant le bouton ; ajouter un champ piège invisible `website` (un robot le remplit, une personne non).
3. Dans `app.js`, remplacer les deux lignes qui affichent le succès (`var s = $('#success-slot')…` et `wrap.classList.add('done')`) par :

```js
var data = new FormData(form);
data.set('creneau', chosen || '');
if (data.get('website')) return;               // champ piège rempli : on ignore
fetch(form.dataset.endpoint, { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
  .then(function (r) {
    if (!r.ok) throw new Error(r.status);
    var s = $('#success-slot'); if (s) s.textContent = chosen ? 'Créneau souhaité : ' + chosen + '.' : 'Nous vous proposerons un créneau.';
    wrap.classList.add('done');
  })
  .catch(function () { $('#form-error').textContent = 'L\'envoi a échoué. Réessayez ou écrivez-nous par e-mail.'; });
```

4. Supprimer la note « Aperçu : ce formulaire n'envoie rien… » dans `build_contact()`.
5. Ajouter sous le bouton la mention d'information RGPD (responsable du traitement, finalité, durée, droits) et le lien vers la politique de confidentialité.

Option 2 (squelette de la fonction, à placer dans un dossier `functions/` à la racine du projet déployé ; vérifier l'emplacement attendu par Cloudflare selon le mode de déploiement) :

```js
export async function onRequestPost({ request, env }) {
  const f = await request.formData();
  if (f.get('website')) return new Response('ok');
  // env.MAIL_ENDPOINT, env.MAIL_KEY et env.MAIL_TO sont des variables que vous définissez
  // dans Cloudflare Pages > Réglages > Variables (clé en « secret »)
  const r = await fetch(env.MAIL_ENDPOINT, {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + env.MAIL_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ to: env.MAIL_TO, subject: 'Nouvelle demande NOVOLENS', fields: Object.fromEntries(f) })
  });
  return new Response(r.ok ? 'ok' : 'erreur', { status: r.ok ? 200 : 502 });
}
```

Le format exact de la requête dépend du service d'e-mail choisi. Dans ce cas, `data-endpoint` vaut `/api/contact`. Tester par un envoi réel depuis l'adresse de prévisualisation `.pages.dev` avant la mise en ligne.

## e) Mise en ligne sur Cloudflare Pages

**La mise en ligne exige l'accord explicite de l'utilisateur** (le brief l'impose pour toute publication sur un domaine). Rien n'a été déployé par cette mission. Ne pas commencer avant d'avoir cet accord et d'avoir terminé la checklist (section g).

Prérequis : un compte Cloudflare (l'offre gratuite suffit pour Pages), un nom de domaine dont vous êtes titulaire, le site reconstruit et audité.

| Étape | Action |
|---|---|
| 1. Choisir le mode | **Envoi direct** : `npx wrangler pages deploy livrables/site --project-name <nom-du-projet>` (la première fois, `npx wrangler login`). **Intégration Git** : Cloudflare > Workers et Pages > Créer > Pages > Se connecter à Git ; commande de build : aucune ; dossier de sortie : `missions/2026-11-16-site-novolens-agence/livrables/site` (le dossier `site/` est déjà généré) |
| 2. Premier déploiement | Il crée l'adresse `<nom-du-projet>.pages.dev`. La relire page par page, tester le formulaire, la page 404 (servie automatiquement quand le fichier `404.html` existe) et le mobile |
| 3. Domaine | Projet Pages > Domaines personnalisés > Configurer. Si le DNS du domaine est chez Cloudflare, l'enregistrement est ajouté tout seul ; sinon créer chez le registrar un CNAME de `www` vers `<nom-du-projet>.pages.dev` (le domaine nu `novolens.fr` exige le DNS Cloudflare). Le certificat HTTPS est automatique. Rediriger le domaine nu vers `www` (règle de redirection Cloudflare) ou l'inverse, un seul des deux est canonique |
| 4. Remplacer le domaine d'exemple | Voir ci-dessous |
| 5. Après mise en ligne | Ouvrir l'adresse finale, vérifier le cadenas, `…/robots.txt`, `…/sitemap.xml`, déclarer le sitemap dans Google Search Console et Bing Webmaster Tools |
| 6. Retour arrière | Cloudflare conserve les déploiements précédents : Déploiements > Revenir à cette version |

**Remplacer `https://www.novolens.fr/`** (domaine d'exemple, non confirmé) :
- `sitemap.xml` et `robots.txt` sont générés par `v3_extra.py` · `build_seo()`. Changer la ligne `base = "https://www.novolens.fr/"`, reconstruire, puis vérifier avec `grep -rn "https://www.novolens.fr" site/` (la commande ne doit rien renvoyer si le domaine a changé).
- Cloudflare Pages sert normalement `/page` pour `page.html` et redirige `/page.html` vers `/page`. Contrôler avec `curl -I https://<nom-du-projet>.pages.dev/contact.html`. Si la redirection est confirmée, écrire les adresses du sitemap et des balises canoniques sans `.html` (dans `build_seo()` : `p[:-5]` au lieu de `p`).

**Balises canoniques à ajouter** : aucune page n'en a aujourd'hui. Dans `build.py` · `page()`, après la ligne qui construit `head` avec la description :

```python
BASE = os.environ.get("SITE_URL", "https://www.novolens.fr/")
canon = BASE + ("" if fname == "index.html" else fname[:-5])   # sans .html
if fname != "404.html":
    head += f'<link rel="canonical" href="{canon}">\n<meta property="og:url" content="{canon}">\n'
```

Utiliser la même constante `BASE` dans `build_seo()` pour ne changer le domaine qu'à un endroit (`v3_extra.py` est exécuté dans l'espace de noms de `build.py`). Lancer alors : `SITE_URL=https://votre-domaine/ V2=1 V3=1 python3 build.py`.

Autres éléments à ajouter avant la mise en ligne, absents du site actuel :

| Élément | Comment |
|---|---|
| Squelette complet de l'accueil | `index.html` est généré sans `<!doctype>`, `<html lang="fr">`, `<meta charset>` ni `viewport` (branche `if index:` de `page()`). Réserver cette branche à l'artefact : `if index and os.environ.get("ARTIFACT") == "1":` ; sans cette variable, l'accueil prend le squelette des autres pages |
| Titre de l'accueil | Supprimer `if V3 and index: title = "NOVOLENS"` dans `page()` (titre proposé dans L03) |
| Page cas client en `noindex` | Tant qu'elle est un gabarit : `<meta name="robots" content="noindex">` dans `build_cas()` et retrait de `build_seo()` et du pied de page |
| Favicon | Enregistrer le logo SVG (fonction `logo()`) dans `site-src/img/favicon.svg` et ajouter `<link rel="icon" href="img/favicon.svg">` dans `page()` |
| Image de partage | Créer une image 1200 × 630 `img/og.jpg` (moins de 250 Ko) et ajouter `<meta property="og:image" content="{BASE}img/og.jpg">` dans `page()` |
| Pages légales | Créer `mentions-legales.html`, `confidentialite.html`, `cgv.html` (contenu fourni par l'éditeur), les ajouter à `footer()`, au sitemap et à la liste `pages` de `build_seo()` |
| En-têtes de sécurité | Fichier `site-src/_headers` copié à la reconstruction (après `shutil.copytree(...)` dans `build.py` : `shutil.copy(os.path.join(HERE, "_headers"), DIST)`), avec par exemple `/*` puis, indentés, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: DENY` |

## f) Analytics et consentement aux cookies

Constat : le site ne contient ni outil de mesure d'audience, ni bandeau de consentement, ni cookie, ni `localStorage`. Le seul appel à un service tiers est le chargement des polices Google Fonts (constante `FONTS` de `build.py`), qui transmet l'adresse IP du visiteur à Google.

| À faire | Comment |
|---|---|
| Héberger les polices soi-même | Télécharger Newsreader, Inter et Caveat (fichiers `woff2`), les placer dans `site-src/fonts/`, déclarer des `@font-face` dans `site-src/style.css`, copier le dossier à la reconstruction, supprimer la constante `FONTS` et son insertion dans `page()` |
| Choisir un type de mesure | **A. Mesure d'audience sans consentement** : outil configuré pour l'exemption de la CNIL (statistiques anonymes de fréquentation uniquement, pas de croisement avec d'autres données, pas de suivi entre sites), par exemple Matomo en mode exempté, Plausible ou Cloudflare Web Analytics. Aucun bandeau n'est alors nécessaire, mais la politique de confidentialité doit l'indiquer. **B. Mesure avancée ou publicité** (Google Analytics, pixel LinkedIn, etc.) : un bandeau de consentement est obligatoire |
| Si option A | Ajouter le script fourni par l'outil juste avant `</body>` dans `page()` de `build.py` ; le jeton ou l'identifiant vient de votre compte, il ne figure pas dans ce dépôt |
| Si option B | Ajouter un bandeau avec « Tout accepter » et « Tout refuser » de même importance, un bouton « Gérer mes cookies » dans le pied de page, aucun script de mesure chargé avant le « oui », choix conservé 6 mois au plus. Fichier à créer : `site-src/consent.js` (affiche le bandeau, mémorise le choix, injecte le script d'analyse seulement après acceptation), inclus par `page()` ; accessibilité : bandeau atteignable au clavier, focus visible |
| Événements utiles | Clic sur « Réserver un échange » (`a[href="contact.html"]`), envoi réussi du formulaire (dans le `.then` de la section d), ouverture de la vidéo (`[data-open-video]`) |
| Politique de confidentialité | Citer : hébergeur (Cloudflare), service de formulaire ou d'e-mail, outil d'analyse, finalités, durées de conservation, droits d'accès, de rectification et d'opposition, contact |

## g) Checklist avant mise en ligne

- [ ] Accord explicite de l'utilisateur pour publier et sur quel domaine
- [ ] Toutes les affirmations de `L03-contenu.md` sont tranchées : confirmées par une source, ou reformulées (P1 à P15) ; +70 % et « < 1 mois » validés ou retirés
- [ ] Mentions internes remplacées (tableau « Mentions internes visibles » de L03) : cartes de cas clients, « Chiffre à confirmer », « (à confirmer) », « Aperçu : ce formulaire… », étiquette « Photo remplaçable »
- [ ] Témoignages fictifs retirés ou remplacés par de vrais avis autorisés ; page cas client en `noindex`
- [ ] Dates figées retirées (carte de livraison, notifications du hero, créneaux du formulaire)
- [ ] Courbe et entonnoir cohérents ; « trois étapes » corrigé en « cinq étapes » sur Comment ça marche
- [ ] Photos validées (droits, cadrage, moins de 250 Ko), textes alternatifs relus
- [ ] E-mail réel, formulaire branché et testé de bout en bout, note « Aperçu » supprimée, mention RGPD ajoutée
- [ ] Pages mentions légales, confidentialité et CGV créées et liées dans le pied de page
- [ ] Domaine remplacé dans `build_seo()`, balises canoniques, favicon, image de partage ajoutés ; `sitemap.xml` et `robots.txt` regénérés
- [ ] `index.html` avec `<!doctype>`, `lang="fr"`, titre complet
- [ ] Polices hébergées sur le site ; analytics et consentement traités (section f)
- [ ] Audit relancé : aucun élément dans `summary`, contrastes OK, `index.html` et chaque page sous 60 Ko, images sous 250 Ko
- [ ] Test à la main à 400, 820 et 1360 px, au clavier (Tab, menu mobile, FAQ), avec mouvement réduit activé
- [ ] Déploiement de prévisualisation `.pages.dev` relu ; DNS, HTTPS et redirection `www` vérifiés
- [ ] Sitemap déclaré dans Google Search Console ; sauvegarde du dépôt faite avant le déploiement

## h) Lancer l'audit

Depuis `missions/2026-11-16-site-novolens-agence/` :

```bash
node livrables/audit/audit.js livrables/site > livrables/audit/resultat.json
```

Prérequis : Node.js et Playwright avec son navigateur (`npm install playwright` puis `npx playwright install chromium`). Le script ouvre chaque page du dossier à 400, 820 et 1360 px, puis teste le clavier et le mouvement réduit, calcule 15 contrastes (seuil 4,5 ; 3 pour grand texte) et pèse pages et images.

Lire le résultat : le bloc `summary` doit avoir toutes ses listes vides.

| Clé de `summary` | Signification d'une liste non vide |
|---|---|
| `html_over_60kb` | page HTML de plus de 60 Ko |
| `images_over_250kb` | image de plus de 250 Ko |
| `overflow` | défilement horizontal à une des trois largeurs |
| `console_errors` | erreur dans la console (les erreurs de polices et de chargement réseau sont ignorées, le test se fait hors ligne) |
| `h1_not_one` | page sans h1 ou avec plusieurs h1 |
| `no_description` | description de moins de 40 caractères |
| `imgs_without_dims`, `imgs_without_alt` | image sans `width`/`height` ou sans attribut `alt` |
| `broken_links` | lien interne vers un fichier absent |
| `focus_not_visible` | focus clavier invisible |
| `reduced_motion_hidden` | contenu masqué avec mouvement réduit |
| `contrast_failures` | paire de couleurs sous le seuil |

Le script ne vérifie pas : le texte, les canoniques, le squelette HTML de l'accueil (`<!doctype>`), le formulaire réel et les liens externes. Ces points relèvent de la checklist de la section g. Relancer l'audit après chaque reconstruction et avant chaque déploiement.
