"""Plan de test : criblage (petite population) -> selection de modele -> validation hors echantillon -> population complete.
Usage : python3 -I analyze.py <dossier_data>
"""
import sys, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.discrete.conditional_models import ConditionalLogit
from statsmodels.stats.multitest import multipletests
from scipy import stats
warnings.filterwarnings("ignore")
D = sys.argv[1]
P = pd.read_csv(f"{D}/partants.csv"); R = pd.read_csv(f"{D}/courses.csv")
rng = np.random.default_rng(42)
# valeurs manquantes : ecart au lot = 0 (neutre) + indicatrice deja presente pour le record
for c in ["record_rel", "musique_moy_rel", "musique_victoires", "musique_dq", "log_gains_rel", "age_rel"]:
    P[c] = P[c].fillna(0 if c.endswith("_rel") else P[c].median())

# ------------------------------------------------------------------ variables
P["log_drv_wins"] = np.log1p(P["drv_prior_wins"])
P["log_trn_wins"] = np.log1p(P["trn_prior_wins"])
P["log_montant"] = np.log(P["montant"])
P["lp_x_partants"] = P["log_p_impl"] * (P["partants"] - P["partants"].mean())
P["lp_x_montant"] = P["log_p_impl"] * (P["log_montant"] - P["log_montant"].mean())
FEATS = {  # facteur -> (colonne, hypothese de signe sur la proba de gagner)
    "cote presse (log p implicite)": ("log_p_impl", "+"),
    "record (reduction km, relatif au lot)": ("record_rel", "-"),
    "forme : place moyenne 5 dernieres (relatif)": ("musique_moy_rel", "-"),
    "forme : victoires sur 5 dernieres": ("musique_victoires", "+"),
    "forme : disqualifications/arrets sur 5": ("musique_dq", "-"),
    "gains (log, relatif au lot)": ("log_gains_rel", "+"),
    "age (relatif au lot)": ("age_rel", "?"),
    "male (h/m) vs femelle": ("male", "?"),
    "recul 25 m": ("recul", "-"),
    "driver = entraineur": ("driver_entraineur", "?"),
    "driver : victoires anterieures (log)": ("log_drv_wins", "+"),
    "entraineur : victoires anterieures (log)": ("log_trn_wins", "+"),
    "numero de depart": ("numero", "-"),
}
CONFIG = {"cote x nombre de partants": "lp_x_partants", "cote x allocation (log)": "lp_x_montant"}
# standardisation (z) sur l'ensemble, sauf indicatrices
for c in set(v[0] for v in FEATS.values()) | set(CONFIG.values()):
    if P[c].nunique() > 2:
        P[c + "_z"] = (P[c] - P[c].mean()) / P[c].std()
    else:
        P[c + "_z"] = P[c]
z = lambda c: c + "_z"

races = P.drop_duplicates("race_id").sort_values(["date", "race_id"])["race_id"].tolist()
SCREEN, VALID = races[:20], races[20:]
Ps, Pv = P[P.race_id.isin(SCREEN)], P[P.race_id.isin(VALID)]

def clogit(df, cols):
    m = ConditionalLogit(df["win"].values, df[cols].values, groups=df["race_id"].values).fit(disp=0, method="bfgs", maxiter=500)
    return m

def race_ll(df, cols, beta):
    """log-vraisemblance du gagnant, course par course (softmax intra-course)."""
    out = []
    for rid, g in df.groupby("race_id"):
        u = g[cols].values @ beta
        u = u - u.max()
        p = np.exp(u) / np.exp(u).sum()
        out.append(dict(race_id=rid, ll=np.log(p[g["win"].values == 1][0]),
                        top1=int(g["win"].values[np.argmax(p)] == 1),
                        brier=np.sum((p - g["win"].values) ** 2)))
    return pd.DataFrame(out)

rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))

