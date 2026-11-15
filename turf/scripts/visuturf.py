"""Reconstruction d'un graphique de type Visuturf pour chaque course + test des regles de Hari, sans regarder la cote.
Axe vertical = valeur du cheval (performances sur ses dernieres courses) ; axe horizontal = valeur du jockey (reussite a Vincennes) ;
taille et couleur = forme (tendance : 3 dernieres courses contre les 3 precedentes). Axes = moyennes du lot.
Regles de Hari (fixees avant le test) :
  Q1 le favori (plus petit rang de valeur cheval + jockey, zone verte) est valide s'il est dans l'encart haut-droite, ni trop excentre : on le joue ;
  Q2 un cheval de la zone jaune (bon jockey, cheval moyen) bien au milieu, pas pres des bords ;
  Q3 un cheval de la zone haut-gauche (meilleur cheval, jockey moyen) a la limite du graphique ;
  EXCLUS : zone rouge (cheval et jockey sous la moyenne), chevaux hors graphique (sans historique), chevaux proches de la croisee des axes.
Les donnees sont des courses ANTERIEURES a la course (aucune triche). La cote n'est utilisee qu'APRES, pour juger si la selection bat le marche.
Usage : python3 -I visuturf.py <dossier_data> <dossier_graphiques>
"""
import sys, os, json, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
warnings.filterwarnings("ignore")
D, G = sys.argv[1], sys.argv[2]; os.makedirs(G, exist_ok=True); out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(out[-1])
H = pd.read_csv(f"{D}/partants_ids.csv"); have = {f[:-5] for f in os.listdir(f"{D}/perfs") if f.endswith(".json")}
full = H.groupby("race").horse_id.apply(lambda s: set(s) <= have); H = H[H.race.isin(full[full].index)]
def score(rang, n):
    s = str(rang or "").strip()
    if not s.isdigit(): return 0.0                       # faute / disqualification / arret
    r = int(s)
    if r == 0: return 0.1                                # non place
    return float(np.clip(1 - (r - 1) / max(n - 1, 1), 0, 1))
P = []
for h in {*H.horse_id}:
    for x in json.load(open(f"{D}/perfs/{h}.json")):
        if x.get("speciality") != "A": continue
        P.append(dict(horse=x["id"], date=x["datePerf"][:10], hip=str(x.get("numHippodrome")), s=score(x.get("rang"), x.get("nbPartant") or 12),
                      top3=int(str(x.get("rang") or "").strip().isdigit() and 1 <= int(str(x.get("rang")).strip()) <= 3), driver=x.get("driverId")))
P = pd.DataFrame(P)
V = P[(P.hip == "7500") & P.driver.notna()].sort_values("date")
def shrink(t, n, prior, k): return (t + prior * k) / (n + k)
rows = []
for r in H.itertuples():
    h = P[(P.horse == r.horse_id) & (P.date < r.date)].sort_values("date", ascending=False)
    dv = V[(V.driver == r.driver_id) & (V.date < r.date)]
    w = np.array([6, 5, 4, 3, 2, 1.0])[:min(6, len(h))]
    y = (np.dot(h.head(6).s.values, w) + 0.4 * 2) / (w.sum() + 2) if len(h) else np.nan   # valeur du cheval (performances recentes)
    f = (h.head(3).s.mean() - h.iloc[3:6].s.mean()) if len(h) >= 5 else (0.0 if len(h) else np.nan)   # forme : tendance
    rows.append(dict(race=r.race, numero=r.numero, horse=r.horse_id, y_cheval=y, forme=f, x_jockey=shrink(dv.top3.sum(), len(dv), 0.25, 15), n_hist=len(h), n_drv=len(dv)))
