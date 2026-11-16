"""Approche 3 (suite) : paris 'simple place' simules (cheval dans les 3 premiers, courses de 12 partants et plus).
Rapports places : bareme fourni par Hari selon la cote PMU du cheval place (hypotheses basse / moyenne / haute).
Decision avant course : proba de top 3 (hors echantillon) x rapport place estime d'apres la cote presse >= seuil.
Usage : python3 -I value_place.py <dossier_data>
"""
import sys, warnings
import numpy as np, pandas as pd
from itertools import permutations
from scipy.optimize import minimize_scalar
from sklearn.ensemble import RandomForestClassifier
warnings.filterwarnings("ignore")
D = sys.argv[1]
P = pd.read_csv(f"{D}/partants_top4.csv").reset_index(drop=True)
rng = np.random.default_rng(5)
P["top3"] = (P.position <= 3).astype(int)

# ---------------- bareme des rapports places (pour 1 euro), d'apres Hari
# favori / cote < 5 : 1,5-2 ; 5-10 : 1,8-2,5 ; 10-15 : 2,5-3,5 ; 20 : 3,5-5
# trou 15-20 : interpole (3,0-4,25) ; au-dela de 20 : bareme '20' (prudent, sous-estime sans doute les tres gros outsiders)
BAREME = [(5, (1.5, 2.0)), (10, (1.8, 2.5)), (15, (2.5, 3.5)), (20, (3.0, 4.25)), (np.inf, (3.5, 5.0))]
def rapport(cote, scen):
    for lim, (lo, hi) in BAREME:
        if cote < lim:
            return {"bas": lo, "moyen": (lo + hi) / 2, "haut": hi}[scen]
    return np.nan

# ---------------- variables (memes que l'analyse arbres)
P["log_drv_top4"] = np.log1p(P["drv_prior_top4"]); P["log_trn_top4"] = np.log1p(P["trn_prior_top4"])
P["log_montant"] = np.log(P["montant"])
for c in ["record_rel", "musique_moy_rel", "log_gains_rel", "age_rel"]: P[c] = P[c].fillna(0)
for c in ["musique_derniere", "presse_rang_moy"]: P[c] = P[c].fillna(P[c].median())
ALL = ["log_p_impl", "rang_cote", "desaccord_presse", "presse_part_cite", "presse_part_1er", "presse_rang_moy", "cl_favoris_score",
       "cl_forme", "cl_classe", "cl_progres", "cl_regularite", "apt_outsider", "apt_gros_outsider", "apt_seconde_chance",
       "record_rel", "musique_moy_rel", "musique_derniere", "musique_top4", "musique_victoires", "musique_dq", "log_gains_rel",
       "age_rel", "male", "recul", "numero", "log_drv_top4", "log_trn_top4", "driver_entraineur", "entourage_en_forme",
       "partants", "log_montant", "distance", "femelles_course", "age_max_course"]
races = P.drop_duplicates("race_id").sort_values(["date", "race_id"]).race_id.tolist()

def harville_top3(p):
    n = len(p); out = np.zeros(n)
    for i in range(n):
        s = p[i]
        for j in range(n):
            if j == i: continue
            s += p[j] * p[i] / (1 - p[j])
            for k in range(n):
                if k in (i, j): continue
                s += p[j] * p[k] / (1 - p[j]) * p[i] / (1 - p[j] - p[k])
        out[i] = s
    return out

# ---------------- probabilites de top 3 hors echantillon
# A : cote presse recalibree (exposant ajuste sur l'ordre des 3 premiers, Plackett-Luce) + Harville
def fit_beta(df):
    def nll(b):
        s = 0
        for _, g in df.groupby("race_id"):
            u = b * g.log_p_impl.values; pos = g.position.values; alive = np.ones(len(u), bool)
            for k in (1, 2, 3):
                w = np.where(pos == k)[0][0]; m = u[alive].max()
                s -= u[w] - (m + np.log(np.exp(u[alive] - m).sum())); alive[w] = False
        return s
    return minimize_scalar(nll, bounds=(0.1, 4), method="bounded").x
pA = pd.Series(np.nan, index=P.index); betas = []
for r in races:
    b = fit_beta(P[P.race_id != r]); betas.append(b)
    g = P[P.race_id == r]; u = np.exp(b * g.log_p_impl.values); u /= u.sum()
    pA[g.index] = harville_top3(u)
pRaw = pd.Series(np.nan, index=P.index)  # cote presse brute + Harville (sans aucune estimation)
for r in races:
    g = P[P.race_id == r]; pRaw[g.index] = harville_top3(g.p_impl.values)
# B : foret aleatoire top 3, normalisee pour que la somme = 3 par course
pB = pd.Series(np.nan, index=P.index)
for r in races:
    tr, te = P.race_id != r, P.race_id == r
    m = RandomForestClassifier(n_estimators=300, min_samples_leaf=10, max_features="sqrt", random_state=0, n_jobs=2).fit(P.loc[tr, ALL], P.loc[tr, "top3"])
    pB[te] = m.predict_proba(P.loc[te, ALL])[:, 1]
