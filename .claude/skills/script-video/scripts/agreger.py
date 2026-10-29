"""Agrège les spectateurs simulés : rétention (avec intervalle à 90 % par tirage sur les panels),
durée moyenne, clic sur l'impression, engagement, notes, profils, départs par tranche de 30 s.

  python3 -I agreger.py simu/ 260                          (fichiers panel-*.json ou segment-*.json)
  python3 -I agreger.py simu/ 260 --avant ancien/ 367      (compare à une simulation précédente)
"""
import glob, json, os, random, statistics as st, sys, collections


def charger(dossier):
    P = {}
    for f in sorted(glob.glob(os.path.join(dossier, "panel-*.json")) + glob.glob(os.path.join(dossier, "segment-*.json"))):
        P[os.path.basename(f).split("-", 1)[1][:-5]] = json.load(open(f))
    return P


def ret(V, t, D):
    return 100 * sum(min(v["watch_s"], D) >= min(t, D) for v in V) / len(V)


def ic(P, f, n=2000):
    """intervalle à 90 % en retirant les panels avec remise (les spectateurs d'un même agent ne sont pas indépendants)"""
    k = list(P); random.seed(1); x = sorted(f([v for _ in k for v in P[random.choice(k)]]) for _ in range(n))
    return round(x[int(.05 * n)]), round(x[int(.95 * n)])


def resume(P, D):
    V = [v for p in P.values() for v in p]; o = {"n": len(V), "duree": D}
    pts = sorted({15, 30, 60, 90, 120, 180, 240, D} | {round(D * q) for q in (.25, .5, .75)})
    o["retention"] = {t: [round(ret(V, t, D)), *ic(P, lambda W, t=t: ret(W, t, D))] for t in pts if t <= D}
    o["retention_pct_duree"] = {f"{q}%": round(ret(V, D * q / 100, D)) for q in (25, 50, 75, 100)}
    avd = lambda W: st.mean(min(v["watch_s"], D) for v in W)
    o["duree_moyenne_s"] = [round(avd(V)), *ic(P, avd)]; o["duree_moyenne_pct"] = round(100 * avd(V) / D)
    for k in ("clic_spontane", "like", "subscribe", "share", "clic_description"):
        if k in V[0]: o[k] = sum(bool(v.get(k)) for v in V)
    o["comments"] = sum(bool(v.get("comment")) for v in V)
    o["notes"] = {k: round(st.mean(v[k] for v in V), 2) for k in ("valeur_percue", "originalite", "voix", "credibilite") if k in V[0]}
    seg = collections.defaultdict(list)
    for name, p in P.items(): seg[name[0]] += p
    o["profils"] = {s: {"duree_moy_s": round(avd(g)), "jusqu_au_bout": sum(v["watch_s"] >= D - 5 for v in g), "n": len(g)} for s, g in sorted(seg.items())}
    o["departs_par_30s"] = dict(sorted(collections.Counter(int(min(v["watch_s"], D) // 30 * 30) for v in V if v["watch_s"] < D - 5).items()))
    return o


if __name__ == "__main__":
    a = sys.argv[1:]; out = resume(charger(a[0]), int(a[1]))
    if "--avant" in a:
        i = a.index("--avant"); av = resume(charger(a[i + 1]), int(a[i + 2])); out["avant"] = {k: av[k] for k in ("n", "duree", "retention", "retention_pct_duree", "duree_moyenne_s", "duree_moyenne_pct", "notes")}
    json.dump(out, open(os.path.join(a[0], "agregat.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))
