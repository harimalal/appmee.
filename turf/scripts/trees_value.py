"""Approche 1 : arbres (foret aleatoire, gradient boosting, arbre court) sur le top 4.
Approche 3 : valeur - paris gagnant simules (decision : proba modele x cote presse ; gain : cote PMU reelle du gagnant).
Toutes les predictions sont hors echantillon (la course predite n'est jamais dans l'entrainement).
Usage : python3 -I trees_value.py <dossier_data>
"""
import sys, warnings
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.linear_model import LogisticRegression
from scipy import stats
warnings.filterwarnings("ignore")
D = sys.argv[1]
P = pd.read_csv(f"{D}/partants_top4.csv").reset_index(drop=True)
rng = np.random.default_rng(11)

P["log_drv_top4"] = np.log1p(P["drv_prior_top4"]); P["log_trn_top4"] = np.log1p(P["trn_prior_top4"])
P["log_montant"] = np.log(P["montant"])
P["desaccord_presse"] = P["desaccord_presse"] - P.groupby("race_id")["desaccord_presse"].transform("mean")
for c in ["record_rel", "musique_moy_rel", "log_gains_rel", "age_rel"]: P[c] = P[c].fillna(0)
for c in ["musique_derniere", "presse_rang_moy"]: P[c] = P[c].fillna(P[c].median())

FEATS = {
    "log_p_impl": "cote presse (proba implicite)", "rang_cote": "rang de cote dans la course",
    "desaccord_presse": "desaccord Paris-Turf / Tierce Mag.",
    "presse_part_cite": "part des journaux qui le citent", "presse_part_1er": "part des journaux qui le mettent 1er",
    "presse_rang_moy": "rang moyen dans les pronostics", "cl_favoris_score": "classement presse 'favoris'",
    "cl_forme": "classement presse 'forme'", "cl_classe": "classement presse 'classe'", "cl_progres": "classement presse 'progres'",
    "cl_regularite": "classement presse 'regularite'", "apt_outsider": "etiquette 'outsider'",
    "apt_gros_outsider": "etiquette 'gros outsider'", "apt_seconde_chance": "etiquette 'seconde chance'",
    "record_rel": "record km (relatif au lot)", "musique_moy_rel": "place moyenne 5 dernieres (relatif)",
    "musique_derniere": "derniere place", "musique_top4": "nb de top 4 sur 5", "musique_victoires": "nb de victoires sur 5",
    "musique_dq": "disqualifications/arrets sur 5", "log_gains_rel": "gains (relatif)",
    "age_rel": "age (relatif)", "male": "male", "recul": "recul 25 m", "numero": "numero de depart",
    "log_drv_top4": "driver : top 4 anterieurs", "log_trn_top4": "entraineur : top 4 anterieurs",
    "driver_entraineur": "driver = entraineur", "entourage_en_forme": "entourage 'en forme'",
    "partants": "nb de partants", "log_montant": "allocation", "distance": "distance",
    "femelles_course": "course de femelles", "age_max_course": "age max de la course",
}
ODDS = ["log_p_impl", "rang_cote", "desaccord_presse"]
PRESSE = ["presse_part_cite", "presse_part_1er", "presse_rang_moy", "cl_favoris_score", "cl_forme", "cl_classe",
          "cl_progres", "cl_regularite", "apt_outsider", "apt_gros_outsider", "apt_seconde_chance"]
ALL = list(FEATS)
NO_MARKET = [c for c in ALL if c not in ODDS + PRESSE]
races = P.drop_duplicates("race_id").sort_values(["date", "race_id"]).race_id.tolist()

def make(kind):
    if kind == "rf":  return RandomForestClassifier(n_estimators=400, min_samples_leaf=10, max_features="sqrt", random_state=0, n_jobs=-1)
    if kind == "gb3": return HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=150, min_samples_leaf=20, l2_regularization=1.0, random_state=0)
    if kind == "gb1": return HistGradientBoostingClassifier(max_depth=1, learning_rate=0.05, max_iter=150, min_samples_leaf=20, l2_regularization=1.0, random_state=0)
    if kind == "tree": return DecisionTreeClassifier(max_depth=3, min_samples_leaf=30, random_state=0)
    if kind == "logit": return LogisticRegression(C=0.3, max_iter=2000)

