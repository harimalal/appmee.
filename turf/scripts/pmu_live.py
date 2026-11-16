"""Lecture EN DIRECT avant course : cotes PMU (direct contre reference du matin), regles figees, probabilites d'etre dans les 3.
Usage : python3 -I pmu_live.py <dossier_courses> <JJMMAAAA> <reunion> <courses ex: 1,4>
"""
import sys, os, json, re, subprocess, time, warnings, glob
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd, statsmodels.api as sm
warnings.filterwarnings("ignore")
B, DATE, R, COURSES = sys.argv[1], sys.argv[2], sys.argv[3], [int(x) for x in sys.argv[4].split(",")]
D = f"{B}/data"; W = f"{B}/web/live"; os.makedirs(W, exist_ok=True)
O = pd.read_csv(f"{D}/feat_origine.csv"); O = O[(O.discipline == "A") & (O.cote > 0)].copy()
q = 1 / O.cote; O["p"] = q / q.groupby(O.race).transform("sum")
O["ent"] = O.groupby("race").p.transform(lambda s: -(s * np.log(s)).sum() / np.log(len(s))); O["pfav"] = O.groupby("race").p.transform("max"); Ro = O.drop_duplicates("race")
ZF, ZE = (Ro.pfav.mean(), Ro.pfav.std()), (Ro.ent.mean(), Ro.ent.std()); lis_o = (Ro.pfav - ZF[0]) / ZF[1] - (Ro.ent - ZE[0]) / ZE[1]; T1, T2 = lis_o.quantile([1 / 3, 2 / 3])
A = pd.read_csv(f"{D}/proba_top3_82.csv"); CAL = sm.GLM(A.y, sm.add_constant(A[["lp"]]), family=sm.families.Binomial()).fit()
def p3(lp): return 1 / (1 + np.exp(-(CAL.params["const"] + CAL.params["lp"] * lp)))

import unicodedata
def norm(x): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", x or "").encode("ascii", "ignore").decode().lower())
def geny_info(date_iso, hip, libelle):
    """Page Geny de la course : records, 'vient battre son record', derniers succes, changement d'entraineur, pronostics presse. Renvoie (flags par cheval, texte pronos)."""
    home = subprocess.run(["curl", "-sS", "-m", "40", "-A", "Mozilla/5.0 (analyse privee)", "https://www.geny.com/"], capture_output=True, text=True).stdout
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", libelle.lower()).encode("ascii", "ignore").decode())).strip("-")
    m = re.search(r'href="(/course/\d+-%s-%s-%s)/' % (date_iso, norm(hip), re.escape(slug)), home) or re.search(r'href="(/course/\d+-%s-[a-z0-9\-]*%s)/' % (date_iso, re.escape(slug)), home)
    if not m: return {}, "Geny : page de la course introuvable"
    time.sleep(2); raw = subprocess.run(["curl", "-sS", "-m", "40", "-A", "Mozilla/5.0 (analyse privee)", "https://www.geny.com" + m.group(1) + "/partants-pronostics"], capture_output=True, text=True).stdout
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', raw, flags=re.S); txt = "".join(json.loads('"' + c + '"') for c in chunks)
    def block(name):
        k = txt.find('"queryKey":["%s"' % name)
        if k < 0: return None
        st = txt.rfind('{"dehydratedAt"', 0, k); dep = 0
        for j in range(st, len(txt)):
            if txt[j] == "{": dep += 1
            elif txt[j] == "}":
                dep -= 1
                if dep == 0: return json.loads(txt[st:j + 1])["state"]["data"]
    fl = {}; b = block("bons-a-savoir-course") or {}
    lab = {"recordsHippodrome": "record sur la piste", "recordsDistance": "record a la distance", "viennentBattreRecord": "vient de battre son record", "derniersSuccesParcours": "a gagne sur ce parcours",
           "viennentChangerEntraineur": "change d'entraineur", "premieresFoisDeferre": "1re fois deferre", "premieresFoisOeilleres": "1res oeilleres"}
    for k, l in lab.items():
        for x in b.get(k) or []: fl.setdefault(norm(x["cheval"]["nom"]), []).append(l)
    pr = block("pronosticsCourse") or {}; pt = []
    for k in ["geny", "pronoDerniereMinute", "synthesePresse", "tableRonde"]:
        if pr.get(k): pt.append(k + " : " + " > ".join(dict.fromkeys(re.findall(r'"nom": "([^"]+)"', json.dumps(pr[k], ensure_ascii=False)))))
    if pr.get("presse"): pt.append("presse (" + str(len(pr["presse"])) + " journaux) : " + " | ".join(" > ".join(dict.fromkeys(re.findall(r'"nom": "([^"]+)"', json.dumps(j, ensure_ascii=False))))[:90] for j in pr["presse"][:6]))
    return fl, ("Pronostics Geny/presse : " + " || ".join(pt)) if pt else "Pronostics Geny/presse : pas encore publies"

