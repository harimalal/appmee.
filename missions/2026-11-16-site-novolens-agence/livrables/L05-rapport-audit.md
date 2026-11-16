# Rapport d'audit chiffré — site NOVOLENS V3

Date : 2026-11-16. Outil : `livrables/audit/audit.js` (Playwright), résultats bruts dans `livrables/audit/resultat.json`. Les contrôles sont mécaniques et reproductibles : `node livrables/audit/audit.js livrables/site`.

## Résultat de synthèse
- 9 pages auditées à 400, 820 et 1360 px : aucun débordement horizontal, aucune erreur de console, un seul `h1` par page.
- Poids : plus grosse page HTML 55,7 Ko (index) pour un budget de 60 Ko ; plus grosse image 198 Ko pour un budget de 250 Ko.
- Contrastes : 15 paires sur 15 au niveau AA (4,5:1).
- Clavier : focus visible sur les 8 premiers éléments tabulés de chaque page (testé). Fermeture du menu avec Échap et pilotage des onglets aux flèches : implémentés, non testés automatiquement.
- Mouvement réduit : aucun bloc de contenu resté masqué.
- Liens internes : aucun lien cassé. Images : toutes avec dimensions et texte alternatif.

## Détail par page
| page | poids HTML | h1 | description | débordement | erreurs console | focus visible | blocs masqués (mouvement réduit) |
|---|---|---|---|---|---|---|---|
| 404.html | 4.2 Ko | 1 | non | aucun | 0 | oui | 0 |
| cas-client.html | 24.7 Ko | 1 | oui | aucun | 0 | oui | 0 |
| comment-ca-marche.html | 52 Ko | 1 | oui | aucun | 0 | oui | 0 |
| contact.html | 10.4 Ko | 1 | oui | aucun | 0 | oui | 0 |
| faq.html | 13.5 Ko | 1 | oui | aucun | 0 | oui | 0 |
| index.html | 55.7 Ko | 1 | oui | aucun | 0 | oui | 0 |
| pourquoi-nous.html | 16.7 Ko | 1 | oui | aucun | 0 | oui | 0 |
| resultats.html | 13 Ko | 1 | oui | aucun | 0 | oui | 0 |
| tarifs.html | 14.1 Ko | 1 | oui | aucun | 0 | oui | 0 |

## Contrastes (texte et fond réellement utilisés)
| paire | ratio | seuil | conforme |
|---|---|---|---|
| encre sur blanc | 18.34:1 | 4.5:1 | oui |
| encre sur violet clair | 15.78:1 | 4.5:1 | oui |
| encre sur violet fin de dégradé | 12.34:1 | 4.5:1 | oui |
| texte secondaire sur blanc | 11.92:1 | 4.5:1 | oui |
| texte secondaire sur violet clair | 10.25:1 | 4.5:1 | oui |
| texte secondaire sur violet fin de dégradé | 8.02:1 | 4.5:1 | oui |
| gris muted sur blanc | 8.05:1 | 4.5:1 | oui |
| gris muted sur violet fin de dégradé | 5.41:1 | 4.5:1 | oui |
| violet de marque sur blanc | 7.17:1 | 4.5:1 | oui |
| violet de marque sur violet clair | 6.17:1 | 4.5:1 | oui |
| violet de marque sur violet fin de dégradé | 4.82:1 | 4.5:1 | oui |
| blanc sur bouton violet | 7.17:1 | 4.5:1 | oui |
| blanc sur violet clair du bouton | 4.75:1 | 4.5:1 | oui |
| encre sur jaune | 13.26:1 | 4.5:1 | oui |
| rouge pastille sans | 5.88:1 | 4.5:1 | oui |

## Images
avec.jpg 52 Ko, card-1.jpg 152 Ko, card-2.jpg 124 Ko, card-3.jpg 169 Ko, card-4.jpg 131 Ko, cta-bg.jpg 198 Ko, eti.jpg 60 Ko, grand.jpg 111 Ko, hero-bg.jpg 197 Ko, livraison.jpg 65 Ko, pme.jpg 55 Ko, sans.jpg 85 Ko.

## Corrections faites pendant l'audit
- Dégradé violet de fin de section éclairci (#CDBBFF vers #D9CDFF) : le violet de marque passait de 4,15:1 à 4,82:1 et le gris secondaire de 3,94:1 à 5,0:1 ou plus.
- Index ramené de 64,7 Ko à 55,7 Ko : icônes et polices des illustrations déplacées dans la feuille de style, second jeu de cartes du mur de preuves cloné par le script.
- Dimensions ajoutées sur les images des étapes ; description ajoutée à la page 404 (vérifiée dans le fichier, hors nouvelle passe complète).
- Notes de développement masquées (« photo remplaçable ») sur le site public.

## Ce que cet audit ne couvre pas
- Lighthouse et mesures réelles de LCP, INP et CLS : non exécutés dans cette session. Les seuils web.dev (LCP 2,5 s, INP 200 ms, CLS 0,1) restent à mesurer après mise en ligne.
- Test sur appareils réels, lecteurs d'écran et outil d'accessibilité automatique de type axe : non faits.
- Contraste vérifié sur les paires de couleurs de la charte, pas sur chaque élément du rendu.
- Les polices Google Fonts n'ont pas été chargées dans l'environnement de test (repli système) : les rendus des captures peuvent différer légèrement.
- La page L02-design-system.html a été ajoutée après la dernière passe complète : contrôlée en capture et sans erreur de console, à 1360 px seulement.
- Chiffres, tarifs, témoignages et cas client : exemples étiquetés, à remplacer. L'e-mail et le domaine du sitemap sont des valeurs d'exemple.
