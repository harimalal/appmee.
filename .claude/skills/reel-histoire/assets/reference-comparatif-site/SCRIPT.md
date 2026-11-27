# SCRIPT — Reel « 28 comparatifs » (v6) — contenu de la v4, plus péchu, démo plein cadre façon site
Skill : reel-histoire (appmee, branche `claude/skill-reel-histoire`). Source : les 28 comparatifs publiés dans le dépôt Reflex IA + ce que Hari dit.
Fichier : `CONTENT/REELS_INSTAGRAM/reel-instagram-reflexia-5.mp4` (remplace la v5 ; une seule version gardée) · **sans musique** (voix + petits bruitages synchronisés ; Hari ajoute sa musique) · 1080×1920 · 30 i/s · **75,9 s** · −14,1 LUFS · aucune image figée plus de 1,2 s · aucun texte qui en chevauche un autre (760 instants, toutes les 0,1 s) · transcription du mixage final comparée par mots : **0,967** (écarts = nombres écrits en chiffres : vingt-huit→28, vingt→20, six→6, huit→8 ; « leurs notes »→« leur note »).
Voix : Gemini TTS, voix Charon, **modèle `gemini-3.8-flash-tts`** (le modèle « lite » avait atteint son plafond du jour) ; accélérée de 16 % (`tempo` 1,16), silences de 0,08 s ; 17 phrases (16 facturées cette fois) ; voix légèrement différente des reels de ce matin.

## Lecture de la consigne de Hari
« Oublie l'instruction précédente, c'était une erreur. Je préfère largement la version précédente. Fais-le un peu plus dynamique, péchu, familier ; arrête la démo dans la fenêtre, fais sans cadre ; fais une démo comme sur un site : zoom, clique, swipe… » → **base = la v4 (86,8 s)** (confirmé par Hari) : accroche « chaque outil IA se dit le meilleur » → skill + système face à une simple demande → critères indispensables et note → piège des mêmes critères (Voix IA, Code, CRM) → tableau → cas d'usage → profils → chiffres → limite. **Gardés de la v5** (non contredits) : CTA à mot-clé « comparatif », sans musique, « REFLEX·IA » en haut au milieu. Règle « une seule version » confirmée par Hari : les v4 et v5 ont été supprimées (sources dans l'historique git).

## Texte lu (mot pour mot)
**Accroche**
1. Chaque outil IA se dit le meilleur, hein !
2. Alors comment tu t'y retrouves, sans perdre des heures de site en site ?
3. J'ai fait vingt-huit comparatifs, un par type d'outil !

**Skill + système, critères, note**
4. Et je les ai faits avec un skill et un système : c'est complet !
5. Une simple demande à ChatGPT ou à Claude ? Franchement, ça reste superficiel : ça ne tient pas compte de tous les paramètres de chaque type d'outil.
6. Pour chaque type, je commence par ce qui compte vraiment : les critères indispensables.
7. Puis je note chaque outil là-dessus, à partir de recherches, sans rien inventer !

**Le piège : pas les mêmes critères (démo : clic des colonnes, swipe entre 3 comparatifs)**
8. Et le piège, c'est de prendre les mêmes critères pour tous les outils !
9. Voix IA : la qualité, le clonage, les langues.
10. Code : les suggestions, l'autonomie, l'éditeur.
11. CRM : le pipeline, l'automatisation, l'IA native.

**Le tableau (démo : swipe du tableau, Score, Prix, Avis)**
12. Après, direct, un tableau : les outils, leurs notes sur vingt, le prix et les avis !

**Les cas d'usage (démo : scroll, clics sur des cartes)**
13. Ensuite, ce que les gens créent avec ces outils : des cas d'usage, avec les bons outils pour chacun !

**Les profils (démo : scroll, clic, swipe vers un autre comparatif)**
14. Et pour chaque profil, l'outil le plus adapté : créateur, équipe, développeur, agence !

**Les chiffres et la limite**
15. Dans chacun : six cas d'usage, et entre six et huit profils !
16. Attention, les notes viennent de mes sources, pas d'un test indépendant.

**Appel**
17. Tu veux le même système pour tes besoins ? Commente « comparatif », et je t'envoie le système IA pour l'adapter à ta sauce !

Écran seulement (non lu) : « Chaque outil se dit le meilleur » · « Comment t'y retrouver ? » · « 28 comparatifs » · « Un skill + un système / complet » · « Une simple demande : superficiel » · « 1. Les critères indispensables » · « 2. Une note par outil » · « Pas les mêmes critères » · « Voix IA · Code · CRM : leurs critères » · « Notes sur 20 / Prix / Avis » · « Les cas d'usage » · « Un outil par profil » · « 28 · 6 · 6 à 8 » · « Notes = mes sources » · « Commente « comparatif » » · « Tu veux le même système ? ».

