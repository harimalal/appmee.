"""Poids et influence des donnees d'entree sur l'arrivee dans les 4 premiers.
Modele principal : logit ordonne eclate (Plackett-Luce) sur les 4 premieres places, choix sequentiels dans la course.
Usage : python3 -I analyze_top4.py <dossier_data>
"""
import sys, warnings
import numpy as np, pandas as pd
from scipy.optimize import minimize
from scipy import stats
from scipy.special import logsumexp
from statsmodels.stats.multitest import multipletests
warnings.filterwarnings("ignore")
D = sys.argv[1]
P = pd.read_csv(f"{D}/partants_top4.csv")
rng = np.random.default_rng(7)

# ------------------------------------------------------------ donnees d'entree retenues (toutes celles disponibles avant course)
P["log_drv_top4"] = np.log1p(P["drv_prior_top4"]); P["log_trn_top4"] = np.log1p(P["trn_prior_top4"])
P["log_montant"] = np.log(P["montant"])
for c in ["record_rel", "musique_moy_rel", "log_gains_rel", "age_rel"]:
    P[c] = P[c].fillna(0)
for c in ["musique_derniere", "presse_rang_moy"]:
    P[c] = P[c].fillna(P[c].median())
P["desaccord_presse"] = P["desaccord_presse"] - P.groupby("race_id")["desaccord_presse"].transform("mean")
lp_c = P["log_p_impl"] - P["log_p_impl"].mean()
for c, v in {"partants": P["partants"], "log_montant": P["log_montant"], "distance": P["distance"] / 100,
             "femelles_course": P["femelles_course"], "age_max_course": P["age_max_course"]}.items():
    P[f"cote_x_{c}"] = lp_c * (v - v.mean())

BLOCS = {
    "Marche (cote)": {"log_p_impl": "cote Paris-Turf (log proba implicite)", "desaccord_presse": "desaccord Paris-Turf vs Tierce Magazine"},
    "Consensus presse": {"presse_part_cite": "part des journaux qui le citent", "presse_part_1er": "part des journaux qui le mettent 1er",
                         "presse_rang_moy": "rang moyen dans les pronostics", "cl_favoris_score": "classement 'favoris'",
                         "cl_forme": "classement 'forme'", "cl_classe": "classement 'classe'", "cl_progres": "classement 'progres'",
                         "cl_regularite": "classement 'regularite'", "apt_outsider": "etiquette 'outsider'",
                         "apt_gros_outsider": "etiquette 'gros outsider'", "apt_seconde_chance": "etiquette 'seconde chance'"},
    "Forme / performance": {"record_rel": "record km (relatif au lot)", "musique_moy_rel": "place moyenne 5 dernieres (relatif)",
                            "musique_derniere": "derniere place", "musique_top4": "nb de top 4 sur 5 dernieres",
                            "musique_victoires": "nb de victoires sur 5", "musique_dq": "nb disqualifications/arrets sur 5",
                            "log_gains_rel": "gains (log, relatif)"},
    "Profil cheval": {"age_rel": "age (relatif)", "male": "male (h/m)", "recul": "recul 25 m", "numero": "numero de depart"},
    "Entourage": {"log_drv_top4": "driver : top 4 anterieurs (log)", "log_trn_top4": "entraineur : top 4 anterieurs (log)",
                  "driver_entraineur": "driver = entraineur", "entourage_en_forme": "entourage cite 'en forme'"},
    "Configuration x cote": {"cote_x_partants": "cote x nb de partants", "cote_x_log_montant": "cote x allocation",
                             "cote_x_distance": "cote x distance", "cote_x_femelles_course": "cote x course de femelles",
                             "cote_x_age_max_course": "cote x age max de la course"},
}
LABEL = {c: l for b in BLOCS.values() for c, l in b.items()}
BLOC_OF = {c: b for b, d in BLOCS.items() for c in d}
ALL = list(LABEL)
SIGN = {"log_p_impl": 1, "presse_part_cite": 1, "presse_part_1er": 1, "presse_rang_moy": -1, "cl_favoris_score": 1,
        "record_rel": -1, "musique_moy_rel": -1, "musique_derniere": -1, "musique_top4": 1, "musique_victoires": 1,
        "musique_dq": -1, "log_gains_rel": 1, "recul": -1, "log_drv_top4": 1, "log_trn_top4": 1, "apt_gros_outsider": -1}
mu, sd = P[ALL].mean(), P[ALL].std().replace(0, 1)
Z = (P[ALL] - mu) / sd
binary = [c for c in ALL if P[c].nunique() <= 2]
Z[binary] = P[binary]  # indicatrices laissees en 0/1

