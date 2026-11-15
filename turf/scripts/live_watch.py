"""Surveillance continue d'une course jusqu'au depart : releve des cotes PMU toutes les 20 s, enregistre la serie, alerte sur les variations >= 3 %.
Usage : python3 -I live_watch.py <dossier_courses> <JJMMAAAA> <reunion> <course>"""
import sys, json, time, subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
B, DATE, R, C = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]; tz = ZoneInfo("Europe/Paris")
base = f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{DATE}/R{R}/C{C}"; out = f"{B}/data/series/{DATE}_R{R}C{C}.json"
def get(u):
    try: return json.loads(subprocess.run(["curl", "-sS", "-m", "20", "-A", "Mozilla/5.0 (analyse privee)", u], capture_output=True, text=True).stdout)
    except Exception: return None
S = dict(depart=None, statut=None, names={}, morning={}, points=[]); prev = None; t0 = time.time()
while time.time() - t0 < 2400:
    info = get(base); P = get(base + "/participants")
    if not info or not P: time.sleep(15); continue
    now = datetime.now(tz); st = info.get("statut"); S["statut"] = st; S["depart"] = datetime.fromtimestamp(info["heureDepart"] / 1000, tz).isoformat()
    cur = {}
    for p in P["participants"]:
        if p["statut"] != "PARTANT" or not (p.get("dernierRapportDirect") or {}).get("rapport"): continue
        n = str(p["numPmu"]); cur[n] = p["dernierRapportDirect"]["rapport"]; S["names"][n] = p["nom"]
        if (p.get("dernierRapportReference") or {}).get("rapport"): S["morning"][n] = p["dernierRapportReference"]["rapport"]
    if cur:
        S["points"].append(dict(t=now.isoformat(), cotes=cur))
        if prev:
            al = [f"n°{n} {S['names'][n][:16]} {prev[n]:g} -> {cur[n]:g} ({cur[n] / prev[n] - 1:+.0%})" for n in cur if n in prev and abs(cur[n] / prev[n] - 1) >= 0.03]
            if al: print(f"[{now:%H:%M:%S}] MOUVEMENT : " + " ; ".join(al), flush=True)
        prev = cur
    json.dump(S, open(out, "w"))
    if str(st).startswith(("EN_COURS", "FIN", "ARRIVEE", "ANNULEE", "COURSE_ANNULEE")): print(f"[{now:%H:%M:%S}] DEPART / statut {st}", flush=True); break
    time.sleep(20)
print("FIN SURVEILLANCE", out)
