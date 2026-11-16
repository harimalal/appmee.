"""Fiche de synthese d'une course, TOUJOURS au meme format. Identifiant : HIPPODROME R<reunion>C<course>.
1. Chevaux a 5 min du depart  2. A 3 min, mouvements de cote significatifs  3. Chevaux prevus + cote finale  4. Arrivee  5. Rapports officiels (simples, couples, 2 sur 4, trio) + resultat de mes couples
Usage : python3 -I fiche_course.py <dossier_courses> <JJMMAAAA> <reunion> <course> [--prevus 13,4,3]
Les releves viennent de data/series/<date>_R<r>C<c>.json (surveillance toutes les 20 s) ; sinon un fichier manuel data/series/manuel_<date>_R<r>C<c>.json.
"""
import sys, os, json, subprocess, re, warnings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd, statsmodels.api as sm
warnings.filterwarnings("ignore")
B, DATE, R, C = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]; D = f"{B}/data"; tz = ZoneInfo("Europe/Paris")
PREV = [int(x) for x in sys.argv[sys.argv.index("--prevus") + 1].split(",")] if "--prevus" in sys.argv else None
def get(u):
    try: return json.loads(subprocess.run(["curl", "-sS", "-m", "30", "-A", "Mozilla/5.0 (analyse privee)", u], capture_output=True, text=True).stdout)
    except Exception: return None
A = pd.read_csv(f"{D}/proba_top3_82.csv"); CAL = sm.GLM(A.y, sm.add_constant(A[["lp"]]), family=sm.families.Binomial()).fit()
def p3(cotes):
    q = np.array([1 / v for v in cotes.values()]); p = q / q.sum(); lp = np.log(p); P = 1 / (1 + np.exp(-(CAL.params["const"] + CAL.params["lp"] * lp)))
    return dict(zip(cotes.keys(), P))
base = f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{DATE}/R{R}/C{C}"; prog = get(f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{DATE}")
reu = next(r for r in prog["programme"]["reunions"] if r["numOfficiel"] == int(R)); hip = reu["hippodrome"]["libelleCourt"]; info = get(base) or {}
cinfo = next(c for c in reu["courses"] if c["numOrdre"] == int(C))
f_auto, f_man = f"{D}/series/{DATE}_R{R}C{C}.json", f"{D}/series/manuel_{DATE}_R{R}C{C}.json"
S = json.load(open(f_man if os.path.exists(f_man) else f_auto)); approx = os.path.exists(f_man)
dep = datetime.fromisoformat(S["depart"]) if S.get("depart") else datetime.fromtimestamp(cinfo["heureDepart"] / 1000, tz)
pts = [(datetime.fromisoformat(p["t"]), {str(k): v for k, v in p["cotes"].items()}) for p in S["points"]]
def at(minutes):
    cible = dep - timedelta(minutes=minutes); c = [p for p in pts if p[0] <= cible] or pts[:1]
    return c[-1] if c else None
t5, t3, fin = (pts[0], pts[1], pts[2]) if approx else (at(5), at(3), pts[-1])
names, morning = S["names"], S["morning"]
def fm(v): return "" if v in ("", None) else f"{v:g}"
def mv(a, b): return f"{b / a - 1:+.0%}" if a else ""
ident = f"{hip} R{R}C{C}"
L = [f"## {ident} - {cinfo.get('libelle', '')} - {cinfo.get('discipline')} {cinfo.get('distance')} m - depart {dep:%H:%M} - {cinfo.get('nombreDeclaresPartants')} partants"]
if approx: L.append("*Releves approximatifs : les cotes sont celles des relevés les plus proches de T-5 et T-3 (surveillance continue non disponible pour cette course).*")
P5, P3_ = p3(t5[1]), p3(t3[1]); ordre = sorted(t3[1], key=lambda n: -P3_[n])
L += ["", f"### 1. Chevaux a 5 min du depart (releve {t5[0]:%H:%M:%S})", "", "| N° | Cheval | Cote T-5 | Cote matin | Mvt vs matin | P(dans les 3) |", "|---|---|---|---|---|---|"]
for n in sorted(t5[1], key=lambda n: -P5[n])[:8]: L.append(f"| {n} | {names[n]} | {t5[1][n]:g} | {fm(morning.get(n))} | {mv(morning.get(n), t5[1][n])} | {P5[n]:.0%} |")
L += ["", f"### 2. A 3 min du depart (releve {t3[0]:%H:%M:%S}) - mouvements significatifs (>= 5 % depuis T-5 ou >= 15 % depuis le matin)", "", "| N° | Cheval | Cote T-5 | Cote T-3 | Mvt T-5 -> T-3 | Mvt depuis le matin | Signal |", "|---|---|---|---|---|---|---|"]
sig = []
for n in t3[1]:
    a, b, m0 = t5[1].get(n), t3[1][n], morning.get(n)
    d1 = b / a - 1 if a else 0; d0 = b / m0 - 1 if m0 else 0
    if abs(d1) >= 0.05 or abs(d0) >= 0.15 or n in ordre[:3]: sig.append((n, a, b, d1, d0))
