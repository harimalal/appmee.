"""Regles de Hari par niveau de lisibilite, sur le graphique de type Visuturf (valeur cheval x valeur jockey), sans utiliser la cote pour CHOISIR.
  Course LISIBLE (tiers superieur)   : 2 chevaux de l'encart haut-droite (zone verte) -> ils doivent etre dans les 3 premiers
  Course MOYENNEMENT lisible          : 1 cheval de l'encart bas-droite (jaune, au milieu, pas pres des bords) + 1 cheval de l'encart haut-gauche, a la limite du bord
  Course PEU lisible (tiers inferieur): on ne joue pas
Zone verte = au-dessus des moyennes cheval ET jockey, pas excentre (<= 2,2 ecarts-types). Jaune = jockey > moyenne (>0,3), cheval entre -1 et 0. Haut-gauche = cheval > 0,3, jockey entre -0,8 et 0 (limite du bord avec la zone verte).
Exclus : zone rouge, chevaux sans historique (hors graphique), chevaux proches de la croisee des axes (< 0,5). Seuils de lisibilite : tiers de l'echantillon d'origine, figes.
La cote ne sert qu'a juger APRES coup (attendu par le marche).
Usage : python3 -I visuturf_regles.py <dossier_data>
"""
import sys, itertools, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
warnings.filterwarnings("ignore")
D = sys.argv[1]; out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(out[-1])
M = pd.read_csv(f"{D}/visuturf_partants.csv")
M["ent"] = M.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s))); M["pfav"] = M.groupby("race").p.transform("max")
full = pd.concat([pd.read_csv(f"{D}/feat_origine.csv"), pd.read_csv(f"{D}/feat_novembre.csv")]); full = full[(full.discipline == "A") & (full.cote > 0)]
O = full[full.race.str.startswith("o")].copy(); q = 1 / O.cote; O["p"] = q / q.groupby(O.race).transform("sum")
O["ent"] = O.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s))); O["pfav"] = O.groupby("race").p.transform("max"); Ro = O.drop_duplicates("race")
zf, ze = (Ro.pfav.mean(), Ro.pfav.std()), (Ro.ent.mean(), Ro.ent.std())
sc = lambda d: (d.pfav - zf[0]) / zf[1] - (d.ent - ze[0]) / ze[1]
O["lis"] = sc(O); t1, t2 = O.drop_duplicates("race").lis.quantile([1 / 3, 2 / 3])
M["lis"] = sc(M); M["classe"] = np.where(M.lis > t2, "lisible", np.where(M.lis > t1, "moyennement lisible", "peu lisible"))
X0 = sm.add_constant(M[["lp"]]); M["pe"] = sm.GLM(M.y, X0, family=sm.families.Binomial()).fit().predict(X0)
M["vert"] = (M.zone == "vert (favoris)") & M.zH.between(0, 2.2) & M.zJ.between(0, 2.2) & ~M.exclu
M["jaune"] = (M.zone == "jaune (bons jockeys)") & (M.zJ > 0.3) & M.zH.between(-1.0, 0) & ~M.exclu
M["hautgauche"] = (M.zH > 0.3) & M.zJ.between(-0.8, 0) & ~M.exclu
M["hautgauche_milieu"] = M.hautgauche & M.zH.between(0.3, 2.0)
say(f"# {M.race.nunique()} courses completes ; classes de lisibilite (seuils figes de l'origine) : " + " | ".join(f"{k} {v}" for k, v in M.drop_duplicates('race').classe.value_counts().items()))
rows = []
for race, g in M.groupby("race"):
    cl = g.classe.iloc[0]; picks = []
    if cl == "lisible": picks = [("vert", r) for r in g[g.vert].sort_values("val", ascending=False).head(2).itertuples()]
    elif cl == "moyennement lisible":
        j = g[g.jaune].sort_values("val", ascending=False).head(1); h = g[g.hautgauche].sort_values("zH", ascending=False).head(1)
        picks = [("jaune", r) for r in j.itertuples()] + [("haut-gauche", r) for r in h.itertuples()]
    for kind, r in picks: rows.append(dict(race=race, classe=cl, kind=kind, y=r.y, pe=r.pe, cote=r.cote, num=r.numero))
R = pd.DataFrame(rows)
def cote_baseline(cl, k_by_race):
    r = []
    for race, k in k_by_race.items():
        if k == 0: continue
        g = M[M.race == race].sort_values("cote").head(k); r.append((g.y.sum(), g.pe.sum(), k))
    return pd.DataFrame(r, columns=["hits", "exp", "k"])
