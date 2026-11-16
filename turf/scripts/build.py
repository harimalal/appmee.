"""Construit les tables d'analyse a partir de la reponse open-pmu-api (Vincennes).
Usage : python3 -I build.py <fichier_json> <dossier_sortie>
"""
import json, re, sys, math, unicodedata
import pandas as pd
import numpy as np

src, out = sys.argv[1], sys.argv[2]
races = json.load(open(src))["message"]
races = sorted(races, key=lambda r: (r["date"], r["r/c"]))

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", " ", s).split()

def key_arrivee(name):          # "MONCLIN J.P." -> "monclin_j"
    t = norm(name)
    if not t: return None
    inits = [w for w in t if len(w) <= 2]
    words = [w for w in t if len(w) > 2]
    return f"{'_'.join(words)}_{inits[0][0] if inits else ''}"

def key_partant(name):          # "j.p. monclin" -> "monclin_j"
    t = norm(name)
    if not t: return None
    inits = [w for w in t if len(w) <= 2]
    words = [w for w in t if len(w) > 2]
    return f"{'_'.join(words)}_{inits[0][0] if inits else ''}"

def parse_conditions(d):
    d = d or ""
    ages = [int(a) for a in re.findall(r"(\d+)\s*(?:a|à|,|et)?\s*(?:\d+\s*)?ans", d)]
    nums = [int(x) for x in re.findall(r"\b(\d+)\b", d.split("ans")[0])] if "ans" in d else []
    age_min = min(nums) if nums else np.nan
    age_max = max(nums) if nums else np.nan
    cap = re.search(r"n'ayant pas gagn[ée] ([\d\.]+)", d)
    floor = re.search(r"ayant gagn[ée] au moins ([\d\.]+)", d)
    return dict(
        age_min=age_min, age_max=age_max,
        gain_cap=float(cap.group(1).replace(".", "")) if cap else np.nan,
        gain_floor=float(floor.group(1).replace(".", "")) if floor else np.nan,
        recul=int("recul" in d.lower()),
        femelles=int(bool(re.search(r"pouliches|juments", d.lower())) and "entiers" not in d.lower()),
        groupe=int(bool(re.search(r"groupe|gr\.", d.lower()))),
    )

# ---------- table course (100 courses) ----------
rows = []
for i, r in enumerate(races):
    win_num = str(r["arrivee"][0])
    w = r["arrivee_details"].get(win_num)
    c = parse_conditions(r["details"])
    rows.append(dict(
        race_id=i, date=r["date"], rc=r["r/c"], type=r["type"], partants=r["partants"],
        montant=r["montant"], distance=r["distance"], n_np=len(r["non_partants"]),
        full_field=int(bool(r.get("partants_details"))),
        win_cote_final=w["cotes"][-1] if w else np.nan,
        win_cote_first=w["cotes"][0] if w else np.nan,
        **c))
R = pd.DataFrame(rows)

# ---------- historique drivers / entraineurs (resultats publies, strictement anterieurs) ----------
hist = []
for r in races:
    for n, h in r["arrivee_details"].items():
        hist.append(dict(date=r["date"], drv=key_arrivee(h["nom_jockey"]),
                         trn=key_arrivee(h["nom_entraineur"]), win=int(h["position"] == 1),
                         top3=int(h["position"] <= 3)))
H = pd.DataFrame(hist)

def prior(col, k, date):
    s = H[(H[col] == k) & (H["date"] < date)]
    return s["win"].sum(), s["top3"].sum(), len(s)

# ---------- table partants (courses avec champ complet) ----------
def musique_feats(m):
    toks = [t for t in (m or "").split(".") if t]
    vals, disq = [], 0
    for t in toks[:5]:
        if t.isdigit():
            v = int(t); vals.append(10 if v == 0 else v)
        else:
            vals.append(10); disq += t in ("d", "a")
    if not vals: return np.nan, np.nan, np.nan, np.nan
    return np.mean(vals), sum(v == 1 for v in vals), sum(v <= 3 for v in vals), disq

prow = []
for i, r in enumerate(races):
    if not r.get("partants_details"): continue
    np_set = set(r["non_partants"]) - set(r["arrivee"])  # incoherence API : gagnant liste non-partant
    pos = {int(n): h["position"] for n, h in r["arrivee_details"].items()}
    fin = {int(n): h for n, h in r["arrivee_details"].items()}
    base = r["distance"]
    for p in r["partants_details"]:
        if p["numero"] in np_set: continue
        mm, nw, nt3, nd = musique_feats(p["musique"])
        drv, trn = key_partant(p["jockey"]), key_partant(p["entraineur"])
        dw, dt3, dn = prior("drv", drv, r["date"])
        tw, tt3, tn = prior("trn", trn, r["date"])
        f = fin.get(p["numero"])
        prow.append(dict(
            race_id=i, date=r["date"], numero=p["numero"], cheval=p["cheval"],
            win=int(pos.get(p["numero"]) == 1), top3=int(pos.get(p["numero"], 99) <= 3),
            position=pos.get(p["numero"], np.nan),
            cote_presse=p["cote_paris_turf"] or p["cote_tierce_magazine"],
            cote_pmu_final=f["cotes"][-1] if f else np.nan,
            age=p["age"], male=int(p["sexe"] in ("h", "m")), gains=p["gains"],
            recul=int((p["distance_m"] or base) > base), record=(p["reduction_km_s"] or np.nan),
            musique_moy=mm, musique_victoires=nw, musique_top3=nt3, musique_dq=nd,
            driver=drv, driver_entraineur=int(drv == trn),
            drv_prior_wins=dw, drv_prior_top3=dt3, drv_prior_n=dn,
            trn_prior_wins=tw, trn_prior_n=tn,
            partants=r["partants"], montant=r["montant"], distance=base))
P = pd.DataFrame(prow)

# probabilite implicite presse, normalisee dans la course (retire la marge)
P["p_impl"] = 1 / P["cote_presse"]
P["p_impl"] = P["p_impl"] / P.groupby("race_id")["p_impl"].transform("sum")
P["log_p_impl"] = np.log(P["p_impl"])
P["rang_cote"] = P.groupby("race_id")["cote_presse"].rank(method="first")
P["fav"] = (P["rang_cote"] == 1).astype(int)
# record : imputation par la mediane de la course + indicateur
P["record_na"] = P["record"].isna().astype(int)
P["record"] = P["record"].fillna(P.groupby("race_id")["record"].transform("median"))
# variables centrees par course (relatives au lot)
for c in ["record", "musique_moy", "gains", "age"]:
    P[c + "_rel"] = P[c] - P.groupby("race_id")[c].transform("mean")
P["log_gains_rel"] = np.log1p(P["gains"]) - P.groupby("race_id")["gains"].transform(lambda s: np.log1p(s).mean())

R.to_csv(f"{out}/courses.csv", index=False)
P.to_csv(f"{out}/partants.csv", index=False)
print("courses", len(R), "| courses champ complet", R.full_field.sum(), "| partants", len(P),
      "| gagnants", P.win.sum(), "| courses sans gagnant identifie", (P.groupby('race_id').win.sum() != 1).sum())
print(R[["partants", "montant", "distance", "recul", "femelles", "gain_cap", "age_min", "age_max", "win_cote_final"]].describe().round(1).to_string())
print(P[["cote_presse", "record", "musique_moy", "gains", "age", "drv_prior_wins", "recul", "record_na"]].describe().round(2).to_string())