## Mise en scène
- **Sans cadre** : plus de fenêtre de navigateur ; la vraie page (version ordinateur 1 280 px) occupe tout l'écran 1 080 × 1 920 ; étiquette unique sur un bandeau blanc en haut ; « REFLEX·IA » en haut au milieu.
- **Démo façon site** : un **curseur** se déplace sur les vraies pages ; des **clics** (onde violette + surbrillance jaune) sur de vraies cibles (carte « Clonage vocal IA » de la page Guides, en-têtes de colonnes Qualité/Clonage/Langues, Suggestions/Agentique/IDE, CRM/Marketing/IA native, Score/Gratuit·Prix/Avis, cartes de cas d'usage et de profils) ; **scroll** continu ; **zooms** sur ce qui est dit ; **swipes** (doigt qui glisse) d'un comparatif à l'autre (Voix IA → Code → CRM, puis Voix IA → Code pour les profils) et swipe horizontal du tableau pour révéler les colonnes cachées (Score, Prix, Avis) ; **plongée** (zoom) de la liste des guides dans un comparatif.
- Les positions des cibles sont **mesurées dans les vraies pages** (`assets/pc2/pages.json`) ; les captures sont des pages entières en version ordinateur (`assets/pc2/`), plus `assets/pc/voix-tableau.jpg` (tableau déplié) pour le swipe horizontal.
- Scènes « skill + système » et « chiffres » : cartes sur fond coloré (schéma, pas une page réelle).

## Sources et statuts
| Élément | Source | Statut |
|---|---|---|
| 28 comparatifs, d'août à octobre 2026 | 28 fichiers `compare_*.md` (tous `format: "guide"`, donc dans la rubrique Guides) | mesuré par comptage |
| Six cas d'usage par comparatif | cartes `cmp-content-card` : 6 dans chacun des 28 | mesuré par motif HTML |
| Six à huit profils par comparatif | cartes `cmp-profile-card` : 6 à 8 par comparatif | mesuré par motif HTML |
| Critères des 3 exemples | en-têtes des tableaux publiés : Voix IA = Qualité · Clonage · Langues ; Code = Suggestions · Agentique · IDE ; CRM = CRM & Pipeline · Marketing auto. · IA native | lus sur les pages |
| « Notes sur vingt », prix, avis | colonnes « Score /20 », « Gratuit · Prix », « Avis » des tableaux | lus sur les pages |
| « Un par type d'outil » | un comparatif par catégorie d'outil | lecture des titres |

## Ce qui vient de Hari, non sourcé dans le dépôt
- **Phrases 4 et 5 (« un skill et un système : c'est complet » ; « une simple demande à ChatGPT ou à Claude, franchement, ça reste superficiel : ça ne tient pas compte de tous les paramètres de chaque type d'outil ») : constat de Hari, non testé ici** ; la vidéo ne dit rien sur les capacités de ChatGPT ou de Claude au-delà de son expérience.
- « Chaque outil IA se dit le meilleur » (rhétorique) ; « sans perdre des heures de site en site » (formule v4 de Hari).
- **CTA** : « Commente « comparatif »… je t'envoie le système IA » = promesse de Hari ; **le système envoyé n'est pas nommé** (je ne sais pas quel fichier c'est).

## Limites
- **Les scores viennent de la notation des comparatifs sources de Reflex IA** (recherche web : notes G2/Capterra, prix, avis), **pas d'un test indépendant** : dit à l'écran et à la voix.
- Prix et notes datés d'août à octobre 2026, susceptibles d'avoir changé.
- **5 tableaux sur 28 ne sont pas strictement triés par score** (Rédaction & Copywriting, LLM, Plateformes IA natives, Moteurs de recherche IA, Outils GEO) ; les 3 exemples montrés (voix IA, assistants de code, CRM) sont triés. Défaut des pages non corrigé ici.
- Dans la vraie page, le tableau défile horizontalement (colonnes Score, Prix, Avis cachées au départ) : le swipe du tableau est donc fidèle ; l'image du tableau déplié est remplacée par une capture à part pour le geste.
- Le curseur, les clics et les swipes sont **une mise en scène** posée sur de vraies pages, pas un enregistrement d'écran.
- **Affiliation (non dite dans la vidéo, décision antérieure de Hari)** : 6 des 28 articles mentionnent des programmes d'affiliation.
- Aucune donnée d'audience, de clics ou de revenus. Son non écouté par moi ; rendu non vu sur téléphone.

## Contrôles
`qa.cjs` vert (nombres autorisés 28, 20, 6, 8, 1, 2) · 0 chevauchement sur 760 instants · ffprobe 1080×1920 / 30 i/s / 75,9 s · −14,1 LUFS · freezedetect (n=0,0008, d=1,2 s) : 0 (après ajout d'une légère dérive de caméra sur trois passages immobiles) · transcription du mixage : 0,967.

## Pipeline (depuis ce dossier, `GOOGLE_API_KEY` en variable d'environnement, jamais affichée)
`python3 -I tts.py $W` → `python3 -I plan.py` → `node events.cjs` → `node qa.cjs` → `node synth.cjs $W` → `node render.cjs --out out/reel-muet.mp4 --frames $W/frames --workers 4` → `python3 -I mix.py $W out/reel-muet.mp4 <sortie>.mp4 --sans-nappe`
Captures : pages entières du site construit en local (`/guides/` et les comparatifs Voix IA, Code, CRM, 1 280 px, échelle 1,5) + relevé des positions dans `assets/pc2/pages.json`.
