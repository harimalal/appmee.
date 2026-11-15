"""Signal faible : la valeur du cheval au-dela de la cote, et la lisibilite de la course.
Regles fixees AVANT les tests (pas d'ajustement sur les resultats) :
 - population cible : chevaux HORS des 3 premiers de la cote presse ("sans les favoris")
 - attendu : proba de top 3 donnee par la cote presse (Harville) ; on mesure observe / attendu
 - modele : logistique avec la cote en 'offset' -> le coefficient mesure uniquement ce que le signal ajoute a la cote
Usage : python3 -I signal_faible.py <json> <dossier_data>
"""
import sys, json, re, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
warnings.filterwarnings("ignore")
src, D = sys.argv[1], sys.argv[2]
P = pd.read_csv(f"{D}/partants_top4.csv").reset_index(drop=True)
R = pd.read_csv(f"{D}/courses.csv")
races_json = sorted(json.load(open(src))["message"], key=lambda r: (r["date"], r["r/c"]))
P["top3"] = (P.position <= 3).astype(int)
rng = np.random.default_rng(3)

# ---------------- commentaire de presse par cheval
com = {}
for i, r in enumerate(races_json):
    for p in (r.get("partants_details") or []):
        com[(i, p["numero"])] = (p.get("commentaire") or "").lower()
P["com"] = [com.get((r, n), "") for r, n in zip(P.race_id, P.numero)]
def has(pat): return P["com"].str.contains(pat, regex=True).astype(int)
SIG = {}
# "fait pour la course" : signaux d'adequation (positifs attendus)
SIG["deferre"] = (has(r"d[ée]ferr|pieds nus"), "+", "deferre / pieds nus annonce")
SIG["engagement"] = (has(r"(bel|bon|id[ée]al|int[ée]ressant|favorable|beau) engagement|engagement (id[ée]al|int[ée]ressant|favorable)|bien engag|au plafond|plafond des gains|en t[êe]te des gains"), "+", "engagement favorable / au plafond des gains")
SIG["objectif"] = (has(r"objectif|pr[ée]par[ée]|vis[ée]e?|cibl"), "+", "course visee / preparee")
SIG["aime_parcours"] = (has(r"(aime|appr[ée]cie|adore|[àa] l'aise) .{0,30}(vincennes|piste|parcours|distance|grande piste|petite piste)|sp[ée]cialiste"), "+", "aime la piste / la distance")
SIG["en_progres"] = (has(r"progr[eè]s|monte en puissance|sur la mont[ée]e|en net progr"), "+", "en progres")
# signaux de doute (negatifs attendus)
SIG["fautif"] = (has(r"fautif|faute|disqualifi|allures? (incertaine|fragile)|pas toujours sage"), "-", "fautif / allures fragiles")
SIG["rentree"] = (has(r"rentr[ée]e|retour a la comp|absent depuis|apr[eè]s une (longue )?absence"), "?", "rentree / retour d'absence")
SIG["decouvre"] = (has(r"d[ée]couvr|premi[eè]re fois|in[ée]dit"), "?", "decouvre une condition")
# signaux numeriques d'adequation
cap = P.race_id.map(R.set_index("race_id")["gain_cap"])
P["ratio_plafond"] = P.gains / cap
SIG["proche_plafond"] = (((P.ratio_plafond >= 0.85) & cap.notna()).astype(int), "+", "gains >= 85 % du plafond de la course")
SIG["meilleur_record"] = ((P.groupby("race_id")["record"].rank(method="min") <= 3).astype(int), "+", "un des 3 meilleurs records du lot")
SIG["forme_victoires"] = ((P.musique_victoires >= 2).astype(int), "+", ">= 2 victoires sur les 5 dernieres")
SIG["driver_regulier"] = ((P.drv_prior_top4 >= 5).astype(int), "+", "driver avec >= 5 top 4 anterieurs")
for k, (v, s, l) in SIG.items(): P[k] = v.values
POS = [k for k, v in SIG.items() if v[1] == "+"]; NEG = [k for k, v in SIG.items() if v[1] == "-"]
P["score_signal"] = P[POS].sum(axis=1) - P[NEG].sum(axis=1)   # poids fixes = 1, pas d'ajustement

# ---------------- attendu par la cote presse : proba de top 3 (Harville sur la proba implicite)
def harville_top3(p):
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
P["p_top3_cote"] = np.nan
for r, g in P.groupby("race_id"):
    P.loc[g.index, "p_top3_cote"] = harville_top3(g.p_impl.values)
