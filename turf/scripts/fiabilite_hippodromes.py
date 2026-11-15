"""Fiabilite de chaque hippodrome (attele) : places trouvees par les 3 premieres cotes, favori gagnant / place, disqualifies, rapport gagnant median.
Usage : python3 -I fiabilite_hippodromes.py <dossier_courses>   (lit data/historique_courses.jsonl produit par collecte_historique.py)
Verdict : FIABLE si l'intervalle a 95 % est au-dessus de la moyenne generale, ALEATOIRE s'il est en dessous. Minimum 12 courses par piste."""
import sys, json, numpy as np, pandas as pd
D = sys.argv[1]; R = []
for l in open(f"{D}/data/historique_courses.jsonl"):
    r = json.loads(l)
    if r["disc"] != "ATTELE" or not r.get("cotes") or not r.get("arr"): continue
    c = {int(k): v for k, v in r["cotes"].items() if v and v > 0}
    if len(c) < 6: continue
    low = sorted(c, key=c.get); arr = [int(a) for a in r["arr"][:3]]
    sg = {a: b / 100 for a, b in r["rap"].get("SIMPLE_GAGNANT", []) if str(a).isdigit()} if r.get("rap") else {}
    R.append(dict(hip=r["hip"], n=len(c), fav_win=int(low[0] == arr[0]), fav_top3=int(low[0] in arr), hit3=sum(x in arr for x in low[:3]), dq=r.get("dq") or 0, gag=(list(sg.values())[0] if sg else np.nan)))
d = pd.DataFrame(R)
g = d.groupby("hip").agg(courses=("n", "size"), partants=("n", "mean"), fav_gagne=("fav_win", "mean"), fav_places=("fav_top3", "mean"), places_3cotes=("hit3", "mean"), dq=("dq", "mean"), rap_gagnant=("gag", "median")).reset_index()
g = g[g.courses >= 12].sort_values("places_3cotes", ascending=False)
mu, sd = d.hit3.mean(), d.hit3.std(); g["se"] = sd / np.sqrt(g.courses)
g["verdict"] = g.apply(lambda r: "FIABLE" if r.places_3cotes - 1.96 * r.se > mu else ("ALEATOIRE" if r.places_3cotes + 1.96 * r.se < mu else "dans la moyenne"), axis=1)
pd.set_option("display.width", 200)
print(f"{len(d)} courses, {d.hip.nunique()} hippodromes ; moyenne generale {mu:.2f} places sur 3 ; favori gagne {d.fav_win.mean():.0%}, place {d.fav_top3.mean():.0%}")
print(g.round(2).drop(columns=["se"]).to_string(index=False))