# ------------------------------------------------------------ logit ordonne eclate (Plackett-Luce) a K places
def stages(df, K=4):
    """liste de (indices des chevaux encore en lice, index du cheval choisi) pour les places 1..K."""
    out = []
    for rid, g in df.groupby("race_id"):
        idx = g.index.values; pos = g["position"].values
        alive = np.ones(len(idx), bool)
        for k in range(1, K + 1):
            w = np.where(pos == k)[0]
            if len(w) != 1: break
            out.append((rid, idx[alive], idx[w[0]], k)); alive[w[0]] = False
    return out

def fit(df, cols, lam=0.0, K=4, discount=None):
    X = Z.loc[df.index, cols].values; pos_of = {ix: i for i, ix in enumerate(df.index)}
    st = [(np.array([pos_of[a] for a in s]), pos_of[c], k) for _, s, c, k in stages(df, K)]
    wts = np.array([1.0 if discount is None else discount ** (k - 1) for *_, k in st])
    def nll(b):
        f, g = 0.0, np.zeros(len(b))
        u = X @ b
        for (s, c, k), w in zip(st, wts):
            us = u[s]; lse = logsumexp(us); p = np.exp(us - lse)
            f -= w * (u[c] - lse); g -= w * (X[c] - p @ X[s])
        return f + lam * b @ b, g + 2 * lam * b
    r = minimize(nll, np.zeros(len(cols)), jac=True, method="L-BFGS-B")
    b = r.x
    Hm = np.zeros((len(b), len(b))); u = X @ b
    for (s, c, k), w in zip(st, wts):
        p = np.exp(u[s] - logsumexp(u[s])); Xs = X[s]; m = p @ Xs
        Hm += w * ((Xs * p[:, None]).T @ Xs - np.outer(m, m))
    Hm += 2 * lam * np.eye(len(b))
    se = np.sqrt(np.diag(np.linalg.pinv(Hm)))
    return dict(b=b, se=se, ll=-(r.fun - lam * b @ b), cols=cols)

def evaluate(df, model, K=4):
    """par course : logL de l'ordre des 4 premiers, nb de top 4 trouves dans les 4 premiers predits, AUC top4."""
    cols = model["cols"]; u_all = Z.loc[df.index, cols].values @ model["b"] if cols else np.zeros(len(df))
    u_all = pd.Series(u_all, index=df.index)
    rows = []
    for rid, g in df.groupby("race_id"):
        u = u_all[g.index].values; pos = g["position"].values
        ll, alive = 0.0, np.ones(len(g), bool)
        for k in range(1, K + 1):
            w = np.where(pos == k)[0][0]
            ll += u[w] - logsumexp(u[alive]); alive[w] = False
        pred4 = np.argsort(-u)[:4]; y = g["top4"].values
        auc = stats.mannwhitneyu(u[y == 1], u[y == 0]).statistic / (y.sum() * (1 - y).sum())
        rows.append(dict(race_id=rid, ll=ll, hits=y[pred4].sum(), auc=auc, n=len(g)))
    return pd.DataFrame(rows)

def evaluate_raw(df):
    """reference : la cote brute Paris-Turf utilisee telle quelle (sans estimation)."""
    m = {"cols": ["log_p_impl"], "b": np.array([P["log_p_impl"].std()])}  # u = log p (Z * sd)
    return evaluate(df, m)

race_order = P.drop_duplicates("race_id").sort_values(["date", "race_id"]).race_id.tolist()
SCREEN, VALID = race_order[:20], race_order[20:]
Ps, Pv = P[P.race_id.isin(SCREEN)], P[P.race_id.isin(VALID)]
rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))

say("# DONNEES")
say(f"40 courses a lot complet, {len(P)} partants, {int(P.top4.sum())} chevaux dans les 4 premiers, {len(ALL)} donnees d'entree en {len(BLOCS)} blocs")
say(f"criblage : {len(SCREEN)} courses ({Ps.date.min()} -> {Ps.date.max()}) | validation : {len(VALID)} courses ({Pv.date.min()} -> {Pv.date.max()})")
say(f"hasard : {4*4/P.groupby('race_id').size().mean():.2f} top 4 trouves sur 4 en moyenne")

# ------------------------------------------------------------ descriptif : poids brut de la cote sur le top 4
say("\n# DESCRIPTIF - taux de top 4 selon le rang de cote presse (40 courses)")
P["rang_bin"] = pd.cut(P["rang_cote"], [0, 1, 2, 3, 4, 6, 9, 20], labels=["1", "2", "3", "4", "5-6", "7-9", "10+"])
d = P.groupby("rang_bin").agg(n=("top4", "size"), top4=("top4", "mean"), victoire=("win", "mean"), p_impl=("p_impl", "mean"))
say(d.round(2).to_string())