P["p_top3_cote"] = P.p_top3_cote.clip(1e-4, 1 - 1e-4)

# ---------------- lisibilite de la course (avant course)
rows = []
for i, r in enumerate(races_json):
    if not r.get("partants_details"): continue
    g = P[P.race_id == i]; p = g.p_impl.values
    pron = [set(v[:5]) for v in (r.get("pronostics_presse") or {}).values()]
    accord = np.mean([len(a & b) / len(a | b) for x, a in enumerate(pron) for b in pron[x + 1:]]) if len(pron) > 1 else np.nan
    rows.append(dict(race_id=i, entropie=-(p * np.log(p)).sum() / np.log(len(p)), p_favori=p.max(), accord_presse=accord))
L = pd.DataFrame(rows)
z = lambda s: (s - s.mean()) / s.std()
L["lisibilite"] = (-z(L.entropie) + z(L.p_favori) + z(L.accord_presse)) / 3
L["classe"] = pd.qcut(L.lisibilite, 3, labels=["peu lisible", "moyenne", "lisible"])
P = P.merge(L[["race_id", "lisibilite", "classe"]], on="race_id")

rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))

# ======================== 1. LISIBILITE : la course lisible est-elle plus previsible ?
say("# 1. LISIBILITE DE LA COURSE (indice avant course : concentration de la cote, poids du favori, accord entre journaux)")
res = []
for rid, g in P.groupby("race_id"):
    y = g.top4.values; s = g.p_impl.values
    res.append(dict(race_id=rid, hits=y[np.argsort(-s)[:4]].sum(), fav_top3=int(g.loc[g.rang_cote == 1, "top3"].iloc[0]),
                    cote_gagnant=g.loc[g.win == 1, "cote_presse"].iloc[0], lisibilite=g.lisibilite.iloc[0], classe=g.classe.iloc[0]))
Q = pd.DataFrame(res)
say(Q.groupby("classe").agg(courses=("hits", "size"), top4_trouves_par_cote=("hits", "mean"), favori_place=("fav_top3", "mean"),
                            cote_presse_moy_gagnant=("cote_gagnant", "mean")).round(2).to_string())
for col in ["hits", "fav_top3", "cote_gagnant"]:
    rho, p = stats.spearmanr(Q.lisibilite, Q[col]); say(f"  correlation lisibilite / {col} : rho={rho:+.2f}, p={p:.3f}")

# ======================== 2. SIGNAUX FAIBLES chez les NON-favoris
NF = P[P.rang_cote >= 4].copy()
say(f"\n# 2. SIGNAUX FAIBLES - chevaux hors des 3 premiers de la cote presse : {len(NF)} chevaux, {int(NF.top3.sum())} places dans les 3 (attendu par la cote : {NF.p_top3_cote.sum():.1f})")
say("Observe/attendu > 1 : le signal fait mieux que ce que la cote prevoit. Coef offset : effet au-dela de la cote (log-odds).")
def oe(df, mask):
    d = df[mask]; o = d.top3.sum(); e = d.p_top3_cote.sum()
    # test : simulation des places attendues (somme de Bernoulli)
    sims = rng.binomial(1, np.tile(d.p_top3_cote.values, (20000, 1))).sum(1)
    p = min(1, 2 * min((sims >= o).mean(), (sims <= o).mean()))
    return len(d), int(o), e, o / e if e > 0 else np.nan, p
def offset_fit(df, cols):
    X = sm.add_constant(df[cols].astype(float)); off = np.log(df.p_top3_cote / (1 - df.p_top3_cote))
    return sm.GLM(df.top3, X, family=sm.families.Binomial(), offset=off).fit()
rows = []
for k, (v, s, l) in SIG.items():
    n, o, e, r_, p = oe(NF, NF[k] == 1)
    try:
        m = offset_fit(NF, [k]); b, pb = m.params[k], m.pvalues[k]
    except Exception: b = pb = np.nan
    rows.append(dict(signal=l, attendu=s, chevaux=n, places=o, attendu_cote=round(e, 1), obs_sur_att=r_, p=p, coef_offset=b, p_offset=pb))
S = pd.DataFrame(rows)
from statsmodels.stats.multitest import multipletests
S["p_holm"] = multipletests(S.p.fillna(1), method="holm")[1]
say(S.round(3).to_string(index=False))

