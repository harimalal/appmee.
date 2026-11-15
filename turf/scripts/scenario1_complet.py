"""SCENARIO 1 : repérer les chevaux les plus susceptibles d'etre dans les 3 premiers, en integrant TOUS les signaux (avant course uniquement).
Groupes de signaux : COTE | CLASSE (Crack, gains, changement de classe) | FORME | HIPPODROME (appetence Vincennes, distance, temps) | JOCKEY (driver Vincennes, affinite, changement) | MARCHE (avis, surperformance vs cote) | PHYSIQUE.
Sortie : (1) valeur de chaque groupe au-dela de la cote, (2) ORDRE DE PRIORITE, (3) modele complet en validation croisee par course, (4) classement des chevaux course par course.
Usage : python3 -I scenario1_complet.py <dossier_data>
"""
import sys, os, json, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
warnings.filterwarnings("ignore")
D = sys.argv[1]; out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(out[-1])
H = pd.read_csv(f"{D}/partants_ids.csv"); have = {f[:-5] for f in os.listdir(f"{D}/perfs") if f.endswith(".json")}
full = H.groupby("race").horse_id.apply(lambda s: set(s) <= have); H = H[H.race.isin(full[full].index)]
def rk(v):
    v = str(v or "").strip()
    return int(v) if v.isdigit() else (-1 if v[:1] in "DTAR" else 99)
