"""Validation hors echantillon des regles sur les courses de Vincennes de novembre 2026 (letrot.com, usage prive).
Les regles sont FIGEES (aucun reglage sur les nouvelles courses). Seuils de lisibilite pris sur les 40 courses d'origine.
Usage : python3 -I validation_novembre.py <dossier_data> <dossier_pages_nov>
"""
import sys, json, html, glob, warnings
import numpy as np, pandas as pd
from scipy import stats
from scipy.special import logsumexp
warnings.filterwarnings("ignore")
D, W = sys.argv[1], sys.argv[2]
rep = []
def say(*a): rep.append(" ".join(str(x) for x in a)); print(rep[-1])

# ---------------- chargement des nouvelles courses
rows = []
for f in sorted(glob.glob(f"{W}/race_*.html")):
    raw = open(f, encoding="utf-8", errors="ignore").read()
    try:
        i = raw.find("<race-detail"); j = raw.find(':payload="', i); k = raw.find('"', j + 10)
        d = json.loads(html.unescape(raw[j + 10:k])); r = d["race"]
    except Exception:
        continue
    if r.get("discipline") != "A": continue
    ps = [p for p in r["partants"] if not p.get("nonPartant")]
    if len(ps) < 6: continue
    fem = int(all(p.get("sexe") == "F" for p in ps)); amax = max(p.get("age") or 0 for p in ps)
    for p in ps:
        rk = p.get("formattedRank")
        rows.append(dict(race=f"{r['dateCourse']}-C{r['numCourse']}", date=r["dateCourse"], partants=len(ps), femelles=fem, age_max=amax,
                         numero=p["leavingNumber"], cote=p.get("rapportProbable"), crack=p.get("crackSeries"), avis=p.get("avisEntraineur"),
                         pos=int(rk) if isinstance(rk, (int, float)) or (isinstance(rk, str) and rk.strip().isdigit()) else np.nan))
N = pd.DataFrame(rows)
N = N[N.cote.notna() & (N.cote > 0)]
N = N[N.groupby("race").cote.transform("size") >= 6]
N["pos"] = N.pos.where(N.pos > 0)
N["win"] = (N.pos == 1).astype(int); N["top3"] = (N.pos <= 3).astype(int); N["top4"] = (N.pos <= 4).astype(int)
say(f"# DONNEES NOVEMBRE : {N.race.nunique()} courses d'attele, {len(N)} partants, du {N.date.min()} au {N.date.max()}")

def prep(M):
    q = 1 / M.cote; M["p"] = q / q.groupby(M.race).transform("sum")
    M["rang_cote"] = M.groupby("race").cote.rank(method="first")
    M["crack0"] = M.crack.where(M.crack > 0, 20000)
    M["crack_rang"] = M.groupby("race").crack0.rank(method="min")
    ent = M.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s)))
    M["entropie"] = ent; M["pfav"] = M.groupby("race").p.transform("max")
    M["petit"] = M.partants <= 14; M["jf"] = (M.femelles == 1) | (M.age_max <= 6)
    M["profil"] = np.where(M.petit, "A/B petit lot", "C/D grand lot") + np.where(M.jf, " | jeunes-femelles", " | mixte")
    return M
def harville(p):
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
def add_p3(M):
    M["p3"] = np.nan
    for _, g in M.groupby("race"): M.loc[g.index, "p3"] = np.clip(harville(g.p.values), 1e-4, 1 - 1e-4)
    return M
N = add_p3(prep(N.reset_index(drop=True)))

# ---------------- reference : 40 courses d'origine (seuils figes)
O0 = pd.read_csv(f"{D}/partants_letrot_merge.csv")
O = pd.DataFrame({"race": O0.race_id, "numero": O0.numero, "cote": O0.cote_pmu, "crack": O0.crack_series, "avis": O0.avis_entraineur,
                  "partants": O0.partants, "femelles": O0.femelles_course, "age_max": O0.age_max_course, "pos": O0.position,
                  "win": O0.win, "top3": O0.top3, "top4": O0.top4})
O = add_p3(prep(O))
def lisib(M):
    r = M.drop_duplicates("race")
    return r
Ro = O.drop_duplicates("race"); zf = (Ro.pfav.mean(), Ro.pfav.std()); ze = (Ro.entropie.mean(), Ro.entropie.std())
def score(M): return (M.pfav - zf[0]) / zf[1] - (M.entropie - ze[0]) / ze[1]
O["lis"] = score(O); N["lis"] = score(N)
seuil = O.drop_duplicates("race").lis.quantile(1 / 3)
N["lisible"] = N.lis > seuil; O["lisible"] = O.lis > seuil
say(f"Indice de lisibilite (cote PMU : favori net + cote concentree). Seuil = tiers inferieur des 40 courses d'origine ; part de courses lisibles : origine {O.drop_duplicates('race').lisible.mean():.0%}, novembre {N.drop_duplicates('race').lisible.mean():.0%}")

