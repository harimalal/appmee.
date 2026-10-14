# Voix off (ElevenLabs) et sous-titres

## Débit et budget
- Voix posée en anglais : ≈ 2,3 mots par seconde ; voix dynamique : ≈ 2,8. En français, compter ≈ 2,5 mots/s posée.
- 60 s de film → 120 à 140 mots, avec des silences pendant la révélation du logo et les gestes forts.
- Les nombres, sigles et symboles s'écrivent comme ils se disent dans le texte envoyé à la voix (`DIT` dans le montage : `'80/20': 'eighty-twenty'`) ; les sous-titres gardent l'écrit.

## Choisir la voix
1. `creative_list_voices` avec les filtres du brief : `gender`, `languages: ['en']`, `accent: 'american'` (code d'accent seulement si une seule langue), `descriptives` (ex. `['calm', 'confident']` pour « calme, type startup »), `use_cases: ['advertisement']` ou `['informative_educational']`.
2. Prendre une voix dont la description parle d'explication produit, de démo d'app ou de SaaS, sans ton « vendeur » (Dropit : « Justin Case – Warm, Trustworthy, Clear », `DtQLDxHbTiQTpVVanTy1`, homme américain posé). Dire à l'utilisateur laquelle et pourquoi. Un `voice_id` vient toujours de cette liste ou de l'utilisateur, jamais de mémoire.

## Générer la prise
1. Texte complet : `node scripts/voix-off.cjs --montage montage-60s.cjs --texte` (consigne de ton entre crochets en tête, une ligne vide entre les répliques : la voix y marque une vraie pause).
2. `creative_generate_speech` avec `model_id: 'eleven_v4'`, ce `voice_id`, ce texte. Elle produit 4 variantes (coût ≈ 750 crédits chacune pour 130 mots, en octobre 2026). Ne relance jamais l'appel pour « réessayer » : chaque appel est facturé.
3. `creative_get_flow_run_status` (flow_id + session_ids) jusqu'à `all_completed`. Chaque génération a une `content_url` (lien signé valable 2 h).
4. Télécharger : `curl -sS -o voix/prise.mp3 "<content_url>"`. Si le réseau bloque `storage.googleapis.com`, demander à l'utilisateur de télécharger la prise depuis le lien du flow ElevenLabs et de la déposer dans `voix/`.
5. Choisir la prise : sans pouvoir écouter, prendre la première par défaut, et dire à l'utilisateur que les autres sont dans le flow ElevenLabs s'il en préfère une.

## Horodatage mot par mot
Les silences ne suffisent pas pour découper la prise : les pauses entre phrases d'une même réplique sont aussi longues que celles entre répliques. Il faut l'horodatage de chaque mot.
1. `creative_add_flow_asset_node` (modality `audio`, `generation_id` de la prise retenue, même `flow_id`) → node_id.
2. `creative_transcribe_audio` avec `connect_from: [node_id]`, `model_id: 'eleven_scribe_v1'` (gratuit dans l'essai Dropit).
3. `creative_get_flow_run_status` → `transcripts[0].words_download_url` ; télécharger en `voix/prise.mots.json` à côté de la prise.
Une reconnaissance locale (faster-whisper) demande de télécharger un modèle sur huggingface.co, souvent bloqué dans les environnements cloud.

## Caler et mixer
```bash
node scripts/voix-off.cjs --montage montage-60s.cjs --prise voix/prise.mp3 --muet sortie/video/film-60s-court-muet.mp4 --essai
```
Lire le placement : une réplique « en retard » de plus de 0,5 s ou une voix qui dépasse la fin du film se corrige dans le **montage** (ralentir le morceau concerné, ralentir la fin, ou avancer l'instant de la réplique), pas en régénérant la voix. Relancer sans `--essai` (et avec `--sortie`, `--nom`, `--langue`) une fois le placement bon. Si le montage change, refaire le rendu `court` d'abord.
Contrôle : `ffmpeg -i sortie/<nom>-voix.m4a -af silencedetect=noise=-40dB:d=0.6 -f null -` doit montrer des silences aux bons endroits ; `ebur128` doit donner ≈ −16 LUFS.

## Sous-titres
- `.srt` pour YouTube (YouTube Studio › Sous-titres › Importer un fichier › avec horodatage), `.vtt` pour une balise `<track>` de page web, et une piste `mov_text` activable dans le MP4 maître.
- Ne pas les incruster si le film a déjà de gros textes à l'écran (ils se superposent). Les incruster seulement pour une version réseaux sans textes à l'écran : `ffmpeg -i film.mp4 -vf "subtitles=film.en.srt:force_style='FontName=…,FontSize=…,MarginV=60'" …`.
- Une page publiée qui ne sert pas les `.vtt` peut créer la piste en JavaScript : `video.addTextTrack('subtitles', 'English', 'en').addCue(new VTTCue(début, fin, texte))`.

## Musique
Pas d'outil fiable pour la générer : demander un morceau libre de droits à l'utilisateur, puis le mixer sous la voix à −20 dB avec un « ducking » (`sidechaincompress`) et un fondu de sortie sur les 2 dernières secondes.
