"""Simulation du jeu complet en appliquant les regles figees, course par course.
Regles appliquees (ordre) : 1 lisibilite  2 profil D ecarte  3 profil C : jeux combines seulement  4 petit lot : favori, sauf avis favorable  8 jamais cote > 40
Paris (1 euro chacun) :
  Profil A/B (petit lot, favori sans avis favorable) : gagnant favori | place favori + 2e + 3e cote | trio desordre = favori en base + 6 chevaux de cote 5 a 20 (15 combinaisons)
  Profil C (grand lot mixte lisible) : trio desordre sur les chevaux de cote 4 a 30 (7 maximum, par cote croissante)
Gagnant : vraie cote PMU. Place : bareme de Hari (milieu ; bas/haut en plus).
Trio : arrivee REELLE, mais rapport ESTIME = (1 - prelevement) / probabilite Harville de la combinaison (pas de rapport officiel disponible).
Usage : python3 -I simulation_jeu.py <dossier_data>
"""
import sys, itertools, numpy as np, pandas as pd
D = sys.argv[1]; PREL = 0.30
BAR = [(5, (1.5, 2.0)), (10, (1.8, 2.5)), (15, (2.5, 3.5)), (20, (3.0, 4.25)), (np.inf, (3.5, 5.0))]
def pay(c, s):
    for lim, (lo, hi) in BAR:
        if c < lim: return {"bas": lo, "moyen": (lo + hi) / 2, "haut": hi}[s]
def prep(M):
    q = 1 / M.cote; M["p"] = q / q.groupby(M.race).transform("sum")
    M["rang_cote"] = M.groupby("race").cote.rank(method="first")
    M["entropie"] = M.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s)))
    M["pfav"] = M.groupby("race").p.transform("max")
    M["petit"] = M.partants <= 14; M["jf"] = (M.femelles == 1) | (M.age_max <= 6)
    return M
O0 = pd.read_csv(f"{D}/partants_letrot_merge.csv")
O = prep(pd.DataFrame({"race": O0.race_id.astype(str), "date": O0.date, "numero": O0.numero, "cote": O0.cote_pmu, "avis": O0.avis_entraineur,
                       "partants": O0.partants, "femelles": O0.femelles_course, "age_max": O0.age_max_course, "pos": O0.position, "win": O0.win, "top3": O0.top3}))
Nv = pd.read_csv(f"{D}/novembre_partants.csv")
N = prep(Nv[["race", "date", "numero", "cote", "avis", "partants", "femelles", "age_max", "pos", "win", "top3"]].copy())
Ro = O.drop_duplicates("race"); zf, ze = (Ro.pfav.mean(), Ro.pfav.std()), (Ro.entropie.mean(), Ro.entropie.std())
sc = lambda M: (M.pfav - zf[0]) / zf[1] - (M.entropie - ze[0]) / ze[1]
O["lis"] = sc(O); N["lis"] = sc(N); seuil = O.drop_duplicates("race").lis.quantile(1 / 3)

def harv(p, a, b, c): return p[a] * p[b] / (1 - p[a]) * p[c] / (1 - p[a] - p[b])
def trio_prob(p, t): return sum(harv(p, *x) for x in itertools.permutations(t))
def play_race(g):
    g = g.sort_values("cote").reset_index(drop=True); f = g.iloc[0]
    petit = f.petit; jf = f.jf
    if g.lis.iloc[0] <= seuil: return "ecartee : peu lisible", []
    if (not petit) and jf: return "ecartee : profil D", []
    bets = []
    p = g.p.values; top3 = set(g[g.pos <= 3].index)
    arr3 = tuple(sorted(top3)) if len(top3) == 3 else None
    def trio(idx, cost_label):
        combos = [c for c in itertools.combinations(idx, 3)] if cost_label == "C" else None
        return combos
    if petit:
        if f.avis == 1: return "ecartee : avis favorable", []
        if f.cote > 40: return "ecartee : cote > 40", []
        bets.append(("gagnant favori", 1.0, f.win * f.cote, {"bas": f.win * f.cote, "haut": f.win * f.cote}))
        for r in range(3):
            h = g.iloc[r]; bets.append((f"place {r+1}", 1.0, h.top3 * pay(h.cote, "moyen"), {"bas": h.top3 * pay(h.cote, "bas"), "haut": h.top3 * pay(h.cote, "haut")}))
        pool = [i for i in range(1, len(g)) if 5 <= g.cote[i] <= 20][:6]
        combos = [(0, a, b) for a, b in itertools.combinations(pool, 2)]
        label = "trio A/B"
        profil = "A/B petit lot"
    else:
        pool = [i for i in range(len(g)) if 4 <= g.cote[i] <= 30][:7]
        combos = list(itertools.combinations(pool, 3)); label = "trio C"; profil = "C grand lot mixte"
    ret = 0.0
    if arr3 is not None and arr3 in {tuple(sorted(c)) for c in combos}:
        ret = (1 - PREL) / trio_prob(p, arr3)
    bets.append((label, float(len(combos)), ret, {"bas": ret, "haut": ret}))
    return profil, bets
