# TOOLING — prosens-site-vente

## Construire la page
Candidats : HTML, CSS, JavaScript natifs (sans dépendance) / GSAP via cdnjs / un générateur de site
Scores : natif=88  GSAP=64  générateur=45
Retenu : natif — déjà disponible, léger, indexable, aucune dépendance ; GSAP reste le plan B si la sobriété bride le design
Connecteur requis : — — statut : connecté
Dépense ou ligne rouge : aucune
Plan B si indisponible : sans objet

## Mouvement et accessibilité
Candidats : CSS (transitions, animations, `animation-timeline` si disponible) et IntersectionObserver / bibliothèque d'animation
Scores : CSS+IO=90  bibliothèque=60
Retenu : CSS et IntersectionObserver avec repli sans mouvement (`prefers-reduced-motion`)
Connecteur requis : — — statut : connecté
Dépense ou ligne rouge : aucune
Plan B si indisponible : sans objet

## Vérification mécanique
Candidats : Playwright pré-installé / aperçu d'artefact
Scores : Playwright=92  aperçu=70
Retenu : Playwright — captures 375, 768, 1440 pixels, console, défilement horizontal, contraste, navigation clavier
Connecteur requis : — — statut : connecté
Dépense ou ligne rouge : aucune
Plan B si indisponible : captures de l'aperçu d'artefact

## Aperçu privé à partager avec l'utilisateur
Candidats : artefact privé / fichiers du dépôt seulement
Scores : artefact=85  dépôt=70
Retenu : fichiers du dépôt (livraison principale) et un artefact privé pour l'aperçu, jamais partagé
Connecteur requis : — — statut : connecté
Dépense ou ligne rouge : aucune tant que l'artefact reste privé
Plan B si indisponible : captures d'écran dans `livrables/`

## Mise en ligne
Retenu : **pas par MAESTRO.** Publier sur Cloudflare Pages ou un domaine est une ligne rouge ; L02 décrit les gestes à faire par l'utilisateur.

## À connecter par l'utilisateur avant la phase 3
- [ ] Lien d'agenda de prise de rendez-vous ou adresse de contact — apporte : le bouton principal fonctionnel — comment : donner le lien ou l'adresse dans la réponse au gate