def oof(kind, cols, target, folds):
    """predictions hors echantillon ; folds = liste de listes de courses de test."""
    pred = pd.Series(np.nan, index=P.index); models = []
    for test in folds:
        tr, te = ~P.race_id.isin(test), P.race_id.isin(test)
        m = make(kind).fit(P.loc[tr, cols], P.loc[tr, target])
        pred[te] = m.predict_proba(P.loc[te, cols])[:, 1]; models.append((test, m))
    return pred, models

def score(pred, target="top4", k=4):
    rows = []
    for rid, g in P.groupby("race_id"):
        s = pred[g.index].values; y = g[target].values
        top = np.argsort(-s)[:k]
        auc = stats.mannwhitneyu(s[y == 1], s[y == 0]).statistic / (y.sum() * (1 - y).sum())
        rows.append(dict(hits=y[top].sum(), auc=auc))
    d = pd.DataFrame(rows); return d.hits.mean(), d.auc.mean(), d

rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))
LOO = [[r] for r in races]
CHRONO = [races[20:]]  # entrainement sur les 20 premieres, test sur les 20 suivantes

# ======================================================================= APPROCHE 1 : ARBRES
say("# APPROCHE 1 - ARBRES DE DECISION (cible : finir dans les 4 premiers)")
say(f"40 courses, {len(P)} partants, {len(ALL)} donnees d'entree. Hasard = {4*4/P.groupby('race_id').size().mean():.2f} top 4 trouves sur 4.")
base = -P["rang_cote"].astype(float)
h, a, d_base = score(base)
say(f"\nReference cote presse (on prend les 4 premiers de la cote) : {h:.2f} top 4 trouves / 4, AUC {a:.3f}")
cands = {
    "Foret aleatoire, toutes donnees": ("rf", ALL), "Gradient boosting profondeur 3 (interactions), toutes": ("gb3", ALL),
    "Gradient boosting profondeur 1 (sans interaction), toutes": ("gb1", ALL),
    "Foret aleatoire SANS cote ni presse": ("rf", NO_MARKET), "Arbre court (3 niveaux), toutes": ("tree", ALL),
    "Logistique penalisee, toutes (reference lineaire)": ("logit", ALL),
}
OOF = {}
tab = []
for name, (kind, cols) in cands.items():
    p_loo, _ = oof(kind, cols, "top4", LOO); OOF[name] = p_loo
    h1, a1, dd = score(p_loo)
    p_ch, _ = oof(kind, cols, "top4", CHRONO); sub = P.race_id.isin(races[20:])
    hh = []; aa = []
    for rid, g in P[sub].groupby("race_id"):
        s = p_ch[g.index].values; y = g.top4.values; hh.append(y[np.argsort(-s)[:4]].sum())
        aa.append(stats.mannwhitneyu(s[y == 1], s[y == 0]).statistic / (y.sum() * (1 - y).sum()))
    diff = dd.hits.values - d_base.hits.values
    w = stats.wilcoxon(diff).pvalue if np.any(diff != 0) else 1.0
    tab.append(dict(modele=name, top4_LOO=h1, AUC_LOO=a1, top4_chrono=np.mean(hh), AUC_chrono=np.mean(aa),
                    vs_cote=f"{diff.mean():+.2f} (p={w:.2f})"))
bh = [d_base.hits[i] for i, r in enumerate(sorted(P.race_id.unique())) if r in races[20:]]
say(pd.DataFrame(tab).round(3).to_string(index=False))
say(f"(colonne chrono = entraine sur les 20 premieres courses, teste sur les 20 suivantes ; cote presse sur ces 20 : {np.mean(bh):.2f})")

