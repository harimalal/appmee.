"""Vitesse de fin mesuree sur les courses PRECEDENTES (letrot.com) : apport au-dela de la cote PMU finale.
Usage : python3 -I vitesse_fin.py <dossier_data>
"""
import sys, json, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests
warnings.filterwarnings("ignore")
D = sys.argv[1]
M = pd.read_csv(f"{D}/partants_letrot_merge.csv")
prev = pd.DataFrame(json.load(open(f"{D}/courses_precedentes.json")), columns=["race_id", "numero", "horse_id", "anciennete", "key"])
R = [json.loads(l) for l in open(f"{D}/temps_precedents.jsonl")]
rows = []
for r in R:
    t = pd.DataFrame(r["runners"])
    if t.empty or t.last500.notna().sum() < 4: continue
    med5, med10 = t.last500.median(), t.last1000.median()
    for _, x in t.iterrows():
        rows.append(dict(key=r["key"], horse_id=x.horse_id, d500=x.last500 - med5 if pd.notna(x.last500) else np.nan,
                         d1000=x.last1000 - med10 if pd.notna(x.last1000) else np.nan,
                         accel=(x.r1000_500 - x.last500) if pd.notna(x.r1000_500) and pd.notna(x.last500) else np.nan,
                         cl500=x.cl_1000_500, n_tr=len(t), rang_prev=x.rang))
T = pd.DataFrame(rows)
J = prev.merge(T, on=["key", "horse_id"], how="inner")
A = J.groupby(["race_id", "numero"]).agg(d500=("d500", "mean"), d500_best=("d500", "min"), d1000=("d1000", "mean"), accel=("accel", "mean"),
                                         n_prev=("d500", "count"), d500_last=("d500", "first")).reset_index()
M = M.merge(A, on=["race_id", "numero"], how="left")
rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))
pages = len(R); avec = sum(1 for r in R if r["runners"])
say(f"# DONNEES : {pages} courses precedentes lues, {avec} avec temps de passage ; partants avec au moins 1 temps anterieur : {M.d500.notna().sum()}/{len(M)}")
say("d500 = ecart (s/km) entre le dernier 500 m du cheval et la mediane du peloton, moyenne de ses 3 dernieres courses chronometrees. Negatif = finit plus vite que le peloton.")
# relatif au lot (seulement parmi les chevaux mesures) ; manquant -> 0 + indicateur
for c in ["d500", "d500_best", "d1000", "accel"]:
    M[c + "_rel"] = M[c] - M.groupby("race_id")[c].transform("mean")
    M[c + "_rang"] = M.groupby("race_id")[c].rank(method="min")
M["mesure"] = M.d500.notna().astype(int)
off = np.log(M.p3_pmu / (1 - M.p3_pmu))
say(f"Lien avec la cote : Spearman(d500, cote PMU) = {stats.spearmanr(M.d500, M.cote_pmu, nan_policy='omit')[0]:+.2f} (positif = la cote integre deja la vitesse de fin)")

say("\n# 1. TAUX D'ARRIVEE SELON LE RANG 'VITESSE DE FIN' DANS LE LOT (chevaux mesures ; 1 = meilleur finisseur)")
S = M[M.mesure == 1].copy()
S["bin"] = pd.cut(S.d500_rang, [0, 1, 2, 3, 5, 8, 20], labels=["1", "2", "3", "4-5", "6-8", "9+"])
say(S.groupby("bin").agg(n=("top3", "size"), victoire=("win", "mean"), top3=("top3", "mean"), top3_attendu=("p3_pmu", "mean"),
                         top4=("top4", "mean"), cote_med=("cote_pmu", "median")).round(2).to_string())

say("\n# 2. EFFET AU-DELA DE LA COTE PMU (logit avec la cote en offset, place dans les 3, chevaux mesures)")
rows = []
offS = off[S.index]
for col, lab in [("d500_rel", "dernier 500 m (moyenne, relatif au lot)"), ("d500_best_rel", "dernier 500 m (meilleur des 3)"),
                 ("d1000_rel", "dernier 1000 m (relatif au lot)"), ("accel_rel", "acceleration 1000-500 -> 500-0 (relatif)"),
                 ("d500_last", "dernier 500 m de la derniere course")]:
    d = S[[col, "top3"]].dropna(); o = offS[d.index]
    if len(d) < 30 or d[col].std() == 0: continue
    x = (d[col] - d[col].mean()) / d[col].std()
    m = sm.GLM(d.top3, sm.add_constant(x), family=sm.families.Binomial(), offset=o).fit()
    rows.append(dict(mesure=lab, chevaux=len(d), odds_ratio_par_ecart_type=np.exp(m.params.iloc[1]), p=m.pvalues.iloc[1]))
