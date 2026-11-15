"""Variables AVANT COURSE par cheval, pour les 40 courses d'origine et les courses de novembre (pages letrot deja telechargees, usage prive).
Seules les courses ANTERIEURES a la date de la course sont utilisees pour la forme et l'appetence Vincennes.
Usage : python3 -I parse_features.py <dossier_courses>
"""
import sys, os, re, json, html, glob
import numpy as np, pandas as pd
B = sys.argv[1]
def rk(perf):
    m = re.match(r"(\d+|D|T|A|R)", perf or "")
    if not m: return None
    s = m.group(1)
    return int(s) if s.isdigit() else -1  # -1 = disqualifie / arrete
def rec_sec(v):
    m = re.match(r"(\d+)'(\d+)\"(\d)", v or "")
    return int(m.group(1)) * 60 + int(m.group(2)) + int(m.group(3)) / 10 if m else np.nan
def parse(f, race_id):
    raw = open(f, encoding="utf-8", errors="ignore").read()
    i = raw.find("<race-detail"); j = raw.find(':payload="', i); k = raw.find('"', j + 10)
    d = json.loads(html.unescape(raw[j + 10:k])); r = d["race"]; date = r["dateCourse"][:10]; rows = []
    for p in r["partants"]:
        if p.get("nonPartant"): continue
        prev = [(rk(m["perf"]), m["course"]["key"].split("-")[3]) for m in (p.get("musics") or []) if m.get("course") and m["course"].get("key") and m["course"]["key"][:10] < date]
        songs = [rk(s) for s in re.findall(r"\b(\d+[a-z]|[DTAR][a-z])\b", (p.get("song") or "")) if rk(s) is not None]
        vin = [x for x in prev if x[1] == "7500"]
        rows.append(dict(race=race_id, date=date, numero=p["leavingNumber"], discipline=r.get("discipline"), categorie=r.get("categorie"), allocation=r.get("allocation"),
                         distance=r.get("distance"), autostart=r.get("autostart"), partants=len([q for q in r["partants"] if not q.get("nonPartant")]),
                         sexe=p.get("sexe"), age=p.get("age"), crack=p.get("crackSeries"), avis=p.get("avisEntraineur"), ferrure=p.get("ferrure"),
                         cote=p.get("rapportProbable"), gains=float(p.get("earnings") or 0), gains_moy=float(p.get("earningsAverage") or 0), record=rec_sec(p.get("record")),
                         driver=p.get("driver"), pos=p.get("formattedRank"), n_song=len(songs), song_top3=sum(1 for s in songs[:5] if 1 <= s <= 3), song_win=sum(1 for s in songs[:5] if s == 1),
                         song_dq=sum(1 for s in songs[:5] if s == -1), n_prev5=len(prev), vin_n=len(vin), vin_top3=sum(1 for x in vin if x[0] is not None and 1 <= x[0] <= 3),
                         rentree=int(bool(p.get("isOldestLastRace"))), debut_ferre=int(bool(p.get("firstFerrure")))))
    return rows
orig, nov = [], []
for f in sorted(glob.glob(f"{B}/web/races/race_*.html")): orig += parse(f, f"o{int(os.path.basename(f).split('_')[1])}")
for f in sorted(glob.glob(f"{B}/web/nov/race_2026-*.html")):
    nom = os.path.basename(f)[5:-5]; nov += parse(f, nom.replace("_C", "-C"))
O, N = pd.DataFrame(orig), pd.DataFrame(nov)
for M in (O, N):
    M["pos"] = pd.to_numeric(M.pos, errors="coerce")
    M["race_ok"] = M.discipline == "A"
O.to_csv(f"{B}/data/feat_origine.csv", index=False); N.to_csv(f"{B}/data/feat_novembre.csv", index=False)
print(len(O), O.race.nunique(), "origine |", len(N), N.race.nunique(), "novembre")
print(O.categorie.value_counts().to_dict(), N.categorie.value_counts().to_dict())
print("vin_n > 0 :", (O.vin_n > 0).mean().round(2), (N.vin_n > 0).mean().round(2), "| n_prev5 moyen", O.n_prev5.mean().round(1), N.n_prev5.mean().round(1))
