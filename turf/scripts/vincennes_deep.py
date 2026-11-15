"""Approfondissement : vitesse de fin, reussite du driver a Vincennes, fautes, appetence cheval/driver pour Vincennes.
Regles fixees avant les tests. Effet mesure AU-DELA de la cote (offset = proba de top 3 donnee par la cote presse).
Usage : python3 -I vincennes_deep.py <json> <dossier_data>
"""
import sys, json, re, unicodedata, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
warnings.filterwarnings("ignore")
src, D = sys.argv[1], sys.argv[2]
P = pd.read_csv(f"{D}/partants_signaux.csv").reset_index(drop=True)
races = sorted(json.load(open(src))["message"], key=lambda r: (r["date"], r["r/c"]))
rng = np.random.default_rng(9)

def key(name):
    s = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z ]", " ", s).split(); w = [x for x in t if len(x) > 2]; i = [x for x in t if len(x) <= 2]
    return f"{'_'.join(w)}_{i[0][0] if i else ''}" if t else None
horse = lambda n: re.sub(r"[^a-z ]", "", unicodedata.normalize("NFKD", (n or "").lower()).encode("ascii", "ignore").decode()).strip()

# ---------------- historique a Vincennes (strictement anterieur a la course)
# A) arrivees publiees des 100 courses : top 7 / top 3 / victoires (pas de denominateur)
# B) courses a lot complet : vraies montes (denominateur connu) -> taux de reussite
arr, rides = [], []
for i, r in enumerate(races):
    for n, h in r["arrivee_details"].items():
        arr.append(dict(date=r["date"], cheval=horse(h["nom_cheval"]), drv=key(h["nom_jockey"]), pos=h["position"]))
    if r.get("partants_details"):
        pos = {int(n): h["position"] for n, h in r["arrivee_details"].items()}
        npset = set(r["non_partants"]) - set(r["arrivee"])
        for p in r["partants_details"]:
            if p["numero"] in npset: continue
            rides.append(dict(date=r["date"], cheval=horse(p["cheval"]), drv=key(p["jockey"]), top3=int(pos.get(p["numero"], 99) <= 3)))
A, Rr = pd.DataFrame(arr), pd.DataFrame(rides)
P["cheval_k"] = P.cheval.map(horse)
feat = []
for _, x in P.iterrows():
    a_h = A[(A.cheval == x.cheval_k) & (A.date < x.date)]; a_d = A[(A.drv == x.driver) & (A.date < x.date)]
    r_d = Rr[(Rr.drv == x.driver) & (Rr.date < x.date)]; r_h = Rr[(Rr.cheval == x.cheval_k) & (Rr.date < x.date)]
    feat.append(dict(
        chv_vinc_top7=len(a_h), chv_vinc_top3=int((a_h.pos <= 3).sum()), chv_vinc_courues=len(r_h),
        drv_vinc_top3=int((a_d.pos <= 3).sum()), drv_vinc_montes=len(r_d),
        drv_vinc_taux=(r_d.top3.sum() + 1) / (len(r_d) + 5)))  # taux lisse (a priori 20 %)
P = pd.concat([P, pd.DataFrame(feat)], axis=1)

# ---------------- textes (commentaire de presse)
com = {(i, p["numero"]): (p.get("commentaire") or "").lower() for i, r in enumerate(races) for p in (r.get("partants_details") or [])}
P["com"] = [com.get((r, n), "") for r, n in zip(P.race_id, P.numero)]
has = lambda pat: P.com.str.contains(pat, regex=True).astype(int)

SIG = {
 # vitesse de fin (seul indicateur disponible : le texte ; pas de temps partiels dans l'API)
 "finisseur": (has(r"finisseur|pointe de vitesse|(bel|bon|bel|joli|gros) effort final|belle fin de course|(termin|fini)\w* (tr[eè]s )?fort|vitesse terminale|bonne acc[ée]l[ée]ration|en trombe"), "+", "finisseur / vitesse de fin (texte)"),
 "meilleur_record": (P.meilleur_record, "+", "un des 3 meilleurs records du lot"),
 # fautes
 "fautif_texte": (has(r"fautif|faute|disqualifi|allures? (incertaine|fragile)|pas toujours sage|n'est pas sage|a tendance [àa] se mettre"), "-", "fautif / allures fragiles (texte)"),
 "dq_musique": ((P.musique_dq >= 1).astype(int), "-", ">= 1 disqualification/arret sur 5 courses"),
 "sage_texte": (has(r"tr[eè]s sage|sans faute|s[ûu]r (au trot|dans ses allures)|allures s[ûu]res|parfaitement sage"), "+", "sage / allures sures (texte)"),
 "deferre_et_fautif": (P.deferre * has(r"fautif|faute|disqualifi|allures? (incertaine|fragile)"), "-", "deferre ET fautif"),
 # appetence cheval pour Vincennes (historique reel des 100 courses)
 "chv_deja_place_vinc": ((P.chv_vinc_top7 >= 1).astype(int), "+", "cheval deja dans les 7 premiers a Vincennes"),
 "chv_deja_top3_vinc": ((P.chv_vinc_top3 >= 1).astype(int), "+", "cheval deja dans les 3 premiers a Vincennes"),
 "chv_aime_vinc_texte": (has(r"(aime|appr[ée]cie|adore|[àa] l'aise|affectionne|son jardin).{0,40}(vincennes|cendr[ée]e|grande piste|petite piste)"), "+", "aime Vincennes (texte)"),
 # reussite du driver a Vincennes
 "drv_top_taux": ((P.drv_vinc_taux >= P.drv_vinc_taux.quantile(0.75)).astype(int), "+", "driver : taux de top 3 a Vincennes dans le quart superieur"),
 "drv_top3_vinc": ((P.drv_vinc_top3 >= 3).astype(int), "+", "driver : >= 3 top 3 anterieurs a Vincennes"),
 "duo_drv_chv": (((P.chv_vinc_top7 >= 1) & (P.drv_vinc_top3 >= 3)).astype(int), "+", "cheval deja place a Vincennes ET driver performant a Vincennes"),
}
for k, (v, s, l) in SIG.items(): P[k] = np.asarray(v)
logit_off = np.log(P.p_top3_cote / (1 - P.p_top3_cote))

