"""Extrait des pages course letrot.com : Crack Series au partant, ferrure, avis entraineur, cote PMU finale de tous les partants,
indicateurs avant course, et temps de passage (apres course, pour l'historique uniquement).
Usage : python3 -I parse_letrot.py <dossier_pages> <dossier_data>
"""
import sys, os, re, json, html, glob
import pandas as pd
src, D = sys.argv[1], sys.argv[2]
rows, sect = [], []
def sec(v):
    if not v: return None
    m = re.search(r"(\d+):(\d+)\.(\d)$", v)  # "1970-01-01 00:01:11.1" -> 71.1 s/km
    return int(m.group(1)) * 60 + int(m.group(2)) + int(m.group(3)) / 10 if m else None
for f in sorted(glob.glob(f"{src}/race_*.html")):
    race_id = int(os.path.basename(f).split("_")[1])
    raw = open(f, encoding="utf-8", errors="ignore").read()
    i = raw.find("<race-detail"); j = raw.find(':payload="', i); k = raw.find('"', j + 10)
    d = json.loads(html.unescape(raw[j + 10:k]))
    race = d["race"]
    for p in race["partants"]:
        rows.append(dict(
            race_id=race_id, letrot_race=race["id"], numero=p.get("leavingNumber"), cheval_letrot=p.get("name"),
            crack_series=p.get("crackSeries"), ferrure=p.get("ferrure"), first_ferrure=int(bool(p.get("firstFerrure"))),
            avis_entraineur=p.get("avisEntraineur"), cote_pmu_letrot=p.get("rapportProbable"), favori_pmu=int(bool(p.get("favoris"))),
            non_partant=int(bool(p.get("nonPartant"))), rang_letrot=p.get("formattedRank"),
            gains_moyens=p.get("earningsAverage"), age_letrot=p.get("age"),
            rentree=int(bool(p.get("isOldestLastRace"))), course_rapprochee=int(bool(p.get("courseRapprochee"))),
            premier_gp=int(bool(p.get("firstGP"))), changement_entraineur=int(bool(p.get("changementEntraineur"))),
            premier_driver=int(bool(p.get("firstJockey"))), premier_autostart=int(bool(p.get("firstAutostart"))),
            autostart=race.get("autostart"), categorie=race.get("categorie"), quinte=int(bool(race.get("quinte")))))
    for hid, t in (d.get("trackings") or {}).items():
        sect.append(dict(race_id=race_id, date=race["dateCourse"], numero=t.get("leavingNumber"), cheval_letrot=t.get("horseName"),
                         horse_id=hid, rang=t.get("rank"), last1000=sec(t.get("reductionLast1000")), last500=sec(t.get("reductionLast500")),
                         cl_1000_500=t.get("classement1000500"), dist_premier=t.get("distanceRapportPremier")))
L = pd.DataFrame(rows); S = pd.DataFrame(sect)
L.to_csv(f"{D}/letrot_partants.csv", index=False); S.to_csv(f"{D}/letrot_temps_passage.csv", index=False)
print(len(L), "partants letrot |", L.race_id.nunique(), "courses |", "crack_series renseigne :", L.crack_series.notna().sum(),
      "| =0 :", (L.crack_series == 0).sum())
print(L[["crack_series", "cote_pmu_letrot", "avis_entraineur"]].describe().round(1).to_string())
print(L.ferrure.value_counts().head(10).to_dict()); print(L.avis_entraineur.value_counts().to_dict())
print(len(S), "temps de passage |", S.last500.notna().sum(), "avec dernier 500 m")
