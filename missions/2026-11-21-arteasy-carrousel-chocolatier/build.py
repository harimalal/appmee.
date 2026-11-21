#!/usr/bin/env python3
"""Carrousel animé arteasy (chocolatier) : voix Google (Gemini TTS) + zooms + transitions.
Usage : python3 build.py   (GOOGLE_API_KEY dans l'environnement)"""
import base64, json, os, re, subprocess, sys, time, wave

D = os.path.dirname(os.path.abspath(__file__))
VOIX_NARRATEUR, VOIX_SOPHIE, MODELE = "Charon", "Aoede", "gemini-3.1-flash-tts-preview"
FPS, T = 30, 0.45

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

def duree(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

def appel(modele, corps):
    open(f"{D}/tmp/req.json", "w").write(json.dumps(corps))
    r = subprocess.run(["curl", "-s", "-H", f"x-goog-api-key: {os.environ['GOOGLE_API_KEY']}",
        "-H", "Content-Type: application/json",
        f"https://generativelanguage.googleapis.com/v1beta/models/{modele}:generateContent",
        "-d", f"@{D}/tmp/req.json"], capture_output=True, text=True)
    return json.loads(r.stdout)

SUF = os.environ.get("VARIANTE", "")
os.makedirs(f"{D}/tmp", exist_ok=True)
PRISE = f"{D}/voix/histoire{SUF}.wav"
if not os.path.exists(PRISE):
    texte = open(f"{D}/voix/histoire{SUF}.txt").read()
    corps = {"contents": [{"parts": [{"text": texte}]}],
      "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
        {"speaker": "Narrateur", "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOIX_NARRATEUR}}},
        {"speaker": "Sophie", "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOIX_SOPHIE}}}]}}}}
    for essai in range(4):
        d = appel(MODELE, corps)
        try:
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]); break
        except Exception:
            print("essai", essai + 1, str(d)[:200], file=sys.stderr); time.sleep(10)
    else:
        sys.exit("voix impossible")
    with wave.open(PRISE, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
AUDIO_D = duree(PRISE)

# début de chaque diapo dans la prise : voix/alignement{SUF}.json (transcription Gemini par fenêtres, recalée sur les silences)
ALIGN = f"{D}/voix/alignement{SUF}.json"

def aligner():
    """Début de chaque diapo : transcription Gemini par fenêtres de 45 s, recalée sur la fin du silence le plus proche."""
    blocs = open(f"{D}/voix/histoire{SUF}.txt").read().split("\n\n")[1:]
    am = [re.sub(r"\[[^\]]*\]", "", bl.split("\n")[0].split(": ", 1)[-1])[:70] for bl in blocs]
    liste = " | ".join(f"{i+1}. {x}" for i, x in enumerate(am))
    est, a = {1: 0.0}, 0.0
    while a < AUDIO_D - 5:
        b = min(a + 45, AUDIO_D)
        sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a), "-to", str(b), "-i", PRISE, "-b:a", "64k", f"{D}/tmp/w.mp3"])
        q = ("Extrait d'une histoire racontée en passages numérotés. Ouvertures : " + liste +
             ". Quels passages commencent dans cet extrait, et à quelle seconde depuis le début de l'extrait (précision 0,3 s) ? "
             'Réponds uniquement par un objet JSON {"numéro": secondes}.')
        d = appel("gemini-3.8-flash", {"contents": [{"parts": [{"text": q},
            {"inlineData": {"mimeType": "audio/mpeg", "data": base64.b64encode(open(f"{D}/tmp/w.mp3", "rb").read()).decode()}}]}]})
        try:
            r = json.loads(re.search(r"\{.*\}", d["candidates"][0]["content"]["parts"][-1]["text"], re.S).group(0))
            for k, v in r.items():
                k, v = int(k), float(v)
                if k not in est and 1.0 < v < (b - a) - 1.0:
                    est[k] = a + v
        except Exception as e:
            print("fenêtre", a, "illisible", e, file=sys.stderr)
        a += 35
    manque = [i for i in range(1, len(S) + 1) if i not in est]
    if manque:
        sys.exit(f"passages sans horodatage : {manque}")
    sil = subprocess.run(["ffmpeg", "-i", PRISE, "-af", "silencedetect=n=-35dB:d=0.4", "-f", "null", "-"], capture_output=True, text=True).stderr
    fins = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sil)]
    deb = [0.0]
    for i in range(2, len(S) + 1):
        p = min(fins, key=lambda f: abs(f - est[i]))
        deb.append(round((p if abs(p - est[i]) < 1.0 else est[i]) - 0.4, 2))  # voix mesurée ~0,4 s avant la fin du silence
    json.dump({"methode": "Gemini par fenêtres, recalé sur les silences", "gemini": est, "debuts": deb}, open(ALIGN, "w"), ensure_ascii=False)

if not os.path.exists(ALIGN):
    aligner()
B = json.load(open(ALIGN))["debuts"]
assert len(B) == len(S) and all(x < y for x, y in zip(B, B[1:])), B
print("débuts", [round(x, 1) for x in B], "audio", round(AUDIO_D, 1))

# la diapo i entre à l'écran juste avant ses premiers mots ; la voix est continue (une seule prise)
DECAL = 0.4
starts = [0.0] + [B[i] + DECAL - 0.1 - T for i in range(1, len(S))]
fin = AUDIO_D + DECAL + 1.2
durs = [(starts[i + 1] + T if i + 1 < len(S) else fin) - starts[i] for i in range(len(S))]
total = fin

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
entrees += ["-i", PRISE]
ms = int(DECAL * 1000)
filt.append(f"[{len(S)}:a]aresample=44100,adelay={ms}|{ms},loudnorm=I=-16:TP=-1.5[aud]")
sh(["ffmpeg", "-y", "-loglevel", "error", *entrees, "-filter_complex", ";".join(filt),
    "-map", f"[{prev}]", "-map", "[aud]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", f"{D}/sortie/arteasy-chocolatier-video-voix{SUF}-4x5.mp4"])
print("ok", total)