# importance par permutation (LOO, permutation a l'interieur de la course testee)
say("\n# IMPORTANCE DES FACTEURS (foret aleatoire, permutation hors echantillon)")
say("Baisse de l'AUC quand on melange le facteur : grande baisse = facteur utilise par le modele.")
_, models = oof("rf", ALL, "top4", LOO)
imp = {c: [] for c in ALL}
for (test, m) in models:
    te = P[P.race_id.isin(test)]; y = te.top4.values
    def auc(s): return stats.mannwhitneyu(s[y == 1], s[y == 0]).statistic / (y.sum() * (1 - y).sum())
    a0 = auc(m.predict_proba(te[ALL])[:, 1])
    for c in ALL:
        for _ in range(5):
            X = te[ALL].copy(); X[c] = rng.permutation(X[c].values)
            imp[c].append(a0 - auc(m.predict_proba(X)[:, 1]))
I = pd.DataFrame([dict(facteur=FEATS[c], baisse_AUC=np.mean(v), IC95=1.96 * np.std(v) / np.sqrt(len(v) / 5)) for c, v in imp.items()])
I["signal"] = np.where(I.baisse_AUC - I.IC95 > 0, "oui", "non")
say(I.sort_values("baisse_AUC", ascending=False).round(4).to_string(index=False))
# importance par blocs (on melange tout le bloc d'un coup)
say("\nImportance par bloc (bloc melange en entier) :")
BLOCS = {"cote": ODDS, "consensus presse": PRESSE,
         "forme": ["record_rel", "musique_moy_rel", "musique_derniere", "musique_top4", "musique_victoires", "musique_dq", "log_gains_rel"],
         "profil cheval": ["age_rel", "male", "recul", "numero"],
         "entourage": ["log_drv_top4", "log_trn_top4", "driver_entraineur", "entourage_en_forme"],
         "configuration course": ["partants", "log_montant", "distance", "femelles_course", "age_max_course"]}
for b, cols in BLOCS.items():
    v = []
    for (test, m) in models:
        te = P[P.race_id.isin(test)]; y = te.top4.values
        auc = lambda s: stats.mannwhitneyu(s[y == 1], s[y == 0]).statistic / (y.sum() * (1 - y).sum())
        a0 = auc(m.predict_proba(te[ALL])[:, 1])
        for _ in range(5):
            X = te[ALL].copy(); perm = rng.permutation(len(X))
            X[cols] = X[cols].values[perm]
            v.append(a0 - auc(m.predict_proba(X)[:, 1]))
    say(f"  {b:22s} baisse AUC = {np.mean(v):+.4f} (IC95 +/- {1.96*np.std(v)/np.sqrt(len(v)/5):.4f})")

# regles lisibles : arbre court sur toutes les courses
say("\n# REGLES LISIBLES - arbre a 3 niveaux sur les 40 courses (description, pas une preuve)")
t = make("tree").fit(P[ALL], P["top4"])
txt = export_text(t, feature_names=[FEATS[c] for c in ALL], show_weights=True, decimals=2)
say(txt)
say("Lecture : weights = [nb hors top 4, nb dans le top 4] dans chaque feuille.")

# interactions : profondeur 3 vs profondeur 1
say("Interactions : si le boosting profondeur 3 ne fait pas mieux que la profondeur 1, aucune interaction utile n'est detectee.")

# ======================================================================= APPROCHE 3 : VALEUR
say("\n# APPROCHE 3 - VALEUR : paris simules 'simple gagnant' a 1 euro")
say("Decision avant course : proba du modele x cote presse ('esperance') >= seuil. Gain : cote PMU reelle du gagnant (derniere des 3 cotes publiees).")
say("Probabilites de victoire toutes hors echantillon (leave-one-race-out). Rapport PMU suppose 'pour 1 euro, mise incluse'.")
# modele A : cote recalibree (logit conditionnel, 1 parametre) en LOO
from scipy.optimize import minimize_scalar
def fit_beta(df):
    def nll(b):
        s = 0
        for _, g in df.groupby("race_id"):
            u = b * g.log_p_impl.values; u -= u.max()
            s -= u[g.win.values == 1][0] - np.log(np.exp(u).sum())
        return s
    return minimize_scalar(nll, bounds=(0.1, 4), method="bounded").x
