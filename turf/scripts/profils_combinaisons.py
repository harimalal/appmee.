"""Combinaisons de cotes par profil de course, avec fourchettes.
- Arrivees (cote PMU finale des 4 premiers) : 98 courses d'attele.
- Nombre de chevaux par tranche de cote (cout d'un jeu) : cote presse des 40 courses a lot complet.
Usage : python3 -I profils_combinaisons.py <json> <dossier_data>
"""
import sys, json, warnings
import numpy as np, pandas as pd
from statsmodels.stats.proportion import proportion_confint
warnings.filterwarnings("ignore")
src, D = sys.argv[1], sys.argv[2]
races = sorted(json.load(open(src))["message"], key=lambda r: (r["date"], r["r/c"]))
R = pd.read_csv(f"{D}/courses.csv")
P = pd.read_csv(f"{D}/partants_signaux.csv")

def profil(partants, femelles, age_max):
    lot = "petit lot (<=14)" if partants <= 14 else "grand lot (>=15)"
    cat = "jeunes ou femelles" if (femelles == 1 or age_max <= 6) else "mixte, ages > 6 ans"
    return f"{lot} | {cat}"
rows = []
for i, r in enumerate(races):
    if r["type"] != "Attelé": continue
    rr = R[R.race_id == i].iloc[0]
    cotes = []
    for n in r["arrivee"][:4]:
        h = r["arrivee_details"].get(str(n)); v = [x for x in (h["cotes"] if h else []) if x is not None]
        cotes.append(v[-1] if v else np.nan)
    if any(np.isnan(cotes)): continue
    rows.append(dict(race_id=i, profil=profil(r["partants"], rr.femelles, rr.age_max), partants=r["partants"],
                     c1=cotes[0], c2=cotes[1], c3=cotes[2], c4=cotes[3]))
A = pd.DataFrame(rows)
TR = [(0, 5, "< 5"), (5, 10, "5-10"), (10, 20, "10-20"), (20, 40, "20-40"), (40, 1e9, "> 40")]
def tr(c):
    for lo, hi, t in TR:
        if lo <= c < hi: return t
def ic(k, n):
    lo, hi = proportion_confint(k, n, method="wilson"); return f"{k/n:.0%} [{lo:.0%}-{hi:.0%}]"

# taille des tranches (cout) : cote presse, 40 courses
P["profil"] = [profil(a, b, c) for a, b, c in zip(P.partants, P.femelles_course, P.age_max_course)]
P["tr"] = P.cote_presse.map(tr)
taille = P.groupby(["profil", "race_id", "tr"]).size().unstack(fill_value=0).groupby("profil").mean()

out = []
def say(*a): out.append(" ".join(str(x) for x in a))
say("# COMBINAISONS DE COTES PAR PROFIL DE COURSE (trot attele, Vincennes)")
say("Cotes = cote PMU finale des chevaux arrives. Fourchette = 50 % central des cas [25e-75e centile] ; plafond 90 % = 9 fois sur 10 la cote est en dessous.")
say("Entre crochets apres un % : intervalle de confiance a 95 % (petits effectifs -> fourchettes larges).\n")
for pf, g in A.groupby("profil"):
    n = len(g)
    say(f"=================== {pf} : {n} courses ===================")
    for pos, lab in [("c1", "Gagnant"), ("c2", "2e"), ("c3", "3e"), ("c4", "4e")]:
        q = g[pos].quantile([.25, .5, .75, .9])
        say(f"  {lab:8s}: mediane {q[.5]:5.1f} | fourchette {q[.25]:4.1f}-{q[.75]:5.1f} | plafond 90 % : {q[.9]:5.1f}")
    allc = g[["c1", "c2", "c3", "c4"]]
    say("  Gagnant par tranche : " + " | ".join(f"{t} {ic(int((g.c1.map(tr) == t).sum()), n)}" for *_, t in TR))
    comp = allc.apply(lambda s: s.map(tr)).apply(lambda r: r.value_counts(), axis=1).reindex(columns=[t for *_, t in TR]).fillna(0)
    say("  Top 4 moyen         : " + " | ".join(f"{t}: {comp[t].mean():.2f}" for *_, t in TR))
    say("  Au moins 1 cheval du top 4 en tranche : " + " | ".join(f"{t} {ic(int((comp[t] >= 1).sum()), n)}" for *_, t in TR))
    for plaf in [10, 20, 30, 50]:
        say(f"  Couverture si on ne prend que les cotes <= {plaf:2d} : gagnant {ic(int((g.c1 <= plaf).sum()), n)}, "
            f"trio (3 premiers) {ic(int((allc.iloc[:, :3] <= plaf).all(1).sum()), n)}, quarte (4 premiers) {ic(int((allc <= plaf).all(1).sum()), n)}")
    if pf in taille.index:
        t = taille.loc[pf]
        say("  Nb moyen de partants par tranche (cote presse, cout du jeu) : " + " | ".join(f"{k}: {t.get(k, 0):.1f}" for *_, k in TR))
    else:
        say("  Nb de partants par tranche : pas de course a lot complet dans ce profil")
    say("")
A.to_csv(f"{D}/profils_arrivees.csv", index=False)
open(f"{D}/rapport_profils.txt", "w").write("\n".join(out))
print("\n".join(out))
