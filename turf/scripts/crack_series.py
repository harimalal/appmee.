"""Crack Series (letrot.com) et donnees letrot avant course : apport au-dela de la cote PMU finale.
Usage : python3 -I crack_series.py <dossier_data>
"""
import sys, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
from scipy.optimize import minimize
from scipy.special import logsumexp
from statsmodels.stats.multitest import multipletests
warnings.filterwarnings("ignore")
D = sys.argv[1]
P = pd.read_csv(f"{D}/partants_signaux.csv")
L = pd.read_csv(f"{D}/letrot_partants.csv").rename(columns={"rentree": "rentree_letrot"})
M = P.merge(L, on=["race_id", "numero"], how="left")
rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))
nm = M.cheval_letrot.isna().sum()
ok_name = (M.cheval.str.upper().str.replace(r"[^A-Z]", "", regex=True) == M.cheval_letrot.str.upper().str.replace(r"[^A-Z]", "", regex=True)).mean()
say(f"# DONNEES : {len(M)} partants, {M.race_id.nunique()} courses ; non retrouves sur letrot : {nm} ; noms concordants : {ok_name:.0%}")

# ---------------- cote PMU finale (tous les partants) -> proba implicite
M["cote_pmu"] = M.cote_pmu_letrot.where(M.cote_pmu_letrot > 0)
M["cote_pmu"] = M.cote_pmu.fillna(M.cote_presse)
q = 1 / M.cote_pmu; M["p_pmu"] = q / q.groupby(M.race_id).transform("sum"); M["log_p_pmu"] = np.log(M.p_pmu)
M["rang_pmu"] = M.groupby("race_id").cote_pmu.rank(method="first")
# ---------------- Crack Series : rang au classement (plus petit = meilleur) ; 0 = non classe
M["crack"] = M.crack_series.where(M.crack_series > 0, M.crack_series.max() + 1)
M["log_crack"] = np.log(M.crack)
M["crack_rang_course"] = M.groupby("race_id").crack.rank(method="min")           # 1 = meilleur Crack Series du lot
M["crack_rel"] = M.log_crack - M.groupby("race_id").log_crack.transform("mean")   # <0 = mieux classe que la moyenne du lot
rho, p = stats.spearmanr(M.crack, M.cote_pmu)
say(f"Sens de l'indice : correlation Crack Series / cote PMU = {rho:+.2f} (p={p:.1e}) -> {'plus petit = meilleur (rang)' if rho > 0 else 'plus grand = meilleur'}")
rho2, p2 = stats.spearmanr(M.cote_pmu, M.cote_presse)
say(f"Cote PMU finale vs cote presse : correlation {rho2:+.2f}")

# ---------------- 1. descriptif : top 4 selon le rang Crack Series dans la course
say("\n# 1. TAUX D'ARRIVEE SELON LE RANG CRACK SERIES DANS LA COURSE (1 = meilleur classe du lot)")
M["crack_bin"] = pd.cut(M.crack_rang_course, [0, 1, 2, 3, 5, 8, 20], labels=["1", "2", "3", "4-5", "6-8", "9+"])
M["cote_bin"] = pd.cut(M.rang_pmu, [0, 1, 2, 3, 5, 8, 20], labels=["1", "2", "3", "4-5", "6-8", "9+"])
t = M.groupby("crack_bin").agg(n=("win", "size"), victoire=("win", "mean"), top3=("top3", "mean"), top4=("top4", "mean"), p_pmu=("p_pmu", "mean"))
t2 = M.groupby("cote_bin").agg(top4_selon_cote=("top4", "mean"))
say(t.join(t2.rename_axis("crack_bin")).round(2).to_string())

# ---------------- modeles Plackett-Luce (ordre des 4 premiers)
def stages(df, K=4):
    out = []
    for rid, g in df.groupby("race_id"):
        idx = g.index.values; pos = g.position.values; alive = np.ones(len(idx), bool)
        for k in range(1, K + 1):
            w = np.where(pos == k)[0]
            if len(w) != 1: break
            out.append((idx[alive], idx[w[0]])); alive[w[0]] = False
    return out
def fit(df, cols, lam=0.0):
    X = df[cols].values.astype(float); pos = {ix: i for i, ix in enumerate(df.index)}
    st = [(np.array([pos[a] for a in s]), pos[c]) for s, c in stages(df)]
    def nll(b):
        u = X @ b; f = 0.0; g = np.zeros(len(b))
        for s, c in st:
            lse = logsumexp(u[s]); p = np.exp(u[s] - lse); f -= u[c] - lse; g -= X[c] - p @ X[s]
        return f + lam * b @ b, g + 2 * lam * b
    r = minimize(nll, np.zeros(len(cols)), jac=True, method="L-BFGS-B"); b = r.x
    H = np.zeros((len(b), len(b))); u = X @ b
    for s, c in st:
        p = np.exp(u[s] - logsumexp(u[s])); m = p @ X[s]; H += (X[s] * p[:, None]).T @ X[s] - np.outer(m, m)
    se = np.sqrt(np.diag(np.linalg.pinv(H + 2 * lam * np.eye(len(b)))))
    return b, se, -(r.fun - lam * b @ b)