pB = 3 * pB / pB.groupby(P.race_id).transform("sum")
pC = (pA + pB) / 2

rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))
say("# PARIS 'SIMPLE PLACE' SIMULES (1 euro, cheval dans les 3 premiers)")
say("Rapports places : bareme de Hari selon la cote PMU du cheval place. Scenarios bas / moyen / haut = bornes et milieu des fourchettes.")
say(f"Exposant de recalibrage de la cote (ordre des 3 premiers) : {np.mean(betas):.2f} (1 = cote presse prise telle quelle)")

# calibration : la cote presse prevoit-elle bien le top 3 ?
say("\n# CALIBRATION top 3 par tranche de cote presse")
P["tranche"] = pd.cut(P.cote_presse, [0, 5, 10, 15, 20, 40, 1000], labels=["<5", "5-10", "10-15", "15-20", "20-40", ">40"])
cal = P.groupby("tranche").agg(partants=("top3", "size"), places=("top3", "sum"), taux_place=("top3", "mean"),
                                proba_cote_brute=("top3", lambda s: pRaw[s.index].mean()), proba_modele_A=("top3", lambda s: pA[s.index].mean()))
for scen in ["bas", "moyen", "haut"]:
    ret = P.top3 * P.cote_pmu_final.map(lambda c: rapport(c, scen) if pd.notna(c) else 0)
    cal[f"rendement_{scen}"] = ret.groupby(P.tranche).sum() / cal.partants - 1
say(cal.round(3).to_string(formatters={c: (lambda x: f"{x:+.0%}") for c in cal.columns if c.startswith("rendement")}))
say("rendement_x = gain moyen par euro si on joue PLACE tous les chevaux de la tranche (0 % = on recupere sa mise).")

# strategies
def run(mask, scen):
    mask = pd.Series(mask, index=P.index).fillna(False).astype(bool)
    ret = (mask & (P.top3 == 1)) * P.cote_pmu_final.map(lambda c: rapport(c, scen) if pd.notna(c) else 0)
    per = pd.DataFrame(dict(bet=mask.astype(int), ret=ret)).groupby(P.race_id).sum()
    n = per.bet.sum()
    if n == 0: return n, 0, np.nan, ""
    bs = []
    for _ in range(2000):
        s = per.iloc[rng.integers(0, len(per), len(per))]
        bs.append(s.ret.sum() / s.bet.sum() - 1 if s.bet.sum() else np.nan)
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return int(n), int((mask & (P.top3 == 1)).sum()), per.ret.sum() / n - 1, f"{lo:+.0%} / {hi:+.0%}"
est = P.cote_presse.map(lambda c: rapport(c, "moyen"))  # rapport place estime AVANT course (cote presse, scenario moyen)
strat = {"Tous les partants": np.ones(len(P), bool), "Favori presse": P.rang_cote == 1, "2e de la cote presse": P.rang_cote == 2,
         "3 premiers de la cote presse": P.rang_cote <= 3, "Cotes presse 5-10": P.cote_presse.between(5, 10, inclusive="left"),
         "Cotes presse 10-20": P.cote_presse.between(10, 20, inclusive="left"), "Cotes presse >= 20": P.cote_presse >= 20}
for nm, pm in [("A cote recalibree", pA), ("B foret aleatoire", pB), ("C moyenne A+B", pC)]:
    for k in [1.0, 1.1, 1.25]:
        strat[f"{nm} : esperance >= {k}"] = (pm * est >= k).values
    strat[f"{nm} : meilleur cheval du modele"] = (pm == pm.groupby(P.race_id).transform("max")).values
rows = []
for nm, m in strat.items():
    r = {"strategie": nm}
    for scen in ["bas", "moyen", "haut"]:
        n, w, roi, ic = run(m, scen)
        r.update({"paris": n, "places": w, f"ROI_{scen}": roi})
        if scen == "moyen": r["IC95_moyen"] = ic
    rows.append(r)
V = pd.DataFrame(rows)[["strategie", "paris", "places", "ROI_bas", "ROI_moyen", "ROI_haut", "IC95_moyen"]]
say("\n# STRATEGIES (40 courses, hors echantillon)")
say(V.to_string(index=False, formatters={c: (lambda x: f"{x:+.0%}" if pd.notna(x) else "") for c in ["ROI_bas", "ROI_moyen", "ROI_haut"]}))
say(f"\n{len(strat)} strategies testees : le meilleur resultat est optimiste par construction (risque de coup de chance).")
open(f"{D}/rapport_place.txt", "w").write("\n".join(rep)); V.to_csv(f"{D}/strategies_place.csv", index=False)
print("\n".join(rep))
