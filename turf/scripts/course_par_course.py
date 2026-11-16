"""Course par course : on applique la grille de regles FIGEE et on regarde le resultat de chaque course jouee (aucun reglage).
Grille (ordre de prise en compte) :
  1. course peu lisible (tiers inferieur, seuil des 40 courses d'origine)  -> on ne joue pas        (regles 2, 7)
  2. profil D (grand lot, jeunes ou femelles)                               -> on ne joue pas        (regles 19, 20, 26)
  3. profil C (grand lot, mixte)                                            -> pas de favori en simple (regle 20)
  4. profils A / B (petit lot) : favori PMU, sauf avis entraineur favorable -> on joue le favori   (regles 16, 24)
Mise : 1 euro gagnant + 1 euro place sur le favori (bareme de Hari : bas/moyen/haut). Cote > 40 jamais jouee (regle 8).
Usage : python3 -I course_par_course.py <dossier_data>
"""
import sys, numpy as np, pandas as pd
D = sys.argv[1]
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
O = prep(pd.DataFrame({"race": O0.race_id, "date": O0.date, "numero": O0.numero, "cote": O0.cote_pmu, "avis": O0.avis_entraineur,
                       "partants": O0.partants, "femelles": O0.femelles_course, "age_max": O0.age_max_course, "pos": O0.position,
                       "win": O0.win, "top3": O0.top3}))
Nv = pd.read_csv(f"{D}/novembre_partants.csv")
N = prep(Nv[["race", "date", "numero", "cote", "avis", "partants", "femelles", "age_max", "pos", "win", "top3"]].copy())
Ro = O.drop_duplicates("race"); zf, ze = (Ro.pfav.mean(), Ro.pfav.std()), (Ro.entropie.mean(), Ro.entropie.std())
sc = lambda M: (M.pfav - zf[0]) / zf[1] - (M.entropie - ze[0]) / ze[1]
O["lis"] = sc(O); N["lis"] = sc(N); seuil = O.drop_duplicates("race").lis.quantile(1 / 3)
lines = []
def say(*a): lines.append(" ".join(str(x) for x in a)); print(lines[-1])
def run(M, nom):
    out = []
    for race, g in M.groupby("race", sort=False):
        f = g[g.rang_cote == 1].iloc[0]
        profil = ("A/B petit lot" if f.petit else "C/D grand lot") + (" jeunes-femelles" if f.jf else " mixte")
        if g.lis.iloc[0] <= seuil: dec, why = 0, "peu lisible"
        elif (not f.petit) and f.jf: dec, why = 0, "profil D"
        elif not f.petit: dec, why = 0, "profil C (pas de favori en simple)"
        elif f.avis == 1: dec, why = 0, "avis entraineur favorable"
        elif f.cote > 40: dec, why = 0, "cote > 40"
        else: dec, why = 1, "JOUE le favori"
        row = dict(course=f"{g.date.iloc[0]} {race}", partants=int(g.partants.iloc[0]), profil=profil, favori=int(f.numero), cote=f.cote, avis=int(f.avis) if pd.notna(f.avis) else -1,
                   decision=dec, raison=why, arrivee=int(f.pos) if pd.notna(f.pos) else 0, win=int(f.win), top3=int(f.top3))
        row["gain_gagnant"] = (f.win * f.cote - 1) if dec else 0.0
        for s in ["bas", "moyen", "haut"]: row[f"gain_place_{s}"] = (f.top3 * pay(f.cote, s) - 1) if dec else 0.0
        out.append(row)
    R = pd.DataFrame(out); R["nom"] = nom; return R
RO, RN = run(O, "origine"), run(N, "NOVEMBRE")

