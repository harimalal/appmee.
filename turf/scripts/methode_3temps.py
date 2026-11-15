"""Methode en 3 temps (idee de Hari), regles fixees AVANT le test :
1 ecarter : aucun signal coche ET cote meritee (>=10) ET pas de course visee (pas de forte baisse de cote depuis le matin)
2 signaux faibles (perfs AVANT la course : forme, progression, correspondance, face-a-face, pas de DQ, classe)
3 s'il reste plus de 3 chevaux : departager par la cote
Variantes : A = pool non ecarte, 3 plus bas cotes ; B = pool a >=2 signaux, 3 plus bas cotes ; C = score de signaux, depart cote ; BASE = 3 plus bas cotes."""
import json, sys, itertools, numpy as np, pandas as pd
from datetime import datetime
N=sys.argv[1]
import statsmodels.api as sm
Ac=pd.read_csv(f"{N}/data/proba_top3_82.csv"); CAL=sm.GLM(Ac.y,sm.add_constant(Ac[["lp"]]),family=sm.families.Binomial()).fit()
def p3(c):
    q={k:1/v for k,v in c.items()}; t=sum(q.values()); return {k:1/(1+np.exp(-(CAL.params["const"]+CAL.params["lp"]*np.log(v/t)))) for k,v in q.items()}
H={ (r["d"],r["R"],r["C"]):r for r in map(json.loads,open(f"{N}/data/historique_courses.jsonl")) }
rows=[]; elim=[]; HOR=[]
for l in open(f"{N}/data/perfs_hist.jsonl"):
    x=json.loads(l); key=(x["d"],x["R"],x["C"]); r=H.get(key)
    if not r or not x["p"]: continue
    day=datetime.strptime(x["d"],"%d%m%Y"); cotes={int(k):v for k,v in r["cotes"].items() if v and v>0}; ref={int(k):v for k,v in (r.get("ref") or {}).items() if v}
    if len(cotes)<6: continue
    arr=[int(a) for a in r["arr"][:3]]; dist=r["dist"]; hip=r["hip"].upper()
    perf={p["numPmu"]:p["coursesCourues"] for p in x["p"]}; names={p["numPmu"]:p["nomCheval"] for p in x["p"]}; inv={v:k for k,v in names.items()}
    # allocation du jour inconnue dans le fichier collecte : approximee par la mediane des allocations recentes du lot (sinon on ignore la dimension allocation)
    def rk(c):
        for q in c["participants"]:
            if q["itsHim"]:
                pl=q["place"]; return pl["place"] if pl["statusArrivee"]=="PLACE" and pl["place"] else 12
    S={}
    for n in cotes:
        cs=[c for c in perf.get(n,[]) if datetime.fromtimestamp(c["date"]/1000)<day][:5]
        if not cs: S[n]=dict(sig=0,ok=False,det={}); continue
        rr=[rk(c) or 12 for c in cs]; det={}
        det["forme"]=any(v<=3 for v in rr[:3])
        det["progression"]=len(rr)>=3 and rr[0]<np.mean(rr[1:3]) 
        det["corresp"]=any((v<=3) and ((hip.split()[-1] in c["hippodrome"].upper()) + (abs(c["distance"]-dist)<=150))>=1 and (hip.split()[-1] in c["hippodrome"].upper() or abs(c["distance"]-dist)<=150) for c,v in zip(cs,rr))
        det["sans_dq"]=all(not any(q["itsHim"] and q["place"]["statusArrivee"]!="PLACE" for q in c["participants"]) for c in cs[:3])
        det["classe"]=any((v<=5) and c.get("allocation",0) and c["allocation"]>=r.get("alloc",0)*1.0 for c,v in zip(cs,rr)) if r.get("alloc") else False
        win=lose=0
        for c in cs:
            pres={q["nomCheval"]:q["place"] for q in c["participants"]}; me=pres.get(names[n])
            if not me or me["statusArrivee"]!="PLACE": continue
            for m,nm in names.items():
                if m!=n and m in cotes and nm in pres and pres[nm]["statusArrivee"]=="PLACE":
                    if me["place"]<pres[nm]["place"]: win+=1
                    elif me["place"]>pres[nm]["place"]: lose+=1
        det["face_a_face"]=win>lose
        S[n]=dict(sig=sum(det.values()),ok=True,det=det)
    drop={n:(cotes[n]/ref[n]-1) if n in ref else 0 for n in cotes}
    elimines=[n for n in cotes if S[n]["sig"]==0 and cotes[n]>=10 and drop[n]>-0.2]
    P=p3(cotes)
    for n in elimines: elim.append(dict(d=x["d"],cote=cotes[n],top3=int(n in arr),att=P[n]))
    for n in cotes: HOR.append(dict(d=x["d"],n=n,cote=cotes[n],top3=int(n in arr),att=P[n],sig=S[n]["sig"],**S[n]["det"]))
    low=sorted(cotes,key=lambda n:cotes[n])
    pool=[n for n in low if n not in elimines]
    A=pool[:3]
    B=[n for n in pool if S[n]["sig"]>=2][:3]
    for n in low:
        if len(B)<3 and n not in B: B.append(n)
    B3=[n for n in pool if S[n]["sig"]>=3][:3]
    for n in low:
        if len(B3)<3 and n not in B3: B3.append(n)
    C=sorted(cotes,key=lambda n:(-S[n]["sig"],cotes[n]))[:3]
    BASE=low[:3]
    sp={int(a):b/100 for a,b in r["rap"].get("SIMPLE_PLACE",[]) if str(a).isdigit()}
    cp={tuple(sorted(map(int,a.split("-")))):b/100 for a,b in r["rap"].get("COUPLE_PLACE",[]) if all(t.isdigit() for t in a.split("-"))}
    rec=dict(d=day,key=x["d"],R=r["R"],C=r["C"],hip=hip,n=len(cotes),nelim=len(elimines),npool=len(pool))
    for nm,sel in (("BASE",BASE),("A",A),("B",B),("B3",B3),("C",C)):
        rec[nm+"_hit"]=sum(n in arr for n in sel)
        rec[nm+"_cp"]=sum(cp.get(tuple(sorted(p)),0)-1 for p in itertools.combinations(sel,2))
        rec[nm+"_sp"]=sum(sp.get(n,0)-1 for n in sel)
    rows.append(rec)
