"""Signaux d'historique complet (letrot.com, usage prive) : appetence Vincennes, vitesse a Vincennes, distance, driver a Vincennes, affinite cheval-driver, fautes.
Toutes les variables n'utilisent que des courses ANTERIEURES a la date de la course. Evaluation : validation croisee par course.
Usage : python3 -I historique_chevaux.py <dossier_data>
"""
import sys, os, json, re, warnings, itertools
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import log_loss, roc_auc_score
warnings.filterwarnings("ignore")
D = sys.argv[1]; out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(out[-1])
H = pd.read_csv(f"{D}/partants_ids.csv")
have = {f[:-5] for f in os.listdir(f"{D}/perfs") if f.endswith(".json")}
H = H[H.horse_id.isin(have)]
# courses completes seulement (tous les partants ont leur historique)
full = pd.read_csv(f"{D}/partants_ids.csv").groupby("race").horse_id.apply(lambda s: set(s) <= have)
H = H[H.race.isin(full[full].index)]
def rk(v):
    v = str(v or "").strip()
    if v.isdigit(): return int(v)
    return -1 if v[:1] in "DTAR" else 99
def red(v):
    try: x = int(v); return (x // 1000 * 60 + (x % 1000) // 10 + (x % 10) / 10) if x > 0 else np.nan
    except Exception: return np.nan
P = []
for h in {*H.horse_id}:
    for x in json.load(open(f"{D}/perfs/{h}.json")):
        if x.get("speciality") != "A": continue
        P.append(dict(horse=x["id"], date=x["datePerf"][:10], hip=str(x.get("numHippodrome")), dist=x.get("distance") or 0, rang=rk(x.get("rang")), red=red(x.get("reduction")),
                      driver=x.get("driverId"), n=x.get("nbPartant") or 0, ferrure=x.get("ferrure"), cote=x.get("rapportProbable")))
P = pd.DataFrame(P); P["top3"] = ((P.rang >= 1) & (P.rang <= 3)).astype(int); P["dq"] = (P.rang == -1).astype(int)
say(f"# {H.race.nunique()} courses completes ({len(H)} partants, {H.horse_id.nunique()} chevaux), {len(P)} courses passees d'attele en historique")
# pool pour le driver : courses a Vincennes de tous les chevaux recuperes (une ligne par cheval et par course)
V = P[P.hip == "7500"].dropna(subset=["driver"])
def shrink(t, n, prior=0.25, k=6): return (t + prior * k) / (n + k)
rows = []
dpool = V.sort_values("date")
for r in H.itertuples():
    h = P[(P.horse == r.horse_id) & (P.date < r.date)].sort_values("date", ascending=False)
    cur_dist = None
    all_n, all_t = len(h), h.top3.sum(); v = h[h.hip == "7500"]
    dv = dpool[(dpool.driver == r.driver_id) & (dpool.date < r.date)]
    ha = h[h.driver == r.driver_id] if r.driver_id else h.iloc[0:0]
    rows.append(dict(race=r.race, numero=r.numero, h_n=all_n, h_rate=shrink(all_t, all_n), h_rate8=shrink(h.head(8).top3.sum(), min(8, all_n)),
                     v_n=len(v), v_rate=shrink(v.top3.sum(), len(v)), v_win=shrink((v.rang == 1).sum(), len(v), 0.08), v_rel=shrink(v.top3.sum(), len(v)) - shrink(all_t, all_n),
                     v_speed=v.head(5).red.min() if len(v) else np.nan, v_speed_mean=v.head(5).red.mean() if len(v) else np.nan,
                     drv_n=len(dv), drv_rate=shrink(dv.top3.sum(), len(dv), 0.25, 15), aff_n=len(ha), aff_rate=shrink(ha.top3.sum(), len(ha), 0.25, 4),
                     dq10=h.head(10).dq.sum(), jours=(pd.Timestamp(r.date) - pd.Timestamp(h.date.iloc[0])).days if len(h) else 365))
F = pd.DataFrame(rows)
# dist : course du jour -> distance de la course
base = pd.concat([pd.read_csv(f"{D}/feat_origine.csv"), pd.read_csv(f"{D}/feat_novembre.csv")]); base = base[(base.discipline == "A") & (base.cote > 0)]
M = base.merge(F, on=["race", "numero"], how="inner").merge(H[["race", "numero", "ech"]], on=["race", "numero"], how="left")
M = M[M.groupby("race").cote.transform("size") >= 6].reset_index(drop=True)
q = 1 / M.cote; M["p"] = q / q.groupby(M.race).transform("sum"); M["lp"] = np.log(M.p); M["pos"] = M.pos.where(M.pos > 0); M["y"] = (M.pos <= 3).astype(int)
def rel(s): return s - s.groupby(M.race).transform("mean")
M["v_speed_rel"] = rel((-M.v_speed).fillna(-M.groupby("race").v_speed.transform("mean")).fillna(0)); M["v_speed_mean_rel"] = rel((-M.v_speed_mean).fillna(-M.groupby("race").v_speed_mean.transform("mean")).fillna(0))
for c in ["h_rate", "h_rate8", "v_rate", "v_win", "v_rel", "drv_rate", "aff_rate", "dq10"]: M[c + "_rel"] = rel(M[c])
M["jours_log"] = rel(np.log1p(M.jours)); M["rang_cote"] = M.groupby("race").cote.rank(method="first")
M["f_classe"] = rel(-np.log(M.crack.where(M.crack > 0, M.crack.max() + 1))); M["f_avis"] = (M.avis == 1).astype(float)
NEW = ["v_rate_rel", "v_rel_rel", "v_win_rel", "v_speed_rel", "drv_rate_rel", "aff_rate_rel", "dq10_rel", "h_rate8_rel", "jours_log"]
LAB = {"v_rate_rel": "appetence Vincennes (taux de places a Vincennes)", "v_rel_rel": "mieux a Vincennes qu'ailleurs", "v_win_rel": "victoires a Vincennes",
       "v_speed_rel": "meilleur temps km a Vincennes (5 dernieres)", "drv_rate_rel": "driver : taux de places a Vincennes", "aff_rate_rel": "affinite cheval-driver",
       "dq10_rel": "fautes (10 dernieres)", "h_rate8_rel": "forme (taux de places, 8 dernieres)", "jours_log": "jours depuis la derniere course (log)"}
say(f"Analyse sur {M.race.nunique()} courses, {len(M)} partants, {int(M.y.sum())} places")
# --- effet de chaque signal au-dela de la cote (logit avec la cote recalibree)
X0 = sm.add_constant(M[["lp"]]); m0 = sm.GLM(M.y, X0, family=sm.families.Binomial()).fit(); M["pe"] = m0.predict(X0)
rows = []
for c in NEW:
    x = (M[c] - M[c].mean()) / M[c].std(); m = sm.GLM(M.y, sm.add_constant(pd.concat([M.lp, x.rename("x")], axis=1)), family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(M.race)[0]})
    rows.append(dict(signal=LAB[c], odds_ratio=np.exp(m.params["x"]), ic_bas=np.exp(m.conf_int().loc["x", 0]), ic_haut=np.exp(m.conf_int().loc["x", 1]), p=m.pvalues["x"]))