say("# COURSE PAR COURSE : NOVEMBRE 2026 (hors echantillon), 1 euro gagnant + 1 euro place sur le favori quand la grille dit JOUE")
say(f"{'course':28s} {'lot':>3s} {'profil':27s} {'fav':>3s} {'cote':>5s} {'avis':>4s}  decision                              arrivee  gagnant  place(moyen)")
for _, r in RN.iterrows():
    res = f"{r.arrivee}e" if r.arrivee else "hors top"
    if r.decision: say(f"{r.course:28s} {r.partants:3d} {r.profil:27s} {r.favori:3d} {r.cote:5.1f} {r.avis:4d}  JOUE le favori{'':23s} {res:>8s}  {r.gain_gagnant:+7.1f}  {r.gain_place_moyen:+7.2f}")
    else: say(f"{r.course:28s} {r.partants:3d} {r.profil:27s} {r.favori:3d} {r.cote:5.1f} {r.avis:4d}  passe : {r.raison:28s} {res:>8s}")
def bilan(R, titre):
    J, S = R[R.decision == 1], R[R.decision == 0]
    say(f"\n## {titre}")
    say(f"  Courses jouees : {len(J)} sur {len(R)} | favori gagnant {int(J.win.sum())} ({J.win.mean():.0%}) | favori dans les 3 : {int(J.top3.sum())} ({J.top3.mean():.0%})")
    if len(J):
        say(f"  Gagnant : mise {len(J)} euros, gain net {J.gain_gagnant.sum():+.1f} ({J.gain_gagnant.mean():+.0%})")
        say(f"  Place   : gain net {J.gain_place_bas.sum():+.1f} / {J.gain_place_moyen.sum():+.1f} / {J.gain_place_haut.sum():+.1f} euros (bas/moyen/haut) = {J.gain_place_bas.mean():+.0%} / {J.gain_place_moyen.mean():+.0%} / {J.gain_place_haut.mean():+.0%}")
        # sequence cumulee
        cum = J.gain_gagnant.cumsum() + J.gain_place_moyen.cumsum(); say(f"  Cumul gagnant + place (moyen), course apres course : " + " ".join(f"{x:+.1f}" for x in cum))
    # controle : le meme pari sur les courses ecartees aurait-il fait pire ?
    if len(S):
        S = S.copy(); S["gp"] = [(w * c - 1) for w, c in zip(S.win, S.cote)]
        S["pm"] = [t * pay(c, "moyen") - 1 for t, c in zip(S.top3, S.cote)]
        say(f"  Controle, favori sur les {len(S)} courses ECARTEES : gagnant {S.gp.mean():+.0%} ({int(S.win.sum())} victoires), place moyen {S.pm.mean():+.0%} ({int(S.top3.sum())} places)")
        for why, g in S.groupby("raison"):
            say(f"      - {why:36s}: {len(g):2d} courses | gagnant {g.gp.mean():+.0%} | place {g.pm.mean():+.0%}")
bilan(RN, "BILAN NOVEMBRE (hors echantillon)")
bilan(RO, "BILAN 40 COURSES D'ORIGINE (la grille a ete construite sur elles : indicatif seulement)")
# par profil, novembre
say("\n## Novembre, courses jouees par profil")
J = RN[RN.decision == 1]
say(J.groupby("profil").agg(courses=("win", "size"), gagnants=("win", "sum"), places=("top3", "sum"), net_gagnant=("gain_gagnant", "sum"), net_place_moyen=("gain_place_moyen", "sum")).round(1).to_string())
# serie : on repete 20 000 fois en tirant au hasard 20 des courses jouees pour voir la dispersion
rng = np.random.default_rng(0); g = (J.gain_gagnant + J.gain_place_moyen).values
if len(g) >= 10:
    sims = [rng.choice(g, size=len(g), replace=True).sum() for _ in range(20000)]
    say(f"\nDispersion (reechantillonnage des {len(g)} courses jouees, gagnant + place moyen) : gain net median {np.median(sims):+.1f} euros, intervalle a 90 % de {np.percentile(sims, 5):+.1f} a {np.percentile(sims, 95):+.1f} euros ; probabilite d'etre en gain {np.mean(np.array(sims) > 0):.0%}")
RN.to_csv(f"{D}/course_par_course_novembre.csv", index=False)
open(f"{D}/rapport_course_par_course.txt", "w").write("\n".join(lines))
