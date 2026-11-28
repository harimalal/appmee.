# SCRIPT — Reel « Comment j'ai comparé les outils IA en 28 comparatifs » (v4, 86,8 s, 1080×1920, 30 fps)

Skill : reel-histoire (5e essai). Source : artefact « Comparatif Factory » (04/10/2026), croisé avec `SKILL_COMPARATIF_FACTORY.md`, `Comparatif Outils/PUBLISH_QUEUE_COMPARATIFS.md` et les 28 fichiers `src/content/blog/compare_*.md`. Décisions de Hari : playbook « Comparatif Factory », hook gardé, affiliation seulement dans ce fichier ; v4 (27/11) : le skill et le système sont introduits face à une simple demande ChatGPT / Claude, le piège « mêmes critères pour tous » est dit, les critères par type sont raccourcis. v3 : on retire « 4 critères, score sur 20, prix, avis », on explique ce que le comparatif prend en compte (critères indispensables, qui changent d'un type d'outil à l'autre), 3 exemples, puis les vrais comparatifs à l'écran, les cas d'usage et les profils. Voix : Google Gemini TTS, voix Charon, modèle `gemini-3.8-flash-lite-tts`. Rendu 100 % local ; aucune image générée : tableaux, cas d'usage et profils sont de vrais éléments de comparatifs publiés, captés sur le site construit en local. Versions précédentes gardées en local, non versionnées : `out/reel-comparatif-factory-v1-petites-fenetres.mp4`, `out/reel-comparatif-factory-v2-moteur.mp4`, `out/reel-comparatif-factory-v3-critere-chiffres.mp4`.

## Texte lu (18 phrases)
t0 Chaque outil IA se dit le meilleur.
t1 Comment s'y retrouver, pour ce dont tu as besoin, sans passer des heures sur différents sites ?
t2 J'ai fait vingt-huit comparatifs, un par type d'outil.
s0 Je les ai faits avec un skill et un système, pour un résultat complet.
s0b Une simple demande à ChatGPT ou à Claude reste superficielle : elle ne tient pas compte de tous les paramètres de chaque type d'outil.
s2 Pour chaque type, je commence par ce qui compte vraiment : les critères indispensables.
s3 Chaque outil est ensuite noté sur ces critères, à partir de recherches, sans rien inventer.
c1 Le piège : prendre les mêmes critères pour tous les outils.
c2 Voix IA : la qualité, le clonage, les langues.
c3 Code : les suggestions, l'autonomie, l'éditeur.
c4 CRM : le pipeline, l'automatisation, l'IA native.
tb1 D'abord, un tableau : les outils, leurs notes sur vingt, le prix et les avis.
d2 Voilà trois de ces comparatifs, tels qu'ils sont publiés.
u1 Ensuite, ce que les utilisateurs créent avec ces outils : six cas d'usage, chacun avec les outils qui vont avec.
pf1 Et pour chaque profil, l'outil le plus adapté : créateur YouTube, équipe formation, développeur, agence de doublage.
n2 Dans chacun : six cas d'usage, et entre six et huit profils.
n3 Les notes viennent de mes sources, pas d'un test indépendant.
k1 Abonne-toi pour plus d'astuces IA : sans compétences techniques, rapides, et terriblement efficaces.
Retouche de formulation antérieure : s2 (« je pars de » entendu « je parle de » → « je commence par »). Le prix, dit à l'écran seulement, figure dans les critères de chaque carte.

## Sources des nombres et des critères
| Élément | Source | Statut |
|---|---|---|
| 28 comparatifs, d'août à octobre | 28 fichiers `compare_*.md` (tous `format: "guide"`) ; 17 en août, 5 en septembre, 6 en octobre 2026 | mesuré par comptage |
| 6 cas d'usage par comparatif | cartes `cmp-content-card` : 6 dans chacun des 28 (168 en tout) | mesuré par motif HTML |
| 6 à 8 profils par comparatif | cartes `cmp-profile-card` : 6 à 8 par comparatif (178 en tout) | mesuré par motif HTML |
| Critères des 3 exemples | en-têtes des tableaux publiés : Voix IA = Qualité · Clonage · Langues · Prix ; Assistants de code = Suggestions · Agentique · IDE · Prix ; CRM & marketing = CRM & Pipeline · Marketing auto. · IA native · Prix | lus sur les pages ; chaque page explique ses 4 critères dans un encart « 4 critères pour choisir votre… » |
| « notes sur vingt » | colonne « Score /20 » des tableaux | lu sur les captures |

Écartés : « 1 comparatif par jour » (artefact) et « 2 par jour » (en-tête de la file) : cadence réelle 28 comparatifs en 82 jours ; 25 « Publié le » dans la file (28 fichiers) ; 213 noms d'outils dans le champ `outils` (non dédoublonnés) ; « 4 critères, score sur 20 » et « 10 sections, build » (retirés de la voix à la demande de Hari).

## Ce qui vient de Hari, non sourcé dans le dépôt
- **s0 et s0b (« un skill et un système, pour un résultat complet » ; « une simple demande à ChatGPT ou à Claude reste superficielle et ne tient pas compte de tous les paramètres de chaque type d'outil ») : constat de Hari, non testé ici ; la vidéo ne dit rien sur les capacités de ChatGPT ou de Claude au-delà de son expérience.** Le piège « mêmes critères pour tous » : formulation de Hari, étayée par le fait que les en-têtes de critères diffèrent d'un comparatif à l'autre (voir sources).
- « Chaque outil IA se dit le meilleur » ; « sans passer des heures sur différents sites » ; « les critères indispensables » (les must-haves d'un type d'outil) ; « par métier » = les profils des comparatifs ; CTA : formule des reels précédents.

## Limites
- **Les scores viennent de la notation des comparatifs sources de Reflex IA** (recherche web : notes G2/Capterra, prix, avis), **pas d'un test indépendant** : dit à l'écran et à la voix.
- « Sans rien inventer » : règle du moteur, pas une vérification ligne par ligne.
- **Affiliation (non dite dans la vidéo, sur décision de Hari)** : les sources s'appellent `comparatif_affiliation_*` et 6 des 28 articles mentionnent des programmes d'affiliation.
- Prix et notes datés d'août à octobre 2026, susceptibles d'avoir changé.
- **5 tableaux sur 28 ne sont pas strictement triés par score** (Rédaction & Copywriting, LLM, Plateformes IA natives, Moteurs de recherche IA, Outils GEO) : correction de l'annonce précédente (« 2 »), qui reposait sur un contrôle incomplet. Les 3 exemples montrés (voix IA, assistants de code, CRM) sont triés. Défaut des pages non corrigé ici.
- 3 comparatifs montrés sur 28, choisis pour leurs critères différents et leur tri correct ; les cas d'usage et les profils viennent du seul comparatif « Voix IA ».
- Aucune donnée d'audience, de clics ou de revenus.
- Son non écouté par moi ; à vérifier : « CRM », « IA native », « Claude Code ».

## Contrôles
`qa.cjs` vert · −14,2 LUFS (crête −1,2 dBFS) · 0 image figée > 1,2 s · durée 86,8 s (sous 90 s) · transcription du mixage final : 0,982 par mots (écarts : pluriels) · synthèse vocale : 6 appels pour la v4 (10 + 1 pour la v3), le reste en cache.
