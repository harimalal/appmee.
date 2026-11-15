"""Suivi EN DIRECT d'une reunion de Vincennes (letrot.com, usage prive, 1 page par releve, delai 3 s entre pages).
Pour chaque course d'attele : releves de cote a H-40, H-20, H-8 min (decision) puis H-2 min (mise a jour). Regles figees (lisibilite, profil, favori/avis) + probabilites d'etre dans les 3.
Usage : python3 -I live_run.py <dossier_courses> <date AAAA-MM-JJ> <courses ex: 1,3,4,5,7,9>
         python3 -I live_run.py <dossier_courses> test <fichier_page.html>      (essai a blanc sur une page deja jouee)
"""
import sys, os, json, html, time, subprocess, re, warnings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd, statsmodels.api as sm
warnings.filterwarnings("ignore")
HIP = os.environ.get("HIP", "7500")
B = sys.argv[1]; D = f"{B}/data"; W = f"{B}/web/live"; os.makedirs(W, exist_ok=True)
# ---------- reglages figes (issus des 82 courses d'analyse)
O = pd.read_csv(f"{D}/feat_origine.csv"); O = O[(O.discipline == "A") & (O.cote > 0)].copy()
q = 1 / O.cote; O["p"] = q / q.groupby(O.race).transform("sum")
O["ent"] = O.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s))); O["pfav"] = O.groupby("race").p.transform("max"); Ro = O.drop_duplicates("race")
ZF, ZE = (Ro.pfav.mean(), Ro.pfav.std()), (Ro.ent.mean(), Ro.ent.std())
lis_o = (Ro.pfav - ZF[0]) / ZF[1] - (Ro.ent - ZE[0]) / ZE[1]; T1, T2 = lis_o.quantile([1 / 3, 2 / 3])
A = pd.read_csv(f"{D}/proba_top3_82.csv"); CAL = sm.GLM(A.y, sm.add_constant(A[["lp"]]), family=sm.families.Binomial()).fit()
def p3(lp): return 1 / (1 + np.exp(-(CAL.params["const"] + CAL.params["lp"] * lp)))
def page(path):
    raw = open(path, encoding="utf-8", errors="ignore").read(); i = raw.find("<race-detail"); j = raw.find(':payload="', i); k = raw.find('"', j + 10)
    return json.loads(html.unescape(raw[j + 10:k]))
def fetch(date, c, label):
    f = f"{W}/{HIP}_{date}_C{c}_{label}.html"
    subprocess.run(["curl", "-sS", "-m", "60", "-A", "Mozilla/5.0 (analyse privee)", "-o", f, f"https://www.letrot.com/courses/{date}/{HIP}/{c}"]); time.sleep(3)
    return f
def snap(date, c, label):
    P = page(fetch(date, c, label)); r = P["race"]
    s = {int(p["leavingNumber"]): p.get("rapportProbable") for p in r["partants"] if not p.get("nonPartant")}
    json.dump(dict(t=datetime.now(ZoneInfo("Europe/Paris")).isoformat(), cotes=s), open(f"{W}/{HIP}_{date}_C{c}_{label}.json", "w")); os.remove(f"{W}/{date}_C{c}_{label}.html") if False else None
    return P, s