def red(v):
    try: x = int(v); return (x // 1000 * 60 + (x % 1000) // 10 + (x % 10) / 10) if x > 0 else np.nan
    except Exception: return np.nan
P = []
for h in {*H.horse_id}:
    for x in json.load(open(f"{D}/perfs/{h}.json")):
        if x.get("speciality") != "A": continue
        r = rk(x.get("rang")); n = x.get("nbPartant") or 12
        s = 0.0 if r == -1 else (0.1 if r in (0, 99) else float(np.clip(1 - (r - 1) / max(n - 1, 1), 0, 1)))
        P.append(dict(horse=x["id"], date=x["datePerf"][:10], hip=str(x.get("numHippodrome")), dist=x.get("distance") or 0, rang=r, s=s, red=red(x.get("reduction")), driver=x.get("driverId"),
                      cote=x.get("rapportProbable"), alloc=x.get("allocation") or 0, top3=int(1 <= r <= 3), dq=int(r == -1)))
P = pd.DataFrame(P).sort_values("date")
# surperformance vs cote : residu moyen (a-t-il souvent place alors que la cote disait non ?)
cp = P[(P.cote > 0) & (P.rang >= 0) & (P.rang < 99)].copy(); cp["l"] = np.log(1 / cp.cote)
mm = sm.GLM(cp.top3, sm.add_constant(cp[["l"]]), family=sm.families.Binomial()).fit()
P["resid"] = np.nan; ok = (P.cote > 0)
P.loc[ok, "resid"] = P.top3[ok] - mm.predict(sm.add_constant(pd.DataFrame({"l": np.log(1 / P.cote[ok])}), has_constant="add"))
V = P[(P.hip == "7500") & P.driver.notna()]
def shrink(t, n, prior=0.25, k=6): return (t + prior * k) / (n + k)
base = pd.concat([pd.read_csv(f"{D}/feat_origine.csv"), pd.read_csv(f"{D}/feat_novembre.csv")]); base = base[(base.discipline == "A") & (base.cote > 0)]
rows = []
for r in H.merge(base[["race", "numero", "distance", "allocation"]], on=["race", "numero"]).itertuples():
    h = P[(P.horse == r.horse_id) & (P.date < r.date)].sort_values("date", ascending=False); v = h[h.hip == "7500"]
    dv = V[(V.driver == r.driver_id) & (V.date < r.date)]; ha = h[h.driver == r.driver_id]; near = h[(h.dist - (r.distance or 0)).abs() <= 250]
    w = np.array([6, 5, 4, 3, 2, 1.0])[:min(6, len(h))]
    rows.append(dict(race=r.race, numero=r.numero, h_n=len(h), s6=(np.dot(h.head(6).s.values, w) + 0.8) / (w.sum() + 2) if len(h) else 0.4,
                     trend=(h.head(3).s.mean() - h.iloc[3:6].s.mean()) if len(h) >= 5 else 0.0, h_rate8=shrink(h.head(8).top3.sum(), min(8, len(h))),
                     v_n=len(v), v_rate=shrink(v.top3.sum(), len(v)), v_win=shrink((v.rang == 1).sum(), len(v), 0.08), v_rel=shrink(v.top3.sum(), len(v)) - shrink(h.top3.sum(), len(h)),
                     v_speed=v.head(5).red.min() if len(v) else np.nan, dist_rate=shrink(near.top3.sum(), len(near), 0.25, 4),
                     drv_rate=shrink(dv.top3.sum(), len(dv), 0.25, 15), aff_rate=shrink(ha.top3.sum(), len(ha), 0.25, 4), drv_chg=int(len(h) > 0 and h.driver.iloc[0] != r.driver_id),
                     surp10=h.head(10).resid.mean() if h.head(10).resid.notna().any() else 0.0, dq10=h.head(10).dq.sum(),
                     alloc_chg=(np.log1p(r.allocation or 0) - np.log1p(h.head(5).alloc.mean())) if len(h) else 0.0, jours=(pd.Timestamp(r.date) - pd.Timestamp(h.date.iloc[0])).days if len(h) else 365))
F = pd.DataFrame(rows)
M = base.merge(F, on=["race", "numero"], how="inner").merge(H[["race", "numero", "ech"]], on=["race", "numero"], how="left")
M = M[M.groupby("race").cote.transform("size") >= 6].reset_index(drop=True)
q = 1 / M.cote; M["p"] = q / q.groupby(M.race).transform("sum"); M["lp"] = np.log(M.p); M["pos"] = M.pos.where(M.pos > 0); M["y"] = (M.pos <= 3).astype(int)
M["rang_cote"] = M.groupby("race").cote.rank(method="first")
def rel(s): return s - s.groupby(M.race).transform("mean")
M["f_classe"] = rel(-np.log(M.crack.where(M.crack > 0, M.crack.max() + 1))); M["f_gm"] = rel(np.log1p(M.gains_moy)); M["f_alloc"] = M.alloc_chg
M["f_s6"] = rel(M.s6); M["f_trend"] = M.trend; M["f_h8"] = rel(M.h_rate8); M["f_jours"] = rel(np.log1p(M.jours)); M["f_dq"] = rel(M.dq10.astype(float))
M["f_vrate"] = rel(M.v_rate); M["f_vrel"] = rel(M.v_rel); M["f_vwin"] = rel(M.v_win); M["f_dist"] = rel(M.dist_rate)
M["f_vspeed"] = rel((-M.v_speed).fillna(-M.groupby("race").v_speed.transform("mean")).fillna(0))
M["f_drv"] = rel(M.drv_rate); M["f_aff"] = rel(M.aff_rate); M["f_drvchg"] = M.drv_chg.astype(float)
M["f_avis"] = (M.avis == 1).astype(float); M["f_surp"] = rel(M.surp10)
M["f_age"] = rel(M.age.astype(float)); M["f_fem"] = (M.sexe == "F").astype(float); M["f_d4"] = (M.ferrure == "D4").astype(float)
GROUPES = {"CLASSE (Crack, gains, changement de classe)": ["f_classe", "f_gm", "f_alloc"],
           "FORME (valeur recente, tendance, repos, fautes)": ["f_s6", "f_trend", "f_h8", "f_jours", "f_dq"],
           "HIPPODROME (appetence Vincennes, distance, temps)": ["f_vrate", "f_vrel", "f_vwin", "f_dist", "f_vspeed"],
           "JOCKEY (driver Vincennes, affinite, changement)": ["f_drv", "f_aff", "f_drvchg"],
           "MARCHE (avis entraineur, surperformance vs cote)": ["f_avis", "f_surp"],
           "PHYSIQUE (age, sexe, deferre)": ["f_age", "f_fem", "f_d4"]}
ALL = sum(GROUPES.values(), [])
say(f"# SCENARIO 1 - {M.race.nunique()} courses d'attele de Vincennes, {len(M)} partants, {int(M.y.sum())} places ; {len(ALL)} signaux, tous calcules AVANT la course")
# lisibilite / gardees
M["ent"] = M.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s))); M["pfav"] = M.groupby("race").p.transform("max")
Ro = M[M.ech == "origine"].drop_duplicates("race"); zf, ze = (Ro.pfav.mean(), Ro.pfav.std()), (Ro.ent.mean(), Ro.ent.std())
M["lis"] = (M.pfav - zf[0]) / zf[1] - (M.ent - ze[0]) / ze[1]; seuil = Ro.assign(lis=(Ro.pfav - zf[0]) / zf[1] - (Ro.ent - ze[0]) / ze[1]).lis.quantile(1 / 3)
M["petit"] = M.partants <= 14; M["jf"] = M.groupby("race").sexe.transform(lambda s: (s == "F").all()) | (M.groupby("race").age.transform("max") <= 6)
M["gardee"] = (M.lis > seuil) & ~((~M.petit) & M.jf)
# --- CV
def cv(cols, model="logit", reps=3, C=0.3):
    pr = np.zeros(len(M)); races = M.race.unique()
    for rep in range(reps):
        perm = np.random.default_rng(rep).permutation(races); fold = {r: i % 10 for i, r in enumerate(perm)}; f = M.race.map(fold).values
        for i in range(10):
            tr, te = f != i, f == i; Xtr = M.loc[tr, cols].values; mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
            m = LogisticRegression(C=C, max_iter=500) if model == "logit" else HistGradientBoostingClassifier(max_depth=2, learning_rate=0.05, max_iter=120, min_samples_leaf=25, l2_regularization=5.0, random_state=0)
            pr[te] += m.fit((Xtr - mu) / sd, M.y[tr]).predict_proba((M.loc[te, cols].values - mu) / sd)[:, 1] / reps
    return pr