for col, lab in [("d500_rang", "meilleur finisseur du lot (rang 1)"), ("d500_rang", "dans les 3 meilleurs finisseurs")]:
    x = (S[col] <= (1 if "rang 1" in lab else 3)).astype(float)
    m = sm.GLM(S.top3, sm.add_constant(x), family=sm.families.Binomial(), offset=offS).fit()
    sub = S[x == 1]
    rows.append(dict(mesure=lab, chevaux=len(sub), odds_ratio_par_ecart_type=np.exp(m.params.iloc[1]), p=m.pvalues.iloc[1],
                     places=int(sub.top3.sum()), attendu=round(sub.p3_pmu.sum(), 1)))
Tb = pd.DataFrame(rows); Tb["p_holm"] = multipletests(Tb.p, method="holm")[1]
say(Tb.round(3).to_string(index=False))
say("(odds ratio < 1 pour une mesure en secondes = plus rapide en fin de course -> plus de chances au-dela de la cote)")

say("\n# 3. STABILITE : meilleurs finisseurs (3 premiers du lot) par moitie de periode et par statut")
order = M.drop_duplicates("race_id").sort_values(["date", "race_id"]).race_id.tolist()
S["moitie"] = np.where(S.race_id.isin(order[:20]), "courses 1-20", "courses 21-40")
S["statut"] = np.where(S.rang_pmu <= 3, "3 premieres cotes", "non-favoris")
B = S[S.d500_rang <= 3]
say(B.groupby(["moitie"]).agg(n=("top3", "size"), places=("top3", "sum"), attendu=("p3_pmu", "sum")).round(1).to_string())
say(B.groupby(["statut"]).agg(n=("top3", "size"), places=("top3", "sum"), attendu=("p3_pmu", "sum"), gagnants=("win", "sum")).round(1).to_string())

say("\n# 4. PARIS SIMULES (1 euro) : gagnant = cote PMU, place = bareme de Hari (bas/moyen/haut)")
BAR = [(5, (1.5, 2.0)), (10, (1.8, 2.5)), (15, (2.5, 3.5)), (20, (3.0, 4.25)), (np.inf, (3.5, 5.0))]
def rapport(c, s):
    for lim, (lo, hi) in BAR:
        if c < lim: return {"bas": lo, "moyen": (lo + hi) / 2, "haut": hi}[s]
def sim(d, lab):
    n = len(d)
    if n == 0: return
    g = (d.win * d.cote_pmu).sum() / n - 1
    pl = [(d.top3 * d.cote_pmu.map(lambda c: rapport(c, s))).sum() / n - 1 for s in ["bas", "moyen", "haut"]]
    say(f"  {lab:62s}: {n:3d} paris | gagnant {g:+.0%} ({int(d.win.sum())}) | place {pl[0]:+.0%}/{pl[1]:+.0%}/{pl[2]:+.0%} ({int(d.top3.sum())} places)")
sim(S[S.d500_rang == 1], "Meilleur finisseur du lot")
sim(S[(S.d500_rang <= 3) & (S.rang_pmu >= 4)], "Non-favori (4e cote et +) parmi les 3 meilleurs finisseurs")
sim(S[(S.d500_rang <= 3) & (S.rang_pmu >= 4) & (S.cote_pmu <= 20)], "  ... et cote <= 20")
sim(S[(S.rang_pmu == 1) & (S.d500_rang <= 3)], "Favori PMU ET parmi les 3 meilleurs finisseurs")
sim(S[(S.rang_pmu == 1) & (S.d500_rang > 3)], "Favori PMU mais PAS parmi les 3 meilleurs finisseurs")
sim(M[(M.rang_pmu == 1) & (M.avis_entraineur != 1)], "Rappel regle 24 : favori PMU sans avis favorable")
sim(S[(S.rang_pmu == 1) & (S.avis_entraineur != 1) & (S.d500_rang <= 3)], "Favori sans avis favorable ET bon finisseur")
say("\nNB : plusieurs strategies testees sur 40 courses -> resultats a confirmer.")
open(f"{D}/rapport_vitesse_fin.txt", "w").write("\n".join(rep)); print("\n".join(rep))