say("\nScore cumule (nb de signaux positifs - signaux negatifs, poids fixes a 1) :")
for lo, hi, lab in [(-9, 0, "score <= 0"), (1, 1, "score 1"), (2, 2, "score 2"), (3, 99, "score >= 3")]:
    n, o, e, r_, p = oe(NF, NF.score_signal.between(lo, hi))
    say(f"  {lab:12s}: {n:4d} chevaux, {o:3d} places / {e:5.1f} attendus -> obs/att {r_:.2f} (p={p:.3f})")
m = offset_fit(NF, ["score_signal"])
say(f"  logistique offset : +1 point de score = x{np.exp(m.params['score_signal']):.2f} sur la cote de top 3 au-dela de la cote presse (p={m.pvalues['score_signal']:.3f})")
# stabilite : 20 premieres courses / 20 suivantes
order = P.drop_duplicates("race_id").sort_values(["date", "race_id"]).race_id.tolist()
for lab, ids in [("20 premieres courses", order[:20]), ("20 suivantes", order[20:])]:
    d = NF[NF.race_id.isin(ids)]
    n, o, e, r_, p = oe(d, d.score_signal >= 2)
    say(f"  stabilite {lab}: score >= 2 -> {n} chevaux, {o} places / {e:.1f} attendus (obs/att {r_:.2f}, p={p:.3f})")

# ======================== 3. SIGNAL x LISIBILITE
say("\n# 3. SIGNAL FAIBLE SELON LA LISIBILITE DE LA COURSE (non-favoris, score >= 2)")
for c in ["peu lisible", "moyenne", "lisible"]:
    d = NF[NF.classe == c]
    n, o, e, r_, p = oe(d, d.score_signal >= 2)
    n0, o0, e0, r0, p0 = oe(d, d.score_signal < 2)
    say(f"  {c:12s}: signal -> {n:3d} chevaux, {o:2d} places / {e:4.1f} att. (obs/att {r_:.2f}, p={p:.3f}) | sans signal : obs/att {r0:.2f}")

# ======================== 4. PARIS PLACES (bareme de Hari) sur les non-favoris a signal
BAREME = [(5, (1.5, 2.0)), (10, (1.8, 2.5)), (15, (2.5, 3.5)), (20, (3.0, 4.25)), (np.inf, (3.5, 5.0))]
def rapport(c, scen):
    for lim, (lo, hi) in BAREME:
        if c < lim: return {"bas": lo, "moyen": (lo + hi) / 2, "haut": hi}[scen]
say("\n# 4. PARIS PLACES SIMULES (1 euro) - non-favoris selectionnes par le signal, bareme de Hari (bas / moyen / haut)")
def roi(mask):
    d = P[mask]; out = []
    for scen in ["bas", "moyen", "haut"]:
        ret = (d.top3 * d.cote_pmu_final.map(lambda c: rapport(c, scen) if pd.notna(c) else 0)).sum()
        out.append(ret / len(d) - 1 if len(d) else np.nan)
    return len(d), int(d.top3.sum()), out
strats = {
    "Non-favoris, tous": P.rang_cote >= 4,
    "Non-favoris, score >= 2": (P.rang_cote >= 4) & (P.score_signal >= 2),
    "Non-favoris, score >= 3": (P.rang_cote >= 4) & (P.score_signal >= 3),
    "Non-favoris cote <= 20, score >= 2": (P.rang_cote >= 4) & (P.score_signal >= 2) & (P.cote_presse <= 20),
    "Non-favoris, score >= 2, course lisible": (P.rang_cote >= 4) & (P.score_signal >= 2) & (P.classe == "lisible"),
    "Non-favoris, score >= 2, course peu lisible": (P.rang_cote >= 4) & (P.score_signal >= 2) & (P.classe == "peu lisible"),
    "Reference : favori presse": P.rang_cote == 1,
    "Favori presse, course lisible": (P.rang_cote == 1) & (P.classe == "lisible"),
    "Favori presse, course peu lisible": (P.rang_cote == 1) & (P.classe == "peu lisible"),
}
for k, m in strats.items():
    n, w, (b, mo, h) = roi(m)
    say(f"  {k:46s}: {n:3d} paris, {w:2d} places -> {b:+.0%} / {mo:+.0%} / {h:+.0%}")
say(f"\n{len(SIG)} signaux et {len(strats)} strategies testes : prudence, un resultat isole peut etre du au hasard.")
open(f"{D}/rapport_signal_faible.txt", "w").write("\n".join(rep))
P.drop(columns=["com"]).to_csv(f"{D}/partants_signaux.csv", index=False)
print("\n".join(rep))
