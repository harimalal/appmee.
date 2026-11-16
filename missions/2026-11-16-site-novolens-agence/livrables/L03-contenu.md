# L03 — Contenu source relu du site NOVOLENS V3

Mission `site-novolens-agence`, état du 2026-11-16. Les textes ci-dessous sont extraits du HTML généré dans `livrables/site/` (aucune réécriture de zéro). Pour modifier un texte, on ne touche jamais au HTML : on change la source indiquée dans `livrables/site-src/`, puis on reconstruit (voir L04).

## Comment lire ce document

| Statut | Sens |
|---|---|
| repris du visuel de départ | chiffre ou promesse du visuel fourni au départ ; le site le signale par l'astérisque du pied de page (« +70 % » et « < 1 mois ») |
| exemple illustratif | valeur inventée pour montrer le fonctionnement ; elle est étiquetée « exemple » sur le site |
| hypothèse à confirmer | affirmation écrite pour que la page tienne debout ; aucune source ne l'établit encore |

Fichiers sources : `build.py` (pages, pied de page, FAQ, formulaire), `story.py` (parcours en étapes), `ucards.py` (les 4 encarts), `v3_extra.py` (cas client, 404, sitemap, robots), `app.js` (hero animé, formulaire, simulateur). Chemins relatifs à `livrables/`.

## Constats prioritaires et état de traitement

Les constats ci-dessous ont été relevés à la première relecture ; la colonne « État » reflète le site reconstruit le 2026-11-16 (version 18 h 12). Dans les tableaux « À valider », une recommandation qui commence par « Traité » est déjà appliquée dans le site actuel ; la suite de la phrase dit ce qui reste.

| # | Constat | État | Où | Correction |
|---|---|---|---|---|
| 1 | `index.html` était écrit en fragment, sans `<!doctype>`, `<html lang>`, `<meta charset>` ni `viewport` | Traité : document complet ; la variante en fragment pour l'artefact est dans `livrables/site-artefact/index.html` | `build.py` · `page()` | Aucune |
| 2 | Le titre de l'accueil était « NOVOLENS » seul | Traité : « NOVOLENS, prospection B2B externalisée » | `build.py` · `page()` | Aucune |
| 3 | Textes de remplissage et remarques internes visibles | Traité en grande partie (cartes de cas clients, pied de page, « Chiffre à confirmer », note des tarifs) ; reste à faire pour les points du tableau « Mentions internes » | voir ce tableau | Voir ce tableau |
| 4 | Chiffres contradictoires | Traité pour la courbe (cumul de 8) et pour l'introduction de Méthode (« Cinq étapes »). Reste à faire : description SEO de Méthode (« trois étapes »), illustration de l'étape 5 (barres 3 à 17), pilotage « hebdomadaire » ou « régulier » | `build.py` · `build_methode()`, `build_tarifs()` ; `story.py` · `il5()` | Voir les tableaux « À valider » |
| 5 | Trois témoignages nommés (Thomas L., Sophie M., Marc D.) sont fictifs | Reste à faire | `build.py` · `proof_wall()` | Les retirer avant mise en ligne ou les remplacer par de vrais avis signés |
| 6 | Dates figées dans les exemples | Traité (carte de livraison, hero calculé à partir du jour, créneaux en jours de semaine) | `build.py`, `app.js` | Aucune |
| 7 | Poids des pages | Conforme : accueil 55,7 Ko, Méthode 51,7 Ko (limite 60 Ko) | `site/` | Relancer l'audit après chaque ajout |
| 8 | Pages légales absentes et pied de page sans liens vers elles | Reste à faire : les mentions de remplissage sont retirées, les trois pages sont à créer (voir L04, section e) | `build.py` · `footer()` | Créer mentions légales, confidentialité et CGV |

## Titres SEO et descriptions : actuel et proposition

Longueur recommandée : titre 60 caractères au plus, description 155 au plus. Pour changer : dernier appel `page(...)` de chaque fonction `build_*()` dans `build.py` (et `v3_extra.py` pour le cas client). Le titre de l'accueil est déjà corrigé (« NOVOLENS, prospection B2B externalisée »). Si les autres titres prennent le suffixe « | NOVOLENS », adapter aussi le calcul du fil d'Ariane dans `page()` : `title.replace(" NOVOLENS","").replace("NOVOLENS ","")` doit devenir `title.split(" | ")[0]`.

| Page | Titre actuel | Proposition (longueur) | Description proposée (longueur) |
|---|---|---|---|
| `index.html` | NOVOLENS, prospection B2B externalisée (38) | Conservé : NOVOLENS, prospection B2B externalisée (38) | NOVOLENS prend en charge votre prospection B2B : nous qualifions et livrons des rendez-vous avec des décideurs de PME, ETI et grands groupes. (141) |
| `pourquoi-nous.html` | Pourquoi NOVOLENS (17) | Pourquoi externaliser sa prospection B2B \| NOVOLENS (51) | Pourquoi confier sa prospection B2B à NOVOLENS : démarrage rapide visé, ciblage sur mesure, qualification selon vos critères et pilotage mesurable. (147) |
| `comment-ca-marche.html` | Comment ça marche, NOVOLENS (27) | Méthode de prospection B2B en 5 étapes \| NOVOLENS (49) | La méthode NOVOLENS en cinq étapes : calibrage, prospection, qualification, rendez-vous livrés avec contexte et pilotage par le reporting. (138) |
| `resultats.html` | Résultats NOVOLENS (18) | Résultats et indicateurs de prospection \| NOVOLENS (50) | Les indicateurs suivis par NOVOLENS : rendez-vous qualifiés, entonnoir de prospection et exemple de reporting. Chiffres d'exemple en attendant les premiers cas clients. (168) |
| `cas-client.html` | Cas client modèle NOVOLENS (26) | Cas client modèle : du ciblage au rendez-vous \| NOVOLENS (56) | Gabarit de cas client NOVOLENS : contexte, action, résultat et parole du dirigeant. Données d'exemple. (102) |
| `tarifs.html` | Tarifs NOVOLENS (15) | Tarifs de prospection B2B sur devis \| NOVOLENS (46) | Tarifs NOVOLENS : trois formules de prospection B2B externalisée, sur devis, adaptées à votre cible et à votre volume de rendez-vous. (133) |
| `faq.html` | FAQ NOVOLENS (12) | FAQ prospection B2B externalisée \| NOVOLENS (43) | Réponses aux questions fréquentes sur NOVOLENS : rendez-vous qualifiés, délais, méthode, reporting, engagement et tarifs. (121) |
| `contact.html` | Contact NOVOLENS (16) | Réserver un échange de 15 min \| NOVOLENS (40) | Réservez un échange de 15 minutes avec un expert NOVOLENS pour parler de vos objectifs de croissance. Sans engagement, réponse sous 24 h. (137) |

Les descriptions de `cas-client`, `tarifs`, `faq` et `contact` (102 à 137 caractères) restent valables. Page 404 : titre « Page introuvable NOVOLENS », à laisser tel quel (ajouter `noindex` est inutile, le serveur renvoie déjà le code 404).

## Promesses non sourcées et reformulations prudentes