BAR = [(5, (1.5, 2.0)), (10, (1.8, 2.5)), (15, (2.5, 3.5)), (20, (3.0, 4.25)), (np.inf, (3.5, 5.0))]
def pay(c, s):
    for lim, (lo, hi) in BAR:
        if c < lim: return {"bas": lo, "moyen": (lo + hi) / 2, "haut": hi}[s]
def roi(d):
    n = len(d)
    if n == 0: return "0 pari"
    g = (d.win * d.cote).sum() / n - 1
    pl = [(d.top3 * d.cote.map(lambda c: pay(c, s))).sum() / n - 1 for s in ["bas", "moyen", "haut"]]
    return f"{n:3d} paris | {int(d.win.sum()):2d} gagnants ({d.win.mean():.0%}) | gagnant {g:+.0%} | place {pl[0]:+.0%}/{pl[1]:+.0%}/{pl[2]:+.0%} ({int(d.top3.sum())} places)"
def both(label, fo, fn=None):
    fn = fn or fo
    say(f"  {label}\n      origine  : {roi(O[fo(O)])}\n      NOVEMBRE : {roi(N[fn(N)])}")

# ---------------- R1/R23 : la cote trouve combien de chevaux du top 4 ?
say("\n# R1 / R23. La cote PMU finale trouve le top 4")
def hits(M):
    h = [g.sort_values("cote").head(4).top4.sum() for _, g in M.groupby("race")]
    return np.mean(h), len(h)
def auc(M):
    a = []
    for _, g in M.groupby("race"):
        y = g.top4.values
        if 0 < y.sum() < len(y): a.append(stats.mannwhitneyu(-g.cote.values[y == 1], -g.cote.values[y == 0]).statistic / (y.sum() * (1 - y).sum()))
    return np.mean(a)
for lab, M in [("origine (40 courses)", O), ("NOVEMBRE", N)]:
    h, n = hits(M); say(f"  {lab:22s}: {h:.2f} chevaux du top 4 trouves sur 4 par course ({n} courses), AUC {auc(M):.2f}")

# ---------------- R2/R7 : lisibilite
say("\n# R2 / R7. Courses lisibles contre peu lisibles : top 4 trouves par la cote")
for lab, M in [("origine", O), ("NOVEMBRE", N)]:
    a = [g.sort_values("cote").head(4).top4.sum() for _, g in M[M.lisible].groupby("race")]
    b = [g.sort_values("cote").head(4).top4.sum() for _, g in M[~M.lisible].groupby("race")]
    tt = stats.mannwhitneyu(a, b, alternative="greater").pvalue if len(a) > 2 and len(b) > 2 else np.nan
    say(f"  {lab:9s}: lisibles {np.mean(a):.2f} ({len(a)} courses) | peu lisibles {np.mean(b):.2f} ({len(b)} courses) | p unilateral {tt:.3f}")
fav = lambda M: M.rang_cote == 1
both("Favori en course peu lisible (regle 7 : -22 % au place)", lambda M: fav(M) & ~M.lisible)
both("Favori en course lisible", lambda M: fav(M) & M.lisible)

# ---------------- R16 / R20 / R26 : le favori par profil
say("\n# R16 / R20 / R26. Le favori selon la taille du lot et le profil")
both("Favori, petit lot (14 ou moins)  [regle 16 : a jouer]", lambda M: fav(M) & M.petit)
both("Favori, grand lot (15 ou plus)   [regle 20 : a eviter]", lambda M: fav(M) & ~M.petit)
both("Favori, petit lot mixte  [profil A]", lambda M: fav(M) & M.petit & ~M.jf)
both("Favori, petit lot jeunes-femelles  [profil B]", lambda M: fav(M) & M.petit & M.jf)
both("Favori, grand lot mixte  [profil C]", lambda M: fav(M) & ~M.petit & ~M.jf)
both("Favori, grand lot jeunes-femelles  [profil D : a eviter]", lambda M: fav(M) & ~M.petit & M.jf)
say("  Part des gagnants a cote < 5 par profil (tableau des profils)")
for lab, M in [("origine", O), ("NOVEMBRE", N)]:
    w = M[M.win == 1]
    t = w.groupby(["petit", "jf"]).agg(courses=("cote", "size"), cote_inf5=("cote", lambda s: (s < 5).mean()), mediane=("cote", "median")).round(2)
    say(f"   {lab}\n" + "\n".join("      " + l for l in t.to_string().split("\n")))