for n, a, b, d1, d0 in sorted(sig, key=lambda x: x[2]):
    flag = "BAISSE" if (d1 <= -0.05 or d0 <= -0.15) else ("HAUSSE" if (d1 >= 0.05 or d0 >= 0.15) else "stable")
    L.append(f"| {n} | {names[n]} | {fm(a)} | {b:g} | {d1:+.0%} | {d0:+.0%} | {flag} |")
prevus = PREV or ordre[:3]; prevus = [str(x) for x in prevus]
L += ["", "### 3. Chevaux prevus (3 plus probables a T-3) et cote finale", "", "| Rang prevu | N° | Cheval | Cote T-5 | Cote T-3 | Cote au depart | P(dans les 3) |", "|---|---|---|---|---|---|---|"]
for i, n in enumerate(prevus, 1): L.append(f"| {i} | {n} | {names[n]} | {fm(t5[1].get(n))} | {fm(t3[1].get(n))} | {fm(fin[1].get(n))} | {P3_.get(n, 0):.0%} |")
arr = info.get("ordreArrivee") or []; inc = info.get("incidents") or []; ordre_arr = [str(x[0]) if isinstance(x, list) else str(x) for x in arr]
L += ["", f"### 4. Arrivee ({info.get('statut')})", ""]
if ordre_arr:
    L += ["| Rang | N° | Cheval | Cote au depart | Prevu ? |", "|---|---|---|---|---|"]
    for i, n in enumerate(ordre_arr[:5], 1): L.append(f"| {i} | {n} | {names.get(n, '?')} | {fm(fin[1].get(n))} | {'oui' if n in prevus else ''} |")
    for x in inc:
        if x["type"] != "NON_PARTANT": L.append(f"\nIncident : {x['type']} - n° {', '.join(map(str, x['numeroParticipants']))}")
else: L.append("Arrivee pas encore connue.")
rap = get(base + "/rapports-definitifs"); L += ["", "### 5. Rapports officiels (pour 1 euro)", ""]
def eur(c): return f"{c / 100:.2f} EUR"
pairs = [tuple(sorted((a, b), key=int)) for i, a in enumerate(prevus) for b in prevus[i + 1:]]
if isinstance(rap, list) and rap:
    tab = {x["typePari"]: x["rapports"] for x in rap}
    def one(t, lab):
        v = [(r["combinaison"], r["dividendePourUnEuro"]) for r in tab.get(t, []) if "NP" not in r["combinaison"] and r["dividendePourUnEuro"] > 0]
        return f"| {lab} | " + " ; ".join(f"{c} : {eur(d)}" for c, d in v) + " |"
    L += ["| Pari | Combinaison : rapport |", "|---|---|", one("SIMPLE_GAGNANT", "Simple gagnant"), one("SIMPLE_PLACE", "Simple place"), one("COUPLE_GAGNANT", "Couple gagnant"), one("COUPLE_PLACE", "Couple place"), one("DEUX_SUR_QUATRE", "2 sur 4"), one("TRIO", "Trio")]
    def pay(t, pr):
        k = "-".join(sorted(pr, key=int)); return next((r["dividendePourUnEuro"] for r in tab.get(t, []) if "NP" not in r["combinaison"] and "-".join(sorted(r["combinaison"].split("-"), key=int)) == k and r["dividendePourUnEuro"] > 0), 0)
    L += ["", "**Mes couples prevus (1 euro chacun)**", "", "| Couple | Couple place | 2 sur 4 | Gain net (couple place + 2 sur 4 = 2 euros) |", "|---|---|---|---|"]
    tot = 0
    for pr in pairs:
        cp, d4 = pay("COUPLE_PLACE", pr), pay("DEUX_SUR_QUATRE", pr); g = (cp + d4) / 100 - 2; tot += g
        L.append(f"| {'-'.join(pr)} | {eur(cp) if cp else 'perdu'} | {eur(d4) if d4 else 'perdu'} | {g:+.2f} EUR |")
    sg = pay("SIMPLE_GAGNANT", (prevus[0],)) if False else next((r["dividendePourUnEuro"] for r in tab.get("SIMPLE_GAGNANT", []) if r["combinaison"] == prevus[0] and r["dividendePourUnEuro"] > 0), 0)
    L.append(f"\nTotal des 3 couples (couple place + 2 sur 4) : mise {2 * len(pairs)} EUR, gain net {tot:+.2f} EUR. Prevu n°1 (n°{prevus[0]}) au simple gagnant : {eur(sg) if sg else 'perdu'}.")
else: L.append("Rapports officiels pas encore publies.")
txt = "\n".join(L); print(txt); open(f"{D}/fiches/{hip.replace(' ', '_')}_R{R}C{C}.md", "w").write(txt)
