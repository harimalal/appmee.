# SCRIPT — Reel n°10 « Nouvelle charte, tout le site d'un coup »
Skill : reel-histoire (mode direct, approche besoin). Fichier : `out/reel-charte.mp4`, rangé sous `CONTENT/REELS_INSTAGRAM/reel-instagram-reflexia-10.mp4` · couverture `couverture-reel-instagram-reflexia-10.png` (« Nouvelle charte », pastille « Une maquette → tout le site ») · sans musique, bruitages bas (`--sfx 0.3`) · 1080×1920 · 30 i/s · **42,1 s** · −14,1 LUFS · fond bleu-noir reflet.
Voix : Gemini TTS, Charon, `gemini-3.1-flash-tts-preview`, tempo 1,16 (10 phrases facturées).

## Demande de Hari (28/11/2026)
Le passage de l'ancienne charte (« très connotée Claude Code ») à la nouvelle (« les quatre couleurs »), sur toutes les pages (accueil, blog…) sans rien casser, grâce au système ; bien montrer l'avant/après (même contenu) ; la nouvelle charte trouvée avec une maquette : GPT Image a généré cinq ou six maquettes, Hari en a donné une à Claude, qui a tout fait.

## Ce que le dépôt établit (sources)
| Fait | Source |
|---|---|
| Ancienne charte : fond crème `#faf8f5`, sable `#f2ead8`, accent terracotta `#c8522a` | `src/styles/global.css` au commit `df3b980` (02/05/2026) |
| Nouvelle charte : blanc, accent rose `#E84393`, violet `#6C5CE7`, vert `#00B388`, orange `#FF6B35` ; polices Inter + Instrument Serif | commit `cffda46` (13/05/2026) « Redesign complet — nouvelle charte graphique Inter + Instrument Serif » |
| La maquette : `REFLEX IA landing page.pdf` (créée le 02/05/2026 à 01:06 UTC), ajoutée au dépôt avec le commit `0950e34` « Refonte complète du site : design PDF appliqué à toutes les pages » (02/05/2026, 03:17) | `git show 0950e34` |
| Même contenu : aucune différence dans `src/content/` entre `df3b980` et `cffda46` ; mêmes 25 pages construites avant et après (`astro build`, liste identique) | builds locaux du 28/11/2026 |
| Toutes les pages touchées : layout commun, accueil, rubriques, blog, manifeste, landing, styles | `git show --stat 0950e34 cffda46` |

Avant/après montrés : captures 1 280 px des deux builds (`assets/pg/avant-*.jpg` = `df3b980`, `assets/pg/apres-*.jpg` = `cffda46`) ; maquette : page 1 du PDF (`assets/maquette-1.jpg`) ; typographie : extrait réel de l'accueil après (`assets/typo.jpg`).

## Texte lu
1. Changer le look de tout ton site, sans rien casser ? Je l'ai fait d'un coup ! *(dit de Hari)*
2. Avant, mon site était crème et orange. Il ressemblait trop à Claude. *(couleurs : établi ; « trop Claude » : avis de Hari)*
3. D'habitude, refaire un design, c'est long, et ça casse des pages. *(généralité, non mesurée)*
4. Moi, j'ai demandé cinq ou six maquettes à GPT Image. *(dit de Hari)*
5. J'en ai gardé une seule, et je l'ai donnée à Claude.
6. Claude a fait tout le reste : la page d'accueil, le blog, les articles, les rubriques.
7. Quatre couleurs, une nouvelle police, et partout la même charte.
8. Et rien n'a cassé : mêmes pages, même contenu, juste un nouveau look.
9. Regarde l'avant, et l'après.
10. Tu veux faire pareil sur ton site ? Commente « charte », et je t'envoie la méthode !

## Mise en scène (fond bleu-noir reflet, un changement toutes les 2 à 4 s)
hook : l'accueil réel bascule de l'ancienne à la nouvelle charte (balayage) · avant : la page crème, deux pastilles crème/terracotta, logo Claude 3D à « Claude » · d'habitude : quatre pages qui tremblent, croix rouges, horloge · maquettes : six emplacements, **seul celui du milieu en bas est la vraie maquette** (les cinq autres sont des cadres neutres : les images GPT Image ne sont pas dans le dépôt), la vraie maquette vient au centre puis part vers le logo Claude · pages : accueil, blog, article, rubrique basculent l'un après l'autre · palette : les quatre couleurs, l'extrait réel de la nouvelle typographie, quatre pages après · rien n'a cassé : avant/après côte à côte, « ✓ Mêmes pages », « ✓ Même contenu » · avant/après plein écran sur un article (balayage aller-retour) · CTA « charte ».

## Limites
- **Les cinq ou six maquettes GPT Image** : dit de Hari, absentes du dépôt ; à l'écran, cinq cadres neutres + la vraie maquette retenue. Si Hari envoie les images, elles remplaceront les cadres.
- **« D'un coup »** : la bascule tient en deux commits (02/05 : structure de toutes les pages d'après la maquette ; 13/05 : couleurs et polices). Le reel montre l'avant du 02/05 et l'après du 13/05.
- « Ressemblait trop à Claude » : avis de Hari (palette crème/terracotta proche de celle de Claude).
- La forme des pages change aussi (pas seulement les couleurs) ; le contenu, lui, est identique.

## Contrôles
`qa.cjs` vert · chevauchements 0 sur 422 instants · 1080×1920 / 30 i/s / 42,1 s · −14,1 LUFS · freezedetect 0 · transcription du mixage 0,952 par mots.