# ---------------- R24 : avis entraineur sur le favori
say("\n# R24. Favori selon l'avis de l'entraineur")
both("Favori SANS avis favorable (avis != 1) : a jouer", lambda M: fav(M) & (M.avis != 1))
both("Favori AVEC avis favorable (avis = 1) : a se mefier", lambda M: fav(M) & (M.avis == 1))
for lab, M in [("origine", O), ("NOVEMBRE", N)]:
    a = M[M.avis == 1]; say(f"  Tous chevaux a avis favorable ({lab}) : {int(a.top3.sum())} places pour {a.p3.sum():.1f} attendus (cote)")

# ---------------- R25 : Crack Series non-favoris
say("\n# R25. Non-favoris (4e cote et +) dans les 3 meilleurs Crack Series du lot")
for lab, M in [("origine", O), ("NOVEMBRE", N)]:
    d = M[(M.rang_cote >= 4) & (M.crack_rang <= 3)]; o, e = d.top3.sum(), d.p3.sum()
    sims = np.random.default_rng(1).binomial(1, np.tile(d.p3.values, (20000, 1))).sum(1)
    say(f"  {lab:9s}: {len(d)} chevaux, {int(o)} places pour {e:.1f} attendus (obs/att {o/e:.2f}, p bilateral {min(1, 2*min((sims>=o).mean(), (sims<=o).mean())):.3f}) | " + roi(d))
both("Cote PMU des 3 premieres + meilleur Crack du lot", lambda M: (M.rang_cote <= 3) & (M.crack_rang == 1))

# ---------------- R8 / R9 : outsiders
say("\n# R8 / R9. Gros outsiders")
both("Cote de plus de 40 (regle 8 : 0 victoire, -79 % au place)", lambda M: M.cote > 40)

# ---------------- R17 / R18 : composition du top 4
say("\n# R17 / R18. Composition du top 4 en cotes")
def compo(M):
    t = M[M.top4 == 1]
    g = t.groupby("race").agg(n_inf5=("cote", lambda s: (s < 5).sum()), n_5_10=("cote", lambda s: ((s >= 5) & (s < 10)).sum()),
                              n_10_20=("cote", lambda s: ((s >= 10) & (s < 20)).sum()), n_sup20=("cote", lambda s: (s >= 20).sum()),
                              n10=("cote", lambda s: (s >= 10).sum()))
    return g
for lab, M in [("origine", O), ("NOVEMBRE", N)]:
    g = compo(M); petit = M.drop_duplicates("race").set_index("race").petit
    g = g.join(petit)
    say(f"  {lab:9s} (moyenne du top 4) : <5 {g.n_inf5.mean():.2f} | 5-10 {g.n_5_10.mean():.2f} | 10-20 {g.n_10_20.mean():.2f} | >=20 {g.n_sup20.mean():.2f} ; "
        f"au moins un cheval >=20 : {(g.n_sup20 >= 1).mean():.0%} ; au moins 2 chevaux >=10 : {(g.n10 >= 2).mean():.0%}")
    say(f"            cotes >=10 dans le top 4 : petit lot {g[g.petit].n10.mean():.2f} ({g.petit.sum()} courses) contre grand lot {g[~g.petit].n10.mean():.2f} ({(~g.petit).sum()} courses)")

# ---------------- R27 : Crack Series seul
say("\n# R27. Crack Series seul contre la cote")
def auc_by(M, col, sign=1):
    a = []
    for _, g in M.groupby("race"):
        y = g.top4.values
        if 0 < y.sum() < len(y): a.append(stats.mannwhitneyu(-sign * g[col].values[y == 1], -sign * g[col].values[y == 0]).statistic / (y.sum() * (1 - y).sum()))
    return np.mean(a)
for lab, M in [("origine", O), ("NOVEMBRE", N)]:
    say(f"  {lab:9s}: AUC cote {auc_by(M, 'cote'):.2f} | AUC Crack Series {auc_by(M, 'crack0'):.2f}")

# ---------------- tableau des profils : couverture trio
say("\n# Tableau des profils : couverture trio avec cotes <= 20 / <= 30 (3 premiers tous sous le plafond)")
for lab, M in [("origine", O), ("NOVEMBRE", N)]:
    for key, g in M[M.pos <= 3].groupby(["petit", "jf"]):
        c = g.groupby("race").cote.max()
        say(f"  {lab:9s} {'petit lot' if key[0] else 'grand lot'} {'jeunes-femelles' if key[1] else 'mixte':16s}: {len(c):2d} courses | <=20 : {(c<=20).mean():.0%} | <=30 : {(c<=30).mean():.0%} | <=50 : {(c<=50).mean():.0%}")
open(f"{D}/rapport_validation_novembre.txt", "w").write("\n".join(rep))
N.to_csv(f"{D}/novembre_partants.csv", index=False)
