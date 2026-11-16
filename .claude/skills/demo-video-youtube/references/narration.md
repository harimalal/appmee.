# Narration : la démo qui mène à un résultat

Ce n'est pas un « how to ». C'est une démonstration qui part d'un **problème vécu**, montre ce qu'on a construit pour le régler, puis comment. L'oral porte l'explication : à l'écran, **un titre et une structure par slide**, le reste se voit.

**Chaque sujet a son récit.** Le modèle (`assets/demo-modele.html`) fournit le moteur, le kit d'interfaces et un exemple de ton. Il ne fournit pas un plan à remplir. Ne recopie ni ses 20 slides, ni leur ordre, ni leurs titres, ni leurs animations : choisis les sections, leur nombre et leur ordre pour ce sujet, et invente les animations et les encarts qui montrent *ce* sujet (une boucle pour un processus, des barres qui se remplissent pour un avancement, un mur de titres pour une dispersion…).

## Les trois premières slides : toujours dans cet ordre

1. **L'accroche : le problème, montré.** Une scène où l'on vit le problème, sans titre ni explication : une vraie interface qui déborde, une question tapée qui reste sans réponse, une corvée qui se répète. C'est le moment « c'est exactement moi ». La slide « Quelle vidéo faire ? » de la démo Veille est le bon modèle.
2. **Le titre.** Le nom de la solution en très grand, avec derrière **la solution illustrée** : redessinée, simplifiée, pas forcément à l'identique, **floutée et très transparente** (opacité 10 à 20 %, flou 6 à 12 px). Un sous-titre d'une ligne.
3. **Le bénéfice immédiat.** Ce que ça apporte, sans effort et sans coût en plus (pas d'outil à payer, pas de saisie, pas de technique), avec l'interface en fond légèrement floutée ou sous un dégradé. Trois promesses courtes, chacune vraie et vérifiable. Pas d'appel à l'action ici.

## Ensuite : les sections, à choisir et à ordonner selon le sujet

| Section | Ce qu'elle dit | Idées de mise en scène |
|---|---|---|
| À quoi ça sert | Les questions auxquelles ça répond, ou les tâches que ça fait | Question → réponse qui pointe la zone de l'interface |
| Pourquoi le faire | Le coût de ne rien faire | Une boucle qui se répète, un compteur qui monte |
| Pour qui | 2 à 3 profils concrets | Chaque profil avec *son* exemple (ses projets, ses clients) |
| Les méthodes fastidieuses | Ce qu'on fait à la main, avec ses **plus et ses moins** | Interface remplie à la main (au moins 10 lignes), encart + / − |
| Les méthodes à la mode | Ce qu'on conseille partout et qui ne règle pas le fond, avec **plus et moins** | Liste avec plus en vert et moins en rouge ; **pas de graphique** |
| La solution | Le principe, en une image | Schéma animé du mécanisme (boucle, flux, avant → après) |
| Ce que ça facilite | 3 à 5 points concrets | Une micro-animation par point dans l'interface |
| Le détail de la solution | Structure, prompt, étapes réelles, vraie page encart par encart | Saisie dans la vraie interface, zooms dans la vraie capture |
| Le temps, en gros | Combien de temps à la main (estimation) face au temps réel, sur le seul périmètre de la vidéo | Deux colonnes rouge / accent, gros chiffres, compteur |
| La croissance | Comment le résultat a grandi | Courbe cumulée tirée des vraies dates, qui se dessine, un repère sur le décollage |
| Le teaser | Un sujet voisin, gardé pour une autre vidéo | Une bulle de commentaire YouTube : « écris SITE en commentaire » |
| Le bilan | Ce que ça a donné, en vrais chiffres | Compteurs, avant / après |
| L'appel à l'action | S'abonner, liker, commenter avec une demande utile | Boutons, saisie en boucle, « le prompt est dans la description » |

Longueur indicative : 12 à 18 slides. Une section peut tenir en deux slides si elle le mérite, ou disparaître si elle n'apporte rien au sujet.

## Règles d'écriture

- **Un titre par slide**, court, en majuscules condensées, un seul mot en couleur d'accent. Un surtitre au-dessus.
- **Une structure par slide** : deux cartes, une liste, une interface, un schéma. Pas de mélange.
- **L'oral dit le reste** : chaque slide a sa note (touche N) de 1 à 3 phrases, écrite pour être dite.
- **Vrais chiffres, vraies images** : ceux de la conversation et de l'artefact. Une estimation est écrite comme telle à l'écran.
- **Ne pas inventer l'histoire** : si tu n'as pas la conversation d'origine, présente le prompt et les étapes comme la méthode à suivre, pas comme ce qui s'est dit.
- **Pas de prix d'outils** : ils changent. Classe en gratuit, freemium, payant.
- **Appels à l'action** : jamais en entrée. Le premier est un **petit bandeau en bas de l'écran** (avatar, S'abonner qui passe à Abonné, J'aime), sur la slide « Pour qui » ou juste après. Le second, complet, à la fin. Le commentaire demandé est utile, pas un « like si tu aimes ».
- **La voix** : « je » quand le créateur raconte son expérience (ce qu'il a essayé, ce qu'il a construit), « tu » seulement pour s'adresser au spectateur (« si tu mènes plusieurs projets… »). Demande-le si ce n'est pas clair.
- **Ce qu'il a vraiment essayé** : demande quels outils il a utilisés avant, et raconte cet essai à la première personne, avec ses vrais plus et ses vrais moins.
- **Rien ne se perd** : quand une nouvelle version retire des slides, garde-les **en réserve** après la fin (une slide intercalaire « Slides en réserve », ids préfixés `r-`), pour le montage.
- Pendant un zoom, masque le titre (`data-hudoff`) pour ne pas recouvrir l'interface.

## Le design, avant de tout construire

Ne reprends pas d'office le thème du modèle (bleu nuit et jaune) : il est jugé trop sombre et trop basique. Une fois le déroulé validé, fais une **planche de design** : 2 ou 3 directions claires, chacune avec une vraie signature (palette, typographie, surfaces, un détail reconnaissable), montrées sur les 4 mêmes slides (titre, bénéfice, liste plus/moins, une slide de chiffres). Mets les vraies images du sujet en fond. Publie la planche, fais choisir, puis seulement construis.

Le choix qui a plu pour la démo Product Hunt (28 octobre 2026) : **pastel produit** (dégradés rose, lilas, pêche ; cartes en verre dépoli ; ombres colorées ; accent corail ; surligneur jaune) **avec l'impact de la v1** (grands titres condensés en capitales, gros chiffres). Il s'applique par-dessus le modèle avec `assets/theme-pastel.css` (à ajouter après les autres styles) : variables de couleur, `.slide`, `.title`, `.eyebrow`, surfaces, et remplacement des couleurs écrites en dur pour le fond sombre.

Ce thème se décline sans refaire de planche quand le créateur dit « même style, mais… » : changer `--vio` (la couleur secondaire) et le fond de la pub suffit. Démo Blog Factory : `--vio:#B39DF5` (violet pâle), pub sur un dégradé lilas clair avec texte foncé.

## Le script, toujours d'abord

Écris le **déroulé en texte** avant tout code : une ligne par slide, avec le titre, ce qu'on voit (structure et animation) et la phrase d'oral. Fais-le valider : c'est là que se jouent les retours. Ensuite seulement, rends-le concret, en slides explicatives et animées.

## Exemple : « Démo Veille YouTube » (20 slides)

Résultat → appel à l'action → blocage (« Quelle vidéo faire ? ») → piège (les vues brutes mentent) → la jungle (5 bénéfices) → pour qui → à la main (12 lignes) → autres solutions → pivot → Claude Desktop + Chrome → prompt → collecte → calcul → classement → pourquoi ça marche → ce que l'outil donne → rendu final → encarts → avant / après → appel à l'action. C'est un récit parmi d'autres, propre à ce sujet-là.
