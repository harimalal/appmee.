"""Test du jeu fonde sur les tendances de Vincennes (T1, T2 : top 4 = 2-3 chevaux des cotes 1-5 + environ 1 des cotes 6-10).
Formules definies AVANT le test, toutes en desordre, 1 euro par combinaison, toutes les courses de 10 partants ou plus (aucun filtre) :
  F1 trio  : 2 chevaux des cotes 1-5 + 1 cheval des cotes 6-10          (50 combinaisons)
  F2 trio  : 3 chevaux des cotes 1-5                                    (10 combinaisons)
  F3 trio  : F1 + F2                                                    (60 combinaisons)
  F4 trio  : favori en base + 1 des cotes 2-5 + 1 des cotes 6-10        (20 combinaisons)
  F5 quarte: 3 chevaux des cotes 1-5 + 1 cheval des cotes 6-10          (50 combinaisons)
Mesure : taux de reussite observe contre le taux attendu par la cote (Harville) pour les MEMES combinaisons. Si obs/att > 1, les tendances apportent
un avantage sur le marche. Rapport estime = (1 - 30 %) / probabilite Harville de l'arrivee (pas de rapport officiel) : le rendement estime est
donc 0,70 x obs/att - 1 en moyenne.
Usage : python3 -I test_tendances.py <dossier_data>
"""
import sys, itertools, numpy as np, pandas as pd
D = sys.argv[1]; PREL = 0.30
O0 = pd.read_csv(f"{D}/partants_letrot_merge.csv"); Nv = pd.read_csv(f"{D}/novembre_partants.csv")
O = pd.DataFrame({"race": O0.race_id.astype(str), "cote": O0.cote_pmu, "pos": O0.position, "partants": O0.partants})
N = Nv[["race", "cote", "pos", "partants"]].copy()
def h3(p, a, b, c): return p[a] * p[b] / (1 - p[a]) * p[c] / (1 - p[a] - p[b])
def h4(p, a, b, c, d): return h3(p, a, b, c) * p[d] / (1 - p[a] - p[b] - p[c])
def tri(p, t): return sum(h3(p, *x) for x in itertools.permutations(t))
def qua(p, t): return sum(h4(p, *x) for x in itertools.permutations(t))
def formules(n):
    A = list(range(5)); B = list(range(5, min(10, n)))
    f1 = [tuple(sorted(c + (b,))) for c in itertools.combinations(A, 2) for b in B]
    f2 = list(itertools.combinations(A, 3))
    f4 = [tuple(sorted((0, a, b))) for a in range(1, 5) for b in B]
    f5 = [tuple(sorted(c + (b,))) for c in itertools.combinations(A, 3) for b in B]
    return {"F1 trio 2 (cotes 1-5) + 1 (cotes 6-10)": ("t", f1), "F2 trio 3 des cotes 1-5": ("t", f2), "F3 trio F1 + F2": ("t", sorted(set(f1) | set(f2))),
            "F4 trio favori + 1 (2-5) + 1 (6-10)": ("t", f4), "F5 quarte 3 (cotes 1-5) + 1 (cotes 6-10)": ("q", f5)}
def run(M):
    rows = []
    for race, g in M.groupby("race", sort=False):
        g = g.sort_values("cote").reset_index(drop=True)
        n = len(g)
        if n < 10: continue
        q = 1 / g.cote; p = (q / q.sum()).values
        f3 = tuple(sorted(g.index[g.pos.fillna(99) <= 3])); f4 = tuple(sorted(g.index[g.pos.fillna(99) <= 4]))
        for name, (kind, combos) in formules(n).items():
            if kind == "t":
                if len(f3) != 3: continue
                e = sum(tri(p, c) for c in combos); hit = f3 in set(combos); ret = (1 - PREL) / tri(p, f3) if hit else 0.0
            else:
                if len(f4) != 4: continue
                e = sum(qua(p, c) for c in combos); hit = f4 in set(combos); ret = (1 - PREL) / qua(p, f4) if hit else 0.0
            rows.append(dict(race=race, n=n, petit=n <= 14, formule=name, cout=len(combos), hit=int(hit), att=e, retour=ret))
    return pd.DataFrame(rows)
out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(out[-1])
rng = np.random.default_rng(0)
def table(R, titre):
    say(f"\n## {titre}")
    say(f"{'formule':44s} {'courses':>7s} {'cout/crs':>8s} {'touche':>7s} {'attendu':>8s} {'obs/att':>8s} {'p':>6s} {'gain estime':>12s}")
    for f, g in R.groupby("formule", sort=False):
        n = len(g); hit = g.hit.sum(); att = g.att.sum()
        sims = rng.binomial(1, np.tile(g.att.clip(0, 1).values, (20000, 1))).sum(1)
        pv = min(1, 2 * min((sims >= hit).mean(), (sims <= hit).mean()))
        mise = g.cout.sum(); gain = g.retour.sum() - mise
        say(f"{f:44s} {n:7d} {g.cout.mean():8.0f} {int(hit):3d}/{n:<3d} {att:8.1f} {hit / att:8.2f} {pv:6.2f} {gain:+8.0f} ({gain / mise:+.0%})")
RO, RN = run(O), run(N)
say(f"# TEST DES TENDANCES : courses de 10 partants ou plus, aucun filtre (origine {RO.race.nunique()} courses, novembre {RN.race.nunique()} courses)")
say("Les formules viennent des tendances observees dans l'echantillon d'origine (T1, T2). Novembre sert de confirmation, mais ses tendances ont ete lues avant de fixer les formules : a prendre comme indicatif.")
table(RO, "ORIGINE (40 courses)"); table(RN, "NOVEMBRE 2026")
table(pd.concat([RO.assign(race="o" + RO.race), RN]), "LES DEUX ENSEMBLE")
for nm, flag in [("PETITS LOTS (14 ou moins)", True), ("GRANDS LOTS (15 ou plus)", False)]:
    table(pd.concat([RO.assign(race="o" + RO.race), RN]).query("petit == @flag"), f"LES DEUX ENSEMBLE - {nm}")
# serie cumulee F3 novembre / origine
for lab, R in [("origine", RO), ("novembre", RN)]:
    g = R[R.formule.str.startswith("F3")]; cum = (g.retour - g.cout).cumsum()
    say(f"\nGain cumule F3, {lab}, course apres course : " + " ".join(f"{x:+.0f}" for x in cum))
open(f"{D}/rapport_test_tendances.txt", "w").write("\n".join(out))
