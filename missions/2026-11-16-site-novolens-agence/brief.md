# BRIEF — Site NOVOLENS niveau agence

mission: site-novolens-agence
date: 2026-11-16
mode: complete
verdict: lancer sous condition
verrouillé: non

## À retenir
- Objectif : un site vitrine multi-pages NOVOLENS abouti, rapide, accessible, animé, prêt à recevoir les vraies données.
- Livré dans le dépôt (sources du site, design system, contenu, guide, audit) et en V3 d'artefact privé. V1 et V2 restent intactes.
- Niveau « agence » défini par une liste vérifiable, sans promesse d'équivalence de prix.
- Ce que MAESTRO fait seul : benchmark, débat d'équipe, production page par page, audit chiffré, livraison.
- Ce qui demande votre accord : mise en ligne réelle, dépense, tout envoi, fusion ou PR.
- Conditions : (1) chiffres, tarifs et témoignages restent des exemples étiquetés tant que vous ne fournissez pas les vrais ; (2) pas de vidéo générée ni de tournage dans cette mission ; (3) l'e-mail de contact et les mentions légales restent des valeurs d'exemple.
- Options d'exécution proposées : sous-agents en parallèle oui (vous avez demandé toute la puissance), reprise automatique non, modèle imposé aucun.

## Objectif
Livrer à NOVOLENS un site vitrine français de 8 pages, de finition professionnelle, qui explique la valeur (des rendez-vous qualifiés sans effort de prospection) et amène à réserver un échange de 15 minutes.

## Définition de « fini »
- 8 pages : accueil, pourquoi nous, comment ça marche, résultats, tarifs, FAQ, contact, page cas client modèle. Chacune ouvre sans erreur console, sans débordement horizontal à 400, 820 et 1360 px.
- Chaque étape de la méthode a une animation qui montre l'action, le moyen et le gain client.
- Contrastes de texte AA vérifiés par calcul ; focus clavier visible ; navigation entièrement utilisable au clavier ; `prefers-reduced-motion` respecté.
- Poids : aucune image de plus de 250 Ko, pages HTML de moins de 60 Ko hors images ; chaque page a un titre, une description et une balise `h1` unique ; FAQ en données structurées.
- Tout chiffre, prix ou témoignage non fourni est étiqueté « exemple » ; aucun « à compléter » ni espace réservé vide.
- Audit : score d'au moins 80/100 par livrable, aucun critère à 0 ou 1.

## Livrables
| id | livrable | type | format et extension | langue | canal de livraison | grille d'audit |
|---|---|---|---|---|---|---|
| L01 | Site NOVOLENS V3 (8 pages) | page web | HTML, CSS, JS, images | français | dossier `livrables/site/` du dépôt + artefact privé V3 | page web (ad hoc ci-dessous) |
| L02 | Design system | page web | `design-system.html` | français | dossier du dépôt | page web |
| L03 | Contenu source relu | texte | `contenu.md` | français | dossier du dépôt | texte |
| L04 | Guide d'intégration et de remplacement des médias et données | texte | `guide.md` | français | dossier du dépôt | texte |
| L05 | Rapport d'audit chiffré du site | texte | `rapport-audit.md` | français | dossier du dépôt | texte |

Grille ad hoc pour L01 et L02 (100 points) : fidélité à la charte et cohérence visuelle 20 ; clarté de la valeur en un coup d'œil (action, moyen, gain) 20 ; accessibilité et responsive vérifiés 20 ; performance et SEO technique 20 ; qualité du texte et exactitude (aucune affirmation non sourcée) 20. Vérification concrète : rendu Playwright à 3 largeurs, console sans erreur, calcul des contrastes, poids des fichiers, validation des liens internes.

## Périmètre
- Inclus : refonte V3 à partir de V1/V2, réécriture du texte, design system, animations illustratives, photos Unsplash pleines, SEO technique, guide, audit, publication en artefact privé V3.
- Exclu : tournage photo/vidéo, vidéo générée, logo et identité de marque, vrais cas clients, intégration CRM, agenda ou messagerie, mise en ligne sur un domaine, mentions légales rédigées, tests utilisateurs.

