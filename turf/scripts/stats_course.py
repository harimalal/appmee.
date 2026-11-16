"""Stats driver / entraineur / tandem (echantillon de carrieres en cache) + conditions de la course + cotes au depart. Usage : python3 -I stats_course.py <dossier> <AAAA-MM-JJ> <hip_letrot> <course> <A|M> [--cotes]"""
import sys, json, glob, subprocess, pandas as pd
N,DATE,HIP,C,SPEC=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]; D=f"{N}/data"
def rk(v):
    v=str(v or "").strip()
    if v.isdigit(): return int(v) if int(v)>0 else 99
    return -1 if v[:1] in "DTAR" else 99
rows=[]
for f in glob.glob(f"{D}/perfs/*.json"):
    for x in json.load(open(f)):
        if x.get("speciality")!=SPEC or x["datePerf"][:10]>=DATE: continue
        rows.append(dict(id=x["id"],date=x["datePerf"][:10],hip=str(x.get("numHippodrome")),driver=x.get("driverId"),coach=x.get("coachId"),r=rk(x.get("rang"))))
P=pd.DataFrame(rows).drop_duplicates(["id","date","hip"]); P["top3"]=((P.r>=1)&(P.r<=3)).astype(int); P["win"]=(P.r==1).astype(int); P["dq"]=(P.r==-1).astype(int)
V=P[P.hip==HIP]
race=json.load(open(f"{D}/deep/{DATE}_{HIP}_C{C}.json"))
print(f"{race['nomCourse']} | {race['discipline']} {race['distance']} m | {race['allocation']} EUR | cat {race.get('categorie')} | {race.get('conditionAge')} | {race.get('heureCourse')} | autostart {race.get('autostart')} | piste {race.get('typePiste')} corde {race.get('corde')} | Equidia {[(e['numPartant'],e['coteProb']) for e in (race.get('pronosticEquidia') or [])]}")
print(f"reference (pool {SPEC}) : tous hippodromes win {P.win.mean():.0%} place {P.top3.mean():.0%} DQ {P.dq.mean():.0%} ; ce hippodrome ({len(V)} courses) win {V.win.mean():.0%} place {V.top3.mean():.0%} DQ {V.dq.mean():.0%}")
cotes={}
if "--cotes" in sys.argv:
    dstr=DATE[8:10]+DATE[5:7]+DATE[:4]; R=sys.argv[sys.argv.index("--cotes")+1]
    t=subprocess.run(["curl","-sS","-m","30","-A","Mozilla/5.0",f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{dstr}/R{R}/C{C}/participants"],capture_output=True,text=True).stdout
    for p in json.loads(t)["participants"]: cotes[p["numPmu"]]=((p.get("dernierRapportReference") or {}).get("rapport"),(p.get("dernierRapportDirect") or {}).get("rapport"),p["statut"])
f=lambda s:f"{len(s):3d}/{s.win.mean():.0%}/{s.top3.mean():.0%}/{s.dq.mean():.0%}" if len(s) else "  0/-"
print("n | cheval | driver : tous hippo (courses/win/place/DQ) | ce hippo | entraineur : tous | ce hippo | tandem | cote matin->depart")
for p in sorted(race["partants"],key=lambda p:p["leavingNumber"]):
    if p["nonPartant"]: print(f"{p['leavingNumber']:2d} {p['name']} NON-PARTANT"); continue
    dd=P[P.driver==p["driverId"]]; dv=V[V.driver==p["driverId"]]; cd=P[P.coach==p["coachId"]]; cv=V[V.coach==p["coachId"]]; td=P[(P.driver==p["driverId"])&(P.coach==p["coachId"])]
    ck=cotes.get(p["leavingNumber"],("","",""))
    print(f"{p['leavingNumber']:2d} {p['name'][:19]:19s} | {p['driver'][:15]:15s} {f(dd)} | {f(dv)} | {p['coach'][:12]:12s} {f(cd)} | {f(cv)} | tandem {f(td)} | {ck[0]}->{ck[1]}")