def analyser(P, snaps, titre=""):
    r = P["race"]; ps = [p for p in r["partants"] if not p.get("nonPartant")]; date = r["dateCourse"][:10]
    L = [f"=== COURSE {r['numero']} - {r['nomCourse']} - depart {r['heureCourse']} - {r['distance']} m - {len(ps)} partants {titre}"]
    cot = {int(p["leavingNumber"]): p.get("rapportProbable") for p in ps}
    if not all(v and v > 0 for v in cot.values()):
        L.append("  Cotes non publiees (ou incompletes) : pas de decision possible pour l'instant."); return "\n".join(L)
    df = pd.DataFrame([dict(num=int(p["leavingNumber"]), nom=p["name"], cote=cot[int(p["leavingNumber"])], avis=p.get("avisEntraineur"), crack=p.get("crackSeries") or 0, sexe=p["sexe"], age=p["age"],
                            song=p.get("song") or "", driver=p.get("driver"), ferrure=p.get("ferrure"),
                            vin=[m for m in (p.get("musics") or []) if m.get("course") and m["course"].get("key") and m["course"]["key"][:10] < date and m["course"]["key"].split("-")[3] == HIP]) for p in ps])
    df["vin_n"] = df.vin.map(len); df["vin_t3"] = df.vin.map(lambda v: sum(1 for m in v if re.match(r"[123]", m["perf"] or "")))
    df["song_t3"] = df.song.map(lambda s: sum(1 for x in re.findall(r"\b(\d+)[a-z]", s)[:5] if x in ("1", "2", "3")))
    qq = 1 / df.cote; df["p"] = qq / qq.sum(); df["lp"] = np.log(df.p); df["P3"] = p3(df.lp)
    ent = -(df.p * np.log(df.p)).sum() / np.log(len(df)); pfav = df.p.max(); lis = (pfav - ZF[0]) / ZF[1] - (ent - ZE[0]) / ZE[1]
    classe = "LISIBLE" if lis > T2 else ("MOYENNEMENT LISIBLE" if lis > T1 else "PEU LISIBLE")
    petit = len(df) <= 14; jf = bool((df.sexe == "F").all() or df.age.max() <= 6)
    profil = ("petit lot" if petit else "grand lot") + (", jeunes/femelles" if jf else ", mixte")
    df["rang"] = df.cote.rank(method="first").astype(int); df["crack_rang"] = df.crack.where(df.crack > 0, 99999).rank(method="min").astype(int)
    # mouvement de cote : premier releve valide -> dernier
    mv = {}
    if len(snaps) >= 2:
        first = next((s["cotes"] for s in snaps if all(v for v in s["cotes"].values())), None)
        if first: mv = {int(n): np.log(cot[int(n)] / first[str(n)]) if str(n) in first else np.log(cot[int(n)] / first[n]) for n in cot if (str(n) in first or n in first)}
    df["mv"] = df.num.map(mv)
    L.append(f"  Lisibilite : {classe} (indice {lis:+.2f}) | profil : {profil} | favori n°{int(df[df.rang == 1].num.iloc[0])} cote {df.cote.min():g}")
    fav = df[df.rang == 1].iloc[0]
    if classe == "PEU LISIBLE": dec = "NE PAS JOUER : course peu lisible (regle 2/7)"
    elif (not petit) and jf: dec = "NE PAS JOUER : grand lot de jeunes/femelles, profil D (regles 19/20/26)"
    elif not petit: dec = "PROFIL C (grand lot mixte) : pas de favori en simple ; jeux combines seulement avec les 3 meilleures probabilites"
    elif fav.avis == 1: dec = f"PETIT LOT mais le favori n°{int(fav.num)} a l'avis ENTRAINEUR FAVORABLE : mefiance, pas de favori en simple (regle 24) ; jeux combines possibles"
    else: dec = f"JOUER le favori n°{int(fav.num)} ({fav.nom}, cote {fav.cote:g}) : gagnant + place (regles 16/24)"
    L.append("  DECISION : " + dec)
    top = df.sort_values("P3", ascending=False)
    L.append("  Chevaux les plus probables dans les 3 (probabilite calibree sur 82 courses) :")
    for r_ in top.head(6).itertuples():
        m = "" if pd.isna(r_.mv) else (f" | cote {'RACCOURCIT' if r_.mv < -0.08 else ('DERIVE' if r_.mv > 0.08 else 'stable')} ({np.exp(r_.mv) - 1:+.0%})")
        L.append(f"    n°{r_.num:2d} {r_.nom[:22]:22s} cote {r_.cote:6g} | P(dans les 3) {r_.P3:4.0%} | avis {r_.avis} | classe Crack n°{r_.crack_rang} | forme {r_.song_t3}/5 | Vincennes {r_.vin_t3}/{r_.vin_n}{m}")
    surp = df[(df.rang >= 4) & (df.rang <= 12)].copy(); surp["pts"] = (surp.mv.fillna(0) < -0.10).astype(int) + (surp.crack_rang <= 3).astype(int) + (surp.vin_t3 >= 2).astype(int) + (surp.song_t3 >= 3).astype(int)
    s2 = surp[surp.pts >= 2].sort_values("pts", ascending=False).head(3)
    if len(s2): L.append("  Signaux de SURPRISE (cote 4-12 avec au moins 2 signaux : cote qui raccourcit, bonne classe, bon a Vincennes, bonne forme) - NON VALIDES statistiquement : " + " ; ".join(f"n°{r_.num} {r_.nom[:18]} (cote {r_.cote:g}, {r_.pts} signaux)" for r_ in s2.itertuples()))
    L.append("  Selon les tests : la cote reste l'outil le plus fiable ; ces indications aident a trier, elles ne garantissent rien.")
    return "\n".join(L)
if sys.argv[2] == "once":
    date = sys.argv[3]; import glob
    for c in [int(x) for x in sys.argv[4].split(",")]:
        label = datetime.now(ZoneInfo("Europe/Paris")).strftime("%H%M%S")
        try:
            P, s_ = snap(date, c, label); r = P["race"]
            prev = sorted(glob.glob(f"{W}/{HIP}_{date}_C{c}_*.json"))
            sn = [json.load(open(x)) for x in prev]
            print(analyser(P, sn, f"({HIP}, releve {label}, {len(sn)} releve(s))"), flush=True)
        except Exception as e: print("ERREUR", c, e, flush=True)
    sys.exit()
if sys.argv[2] == "test":
    print(analyser(page(sys.argv[3]), [], "(ESSAI A BLANC sur une course deja courue)")); sys.exit()
date = sys.argv[2]; courses = [int(x) for x in sys.argv[3].split(",")]; prog = {r["c"]: r for r in json.load(open(f"{D}/live_programme.json"))}
tz = ZoneInfo("Europe/Paris")
def at(c, off): h, m = map(int, prog[c]["heure"].split(":")); return datetime.fromisoformat(date).replace(hour=h, minute=m, tzinfo=tz) + timedelta(minutes=off)
def wait(t):
    s = (t - datetime.now(tz)).total_seconds()
    if s > 0: time.sleep(s)
plan = sorted([(at(c, off), c, lab) for c in courses for off, lab in [(-40, "m40"), (-20, "m20"), (-8, "m8"), (-2, "m2")]])
snaps = {c: [] for c in courses}
for t, c, lab in plan:
    if t < datetime.now(tz) - timedelta(minutes=3): continue
    wait(t)
    try:
        P, s = snap(date, c, lab); snaps[c].append(json.load(open(f"{W}/{date}_C{c}_{lab}.json")))
        if lab in ("m8", "m2"):
            txt = analyser(P, snaps[c], "(decision H-8 min)" if lab == "m8" else "(MISE A JOUR H-2 min)")
            open(f"{W}/reco_C{c}_{lab}.txt", "w").write(txt); print(txt, flush=True)
    except Exception as e: print("ERREUR", c, lab, e, flush=True)