def ev(g, u):
    pos = g.position.values; ll = 0.0; alive = np.ones(len(g), bool)
    for k in range(1, 5):
        w = np.where(pos == k)[0][0]; ll += u[w] - logsumexp(u[alive]); alive[w] = False
    y = g.top4.values; top = np.argsort(-u)[:4]
    return ll, y[top].sum(), stats.mannwhitneyu(u[y == 1], u[y == 0]).statistic / (y.sum() * (1 - y).sum())
order = M.drop_duplicates("race_id").sort_values(["date", "race_id"]).race_id.tolist()
def loo(cols, fixed=None, lam=0.0):
    out = []
    for rid in order:
        te = M[M.race_id == rid]
        if fixed is not None: u = te[list(fixed)].values @ np.array(list(fixed.values()))
        else:
            b, _, _ = fit(M[M.race_id != rid], cols, lam); u = te[cols].values.astype(float) @ b
        out.append(ev(te, u))
    return pd.DataFrame(out, columns=["ll", "hits", "auc"])
z = lambda s: (s - s.mean()) / s.std()
M["z_crack"] = z(M.crack_rel)

say("\n# 2. CRACK SERIES SEUL ET AU-DELA DE LA COTE (Plackett-Luce, 4 premieres places, 40 courses)")
b0, se0, ll0 = fit(M, ["log_p_pmu"])
b1, se1, ll1 = fit(M, ["z_crack"])
b2, se2, ll2 = fit(M, ["log_p_pmu", "z_crack"])
LR = 2 * (ll2 - ll0)
say(f"Cote PMU seule : coef {b0[0]:.2f} (logL {ll0:.1f})")
say(f"Crack Series seul : coef {b1[0]:+.2f} par ecart-type (p={2*stats.norm.sf(abs(b1[0]/se1[0])):.1e}) (logL {ll1:.1f})")
say(f"Cote + Crack Series : coef Crack {b2[1]:+.2f} (IC95 {b2[1]-1.96*se2[1]:+.2f} a {b2[1]+1.96*se2[1]:+.2f}), test LR = {LR:.2f}, p={stats.chi2.sf(LR,1):.4f}")
say("(coef negatif = mieux classe au Crack Series -> plus de chances, car un petit rang = meilleur)")

say("\nValidation croisee (course retiree a la fois) :")
R = {"Cote PMU finale brute": loo(None, {"log_p_pmu": 1.0}), "Cote presse brute": loo(None, {"log_p_impl": 1.0}),
     "Cote PMU recalibree": loo(["log_p_pmu"]), "Crack Series seul": loo(["z_crack"]), "Cote PMU + Crack Series": loo(["log_p_pmu", "z_crack"])}
base = R["Cote PMU finale brute"]
rows = []
for k, d in R.items():
    diff = d.ll - base.ll; pw = stats.wilcoxon(diff).pvalue if np.any(diff != 0) else 1.0
    rows.append(dict(modele=k, logL_ordre4=d.ll.mean(), top4_trouves=d.hits.mean(), AUC=d.auc.mean(), gain_vs_cote_PMU=f"{diff.mean():+.3f} (p={pw:.3f})",
                     courses_ameliorees=f"{int((diff>0).sum())}/40"))
say(pd.DataFrame(rows).round(3).to_string(index=False))

# ---------------- 3. autres donnees letrot avant course (au-dela de la cote PMU)
say("\n# 3. AUTRES DONNEES LETROT AVANT COURSE : apport au-dela de la cote PMU (logit offset, place dans les 3)")
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
M["p3_pmu"] = np.nan
for rid, g in M.groupby("race_id"): M.loc[g.index, "p3_pmu"] = harville_top3(g.p_pmu.values)
M["p3_pmu"] = M.p3_pmu.clip(1e-4, 1 - 1e-4); off = np.log(M.p3_pmu / (1 - M.p3_pmu))
M["avis_positif"] = (M.avis_entraineur == 3).astype(int); M["avis_negatif"] = (M.avis_entraineur == 1).astype(int)
M["deferre_4"] = (M.ferrure == "D4").astype(int)
M["meilleur_crack_lot"] = (M.crack_rang_course <= 2).astype(int)
SIG = {"meilleur_crack_lot": "parmi les 2 meilleurs Crack Series du lot", "z_crack": "Crack Series relatif (par ecart-type, - = mieux classe)",
       "avis_positif": "avis entraineur defavorable (3)", "avis_negatif": "avis entraineur favorable (1, trainer confiant)", "deferre_4": "deferre des 4 pieds (D4)",
       "first_ferrure": "changement de ferrure (premiere fois)", "changement_entraineur": "changement d'entraineur",
       "rentree_letrot": "rentree (derniere course la plus ancienne)", "course_rapprochee": "course rapprochee", "premier_driver": "nouveau driver",
       "premier_gp": "premiere fois sur la grande piste"}
