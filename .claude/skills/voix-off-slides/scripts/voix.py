"""Voix off Gemini : casting, prises, transcription.

  python3 -I voix.py casting extrait.txt casting/ --voix Puck,Achird,Iapetus [--modele M]
  python3 -I voix.py prises script.txt prises/ --voix Achird [--modele M] [--mots 300]
  python3 -I voix.py transcrire fichier.wav

Le texte est envoyé SEUL : toute consigne de jeu serait lue à voix haute.
Clé : GOOGLE_API_KEY.
"""
import argparse, base64, difflib, json, os, re, subprocess, sys, time, urllib.error, urllib.request, wave
from concurrent.futures import ThreadPoolExecutor

API = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent?key={}"
MODELE = "gemini-2.5-flash-preview-tts"
TRANSCRIPTEUR = "gemini-3.5-flash"


def _post(modele, body, timeout=600):
    req = urllib.request.Request(API.format(modele, os.environ["GOOGLE_API_KEY"]),
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    for essai in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=timeout))
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code == 429 and "PerDay" in msg:
                raise SystemExit(f"Quota journalier atteint pour {modele} : {msg[:300]}")
            if e.code in (429, 500, 503) and essai < 3:
                time.sleep(20 * (essai + 1)); continue
            raise SystemExit(f"HTTP {e.code} sur {modele} : {msg[:300]}")


def tts(texte, sortie, voix, modele=MODELE):
    body = {"contents": [{"parts": [{"text": texte}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voix}}}}}
    c = _post(modele, body)["candidates"][0]
    if "content" not in c:
        raise SystemExit(f"Pas d'audio ({c.get('finishReason')}) : texte trop long ?")
    b = base64.b64decode(c["content"]["parts"][0]["inlineData"]["data"])
    if b[:4] == b"RIFF":                      # WAV complet (gemini-3.8-flash-tts)
        open(sortie, "wb").write(b)
    else:                                     # PCM 16 bits 24 kHz brut (2.5 / 3.1)
        w = wave.open(sortie, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b); w.close()


def transcrire(fichier):
    body = {"contents": [{"parts": [
        {"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(open(fichier, "rb").read()).decode()}},
        {"text": "Transcris mot pour mot ce qui est dit dans cet audio, en français. Réponds uniquement par la transcription."}]}]}
    d = _post(TRANSCRIPTEUR, body, timeout=300)
    return "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"]).strip()


def duree(fichier):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fichier]))


def mots(s):
    return re.sub(r"[^a-zà-ÿ0-9 ]", " ", s.lower().replace("’", "'")).split()


def lire_script(chemin):
    """##NN id\\ntexte → [(n, id, texte)]"""
    p = re.split(r"^##(\d\d) (\S+)\n", open(chemin).read(), flags=re.M)[1:]
    return [(n, i, t.strip()) for n, i, t in zip(p[::3], p[1::3], p[2::3])]


def controle(texte, fichier):
    tr = transcrire(fichier)
    r = difflib.SequenceMatcher(None, mots(texte), mots(tr)).ratio()
    return r, len(texte.split()) / duree(fichier) * 60, tr


def cmd_casting(a):
    os.makedirs(a.dossier, exist_ok=True); texte = open(a.extrait).read().strip()
    def un(v):
        f = os.path.join(a.dossier, f"{v}.wav"); tts(texte, f, v, a.modele)
        r, wpm, _ = controle(texte, f)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f, "-b:a", "128k", f[:-4] + ".mp3"], check=True)
        return v, r, wpm
    with ThreadPoolExecutor(3) as ex:
        for v, r, wpm in ex.map(un, a.voix.split(",")):
            print(f"{v:15} texte {r:.0%}  {wpm:.0f} mots/min" + ("  ⚠ ne lit pas le texte" if r < 0.8 else ""))


def cmd_prises(a):
    os.makedirs(a.dossier, exist_ok=True); S = lire_script(a.script)
    groupes, n = [[]], 0
    for s in S:                                   # coupe entre deux slides, ≈ a.mots mots par prise
        if n >= a.mots * 0.95 and groupes[-1]: groupes.append([]); n = 0
        groupes[-1].append(s); n += len(s[2].split())
    json.dump([[s[0] for s in g] for g in groupes], open(os.path.join(a.dossier, "groupes.json"), "w"))
    def une(k):
        g = groupes[k]; texte = "\n\n".join(s[2] for s in g); f = os.path.join(a.dossier, f"{k + 1}.wav")
        for essai in range(2):
            tts(texte, f, a.voix, a.modele); r, wpm, _ = controle(texte, f)
            if r >= 0.85 and 140 <= wpm <= 230: break
        return k + 1, len(texte.split()), duree(f), wpm, r
    with ThreadPoolExecutor(4) as ex:
        for k, nm, d, wpm, r in ex.map(une, range(len(groupes))):
            print(f"prise {k} : {nm} mots, {d:.0f} s, {wpm:.0f} mots/min, texte {r:.0%}" + ("  ⚠ à écouter" if r < 0.85 or not 140 <= wpm <= 230 else ""))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("casting"); c.add_argument("extrait"); c.add_argument("dossier"); c.add_argument("--voix", required=True); c.add_argument("--modele", default=MODELE)
    p = sp.add_parser("prises"); p.add_argument("script"); p.add_argument("dossier"); p.add_argument("--voix", default="Achird"); p.add_argument("--modele", default=MODELE); p.add_argument("--mots", type=int, default=300)
    t = sp.add_parser("transcrire"); t.add_argument("fichier")
    a = ap.parse_args()
    if a.cmd == "transcrire": print(transcrire(a.fichier))
    else: {"casting": cmd_casting, "prises": cmd_prises}[a.cmd](a)