F = pd.DataFrame(rows)
base = pd.concat([pd.read_csv(f"{D}/feat_origine.csv"), pd.read_csv(f"{D}/feat_novembre.csv")]); base = base[(base.discipline == "A") & (base.cote > 0)]
M = base.merge(F, on=["race", "numero"], how="inner").merge(H[["race", "numero", "ech"]], on=["race", "numero"], how="left")
M = M[M.groupby("race").cote.transform("size") >= 6].reset_index(drop=True)
q = 1 / M.cote; M["p"] = q / q.groupby(M.race).transform("sum"); M["lp"] = np.log(M.p); M["pos"] = M.pos.where(M.pos > 0); M["y"] = (M.pos <= 3).astype(int)
M["rang_cote"] = M.groupby("race").cote.rank(method="first")
def z(s): return (s - s.groupby(M.race).transform("mean")) / (s.groupby(M.race).transform("std") + 1e-9)
M["zH"] = z(M.y_cheval.fillna(M.groupby("race").y_cheval.transform("mean"))); M["zJ"] = z(M.x_jockey)
M["hors"] = M.y_cheval.isna() | (M.n_hist < 3)
M["dist_croisee"] = np.sqrt(M.zH ** 2 + M.zJ ** 2)
# --- zones
M["zone"] = np.select([M.zH > 0, ], [np.where(M.zJ > 0, "vert (favoris)", "bleu (meilleurs chevaux)")], default=np.where(M.zJ > 0, "jaune (bons jockeys)", "rouge (outsiders)"))
M.loc[M.hors, "zone"] = "hors graphique"
M["exclu"] = M.hors | ((M.zH <= 0) & (M.zJ <= 0)) | (M.dist_croisee < 0.5)
M["val"] = M.zH + M.zJ                                               # 'valeur' pour reperer le favori du graphique
M["q1"] = (M.zone == "vert (favoris)") & (M.zH.between(0, 2.2)) & (M.zJ.between(0, 2.2)) & ~M.exclu
M["q2"] = (M.zone == "jaune (bons jockeys)") & (M.zJ > 0.3) & (M.zH > -1.0) & ~M.exclu
M["q3"] = (M.zone == "bleu (meilleurs chevaux)") & (M.zH > 0.8) & ~M.exclu
say(f"# {M.race.nunique()} courses completes, {len(M)} partants, historique et jockey calcules AVANT chaque course")
X0 = sm.add_constant(M[["lp"]]); m0 = sm.GLM(M.y, X0, family=sm.families.Binomial()).fit(); M["pe"] = m0.predict(X0)     # attendu par la cote
def ligne(lab, d):
    if len(d) == 0: say(f"  {lab:62s}: aucun cheval"); return
    o, e = d.y.sum(), d.pe.sum(); sims = np.random.default_rng(0).binomial(1, np.tile(d.pe.clip(0, 1).values, (10000, 1))).sum(1)
    pv = min(1, 2 * min((sims >= o).mean(), (sims <= o).mean()))
    say(f"  {lab:62s}: {len(d):4d} chevaux, {int(o):3d} dans les 3 ({o/len(d):.0%}) | attendu par la cote {e:5.1f} ({e/len(d):.0%}) | x{o/e:.2f} p={pv:.2f} | cote mediane {d.cote.median():.1f}")