say("# DONNEES")
say(f"courses (toutes) : {len(R)} | courses a champ complet : {len(races)} | partants : {len(P)}")
say(f"criblage : {len(SCREEN)} courses / {len(Ps)} partants ({Ps.date.min()} -> {Ps.date.max()})")
say(f"validation : {len(VALID)} courses / {len(Pv)} partants ({Pv.date.min()} -> {Pv.date.max()})")

# ------------------------------------------------------------------ PHASE 1 : criblage univarie
say("\n# PHASE 1 - CRIBLAGE (20 courses) : logit conditionnel, un facteur a la fois")
say("coef = effet d'1 ecart-type (ou de l'indicatrice) sur le log-odds de gagner ; 'ajuste' = controle par la cote")
rows = []
for name, (col, sign) in FEATS.items():
    try:
        m1 = clogit(Ps, [z(col)])
        b1, p1 = m1.params[0], m1.pvalues[0]
    except Exception:
        b1 = p1 = np.nan
    if col != "log_p_impl":
        try:
            m2 = clogit(Ps, [z("log_p_impl"), z(col)])
            b2, p2 = m2.params[1], m2.pvalues[1]
        except Exception:
            b2 = p2 = np.nan
    else:
        b2 = p2 = np.nan
    rows.append(dict(facteur=name, col=col, signe_attendu=sign, coef_seul=b1, p_seul=p1, coef_ajuste=b2, p_ajuste=p2))
for name, col in CONFIG.items():
    m2 = clogit(Ps, [z("log_p_impl"), z(col)])
    rows.append(dict(facteur=name, col=col, signe_attendu="?", coef_seul=np.nan, p_seul=np.nan,
                     coef_ajuste=m2.params[1], p_ajuste=m2.pvalues[1]))
S1 = pd.DataFrame(rows)
mask = S1.p_seul.notna()
S1.loc[mask, "p_seul_holm"] = multipletests(S1.loc[mask, "p_seul"], method="holm")[1]
mask = S1.p_ajuste.notna()
S1.loc[mask, "p_ajuste_holm"] = multipletests(S1.loc[mask, "p_ajuste"], method="holm")[1]
# regle de retenue (criblage permissif, annoncee a l'avance) : p < 0.20 en seul OU en ajuste, et signe coherent si attendu
def keep(r):
    sig = (r.p_seul < 0.20) or (r.p_ajuste < 0.20)
    s = r.coef_ajuste if not np.isnan(r.coef_ajuste) else r.coef_seul
    ok = r.signe_attendu == "?" or (np.sign(s) == (1 if r.signe_attendu == "+" else -1))
    return bool(sig and ok)
S1["retenu"] = S1.apply(keep, axis=1)
say(S1[["facteur", "signe_attendu", "coef_seul", "p_seul", "coef_ajuste", "p_ajuste", "p_ajuste_holm", "retenu"]]
    .round(3).to_string(index=False))
kept = [c for c in S1[S1.retenu].col if c != "log_p_impl"]

# ------------------------------------------------------------------ PHASE 2 : modeles candidats (ajustes sur criblage)
say("\n# PHASE 2 - MODELES CANDIDATS (ajustes sur les 20 courses de criblage)")
MODELS = {
    "M0 cote seule": [z("log_p_impl")],
    "M1 cote + facteurs retenus": [z("log_p_impl")] + [z(c) for c in kept],
    "M2 fondamentaux seuls (sans cote)": [z(c) for c in kept] or [z("record_rel")],
    "M3 cote + record + forme (a priori)": [z("log_p_impl"), z("record_rel"), z("musique_moy_rel")],
}
fits = {}
for k, cols in MODELS.items():
    m = clogit(Ps, cols); fits[k] = (cols, m)
    aic = -2 * m.llf + 2 * len(cols)
    say(f"{k}: k={len(cols)} logL={m.llf:.2f} AIC={aic:.1f} | " +
        ", ".join(f"{c.replace('_z','')}={b:+.2f} (p={p:.3f})" for c, b, p in zip(cols, m.params, m.pvalues)))