## Contraintes
- Budget : aucune dépense. Images Unsplash libres de droits uniquement.
- Délai : une session de travail longue ; état poussé sur la branche après chaque livrable.
- Ton ou voix : professionnel, direct, légèrement institutionnel pour s'adresser aux dirigeants de PME, ETI et grands groupes.
- Langue : français.
- À ne surtout pas faire : thème sombre, écraser V1 ou V2, inventer des chiffres sans les étiqueter, copier hatmada.io, promettre une valeur facturée.

## Décisions de fond
| décision | choix | pourquoi | écarté | réversible (coût) |
|---|---|---|---|---|
| Architecture | site statique multi-pages | fiable, rapide, hébergeable partout | framework | oui, faible |
| Conversion | un seul appel à l'action par page | pratiques B2B récurrentes | appels multiples | oui, faible |
| Médias | animation HTML/SVG + photos Unsplash, zones vidéo prêtes | gratuit, léger, publiable | vidéo générée | oui, faible |
| Niveau agence | liste de critères vérifiables | mesurable et honnête | équivalence de prix | oui, nul |

## Doctrine d'arbitrage
Ordre de tranchage par défaut : contrainte dure du brief, puis fiable > évident > beau, puis l'option la plus réversible.
Règles propres à cette mission : en cas de doute entre un effet spectaculaire et la lisibilité de l'action, la lisibilité gagne ; aucune animation ne cache le texte à l'arrêt.

## Stories de vérification
- Étant donné un visiteur sur l'accueil, quand il fait défiler la section « 4 étapes », alors chaque étape montre une animation de l'action, le moyen utilisé et le gain client.
- Étant donné un visiteur au clavier, quand il tabule, alors chaque lien et bouton a un focus visible et le menu mobile s'ouvre et se ferme.
- Étant donné un visiteur qui remplit le formulaire sans e-mail valide, quand il envoie, alors un message d'erreur clair apparaît sans quitter la page.
- Étant donné un visiteur avec mouvement réduit, quand il ouvre le site, alors tout le contenu est visible sans animation.
Sans objet pour ce type de livrable : non

## Direction visuelle
Couleurs : violet #4B39DD et #7656F5, jaune de surlignage #FFD84D, encre #14102F, fonds blanc #FFFFFF et dégradé violet #F1EBFF vers #CDBBFF en alternance. Typographies : Newsreader (titres, gras) et Inter (texte), Caveat pour les annotations. Rayons 20 à 28 px. Photos pleines, non transparentes. Thème clair uniquement. Référence d'inspiration : animations et structure de hatmada.io, sans copie.

## Actions exigeant un accord humain
Publication du site sur un domaine, dépense de crédits, envoi de message, fusion, ouverture de PR, suppression de V1 ou V2.

## Options d'exécution
- sous-agents en parallèle : oui
- reprise automatique : non
- modèle imposé : aucun

## Hypothèses, risques et plan B
- Hypothèse retenue : les sources V1/V2 sont la base ; elles sont recopiées dans le dépôt pour ne pas être perdues avec le conteneur.
- Risque : promesse « niveau agence à 40-60 k€ » perçue comme garantie — parade : la liste vérifiable est le seul engagement, annoncée au gate.
- Risque : chiffres inventés pris pour réels — parade : étiquette « exemple » sur chaque chiffre non fourni.
- Risque : perte des fichiers avec le conteneur — parade : commit et push après chaque livrable.
- Risque : sous-agents qui divergent de style — parade : design system produit en premier et imposé à chaque agent.
- Plan B : si les sous-agents ne sont pas disponibles, production séquentielle page par page.

## Matériaux fournis
Visuel de départ NOVOLENS, V1 et V2 publiées, sources dans le dossier de session, photos Unsplash déjà téléchargées.

## Avenants
Journal des changements de périmètre après verrouillage (ajoutés par `lock-brief.sh --avenant`).
