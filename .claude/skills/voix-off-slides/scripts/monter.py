"""Assemble la prise vidéo et la voix, puis contrôle le calage.

  python3 -I monter.py prise/journal.json prises/ video.mp4 [script.txt]

La voix complète (prises bout à bout) démarre 0,4 s après le premier changement de slide.
Contrôle : écart plan/prise, puis transcription de 4 s et une image à 4 changements de slide.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voix import transcrire, lire_script

journal, dossier, sortie = sys.argv[1:4]
L = json.load(open(journal)); G = json.load(open(os.path.join(dossier, "groupes.json")))
liste = os.path.join(dossier, "liste.txt")
open(liste, "w").write("".join(f"file '{k + 1}.wav'\n" for k in range(len(G))))
voix = os.path.join(dossier, "voix-complete.wav")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", voix], check=True)

s0 = L["slides"][0]
ecart = max(abs((s["start"] - s0["start"]) - (s["prevu"] - s0["prevu"])) for s in L["slides"])
print(f"écart max plan/prise : {ecart:.2f} s" + ("  ⚠" if ecart > 0.1 else ""))
t0 = s0["start"] - 0.1; dur = L["end"] - t0
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", L["video"], "-i", voix,
                "-filter_complex", "[0:v]crop=1920:1080:16:0,fps=30,format=yuv420p[v];[1:a]aresample=48000,adelay=400|400,apad[a]",
                "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-c:a", "aac", "-b:a", "160k", sortie], check=True)
print(f"vidéo : {dur / 60:.2f} min → {sortie}")

TX = {n: t for n, _, t in lire_script(sys.argv[4])} if len(sys.argv) > 4 else {}
S = L["slides"]; base = os.path.splitext(sortie)[0]
for k in sorted({0, len(S) // 3, 2 * len(S) // 3, len(S) - 1}):
    s = S[k]; t = s["start"] - t0
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-t", "4", "-i", sortie, "-vn", base + "-c.wav"], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t + 2:.2f}", "-i", sortie, "-frames:v", "1", "-vf", "scale=640:-1", f"{base}-slide{s['n']}.png"], check=True)
    print(f"slide {s['n']} à {t:.1f} s → entendu : {transcrire(base + '-c.wav')[:70]!r}")
    if TX: print(f"            attendu : {TX[s['n']][:70]!r}")
os.remove(base + "-c.wav")
print("Regarder les images", base + "-slide*.png")