# ------------------------------------------------------------ PHASE 1 : criblage (20 courses), chaque facteur seul puis ajuste sur la cote
say("\n# PHASE 1 - CRIBLAGE sur 20 courses (Plackett-Luce, places 1 a 4)")
base_s = fit(Ps, ["log_p_impl"])
rows = []
for c in ALL:
    m1 = fit(Ps, [c]); b1, p1 = m1["b"][0], 2 * stats.norm.sf(abs(m1["b"][0] / m1["se"][0]))
    if c != "log_p_impl":
        m2 = fit(Ps, ["log_p_impl", c]); b2 = m2["b"][1]; LR = 2 * (m2["ll"] - base_s["ll"]); p2 = stats.chi2.sf(max(LR, 0), 1)
    else:
        b2 = p2 = np.nan
    rows.append(dict(bloc=BLOC_OF[c], donnee=LABEL[c], col=c, coef_seul=b1, p_seul=p1, coef_ajuste=b2, p_ajuste=p2))
S1 = pd.DataFrame(rows)
m = S1.p_ajuste.notna(); S1.loc[m, "p_ajuste_holm"] = multipletests(S1.loc[m, "p_ajuste"], method="holm")[1]
def keep(r):
    s = r.coef_ajuste if not np.isnan(r.coef_ajuste) else r.coef_seul
    ok = SIGN.get(r.col) is None or np.sign(s) == SIGN[r.col]
    return bool(((r.p_ajuste < 0.20) if not np.isnan(r.p_ajuste) else r.p_seul < 0.20) and ok)
S1["retenu"] = S1.apply(keep, axis=1)
say(S1[["bloc", "donnee", "coef_seul", "p_seul", "coef_ajuste", "p_ajuste", "p_ajuste_holm", "retenu"]].round(3).to_string(index=False))
kept = [c for c in S1[S1.retenu].col if c != "log_p_impl"]

# ------------------------------------------------------------ PHASE 2 : modeles candidats
say("\n# PHASE 2 - MODELES CANDIDATS (ajustes sur le criblage)")
# lambda ridge par validation croisee interne (5 plis de courses) sur le criblage
def cv_lam(df, cols, lams, folds=5):
    ids = np.array(sorted(df.race_id.unique())); rng.shuffle(ids); parts = np.array_split(ids, folds)
    best = None
    for lam in lams:
        tot = 0
        for f in parts:
            tr, te = df[~df.race_id.isin(f)], df[df.race_id.isin(f)]
            tot += evaluate(te, fit(tr, cols, lam)).ll.sum()
        if best is None or tot > best[1]: best = (lam, tot)
    return best[0]
lam_all = cv_lam(Ps, ALL, [1, 3, 10, 30, 100])
lam_kept = cv_lam(Ps, ["log_p_impl"] + kept, [0.3, 1, 3, 10, 30]) if kept else 0
presse_cols = ["log_p_impl"] + [c for c in BLOCS["Consensus presse"]]
lam_presse = cv_lam(Ps, presse_cols, [1, 3, 10, 30, 100])
CANDS = {
    "M0 cote seule (recalibree)": (["log_p_impl"], 0),
    "M1 cote + facteurs retenus (ridge)": (["log_p_impl"] + kept, lam_kept),
    "M2 cote + consensus presse (ridge)": (presse_cols, lam_presse),
    "M3 toutes les donnees (ridge)": (ALL, lam_all),
    "M4 sans cote : forme + profil + entourage (ridge)": ([c for b in ["Forme / performance", "Profil cheval", "Entourage"] for c in BLOCS[b]], lam_all),
}
fits = {}
for k, (cols, lam) in CANDS.items():
    fits[k] = fit(Ps, cols, lam)
    say(f"{k}: {len(cols)} variables, lambda={lam}, logL criblage={fits[k]['ll']:.1f}")

# ------------------------------------------------------------ PHASE 3 : validation hors echantillon
say("\n# PHASE 3 - VALIDATION sur les 20 courses suivantes (coefficients figes)")
res = {"Hasard": evaluate(Pv, {"cols": [], "b": np.array([])}), "Cote brute Paris-Turf": evaluate_raw(Pv)}
for k, m in fits.items(): res[k] = evaluate(Pv, m)
say(pd.DataFrame([dict(modele=k, logL_ordre4=d.ll.mean(), top4_trouves_sur4=d.hits.mean(), AUC_top4=d.auc.mean())
                  for k, d in res.items()]).round(3).to_string(index=False))
ref = res["Cote brute Paris-Turf"].set_index("race_id")
for k in fits:
    dd = res[k].set_index("race_id")
    dl, dh = (dd.ll - ref.ll).values, (dd.hits - ref.hits).values
    bs = [rng.choice(dl, len(dl)).mean() for _ in range(5000)]
    say(f"{k} vs cote brute : logL {dl.mean():+.3f}/course (IC95 {np.percentile(bs,2.5):+.3f} a {np.percentile(bs,97.5):+.3f}), "
        f"Wilcoxon p={stats.wilcoxon(dl).pvalue:.3f} ; top 4 trouves {dh.mean():+.2f}/course")