def run(M):
    rows = []
    for race, g in M.groupby("race", sort=False):
        profil, bets = play_race(g)
        for name, mise, ret, alt in bets: rows.append(dict(race=race, date=g.date.iloc[0], profil=profil, pari=name, mise=mise, retour=ret, retour_bas=alt["bas"], retour_haut=alt["haut"]))
        if not bets: rows.append(dict(race=race, date=g.date.iloc[0], profil=profil, pari="aucun", mise=0.0, retour=0.0, retour_bas=0.0, retour_haut=0.0))
    return pd.DataFrame(rows)
out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(out[-1])
def bilan(R, titre):
    J = R[R.mise > 0]; n = J.race.nunique()
    say(f"\n## {titre}")
    say(f"  Courses jouees : {n} sur {R.race.nunique()} | mise totale {J.mise.sum():.0f} euros | retour {J.retour.sum():.1f} euros | gain net {J.retour.sum() - J.mise.sum():+.1f} euros ({(J.retour.sum() - J.mise.sum()) / J.mise.sum():+.0%})")
    t = J.groupby("pari").agg(paris=("mise", "size"), mise=("mise", "sum"), retour=("retour", "sum"))
    t["gain_net"] = t.retour - t.mise; t["rendement"] = t.gain_net / t.mise
    say("  Par type de pari :\n" + "\n".join("    " + l for l in t.round(2).to_string().split("\n")))
    t2 = J.groupby("profil").agg(courses=("race", "nunique"), mise=("mise", "sum"), retour=("retour", "sum")); t2["gain_net"] = t2.retour - t2.mise
    say("  Par profil :\n" + "\n".join("    " + l for l in t2.round(1).to_string().split("\n")))
    simple = J[~J.pari.str.startswith("trio")]; tr = J[J.pari.str.startswith("trio")]
    for lab, S in [("Simples seuls (gagnant favori + places)", simple), ("Trios seuls", tr)]:
        if len(S): say(f"  {lab} : mise {S.mise.sum():.0f}, retour {S.retour.sum():.1f}, gain net {S.retour.sum() - S.mise.sum():+.1f} ({(S.retour.sum() - S.mise.sum()) / S.mise.sum():+.0%}) ; avec bareme bas/haut : {(S.retour_bas.sum() - S.mise.sum()) / S.mise.sum():+.0%} / {(S.retour_haut.sum() - S.mise.sum()) / S.mise.sum():+.0%}")
    hit = tr[tr.retour > 0]
    say(f"  Trios touches : {len(hit)} sur {len(tr)} ({len(hit)/max(len(tr),1):.0%}) ; rapport estime median {hit.retour.median() if len(hit) else float('nan'):.0f} euros, max {hit.retour.max() if len(hit) else float('nan'):.0f} euros")
    byrace = J.groupby("race", sort=False).agg(mise=("mise", "sum"), retour=("retour", "sum")); cum = (byrace.retour - byrace.mise).cumsum()
    say("  Gain cumule course apres course : " + " ".join(f"{x:+.0f}" for x in cum) + f"  | point bas {cum.min():+.0f} euros")
    return J
say("# SIMULATION DU JEU COMPLET (regles figees). Mise 1 euro par pari / combinaison. Rapports du trio ESTIMES (prelevement 30 %).")
RN, RO = run(N), run(O)
say("\n## NOVEMBRE 2026, course par course")
for race, g in RN.groupby("race", sort=False):
    if g.mise.sum() == 0: say(f"  {race:16s} {g.profil.iloc[0]}"); continue
    say(f"  {race:16s} {g.profil.iloc[0]:18s} mise {g.mise.sum():3.0f} | retour {g.retour.sum():7.1f} | net {g.retour.sum() - g.mise.sum():+7.1f}  (" + ", ".join(f"{r.pari} {r.retour - r.mise:+.1f}" for r in g.itertuples()) + ")")
JN = bilan(RN, "BILAN NOVEMBRE (hors echantillon)")
bilan(RO, "BILAN 40 COURSES D'ORIGINE (grille construite sur elles : indicatif)")
# sensibilite unique : prelevement du trio
for prel in (0.25, 0.35):
    pass
RN.to_csv(f"{D}/simulation_jeu_novembre.csv", index=False)
open(f"{D}/rapport_simulation_jeu.txt", "w").write("\n".join(out))
