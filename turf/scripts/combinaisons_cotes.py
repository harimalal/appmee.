"""Combinaisons de cotes selon la configuration de course.
Partie 1 (100 courses) : composition du top 4 par tranches de cote PMU finale, selon la configuration.
Partie 2 (40 courses a lot complet) : melange pondere de sources de cote (Paris-Turf, Tierce Magazine, consensus des journaux),
          poids fixes puis poids ajustes, puis poids variables selon la configuration. Tout est evalue hors echantillon.
Usage : python3 -I combinaisons_cotes.py <json> <dossier_data>
"""
import sys, json, re, warnings, itertools
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
from scipy.optimize import minimize
from scipy.special import logsumexp
warnings.filterwarnings("ignore")
src, D = sys.argv[1], sys.argv[2]
races = sorted(json.load(open(src))["message"], key=lambda r: (r["date"], r["r/c"]))
R = pd.read_csv(f"{D}/courses.csv")
P = pd.read_csv(f"{D}/partants_signaux.csv").reset_index(drop=True)
rng = np.random.default_rng(21)
rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))

# =============================================================== PARTIE 1 : composition du top 4 (100 courses)
TR = [(0, 5, "F"), (5, 10, "M"), (10, 20, "O"), (20, 1e9, "G")]   # F favori/petite cote, M moyenne, O outsider, G gros outsider
NOM = {"F": "cote < 5", "M": "5-10", "O": "10-20", "G": ">= 20"}
def tranche(c):
    for lo, hi, t in TR:
        if lo <= c < hi: return t
rows = []
for i, r in enumerate(races):
    cotes = []
    for n in r["arrivee"][:4]:
        h = r["arrivee_details"].get(str(n))
        v = [x for x in (h["cotes"] if h else []) if x is not None]
        cotes.append(v[-1] if v else np.nan)
    if any(np.isnan(cotes)): continue
    t = [tranche(c) for c in cotes]
    rr = R[R.race_id == i].iloc[0]
    rows.append(dict(race_id=i, date=r["date"], partants=r["partants"], montant=r["montant"], distance=r["distance"],
                     femelles=rr.femelles, age_max=rr.age_max, recul=rr.recul, type=r["type"],
                     n_F=t.count("F"), n_M=t.count("M"), n_O=t.count("O"), n_G=t.count("G"),
                     gagnant=t[0], motif="".join(sorted(t, key="FMOG".index)), somme_log_cote=np.log(cotes).sum()))
C = pd.DataFrame(rows)
C = C[C.type == "Attelé"]
C["config_partants"] = pd.cut(C.partants, [0, 14, 16, 30], labels=["<=14", "15-16", ">=17"])
C["config_distance"] = pd.cut(C.distance, [0, 2200, 2750, 9999], labels=["2100 (courte)", "2700", "2850+ (longue)"])
C["config_allocation"] = pd.qcut(C.montant, 3, labels=["petite", "moyenne", "grosse"])
C["config_age"] = np.where(C.age_max <= 6, "jeunes (<=6 ans)", "ages (>6 ans)")
C["config_femelles"] = np.where(C.femelles == 1, "femelles", "mixte")
say(f"# PARTIE 1 - COMPOSITION DU TOP 4 PAR TRANCHE DE COTE PMU FINALE ({len(C)} courses d'attele)")
say("Tranches : F = cote < 5 | M = 5 a 10 | O = 10 a 20 | G = 20 et plus")
say(f"Moyenne par course : {C.n_F.mean():.2f} F, {C.n_M.mean():.2f} M, {C.n_O.mean():.2f} O, {C.n_G.mean():.2f} G (total 4)")
say("\nMotifs les plus frequents (ordre F, M, O, G) :")
mot = C.motif.value_counts()
say((mot.head(10).to_frame("courses").assign(part=lambda d: (d.courses / len(C)).round(2))).to_string())
say(f"Courses avec au moins 1 cote < 5 dans le top 4 : {(C.n_F >= 1).mean():.0%} | au moins 1 cote >= 20 : {(C.n_G >= 1).mean():.0%} | "
    f"au moins 2 cotes >= 10 : {((C.n_O + C.n_G) >= 2).mean():.0%}")
