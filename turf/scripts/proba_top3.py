"""Probabilite d'etre dans les 3 premiers, cheval par cheval : quel modele repere le mieux les chevaux qui finissent dans les 3 ?
Validation croisee par course (aucune course n'est jamais jugee par un modele qui l'a vue). 82 courses d'attele de Vincennes.
Usage : python3 -I proba_top3.py <dossier_data>
"""
import sys, warnings, numpy as np, pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import log_loss, roc_auc_score
warnings.filterwarnings("ignore")
D = sys.argv[1]; out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(out[-1])
O = pd.read_csv(f"{D}/feat_origine.csv"); N = pd.read_csv(f"{D}/feat_novembre.csv"); O["ech"] = "origine"; N["ech"] = "novembre"
M = pd.concat([O, N], ignore_index=True); M = M[(M.discipline == "A") & (M.cote > 0)].copy()
M = M[M.groupby("race").cote.transform("size") >= 6].reset_index(drop=True)
q = 1 / M.cote; M["p"] = q / q.groupby(M.race).transform("sum"); M["lp"] = np.log(M.p)
M["pos"] = M.pos.where(M.pos > 0); M["y"] = (M.pos <= 3).astype(int)
M["rang_cote"] = M.groupby("race").cote.rank(method="first")
def rel(s): return s - s.groupby(M.race).transform("mean")
M["crack0"] = M.crack.where(M.crack > 0, M.crack.max() + 1)
M["f_classe"] = rel(-np.log(M.crack0)); M["f_exp"] = rel(np.log1p(M.gains)); M["f_forme"] = rel(M.song_top3.astype(float))
M["f_vin"] = rel(M.vin_top3 / (M.vin_n + 1)); M["f_dq"] = rel(M.song_dq.astype(float)); M["f_avis"] = (M.avis == 1).astype(float)
M["f_gm"] = rel(np.log1p(M.gains_moy)); M["f_record"] = rel(M.record.fillna(M.record.median()) * -1)
M["f_age"] = rel(M.age.astype(float)); M["f_fem"] = (M.sexe == "F").astype(float); M["f_d4"] = (M.ferrure == "D4").astype(float)
M["f_num"] = M.numero / M.partants; M["f_n"] = M.partants.astype(float); M["f_rentree"] = M.rentree.astype(float)
SIG = ["f_classe", "f_exp", "f_forme", "f_vin", "f_dq", "f_avis"]
ALL = SIG + ["f_gm", "f_record", "f_age", "f_fem", "f_d4", "f_num", "f_n", "f_rentree"]
say(f"# {M.race.nunique()} courses, {len(M)} partants, {int(M.y.sum())} places ; signaux avant course uniquement")
# lisibilite / filtre (seuils figes de l'origine, comme dans l'analyse precedente)
M["ent"] = M.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s))); M["pfav"] = M.groupby("race").p.transform("max")
Ro = M[M.ech == "origine"].drop_duplicates("race"); zf, ze = (Ro.pfav.mean(), Ro.pfav.std()), (Ro.ent.mean(), Ro.ent.std())
M["lis"] = (M.pfav - zf[0]) / zf[1] - (M.ent - ze[0]) / ze[1]; seuil = M[M.ech == "origine"].drop_duplicates("race").lis.quantile(1 / 3)
M["petit"] = M.partants <= 14; M["jf"] = M.groupby("race").sexe.transform(lambda s: (s == "F").all()) | (M.groupby("race").age.transform("max") <= 6)
M["gardee"] = (M.lis > seuil) & ~((~M.petit) & M.jf)
def models():
    return {"1 cote seule (recalibree)": (["lp"], lambda: LogisticRegression(C=100, max_iter=500)),
            "2 cote + signaux (6)": (["lp"] + SIG, lambda: LogisticRegression(C=0.3, max_iter=500)),
            "3 cote + tous les signaux (14)": (["lp"] + ALL, lambda: LogisticRegression(C=0.3, max_iter=500)),
            "4 arbres (gradient boosting, 14 signaux)": (["lp"] + ALL, lambda: HistGradientBoostingClassifier(max_depth=2, learning_rate=0.05, max_iter=120, min_samples_leaf=25, l2_regularization=5.0, random_state=0))}
