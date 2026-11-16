"""Approche 'investisseur' : 1) filtrer les courses (risques negatifs) 2) noter chaque cheval (cote + classe + appetence Vincennes + forme + avis) 3) jouer 2-3 chevaux
en couple place (2 chevaux dans les 3) et en 2 sur 4 (2 chevaux dans les 4), avec et sans le favori.
Modele cale sur une partie des courses et teste sur l'autre (jamais sur ce qui l'a calibre).
Usage : python3 -I modele_investisseur.py <dossier_data>
"""
import sys, itertools, warnings
import numpy as np, pandas as pd
from scipy.optimize import minimize
from scipy.special import logsumexp
from scipy import stats
warnings.filterwarnings("ignore")
D = sys.argv[1]; PREL = 0.30
out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(out[-1])
O = pd.read_csv(f"{D}/feat_origine.csv"); N = pd.read_csv(f"{D}/feat_novembre.csv")
O["ech"] = "origine"; N["ech"] = "novembre"
M = pd.concat([O, N], ignore_index=True)
M = M[(M.discipline == "A") & (M.cote > 0)].copy()
M = M[M.groupby("race").cote.transform("size") >= 6]
q = 1 / M.cote; M["p"] = q / q.groupby(M.race).transform("sum"); M["lp"] = np.log(M.p)
M["rang_cote"] = M.groupby("race").cote.rank(method="first")
M["ent"] = M.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s))); M["pfav"] = M.groupby("race").p.transform("max")
M["petit"] = M.partants <= 14
fem = M.groupby("race").sexe.transform(lambda s: (s == "F").all()); M["jf"] = fem | (M.groupby("race").age.transform("max") <= 6)
M["pos"] = M.pos.where(M.pos > 0)
# --- signaux (relatifs au lot)
def rel(s): return s - s.groupby(M.race).transform("mean")
M["crack0"] = M.crack.where(M.crack > 0, M.crack.max() + 1)
M["f_classe"] = rel(-np.log(M.crack0))                      # classe (Crack Series), + = meilleur
M["f_exp"] = rel(np.log1p(M.gains))                          # experience / gains
M["f_forme"] = rel(M.song_top3.astype(float))                # forme : places sur les 5 dernieres
M["f_vin"] = rel(M.vin_top3 / (M.vin_n + 1))                 # appetence Vincennes (places / courses a Vincennes, lisse)
M["f_dq"] = rel(M.song_dq.astype(float))                     # fautes recentes
M["f_avis"] = (M.avis == 1).astype(float)                    # avis entraineur favorable
SIG = ["f_classe", "f_exp", "f_forme", "f_vin", "f_dq", "f_avis"]
SIGL = {"f_classe": "classe (Crack Series)", "f_exp": "experience (gains)", "f_forme": "forme (places sur 5 dernieres)", "f_vin": "appetence Vincennes", "f_dq": "fautes recentes", "f_avis": "avis entraineur favorable"}

def stages(df, K=4):
    st = []
    for rid, g in df.groupby("race"):
        idx = g.index.values; pos = g.pos.values; alive = np.ones(len(idx), bool)
        for k in range(1, K + 1):
            w = np.where(pos == k)[0]
            if len(w) != 1: break
            st.append((idx[alive], idx[w[0]])); alive[w[0]] = False
    return st
def fit(df, cols, lam, mu=None, sd=None):
    X = df[cols].values.astype(float).copy()
    if mu is None: mu = np.zeros(len(cols)); sd = np.ones(len(cols)); mu[1:] = X[:, 1:].mean(0); sd[1:] = X[:, 1:].std(0) + 1e-9
    X = (X - mu) / sd; ix = {i: n for n, i in enumerate(df.index)}
    st = [(np.array([ix[a] for a in s]), ix[c]) for s, c in stages(df)]
    pen = np.r_[0.0, np.full(len(cols) - 1, lam)]
    def nll(b):
        u = X @ b; f = 0.0; g = np.zeros(len(b))
        for s, c in st:
            l = logsumexp(u[s]); pp = np.exp(u[s] - l); f -= u[c] - l; g -= X[c] - pp @ X[s]
        return f + (pen * b * b).sum(), g + 2 * pen * b
    b = minimize(nll, np.r_[1.0, np.zeros(len(cols) - 1)], jac=True, method="L-BFGS-B").x
    return b, mu, sd
def score(df, cols, b, mu, sd): return ((df[cols].values.astype(float) - mu) / sd) @ b
def ll_order(g, u):
    pos = g.pos.values; ll = 0.0; alive = np.ones(len(g), bool)
    for k in range(1, 5):
        w = np.where(pos == k)[0]
        if len(w) != 1: return np.nan
        ll += u[w[0]] - logsumexp(u[alive]); alive[w[0]] = False
    return ll