say("\nComposition moyenne du top 4 selon la configuration :")
for cfg in ["config_partants", "config_distance", "config_allocation", "config_age", "config_femelles"]:
    g = C.groupby(cfg).agg(courses=("n_F", "size"), F=("n_F", "mean"), M=("n_M", "mean"), O=("n_O", "mean"), G=("n_G", "mean"),
                           gagnant_cote_lt5=("gagnant", lambda s: (s == "F").mean()),
                           au_moins_1_G=("n_G", lambda s: (s >= 1).mean()))
    # test : la configuration change-t-elle la composition ? (chi2 sur le tableau tranches x configuration)
    tab = C.groupby(cfg)[["n_F", "n_M", "n_O", "n_G"]].sum()
    chi = stats.chi2_contingency(tab.values)
    say(f"\n-- {cfg.replace('config_', '')} (chi2 composition : p={chi[1]:.3f})")
    say(g.round(2).to_string())
say("\nModele de Poisson : nombre de cotes >= 10 dans le top 4 selon la configuration (tout ensemble)")
C["n_outsiders"] = C.n_O + C.n_G
X = pd.get_dummies(C[["config_partants", "config_distance", "config_allocation", "config_age", "config_femelles"]], drop_first=True).astype(float)
m = sm.GLM(C.n_outsiders, sm.add_constant(X), family=sm.families.Poisson()).fit()
say("  " + "\n  ".join(f"{k:40s} x{np.exp(v):.2f} (p={p:.3f})" for k, v, p in zip(m.params.index, m.params, m.pvalues) if k != "const"))
# stabilite : moitie 1 / moitie 2
half = len(C) // 2; C = C.sort_values("date")
say("\nStabilite (50 premieres / 49 suivantes) - nombre moyen de cotes >= 10 dans le top 4 :")
for cfg in ["config_partants", "config_distance", "config_allocation", "config_age"]:
    a = C.iloc[:half].groupby(cfg).n_outsiders.mean().round(2).to_dict(); b = C.iloc[half:].groupby(cfg).n_outsiders.mean().round(2).to_dict()
    say(f"  {cfg.replace('config_', ''):12s} 1re moitie {a} | 2e moitie {b}")

# =============================================================== PARTIE 2 : melange pondere de cotes (40 courses)
say("\n# PARTIE 2 - MELANGE PONDERE DE SOURCES DE COTE (40 courses a lot complet)")
# sources : Paris-Turf, Tierce Magazine, consensus des journaux (citations ponderees par 1/rang)
P["log_p_pt"] = P.log_p_impl
tm = 1 / P.cote_tm; tm = tm / tm.groupby(P.race_id).transform("sum"); P["log_p_tm"] = np.log(tm)
cons = {}
for i, r in enumerate(races):
    pron = r.get("pronostics_presse") or {}
    for p in (r.get("partants_details") or []):
        cons[(i, p["numero"])] = sum(1 / (lst.index(p["numero"]) + 1) for lst in pron.values() if p["numero"] in lst)
P["cons_raw"] = [cons.get((a, b), 0) for a, b in zip(P.race_id, P.numero)]
P["p_cons"] = (P.cons_raw + 0.05) / (P.cons_raw + 0.05).groupby(P.race_id).transform("sum")   # +0,05 : un cheval non cite garde une petite chance
P["log_p_cons"] = np.log(P.p_cons)
SRC = ["log_p_pt", "log_p_tm", "log_p_cons"]
say("Correlation entre sources (log proba) :\n" + P[SRC].corr().round(3).to_string())
# configuration (variables de course, centrees)
cfg = pd.DataFrame({"z_partants": P.partants, "z_alloc": np.log(P.montant), "z_dist": P.distance,
                    "z_age": P.age_max_course, "z_lisib": P.lisibilite})
