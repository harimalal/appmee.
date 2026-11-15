"""Protocole TURFITUP applique a une course AVANT depart (donnees PMU : musique, 5 dernieres performances detaillees, face-a-face, correspondance).
Usage : python3 -I protocole_turfitup.py <JJMMAAAA> <R> <C>"""
import sys, json, subprocess, time
from datetime import datetime
from zoneinfo import ZoneInfo
D,R,C=sys.argv[1],sys.argv[2],sys.argv[3]; tz=ZoneInfo("Europe/Paris")
def get(u):
    r=subprocess.run(["curl","-sS","-m","40","-A","Mozilla/5.0 (analyse privee)",u],capture_output=True,text=True).stdout; time.sleep(1); return json.loads(r)
b=f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{D}/R{R}/C{C}"
info=get(b); ps=[p for p in get(b+"/participants")["participants"] if p["statut"]=="PARTANT"]; perf={p["numPmu"]:p["coursesCourues"] for p in get(b+"/performances-detaillees/pretty")["participants"]}
dist=info["distance"]; alloc=info["montantPrix"]; hip="VINCENNES"
print(f"{info['libelle']} - {info['discipline']} {dist} m - {alloc} EUR - {info['nombreDeclaresPartants']} partants - depart {datetime.fromtimestamp(info['heureDepart']/1000,tz):%d/%m %H:%M} - {info.get('categorieParticularite')}")
noms={p["numPmu"]:p["nom"] for p in ps}
def rang(c,n):
    for q in c["participants"]:
        if q["itsHim"]: 
            pl=q["place"]; return pl["place"] if pl["statusArrivee"]=="PLACE" else ("DQ" if "DISQ" in str(pl["statusArrivee"]) else str(pl["statusArrivee"])[:4])
rows={}
for p in ps:
    n=p["numPmu"]; cs=perf.get(n,[])
    L=[]
    for c in cs[:5]:
        r=rang(c,n); L.append((datetime.fromtimestamp(c["date"]/1000,tz).strftime("%d/%m/%y"),c["hippodrome"][:10],c["discipline"][:2],c["distance"],c["allocation"],r,c["nbParticipants"]))
    rows[n]=dict(nom=p["nom"],age=p["age"],sexe=p["sexe"][0],driver=p["driver"],ent=p["entraineur"],avis=p["avisEntraineur"],defer=p["deferre"],corde=p.get("placeCorde"),musique=p["musique"],nc=p["nombreCourses"],nv=p["nombreVictoires"],np_=p["nombrePlaces"],gains=p["gainsParticipant"]["gainsCarriere"]/100,g_an=p["gainsParticipant"]["gainsAnneeEnCours"]/100,
       dchg=p["driverChange"],perfs=L,ref=(p.get("dernierRapportReference") or {}).get("rapport"),cote=(p.get("dernierRapportDirect") or {}).get("rapport"))
json.dump(rows,open(f"{sys.argv[0].rsplit('/',1)[0]}/data/proto_{D}_R{R}C{C}.json","w"),ensure_ascii=False,default=str)
for n,r in sorted(rows.items()):
    print(f"\n#{n} {r['nom']} ({r['age']}{r['sexe']}) driver {r['driver']} / ent {r['ent']} | avis {r['avis']} | {r['defer']} | corde {r['corde']} | musique {r['musique'][:22]} | {r['nv']}V/{r['np_']}P sur {r['nc']} | gains {r['gains']:,.0f} (annee {r['g_an']:,.0f}) | driver change {r['dchg']} | cote matin {r['ref']}")
    for x in r["perfs"]: print("    ",x)
# face-a-face entre partants du jour
print("\n--- FACE-A-FACE (courses passees ou 2 partants d'aujourd'hui se sont rencontres) ---")
seen=set()
for n,cs in perf.items():
    for c in cs:
        key=(c["date"],c["hippodrome"])
        if key in seen: continue
        pres=[q for q in c["participants"] if q["nomCheval"] in noms.values()]
        if len(pres)>=2:
            seen.add(key); print(datetime.fromtimestamp(c["date"]/1000,tz).strftime("%d/%m/%y"),c["hippodrome"],c["distance"],"m :"," > ".join(f"{q['nomCheval']}({q['place']['place'] if q['place']['statusArrivee']=='PLACE' else 'DQ/Autre'})" for q in sorted(pres,key=lambda q:(q['place']['place'] or 99))))