T = pd.DataFrame(rows); T["p_holm"] = multipletests(T.p, method="holm")[1]
say("\n# SIGNAL PAR SIGNAL, AU-DELA DE LA COTE (odds ratio par ecart-type pour etre dans les 3)"); say(T.round(3).to_string(index=False))
# --- modeles en validation croisee
def models():
    return {"1 cote seule": (["lp"], lambda: LogisticRegression(C=100, max_iter=500)),
            "2 cote + historique complet": (["lp"] + NEW, lambda: LogisticRegression(C=0.3, max_iter=500)),
            "3 cote + historique + classe + avis": (["lp"] + NEW + ["f_classe", "f_avis"], lambda: LogisticRegression(C=0.3, max_iter=500)),
            "4 arbres (historique + classe + avis)": (["lp"] + NEW + ["f_classe", "f_avis"], lambda: HistGradientBoostingClassifier(max_depth=2, learning_rate=0.05, max_iter=120, min_samples_leaf=25, l2_regularization=5.0, random_state=0))}
races = M.race.unique(); PRD = {k: np.zeros(len(M)) for k in models()}; REP = 3
for rep in range(REP):
    perm = np.random.default_rng(rep).permutation(races); fold = {r: i % 10 for i, r in enumerate(perm)}; f = M.race.map(fold).values
    for k, (cols, mk) in models().items():
        for i in range(10):
            tr, te = f != i, f == i; Xtr = M.loc[tr, cols].values; mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
            PRD[k][te] += mk().fit((Xtr - mu) / sd, M.y[tr]).predict_proba((M.loc[te, cols].values - mu) / sd)[:, 1] / REP
for k in PRD: M["P " + k] = PRD[k]
def prec3(df, col): return np.array([g.sort_values(col, ascending=False).head(3).y.sum() for _, g in df.groupby("race")])
def auc_race(df, col): return np.mean([roc_auc_score(g.y, g[col]) for _, g in df.groupby("race") if 0 < g.y.sum() < len(g)])
Ro = M[M.ech == "origine"].drop_duplicates("race"); M["ent"] = M.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s))); M["pfav"] = M.groupby("race").p.transform("max")
sc = lambda d: (d.pfav - M.pfav.mean()) / M.pfav.std() - (d.ent - M.ent.mean()) / M.ent.std(); M["lis"] = sc(M); seuil = M.drop_duplicates("race").lis.quantile(1 / 3)
M["petit"] = M.partants <= 14; M["jf"] = M.groupby("race").sexe.transform(lambda s: (s == "F").all()) | (M.groupby("race").age.transform("max") <= 6)
M["gardee"] = (M.lis > seuil) & ~((~M.petit) & M.jf)
def rapport(df, titre):
    say(f"\n## {titre} ({df.race.nunique()} courses, {len(df)} partants)")
    base = prec3(df, "P 1 cote seule")
    say(f"{'modele':40s} {'log-loss':>9s} {'AUC/course':>10s} {'places sur 3 choisis':>21s} {'ecart vs cote':>16s}")
    for k in models():
        c = "P " + k; pr = prec3(df, c); d = pr - base; pv = stats.wilcoxon(d[d != 0]).pvalue if (d != 0).any() else 1.0
        say(f"{k:40s} {log_loss(df.y, df[c].clip(1e-4, 1-1e-4)):9.4f} {auc_race(df, c):10.3f} {pr.mean():14.2f} {'':>6s} {d.mean():+6.2f} (p={pv:.2f})")
rapport(M, "TOUTES LES COURSES"); rapport(M[M.gardee], "COURSES GARDEES"); rapport(M[M.ech == "novembre"], "NOVEMBRE"); rapport(M[M.ech == "origine"], "ORIGINE")
M.to_csv(f"{D}/historique_features.csv", index=False)
open(f"{D}/rapport_historique_chevaux.txt", "w").write("\n".join(out))
