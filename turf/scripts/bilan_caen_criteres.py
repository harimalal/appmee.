import sys, json, re, subprocess, time, unicodedata
import numpy as np, pandas as pd
from datetime import datetime
N=sys.argv[1]; DATE="14112026"; R=8
src=open(f"{N}/pmu_live.py").read().split("\n")
exec("\n".join(src[18:46]))   # norm + geny_info
def get(u):
    r=subprocess.run(["curl","-sS","-m","30","-A","Mozilla/5.0 (analyse privee)",u],capture_output=True,text=True).stdout; time.sleep(1); return json.loads(r)
base=f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{DATE}"
prog=get(base); reu=next(r for r in prog["programme"]["reunions"] if r["numOfficiel"]==R)
rows=[]
for c in range(4,10):
    info=next(x for x in reu["courses"] if x["numOrdre"]==c)
    full=get(f"{base}/R{R}/C{c}"); arr=[x[0] if isinstance(x,list) else x for x in (full.get("ordreArrivee") or [])]
    dqn=set(); 
    for i in full.get("incidents") or []:
        if i["type"].startswith("DISQ"): dqn|=set(i["numeroParticipants"])
    ps=[p for p in get(f"{base}/R{R}/C{c}/participants")["participants"] if p["statut"]=="PARTANT"]
    try: GF,_=geny_info("2026-11-14","CAEN",info.get("libelle",""))
    except Exception as e: GF={}
    n=len(ps)
    for p in ps:
        m=p.get("musique") or ""; num=p["numPmu"]
        fl=GF.get(norm(p["nom"]),[])
        rows.append(dict(C=c,disc=info["discipline"],n=n,num=num,nom=p["nom"],cote=(p.get("dernierRapportDirect") or {}).get("rapport"),ref=(p.get("dernierRapportReference") or {}).get("rapport"),
          avis=str(p.get("avisEntraineur") or "").upper(),forme=sum(1 for t in re.findall(r"(\d|D|A|T)[a-z]",m)[:5] if t in "123"),
          fautes=sum(1 for t in re.findall(r"(\d|D|A|T)[a-z]",m)[:8] if t in "DAT"),drvchg=bool(p.get("driverChange")),deferre=p.get("deferre"),ined=p.get("indicateurInedit"),
          rec_piste="record sur la piste" in fl,rec_dist="record a la distance" in fl,bat_rec="vient de battre son record" in fl,succes="a gagne sur ce parcours" in fl,
          defer1="1re fois deferre" in fl,chg_ent="change d'entraineur" in fl,geny_any=len(fl)>0,
          rang=(arr.index(num)+1) if num in arr else 99,dq=num in dqn,places=3))
df=pd.DataFrame(rows); df["top3"]=(df.rang<=3).astype(int); df["win"]=(df.rang==1).astype(int)
q=1/df.cote; df["p"]=q/q.groupby([df.C]).transform("sum"); df["att"]=np.minimum(df.p*3,0.95)  # places attendues approx. selon la cote (controle)
df.to_pickle(f"{N}/data/caen_criteres.pkl")
print(len(df),"partants,",df.groupby("C").size().to_dict(),"| Geny trouve pour",df.groupby("C").geny_any.sum().to_dict())
print("hors-classement (disqualifies) :",df[df.dq][["C","num","nom"]].values.tolist())
def crit(name,mask):
    a=df[mask]; b=df[~mask]
    if len(a)==0: print(f"{name:34s} aucun"); return
    print(f"{name:34s} {len(a):3d} chevaux | dans les 3 : {a.top3.sum():2d} ({a.top3.mean():3.0%}) | gagne : {a.win.sum()} | disq : {a.dq.sum()} || sans le critere {b.top3.mean():3.0%} | place attendue par la cote {a.att.mean():3.0%}")
print("\nBase : 1 cheval sur", round(1/df.top3.mean(),1),"finit dans les 3 ->",f"{df.top3.mean():.0%}")
crit("avis entraineur POSITIF",df.avis.str.startswith("POSIT"))
crit("forme >=3 places sur 5",df.forme>=3)
crit("forme 0 place sur 5",df.forme==0)
crit("0 faute sur 8 dernieres",df.fautes==0)
crit(">=2 fautes sur 8 dernieres",df.fautes>=2)
crit("Geny : record sur la piste",df.rec_piste)
crit("Geny : record a la distance",df.rec_dist)
crit("Geny : vient de battre son record",df.bat_rec)
crit("Geny : a gagne sur ce parcours",df.succes)
crit("Geny : 1re fois deferre",df.defer1)
crit("Geny : au moins un signal",df.geny_any)
crit("Geny : aucun signal",~df.geny_any)
crit("changement de driver",df.drvchg)
crit("cote > 40 (regle R8 : exclus)",df.cote>40)
a=df[df.disc=="ATTELE"]
print("\n--- Attele seul (5 courses) ---")
df=a; crit("avis POSITIF",df.avis.str.startswith("POSIT")); crit("forme >=3/5",df.forme>=3); crit("0 faute/8",df.fautes==0); crit(">=2 fautes/8",df.fautes>=2); crit("Geny : record piste",df.rec_piste); crit("Geny : record distance",df.rec_dist)
# cumul de criteres
df["score"]=df.avis.str.startswith("POSIT").astype(int)+(df.forme>=3).astype(int)+(df.fautes==0).astype(int)+df.rec_piste.astype(int)+df.rec_dist.astype(int)+df.bat_rec.astype(int)
print("\nCumul de criteres favorables (avis+, forme>=3, 0 faute, record piste, record distance, bat son record) :")
for s,g in df.groupby("score"): print(f"  score {s} : {len(g):2d} chevaux, dans les 3 : {g.top3.sum()} ({g.top3.mean():.0%}), attendu par la cote {g.att.mean():.0%}")
print("\nPar course : les 3 premiers de l'arrivee et leurs criteres")
for c,g in df.groupby("C"):
    for r in g[g.rang<=3].sort_values("rang").itertuples():
        print(f"  C{c} {r.rang}er {r.nom[:20]:20s} cote {r.cote:g} | avis {r.avis[:5]} forme {r.forme}/5 fautes {r.fautes}/8 | rec piste {'o' if r.rec_piste else '-'} dist {'o' if r.rec_dist else '-'} bat rec {'o' if r.bat_rec else '-'}")