say("\n# 1. TOUS LES CHEVAUX PAR ZONE (finissent-ils dans les 3 ? et la cote le prevoyait-elle ?)")
for z_, d in M.groupby("zone"): ligne(z_, d)
say("\n# 2. TES REGLES")
ligne("Chevaux EXCLUS (rouge, hors graphique, pres de la croisee des axes)", M[M.exclu])
ligne("Chevaux NON exclus", M[~M.exclu])
ligne("Q1 - zone verte, ni trop excentree", M[M.q1])
ligne("Q2 - zone jaune, bien au milieu (bon jockey, cheval moyen)", M[M.q2])
ligne("Q3 - zone haut-gauche, a la limite (meilleur cheval, jockey moyen)", M[M.q3])
ligne("Q1 + Q2 + Q3 ensemble", M[M.q1 | M.q2 | M.q3])
ligne("... dont chevaux a cote 8 et plus (valeur cachee, pas payee a la cote)", M[(M.q1 | M.q2 | M.q3) & (M.cote >= 8)])
say("\n# 3. LE FAVORI DU GRAPHIQUE (plus grande valeur cheval + jockey, hors exclus), valide ou non")
fav = M[~M.exclu].sort_values("val", ascending=False).groupby("race").head(1)
ligne("Favori du graphique, valide par Q1", fav[fav.q1]); ligne("Favori du graphique, NON valide (excentre / hors zone verte)", fav[~fav.q1])
ligne("Favori du MARCHE (plus petite cote), pour comparer", M[M.rang_cote == 1])
say("\n# 4. PREVOIR LES 3 DE L'ARRIVEE SANS LA COTE : combien des 3 chevaux retenus par le graphique finissent dans les 3 ?")
def top3_picks(df):
    r = []
    for _, g in df.groupby("race"):
        s = g[~g.exclu].sort_values("val", ascending=False).head(3); r.append(s.y.sum())
    return np.array(r)
def cote_picks(df): return np.array([g.sort_values("cote").head(3).y.sum() for _, g in df.groupby("race")])
a, b = top3_picks(M), cote_picks(M); hasard = np.mean([3 * 3 / len(g) for _, g in M.groupby("race")])
d = a - b
say(f"  3 meilleurs du graphique (hors exclus) : {a.mean():.2f} sur 3 | 3 premieres cotes : {b.mean():.2f} sur 3 | hasard : {hasard:.2f} | ecart graphique - cote : {d.mean():+.2f} (p={stats.wilcoxon(d[d != 0]).pvalue if (d != 0).any() else 1:.2f})")
M.to_csv(f"{D}/visuturf_partants.csv", index=False)
# --- graphique d'une course (comme l'outil) : cercle = cheval, couleur/taille = forme, anneau noir = arrive dans les 3 (affiche apres coup)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
def trace(race, fn):
    g = M[M.race == race]; fig, ax = plt.subplots(figsize=(7.2, 7.2), facecolor="#111"); ax.set_facecolor("black")
    ax.axhline(0, color="#d33", lw=1); ax.axvline(0, color="#d33", lw=1)
    ax.fill_between([0, 3.2], 0, 3.2, color="#1b5e20", alpha=.35); ax.fill_between([-3.2, 0], -3.2, 0, color="#8b1a10", alpha=.45)
    ax.fill_between([0, 3.2], -1.0, 0, color="#f9d44a", alpha=.25); ax.fill_between([-3.2, 0], 0.8, 3.2, color="#2a6fb0", alpha=.25)
    for r in g.itertuples():
        if r.hors: continue
        f = np.clip(r.forme, -0.6, 0.6); c = plt.cm.RdYlGn((f + 0.6) / 1.2); s = 420 + 900 * max(f, 0) - 250 * max(-f, 0)
        ax.scatter(r.zJ, r.zH, s=s, color=c, alpha=.85, edgecolors="white" if r.pos <= 3 else "none", linewidths=2.5 if r.pos <= 3 else 0)
        ax.text(r.zJ, r.zH, str(int(r.numero)), ha="center", va="center", fontsize=9, color="black", fontweight="bold")
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2); ax.set_xlabel("valeur du jockey (Vincennes)", color="white"); ax.set_ylabel("valeur du cheval (dernieres courses)", color="white")
    ax.tick_params(colors="gray"); ax.set_title(f"{race} - cercle blanc = arrive dans les 3 (ajoute apres coup)", color="white", fontsize=10)
    fig.savefig(fn, dpi=110, facecolor="#111"); plt.close(fig)
for race in M.race.unique()[:3]: trace(race, f"{G}/visuturf_{race}.png")
open(f"{D}/rapport_visuturf.txt", "w").write("\n".join(out))