cfg = (cfg - cfg.mean()) / cfg.std()
P = pd.concat([P, cfg], axis=1)
for s in SRC:
    for c in cfg.columns:
        P[f"{s}__{c}"] = P[s] * P[c]

def stages(df, K=4):
    out = []
    for rid, g in df.groupby("race_id"):
        idx = g.index.values; pos = g.position.values; alive = np.ones(len(idx), bool)
        for k in range(1, K + 1):
            w = np.where(pos == k)[0]
            if len(w) != 1: break
            out.append((idx[alive], idx[w[0]])); alive[w[0]] = False
    return out
def fit(df, cols, lam=0.0, prior=None):
    X = df[cols].values; pos = {ix: i for i, ix in enumerate(df.index)}
    st = [(np.array([pos[a] for a in s]), pos[c]) for s, c in stages(df)]
    prior = np.zeros(len(cols)) if prior is None else prior
    def nll(b):
        u = X @ b; f = 0.0; g = np.zeros(len(b))
        for s, c in st:
            lse = logsumexp(u[s]); p = np.exp(u[s] - lse); f -= u[c] - lse; g -= X[c] - p @ X[s]
        return f + lam * ((b - prior) ** 2).sum(), g + 2 * lam * (b - prior)
    return minimize(nll, prior.copy(), jac=True, method="L-BFGS-B").x
def eval_race(g, u, K=4):
    pos = g.position.values; ll = 0.0; alive = np.ones(len(g), bool)
    for k in range(1, K + 1):
        w = np.where(pos == k)[0][0]; ll += u[w] - logsumexp(u[alive]); alive[w] = False
    y = g.top4.values; top = np.argsort(-u)[:4]
    auc = stats.mannwhitneyu(u[y == 1], u[y == 0]).statistic / (y.sum() * (1 - y).sum())
    return ll, y[top].sum(), auc
order = P.drop_duplicates("race_id").sort_values(["date", "race_id"]).race_id.tolist()
def loo(cols=None, fixed=None, lam=0.0, prior=None):
    out = []
    for rid in order:
        te = P[P.race_id == rid]
        if fixed is not None:
            u = te[list(fixed)].values @ np.array(list(fixed.values()))
        else:
            b = fit(P[P.race_id != rid], cols, lam, prior); u = te[cols].values @ b
        out.append(eval_race(te, u))
    return pd.DataFrame(out, columns=["ll", "hits", "auc"])
MOD = {}
MOD["Paris-Turf seul (brut)"] = loo(fixed={"log_p_pt": 1.0})
MOD["Tierce Magazine seul (brut)"] = loo(fixed={"log_p_tm": 1.0})
MOD["Consensus journaux seul (brut)"] = loo(fixed={"log_p_cons": 1.0})
MOD["Melange egal 1/3-1/3-1/3 (sans ajustement)"] = loo(fixed={s: 1 / 3 for s in SRC})
MOD["Melange PT+TM 50/50 (sans ajustement)"] = loo(fixed={"log_p_pt": .5, "log_p_tm": .5})
MOD["Melange ajuste (3 poids estimes)"] = loo(SRC)
INTER = [c for c in P.columns if "__z_" in c]
for lam in [3, 10, 30]:
    MOD[f"Melange + poids selon configuration (ridge {lam})"] = loo(SRC + INTER, lam=lam)
base = MOD["Paris-Turf seul (brut)"]
tab = []
for k, d in MOD.items():
    diff = d.ll - base.ll
    p = stats.wilcoxon(diff).pvalue if np.any(diff != 0) else 1.0
    bs = [rng.choice(diff.values, len(diff)).mean() for _ in range(3000)]
    tab.append(dict(modele=k, logL_ordre4=d.ll.mean(), top4_trouves=d.hits.mean(), AUC=d.auc.mean(),
                    gain_vs_PT=f"{diff.mean():+.3f} [{np.percentile(bs,2.5):+.3f};{np.percentile(bs,97.5):+.3f}] p={p:.2f}"))