def get(url):
    r = subprocess.run(["curl", "-sS", "-m", "30", "-A", "Mozilla/5.0 (analyse privee)", url], capture_output=True, text=True).stdout; time.sleep(1)
    return json.loads(r)
prog = get(f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{DATE}")
reu = next(r for r in prog["programme"]["reunions"] if r["numOfficiel"] == int(R)); nom_h = reu["hippodrome"]["libelleCourt"]
for c in COURSES:
    info = next(x for x in reu["courses"] if x["numOrdre"] == c)
    ps = [p for p in get(f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{DATE}/R{R}/C{c}/participants")["participants"] if p["statut"] == "PARTANT"]
    now = datetime.now(ZoneInfo("Europe/Paris")); dep = datetime.fromtimestamp(info["heureDepart"] / 1000, ZoneInfo("Europe/Paris"))
    L = [f"=== {nom_h} C{c} - {info.get('libelle', '')[:34]} - {info.get('discipline')} {info.get('distance')} m - depart {dep:%H:%M} (releve {now:%H:%M:%S}, depart dans {(dep - now).total_seconds() / 60:.0f} min) - {len(ps)} partants"]
    monte = info.get("discipline") != "ATTELE"
    if monte: L.append("  ATTENTION : course de trot MONTE, mes regles n'ont ete testees que sur l'ATTELE : indications par la cote seulement, sans decision.")
    if not all((p.get("dernierRapportDirect") or {}).get("rapport") for p in ps): L.append("  Cotes pas encore publiees."); print("\n".join(L)); continue
    df = pd.DataFrame([dict(num=p["numPmu"], nom=p["nom"], cote=p["dernierRapportDirect"]["rapport"], ref=(p.get("dernierRapportReference") or {}).get("rapport"), age=p["age"], sexe=p["sexe"], avis=p.get("avisEntraineur"),
                            musique=p.get("musique") or "", driver=p.get("driver"), deferre=p.get("deferre"), drvchg=p.get("driverChange"), ined=p.get("indicateurInedit")) for p in ps])
    df["mv"] = np.where(df.ref.notna(), np.log(df.cote / df.ref), np.nan)
    qq = 1 / df.cote; df["p"] = qq / qq.sum(); df["lp"] = np.log(df.p); df["P3"] = p3(df.lp); df["rang"] = df.cote.rank(method="first").astype(int)
    df["forme"] = df.musique.map(lambda m: sum(1 for t in re.findall(r"(\d|D|A|T)[a-z]", m)[:5] if t in "123"))
    df["dq"] = df.musique.map(lambda m: sum(1 for t in re.findall(r"(\d|D|A|T)[a-z]", m)[:8] if t in "DAT"))
    ent = -(df.p * np.log(df.p)).sum() / np.log(len(df)); lis = (df.p.max() - ZF[0]) / ZF[1] - (ent - ZE[0]) / ZE[1]
    classe = "LISIBLE" if lis > T2 else ("MOYENNEMENT LISIBLE" if lis > T1 else "PEU LISIBLE"); petit = len(df) <= 14
    jf = bool((df.sexe == "FEMELLES").all() or df.age.max() <= 6); fav = df[df.rang == 1].iloc[0]
    L.append(f"  Lisibilite : {classe} (indice {lis:+.2f}) | profil : {'petit lot' if petit else 'grand lot'}, {'jeunes/femelles' if jf else 'mixte'} | favori n°{fav.num} {fav.nom} cote {fav.cote:g} (matin {fav.ref:g})")
    avis_fav = str(fav.avis).upper().startswith("POSIT") or str(fav.avis).upper().startswith("FAVOR")
    if monte: dec = "MONTE : pas de regle testee ; les 3 chevaux ci-dessous sont ceux que la cote juge les plus probables"
    elif classe == "PEU LISIBLE": dec = "NE PAS JOUER : course peu lisible"
    elif (not petit) and jf: dec = "NE PAS JOUER : grand lot de jeunes/femelles (profil D)"
    elif not petit: dec = "PROFIL C (grand lot mixte) : pas de favori en simple ; jeux combines seulement"
    elif avis_fav: dec = f"PETIT LOT mais favori n°{fav.num} a avis entraineur favorable : mefiance, pas de favori en simple"
    else: dec = f"JOUER le favori n°{fav.num} ({fav.nom}, cote {fav.cote:g}) : gagnant + place"
    L.append("  DECISION : " + dec)
    # ---------- application des regles figees, une par une
    n_tr = lambda a, b: int(((df.cote >= a) & (df.cote < b)).sum())
    profil = ("D" if ((not petit) and jf) else ("C" if not petit else ("B" if jf else "A")))
    reg = []
    reg.append(f"R2/R7 lisibilite : {classe} (indice {lis:+.2f}) -> " + ("course a ECARTER" if classe == "PEU LISIBLE" else "course jouable"))
    reg.append(f"R19/R20/R26 profil {profil} ({'petit' if petit else 'grand'} lot {len(df)} partants, {'jeunes/femelles' if jf else 'mixte'}) -> " + {"A": "profil n°1, favori jouable", "B": "favori jouable avec prudence", "C": "pas de favori en simple, jeux combines seulement", "D": "A EVITER"}[profil])
    reg.append(f"R16/R24 favori n°{fav.num} {fav.nom} cote {fav.cote:g}, avis {fav.avis} -> " + ("SANS OBJET : course ecartee par R2/R7 ou R20 ; " if (classe == "PEU LISIBLE" or profil == "D") else "") + ("a jouer (petit lot, avis non favorable)" if (petit and not avis_fav) else ("mefiance : avis favorable (regle fragile)" if petit else "pas de favori en simple en grand lot")))
    out40 = df[df.cote > 40]; reg.append(f"R8 cotes > 40 : {len(out40)} cheval(aux) exclu(s)" + (" (" + ", ".join(f"n°{x}" for x in out40.num) + ")" if len(out40) else ""))
    reg.append(f"R17/R18 outsiders : 80 % des top 4 comptent un cheval de cote >= 20 ; ici {n_tr(5, 10)} chevaux de cote 5-10, {n_tr(10, 20)} de 10-20, {n_tr(20, 40)} de 20-40 pour la couverture")
    reg.append("R29/R27/R28 : pas de bonus ni de malus pour l'experience de la piste, la classe Crack, la ferrure (deja dans la cote)")
    reg.append("R31 : probabilites du modele (cote + signaux) = calibrage sur 82 courses ; elles ne battent pas la cote")
    reg.append("R33 (piste, non validee) : cote qui raccourcit = signal positif ; cote qui derive = prudence")
    comb = {"A": "base = favori (cote < 5) + chevaux de cote 5-20 (environ 7) + 1 ou 2 de cote 20-40 pour le quarte", "B": "meme schema que A, en elargissant aux cotes 20-30", "C": "pas de base favori ; couvrir les cotes 4-30 + 1 cheval de cote 20-40", "D": "a eviter"}[profil]
    cand = df[df.cote <= 40].sort_values("P3", ascending=False)
    if monte: ret = "monte : regles non testees"
    elif classe == "PEU LISIBLE" or profil == "D": ret = "AUCUN (course a ne pas jouer) ; a titre indicatif : " + ", ".join(f"n°{r.num} {r.nom[:14]} ({r.cote:g})" for r in cand.head(3).itertuples())
    elif profil in ("A", "B") and not avis_fav: ret = f"favori n°{fav.num} + " + ", ".join(f"n°{r.num} {r.nom[:14]} ({r.cote:g})" for r in cand[(cand.rang > 1)].head(2).itertuples())
    else: ret = ", ".join(f"n°{r.num} {r.nom[:14]} ({r.cote:g})" for r in cand.head(3).itertuples()) + (" (sans favori en simple)" if profil == "C" or avis_fav else "")
    L.append("  REGLES APPLIQUEES :"); L += ["    - " + x for x in reg]
    L.append(f"  Combinaison type du profil {profil} : {comb}"); L.append(f"  CHEVAUX RETENUS PAR LES REGLES : {ret}")
    if nom_h != "VINCENNES": L.append(f"  ATTENTION : {nom_h} n'est pas Vincennes : toutes ces regles ont ete etablies sur Vincennes et ne sont pas validees ici.")
    try: GF, GP = geny_info(datetime.strptime(DATE, "%d%m%Y").strftime("%Y-%m-%d"), nom_h, info.get("libelle", ""))
    except Exception as e: GF, GP = {}, "Geny indisponible (" + str(e)[:50] + ")"
    L.append("  " + GP)
    L.append("  Les plus probables dans les 3 (proba calibree sur 82 courses de Vincennes ; mouvement = cote maintenant contre cote du matin) :")
    for r in df.sort_values("P3", ascending=False).head(6).itertuples():
        mv = "" if pd.isna(r.mv) else f" | {'RACCOURCIT' if r.mv < -0.08 else ('DERIVE' if r.mv > 0.08 else 'stable')} ({np.exp(r.mv) - 1:+.0%}, matin {r.ref:g})"
        L.append(f"    n°{r.num:2d} {r.nom[:22]:22s} cote {r.cote:6g} | P3 {r.P3:4.0%} | avis {r.avis} | forme {r.forme}/5 | fautes {r.dq}/8 | driver {r.driver}{mv}" + (" | Geny : " + ", ".join(GF[norm(r.nom)]) if norm(r.nom) in GF else ""))
    sur = df[(df.rang >= 4) & (df.rang <= 12)].copy(); sur["pts"] = (sur.mv.fillna(0) < -0.10).astype(int) + (sur.forme >= 3).astype(int) + (sur.dq == 0).astype(int) + (sur.avis.astype(str).str.upper().str.startswith("POSIT")).astype(int)
    s2 = sur[sur.pts >= 3].sort_values("pts", ascending=False).head(3)
    if len(s2): L.append("  A SURVEILLER (cote 4-12, au moins 3 signaux : cote qui raccourcit, bonne forme, pas de faute, avis favorable) - signaux NON valides statistiquement : " + " ; ".join(f"n°{r.num} {r.nom[:18]} (cote {r.cote:g})" for r in s2.itertuples()))
    mm = df[df.mv < -0.15].sort_values("mv").head(3)
    if len(mm): L.append("  Plus fortes baisses de cote depuis le matin : " + " ; ".join(f"n°{r.num} {r.nom[:16]} {r.ref:g} -> {r.cote:g}" for r in mm.itertuples()))
    L.append("  Rappel : selon les tests, la cote reste l'outil le plus fiable ; ceci aide a trier, sans garantie.")
    txt = "\n".join(L); print(txt, flush=True); open(f"{W}/pmu_{DATE}_R{R}_C{c}_{now:%H%M%S}.txt", "w").write(txt)