COLS = ["lp"] + SIG
LAM = 8.0
say(f"# DONNEES : {M.race.nunique()} courses d'attele ({(M.ech=='origine').sum()} partants origine, {(M.ech=='novembre').sum()} novembre), signaux avant course uniquement")

# ---------------- 1. filtre des courses (risques negatifs)
say("\n# 1. FILTRE DES COURSES (risques negatifs)")
Ro = M[M.ech == "origine"].drop_duplicates("race"); zf, ze = (Ro.pfav.mean(), Ro.pfav.std()), (Ro.ent.mean(), Ro.ent.std())
M["lis"] = (M.pfav - zf[0]) / zf[1] - (M.ent - ze[0]) / ze[1]; seuil = M[M.ech == "origine"].drop_duplicates("race").lis.quantile(1 / 3)
M["course_lisible"] = M.lis > seuil; M["profil_D"] = (~M.petit) & M.jf
M["gardee"] = M.course_lisible & ~M.profil_D
def hits_cote(g): return g.sort_values("cote").head(4).pos.le(4).sum()
Rc = M.groupby("race").apply(lambda g: pd.Series(dict(h=hits_cote(g), lisible=g.course_lisible.iloc[0], D=g.profil_D.iloc[0], gardee=g.gardee.iloc[0], cat=g.categorie.iloc[0], alloc=g.allocation.iloc[0], petit=g.petit.iloc[0], ech=g.ech.iloc[0], n=len(g))))
Rc["h"] = Rc.h.astype(float)
for lab, mask in [("lisible", Rc.lisible == True), ("peu lisible", Rc.lisible == False), ("profil D (grand lot jeunes/femelles)", Rc.D == True), ("GARDEES (lisible, hors profil D)", Rc.gardee == True), ("ECARTEES", Rc.gardee == False)]:
    say(f"  {lab:40s}: {mask.sum():3d} courses | top 4 trouves par la cote {Rc[mask].h.mean():.2f}")
Rc["classe_course"] = pd.cut(Rc.alloc.astype(float), [0, 25000, 40000, 1e9], labels=["allocation < 25 000", "25 000-40 000", "> 40 000"])
say("  Par allocation (classe de la course) : " + " | ".join(f"{k} : {g.h.mean():.2f} ({len(g)})" for k, g in Rc.groupby("classe_course")))
say("  Par categorie : " + " | ".join(f"{k} : {g.h.mean():.2f} ({len(g)})" for k, g in Rc.groupby("cat") if len(g) >= 4))
say(f"  Courses gardees : {int(Rc.gardee.sum())} sur {len(Rc)} ({Rc.gardee.mean():.0%})")

# ---------------- 2. modele du cheval : cale sur l'origine, teste sur novembre
say("\n# 2. MODELE DU CHEVAL (cote + signaux), cale sur l'ORIGINE, teste sur NOVEMBRE (jamais vu)")
tr, te = M[M.ech == "origine"], M[M.ech == "novembre"]
b, mu, sd = fit(tr, COLS, LAM)
b0, mu0, sd0 = fit(tr, ["lp"], 0.0)
say("  Poids du modele (par ecart-type, + = favorise le cheval au-dela de sa cote) : lp (cote) " + f"{b[0]:.2f} | " + " | ".join(f"{SIGL[c]} {w:+.2f}" for c, w in zip(SIG, b[1:])))
def eval_ll(df, u_fn):
    return np.array([ll_order(g, u_fn(g)) for _, g in df.groupby("race")])
llm = eval_ll(te, lambda g: score(g, COLS, b, mu, sd)); llc = eval_ll(te, lambda g: score(g, ["lp"], b0, mu0, sd0)); llb = eval_ll(te, lambda g: g.lp.values)
ok = ~np.isnan(llm) & ~np.isnan(llc)
say(f"  Novembre ({ok.sum()} courses), vraisemblance de l'ordre des 4 premiers par course : cote brute {np.nanmean(llb):.3f} | cote recalibree {llc[ok].mean():.3f} | MODELE complet {llm[ok].mean():.3f} (gain vs cote recalibree {np.mean(llm[ok]-llc[ok]):+.3f}, p={stats.wilcoxon(llm[ok]-llc[ok]).pvalue:.2f})")
b_r, mu_r, sd_r = fit(te, COLS, LAM); b0_r, mu0_r, sd0_r = fit(te, ["lp"], 0.0)
llm2 = eval_ll(tr, lambda g: score(g, COLS, b_r, mu_r, sd_r)); llc2 = eval_ll(tr, lambda g: score(g, ["lp"], b0_r, mu0_r, sd0_r)); ok2 = ~np.isnan(llm2) & ~np.isnan(llc2)
say(f"  Controle inverse (cale sur novembre, teste sur l'origine, {ok2.sum()} courses) : gain du modele vs cote recalibree {np.mean(llm2[ok2]-llc2[ok2]):+.3f} (p={stats.wilcoxon(llm2[ok2]-llc2[ok2]).pvalue:.2f})")
say("  Poids calibres sur novembre : lp " + f"{b_r[0]:.2f} | " + " | ".join(f"{SIGL[c]} {w:+.2f}" for c, w in zip(SIG, b_r[1:])))

