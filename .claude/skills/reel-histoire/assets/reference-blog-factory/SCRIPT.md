# SCRIPT — Reel « Comment j'ai publié 64 articles de blog en deux mois » (v2, 82,1 s, 1080×1920, 30 fps)

Skill : reel-histoire (4e essai, 2e version). Source : artefact « Blog Factory Playbook » (23/08/2026), croisé avec `SKILL_BLOG_FACTORY.md`, `BLOG_FACTORY_SKILLS/`, `AUTOMATION/production_log.md` et les fichiers d'articles. Voix : Google Gemini TTS, voix Charon, modèle `gemini-3.8-flash-lite-tts`. Rendu 100 % local, aucune image générée : les pages montrées sont les vraies pages du site construit en local (`npm run build`, 164 pages), captées à 540 px de large. Version précédente (81 articles, 63,5 s) gardée en local : `out/reel-blog-factory-v1-81.mp4`, non versionnée.

## Texte lu (18 phrases)
t1 Comment j'ai publié soixante-quatre articles de blog en deux mois, avec Claude Code ?
t2 Des articles longs, pensés pour le SEO.
p1 Un article de blog, ça se pense d'abord pour le SEO.
p1b Ce que cherche vraiment l'utilisateur, la stratégie de mots-clés, un angle original.
p2 À la main, ça prend des jours.
p3 Et si tu le demandes à une IA, tu obtiens un texte moyen, que tout le monde a déjà écrit.
s1 Grâce à ses skills, Claude Code suit un système en cinq étapes.
s2 D'abord, les vraies questions des lecteurs, et un angle que les autres n'ont pas pris.
s3 Ensuite, une recherche web réelle : les tarifs, les notes, les retours de terrain.
s4 Il rédige : un titre pensé pour ce que les gens tapent, un mot-clé principal, une structure adaptée au sujet.
s5 Puis un audit noté sur cent, sur cinq critères. Sous quatre-vingts, on corrige et on recommence.
s6 Enfin, la publication, seulement si le build passe.
n0 Le même processus à chaque article : la qualité reste dans la même fourchette.
n1 Soixante-quatre articles, d'environ cinq mille mots chacun.
n2 Notés entre quatre-vingt-cinq et cent sur cent, par le processus lui-même.
e1 Voilà ce que ça donne : les pages défilent, comme sur le blog.
e2 Un comparatif, un duel, un tutoriel, une analyse de risques : à chaque fois, la structure suit le sujet.
k1 Abonne-toi pour plus d'astuces IA : sans compétences techniques, rapides, et terriblement efficaces.
Retouches de formulation après validation, pour la synthèse vocale : s1 (« Avec des skills » entendu « Avec tes skills »), s3 (« prix » entendu « prise », remplacé par « les tarifs »).

## Sources des nombres
| Nombre | Source | Statut |
|---|---|---|
| 64 articles « en deux mois » | `AUTOMATION/production_log.md` : lignes « Publié — NN/100 » datées du 01/08 au 30/09/2026 (31 en août, 33 en septembre) | mesuré par comptage ; les 81 articles notés du journal courent du 15/05 au 23/10 (5 mois) : « deux mois » ne vaut que pour ces 64 |
| ≈ 5 200 mots | comptage de ces 64 fichiers (corps, balises HTML retirées) : moyenne 5 212, médiane 5 508, de 3 318 à 6 772 ; 42 sur 64 ≥ 5 000 | **mesuré, approximatif** |
| 85 à 100 | notes du journal pour ces 64 (moyenne 92,4 non montrée ; 6 à 100/100, 50 de 90 à 99, 8 sous 90) | mesuré ; **auto-évaluées** |
| cinq étapes, cinq critères, seuil 80 | `SKILL_BLOG_FACTORY.md` (phases 0 à 4 ; audit SEO technique 20 %, contenu 25 %, lecture 20 %, rétention 20 %, détection IA 15 % ; « si < 80 : corriger + re-audit ») | règle du skill, pas une mesure |
| « les audits corrigent le skill » (écran) | corrections datées dans `SKILL_BLOG_FACTORY.md` (06/08, 12-13/09, 15/09/2026) | sourcé, sans nombre de corrections |

Écartés : 23 articles / moyenne 89 / 4-6 h par article / ~45 000 tokens (artefact figé au 23/08) ; 81 articles (sur 5 mois) ; 132 fichiers (comparatifs inclus) ; « zéro intervention ».

## Ce qui vient de Hari, non sourcé dans le dépôt
- « Un article de blog se pense d'abord pour le SEO : ce que cherche l'utilisateur, la stratégie de mots-clés, un angle original » ; « à la main, ça prend des jours » ; « une IA donne un texte moyen que tout le monde a déjà écrit » ; « la qualité reste dans la même fourchette » (étayé seulement par l'étendue des notes auto-évaluées).
- Étiquettes des pages montrées (Comparatif, Duel, Tutoriel, Analyse des risques, Cas d'usage) : mes qualifications d'après les titres.
- CTA : même formule que les reels précédents.

## Limites
- **Notes auto-évaluées** par l'audit du processus lui-même ; mention affichée.
- Comptage de mots approximatif ; « en deux mois » vrai pour 64 articles seulement.
- La boucle « sous 80, on corrige et on recommence » est une **règle du skill** : le journal ne dit pas combien d'articles ont été corrigés.
- **Production ≠ indexation** : 285 pages non indexées sur 132 articles (reel SEO d'indexation). Non dit dans la vidéo.
- Aucune donnée d'audience, de trafic ou de revenus ; le SEO « pensé » n'est pas un classement obtenu.
- 6 pages montrées sur 64, parmi les mieux notées (96 à 100), toutes d'août-septembre.
- Densité : jusqu'à 60 mots visibles en même temps dans la scène des étapes (liste voulue).
- Son non écouté par moi ; à vérifier : « Claude Code », « skills », « SEO », « build ».

## Contrôles
`qa.cjs` vert · −14,1 LUFS (crête −1,3 dBFS) · 0 image figée > 1,2 s · durée 82,1 s (plafond 90 s) · transcription du mixage final : similarité 1,000 par mots · synthèse vocale : 13 + 2 + 1 appels sur cette version (le reste en cache).
