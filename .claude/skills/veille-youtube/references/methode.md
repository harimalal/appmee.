# Méthode : collecte, filtres, calculs

La méthode est fixe. C'est ce qui rend deux recherches comparables : ne la change pas d'un sujet à l'autre sans le dire dans le champ `method` du rapport.

## 1. Requêtes

Pour un sujet, 3 à 5 requêtes qui couvrent les intentions de recherche :
- le nom seul (`higgsfield`) ;
- nom + intention : `avis`, `test`, `tutoriel`, `vs`, `alternative`, `prix` ;
- une variante dans l'autre langue si le sujet est international (`higgsfield tutorial`).

Note les requêtes telles quelles dans `src`, séparées par des virgules.

## 2. Collecte : deux voies, mêmes données

Pour chaque vidéo, il faut : id, titre, chaîne, vues, date (même approximative), durée, nombre d'abonnés de la chaîne.

**a. Script (Claude Code, ou tout environnement avec Python et accès à youtube.com)**
```
python3 -I <skill>/scripts/collecte.py --sortie <dossier> --miniatures "requête 1" "requête 2" …
```
- Une page de résultats par requête (filtre « Vidéos »), puis une page par chaîne pour les abonnés, avec une pause de 3 à 4 s entre deux pages. C'est le rythme d'une personne qui navigue.
- Sorties : `brut.json` (tout), `lignes.json` (vidéos retenues, calculées, triées), `top.md` (classement lisible), `miniatures/`.
- Le réseau doit autoriser `www.youtube.com` (pages) et `i.ytimg.com` (miniatures). Si un hôte est refusé, dis lequel ajouter aux domaines autorisés de l'environnement.
- **Si YouTube refuse une page** (vérification « robot », consentement, erreur), le script s'arrête, garde ce qu'il a et sort avec le code 2. Ne contourne jamais une vérification : pas de changement de client, d'en-têtes trompeurs ou de cookies empruntés. Propose d'attendre et de relancer (la commande reprend où elle s'est arrêtée), ou de finir au navigateur.
- N'utilise pas yt-dlp en masse, une requête par vidéo : c'est ce qui déclenche la vérification.

**b. Navigateur (claude.ai ou Claude Desktop avec l'extension Claude in Chrome)**
1. Ouvre `youtube.com/results?search_query=<requête>`, clique sur le filtre **Vidéos**.
2. Lis la page : titre, vues, « il y a N … », durée, chaîne. Fais défiler une ou deux fois pour avoir 30 à 40 vidéos.
3. Ouvre la page de chaque chaîne (une seule fois par chaîne) et relève les abonnés.
4. Convertis « il y a N jours / semaines / mois / ans » en âge en jours (1 mois = 30,4 j) : la date est alors **approximative**, à signaler (`approx: true`).

## 3. Filtres (identiques à chaque sujet)

| Garder | Pourquoi |
|---|---|
| Durée ≥ 4 min | Exclut les Shorts : autre algorithme, autre usage |
| Vues ≥ 500 | Sous ce seuil, le ratio n'a pas de sens |
| Âge ≥ 2 jours | Une vidéo d'hier n'a pas fini de monter (marquée « récente » jusqu'à 7 j) |
| Âge ≤ 12 mois | La veille sert à capter ce qui marche maintenant |
| En rapport avec le sujet | Écarte à la main les vidéos hors sujet, et dis-le dans `note` |

## 4. Calculs

- **Ratio** `q` = vues ÷ abonnés. C'est l'indicateur principal : il mesure la vidéo, pas la taille de la chaîne.
- **Vues par mois** `m` = vues ÷ (âge en jours ÷ 30,4). Départage les ex æquo et montre la vitesse.
- **Classement** : ratio décroissant, puis vues par mois. Le rang est `o`, le top 15 a `g = 1`.
- **Tranches** (couleurs du rapport) : 10 × et plus, 5 à 10 ×, 3 à 5 ×, moins de 3 ×.

Pour un chiffre « pourquoi c'est fort », compare toujours deux vidéos du même sujet : « 8 576 vues pour 336 abonnés (25,5 ×) bat 707 986 vues pour 150 000 abonnés (4,7 ×) ».

## 5. Honnêteté

- Aucun chiffre inventé. Une valeur manquante reste manquante (`k: "nd"`), elle n'est pas estimée.
- Les dates tirées de « il y a N mois » sont approximatives : `approx: true` et une phrase dans `note`.
- Les titres affichés par YouTube peuvent être traduits automatiquement selon la langue de la page. Si le titre original compte pour l'analyse, ouvre la vidéo.
- Une corrélation n'est pas une cause : l'analyse donne des hypothèses solides, pas des lois.