# ---------------- 3. selection de 2-3 chevaux et paris (validation croisee par course sur les 2 echantillons)
say("\n# 3. COUPLE PLACE et 2 SUR 4 avec 3 chevaux (3 couples par course) - validation croisee : chaque course est jouee avec un modele qui ne l'a pas vue")
races = M.drop_duplicates("race").race.tolist()
rng = np.random.default_rng(0)
def pair_probs(p, n_sim=20000):
    n = len(p); t = -np.log(rng.random((n_sim, n))) / p; order = np.argsort(t, axis=1)[:, :4]
    P3 = np.zeros((n, n)); P4 = np.zeros((n, n))
    for s in order:
        for a, bb in itertools.combinations(s[:3], 2): P3[a, bb] += 1; P3[bb, a] += 1
        for a, bb in itertools.combinations(s, 2): P4[a, bb] += 1; P4[bb, a] += 1
    return P3 / n_sim, P4 / n_sim
rows = []
for rid in races:
    g = M[M.race == rid].sort_values("cote").reset_index(drop=False)
    if g.pos.le(4).sum() < 4 or g.pos.le(3).sum() < 3: continue
    train = M[M.race != rid]; bb, mm, ss = fit(train, COLS, LAM)
    g["u"] = score(g, COLS, bb, mm, ss); n = len(g); p = g.p.values
    P3, P4 = pair_probs(p, 6000)
    set3, set4 = set(g.index[g.pos <= 3]), set(g.index[g.pos <= 4])
    strat = {"cote seule (top 3 par la cote)": [0, 1, 2], "cote seule sans le favori (2e a 4e)": [1, 2, 3],
             "MODELE (3 meilleurs scores)": list(np.argsort(-g.u.values)[:3]),
             "MODELE sans le favori": [i for i in np.argsort(-g.u.values) if i != 0][:3]}
    for name, sel in strat.items():
        for a, c in itertools.combinations(sel, 2):
            rows.append(dict(race=rid, ech=g.ech.iloc[0], gardee=g.gardee.iloc[0], strat=name, c3=int(a in set3 and c in set3), c4=int(a in set4 and c in set4), e3=P3[a, c], e4=P4[a, c]))
R = pd.DataFrame(rows)
def resume(R, titre):
    say(f"\n## {titre}")
    say(f"{'strategie':40s} {'courses':>7s} | {'couple place':>25s} | {'2 sur 4':>25s}")
    for st, g in R.groupby("strat", sort=False):
        nr = g.race.nunique(); s3, e3, s4, e4 = g.c3.sum(), g.e3.sum(), g.c4.sum(), g.e4.sum()
        sims3 = rng.binomial(1, np.tile(g.e3.clip(0, 1).values, (4000, 1))).sum(1); p3 = min(1, 2 * min((sims3 >= s3).mean(), (sims3 <= s3).mean()))
        sims4 = rng.binomial(1, np.tile(g.e4.clip(0, 1).values, (4000, 1))).sum(1); p4 = min(1, 2 * min((sims4 >= s4).mean(), (sims4 <= s4).mean()))
        g3 = (s3 * (1 - PREL) * len(g) / max(e3, 1e-9) / len(g)) if False else None
        say(f"{st:40s} {nr:7d} | {int(s3):3d}/{len(g)} att {e3:5.1f} x{s3/e3:4.2f} p={p3:.2f} | {int(s4):3d}/{len(g)} att {e4:5.1f} x{s4/e4:4.2f} p={p4:.2f}")
resume(R, "TOUTES LES COURSES (82)")
resume(R[R.gardee], "COURSES GARDEES par le filtre (lisibles, hors profil D)")
resume(R[~R.gardee], "COURSES ECARTEES (controle)")
resume(R[R.gardee & (R.ech == "novembre")], "COURSES GARDEES - NOVEMBRE seul")
resume(R[R.gardee & (R.ech == "origine")], "COURSES GARDEES - ORIGINE seul")
say("\nLecture : 'att' = nombre de couples gagnants attendus avec la cote ; x = observe / attendu (>1 : la selection bat la cote).")
open(f"{D}/rapport_modele_investisseur.txt", "w").write("\n".join(out))
R.to_csv(f"{D}/selection_couples.csv", index=False)