rows = []
for col, lab in SIG.items():
    x = M[col].astype(float)
    m = sm.GLM(M.top3, sm.add_constant(x), family=sm.families.Binomial(), offset=off).fit()
    n1 = int((M[col] > 0).sum()) if M[col].nunique() <= 2 else len(M)
    sub = M[M[col] > 0] if M[col].nunique() <= 2 else M
    rows.append(dict(donnee=lab, chevaux=n1, places=int(sub.top3.sum()), attendu=round(sub.p3_pmu.sum(), 1),
                     obs_att=sub.top3.sum() / sub.p3_pmu.sum(), odds_ratio=np.exp(m.params.iloc[1]), p=m.pvalues.iloc[1]))
T = pd.DataFrame(rows); T["p_holm"] = multipletests(T.p, method="holm")[1]
say(T.round(3).to_string(index=False))

# ---------------- 4. non-favoris bien classes au Crack Series
say("\n# 4. NON-FAVORIS (hors 3 premieres cotes PMU) BIEN CLASSES AU CRACK SERIES")
NF = M[M.rang_pmu >= 4]
for lab, mask in [("meilleur Crack du lot parmi les non-favoris", NF.crack == NF.groupby("race_id").crack.transform("min")),
                  ("Crack Series dans les 3 meilleurs du lot", NF.crack_rang_course <= 3),
                  ("Crack Series moins bon que la mediane du lot", NF.crack_rang_course > NF.groupby("race_id").crack_rang_course.transform("median"))]:
    d = NF[mask]; o, e = d.top3.sum(), d.p3_pmu.sum()
    sims = np.random.default_rng(1).binomial(1, np.tile(d.p3_pmu.values, (20000, 1))).sum(1)
    pv = min(1, 2 * min((sims >= o).mean(), (sims <= o).mean()))
    say(f"  {lab:46s}: {len(d):3d} chevaux, {int(o):2d} places / {e:4.1f} attendus (obs/att {o/e:.2f}, p={pv:.3f})")

# ---------------- 5. paris places (bareme de Hari) avec la vraie cote PMU de tous les partants
BAR = [(5, (1.5, 2.0)), (10, (1.8, 2.5)), (15, (2.5, 3.5)), (20, (3.0, 4.25)), (np.inf, (3.5, 5.0))]
def rapport(c, s):
    for lim, (lo, hi) in BAR:
        if c < lim: return {"bas": lo, "moyen": (lo + hi) / 2, "haut": hi}[s]
M["petit_lot"] = M.partants <= 14
M["profil"] = np.where(M.petit_lot, "petit lot", "grand lot") + np.where((M.femelles_course == 1) | (M.age_max_course <= 6), " / jeunes-femelles", " / mixte ages")
say("\n# 5. PARIS SIMULES (1 euro) - cote PMU finale de tous les partants ; gagnant = cote PMU ; place = bareme de Hari")
def sim(mask, lab):
    d = M[mask]; n = len(d)
    if n == 0: return
    g = (d.win * d.cote_pmu).sum() / n - 1
    pl = [(d.top3 * d.cote_pmu.map(lambda c: rapport(c, s))).sum() / n - 1 for s in ["bas", "moyen", "haut"]]
    say(f"  {lab:58s}: {n:3d} paris | gagnant {g:+.0%} ({int(d.win.sum())} gagnants) | place {pl[0]:+.0%}/{pl[1]:+.0%}/{pl[2]:+.0%}")
sim(M.rang_pmu == 1, "Favori PMU (toutes courses)")
for pf in sorted(M.profil.unique()):
    sim((M.rang_pmu == 1) & (M.profil == pf), f"Favori PMU - {pf}")
sim((M.rang_pmu == 1) & (M.crack_rang_course <= 2), "Favori PMU ET dans les 2 meilleurs Crack Series")
sim((M.rang_pmu == 1) & (M.crack_rang_course > 2), "Favori PMU mais PAS dans les 2 meilleurs Crack Series")
sim((M.rang_pmu == 1) & M.petit_lot & (M.crack_rang_course <= 2), "Favori PMU, petit lot, top 2 Crack Series")
sim((M.rang_pmu.between(2, 5)) & (M.crack_rang_course == 1), "Cote 2e-5e mais MEILLEUR Crack Series du lot")
sim((M.rang_pmu >= 4) & (M.crack_rang_course <= 2), "Non-favori (4e cote et +) dans les 2 meilleurs Crack Series")
say("\nNB : plusieurs strategies testees sur 40 courses -> resultats a confirmer.")

open(f"{D}/rapport_crack_series.txt", "w").write("\n".join(rep))
M.to_csv(f"{D}/partants_letrot_merge.csv", index=False)
print("\n".join(rep))
