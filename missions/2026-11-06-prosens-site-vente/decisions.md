# DÉCISIONS — prosens-site-vente

## Choix validés au cadrage
Voir `brief.md` (verrouillé le 2026-11-06). Positionnement : méthode terrain, closing inclus, définition écrite du rendez-vous qualifié, aucune garantie de volume. Structure : une page en long scroll avec deux entrées PME et grands groupes. Mouvement : CSS et IntersectionObserver, un moment fort, repli sans mouvement. Conversion : un bouton unique, répété quatre fois.

## Fiches des rôles
### Stratège commercial et rédacteur de conversion
- Sortie attendue : tout le texte de la page (L01) et la liste des pièces à fournir (L02)
- Droit de veto : toute promesse non étayée
- Exigence portée : fiabilité
- Sortie de scène : texte final validé par l'audit
- École de pensée : vente B2B de terrain, celle d'un directeur commercial de région qui pilote des équipes et des comptes ; la prospection est un processus qu'on mesure, pas un talent.
- Méthodes éprouvées : (1) définir la cible idéale avant toute action ; (2) qualifier avant de relancer, avec une grille de qualification écrite (famille BANT ou MEDDIC) ; (3) enchaîner les canaux en séquence (appel, email, réseau professionnel) plutôt que de répéter le même ; (4) le closing commence au premier échange : on prépare la conclusion pendant la qualification.
- Angle unique : pour le client, le produit n'est pas « des leads », c'est un agenda de rendez-vous dont il peut vérifier chaque critère.
- Hacks : donner au prospect une raison précise d'accepter l'échange (son contexte, pas le nôtre) ; poser la définition du qualifié comme un contrat.
- Secret sauce : la section « Qu'est-ce qu'un rendez-vous qualifié » vaut plus qu'une garantie de volume : elle déplace la discussion de la quantité vers la qualité mesurable.
- Biais : sur-vendre la méthode et promettre plus que ce qui est prouvé. Compensé par son propre droit de veto sur les promesses non étayées et par la lecture du développeur.

### Directeur artistique et motion
- Sortie attendue : direction visuelle, système de couleurs et de typographie, partition des mouvements
- Droit de veto : tout élément qui ressemble à un gabarit générique
- Exigence portée : élégance
- Sortie de scène : direction visuelle appliquée et validée par l'audit
- École de pensée : design éditorial typographique, la hiérarchie vient de l'échelle des caractères et de la grille, pas de l'ornement.
- Méthodes éprouvées : (1) grille asymétrique avec un grand vide assumé ; (2) hiérarchie par contraste d'échelle et de chasse ; (3) un seul motif visuel réutilisé pour relier les sections ; (4) mouvement qui explique (cause et effet) plutôt qu'il ne décore.
- Angle unique : le visuel est le mécanisme de l'offre (détecter, qualifier, remplir un agenda), pas une illustration générique de « croissance ».
- Hacks : alterner sections sombres et claires pour rythmer sans effet ; utiliser une police à chasse variable pour une identité sans logo.
- Secret sauce : une seule image forte, réutilisée deux fois (en tête de page, puis dépliée dans la section du mécanisme).
- Biais : sur-décorer et multiplier les effets. Compensé par le veto du développeur sur la performance et l'accessibilité.

### Développeur front
- Sortie attendue : `index.html` autonome, performant, accessible, avec vérification mécanique
- Droit de veto : tout effet qui dégrade la performance ou l'accessibilité
- Exigence portée : simplicité
- Sortie de scène : audit passé

## Débats structurants

