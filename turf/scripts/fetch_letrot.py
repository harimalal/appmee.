"""Recupere, pour les 40 courses a lot complet, la page course letrot.com (usage prive, rythme lent : 1 page / 3 s).
Usage : python3 -I fetch_letrot.py <json_open_pmu> <dossier_sortie>
"""
import sys, json, time, os, subprocess
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
races = sorted(json.load(open(src))["message"], key=lambda r: (r["date"], r["r/c"]))
todo = []
for i, r in enumerate(races):
    if not r.get("partants_details"): continue
    reu, crs = r["r/c"].replace("R", "").split("/C")
    todo.append((i, r["date"], int(crs)))
for i, date, crs in todo:
    f = f"{out}/race_{i}_{date}_C{crs}.html"
    if os.path.exists(f) and os.path.getsize(f) > 100000: continue
    url = f"https://www.letrot.com/courses/{date}/7500/{crs}"
    code = subprocess.run(["curl", "-sS", "-m", "40", "-A", "Mozilla/5.0 (analyse privee)", "-o", f, "-w", "%{http_code}", url],
                          capture_output=True, text=True).stdout
    print(i, date, crs, code, os.path.getsize(f) if os.path.exists(f) else 0, flush=True)
    time.sleep(3)
