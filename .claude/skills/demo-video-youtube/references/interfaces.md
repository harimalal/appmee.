# Interfaces reproduites et images réelles

## Le kit du modèle (classes CSS prêtes)

| Interface | Classes | Contenu |
|---|---|---|
| Fenêtre Chrome | `.win` > `.chrome` (`.dots`, `.tabs` > `.tab`, `.url`) | Onglets, barre d'adresse, groupe d'onglets « Claude » (`.tgroup`), zone d'extension (`.ext`), liseré de pilotage (`.glow`) |
| Résultats YouTube | `.yt` (`.top`, `.search`, `.chips` > `.chip`, `.res` > `.row`) | Barre de recherche, filtres, lignes avec miniature, badge de durée, chaîne, description |
| Tableur | `.gs` (`.mb`, `.tool`, `.fx`, `table`) | Barre de menu, barre d'outils, barre de formule, cellules, cellule sélectionnée `.sel` |
| Claude Desktop | `.cd` (`.side`, `.main2`, `.msgs` > `.u` / `.a`, `.box`) | Barre latérale, message utilisateur, réponse, appels d'outils `.toolcall` (`.spin` en cours, `.ok` fait), zone de saisie |
| Terminal Claude Code | `.term` (`.tb`, `.welcome`, `.pr`) | Barre de titre, encart d'accueil, invite |
| Boutons YouTube | `.ytbtn.sub` (S'abonner), `.subd` (Abonné), `.likebox`, `.ctabox`, `.cm` (commentaire) | Appels à l'action |
| Cartes et tableaux sombres | `.card`, `.dt` (`.hr`, `.tr`), `.tool2` (outil + limites), `.ben` (bénéfice), `.lbl` (étiquette sur capture) | Mise en page des slides |
| Pastilles et signaux | `.pill.p0…p3` (tranches), `.tag` (limite, rouge), `.tagok`, `.stamp` (tampon) | |

Pour une autre interface (Notion, n8n, Canva, un SaaS, l'app de l'utilisateur) : reproduis-la au plus près avec la même méthode (mise en page, barres, couleurs, typographie, badges), ou mieux, **capture la vraie** avec `capturer-page.cjs` si elle est accessible.

## Logos et marques

- **Ne redessine jamais un logo ou un wordmark officiel.** Place à son emplacement exact un repère `.logo-slot` (cadre en pointillés + nom de la marque) : il sera recouvert au montage par le vrai fichier.
- Les couleurs d'interface et la mise en page peuvent être fidèles ; c'est le signe distinctif (logo) qui reste un repère.
- Dis-le à l'utilisateur à la livraison : liste des repères à remplacer.

## Images réelles

- **Préférer le vrai** : captures de l'artefact ou de l'app (`page`, `apercu`), vraies miniatures téléchargées pendant la recherche (`t_xxx`, `wall`).
- Les miniatures appartiennent aux créateurs : les montrer pour les analyser est courant, mais garde-les à l'écran le temps du commentaire et cite les chaînes dans la description de la vidéo. Rappelle-le à la livraison.
- Miniatures factices (`.mth`) seulement quand il n'y a pas de vraie image, et jamais présentées comme réelles.
- Taille : un artefact est limité à 16 Mo. Mur de 70 miniatures à 240×135 + une capture pleine page ≈ 3 Mo.
