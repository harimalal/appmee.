"""Temps de fin des courses precedentes (letrot.com, usage prive, 1 page / 3 s). La page est lue puis effacee ; seuls les temps sont gardes.
Usage : python3 -I fetch_precedentes.py <dossier_data> <dossier_tmp>
"""
import sys, os, json, html, re, time, subprocess
D, T = sys.argv[1], sys.argv[2]
os.makedirs(T, exist_ok=True)
keys = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else sorted({r[4] for r in json.load(open(f"{D}/courses_precedentes.json"))})
out = f"{D}/temps_precedents.jsonl"
done = set()
if os.path.exists(out):
    for l in open(out): done.add(json.loads(l)["key"])
def sec(v):
    m = re.search(r"(\d+):(\d+)\.(\d)$", v or "")
    return int(m.group(1)) * 60 + int(m.group(2)) + int(m.group(3)) / 10 if m else None
with open(out, "a") as fo:
    for n, key in enumerate(keys):
        if key in done: continue
        y, m, d, h, c = key.split("-")
        f = f"{T}/page.html"
        code = subprocess.run(["curl", "-sS", "-m", "60", "-A", "Mozilla/5.0 (analyse privee)", "-o", f, "-w", "%{http_code}",
                               f"https://www.letrot.com/courses/{y}-{m}-{d}/{h}/{c}"], capture_output=True, text=True).stdout
        rec = {"key": key, "http": code, "runners": []}
        try:
            raw = open(f, encoding="utf-8", errors="ignore").read()
            i = raw.find("<race-detail"); j = raw.find(':payload="', i); k = raw.find('"', j + 10)
            dd = json.loads(html.unescape(raw[j + 10:k])); race = dd["race"]
            rec.update(distance=race.get("distance"), autostart=race.get("autostart"), discipline=race.get("discipline") or race.get("specialite"),
                       partants=len(race.get("partants") or []))
            for hid, t in (dd.get("trackings") or {}).items():
                rec["runners"].append(dict(horse_id=hid, rang=t.get("rank"), cote=t.get("rapportProbable"), crack=t.get("crackSeries"),
                    last1000=sec(t.get("reductionLast1000")), last500=sec(t.get("reductionLast500")), r1000_500=sec(t.get("reduction1000500")),
                    cl_1000_500=t.get("classement1000500"), dist_premier=t.get("distanceRapportPremier")))
            rec["red"] = {p.get("id"): p.get("reduction") for p in race.get("partants") or []}
        except Exception as e:
            rec["err"] = str(e)[:100]
        fo.write(json.dumps(rec) + "\n"); fo.flush()
        if os.path.exists(f): os.remove(f)
        if n % 50 == 0: print(n, len(keys), key, code, len(rec["runners"]), flush=True)
        time.sleep(3)
print("FINI")