BAR = [(5, 1.75), (10, 2.15), (15, 3.0), (20, 3.6), (np.inf, 4.25)]
def pay(c): return next(v for lim, v in BAR if c < lim)
for cl in ["lisible", "moyennement lisible"]:
    d = R[R.classe == cl]; nr = M[M.classe == cl].race.nunique()
    say(f"\n## Courses {cl.upper()} ({nr} courses)")
    if d.empty: say("  aucun cheval retenu"); continue
    k = d.groupby("race").size().to_dict(); base = cote_baseline(cl, k)
    say(f"  Chevaux retenus : {len(d)} (dans {len(k)} courses) | dans les 3 : {int(d.y.sum())} ({d.y.mean():.0%}) | attendu par la cote : {d.pe.sum():.1f} ({d.pe.mean():.0%}) | x{d.y.sum() / d.pe.sum():.2f} | cote mediane des choisis {d.cote.median():.1f}")
    say(f"  Reperes sur les memes courses : meme nombre de chevaux pris par la cote ({int(base.k.sum())} chevaux) : {int(base.hits.sum())} dans les 3 ({base.hits.sum() / base.k.sum():.0%})")
    for kind, g in d.groupby("kind"): say(f"    - {kind:12s}: {len(g):3d} chevaux, {int(g.y.sum()):2d} dans les 3 ({g.y.mean():.0%}), attendu {g.pe.sum():.1f}, cote mediane {g.cote.median():.1f}")
    by = d.groupby("race").agg(n=("y", "size"), hits=("y", "sum"))
    for n_ in sorted(by.n.unique()):
        s = by[by.n == n_]; say(f"    Courses avec {n_} cheval(aux) retenu(s) : {len(s)} | au moins 1 dans les 3 : {(s.hits >= 1).mean():.0%} | tous dans les 3 : {(s.hits == n_).mean():.0%}")
    ex = d.cote.map(pay); say(f"  Place 1 euro sur chacun (bareme de Hari, milieu) : mise {len(d)}, gain net {(d.y * ex).sum() - len(d):+.1f} euros ({(d.y * ex).sum() / len(d) - 1:+.0%})")
say("\n## Courses PEU LISIBLES : non jouees. Controle : les 3 premieres cotes y trouvent " + f"{np.mean([g.sort_values('cote').head(3).y.sum() for _, g in M[M.classe == 'peu lisible'].groupby('race')]):.2f} places sur 3")
say("\n## Variante : haut-gauche 'au milieu du bord' (cheval entre 0,3 et 2,0, ni tout en haut ni trop bas)")
r2 = []
for race, g in M[M.classe == "moyennement lisible"].groupby("race"):
    h = g[g.hautgauche_milieu].sort_values("zH", ascending=False).head(1)
    for r in h.itertuples(): r2.append((r.y, r.pe))
if r2: a = np.array(r2); say(f"  {len(a)} chevaux, {int(a[:, 0].sum())} dans les 3 ({a[:, 0].mean():.0%}), attendu {a[:, 1].sum():.1f}")
say("\n## VERIFICATION DE L'OBSERVATION : combien des 3 premiers de l'arrivee se trouvent dans chaque encart, selon la lisibilite ?")
say(f"{'classe':22s} {'courses':>7s} | {'encart vert':>22s} | {'encart jaune':>22s} | {'encart haut-gauche':>22s} | {'zone rouge / exclus':>22s}")
for cl in ["lisible", "moyennement lisible", "peu lisible"]:
    g = M[M.classe == cl]; nr = g.race.nunique(); cells = []
    for col in ["vert", "jaune", "hautgauche", "exclu"]:
        top = g[g.y == 1].groupby("race")[col].sum().reindex(g.race.unique()).fillna(0); exp = g.groupby("race").apply(lambda s: (s.pe * s[col]).sum())
        cells.append(f"{top.mean():.2f} des 3 (cote {exp.mean():.2f})")
    say(f"{cl:22s} {nr:7d} | " + " | ".join(f"{c:>22s}" for c in cells))
    if cl == "lisible":
        top = g[g.y == 1].groupby("race").vert.sum().reindex(g.race.unique()).fillna(0); say(f"    Courses lisibles avec au moins 2 des 3 premiers dans l'encart vert : {(top >= 2).mean():.0%} ; au moins 1 : {(top >= 1).mean():.0%}")
open(f"{D}/rapport_visuturf_regles.txt", "w").write("\n".join(out))
