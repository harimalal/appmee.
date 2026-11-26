# Formats par réseau (référence 2026 — vérifier une règle précise avant une publication sensible)

Tailles en pixels. « Sûr » = zone où rien d'important ne doit être caché par l'interface du réseau.

## Images et carrousels

| Réseau | Usage | Format conseillé | Notes |
|---|---|---|---|
| Instagram | Post, carrousel | **1080×1350** (4:5) ; 1080×1080 possible | Carrousel : 2 à 20 images, toutes au même format. La grille de profil recadre en 3:4 au centre. |
| Instagram, Facebook | Story | 1080×1920 (9:16) | Sûr : laisser 250 px libres en haut et 340 en bas. |
| LinkedIn | Post image | 1080×1350 ou 1200×1200 | Le 4:5 prend le plus de place dans le fil. |
| LinkedIn | Carrousel (document) | **PDF**, pages 1080×1350 (ou 1080×1080) | 5 à 12 pages ; téléversé comme « document ». `rendre.cjs … diapos --pdf`. |
| X (Twitter) | Post image | 1600×900 (16:9) ou 1080×1350 | Jusqu'à 4 images par post. |
| Facebook | Post image | 1080×1350 ou 1200×630 (lien) | |
| Pinterest | Épingle | 1000×1500 (2:3) | |
| Threads, Bluesky | Post image | 1080×1350 | |
| Partout | Image de partage d'un lien (Open Graph) | 1200×630 | Texte au centre, rien d'important à moins de 60 px des bords. |
| Product Hunt | Galerie | 1270×760 (exporter ×2) | 1re image = la promesse ; 6 à 8 images ; la vidéo doit être un lien YouTube. |
| Product Hunt | Vignette | 240×240 (exporter 480×480), GIF animé possible | La 1re image du GIF est celle qui s'affiche hors survol. |
| YouTube | Miniature | 1280×720 | 3 à 5 mots, lisible en petit. |
| App Store | Captures iPhone | 1290×2796 (6,7″) ; 1242×2688 accepté | 3 à 10 captures ; la 1re et la 2e font l'essentiel. |
| Google Play | Captures | 1080×1920 (9:16) à 1080×2340 | Plus une image de présentation 1024×500. |

## Vidéos

| Réseau | Format | Durée conseillée | Notes |
|---|---|---|---|
| YouTube | 1920×1080 (16:9) | 60 s à 2 min | Sous-titres en `.srt` séparés ; miniature 1280×720. |
| YouTube Shorts, TikTok, Reels | 1080×1920 (9:16) | **15 à 30 s** (60 s au plus pour rester efficace) | Sûr : 250 px en haut, 400 px en bas, 120 px à droite (boutons). Sous-titres incrustés utiles (lecture sans le son). |
| Instagram fil | 1080×1350 (4:5) | 15 à 30 s | |
| LinkedIn | 1920×1080 ou 1080×1350 | 30 à 90 s | Joué sans le son : textes à l'écran indispensables ; `.srt` téléversable. |
| X | 1920×1080 ou 1080×1350 | 15 à 45 s | |
| Product Hunt | lien YouTube | 60 s à 1 min 30 | |
| Landing page | 1920×1080 ou 1080×1350, MP4 web (crf 26) | 20 à 60 s, en boucle, muet | Aussi en GIF léger pour les e-mails. |

## Longueurs de vidéo et ce qu'elles contiennent

| Durée | Contenu |
|---|---|
| 6 s (accroche publicitaire) | promesse + un geste de l'app + logo |
| 15 s (teaser) | accroche (2 s) + promesse (3 s) + la fonctionnalité phare (7 s) + fin (3 s) |
| 30 s | accroche + problème court + promesse + 2 fonctionnalités + fin |
| 60 s | tout le récit, 3 ou 4 fonctionnalités, voix off |
| 90 s à 2 min | film long : tous les actes, toutes les fonctionnalités, récapitulatif |

Toutes ces versions se taillent dans le film long (16:9) avec un fichier de montage (`montage-15s.cjs`, `montage-30s.cjs`…), ou se construisent dans le diaporama animé pour les formats verticaux et carrés.

## Poids et encodage
- Vidéo : H.264 + AAC, `yuv420p`, `+faststart` ; maître crf 21, web crf 26. Les réseaux recompressent : envoyer le maître.
- Images : JPEG qualité 90 pour les photos et dégradés, PNG pour les aplats et les textes fins ; sous 5 Mo par image (X, LinkedIn), sous 30 Mo par image (Instagram).
- GIF : 15 images/s, palette 48 à 64 couleurs, largeur 480 à 800 px ; sous 3 Mo pour un e-mail.
