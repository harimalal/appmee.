# BRIEF — Site de vente PROSENS

mission: prosens-site-vente
date: 2026-11-06
mode: standard
verdict: lancer sous condition
verrouillé: non

## À retenir
- Objectif : une page de vente PROSENS qui fait réserver un échange à des dirigeants de PME et de grands groupes qui veulent externaliser leur prospection et leur closing.
- Promesse : on ne livre pas des rendez-vous, on livre des clients. Rendez-vous qualifiés confirmés dans l'agenda du client, closing assuré par un commercial senior.
- Différenciation : la concurrence vend le rendez-vous et s'arrête là. PROSENS montre sa définition écrite d'un rendez-vous qualifié, le closing et le parcours de son fondateur. Aucune garantie de volume non étayée.
- Design : moderne, sans stéréotype, sections animées, un moment fort (le rendez-vous qui se remplit dans l'agenda), version sans mouvement complète.
- Livrables : L01 le site (une page autonome, prête à déposer) et L02 le guide de mise en ligne avec les pièces à fournir.
- Condition : l'utilisateur fournit un lien d'agenda ou une adresse de contact, et précise nom, titre et périmètre des ×4 / ×5 du fondateur.
- Fait seul : benchmark, rédaction, design, développement, vérifications, aperçu privé. Demandera un accord : toute publication, tout nom de domaine, toute dépense.

## Objectif
Une page de vente unique pour PROSENS, au français soigné, qui convertit un dirigeant de PME ou de grand groupe en un échange de 30 minutes réservé dans l'agenda de PROSENS.

## Définition de « fini »
- Un dirigeant comprend en 5 secondes ce que fait PROSENS et voit le bouton d'échange sans faire défiler.
- Le bouton principal ouvre le moyen de contact fourni, et apparaît au moins 4 fois dans la page.
- Aucune donnée inventée : chiffres, clients, logos et témoignages absents ou marqués comme déclarations du fondateur.
- Version complète sans mouvement quand `prefers-reduced-motion` est actif ; zéro erreur console ; aucun défilement horizontal de 375 à 1440 pixels.
- Audit : 80/100 minimum, aucun critère à 0 ou 1, 2 passes maximum.

## Livrables
| id | livrable | type | format et extension | langue | canal de livraison | grille d'audit |
|---|---|---|---|---|---|---|
| L01 | Site PROSENS, page de vente complète | Page web | un dossier `L01-prosens/` avec `index.html` autonome (CSS et JS inclus, polices Google Fonts) | français | fichiers du dépôt, aperçu privé en artefact | ad hoc (ci-dessous) |
| L02 | Guide de mise en ligne et pièces à fournir | Document formel | `.md` | français | fichier du dépôt | Document formel |

Grille ad hoc de L01 (somme 100) :
- Clarté de l'offre en 5 secondes et appel à l'action visible : 20
- Différenciation fondée sur le benchmark (méthode, closing, définition du qualifié) : 15
- Honnêteté des preuves : aucune donnée inventée, déclarations attribuées : 15
- Design sans stéréotype, cohérent, lisible de 375 à 1440 pixels : 20
- Mouvement maîtrisé : un moment fort, discret ailleurs, version sans mouvement complète : 15
- Qualité technique : accessibilité (contraste, clavier), console propre, poids raisonnable : 15
Vérification mécanique : captures Playwright à 375, 768 et 1440 pixels, contrôle de la console, du défilement horizontal et de la navigation clavier.

## Périmètre
- Inclus : une page, ses sections (accroche, problème, mécanisme animé, offre PME et grands groupes, méthode en étapes, définition du rendez-vous qualifié, fondateur, objections, appel à l'action final), le texte, le design, le mouvement, le développement, les vérifications.
- Exclu : publication, achat de domaine, branchement d'un formulaire ou d'un outil d'agenda, référencement payant, photos de banque d'images, pages supplémentaires, mentions légales (à fournir par l'utilisateur, le guide les liste), SEO avancé.

## Contraintes
- Budget : aucune dépense.
- Délai : une session.
- Ton ou voix : direct, précis, d'un praticien qui a vendu sur le terrain ; vouvoiement ; pas de jargon marketing.
- Langue : français.
- À ne surtout pas faire : dégradé violet-bleu ; mains qui se serrent ou personnages de banque d'images ; emoji en guise de puces ; cartes toutes identiques à coins arrondis avec barre d'accent ; titres « Boostez », « Révolutionnez », « solutions innovantes » ; tout centrer ; chiffres ou clients inventés ; garantie de volume.

## Décisions de fond
| décision | choix | pourquoi | écarté | réversible (coût) |
|---|---|---|---|---|
| Angle de positionnement | Méthode terrain, closing inclus, définition écrite du rendez-vous qualifié | La concurrence vend le rendez-vous ; une garantie de volume n'est pas étayée | Garantie de volume ; baseline générique | oui, un titre et une section |
| Structure | Une page en long scroll narratif avec deux entrées PME et grands groupes | Demande de l'utilisateur ; se vérifie et se publie en un geste | Site multi-pages | oui |
| Technique de mouvement | CSS et IntersectionObserver, un moment fort, repli sans mouvement | Léger, indexable, accessible | Bibliothèque de scroll sur toute la page | oui, GSAP possible plus tard |
| Chemin de conversion | Bouton unique vers un lien d'agenda, répété 4 fois | Peu de friction, aucun compte externe | Formulaire de qualification | oui |
| Direction visuelle | Tranchée en phase 2 (décision structurante), consignée dans decisions.md | Besoin d'un débat entre rôles | — | oui |

## Doctrine d'arbitrage
Ordre de tranchage par défaut : contrainte dure du brief, puis fiable > évident > beau, puis l'option la plus réversible.
Règles propres à cette mission : une affirmation non étayée est soit retirée, soit présentée comme déclaration du fondateur ; le mouvement ne passe jamais avant la lisibilité.

## Stories de vérification
- Étant donné un dirigeant sur mobile (375 pixels), quand la page s'ouvre, alors il lit la promesse de PROSENS et voit le bouton d'échange sans faire défiler.
- Étant donné un visiteur qui fait défiler la page, quand il atteint la section du parcours, alors les étapes (prospection, qualification, rendez-vous dans l'agenda, closing) s'animent ; avec `prefers-reduced-motion`, la même information est affichée sans mouvement.
- Étant donné un visiteur qui clique sur un bouton d'échange, quand le lien d'agenda est fourni, alors la prise de rendez-vous s'ouvre dans un nouvel onglet.
- Étant donné un directeur d'un grand groupe, quand il choisit l'entrée « Grands groupes », alors il voit l'offre adaptée (volumes, gouvernance, reporting) sans quitter la page.
- Étant donné un visiteur au clavier, quand il navigue, alors chaque bouton et lien est atteignable et visiblement focalisé.
Sans objet pour ce type de livrable : non

## Direction visuelle
Tranchée en phase 2 (décision structurante), avec les interdits de la section Contraintes. Pas de logo imposé : un logotype typographique PROSENS est créé dans la page.

## Actions exigeant un accord humain
Publication du site (Cloudflare Pages ou autre), achat ou branchement d'un nom de domaine, branchement d'un outil d'agenda ou de réception de formulaire, rendre l'artefact d'aperçu public ou le partager, toute dépense, toute génération qui consomme des crédits.

## Options d'exécution
- sous-agents en parallèle : non
- reprise automatique : non
- modèle imposé : aucun

## Hypothèses, risques et plan B
- Hypothèse retenue : marché francophone, offre sans prix affiché, vouvoiement, pas de charte existante.
- Hypothèse retenue : les résultats du fondateur (×4 et ×5 de chiffre d'affaires sur des marchés B2B émergents) sont présentés comme déclarés par lui, sans détail inventé.
- Risque : chiffres du fondateur non étayés — parade : formulation attribuée, et liste des pièces à fournir dans L02.
- Risque : page trop sobre — parade : passage à une bibliothèque de scroll après décision en avenant.
- Risque : le lien d'agenda n'arrive pas — plan B : adresse de contact ; sans l'un ni l'autre, la page ne peut pas être finalisée (condition du verdict).

## Matériaux fournis
Aucun fichier. La dictée de l'utilisateur : offre, cibles, ton, profil du fondateur.

## Avenants
Journal des changements de périmètre après verrouillage (ajoutés par `lock-brief.sh --avenant`).
