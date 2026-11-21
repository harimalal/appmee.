#!/usr/bin/env python3
"""Carrousel animé arteasy (chocolatier) : voix Google (Gemini TTS) + zooms + transitions.
Usage : python3 build.py   (GOOGLE_API_KEY dans l'environnement)"""
import base64, json, os, subprocess, sys, time, wave

D = os.path.dirname(os.path.abspath(__file__))
VOIX, MODELE = "Charon", "gemini-2.5-flash-preview-tts"
STYLE = "Raconte à la première personne, avec chaleur, un peu d'humour, comme un artisan qui se confie : "
FPS, T, MARGE_DEBUT, MARGE_FIN, MIN_D = 30, 0.45, 0.35, 0.9, 3.6

# (texte dit, zoom début, zoom fin, focale début (x,y), focale fin (x,y))
S = [
 ("Samedi de Pâques. J'avais une liste. Le vent aussi.", 1.0, 1.08, (0.49,0.52), (0.51,0.57)),
 ("Six livraisons. Toute ma tournée tenait sur une seule feuille, griffonnée la veille au soir. Comme chaque année.", 1.0, 1.1, (0.5,0.5), (0.5,0.5)),
 ("Sept heures, à l'atelier. Manon prépare. Moi, je compte. Les commandes, je les avais en tête. Et sur la feuille, au cas où.", 1.08, 1.0, (0.51,0.57), (0.49,0.52)),
 ("Neuf heures, dans la camionnette. Fenêtre ouverte. Mauvaise idée. Un coup de vent, et ma tournée est partie sans moi.", 1.0, 1.08, (0.51,0.52), (0.49,0.57)),
 ("Six arrêts prévus. J'en ai fait cinq. L'hôtel, livré avec cinquante minutes de retard. Et le fleuriste, tout simplement oublié.", 1.0, 1.09, (0.5,0.5), (0.5,0.55)),
 ("Onze heures, chez Sophie. La vitrine attendait. Elle avait prévu ses œufs entre les tulipes. Elle m'a appelé trois fois.", 1.08, 1.0, (0.49,0.57), (0.51,0.52)),
 ("Onze heures cinquante, à l'hôtel. Le brunch avait commencé. J'avais l'adresse en tête. Pas l'heure.", 1.0, 1.08, (0.49,0.52), (0.51,0.57)),
 ("Ce que ça m'a coûté ? Quarante œufs jamais livrés chez Sophie. Cinquante minutes de retard à l'hôtel. Cent vingt euros de geste commercial. Et mon samedi de Pâques.", 1.0, 1.09, (0.5,0.5), (0.5,0.55)),
 ("Ce que j'ai compris : le vent n'y est pour rien. Mes livraisons n'existaient que sur un bout de papier. Il suffisait d'un rien.", 1.1, 1.0, (0.5,0.5), (0.5,0.5)),
 ("Le déclic. Avec arteasy, les livraisons du jour se listent depuis les commandes, avec leurs bons de livraison prêts.", 1.0, 1.08, (0.51,0.52), (0.49,0.57)),
 ("Le samedi suivant, on charge. Sans papier. Manon voit la même liste que moi. Rien ne peut s'envoler.", 1.08, 1.0, (0.49,0.57), (0.51,0.52)),
 ("Huit heures cinquante. Cette fois, je suis en avance. Bonjour Sophie, vos quarante œufs arrivent à neuf heures. Je vous attends, j'ai même le temps pour un café.", 1.0, 1.09, (0.5,0.5), (0.5,0.55)),
 ("Et vous, votre tournée tient sur quoi ? Démo gratuite sur arteasy point fr. Installation en trente minutes. Trente jours satisfait ou remboursé.", 1.0, 1.08, (0.5,0.52), (0.5,0.57)),
]

def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)

def tts(i, texte):
    out = f"{D}/voix/{i:02d}.wav"
    if os.path.exists(out):
        return out
    corps = {"contents": [{"parts": [{"text": STYLE + texte}]}],
             "generationConfig": {"responseModalities": ["AUDIO"],
               "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOIX}}}}}
    for essai in range(6):
        r = subprocess.run(["curl", "-s", "-H", f"x-goog-api-key: {os.environ['GOOGLE_API_KEY']}",
            "-H", "Content-Type: application/json",
            f"https://generativelanguage.googleapis.com/v1beta/models/{MODELE}:generateContent",
            "-d", json.dumps(corps)], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            with wave.open(out, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            return out
        except Exception:
            print(f"  voix {i}: essai {essai+1} échoué", r.stdout[:150], file=sys.stderr)
            time.sleep(8 * (essai + 1))
    sys.exit(f"voix {i} impossible")

def duree(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

os.makedirs(f"{D}/tmp", exist_ok=True)
voix = [tts(i + 1, s[0]) for i, s in enumerate(S)]
durs = [max(MIN_D, MARGE_DEBUT + duree(v) + MARGE_FIN) for v in voix]
starts, t = [], 0.0
for d in durs:
    starts.append(t); t += d - T
total = starts[-1] + durs[-1]
print("durées", [round(d, 1) for d in durs], "total", round(total, 1))

# clips avec zoom/déplacement continu
for i, (_, z0, z1, f0, f1) in enumerate(S):
    n = int(durs[i] * FPS) + 1
    p = f"(on/{n})"
    z = f"{z0}+({z1}-{z0})*{p}"
    fx = f"({f0[0]}+({f1[0]}-{f0[0]})*{p})"
    fy = f"({f0[1]}+({f1[1]}-{f0[1]})*{p})"
    x = f"max(0,min(iw-iw/zoom,{fx}*iw-iw/zoom/2))"
    y = f"max(0,min(ih-ih/zoom,{fy}*ih-ih/zoom/2))"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/diapos/{i+1:02d}.png",
        "-vf", f"scale=2160:2700:flags=lanczos,zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=1080x1350:fps={FPS},setsar=1",
        "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", f"{D}/tmp/c{i+1:02d}.mp4"])

# enchaînement (glissé / fondu alterné) + voix posée à l'instant de chaque diapo
entrees, filt = [], []
for i in range(len(S)):
    entrees += ["-i", f"{D}/tmp/c{i+1:02d}.mp4"]
prev = "0:v"
for i in range(1, len(S)):
    tr = "slideleft" if i % 3 else "fade"
    filt.append(f"[{prev}][{i}:v]xfade=transition={tr}:duration={T}:offset={starts[i]:.3f}[x{i}]")
    prev = f"x{i}"
for i, v in enumerate(voix):
    entrees += ["-i", v]
    ms = int((starts[i] + MARGE_DEBUT) * 1000)
    filt.append(f"[{len(S)+i}:a]aresample=44100,adelay={ms}|{ms}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(S))) + f"amix=inputs={len(S)}:normalize=0,loudnorm=I=-16:TP=-1.5[aud]")
sh(["ffmpeg", "-y", "-loglevel", "error", *entrees, "-filter_complex", ";".join(filt),
    "-map", f"[{prev}]", "-map", "[aud]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{D}/sortie/arteasy-chocolatier-video-voix-4x5.mp4"])
print("ok", total)
