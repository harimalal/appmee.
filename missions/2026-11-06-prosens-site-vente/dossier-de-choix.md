# DOSSIER DE CHOIX — prosens-site-vente

Sources détaillées en phase 1 (BENCHMARK.md). Chiffres de prix et de conversion : indicatifs, issus de sources commerciales.

## Choix #1 : angle de positionnement

| Option | Cas réels | Mécanisme | Coût | Risque | Réversible |
|---|---|---|---|---|---|
| A. Garantie de volume | Belkins (« 100+ guaranteed appts / year », à partir de 5 000 $) | Réduit le risque perçu, promesse chiffrée en tête | Engagement ferme à tenir | Promesse invérifiable par nous ; le même acteur nuance ailleurs ses garanties | Oui |
| B. Expertise terrain du fondateur | Lead Camp (agence locale, fondée en 2015) ; CIENCE (méthode « GTM System » en 5 jours) | La méthode et la personne rassurent | Exige des preuves réelles | Chiffres ×4 ×5 non étayés = perte de crédibilité | Oui |
| C. Transparence et closing inclus | Annonces freelances au rendez-vous (définition du « qualifié » souvent floue : le client doit la vérifier) | Définir noir sur blanc ce qu'est un rendez-vous qualifié, aller jusqu'au closing | Plus de rédaction | Peu | Oui |

**Recommandation : B + C**, sans garantie de volume. Parce que : la concurrence vend le rendez-vous, pas le client signé ; une garantie chiffrée n'est pas vérifiable aujourd'hui et le copier-coller d'une promesse de marché détruirait la différence. Ce qui ferait changer d'avis : l'utilisateur confirme un engagement chiffré qu'il peut tenir contractuellement.

## Choix #2 : structure de la page

| Option | Cas réels | Mécanisme | Coût | Risque | Réversible |
|---|---|---|---|---|---|
| A. Long scroll narratif en une page | Pages produit de Linear et Stripe (démo ou dégradé liés au défilement) | Un fil : problème, mécanisme, preuve, offre, fondateur, objections, appel à l'action | Écriture soignée | Page longue si mal rythmée | Oui |
| B. Site multi-pages | Sites d'agences d'externalisation | Une page par service | Plus de contenus à inventer | Dilution, plus de pages sans preuves | Oui |

**Recommandation : A**, avec deux entrées visibles « PME » et « Grands groupes » dans la même page. Parce que : l'utilisateur demande une page de vente ; une seule page se vérifie et se publie en un geste.

## Choix #3 : technique de mouvement

| Option | Cas réels | Mécanisme | Coût | Risque | Réversible |
|---|---|---|---|---|---|
| A. CSS et IntersectionObserver, sans dépendance | Principe de sobriété relevé sur Stripe, Linear, Vercel : peu d'animations, bien choisies, un moment fort | Léger, indexable, fonctionne hors ligne | Effets limités à ce que fait CSS | Aucun | Oui |
| B. Bibliothèque de scroll (GSAP) | Pages « scrollytelling » très animées | Chorégraphies riches | Dépendance, poids, accessibilité à gérer | Performance et référencement | Oui |

**Recommandation : A**, avec un moment fort (le parcours du rendez-vous qui se remplit dans l'agenda) et des mouvements discrets ailleurs ; version complète sans mouvement pour `prefers-reduced-motion`. Parce que : les guides relevés placent les risques sur la performance et le référencement ; B reste possible si A bride le design.

## Choix #4 : chemin de conversion

| Option | Cas réels | Mécanisme | Coût | Risque | Réversible |
|---|---|---|---|---|---|
| A. Un bouton unique vers un agenda | Appels à réserver un échange (pages d'« appointment setting » de SalesHive et Belkins) | Peu de friction | Lien d'agenda à fournir | Aucun | Oui |
| B. Formulaire de qualification | Pages de demande d'appel | Qualifie avant l'échange | Réception à brancher (compte externe) | Fuite de contacts, dépendance | Oui |

**Recommandation : A**, répété 4 fois dans la page, avec deux libellés selon le segment. Repères de marché (indicatifs, sources commerciales) : pages de demande d'appel entre 1,5 % et 4 % de conversion ; services B2B autour de 2,6 % en moyenne et 7,2 % pour le quart supérieur. Ce ne sont pas des promesses.

## Points non tranchés (remontent au gate)
- Lien d'agenda ou adresse de contact : option recommandée, un lien d'agenda.
- Éléments de preuve du fondateur : option recommandée, nom, titre et une phrase chiffrée vérifiable par ×4 / ×5.