m0 = fits["M0 cote seule"][1]
b = m0.params[0] / P["log_p_impl"].std()  # coefficient sur l'echelle brute log p
se = m0.bse[0] / P["log_p_impl"].std()
say(f"calibration cote presse (criblage) : beta brut = {b:.2f} (IC95 {b-1.96*se:.2f}-{b+1.96*se:.2f}) ; beta=1 => cote bien calibree, >1 => favoris sous-estimes")

# ------------------------------------------------------------------ PHASE 3 : validation hors echantillon
say("\n# PHASE 3 - VALIDATION HORS ECHANTILLON (20 courses suivantes, coefficients figes)")
base = pd.DataFrame({"race_id": VALID})
res = {}
nrun = Pv.groupby("race_id").size()
res["Hasard (1/N)"] = pd.DataFrame(dict(race_id=nrun.index, ll=-np.log(nrun.values),
                                        top1=[np.nan] * len(nrun), brier=np.nan))
# cote brute (p implicite, sans re-estimation)
raw = []
for rid, g in Pv.groupby("race_id"):
    p = g["p_impl"].values
    raw.append(dict(race_id=rid, ll=np.log(p[g.win.values == 1][0]), top1=int(g.win.values[np.argmax(p)] == 1),
                    brier=np.sum((p - g.win.values) ** 2)))
res["Cote presse brute"] = pd.DataFrame(raw)
for k, (cols, m) in fits.items():
    res[k] = race_ll(Pv, cols, m.params)
tab = []
for k, d in res.items():
    tab.append(dict(modele=k, logL_total=d.ll.sum(), logL_moy=d.ll.mean(), top1=d.top1.mean(), brier=d.brier.mean()))
say(pd.DataFrame(tab).round(3).to_string(index=False))
ref = res["Cote presse brute"].set_index("race_id").ll
for k in fits:
    diff = res[k].set_index("race_id").ll - ref
    bs = [rng.choice(diff.values, len(diff)).mean() for _ in range(5000)]
    w = stats.wilcoxon(diff.values) if diff.abs().sum() > 0 else None
    say(f"{k} vs cote brute : gain moyen logL/course = {diff.mean():+.3f} (IC95 bootstrap {np.percentile(bs,2.5):+.3f} a {np.percentile(bs,97.5):+.3f})"
        + (f", Wilcoxon p={w.pvalue:.3f}" if w else "") + f", courses ameliorees {int((diff>0).sum())}/{len(diff)}")

# ------------------------------------------------------------------ PHASE 4 : population complete (40 courses) + tests LR
say("\n# PHASE 4 - POPULATION COMPLETE (40 courses) : tests du rapport de vraisemblance vs M0")
full0 = clogit(P, [z("log_p_impl")])
b = full0.params[0] / P["log_p_impl"].std(); se = full0.bse[0] / P["log_p_impl"].std()
say(f"M0 : beta brut cote = {b:.2f} (IC95 {b-1.96*se:.2f}-{b+1.96*se:.2f}), Wald H0 beta=1 : p={2*stats.norm.sf(abs((b-1)/se)):.3f}")
lr = []
for name, (col, _) in list(FEATS.items())[1:] + [(n, (c, "?")) for n, c in CONFIG.items()]:
    m = clogit(P, [z("log_p_impl"), z(col)])
    LR = 2 * (m.llf - full0.llf)
    lr.append(dict(facteur=name, coef=m.params[1], p_wald=m.pvalues[1], LR=LR, p_LR=stats.chi2.sf(LR, 1)))
