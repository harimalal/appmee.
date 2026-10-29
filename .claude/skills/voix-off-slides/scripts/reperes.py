"""Instant où commence chaque slide dans les prises, vérifié par transcription.

  python3 -I reperes.py script.txt prises/ reperes.json

Estimation = part des mots déjà lus dans la prise, recalée sur la plus longue pause
à ±2,5 s ; vérification = les 2,5 s qui suivent doivent contenir le début du paragraphe.
"""
import json, os, re, subprocess, sys, tempfile, difflib
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voix import lire_script, transcrire, duree, mots

script, dossier, sortie = sys.argv[1:4]
TX = {n: t for n, _, t in lire_script(script)}
G = json.load(open(os.path.join(dossier, "groupes.json")))
tmp = tempfile.mkdtemp()


def pauses(f):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return [(float(a), float(b)) for a, b in zip(re.findall(r"silence_start: ([\d.]+)", log), re.findall(r"silence_end: ([\d.]+)", log))]


def entendu(f, t, n):
    c = os.path.join(tmp, f"{n}-{t:.2f}.wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-t", "2.5", "-i", f, c], check=True)
    tr, debut = mots(transcrire(c)), mots(TX[n])[:3]
    # le début du paragraphe doit apparaître dans les premiers mots (ignore un éventuel « voici la transcription »)
    return max((difflib.SequenceMatcher(None, tr[k:k + 3], debut).ratio() for k in range(min(len(tr), 10))), default=0)


def repere(args):
    f, n, est, P = args
    cand = sorted({round(e - 0.1, 2) for s, e in P if abs(e - est) <= 6}, key=lambda x: (abs(x - est) > 2.5, -[e - s for s, e in P if round(e - 0.1, 2) == x][0], abs(x - est)))
    for t in cand[:4]:
        if entendu(f, t, n) >= 0.6: return n, t, True
    return n, (cand[0] if cand else round(est, 2)), False


jobs, off, res = [], {}, {}
total = 0.0
for k, g in enumerate(G):
    f = os.path.join(dossier, f"{k + 1}.wav"); D = duree(f); P = pauses(f); off[k + 1] = total; total += D
    W = [len(TX[n].split()) for n in g]
    for j, n in enumerate(g):
        if j == 0: res[n] = (k + 1, 0.0, True)
        else: jobs.append((f, n, D * sum(W[:j]) / sum(W), P))
prise_de = {n: k + 1 for k, g in enumerate(G) for n in g}
with ThreadPoolExecutor(4) as ex:
    for n, t, ok in ex.map(repere, jobs): res[n] = (prise_de[n], t, ok)
out = [{"n": n, "prise": res[n][0], "t": res[n][1], "abs": round(off[res[n][0]] + res[n][1], 2), "verifie": res[n][2]} for n in sorted(res)]
json.dump({"slides": out, "total": round(total, 2)}, open(sortie, "w"), indent=1)
for r in out: print(r["n"], f"prise {r['prise']}", f"{r['t']:6.2f} s", "ok" if r["verifie"] else "⚠ À VÉRIFIER")
