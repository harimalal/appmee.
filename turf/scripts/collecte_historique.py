"""Historique des courses francaises + etrangeres du programme PMU (API publique) : cotes finales, arrivee, disqualifies, VRAIS rapports (simple place, couple place, couple gagnant, 2 sur 4, trio).
Usage : python3 -I collecte_historique.py <fichier_sortie.jsonl> <jour_debut AAAA-MM-JJ> <jour_fin AAAA-MM-JJ>"""
import sys, json, time, subprocess, os
from datetime import date, timedelta
out, d0, d1 = sys.argv[1], date.fromisoformat(sys.argv[2]), date.fromisoformat(sys.argv[3])
B = "https://online.turfinfo.api.pmu.fr/rest/client/7/programme/"
def get(u):
    for _ in range(2):
        try:
            r = subprocess.run(["curl", "-sS", "-m", "25", "-A", "Mozilla/5.0 (analyse privee)", u], capture_output=True, text=True).stdout
            return json.loads(r) if r.strip() else None
        except Exception: time.sleep(1)
done = set()
if os.path.exists(out):
    for l in open(out): r = json.loads(l); done.add((r["d"], r["R"], r["C"]))
d = d1
with open(out, "a") as fo:
    while d >= d0:
        ds = d.strftime("%d%m%Y"); prog = get(B + ds); time.sleep(0.2)
        if prog:
            for r in prog["programme"]["reunions"]:
                for c in r["courses"]:
                    if (ds, r["numOfficiel"], c["numOrdre"]) in done or not str(c["statut"]).startswith("ARRIVEE_DEFINITIVE"): continue
                    base = f"{B}{ds}/R{r['numOfficiel']}/C{c['numOrdre']}"
                    info = get(base); time.sleep(0.15); P = get(base + "/participants"); time.sleep(0.15); rap = get(base + "/rapports-definitifs"); time.sleep(0.15)
                    if not info or not P: continue
                    cot = {str(p["numPmu"]): p["dernierRapportDirect"]["rapport"] for p in P["participants"] if p["statut"] == "PARTANT" and (p.get("dernierRapportDirect") or {}).get("rapport")}
                    ref = {str(p["numPmu"]): p["dernierRapportReference"]["rapport"] for p in P["participants"] if p["statut"] == "PARTANT" and (p.get("dernierRapportReference") or {}).get("rapport")}
                    rp = {}
                    if isinstance(rap, list):
                        for x in rap:
                            if x["typePari"] in ("SIMPLE_PLACE", "SIMPLE_GAGNANT", "COUPLE_PLACE", "COUPLE_GAGNANT", "DEUX_SUR_QUATRE", "TRIO"):
                                rp[x["typePari"]] = [[y["combinaison"], y["dividendePourUnEuro"]] for y in x["rapports"] if y["dividendePourUnEuro"] > 0 and "NP" not in y["combinaison"]]
                    rec = dict(d=ds, R=r["numOfficiel"], C=c["numOrdre"], hip=r["hippodrome"].get("libelleCourt"), disc=c.get("discipline"), dist=c.get("distance"), n=len(cot),
                               cotes=cot, ref=ref, arr=[x[0] for x in (info.get("ordreArrivee") or [])], dq=sum(len(i["numeroParticipants"]) for i in (info.get("incidents") or []) if "DISQUALIFIE" in i["type"]),
                               terrain=info.get("typePiste") or info.get("terrain") or info.get("penetrometre"), alloc=c.get("montantPrix"), rap=rp)
                    fo.write(json.dumps(rec) + "\n"); fo.flush()
        print(ds, flush=True); d -= timedelta(days=1)
print("FINI")