LRt = pd.DataFrame(lr); LRt["p_holm"] = multipletests(LRt.p_LR, method="holm")[1]
say(LRt.round(3).to_string(index=False))
cols1 = fits["M1 cote + facteurs retenus"][0]
if len(cols1) > 1:
    mf = clogit(P, cols1); LR = 2 * (mf.llf - full0.llf)
    say(f"M1 complet (40 courses) : LR={LR:.2f}, ddl={len(cols1)-1}, p={stats.chi2.sf(LR, len(cols1)-1):.3f}, pseudo-R2 McFadden vs hasard = "
        f"{1 - mf.llf / (-np.log(P.groupby('race_id').size()).sum()):.3f} (M0 : {1 - full0.llf / (-np.log(P.groupby('race_id').size()).sum()):.3f})")
# validation croisee "leave-one-race-out" sur 40 courses (plus robuste qu'un seul decoupage)
say("\nValidation croisee leave-one-race-out (40 courses), logL moyenne du gagnant :")
for k, (cols, _) in fits.items():
    lls = []
    for rid in races:
        tr, te = P[P.race_id != rid], P[P.race_id == rid]
        m = clogit(tr, cols)
        lls.append(race_ll(te, cols, m.params).ll.iloc[0])
    say(f"  {k}: {np.mean(lls):.3f}")
say(f"  Cote presse brute : {np.mean([np.log(g.p_impl.values[g.win.values==1][0]) for _, g in P.groupby('race_id')]):.3f}")
say(f"  Hasard : {np.mean(-np.log(P.groupby('race_id').size())):.3f}")

# ------------------------------------------------------------------ PHASE 5 : configuration de course (niveau course, 100 courses)
say("\n# PHASE 5 - CONFIGURATION DE COURSE (niveau course) : la course est-elle previsible ?")
R = R.dropna(subset=["win_cote_final"]).sort_values(["date", "race_id"]).copy()
R["log_cote_gagnant"] = np.log(R["win_cote_final"])
R["log_montant"] = np.log(R["montant"])
R["dist_cat"] = pd.cut(R["distance"], [0, 2200, 2750, 5000], labels=["2100", "2700", "2850+"])
R["monte"] = (R["type"] == "Monté").astype(int)
form = "log_cote_gagnant ~ partants + log_montant + C(dist_cat) + recul + femelles + age_max + monte"
half = len(R) // 2
for lab, d in [("criblage (50 premieres)", R.iloc[:half]), ("validation (49 suivantes)", R.iloc[half:]), ("total (99)", R)]:
    m = smf.ols(form, d).fit(cov_type="HC1")
    say(f"-- {lab} : n={int(m.nobs)} R2={m.rsquared:.3f} R2aj={m.rsquared_adj:.3f} F p={m.f_pvalue:.3f}")
    say("   " + ", ".join(f"{k}={v:+.3f}(p={p:.2f})" for k, v, p in zip(m.params.index, m.params, m.pvalues) if k != "Intercept"))
# favori presse gagnant selon la configuration (40 courses)
F = P[P.fav == 1][["race_id", "win", "partants", "log_montant", "distance"]]
say(f"\nFavori presse gagnant : {F.win.sum()}/{len(F)} = {F.win.mean():.0%} ; prob. implicite moyenne du favori = {P[P.fav==1].p_impl.mean():.0%}")
mf = smf.logit("win ~ partants + log_montant", F).fit(disp=0)
say("logit favori gagne ~ partants + allocation : " + ", ".join(f"{k}={v:+.2f}(p={p:.2f})" for k, v, p in zip(mf.params.index, mf.params, mf.pvalues)))

# ------------------------------------------------------------------ puissance
say("\n# PUISSANCE")
for n_r in [40, 100, 300, 1000]:
    say(f"  {n_r} courses : effet minimal detectable (alpha 5 %, puissance 80 %) sur un facteur z ~ {2.8/np.sqrt(n_r*0.9):.2f} log-odds/ET")

open(f"{D}/rapport.txt", "w").write("\n".join(rep))
S1.to_csv(f"{D}/criblage.csv", index=False); LRt.to_csv(f"{D}/tests_LR_40courses.csv", index=False)
print("\n".join(rep))