rep = []
def say(*a): rep.append(" ".join(str(x) for x in a))
say("# APPROFONDISSEMENT VINCENNES : effet AU-DELA de la cote presse sur l'arrivee dans les 3 premiers")
say(f"600 partants / 40 courses. Historique reel a Vincennes : {int((P.chv_vinc_top7 > 0).sum())} chevaux deja places dans les 7, "
    f"montes connues pour {int((P.drv_vinc_montes > 0).sum())} drivers-partants.")
def oe(d):
    o = d.top3.sum(); e = d.p_top3_cote.sum()
    sims = rng.binomial(1, np.tile(d.p_top3_cote.values, (20000, 1))).sum(1)
    return len(d), int(o), e, o / e if e else np.nan, min(1, 2 * min((sims >= o).mean(), (sims <= o).mean()))
rows = []
for pop_lab, pop in [("tous", P), ("non-favoris (rang cote >= 4)", P[P.rang_cote >= 4])]:
    for k, (v, s, l) in SIG.items():
        d = pop[pop[k] == 1]
        if len(d) < 5: continue
        n, o, e, r_, p = oe(d)
        m = sm.GLM(pop.top3, sm.add_constant(pop[[k]].astype(float)), family=sm.families.Binomial(),
                   offset=np.log(pop.p_top3_cote / (1 - pop.p_top3_cote))).fit()
        rows.append(dict(population=pop_lab, facteur=l, attendu=s, chevaux=n, places=o, attendu_cote=round(e, 1),
                         obs_sur_att=r_, p=p, odds_ratio=np.exp(m.params[k]), p_offset=m.pvalues[k]))
T = pd.DataFrame(rows)
T["p_holm"] = multipletests(T.p_offset.fillna(1), method="holm")[1]
for pop_lab in T.population.unique():
    say(f"\n## Population : {pop_lab}")
    say(T[T.population == pop_lab].drop(columns="population").round(3).to_string(index=False))
say("\nobs_sur_att > 1 : fait mieux que la cote ; odds_ratio > 1 : effet positif au-dela de la cote ; p_holm : corrige des 24 tests.")

# variables continues (taux du driver, nb de places du cheval a Vincennes)
say("\n## Variables continues (logistique, offset cote) - tous les partants")
for col, lab in [("drv_vinc_taux", "taux de top 3 du driver a Vincennes (lisse)"), ("chv_vinc_top7", "nb de top 7 anterieurs du cheval a Vincennes"),
                 ("drv_vinc_top3", "nb de top 3 anterieurs du driver a Vincennes"), ("record_rel", "record km relatif au lot")]:
    x = P[col].fillna(P[col].median()); x = (x - x.mean()) / x.std()
    m = sm.GLM(P.top3, sm.add_constant(x), family=sm.families.Binomial(), offset=logit_off).fit()
    say(f"  {lab:48s}: odds ratio par ecart-type = {np.exp(m.params.iloc[1]):.2f} (p={m.pvalues.iloc[1]:.3f})")

# lisibilite x driver : le bon driver compte-t-il plus dans les courses peu lisibles ?
say("\n## Driver performant a Vincennes selon la lisibilite de la course (tous partants)")
for c in ["peu lisible", "moyenne", "lisible"]:
    d = P[(P.classe == c) & (P.drv_top3_vinc == 1)]
    n, o, e, r_, p = oe(d) if len(d) else (0, 0, 0, np.nan, np.nan)
    say(f"  {c:12s}: {n:3d} chevaux, {o:2d} places / {e:4.1f} attendus (obs/att {r_:.2f}, p={p:.3f})")

open(f"{D}/rapport_vincennes.txt", "w").write("\n".join(rep))
P.drop(columns=["com"]).to_csv(f"{D}/partants_vincennes.csv", index=False)
print("\n".join(rep))