# ------------------------------------------------------------ PHASE 4 : population complete (40 courses)
say("\n# PHASE 4 - POPULATION COMPLETE (40 courses)")
full0 = fit(P, ["log_p_impl"])
b = full0["b"][0] / P.log_p_impl.std(); se = full0["se"][0] / P.log_p_impl.std()
say(f"Cote seule : coefficient brut {b:.2f} (IC95 {b-1.96*se:.2f}-{b+1.96*se:.2f}) ; 1 = cote juste, >1 = favoris sous-cotes")
lr = []
for c in ALL[1:]:
    m2 = fit(P, ["log_p_impl", c]); LR = 2 * (m2["ll"] - full0["ll"])
    lr.append(dict(bloc=BLOC_OF[c], donnee=LABEL[c], coef_z=m2["b"][1], IC95_bas=m2["b"][1] - 1.96 * m2["se"][1],
                   IC95_haut=m2["b"][1] + 1.96 * m2["se"][1], LR=LR, p=stats.chi2.sf(max(LR, 0), 1)))
LRt = pd.DataFrame(lr); LRt["p_holm"] = multipletests(LRt.p, method="holm")[1]
say("Apport de chaque donnee AU-DELA de la cote (test du rapport de vraisemblance, 1 ddl) :")
say(LRt.sort_values("p").round(3).to_string(index=False))
# donnees seules (sans la cote) : poids brut
say("\nPoids brut de chaque donnee SEULE (sans la cote), coefficient par ecart-type :")
sl = []
for c in ALL:
    m1 = fit(P, [c]); sl.append(dict(bloc=BLOC_OF[c], donnee=LABEL[c], coef_z=m1["b"][0], p=2 * stats.norm.sf(abs(m1["b"][0] / m1["se"][0]))))
SL = pd.DataFrame(sl); SL["p_holm"] = multipletests(SL.p, method="holm")[1]
say(SL.reindex(SL.coef_z.abs().sort_values(ascending=False).index).round(3).to_string(index=False))

# ------------------------------------------------------------ influence : validation croisee par course (40 plis)
say("\n# INFLUENCE - validation croisee leave-one-race-out (40 courses)")
def loo(cols, lam):
    out = []
    for rid in race_order:
        tr, te = P[P.race_id != rid], P[P.race_id == rid]
        out.append(evaluate(te, fit(tr, cols, lam)).iloc[0])
    return pd.DataFrame(out)
base_raw = evaluate_raw(P)
L = {"Cote brute": base_raw, "M0 cote seule": loo(["log_p_impl"], 0)}
lam_full = cv_lam(P, ALL, [3, 10, 30, 100])
L["M3 toutes les donnees (ridge)"] = loo(ALL, lam_full)
for bname, bcols in BLOCS.items():
    if bname == "Marche (cote)": continue
    L[f"cote + {bname}"] = loo(["log_p_impl"] + list(bcols), lam_full)
say(pd.DataFrame([dict(modele=k, logL_ordre4=d.ll.mean(), top4_trouves_sur4=d.hits.mean(), AUC_top4=d.auc.mean())
                  for k, d in L.items()]).round(3).to_string(index=False))
say(f"(lambda ridge choisi par validation croisee : {lam_full})")
# influence par bloc retire du modele complet
say("\nPerte quand on retire un bloc du modele complet (logL ordre 4 par course, LOO) :")
fullL = L["M3 toutes les donnees (ridge)"].ll.mean()
for bname, bcols in BLOCS.items():
    cols = [c for c in ALL if c not in bcols]
    d = loo(cols, lam_full)
    say(f"  sans {bname:22s}: {d.ll.mean() - fullL:+.3f} (negatif = le bloc apporte de l'information)")
mfull = fit(P, ALL, lam_full)
say("\nCoefficients du modele complet ridge (40 courses), par ecart-type, tries par valeur absolue :")
co = pd.DataFrame(dict(bloc=[BLOC_OF[c] for c in ALL], donnee=[LABEL[c] for c in ALL], coef=mfull["b"]))
say(co.reindex(co.coef.abs().sort_values(ascending=False).index).round(3).to_string(index=False))

say("\n# SENSIBILITE : poids decroissant des places basses (Benter : 2e-4e place plus bruitees)")
for disc in [1.0, 0.8, 0.6]:
    m = fit(P, ["log_p_impl"], 0, discount=disc)
    say(f"  ponderation {disc} par place : coef cote z = {m['b'][0]:.2f}")

open(f"{D}/rapport_top4.txt", "w").write("\n".join(rep))
S1.to_csv(f"{D}/criblage_top4.csv", index=False); LRt.to_csv(f"{D}/apport_au_dela_cote_top4.csv", index=False)
print("\n".join(rep))