say("\nValidation croisee (une course retiree a la fois). logL : plus haut = meilleur ; gain vs Paris-Turf brut avec IC95 bootstrap.")
say(pd.DataFrame(tab).round(3).to_string(index=False))

# poids ajustes sur les 40 courses (description)
b = fit(P, SRC)
say(f"\nPoids ajustes sur les 40 courses (echelle log proba) : Paris-Turf {b[0]:+.2f}, Tierce Mag. {b[1]:+.2f}, consensus {b[2]:+.2f} (somme {b.sum():.2f})")
# poids selon la configuration : on ajuste le melange separement par sous-groupe
say("\nPoids du melange ajustes par type de course (description ; petits effectifs) :")
P["g_lisib"] = P.classe
P["g_partants"] = pd.cut(P.partants, [0, 14, 16, 30], labels=["<=14", "15-16", ">=17"]).astype(str)
P["g_dist"] = pd.cut(P.distance, [0, 2200, 2750, 9999], labels=["2100", "2700", "2850+"]).astype(str)
for gcol in ["g_lisib", "g_partants", "g_dist"]:
    for v, sub in P.groupby(gcol):
        n = sub.race_id.nunique()
        if n < 6: say(f"  {gcol[2:]}={v}: {n} courses (trop peu)"); continue
        bb = fit(sub, SRC, lam=1.0, prior=np.array([1/3, 1/3, 1/3]))
        say(f"  {gcol[2:]:9s}={v:12s} ({n:2d} courses) : PT {bb[0]:+.2f} | TM {bb[1]:+.2f} | consensus {bb[2]:+.2f}")

# combinaison pratique : quelle selection de 4 chevaux par configuration ?
say("\n# SELECTION DE 4 CHEVAUX : combien du top 4 trouves selon la regle et la lisibilite (40 courses)")
P["u_mix"] = P[SRC].mean(axis=1)
P["rang_pt"] = P.groupby("race_id").log_p_pt.rank(ascending=False, method="first")
P["rang_mix"] = P.groupby("race_id").u_mix.rank(ascending=False, method="first")
P["rang_cons"] = P.groupby("race_id").log_p_cons.rank(ascending=False, method="first")
RULES = {
    "4 premiers Paris-Turf": lambda g: g.rang_pt <= 4,
    "4 premiers du melange egal": lambda g: g.rang_mix <= 4,
    "4 premiers du consensus": lambda g: g.rang_cons <= 4,
    "3 premiers PT + meilleur consensus hors ces 3": lambda g: (g.rang_pt <= 3) | (g.index == g[g.rang_pt > 3].log_p_cons.idxmax()),
    "2 premiers PT + 2 meilleurs consensus hors ces 2": lambda g: (g.rang_pt <= 2) | g.index.isin(g[g.rang_pt > 2].nlargest(2, "log_p_cons").index),
}
res = []
for name, f in RULES.items():
    for rid, g in P.groupby("race_id"):
        sel = f(g); res.append(dict(regle=name, classe=g.classe.iloc[0], hits=g[sel].top4.sum(), n=sel.sum()))
Rr = pd.DataFrame(res)
say(Rr.pivot_table(index="regle", columns="classe", values="hits", aggfunc="mean").round(2).assign(
    tous=Rr.groupby("regle").hits.mean().round(2)).to_string())
say(f"(nb de chevaux selectionnes par regle : {Rr.groupby('regle').n.mean().round(1).to_dict()})")
say("\nAttention : la partie 'par type de course' et les regles de selection sont descriptives (pas de validation separee).")

open(f"{D}/rapport_combinaisons.txt", "w").write("\n".join(rep))
C.to_csv(f"{D}/composition_top4.csv", index=False)
print("\n".join(rep))