### Décision #1 : direction visuelle
- Tour 1 — Directeur artistique : concept « radar vers agenda ». PROSENS = prospection + sens (direction). Un radar qui balaie, des points qui s'allument, certains se verrouillent et glissent dans les créneaux d'un agenda. Palette : encre sarcelle, papier vert pâle, signal ambre. Typographie : Archivo en chasse élargie pour les titres, IBM Plex Sans pour le texte, IBM Plex Mono pour les données. Sections sombres et claires en alternance, pas de cartes, des filets et de grands chiffres — preuve : Linear et Stripe font démontrer le mécanisme par le mouvement — coût : un visuel à soigner — signal : si le radar n'explique rien.
- Tour 1 — Stratège commercial : un look éditorial sobre, sans illustration, pour ressembler à un directeur commercial et non à une start-up technologique ; le radar risque de passer pour un gadget — preuve : les concurrents relevés misent sur la promesse chiffrée, pas sur le décor ; la confiance d'un dirigeant se gagne par la clarté — coût : moins de « wow » — signal : si le radar démontre réellement le parcours.
- Tour 1 — Développeur : contraste suffisant (texte ambre ou clair sur sarcelle, encre sur papier), poids de page faible, polices limitées à trois familles — signal : un contraste insuffisant ou une police en échec de chargement.
- Tour 2 : le stratège accepte le radar **s'il démontre le parcours** (détecter, qualifier, rendez-vous dans l'agenda, closing) et non s'il décore. Le directeur artistique accepte une typographie sobre partout ailleurs, avec le radar limité à deux apparitions. Troisième voie : un seul motif, en tête de page puis déplié étape par étape dans la section du mécanisme.
- CLÔTURE : direction « radar vers agenda », limitée à deux apparitions, sobriété typographique ailleurs — motif : doctrine (le mouvement ne passe jamais avant la lisibilité) puis fiable > évident > beau.
- Écarté : look purement typographique sans motif (trop proche de la concurrence), radar décoratif répété sur toute la page, illustrations de personnes.
- Réversible : oui — le motif est un seul composant SVG ; le retirer ne casse aucune section.

Jetons arrêtés (à respecter en production) :
- Couleurs : encre `#0B2A2B`, papier `#F2F5F2`, papier appuyé `#E3EBE6`, trait `#C5D3CB`, signal ambre `#FFB020`, texte secondaire `#46605C`, menthe `#8FD4B1` pour les points détectés.
- Typographie : titres Archivo 800 chasse 112, texte IBM Plex Sans 400 et 500, données IBM Plex Mono 500. Secours : `system-ui`, `ui-monospace`.
- Rayons : 0 pour les blocs, 999 pour les boutons ; filets 1 pixel ; espacements en multiples de 8.
- Logotype : mot PROSENS en Archivo élargi avec un petit arc de radar et un point ambre ; créé en SVG dans la page.

### Décision #2 : ordre et rythme des sections
- Tour 1 — Stratège commercial : accroche, problème, mécanisme animé, définition du rendez-vous qualifié, offres PME et grands groupes, comparaison avec les alternatives, fondateur, objections, appel final — preuve : séquence « problème, mécanisme, preuve, offre » relevée sur les pages de services B2B — coût : le fondateur arrive tard — signal : si la confiance chute avant la section.
- Tour 1 — Directeur artistique : le fondateur doit venir tout de suite après l'accroche, car l'offre repose sur sa personne — preuve : l'angle de différenciation est le profil terrain — coût : le mécanisme est repoussé — signal : le fondateur n'a ni nom ni photo à montrer.
- Tour 1 — Développeur : questions en éléments `details` accessibles, navigation par ancres, aucune section qui dépend du mouvement pour être lue.
- Tour 2 : le stratège refuse de monter la section du fondateur car ses chiffres sont déclarés et non étayés ; le directeur artistique propose une **ligne de confiance** dans l'accroche et la section complète plus bas. Troisième voie : une ligne « Piloté par un directeur commercial de région » dès l'accroche, la section complète avant les objections.
- CLÔTURE : ordre du stratège, ligne de confiance dans l'accroche, rythme sombre / clair en alternance (accroche sombre, problème clair, mécanisme sombre, qualifié clair, offres clair appuyé, comparaison clair, fondateur sombre, objections clair, appel final sombre) — motif : contrainte dure du brief (aucune donnée inventée) puis fiable > évident > beau.
- Écarté : section du fondateur juste après l'accroche (met en avant des chiffres non étayés), navigation à onglets pour tout le contenu.
- Réversible : oui — les sections sont des blocs indépendants.

## Décisions d'exécution (non structurantes)
- 2026-11-06 — Contact : un seul réglage `CONTACT_URL` en tête de script ; vide, les boutons ouvrent un panneau « préparer l'échange » qui compose la demande à envoyer ; renseigné, ils ouvrent le lien. Aucun texte provisoire n'est visible dans les deux états (rôle : développeur).
- 2026-11-06 — Fondateur sans nom ni photo : présenté par sa fonction, ses résultats attribués à sa déclaration ; aucun portrait inventé (rôle : stratège).
- 2026-11-06 — Les engagements de la page (définition du qualifié, propriété des données, confirmation du prospect) sont des propositions de la méthode : L02 les liste pour validation (rôle : stratège).
