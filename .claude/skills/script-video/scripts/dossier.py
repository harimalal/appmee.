"""Dossier commun des agents de la simulation : fiche technique + déroulé minuté voix/écran.

  python3 -I dossier.py script.txt slides.json minutage.json fiche.md dossier.md

fiche.md : quelques lignes écrites à la main (titre visé, chaîne, voix, débit, musique, sous-titres, structure…).
minutage.json : celui du skill voix-off-slides (ou une estimation : [{"n","id","T","steps"}]).
"""
import json, re, sys
script, slides, minutage, fiche, sortie = sys.argv[1:6]
p = re.split(r"^##(\d\d) (\S+)\n", open(script).read(), flags=re.M)[1:]
TX = {n: t.strip() for n, t in zip(p[::3], p[2::3])}
S = {s["i"]: s for s in json.load(open(slides))}
tl = json.load(open(minutage))
t, L = 0.4, []
for x in tl:
    m, s = divmod(int(t), 60)
    L.append(f"### [{m}:{s:02d}] Slide {x['n']} ({x['id']}) — {x['T']:.0f} s, {len(x['steps'])} animations\n"
             f"VOIX : {TX.get(x['n'], '')}\nÉCRAN : {S[int(x['n'])]['text'][:600]}\n")
    t += x["T"]
m, s = divmod(int(t), 60)
open(sortie, "w").write(f"# Dossier vidéo à évaluer\n\nDurée : {m} min {s:02d}\n\n## Fiche technique\n{open(fiche).read().strip()}\n\n## Déroulé minuté (voix + écran)\n" + "\n".join(L))
print(sortie, f"({m} min {s:02d}, {len(tl)} slides)")
