"""Protocole TURFITUP applique MECANIQUEMENT (score calcule par le script, avant de regarder l'arrivee). Donnees PMU : 5 dernieres perfs, musique, face-a-face.
Usage : python3 -I protocole_score.py <JJMMAAAA> <R> <C>   (affiche les 3 retenus d'abord, puis seulement ensuite l'arrivee si la course est jouee)"""
import sys, json, subprocess, time
from datetime import datetime
from zoneinfo import ZoneInfo
D,R,C=sys.argv[1],sys.argv[2],sys.argv[3]; HIP=(sys.argv[4] if len(sys.argv)>4 else "VINCENNES").upper(); tz=ZoneInfo("Europe/Paris")
def get(u):
    r=subprocess.run(["curl","-sS","-m","40","-A","Mozilla/5.0 (analyse privee)",u],capture_output=True,text=True).stdout; time.sleep(1)
    try: return json.loads(r)
    except Exception: return {}
b=f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{D}/R{R}/C{C}"
info=get(b); ps=[p for p in get(b+"/participants")["participants"] if p["statut"]=="PARTANT"]; perf={p["numPmu"]:p["coursesCourues"] for p in get(b+"/performances-detaillees/pretty").get("participants",[])}
dist=info["distance"]; alloc=info["montantPrix"]; hip=info.get("hippodrome") or "VINCENNES"; day=datetime.strptime(D,"%d%m%Y").date()
noms={p["numPmu"]:p["nom"] for p in ps}
def res(c):
    for q in c["participants"]:
        if q["itsHim"]:
            pl=q["place"]; return pl["place"] if pl["statusArrivee"]=="PLACE" else "DQ"
S={}
for p in ps:
    n=p["numPmu"]; pts=0; notes=[]; pr=[]
    for c in perf.get(n,[]):
        d=datetime.fromtimestamp(c["date"]/1000,tz).date()
        if d>=day: continue                              # etape 1 : jamais les donnees du jour
        pr.append((d,c,res(c)))
    pr=pr[:5]
    # 1 tendance (recent pese plus) : 3 pts 1er, 2 pts 2e-3e, 1 pt 4e-5e ; DQ = -2
    w=[1.0,.9,.8,.7,.6]; tend=0
    for i,(d,c,r) in enumerate(pr):
        v=3 if r==1 else 2 if r in (2,3) else 1 if r in (4,5) else (-2 if r=="DQ" else 0); tend+=w[i]*v
    pts+=tend; notes.append(f"tendance {tend:.1f}")
    # 2 correspondance hippodrome / distance / allocation (3 dimensions = preuve forte)
    m3=0;m1=0
    for d,c,r in pr:
        ok_h=HIP in c["hippodrome"].upper(); ok_d=abs(c["distance"]-dist)<=150; a=c.get("allocation"); ok_a=bool(a) and 0.6*alloc<=a<=1.6*alloc
        place=isinstance(r,int) and r<=3
        k=ok_h+ok_d+ok_a
        if place and k==3: m3+=1
        elif place and k>=1: m1+=1
    pts+=2.5*m3+0.7*m1; notes.append(f"correspondance 3 dim {m3} / partielle {m1}")
    # 3 dernier DQ : retrograder
    if pr and pr[0][2]=="DQ": pts-=2; notes.append("DQ derniere sortie")
    # 4 avis entraineur favorable (R24 mais ici selon protocole : signal faible a chercher)
    if p["avisEntraineur"]=="POSITIF": pts+=1; notes.append("avis +")
    if p["driverChange"]: notes.append("driver change")
    S[n]=dict(pts=pts,pr=pr,notes=notes)
# 5 face-a-face
ff={n:0 for n in S}
for n,cs in perf.items():
    for c in cs:
        d=datetime.fromtimestamp(c["date"]/1000,tz).date()
        if d>=day: continue
        pres={q["nomCheval"]:q["place"] for q in c["participants"]}
        mine=pres.get(noms.get(n))
        if not mine or mine["statusArrivee"]!="PLACE": continue
        for m,nm in noms.items():
            if m!=n and nm in pres and pres[nm]["statusArrivee"]=="PLACE" and mine["place"]<pres[nm]["place"]: ff[n]+=1
for n in S: S[n]["pts"]+=0.4*ff[n]; S[n]["notes"].append(f"face-a-face gagnes {ff[n]}")
cotes_ref={p["numPmu"]:(p.get("dernierRapportReference") or {}).get("rapport") for p in ps}
rk=sorted(S,key=lambda n:-S[n]["pts"])
print(f"== {HIP} R{R}C{C} {D} - {info['libelle']} - {dist} m - {alloc} EUR - {len(ps)} partants")
print("RETENUS PAR LE PROTOCOLE (score, avant arrivee) :")
for i,n in enumerate(rk[:6],1): print(f"  {i}. n{n} {noms[n]:22s} score {S[n]['pts']:5.1f} | cote matin {cotes_ref[n]} | {', '.join(S[n]['notes'])}")
json.dump({str(n):dict(nom=noms[n],pts=S[n]["pts"],ref=cotes_ref[n]) for n in rk},open(f"{sys.argv[0].rsplit('/',1)[0]}/data/protoscore_{HIP}_{D}_R{R}C{C}.json","w"))