races = M.race.unique(); P = {k: np.zeros(len(M)) for k in models()}
for rep in range(3):
    rng = np.random.default_rng(rep); perm = rng.permutation(races); fold = {r: i % 10 for i, r in enumerate(perm)}; f = M.race.map(fold).values
    for k, (cols, mk) in models().items():
        for i in range(10):
            tr, te = f != i, f == i
            Xtr = M.loc[tr, cols].values; mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
            m = mk().fit((Xtr - mu) / sd, M.y[tr]); P[k][te] += m.predict_proba((M.loc[te, cols].values - mu) / sd)[:, 1] / 3
for k in P: M["P " + k] = P[k]
def prec3(df, col):
    r = []
    for _, g in df.groupby("race"):
        s = g.sort_values(col, ascending=False).head(3); r.append(s.y.sum())
    return np.array(r)
def auc_race(df, col):
    a = []
    for _, g in df.groupby("race"):
        if 0 < g.y.sum() < len(g): a.append(roc_auc_score(g.y, g[col]))
    return np.mean(a)
def rapport(df, titre):
    say(f"\n## {titre} ({df.race.nunique()} courses, {len(df)} partants)")
    base = prec3(df, "P 1 cote seule (recalibree)")
    say(f"{'modele':44s} {'log-loss':>9s} {'AUC/course':>10s} {'3 choisis -> places':>20s} {'ecart vs cote':>14s}")
    for k in models():
        c = "P " + k; pr = prec3(df, c); d = pr - base
        pv = stats.wilcoxon(d[d != 0]).pvalue if (d != 0).any() else 1.0
        say(f"{k:44s} {log_loss(df.y, df[c].clip(1e-4, 1-1e-4)):9.4f} {auc_race(df, c):10.3f} {pr.mean():11.2f} sur 3 {'':>6s} {d.mean():+6.2f} (p={pv:.2f})")
    hasard = (3 * 3 / df.groupby("race").size()).mean()
    say(f"  Repere : au hasard {hasard:.2f} places sur 3 ; favori + 2e + 3e cote = {prec3(df.assign(r=-df.rang_cote), 'r').mean():.2f}")
rapport(M, "TOUTES LES COURSES"); rapport(M[M.gardee], "COURSES GARDEES (lisibles, hors profil D)"); rapport(M[~M.gardee], "COURSES ECARTEES")
rapport(M[M.ech == "novembre"], "NOVEMBRE seul"); rapport(M[M.ech == "origine"], "ORIGINE seul")
# lecture en probabilites : fiabilite
say("\n## Fiabilite : quand le modele annonce une probabilite d'etre dans les 3, que se passe-t-il ? (modele 2, toutes courses)")
c = "P 2 cote + signaux (6)"; M["tr"] = pd.cut(M[c], [0, .15, .3, .45, .6, .75, 1], labels=["< 15 %", "15-30 %", "30-45 %", "45-60 %", "60-75 %", "> 75 %"])
t = M.groupby("tr").agg(chevaux=("y", "size"), annonce=(c, "mean"), reel=("y", "mean")).round(2); say(t.to_string())
say("  Meme lecture sur les COURSES GARDEES :"); t = M[M.gardee].groupby("tr").agg(chevaux=("y", "size"), annonce=(c, "mean"), reel=("y", "mean")).round(2); say(t.to_string())
# combien de chevaux a plus de 50 % par course gardee, et combien de places
M["fort"] = M[c] >= 0.5; g = M[M.gardee & M.fort]
say(f"\n  Chevaux annonces a 50 % ou plus dans les courses gardees : {len(g)} chevaux ({g.race.nunique()} courses), {g.y.mean():.0%} finissent dans les 3 (le modele en annonce {g[c].mean():.0%})")
M.to_csv(f"{D}/proba_top3_82.csv", index=False)
open(f"{D}/rapport_proba_top3.txt", "w").write("\n".join(out))