df=pd.DataFrame(rows).sort_values("d"); E=pd.DataFrame(elim)
print(len(df),"courses attele,",df.hip.nunique(),"hippodromes")
print("\n== ETAPE 1 : chevaux ecartes :",len(E),"soit",f"{df.nelim.mean():.1f} par course ; dans les 3 :",f"{E.top3.mean():.1%}","(cote moyenne",f"{E.cote.mean():.0f})")
# attendu par la cote pour ces ecartes : 1/cote normalise ~ approx via taux global par tranche
print("   places attendues par la cote (calibre) :",f"{E.att.mean():.1%}")
Hd=pd.DataFrame(HOR)
print("\n== SIGNAL PAR SIGNAL : dans les 3 observe / attendu par la cote (calibre), tous partants",len(Hd))
for sg in ("forme","progression","corresp","sans_dq","classe","face_a_face"):
    a=Hd[Hd[sg]==True]; b=Hd[Hd[sg]==False]
    print(f"  {sg:12s} coche : {len(a):5d} chevaux, {a.top3.mean():.1%} observe vs {a.att.mean():.1%} attendu (x{a.top3.sum()/a.att.sum():.2f}) | non coche : {b.top3.mean():.1%} vs {b.att.mean():.1%} (x{b.top3.sum()/b.att.sum():.2f})")
print("  Nombre de signaux coches :")
for k,g in Hd.groupby("sig"): print(f"    {k} signaux : {len(g):5d} chevaux, {g.top3.mean():.1%} observe vs {g.att.mean():.1%} attendu (x{g.top3.sum()/g.att.sum():.2f})")
mid=df.d.quantile(.5)
for per,s in (("TOUT",df),("1re moitie",df[df.d<=mid]),("2e moitie",df[df.d>mid])):
    print(f"\n== {per} ({len(s)} courses)")
    for nm in ("BASE","A","B","B3","C"):
        h=s[nm+"_hit"]; cpv=s[nm+"_cp"]; spv=s[nm+"_sp"]
        print(f"  {nm:4s} dans les 3 : {h.mean():.2f}/course | couples place net {cpv.sum():+.1f} EUR sur {3*len(s)} ({cpv.sum()/(3*len(s)):+.0%}) | simples places net {spv.sum():+.1f} sur {3*len(s)} ({spv.sum()/(3*len(s)):+.0%})")
    for nm in ("B","B3","C"):
        d=s[nm+"_hit"]-s["BASE_hit"]; se=d.std()/np.sqrt(len(d)); print(f"  {nm} - BASE : {d.mean():+.3f} places/course [{d.mean()-1.96*se:+.3f} ; {d.mean()+1.96*se:+.3f}]")
df.to_pickle(f"{N}/data/methode3temps.pkl")