| Réf. | Phrase actuelle | Reformulation proposée | Où modifier |
|---|---|---|---|
| P1 | « +70 % de rendez-vous qualifiés* » | « Un objectif de progression fixé avec vous dès le calibrage » tant que le chiffre n'est pas mesuré ; ensuite « +X % par rapport à leur prospection interne (n missions, période) » avec les vraies valeurs. | site-src/build.py · build_index(), build_resultats() |
| P2 | « < 1 mois pour les premiers résultats » | « Premiers rendez-vous visés en moins d'un mois après le cadrage, selon votre cible. » | site-src/build.py · build_index(), build_pourquoi(), build_methode(), build_resultats() |
| P3 | « Zéro rendez-vous pour rien » ; « Ce qui ne passe pas le filtre ne vous est jamais livré » | « Seuls les rendez-vous qui répondent à vos critères vous sont proposés » ; gain : « Des rendez-vous filtrés ». | site-src/story.py · STEPS[2] |
| P4 | « des décideurs réellement intéressés » ; « prêts à échanger sur vos solutions » | « des décideurs qui ont accepté d'échanger avec vous ». | site-src/build.py · build_index() ; compare() (liste Avec) |
| P5 | « Des rendez-vous prêts à signer » | « Des rendez-vous préparés, avec tout le contexte ». | site-src/story.py · STEPS[3] |
| P6 | « Une croissance accélérée » ; « Des dirigeants qui accélèrent leur croissance avec NOVOLENS » (alors qu'aucun client n'est cité) | « Un agenda commercial alimenté chaque semaine » ; pour la section d'avis, la retirer tant qu'il n'y a pas de vrai avis. | site-src/build.py · compare(), build_index() (preuves) |
| P7 | « Un pipeline prévisible » (accueil, étape 5, reporting, cas client) | « Un pipeline mesurable » : on promet la visibilité, pas la prévision. | site-src/build.py · build_index(), build_methode(), v3_extra.py ; site-src/story.py · STEPS[4] |
| P8 | « Une souplesse totale » | « Une souplesse réelle : vous gardez la main sur la cible et le rythme ; la durée minimale est précisée au devis ». | site-src/build.py · build_pourquoi() |
| P9 | « Le plus choisi » (formule Croissance) | « Recommandé » (avis de l'équipe, vérifiable) ou retirer le badge. | site-src/build.py · build_tarifs() |
| P10 | « Un seul gros client signé suffit souvent à rentabiliser une mission » | « Pour une offre à forte valeur unitaire, un seul client signé peut couvrir une part importante du coût d'une mission : le simulateur le vérifie avec vos chiffres. » | site-src/build.py · build_tarifs() |
| P11 | « jamais de relance agressive » | « Des relances mesurées, dans un cadre validé avec vous. » | site-src/build.py · build_pourquoi() |
| P12 | « Des retours qui parlent de rendez-vous, pas de promesses » | Retirer la section tant qu'aucun témoignage réel n'existe ; ensuite : « Ce que disent nos clients ». | site-src/build.py · build_resultats() |
| P13 | « respectueuse du RGPD et du droit d'opposition » | « Nous encadrons la prospection B2B selon les règles de la CNIL : les personnes contactées sont informées et peuvent s'opposer à tout moment. » + lien vers la politique de confidentialité ; relecture juridique avant publication. | site-src/build.py · build_pourquoi(), liste FAQ |
| P14 | « De nouveaux clients dans votre agenda » (liste qui défile en direct) | « Exemple de rendez-vous livrés » : ce sont des rendez-vous, pas des clients, et ils sont fictifs. | site-src/build.py · build_index() (notifs-title) |
| P15 | « Réponse sous 24 h » (partout) | « Réponse sous 24 h ouvrées » si l'équipe ne répond pas le week-end. | site-src/build.py · cta(), footer(), build_contact(), build_index() |

## Mentions internes visibles sur le site à remplacer

| Où | Texte visible | Fichier · fonction | État et remplacement |
|---|---|---|---|
| Pied de page, toutes les pages | « (à confirmer) » après l'e-mail ; ligne de remplissage sur mentions légales, confidentialité et CGV ; ancienne note « * Chiffres repris du visuel de départ… » | site-src/build.py · footer() | Traité : mention « à confirmer » et ligne de remplissage retirées ; note remplacée par « * Objectif indicatif. Les chiffres, exemples de cas et coordonnées de cette maquette sont donnés à titre illustratif. ». Reste à faire : créer les trois pages légales et leurs liens, retirer la note à la mise en ligne. |
| Accueil, avis clients | « Textes provisoires en attendant les vrais avis clients. » et pastille « Texte provisoire » | site-src/build.py · build_index(), tcard() | Reste à faire : retirer la section (P6, P12). |
| Pourquoi nous | Sous-titre du comparatif ; « Engagements proposés, à valider avant publication. » | site-src/build.py · build_pourquoi() | Traité : le sous-titre du comparatif est devenu « Repères généraux, à adapter à votre situation. ». Reste à faire : supprimer « Engagements proposés, à valider avant publication. ». |
| Résultats | Cartes de cas clients à texte de remplissage, « Chiffre à confirmer », « À remplacer par vos vrais chiffres. », étiquette d'emplacement vidéo | site-src/build.py · build_resultats() | Traité : remplacés par trois cartes « Secteurs ciblés » et des phrases propres. Reste à faire : le cadre « Témoignage vidéo · 60 s » (voir tableau de la page). |
| Tarifs | Note « Formules proposées à titre indicatif, à ajuster avec vos tarifs réels. » | site-src/build.py · build_tarifs() | Traité : remplacée par « Chaque devis est établi après un échange de 15 minutes. ». |
| Contact | « Aperçu : ce formulaire n'envoie rien… » ; « (adresse à confirmer) » | site-src/build.py · build_contact() | Reste à faire : à retirer une fois le formulaire branché et l'adresse confirmée. |
| Comment ça marche, accueil | Pastille « Photo remplaçable : img/etape-N.jpg » en haut de chaque scène d'étape (visible sur grand écran) | site-src/story.py · story() (span photo-tag) | Reste à faire : supprimer la ligne `<span class="photo-tag">` avant la mise en ligne. |

## Blocs communs (texte repris sur plusieurs pages)

### En-tête et navigation

Lien d'évitement « Aller au contenu » ; logo NOVOLENS ; menu : Pourquoi nous, Comment ça marche, Résultats, Tarifs, FAQ ; bouton « Réserver un échange » ; sur mobile, bouton collant « Réserver un échange de 15 min » (absent de la page contact et de la 404). Source : `build.py` · `header()`, `NAV`, `page()` (sticky).

### Appel à l'action final (toutes les pages sauf la 404)

  - Échange stratégique
- **H2** : Parlons de vos objectifs de croissance.
  - Un échange de 15 minutes avec un expert NOVOLENS pour comprendre vos enjeux et voir comment nous pouvons vous apporter des rendez-vous qualifiés.
  - Réserver un échange de 15 min
  - Sans engagement
  - Réponse sous 24 h
  - Échange avec un expert

Source : `build.py` · `cta(title, text)`. Variantes : tarifs (« Demandez votre devis en 15 minutes. »), FAQ (« Une autre question ? »).

### Comparateur Sans / Avec NOVOLENS (accueil, pourquoi nous)

  - Sans NOVOLENS
  - Avec NOVOLENS
  - Lun
  - Mar
  - Mer
  - Jeu
  - Ven
  - à relancer
  - RDV · DG
  - RDV · DAF
  - à relancer
  - RDV · DSI
  - RDV · CEO
  - à relancer
  - RDV · DRH
  - RDV · DA
  - à relancer
  - RDV · DG
  - Pas le temps de prospecter
  - Des opportunités qui passent à côté
  - Des commerciaux qui s'éparpillent
  - Des relances oubliées
  - Un pipeline irrégulier
  - Des mois sans nouveaux clients
  - Des rendez-vous qualifiés dans votre agenda
  - Des décideurs réellement intéressés
  - Un pipeline régulier et prévisible
  - Vos équipes concentrées sur la vente
  - Une croissance accélérée
  - Exemple illustratif d'une semaine d'agenda.

Source : `build.py` · `compare()`.

### Carte de livraison d'un rendez-vous (accueil, comment ça marche)

  - Directeur Général
  - Industrie · 500 M€ · France
  - Rendez-vous qualifié
  - Contexte
  - Projet de modernisation en cours
  - Besoin identifié
  - Recherche de solutions pour optimiser ses opérations
  - Intérêt
  - Élevé
  - Prochain échange
  - Jeudi · 10h00
  - Documents
  - Compte rendu + notes
  - Un rendez-vous qualifié, avec tout le contexte.
  - Profil du décideur
  - Contexte et enjeux
  - Besoin identifié
  - Niveau d'intérêt
  - Compte rendu détaillé
  - Accès au reporting global

Source : `build.py` · `delivery()`.

### Les 4 encarts « action et moyen » (accueil, comment ça marche, cas client)

  - 1
  - *H3* : Calibrage
  - On définit la cible parfaite avec vous.
  - Le moyen
  - Atelier de cadrage
  - Client idéal
  - 2
  - *H3* : Prospection
  - On contacte les bons décideurs à votre place.
  - Le moyen
  - Téléphone
  - E-mail
  - in
  - LinkedIn
  - 3
  - *H3* : Qualification
  - On filtre : seuls les vrais intéressés passent.
  - Le moyen
  - Appel de qualification
  - Critères écrits
  - 4
  - *H3* : Rendez-vous
  - Les rendez-vous tombent dans votre agenda.
  - Le moyen
  - Agenda partagé
  - Dossier de contexte

Source : `ucards.py` · `section()` (textes) et `u1()` à `u4()` (animations).

### Mur de témoignages (accueil, résultats)

  - Texte provisoire
  - En moins d'un mois, nous avons obtenu des rendez-vous qualifiés avec des décideurs que nous n'arrivions pas à contacter.
  - Thomas L.
  - Dirigeant · Industrie
  - Texte provisoire
  - NOVOLENS nous a permis de réactiver des prospects que nous avions mis de côté faute de temps. Des opportunités concrètes et à fort potentiel.
  - Sophie M.
  - Directrice Commerciale · Services B2B
  - Texte provisoire
  - Une équipe très professionnelle, déterminée et persévérante. Les rendez-vous sont bien qualifiés et nous gagnons un temps considérable.
  - Marc D.
  - CEO · Tech & Logiciels
  - Témoignage à venir
  - Nom du client
  - Fonction · Secteur
  - Témoignage à venir
  - Nom du client
  - Fonction · Secteur
  - Témoignage à venir
  - Nom du client
  - Fonction · Secteur

Source : `build.py` · `proof_wall()`, `tcard()`. Le script `app.js` clone les cartes (copie masquée aux lecteurs d'écran) pour le défilement continu.

### Pied de page

  - NOVOLENS
  - Prospection B2B externalisée : des rendez-vous qualifiés avec des décideurs, livrés directement dans votre agenda.
  - *H4* : Site
  - Accueil
  - Pourquoi nous
  - Comment ça marche
  - Résultats
  - Cas client (modèle)
  - *H4* : Offre
  - Tarifs
  - FAQ
  - Réserver un échange
  - *H4* : Contact
  - contact@novolens.fr
  - Réponse sous 24 h
  - © 2026 NOVOLENS. Tous droits réservés.
  - * Objectif indicatif. Les chiffres, exemples de cas et coordonnées de cette maquette sont donnés à titre illustratif.

Source : `build.py` · `footer()`.

## Page Accueil (`index.html`)

- **Titre SEO** : NOVOLENS, prospection B2B externalisée
- **Description** : NOVOLENS livre des rendez-vous qualifiés avec des décideurs : prospection B2B externalisée pour PME, ETI et grands groupes.
- **Balise h1** : unique

### Titres et textes

  - Prospection B2B externalisée
- **H1** : Des rendez-vous qualifiés. Sans effort de prospection.
  - Nous identifions les bons prospects, les contactons, les qualifions et vous livrons des rendez-vous avec des décideurs réellement intéressés.
  - Réserver un échange de 15 min
  - Voir comment ça marche
  - Des rendez-vous avec dirigeants
  - Sans engagement
  - Réponse sous 24 h
  - Échange avec un expert
  - Décideur confirmé
  - Besoin qualifié
  - De nouveaux clients dans votre agenda
  - +70 %
  - de rendez-vous qualifiés*
  - < 1 mois
  - pour les premiers résultats
  - Des comptes stratégiques
  - et un fort potentiel commercial
  - Un pipeline
  - prévisible et mesurable
  - Votre réalité aujourd'hui
- **H2** : Et si votre prochain gros client arrivait déjà dans votre agenda ?
  - Pendant que vous gérez votre entreprise, notre équipe s'occupe de la prospection. Vous recevez des rendez-vous qualifiés avec des décideurs prêts à échanger sur vos solutions.
  - Pourquoi externaliser
  - Sans NOVOLENS
  - Avec NOVOLENS
- *Bloc commun : comparateur Sans / Avec NOVOLENS (voir « Blocs communs »).*
  - Notre approche
- **H2** : De la stratégie au rendez-vous, nous nous occupons de tout.
  - Quatre étapes, une équipe experte en prospection à froid. Regardez ce que vous y gagnez à chaque étape.
  - Étape 1 sur 4
  - *H3* : On définit la cible parfaite avec vous.
  - Un atelier pour fixer vos objectifs, votre client idéal et les critères d'un rendez-vous qui vaut le coup.
  - Profil de client idéal et comptes prioritaires
  - Message et argumentaire validés avec vous
  - Critères de qualification écrits noir sur blanc
  - Ce que vous gagnez
  - Une cible nette
  - Étape 2 sur 4
  - *H3* : On contacte les bons décideurs à votre place.
  - Téléphone, e-mail, LinkedIn : une équipe dédiée prospecte et relance avec persévérance, sans que vos commerciaux s'en occupent.
  - Contacts sélectionnés et vérifiés
  - Séquences multicanales personnalisées
  - Relances jusqu'à une réponse claire
  - Ce que vous gagnez
  - Des heures rendues
  - Étape 3 sur 4
  - *H3* : On filtre : seuls les vrais intéressés passent.
  - Chaque contact est vérifié sur le décideur, le besoin et l'intérêt. Ce qui ne passe pas le filtre ne vous est jamais livré.
  - Fonction et pouvoir de décision confirmés
  - Besoin et contexte identifiés
  - Niveau d'intérêt évalué
  - Ce que vous gagnez
  - Zéro rendez-vous pour rien
  - Étape 4 sur 4
  - *H3* : Les rendez-vous tombent dans votre agenda.
  - Vous recevez des rendez-vous confirmés, avec un dossier complet : profil, contexte, besoin, prochaine étape.
  - Rendez-vous confirmés dans votre agenda
  - Fiche de contexte et compte rendu
  - Vos commerciaux arrivent préparés
  - Ce que vous gagnez
  - Un agenda qui se remplit
  - Voir la méthode en détail
  - Notre livraison
- **H2** : Des rendez-vous prêts à être exploités.
  - Chaque rendez-vous est qualifié et accompagné de toutes les informations nécessaires pour des échanges productifs.
- *Bloc commun : carte de livraison d'un rendez-vous (voir « Blocs communs »).*
  - En 4 étapes
- **H2** : Comprendre NOVOLENS en un coup d'œil.
  - Quatre étapes qui se suivent. À chaque fois, l'action et le moyen utilisé pour obtenir vos rendez-vous.
- *Bloc commun : les 4 encarts « action et moyen » (voir « Blocs communs »).*
  - Pour qui
- **H2** : Pensé pour les entreprises qui ont des ambitions.
  - Des PME aux grands groupes, la même exigence : des décideurs, du contexte, de la régularité.
  - *H3* : PME en croissance
  - Vous avez une offre qui a fait ses preuves et un besoin de nouveaux comptes, sans recruter ni structurer une équipe de prospection.
  - Dirigeants
  - Directions commerciales
  - *H3* : ETI
  - Vous visez des comptes plus complexes et plus structurés, avec plusieurs interlocuteurs à convaincre.
  - Développement
  - Business units
  - *H3* : Grands groupes
  - Vous souhaitez ouvrir de nouveaux marchés ou comptes stratégiques avec une approche ciblée, qualifiée et mesurable.
  - Comptes stratégiques
  - Nouveaux marchés
  - Ils en parlent mieux que nous
- **H2** : Des dirigeants qui accélèrent leur croissance avec NOVOLENS.
  - Textes provisoires en attendant les vrais avis clients.
- *Bloc commun : mur de témoignages (voir « Blocs communs »).*
- *Bloc commun : appel à l'action final (voir « Blocs communs »).*

### À valider

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | « +70 % de rendez-vous qualifiés* » | repris du visuel de départ | `site-src/build.py · build_index() (bloc .stats, data-count="70")` | Voir P1. Garder l'astérisque et la note de pied de page tant que le chiffre n'est pas mesuré ; indiquer base de comparaison, période et nombre de missions dès qu'ils existent. |
| 2 | « < 1 mois pour les premiers résultats » | repris du visuel de départ | `site-src/build.py · build_index() (.stats), build_pourquoi(), build_methode(), build_resultats(), FAQ` | Voir P2. Même formulation partout : premiers rendez-vous visés après le cadrage, selon la cible. |
| 3 | « Des rendez-vous avec dirigeants / directeurs achats / DSI / directeurs commerciaux » (rotateur) | hypothèse à confirmer | `site-src/build.py · constante ROT` | Ne garder que les fonctions que l'équipe sait réellement atteindre. |
| 4 | « des décideurs réellement intéressés » (introduction) et « décideurs prêts à échanger sur vos solutions » | hypothèse à confirmer | `site-src/build.py · build_index() (hero, reality)` | Voir P4. |
| 5 | « De nouveaux clients dans votre agenda » + 5 rendez-vous défilants (jours de semaine calculés à partir de la date du jour ; DG Industrie 500 M€, Directrice Achats Santé Groupe, CEO Tech, Directeur Commercial Distribution ETI, DSI Services B2B 1 200 salariés) | exemple illustratif | `site-src/app.js · bloc « Hero : liste de rendez-vous » (tableau data) ; titre dans site-src/build.py · build_index() (notifs-title)` | Traité : les dates sont maintenant calculées à partir du jour de la visite (`app.js`). Reste à faire : voir P14, renommer le titre en « Exemple de rendez-vous livrés ». |
| 6 | Pastilles « Décideur confirmé » et « Besoin qualifié » | hypothèse à confirmer | `site-src/build.py · build_index() (chip-float)` | Garder si ces deux contrôles figurent bien dans le process de qualification. |
| 7 | « Réserver un échange de 15 min », « Sans engagement », « Échange avec un expert » | hypothèse à confirmer | `site-src/build.py · cta(), build_index(), header()` | Confirmer la durée, que l'échange initial est gratuit et qu'un expert prend l'appel. Préciser « Échange initial sans engagement ». |
| 8 | « Réponse sous 24 h » (hero, CTA, contact, footer) | hypothèse à confirmer | `site-src/build.py · cta(), footer(), build_index(), build_contact()` | Voir P15. Engagement de délai : à tenir ou à adoucir. |
| 9 | Agenda d'exemple Lun-Ven (7 rendez-vous, 4 « à relancer ») et 6 + 5 constats Sans / Avec NOVOLENS | exemple illustratif | `site-src/build.py · compare()` | Légende « Exemple illustratif » déjà présente : la garder. Retirer « Une croissance accélérée » (P6). |
| 10 | « Dès la première semaine » (gain de l'étape 1) | hypothèse à confirmer | `site-src/story.py · STEPS[0] (gain)` | Cohérent avec « Semaine 1 : cadrage » ; confirmer que l'atelier a lieu dans les 7 jours. |
| 11 | « Contacts sélectionnés et vérifiés » | hypothèse à confirmer | `site-src/story.py · STEPS[1] (bullets)` | Préciser la méthode de vérification (source, mise à jour) ou écrire « Contacts sélectionnés selon votre cible ». |
| 12 | « Ce qui ne passe pas le filtre ne vous est jamais livré » et « Zéro rendez-vous pour rien » | hypothèse à confirmer | `site-src/story.py · STEPS[2] (text, gain)` | Voir P3. Promesse absolue non sourcée. |
| 13 | « Des rendez-vous prêts à signer » (gain de l'étape 4) | hypothèse à confirmer | `site-src/story.py · STEPS[3] (gain)` | Voir P5. |
| 14 | Carte de livraison : DG, Industrie · 500 M€ · France, projet de modernisation, intérêt Élevé, prochain échange « Jeudi · 10h00 » | exemple illustratif | `site-src/build.py · delivery()` | Traité : la date fixe est remplacée par un jour de semaine. Reste à faire : ajouter la pastille « Exemple » sur la carte. |
| 15 | Trois cartes « Pour qui » : PME en croissance, ETI, Grands groupes (Dirigeants, Directions commerciales, Développement, Business units, Comptes stratégiques, Nouveaux marchés) | hypothèse à confirmer | `site-src/build.py · build_index() (cibles)` | Confirmer que les trois segments et les fonctions citées sont bien servis. |
| 16 | Section « Des dirigeants qui accélèrent leur croissance avec NOVOLENS » : témoignages de Thomas L., Sophie M., Marc D. + 3 cartes « Témoignage à venir » | exemple illustratif | `site-src/build.py · proof_wall(), tcard(), build_index() (preuves)` | Voir P6 et P12. Personnes fictives : à retirer avant mise en ligne (pratique commerciale trompeuse) ou à remplacer par de vrais avis signés. |
| 17 | « Des comptes stratégiques et un fort potentiel commercial » (statistique 3) | hypothèse à confirmer | `site-src/build.py · build_index() (.stats)` | Phrase non mesurable. Remplacer par « Des comptes choisis avec vous ». |
| 18 | « Un pipeline prévisible et mesurable » (statistique 4) | hypothèse à confirmer | `site-src/build.py · build_index() (.stats)` | Voir P7. |
| 19 | Animations des 4 encarts et du parcours : « 128 comptes ciblés », « 86 décideurs contactés », badge « +8 », « Directeur Général · Industrie », « Mon agenda · Novembre » | exemple illustratif | `site-src/ucards.py · u1() à u4() ; site-src/story.py · il1() à il5()` | Cohérents avec l'entonnoir d'exemple ; à mettre à jour en même temps que lui (voir comment-ca-marche). |

## Page Pourquoi nous (`pourquoi-nous.html`)

- **Titre SEO** : Pourquoi NOVOLENS
- **Description** : Pourquoi externaliser sa prospection B2B avec NOVOLENS : démarrage rapide, ciblage sur mesure, qualification rigoureuse et pilotage mesurable.
- **Balise h1** : unique

### Titres et textes

  - Accueil / Pourquoi nous
  - Pourquoi NOVOLENS
- **H1** : Vos commerciaux vendent. Nous remplissons leur agenda.
  - La prospection à froid demande du temps, de la régularité et du savoir-faire. Nous la prenons en charge de bout en bout pour que vos équipes se concentrent sur ce qu'elles font le mieux : convaincre et signer.
  - Réserver un échange de 15 min
  - Le constat
- **H2** : La prospection passe toujours après l'urgent.
  - Les relances s'oublient, les listes vieillissent, le pipeline se vide en silence. Une activité qui exige de la constance ne tient pas entre deux réunions clients.
  - Sans NOVOLENS
  - Avec NOVOLENS
- *Bloc commun : comparateur Sans / Avec NOVOLENS (voir « Blocs communs »).*
  - Six raisons
- **H2** : Ce que vous gagnez en nous confiant la prospection.
  - *H3* : Un démarrage rapide
  - Après le calibrage, la prospection démarre sans délai de recrutement ni de formation. Premiers résultats visés en moins d'un mois.
  - *H3* : Un ciblage sur mesure
  - Secteur, taille, fonction, signaux d'achat : chaque campagne part de votre client idéal, pas d'un fichier générique.
  - *H3* : Une qualification rigoureuse
  - Un rendez-vous n'est livré que si le décideur, le besoin et l'intérêt sont confirmés selon vos critères.
  - *H3* : L'expertise du démarchage à froid
  - Une équipe dédiée à la prospection, rompue aux objections et à la relance persévérante.
  - *H3* : Un pilotage mesurable
  - Reporting partagé, indicateurs de chaque étape et points réguliers pour ajuster la cible et le message.
  - *H3* : Une souplesse totale
  - Vous gardez la main sur la cible et le rythme, sans structure fixe à porter ni engagement sur l'échange initial.
  - Comparatif
- **H2** : Trois façons de remplir un pipeline.
  - Repères généraux, à adapter à votre situation.
  - Critère
  - Recruter en interne
  - Autres approches
  - NOVOLENS
  - Démarrage
  - Selon le recrutement
  - Selon le prestataire
  - Moins d'un mois visé
  - Coût
  - Fixe, chargé
  - Variable
  - Sur devis, adapté à votre cible
  - Expertise du froid
  - À construire
  - Variable
  - Équipe dédiée et rodée
  - Qualification
  - Dépend du profil
  - Dépend du prestataire
  - Critères définis avec vous
  - Visibilité
  - Dépend du CRM
  - Dépend du prestataire
  - Reporting partagé en continu
  - Flexibilité
  - Faible
  - Variable
  - Élevée, sans engagement initial
  - Nos engagements
- **H2** : Une prospection sérieuse, transparente, respectueuse.
  - Engagements proposés, à valider avant publication.
  - *H3* : Transparence
  - Vous voyez qui est contacté, ce qui est dit et où en est chaque piste.
  - *H3* : Conformité
  - Prospection B2B encadrée, respectueuse du RGPD et du droit d'opposition.
  - *H3* : Image de marque
  - Un discours validé avec vous, un ton professionnel, jamais de relance agressive.
- *Bloc commun : appel à l'action final (voir « Blocs communs »).*

### À valider

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | « Premiers résultats visés en moins d'un mois » ; « la prospection démarre sans délai de recrutement ni de formation » | hypothèse à confirmer | `site-src/build.py · build_pourquoi() (arguments, « zap »)` | Voir P2. Écrire « peut démarrer dès la fin du calibrage ». |
| 2 | « Un rendez-vous n'est livré que si le décideur, le besoin et l'intérêt sont confirmés selon vos critères » | hypothèse à confirmer | `site-src/build.py · build_pourquoi() (arguments, « shield »)` | Garder si le contrôle est réel ; sinon « Chaque rendez-vous est qualifié selon les critères définis avec vous ». |
| 3 | « Une équipe dédiée à la prospection, rompue aux objections » | hypothèse à confirmer | `site-src/build.py · build_pourquoi() (arguments, « phone »)` | Ajouter un fait vérifiable (taille ou ancienneté de l'équipe) ou supprimer « rompue aux objections ». |
| 4 | « Une souplesse totale » ; « sans structure fixe à porter ni engagement sur l'échange initial » | hypothèse à confirmer | `site-src/build.py · build_pourquoi() (arguments, « sliders »)` | Voir P8. |
| 5 | Comparatif : Recruter en interne (« Selon le recrutement », « Fixe, chargé », « Faible »), Autres approches (« Selon le prestataire », « Variable », « Dépend du prestataire »), NOVOLENS (« Moins d'un mois visé », « Élevée ») | hypothèse à confirmer | `site-src/build.py · build_pourquoi() (fonction row() et tableau)` | Traité : la colonne est renommée « Autres approches » et les jugements sur des tiers sont neutralisés. Reste à faire : faire confirmer par l'équipe les cases de la colonne NOVOLENS (« Moins d'un mois visé », « Équipe dédiée et rodée », « Élevée »). |
| 6 | Engagement « Transparence » : « Vous voyez qui est contacté, ce qui est dit et où en est chaque piste » | hypothèse à confirmer | `site-src/build.py · build_pourquoi() (engage)` | Vérifier que le reporting donne bien accès aux échanges ; sinon « Vous suivez l'avancement de chaque piste ». |
| 7 | Engagement « Conformité » : « respectueuse du RGPD et du droit d'opposition » | hypothèse à confirmer | `site-src/build.py · build_pourquoi() (engage), FAQ` | Voir P13. À faire relire par un juriste. |
| 8 | Engagement « Image de marque » : « jamais de relance agressive » | hypothèse à confirmer | `site-src/build.py · build_pourquoi() (engage)` | Voir P11. |
| 9 | Agenda d'exemple Sans / Avec NOVOLENS | exemple illustratif | `site-src/build.py · compare()` | Légende déjà présente. |

## Page Comment ça marche (`comment-ca-marche.html`)

- **Titre SEO** : Comment ça marche, NOVOLENS
- **Description** : La méthode NOVOLENS en trois étapes : calibrage, prospection, rendez-vous qualifiés livrés avec contexte et reporting.
- **Balise h1** : unique

### Titres et textes

  - Accueil / Comment ça marche
  - Notre méthode
- **H1** : De la stratégie au rendez-vous, nous nous occupons de tout.
  - Cinq étapes, une équipe experte en prospection à froid, un reporting clair. Vous n'intervenez que pour définir la cible et accueillir les rendez-vous.
- *Étapes 1 à 4 : identiques à l'accueil.*
  - Étape 5 sur 5
  - *H3* : Vous pilotez avec des chiffres, pas des impressions.
  - Un reporting partagé suit chaque étape, du compte ciblé au rendez-vous. Un point régulier ajuste la cible et le message.
  - Tableau de bord partagé en continu
  - Point de pilotage régulier
  - Ajustements rapides de cible et de message
  - Ce que vous gagnez
  - Un pipeline prévisible
  - Vos 30 premiers jours
- **H2** : Des premiers résultats en moins d'un mois.
  - Calendrier type, ajusté à votre marché.
  - Semaine 1
  - *H3* : Cadrage
  - Objectifs, cible, critères de qualification et message validés ensemble.
  - Semaine 2
  - *H3* : Lancement
  - Listes de contacts construites, séquences de prospection mises en route.
  - Semaine 3
  - *H3* : Premiers rendez-vous
  - Les premiers décideurs qualifiés arrivent dans votre agenda.
  - Semaine 4
  - *H3* : Bilan et ajustements
  - Point de pilotage : on affine la cible, le message, le rythme.
  - L'entonnoir
- **H2** : Du ciblage au rendez-vous, chaque étape se mesure.
  - Exemple d'un cycle de prospection : 128 entreprises ciblées donnent 8 rendez-vous planifiés. Vous voyez où se situe chaque contact et ce qui fonctionne.
  - Chiffres d'exemple, à titre illustratif.
  - Entreprises ciblées
  - 128
  - Décideurs contactés
  - 86
  - 67 %
  - Projets qualifiés
  - 24
  - 28 %
  - Rendez-vous planifiés
  - 8
  - 33 %
  - Notre livraison
- **H2** : Un dossier complet pour chaque rendez-vous.
  - Vos commerciaux arrivent préparés : profil, contexte, besoin, niveau d'intérêt et prochaine étape.
- *Bloc commun : carte de livraison d'un rendez-vous (voir « Blocs communs »).*
  - NOVOLENS · REPORTING
  - 128
  - Entreprises ciblées
  - 86
  - Décideurs contactés
  - 24
  - Projets qualifiés
  - 8
  - Rendez-vous planifiés
  - 1
  - 2
  - 4
  - 5
  - 7
  - 8
  - Sem. 1
  - Sem. 2
  - Sem. 3
  - Sem. 4
  - Sem. 5
  - Sem. 6
  - Données d'exemple, à titre illustratif.
  - Reporting
- **H2** : Un pipeline prévisible et mesurable.
  - Un tableau de bord partagé suit les entreprises ciblées, les décideurs contactés, les projets qualifiés et les rendez-vous planifiés. Vous pilotez avec des chiffres, pas des impressions.
  - En 4 étapes
- **H2** : La méthode en un coup d'œil.
  - Quatre étapes qui se suivent : l'action, et le moyen utilisé pour chacune.
- *Bloc commun : les 4 encarts « action et moyen » (voir « Blocs communs »).*
- *Bloc commun : appel à l'action final (voir « Blocs communs »).*

### À valider

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | « Trois étapes » dans la description SEO (la page montre 5 étapes, l'accueil 4) | hypothèse à confirmer | `site-src/build.py · build_methode() (hero) et page() de build_methode()` | Traité : l'introduction de la page dit maintenant « Cinq étapes ». Reste à faire : la description SEO dit encore « trois étapes » (appel `page(...)` de `build_methode()`), voir la proposition SEO. |
| 2 | « Vous n'intervenez que pour définir la cible et accueillir les rendez-vous » | hypothèse à confirmer | `site-src/build.py · build_methode() (hero)` | Contredit « validés avec vous » et le point de pilotage. Écrire « Votre rôle : définir la cible, valider le message, accueillir les rendez-vous ». |
| 3 | Étape 5 : « Tableau de bord partagé en continu », « Ajustements rapides de cible et de message » | hypothèse à confirmer | `site-src/story.py · STEPS[4]` | Confirmer l'outil de reporting et sa fréquence de mise à jour ; écrire « mis à jour chaque semaine » si c'est le cas. |
| 4 | Calendrier des 30 jours : S1 cadrage, S2 lancement, S3 premiers rendez-vous, S4 bilan | hypothèse à confirmer | `site-src/build.py · build_methode() (tl)` | Dépend de P2 ; mentionner que S3 est un objectif et non une garantie. |
| 5 | Entonnoir d'exemple : 128 entreprises ciblées, 86 décideurs contactés (67 %), 24 projets qualifiés (28 %), 8 rendez-vous planifiés (33 %) | exemple illustratif | `site-src/build.py · funnel() (rows) ; texte dans build_methode() (fun)` | Taux cohérents (86/128, 24/86, 8/24). Valeurs reprises dans laptop(), build_resultats(), v3_extra.py build_cas(), story.py il5(), ucards.py u3()/u4() : les changer partout. |
| 6 | Reporting d'exemple : tableau de bord 128 / 86 / 24 / 8 et courbe cumulée 1, 2, 4, 5, 7, 8 rendez-vous (8 en 6 semaines) | exemple illustratif | `site-src/build.py · laptop() (liste [3, 5, 8, 11, 14, 16])` | Traité : tableau de bord et courbe de `laptop()` sont cohérents avec l'entonnoir (8 rendez-vous). Reste à faire : l'illustration de l'étape 5 garde les barres 3, 5, 8, 11, 14, 17 (`story.py` · `il5()`, liste vals, hauteur v*11) : l'aligner. |
| 7 | « Téléphone, e-mail, LinkedIn » comme canaux de prospection | hypothèse à confirmer | `site-src/story.py · STEPS[1] ; site-src/ucards.py · section() (moyens)` | Confirmer les canaux utilisés (et la façon d'utiliser LinkedIn). |
| 8 | « Fiche de contexte et compte rendu » livrés avec chaque rendez-vous | hypothèse à confirmer | `site-src/build.py · delivery(), site-src/story.py · STEPS[3]` | Confirmer le contenu réel du dossier. |
| 9 | Fréquence du point de pilotage : « régulier » ici, « hebdomadaire » dans la formule Croissance | hypothèse à confirmer | `site-src/story.py · STEPS[4] ; site-src/build.py · build_tarifs() (plan Croissance)` | Aligner les deux : par exemple « point de pilotage toutes les deux semaines » si c'est la réalité. |

## Page Résultats (`resultats.html`)

- **Titre SEO** : Résultats NOVOLENS
- **Description** : Résultats NOVOLENS : rendez-vous qualifiés, premiers résultats en moins d'un mois, cas clients et témoignages de dirigeants.
- **Balise h1** : unique

### Titres et textes

  - Accueil / Résultats
  - Résultats
- **H1** : Des rendez-vous qui font avancer votre pipeline.
  - Les indicateurs que nous suivons, les cas clients qui arrivent et les retours de dirigeants.
  - +70 %
  - *H3* : de rendez-vous qualifiés*
  - Objectif de progression fixé avec vous dès le calibrage, mesuré dans le reporting.
  - < 1 mois
  - *H3* : pour les premiers résultats
  - Du calibrage aux premiers rendez-vous dans votre agenda.
  - 24
  - *H3* : projets qualifiés (exemple)
  - Sur 128 entreprises ciblées, 8 rendez-vous planifiés dans l'exemple de reporting.
  - Montée en puissance
- **H2** : Un pipeline qui se remplit semaine après semaine.
  - La régularité fait la différence : chaque semaine ajoute de nouveaux rendez-vous qualifiés à vos équipes. Dans l'exemple, 8 rendez-vous cumulés en 6 semaines.
  - Courbe d'exemple, à titre illustratif.
  - *H4* : Rendez-vous qualifiés cumulés, 6 semaines (exemple)
  - 1
  - 2
  - 4
  - 5
  - 7
  - 8
  - S1
  - S2
  - S3
  - S4
  - S5
  - S6
  - Secteurs ciblés
- **H2** : Trois secteurs où nous construisons nos premiers cas.
  - Un exemple de cas complet est présenté dans le gabarit de cas client.
  - *H3* : Industrie
  - Directeur Général
  - ETI
  - Des décideurs difficiles à joindre et des cycles de vente longs : le rendez-vous qualifié ouvre le dialogue au bon niveau.
  - *H3* : Santé
  - Direction Achats
  - Groupe
  - Des achats structurés, plusieurs interlocuteurs : une approche par compte et un contexte clair avant chaque échange.
  - *H3* : Tech & Logiciels
  - CEO
  - Scale-up
  - Des équipes qui vendent déjà : la prospection prend en charge les relances pour que le pipeline reste régulier.
  - Témoignage vidéo · 60 s
  - La parole aux dirigeants
- **H2** : Des retours qui parlent de rendez-vous, pas de promesses.
  - Les vidéos et verbatims clients apparaîtront ici dès leur validation. Les textes affichés dans le mur ci-dessous sont des exemples.
- *Bloc commun : mur de témoignages (voir « Blocs communs »).*
- *Bloc commun : appel à l'action final (voir « Blocs communs »).*

### À valider

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | « +70 % de rendez-vous qualifiés* » + phrase « Objectif de progression fixé avec vous dès le calibrage, mesuré dans le reporting. » | repris du visuel de départ | `site-src/build.py · build_resultats() (kp)` | Traité : « Chiffre à confirmer » est retiré et la phrase reprend P1. Reste à faire : valider le chiffre lui-même. |
| 2 | « < 1 mois pour les premiers résultats » | repris du visuel de départ | `site-src/build.py · build_resultats() (kp)` | Voir P2. |
| 3 | « 24 projets qualifiés (exemple) » ; « Sur 128 entreprises ciblées, 8 rendez-vous planifiés » | exemple illustratif | `site-src/build.py · build_resultats() (kp)` | Étiquette « exemple » présente : la garder. |
| 4 | Courbe « Rendez-vous qualifiés cumulés, 6 semaines (exemple) » : 1, 2, 4, 5, 7, 8 | exemple illustratif | `site-src/build.py · build_resultats() (liste vals)` | Traité : cumul de 8 rendez-vous, cohérent avec l'entonnoir. |
| 5 | Trois cartes « Secteurs ciblés » : Industrie (Directeur Général, ETI), Santé (Direction Achats, Groupe), Tech & Logiciels (CEO, Scale-up), chacune avec une phrase sur l'enjeu type | hypothèse à confirmer | `site-src/build.py · build_resultats() (cas)` | Traité : textes de remplissage, pastilles et compteurs retirés ; les phrases décrivent des enjeux types, pas des résultats. Reste à faire : confirmer que ces trois secteurs sont bien ceux visés. |
| 6 | Cadre vidéo « Témoignage vidéo · 60 s » et phrase « Les vidéos et verbatims clients apparaîtront ici dès leur validation. Les textes affichés dans le mur ci-dessous sont des exemples. » | hypothèse à confirmer | `site-src/build.py · build_resultats() (vid)` | Traité : l'étiquette d'emplacement est retirée et la phrase précise que les textes du mur sont des exemples. Reste à faire : retirer le cadre vidéo tant qu'aucun témoignage réel n'existe. |
| 7 | « Des retours qui parlent de rendez-vous, pas de promesses » | hypothèse à confirmer | `site-src/build.py · build_resultats() (vid)` | Voir P12. |
| 8 | Mur de témoignages (Thomas L., Sophie M., Marc D.) | exemple illustratif | `site-src/build.py · proof_wall()` | Voir P6. |
| 9 | Description SEO : « cas clients et témoignages de dirigeants » | hypothèse à confirmer | `site-src/build.py · build_resultats() (page())` | Annonce des contenus qui n'existent pas encore : remplacer (voir proposition SEO). |

## Page Cas client modèle (`cas-client.html`)

- **Titre SEO** : Cas client modèle NOVOLENS
- **Description** : Gabarit de cas client NOVOLENS : contexte, action, résultat et parole du dirigeant. Données d'exemple.
- **Balise h1** : unique

### Titres et textes

  - Accueil / Cas client modèle
  - Cas client · gabarit
- **H1** : Un cas client, du ciblage au contrat.
  - Ce gabarit montre comment un cas réel sera présenté : le contexte, l'action, le résultat et la parole du dirigeant. Toutes les données ci-dessous sont des exemples illustratifs.
  - Exemple illustratif, à remplacer par un client réel
  - Secteur
  - Industrie (exemple)
  - Taille
  - ETI (exemple)
  - Cible visée
  - Directions générales (exemple)
  - Durée
  - 3 mois (exemple)
  - Le contexte
- **H2** : Un agenda commercial qui ne se remplissait plus.
  - Une équipe commerciale compétente, mais sans temps pour prospecter les grands comptes. Les relances s'oubliaient et le pipeline dépendait de quelques clients historiques.
  - Sans NOVOLENS
  - Avec NOVOLENS
  - L'action
- **H2** : Quatre étapes, un seul objectif : le rendez-vous qualifié.
- *Bloc commun : les 4 encarts « action et moyen » (voir « Blocs communs »).*
  - NOVOLENS · REPORTING
  - 128
  - Entreprises ciblées
  - 86
  - Décideurs contactés
  - 24
  - Projets qualifiés
  - 8
  - Rendez-vous planifiés
  - 1
  - 2
  - 4
  - 5
  - 7
  - 8
  - Sem. 1
  - Sem. 2
  - Sem. 3
  - Sem. 4
  - Sem. 5
  - Sem. 6
  - Données d'exemple, à titre illustratif.
  - Le résultat
- **H2** : Un pipeline devenu prévisible.
  - Dans cet exemple, 128 comptes ciblés donnent 8 rendez-vous planifiés. Le reporting partagé montre où se situe chaque contact.
  - Entreprises ciblées
  - 128
  - Décideurs contactés
  - 86
  - 67 %
  - Projets qualifiés
  - 24
  - 28 %
  - Rendez-vous planifiés
  - 8
  - 33 %
  - Chiffres d'exemple, à titre illustratif.
  - Texte provisoire
  - Une équipe très professionnelle, déterminée et persévérante. Les rendez-vous sont bien qualifiés et nous gagnons un temps considérable.
  - Marc D. (exemple)
  - CEO · Tech & Logiciels
  - *H3* : Ce que ce cas contiendra
  - Le nom du client avec son accord, les objectifs de départ, le nombre de rendez-vous réels, le nombre de projets ouverts et la durée du cycle de vente.
- *Bloc commun : appel à l'action final (voir « Blocs communs »).*

### À valider

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | Fiche : Industrie, ETI, Directions générales, 3 mois | exemple illustratif | `site-src/v3_extra.py · build_cas() (fiche)` | Étiquettes « (exemple) » présentes. |
| 2 | « Une équipe commerciale compétente, mais sans temps pour prospecter… le pipeline dépendait de quelques clients historiques » | exemple illustratif | `site-src/v3_extra.py · build_cas() (ctx)` | Récit fictif ; à remplacer par le vrai contexte du client. |
| 3 | Entonnoir et tableau de bord 128 / 86 / 24 / 8, courbe hebdomadaire | exemple illustratif | `site-src/build.py · funnel(), laptop() ; site-src/v3_extra.py · build_cas() (res)` | Voir comment-ca-marche pour l'incohérence de la courbe. |
| 4 | « Un pipeline devenu prévisible » (titre de résultat) | hypothèse à confirmer | `site-src/v3_extra.py · build_cas() (res)` | Présente un résultat acquis dans un exemple. Écrire « Exemple de résultat : un pipeline mesurable » (P7). |
| 5 | Citation de Marc D. (exemple), CEO · Tech & Logiciels | exemple illustratif | `site-src/v3_extra.py · build_cas() (quote)` | Voir P6. |
| 6 | Page gabarit présente dans le sitemap et dans le pied de page (« Cas client (modèle) ») | hypothèse à confirmer | `site-src/v3_extra.py · build_seo() ; site-src/build.py · footer()` | Tant qu'aucun cas réel n'existe : ajouter `<meta name="robots" content="noindex">` dans cette page, retirer l'URL du sitemap et le lien du pied de page. |

## Page Tarifs (`tarifs.html`)

- **Titre SEO** : Tarifs NOVOLENS
- **Description** : Tarifs NOVOLENS : trois formules de prospection B2B externalisée, sur devis, adaptées à votre cible et à votre volume de rendez-vous.
- **Balise h1** : unique

### Titres et textes

  - Accueil / Tarifs
  - Tarifs
- **H1** : Une offre sur mesure, calée sur votre cible.
  - Le prix dépend de la cible, du volume de rendez-vous visé et de la durée. Nous construisons un devis après un échange de 15 minutes, sans engagement.
  - *H3* : Lancement
  - Tester sur une cible
  - Sur devis
  - Mission pilote d'un mois
  - Atelier de cadrage
  - Une cible et un message
  - Prospection et qualification
  - Rendez-vous livrés avec contexte
  - Bilan de fin de mission
  - Demander un devis
  - Le plus choisi
  - *H3* : Croissance
  - Un flux régulier de rendez-vous
  - Sur devis
  - Engagement mensuel, durée à définir
  - Tout Lancement
  - Plusieurs cibles et messages
  - Relances multicanales persévérantes
  - Reporting partagé en continu
  - Point de pilotage hebdomadaire
  - Demander un devis
  - *H3* : Grands comptes
  - Comptes stratégiques et nouveaux marchés
  - Sur devis
  - Approche sur mesure
  - Tout Croissance
  - Approche par compte, multi-interlocuteurs
  - Recherche de signaux d'achat
  - Coordination avec vos équipes ventes
  - Pilotage dédié
  - Demander un devis
  - Chaque devis est établi après un échange de 15 minutes.
  - Simulateur de gain
- **H2** : Combien vaut un flux de rendez-vous pour vous ?
  - Entrez vos propres chiffres. Le calcul se fait dans votre navigateur et n'est pas une promesse de résultat.
  - Valeurs d'exemple, remplacez-les par les vôtres
  - Valeur moyenne d'un client (€)
  - Rendez-vous qui deviennent clients (%)
  - Rendez-vous qualifiés par mois
  - Nouveaux clients par mois
  - 0
  - Chiffre d'affaires par mois
  - 0
  - Sur 12 mois
  - 0
  - Estimation calculée uniquement à partir de vos chiffres : rendez-vous par mois × taux × valeur d'un client.
  - Dans toutes les formules
- **H2** : Ce qui est toujours inclus.
  - *H4* : Ciblage sur mesure
  - *H4* : Prospection multicanale
  - *H4* : Qualification des besoins
  - *H4* : Prise de rendez-vous
  - *H4* : Dossier de contexte
  - *H4* : Reporting partagé
  - Votre devis
- **H2** : Comment nous construisons votre prix.
  - Un seul gros client signé suffit souvent à rentabiliser une mission. Nous partons donc de la valeur d'un client pour calibrer l'effort de prospection.
  - 1
  - *H4* : Valeur d'un client
  - Panier moyen, cycle de vente et taux de signature de vos équipes.
  - 2
  - *H4* : Cible et volume
  - Nombre de comptes à atteindre et de rendez-vous visés par mois.
  - 3
  - *H4* : Durée et rythme
  - Mission pilote ou engagement mensuel, selon votre besoin.
- *Bloc commun : appel à l'action final (voir « Blocs communs »).*

### À valider

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | Trois formules : Lancement (mission pilote d'un mois), Croissance (engagement mensuel, durée à définir), Grands comptes (approche sur mesure) et leurs listes de contenus | hypothèse à confirmer | `site-src/build.py · build_tarifs() (appels plan())` | Aucune offre n'a été fournie. Faire valider noms, durées et contenus. |
| 2 | Prix « Sur devis » pour les trois formules | hypothèse à confirmer | `site-src/build.py · build_tarifs() (plan(), bloc .price)` | Option : afficher « À partir de … € / mois » une fois les tarifs validés, ce qui augmente la conversion. |
| 3 | Badge « Le plus choisi » sur Croissance | hypothèse à confirmer | `site-src/build.py · build_tarifs() (plan(hot=True))` | Voir P9. Aucun client à ce jour : l'affirmation est invérifiable. |
| 4 | « Point de pilotage hebdomadaire » (Croissance) | hypothèse à confirmer | `site-src/build.py · build_tarifs()` | Aligner avec « régulier » ailleurs (voir comment-ca-marche). |
| 5 | Simulateur : 20 000 € de valeur client, 20 % de transformation, 8 rendez-vous par mois (résultat : 1,6 client, 32 000 € par mois, 384 000 € sur 12 mois) | exemple illustratif | `site-src/build.py · build_tarifs() (sim, attributs value=) ; site-src/app.js · bloc « V3 : rotateur, simulateur »` | Libellé « Valeurs d'exemple » présent. Ajouter « hors durée du cycle de vente » sous le résultat, car le calcul suppose une conversion immédiate. |
| 6 | « Un seul gros client signé suffit souvent à rentabiliser une mission » | hypothèse à confirmer | `site-src/build.py · build_tarifs() (how)` | Voir P10. |
| 7 | « Nous revenons vers vous sous 24 h avec une proposition adaptée » (appel à l'action) | hypothèse à confirmer | `site-src/build.py · build_tarifs() (cta)` | Confirmer que le devis est bien envoyé sous 24 h ; sinon « Nous vous répondons sous 24 h et envoyons une proposition ensuite ». |
| 8 | « Dans toutes les formules » : ciblage sur mesure, prospection multicanale, qualification des besoins, prise de rendez-vous, dossier de contexte, reporting partagé | hypothèse à confirmer | `site-src/build.py · build_tarifs() (inc)` | Confirmer que ces six éléments sont inclus partout, y compris dans Lancement. |
| 9 | Note « Chaque devis est établi après un échange de 15 minutes. » | hypothèse à confirmer | `site-src/build.py · build_tarifs() (pl)` | Traité : la remarque interne est remplacée par cette phrase. Reste à faire : confirmer le principe du devis après échange. |

## Page FAQ (`faq.html`)

- **Titre SEO** : FAQ NOVOLENS
- **Description** : Réponses aux questions fréquentes sur NOVOLENS : rendez-vous qualifiés, délais, méthode, reporting, engagement et tarifs.
- **Balise h1** : unique

### Titres et textes

  - Accueil / FAQ
  - Questions fréquentes
- **H1** : Tout ce que vous voulez savoir avant de nous parler.
  - Une question qui n'est pas ici ? Réservez un échange de 15 minutes, un expert vous répond.
  - Tout ouvrir
  - Qu'est-ce qu'un rendez-vous qualifié ?
  - C'est un échange confirmé avec un décideur dont nous avons vérifié la fonction, le besoin, l'intérêt et la disponibilité, selon les critères définis avec vous lors du calibrage.
  - En combien de temps obtient-on les premiers résultats ?
  - Nous visons les premiers rendez-vous en moins d'un mois après le cadrage. Le délai exact dépend de votre cible et de votre marché.
  - À quelles entreprises s'adresse NOVOLENS ?
  - Aux PME en croissance, aux ETI et aux grands groupes qui vendent en B2B et veulent remplir leur pipeline avec des décideurs, notamment dans l'industrie, la santé, la tech et les services B2B.
  - Comment prospectez-vous ?
  - Par une approche multicanale personnalisée : appels, e-mails et messages professionnels, avec des relances persévérantes jusqu'à obtenir une réponse claire.
  - Qui contacte mes prospects, et en quel nom ?
  - Une équipe dédiée, formée à votre offre. Le discours et le positionnement sont validés avec vous avant le lancement.
  - Comment suis-je tenu informé ?
  - Vous disposez d'un reporting partagé qui suit chaque étape, du ciblage au rendez-vous planifié, et d'un point de pilotage régulier.
  - Que se passe-t-il après le rendez-vous ?
  - Vos équipes prennent le relais avec un dossier complet : profil du décideur, contexte, besoin identifié, niveau d'intérêt et compte rendu.
  - Y a-t-il un engagement ?
  - L'échange initial de 15 minutes est sans engagement. Ensuite, la durée dépend de la formule choisie, de la mission pilote à l'engagement mensuel.
  - Comment sont calculés vos tarifs ?
  - Sur devis, selon la cible, le volume de rendez-vous visé et la durée. Nous partons de la valeur d'un client pour calibrer l'effort.
  - Et pour les données personnelles ?
  - Nous menons une prospection B2B encadrée, respectueuse du RGPD, avec un droit d'opposition simple pour les personnes contactées.
- *Bloc commun : appel à l'action final (voir « Blocs communs »).*

### À valider

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | Q1 : un rendez-vous qualifié vérifie « la fonction, le besoin, l'intérêt et la disponibilité » | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 0)` | Confirmer les quatre critères réellement contrôlés. |
| 2 | Q2 : « premiers rendez-vous en moins d'un mois après le cadrage » | repris du visuel de départ | `site-src/build.py · liste FAQ (index 1)` | Formulation de référence pour P2. |
| 3 | Q3 : clients visés dont « l'industrie, la santé, la tech et les services B2B » | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 2)` | Aucun client à ce jour dans ces secteurs : écrire « notamment » seulement si l'équipe y a de l'expérience, sinon « tous secteurs B2B ». |
| 4 | Q4 : « appels, e-mails et messages professionnels, avec des relances persévérantes jusqu'à obtenir une réponse claire » | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 3)` | Fixer un nombre maximal de relances pour rester cohérent avec « jamais de relance agressive ». |
| 5 | Q5 : la question « en quel nom ? » reçoit une réponse sur l'équipe mais pas sur le nom utilisé | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 4)` | Réponse proposée : « Nous contactons vos prospects en votre nom, avec un discours et une signature validés par vous, ou sous l'identité de NOVOLENS si vous préférez rester discret. Le choix se fait au calibrage. » (à valider). |
| 6 | Q6 : « reporting partagé » et « point de pilotage régulier » | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 5)` | Voir comment-ca-marche (fréquence). |
| 7 | Q7 : dossier après rendez-vous (profil, contexte, besoin, niveau d'intérêt, compte rendu) | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 6)` | Confirmer le contenu réel du dossier. |
| 8 | Q8 : échange de 15 minutes sans engagement, durée selon la formule (« de la mission pilote à l'engagement mensuel ») | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 7)` | Ajouter la durée minimale d'engagement et le préavis une fois fixés. |
| 9 | Q9 : tarifs « sur devis, selon la cible, le volume et la durée » | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 8)` | Cohérent avec la page tarifs. |
| 10 | Q10 : « prospection B2B encadrée, respectueuse du RGPD, avec un droit d'opposition simple » | hypothèse à confirmer | `site-src/build.py · liste FAQ (index 9)` | Voir P13. |
| 11 | Données structurées FAQPage : reprennent les 10 réponses ci-dessus | hypothèse à confirmer | `site-src/build.py · build_faq() (ld, généré depuis la liste FAQ)` | Une seule modification dans la liste FAQ met à jour la page et les données structurées. |

## Page Contact (`contact.html`)

- **Titre SEO** : Contact NOVOLENS
- **Description** : Réservez un échange de 15 minutes avec un expert NOVOLENS pour parler de vos objectifs de croissance. Sans engagement, réponse sous 24 h.
- **Balise h1** : unique

### Titres et textes

  - Accueil / Contact
  - Échange stratégique
- **H1** : Parlons de vos objectifs de croissance.
  - Un échange de 15 minutes avec un expert NOVOLENS pour comprendre vos enjeux et voir comment nous pouvons vous apporter des rendez-vous qualifiés.
  - Prénom *
  - Nom *
  - E-mail professionnel *
  - Téléphone
  - Entreprise *
  - Fonction *
  - Taille de l'entreprise
  - PME (10 à 250 salariés)
  - ETI (250 à 5 000 salariés)
  - Grand groupe (5 000 salariés et plus)
  - Votre objectif
  - Créneau souhaité (facultatif)
  - *H4* : Mardi
  - 9h30
  - 11h00
  - 14h30
  - 16h00
  - *H4* : Mercredi
  - 9h30
  - 11h00
  - 14h30
  - 16h00
  - *H4* : Jeudi
  - 9h30
  - 11h00
  - 14h30
  - 16h00
  - Aucun créneau choisi.
  - J'accepte d'être recontacté au sujet de ma demande.
  - Réserver mon échange
  - Aperçu : ce formulaire n'envoie rien tant qu'il n'est pas relié à votre messagerie ou à votre agenda.
  - *H3* : Merci, votre demande est prête.
  - Un expert NOVOLENS vous répond sous 24 h.
  - Retour à l'accueil
  - Et ensuite ?
- **H2** : Trois étapes, sans engagement.
  - 1
  - *H4* : Réponse sous 24 h
  - Un expert confirme le créneau ou vous propose une alternative.
  - 2
  - *H4* : Échange de 15 minutes
  - Vos objectifs, votre cible, vos contraintes. Nous écoutons d'abord.
  - 3
  - *H4* : Proposition sur mesure
  - Si cela a du sens pour vous, nous vous envoyons un devis adapté.
  - Sans engagement
  - Réponse sous 24 h
  - Échange avec un expert
  - Vous préférez écrire ? contact@novolens.fr (adresse à confirmer)

### À valider

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | Tailles d'entreprise : PME (10 à 250 salariés), ETI (250 à 5 000), Grand groupe (5 000 et plus) | hypothèse à confirmer | `site-src/build.py · build_contact() (select #taille)` | Seuils usuels (UE pour les PME, INSEE pour les ETI). Confirmer qu'on ne cible pas les entreprises de moins de 10 salariés. |
| 2 | Créneaux : mardi, mercredi, jeudi à 9h30, 11h00, 14h30, 16h00 | exemple illustratif | `site-src/build.py · build_contact() (liste days)` | Traité : les dates sont remplacées par des jours de semaine (plus rien de périmé). Reste à faire : relier ces créneaux à de vraies disponibilités ou à un agenda en ligne (guide, section d). |
| 3 | « Un expert NOVOLENS vous répond sous 24 h » (message de succès et étape 1) | hypothèse à confirmer | `site-src/build.py · build_contact() (success, side)` | Voir P15. |
| 4 | « Échange de 15 minutes : vos objectifs, votre cible, vos contraintes » | hypothèse à confirmer | `site-src/build.py · build_contact() (side)` | Confirmer la durée. |
| 5 | Adresse contact@novolens.fr « (adresse à confirmer) » | hypothèse à confirmer | `site-src/build.py · footer() ; build_contact() (side)` | Traité dans le pied de page (la mention « à confirmer » y est retirée). Reste à faire : remplacer l'adresse par la vraie et retirer « (adresse à confirmer) » dans la colonne de contact (`build_contact()`, bloc side). |
| 6 | Case « J'accepte d'être recontacté au sujet de ma demande » | hypothèse à confirmer | `site-src/build.py · build_contact() (consent)` | Ajouter sous le bouton : responsable du traitement, finalité, durée de conservation, droits et lien vers la politique de confidentialité. |
| 7 | Note « Aperçu : ce formulaire n'envoie rien tant qu'il n'est pas relié… » | hypothèse à confirmer | `site-src/build.py · build_contact() (form)` | Vraie à ce jour (l'envoi est simulé dans app.js). À supprimer dès que le formulaire est branché. |
| 8 | Neuf champs dans le formulaire | hypothèse à confirmer | `site-src/build.py · build_contact()` | Le dossier de choix recommandait 5 champs ou moins : passer Téléphone, Taille et Objectif en facultatifs ou les retirer. |

## Page introuvable (`404.html`)

  - Erreur 404
- **H1** : Cette page n'existe pas.
  - Le lien est peut-être ancien. Revenez à l'accueil ou réservez directement un échange.
  - Retour à l'accueil Réserver un échange

Aucune affirmation à valider.

## Affirmations du pied de page (toutes les pages)

| # | Affirmation | Statut | Où la modifier | Recommandation |
|---|---|---|---|---|
| 1 | Adresse contact@novolens.fr | hypothèse à confirmer | `site-src/build.py · footer()` | Traité : la mention « (à confirmer) » est retirée du pied de page. Reste à faire : remplacer par l'adresse réelle. |
| 2 | « Réponse sous 24 h » | hypothèse à confirmer | `site-src/build.py · footer()` | Voir P15. |
| 3 | Ligne sur mentions légales, confidentialité et CGV : retirée du pied de page | hypothèse à confirmer | `site-src/build.py · footer()` | Traité : texte de remplissage retiré. Reste à faire : créer les trois pages et leurs liens (L04, section e, avec la liste des champs obligatoires). |
| 4 | « © 2026 NOVOLENS. Tous droits réservés. » | hypothèse à confirmer | `site-src/build.py · footer()` | Ajouter la forme juridique exacte de la société une fois connue. |
| 5 | « * Objectif indicatif. Les chiffres, exemples de cas et coordonnées de cette maquette sont donnés à titre illustratif. » | exemple illustratif | `site-src/build.py · footer()` | Traité : remplace l'ancienne note. Reste à faire : retirer cette note à la mise en ligne, une fois chiffres et coordonnées validés. |

## Synthèse

| Page | Affirmations à valider |
|---|---|
| Accueil | 19 |
| Pourquoi nous | 9 |
| Comment ça marche | 9 |
| Résultats | 9 |
| Cas client modèle | 6 |
| Tarifs | 9 |
| FAQ | 11 |
| Contact | 8 |
| Pied de page | 5 |
| **Total** | **85** |

S'y ajoutent 15 promesses non sourcées reformulées (références P1 à P15) et 7 zones de texte interne à remplacer.