pA = pd.Series(np.nan, index=P.index); betas = []
for r in races:
    b = fit_beta(P[P.race_id != r]); betas.append(b)
    g = P[P.race_id == r]; u = b * g.log_p_impl.values; u = np.exp(u - u.max()); pA[g.index] = u / u.sum()
say(f"Modele A 'cote recalibree' : exposant moyen {np.mean(betas):.2f} (>1 = on renforce les favoris)")
# modele B : foret aleatoire victoire, normalisee dans la course
pB_raw, _ = oof("rf", ALL, "win", LOO)
pB = pB_raw / pB_raw.groupby(P.race_id).transform("sum")
pC = (pA + pB) / 2
pPress = P["p_impl"]
pay = P["cote_pmu_final"].fillna(0)  # n'est utilise que si le cheval gagne (cote du gagnant toujours connue)
pay_first = P["race_id"].map(lambda r: np.nan)  # sensibilite : premiere cote publiee
import json  # premiere cote PMU pour le gagnant (sensibilite)
def roi(mask, pay_col):
    bets = P[mask]; n = len(bets)
    if n == 0: return dict(paris=0, gagnants=0, mise=0, retour=0, ROI=np.nan, IC95="")
    gain = (bets.win * pay_col[bets.index]).sum()
    # bootstrap par course
    per = P.assign(bet=mask.astype(int), ret=mask.astype(int) * P.win * pay_col).groupby("race_id")[["bet", "ret"]].sum()
    bs = []
    for _ in range(3000):
        s = per.sample(len(per), replace=True, random_state=int(rng.integers(1e9)))
        bs.append(s.ret.sum() / s.bet.sum() - 1 if s.bet.sum() > 0 else np.nan)
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return dict(paris=n, gagnants=int(bets.win.sum()), mise=n, retour=round(gain, 1), ROI=gain / n - 1, IC95=f"{lo:+.0%} a {hi:+.0%}")
strat = {
    "Tout jouer (tous les partants)": P.index == P.index,
    "Favori presse a chaque course": P.rang_cote == 1,
    "Les 3 premiers de la cote presse": P.rang_cote <= 3,
}
for nameM, pm in [("A cote recalibree", pA), ("B foret aleatoire", pB), ("C moyenne A+B", pC)]:
    for k in [1.0, 1.1, 1.25, 1.5]:
        strat[f"{nameM} : esperance >= {k}"] = (pm * P.cote_presse >= k)
    strat[f"{nameM} : meilleur cheval du modele"] = pm == pm.groupby(P.race_id).transform("max")
rows = []
for n, m in strat.items():
    rows.append(dict(strategie=n, **roi(pd.Series(m, index=P.index), pay)))
V = pd.DataFrame(rows)
say(V.to_string(index=False, formatters={"ROI": lambda x: f"{x:+.0%}" if pd.notna(x) else ""}))
say(f"\nNb de strategies testees : {len(strat)} -> avec autant d'essais, une ou deux peuvent sembler rentables par pur hasard.")

# calibration : la cote presse est-elle trop genereuse avec les outsiders ?
say("\n# CALIBRATION - victoires observees vs probabilite implicite de la cote presse")
P["tranche"] = pd.cut(P.cote_presse, [0, 5, 10, 20, 40, 1000], labels=["<=5", "5-10", "10-20", "20-40", ">40"])
C = P.groupby("tranche").agg(partants=("win", "size"), victoires=("win", "sum"), taux=("win", "mean"), p_implicite=("p_impl", "mean"),
                              cote_pmu_moy_gagnants=("cote_pmu_final", lambda s: s[P.loc[s.index, "win"] == 1].mean()))
C["rendement_si_on_joue_tout"] = P.groupby("tranche").apply(lambda g: (g.win * g.cote_pmu_final.fillna(0)).sum() / len(g) - 1)
say(C.round(3).to_string())

open(f"{D}/rapport_arbres_valeur.txt", "w").write("\n".join(rep))
V.to_csv(f"{D}/valeur_strategies.csv", index=False); I.to_csv(f"{D}/importance_foret.csv", index=False)
print("\n".join(rep))
