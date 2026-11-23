"""Minutage de la prise vidéo : chaque slide dure de son repère au suivant,
ses étapes se répartissent sur cette durée.

  python3 -I minutage.py reperes.json slides.json minutage.json
"""
import json, sys
reperes, slides, sortie = sys.argv[1:4]
R = json.load(open(reperes)); sl = R["slides"]
S = {s["i"]: s for s in json.load(open(slides))}
tl = []
for k, s in enumerate(sl):
    T = (sl[k + 1]["abs"] if k + 1 < len(sl) else R["total"] + 1.5) - s["abs"]
    n = S[int(s["n"])]["steps"]; st = []
    for j in range(1, n + 1):
        t = 0.3 * T if n == 1 else T * (0.08 + 0.80 * (j - 1) / (n - 1))
        if st and t < st[-1] + 0.8: t = st[-1] + 0.8
        st.append(round(t, 2))
    if st and st[-1] > T - 0.3: print(f"⚠ slide {s['n']} : {n} étapes en {T:.1f} s, animations serrées")
    tl.append({"n": s["n"], "id": S[int(s["n"])]["id"], "T": round(T, 2), "steps": st})
json.dump(tl, open(sortie, "w"), indent=1)
print(len(tl), "slides,", round(sum(x["T"] for x in tl) / 60, 2), "min")