def prec3(pr, mask=None):
    d = M.assign(pr=pr); d = d if mask is None else d[mask]
    return np.array([g.sort_values("pr", ascending=False).head(3).y.sum() for _, g in d.groupby("race")])
def ll_race(pr): d = M.assign(l=-(M.y * np.log(np.clip(pr, 1e-4, 1)) + (1 - M.y) * np.log(np.clip(1 - pr, 1e-4, 1)))); return d.groupby("race").l.mean().values
base_pr = cv(["lp"], C=100); base_ll = ll_race(base_pr); base_p3 = prec3(base_pr)
say(f"Repere : cote seule = {base_p3.mean():.2f} places sur 3 choisis ; hasard = {np.mean([3 * 3 / len(g) for _, g in M.groupby('race')]):.2f} ; log-loss {base_ll.mean():.4f}")
say("\n# 1. VALEUR DE CHAQUE GROUPE DE SIGNAUX, AJOUTE A LA COTE (validation croisee ; log-loss plus bas = mieux)")
res = []
for g, cols in GROUPES.items():
    pr = cv(["lp"] + cols); dl = base_ll - ll_race(pr); d3 = prec3(pr) - base_p3
    res.append(dict(groupe=g, gain_logloss=dl.mean(), p_logloss=stats.wilcoxon(dl).pvalue if (dl != 0).any() else 1, gain_places_sur3=d3.mean()))
R1 = pd.DataFrame(res).sort_values("gain_logloss", ascending=False); say(R1.round(4).to_string(index=False))
say("  (gain_logloss > 0 : le groupe ameliore la prediction au-dela de la cote)")
say("\n# 2. IMPORTANCE EN RETIRANT UN GROUPE DU MODELE COMPLET (perte si on l'enleve)")
prF = cv(["lp"] + ALL); llF = ll_race(prF); res = []
for g, cols in GROUPES.items():
    pr = cv(["lp"] + [c for c in ALL if c not in cols]); res.append(dict(groupe=g, perte_logloss=(ll_race(pr) - llF).mean()))
