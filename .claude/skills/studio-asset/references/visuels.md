# Composer les visuels : posts, carrousels, diaporamas

## Règles communes
- **Un message par image.** Un titre de 3 à 8 mots, une phrase de soutien au plus, un écran de l'app.
- **Le vrai produit** : captures réelles dans un téléphone entier (classe `.ph`), jamais coupé sur un bord sauf choix délibéré d'un gros plan.
- **Les mots de la landing** pour les titres ; un mot surligné (`.mk`) ou en couleur d'accent (`.acc`), pas plus.
- **Lisible sur un téléphone** : sur un visuel de 1080 de large, titre ≥ 80 px, texte ≥ 36 px. Avec `--u` (1 % du petit côté), titre ≈ `calc(var(--u)*8)` et texte ≥ `calc(var(--u)*3.4)`.
- **Des fonds de la palette de la marque**, qui changent d'une image à l'autre pour rythmer une série ; le dégradé de marque réservé à la première et à la dernière.
- **Une bulle ou une flèche manuscrite** pour pointer le détail qui compte sur l'écran.
- **Respecter les zones sûres** des formats verticaux (voir `formats.md`).

## Post unique
1 diapositive du diaporama (ou un bloc de la planche) : titre + capture + éventuellement un chiffre ou une citation. Décliner le même post dans les formats demandés avec `--format` (1080x1350, 1080x1080, 1080x1920, 1600x900) : la mise en page s'adapte grâce aux classes `portrait` / `carre` / `paysage` ; vérifier chaque format en image.

## Carrousel (Instagram, LinkedIn)
Le carrousel se lit comme un mini-récit qu'on fait défiler ; chaque page doit donner envie de passer à la suivante.
1. **Couverture** : la promesse ou une question qui accroche, gros texte, et un indice de défilement (« → », « Swipe »).
2. **Le problème** en une page.
3. **3 à 6 pages, une fonctionnalité chacune** : numéro, bénéfice, capture.
4. **Preuve** : chiffre, résultat, citation d'utilisateur (seulement si réelle).
5. **Appel à l'action** : slogan + adresse.
Sorties : images `NOM-01.jpg…` pour Instagram, `NOM.pdf` pour LinkedIn (`rendre.cjs … diapos --pdf`). Toutes les pages au même format.

## Diaporama statique
Même structure que le carrousel, en 16:9 (1920×1080) pour une présentation, un e-mail ou un site : `--format 1920x1080 diapos --pdf`.

## Diaporama animé
Même source que le carrousel, rendue en vidéo (`rendre.cjs … film`) :
- **Transitions entre diapositives** (`data-transition`) : `glisse` ou `pousse` pour avancer dans un récit, `zoom` pour une révélation, `rideau` pour un avant/après, `flou` pour la fin, `fondu` par défaut. Varier, mais garder 2 ou 3 types par vidéo.
- **Entrées des éléments** (`data-entree` + `data-delai`) en cascade : pastille (0 s) → titre (0,15 s) → téléphone (0,35 s) → bulle (0,8 s). `machine` pour une phrase tapée, `pop` pour un badge, `masque` pour un surlignage, `data-compte` pour un chiffre qui monte.
- **Écrans qui changent dans le téléphone** (`<img data-a="1.8">`) pour montrer une action sans film complet.
- **Durée** : 2,5 à 4 s par diapositive ; 15 s ≈ 5 diapositives, 30 s ≈ 8 à 10.
- **Sortie** : MP4 (+ `--gif 600` pour un GIF), au format du réseau. Pour une voix off ou des sous-titres sur un diaporama, faire un fichier de montage d'un seul morceau `[0, DUREE, 1]` avec ses répliques, puis `voix-off.cjs` comme pour le film.

## Package complet
Tout produire depuis les mêmes captures et les mêmes textes, dans `sortie/` rangé par usage :
```
sortie/
  video/        film long 16:9, 60 s avec voix 16:9, 30 s 9:16, 15 s 9:16, 15 s 1:1, GIF de landing, sous-titres, piste voix
  product-hunt/ galerie 1270×760 ×6–8, vignette PNG + GIF, miniature YouTube
  instagram/    carrousel 1080×1350, 3 posts 1080×1350, 2 stories 1080×1920
  linkedin/     carrousel PDF, post 1080×1350, vidéo 1080×1350
  x/            2 posts 1600×900, vidéo 16:9
  web/          image de partage 1200×630, vidéo de landing en boucle, GIF d'e-mail
  stores/       captures App Store 1290×2796 et Google Play 1080×1920 + bannière 1024×500 (si app mobile)
  textes/       légendes de chaque post, texte de la voix off, fil X, post LinkedIn
```
Puis `node scripts/index-package.cjs sortie "Package <App>"` pour une page de revue de tout le package.
