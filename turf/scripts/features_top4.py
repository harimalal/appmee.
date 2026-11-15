"""Ajoute aux partants les donnees d'entree supplementaires (consensus presse, classements, entourage, historique top 4).
Usage : python3 -I features_top4.py <json> <dossier_data>
"""
import json, sys, re, unicodedata
import numpy as np, pandas as pd

src, D = sys.argv[1], sys.argv[2]
races = sorted(json.load(open(src))["message"], key=lambda r: (r["date"], r["r/c"]))
P = pd.read_csv(f"{D}/partants.csv")
R = pd.read_csv(f"{D}/courses.csv")

def toks(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z ]", " ", s).split()
    words = [w for w in t if len(w) > 2]; inits = [w for w in t if len(w) <= 2]
    return f"{'_'.join(words)}_{inits[0][0] if inits else ''}" if t else None

# historique top 4 drivers / entraineurs (strictement anterieur a la date de la course)
hist = []
for r in races:
    for n, h in r["arrivee_details"].items():
        hist.append((r["date"], toks(h["nom_jockey"]), toks(h["nom_entraineur"]), int(h["position"] <= 4)))
H = pd.DataFrame(hist, columns=["date", "drv", "trn", "top4"])

new = []
for i, r in enumerate(races):
    if not r.get("partants_details"): continue
    pron = r.get("pronostics_presse") or {}
    cl = r.get("classements") or {}
    ap = r.get("aptitudes") or {}
    forme_ent = set(toks(x) for x in (r.get("entraineurs_en_forme") or []) + (r.get("jockeys_en_forme") or []))
    nj = max(len(pron), 1)
    for p in r["partants_details"]:
        n = p["numero"]
        ranks = [lst.index(n) + 1 if n in lst else 10 for lst in pron.values()]
        fav = cl.get("favoris", [])
        drv, trn = toks(p["jockey"]), toks(p["entraineur"])
        hd = H[(H.drv == drv) & (H.date < r["date"])]
        ht = H[(H.trn == trn) & (H.date < r["date"])]
        mus = [t for t in (p["musique"] or "").split(".") if t]
        last = (10 if mus[0] in ("0", "d", "a") else int(mus[0])) if mus and (mus[0].isdigit() or mus[0] in "da") else np.nan
        top4_mus = sum(1 for t in mus[:5] if t.isdigit() and 1 <= int(t) <= 4)
        new.append(dict(
            race_id=i, numero=n,
            cote_tm=p["cote_tierce_magazine"],
            presse_part_cite=sum(x < 10 for x in ranks) / nj,
            presse_part_1er=sum(x == 1 for x in ranks) / nj,
            presse_rang_moy=np.mean(ranks) if ranks else np.nan,
            cl_favoris_score=(8 - (fav.index(n) + 1)) if n in fav else 0,
            cl_forme=int(n in cl.get("forme", [])), cl_classe=int(n in cl.get("classe", [])),
            cl_progres=int(n in cl.get("progres", [])), cl_regularite=int(n in cl.get("regularite", [])),
            apt_outsider=int(any(x["numero"] == n for x in ap.get("outsiders", []))),
            apt_gros_outsider=int(any(x["numero"] == n for x in ap.get("gros_outsiders", []))),
            apt_seconde_chance=int(any(x["numero"] == n for x in ap.get("secondes_chances", []))),
            entourage_en_forme=int(drv in forme_ent or trn in forme_ent),
            drv_prior_top4=int(hd.top4.sum()), trn_prior_top4=int(ht.top4.sum()),
            musique_derniere=last, musique_top4=top4_mus,
            femelles_course=int(R.loc[R.race_id == i, "femelles"].iloc[0]),
            age_max_course=R.loc[R.race_id == i, "age_max"].iloc[0]))
N = pd.DataFrame(new)
P = P.drop(columns=[c for c in N.columns if c in P.columns and c not in ("race_id", "numero")]).merge(N, on=["race_id", "numero"], how="left")
P["top4"] = (P["position"] <= 4).astype(int)
pt = 1 / P["cote_tm"]; pt = pt / pt.groupby(P.race_id).transform("sum")
P["desaccord_presse"] = P["log_p_impl"] - np.log(pt)        # >0 : Paris-Turf plus optimiste que Tierce Magazine
P.to_csv(f"{D}/partants_top4.csv", index=False)
print(len(P), "partants |", P.top4.sum(), "top 4 |", P.groupby("race_id").top4.sum().value_counts().to_dict())
print(P[["presse_part_cite", "presse_rang_moy", "cl_favoris_score", "apt_outsider", "entourage_en_forme",
         "drv_prior_top4", "musique_derniere", "musique_top4", "desaccord_presse"]].describe().round(2).to_string())