say(pd.DataFrame(res).sort_values("perte_logloss", ascending=False).round(4).to_string(index=False))
say("\n# 3. SIGNAL PAR SIGNAL, AU-DELA DE LA COTE (odds ratio par ecart-type ; IC95 ; Holm)")
from statsmodels.stats.multitest import multipletests
rows = []
for c in ALL:
    x = (M[c] - M[c].mean()) / (M[c].std() + 1e-9); m = sm.GLM(M.y, sm.add_constant(pd.concat([M.lp, x.rename("x")], axis=1)), family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(M.race)[0]})
    rows.append(dict(signal=c, odds_ratio=np.exp(m.params["x"]), ic_bas=np.exp(m.conf_int().loc["x", 0]), ic_haut=np.exp(m.conf_int().loc["x", 1]), p=m.pvalues["x"]))
T = pd.DataFrame(rows); T["p_holm"] = multipletests(T.p, method="holm")[1]; say(T.sort_values("p").round(3).to_string(index=False))
say("\n# 4. MODELES COMPLETS (validation croisee, aucune course vue pendant son calibrage)")
prG = cv(["lp"] + ALL, model="gbm"); prC = cv(["lp", "f_classe", "f_avis"])
def rep(titre, mask):
    n = M[mask].race.nunique() if mask is not None else M.race.nunique(); d = M.assign(c=base_pr, f=prF, g=prG, k=prC); d = d if mask is None else d[mask]
    b = prec3(d.c.values, None) if False else np.array([g.sort_values("c", ascending=False).head(3).y.sum() for _, g in d.groupby("race")])
    say(f"\n## {titre} ({n} courses)")
    for lab, col in [("cote seule", "c"), ("cote + classe + avis", "k"), ("MODELE COMPLET (regression)", "f"), ("MODELE COMPLET (arbres)", "g")]:
        a = np.array([g.sort_values(col, ascending=False).head(3).y.sum() for _, g in d.groupby("race")]); dd = a - b
        auc = np.mean([roc_auc_score(g.y, g[col]) for _, g in d.groupby("race") if 0 < g.y.sum() < len(g)])
        say(f"  {lab:32s}: {a.mean():.2f} places sur les 3 chevaux choisis (ecart vs cote {dd.mean():+.2f}, p={stats.wilcoxon(dd[dd != 0]).pvalue if (dd != 0).any() else 1:.2f}) | AUC/course {auc:.3f}")
rep("TOUTES LES COURSES", None); rep("COURSES GARDEES (lisibles, hors profil D)", M.gardee); rep("COURSES ECARTEES", ~M.gardee)
rep("NOVEMBRE", M.ech == "novembre"); rep("ORIGINE", M.ech == "origine")
M["P_modele"] = prF; M["P_cote"] = base_pr
say("\n# 5. FIABILITE DES PROBABILITES DU MODELE COMPLET")
M["tr"] = pd.cut(M.P_modele, [0, .15, .3, .45, .6, .75, 1], labels=["< 15 %", "15-30 %", "30-45 %", "45-60 %", "60-75 %", "> 75 %"])
for lab, d in [("toutes", M), ("gardees", M[M.gardee])]:
    t = d.groupby("tr").agg(chevaux=("y", "size"), annonce=("P_modele", "mean"), reel=("y", "mean")).round(2); say(f"  {lab} :\n" + "\n".join("    " + l for l in t.to_string().split("\n")))
M.to_csv(f"{D}/scenario1_partants.csv", index=False)
sel = M.sort_values(["race", "P_modele"], ascending=[True, False]).groupby("race").head(3)[["race", "ech", "gardee", "numero", "cote", "P_modele", "P_cote", "pos", "y"]]; sel.to_csv(f"{D}/scenario1_choix_par_course.csv", index=False)
open(f"{D}/rapport_scenario1.txt", "w").write("\n".join(out))
