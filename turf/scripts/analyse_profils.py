import json, sys, numpy as np, pandas as pd
from datetime import datetime
D=sys.argv[1]
rows=[]
for l in open(f"{D}/data/historique_courses.jsonl"):
    r=json.loads(l)
    if not r.get("cotes") or not r.get("arr") or not r.get("rap"): continue
    c={k:v for k,v in r["cotes"].items() if v and v>0}
    if len(c)<4: continue
    rap=r["rap"]
    sp={a:b for a,b in rap.get("SIMPLE_PLACE",[]) if a.isdigit()}
    cp={tuple(sorted(a.split("-"),key=int)):b for a,b in rap.get("COUPLE_PLACE",[]) if all(x.isdigit() for x in a.split("-"))}
    if not sp: continue
    ordre=sorted(c,key=lambda k:c[k]); q=np.array([1/c[k] for k in ordre]); p=q/q.sum()
    ent=-(p*np.log(p)).sum()/np.log(len(p))
    ref=r.get("ref") or {}
    def pair(a,b): return cp.get(tuple(sorted((a,b),key=int)),0)/100
    f,s,t=ordre[0],ordre[1],ordre[2]
    rows.append(dict(date=datetime.strptime(r["d"],"%d%m%Y"),R=r["R"],C=r["C"],hip=r["hip"],disc=r["disc"],n=len(c),cf=c[f],c2=c[s],c3=c[t],pf=p[0],p2=p[1],ent=ent,dq=r.get("dq") or 0,
        fav_top=int(f in sp), sp_f=sp.get(f,0)/100, cp_fs=pair(f,s), cp_ft=pair(f,t), nplaces=len(sp),
        mv_f=(c[f]/ref[f]-1) if ref.get(f) else np.nan, terrain=r.get("terrain"), alloc=r.get("alloc")))
df=pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
df["gap"]=df.c2/df.cf
df["hit_fs"]=(df.cp_fs>0).astype(int); df["hit_ft"]=(df.cp_ft>0).astype(int)
mid=df.date.quantile(.5); df["per"]=np.where(df.date<=mid,"A (anc.)","B (recent)")
df.to_pickle(f"{D}/data/df_profils.pkl")
print(len(df),"courses",df.date.min().date(),df.date.max().date(),"coupure",mid.date())
print(df.groupby("disc").size().to_string())
print("terrain non nul:",df.terrain.notna().sum())
def roi(sub,col): 
    if len(sub)==0: return (0,np.nan,np.nan,np.nan,np.nan)
    g=sub[col]-1; m=g.mean(); se=g.std()/np.sqrt(len(g)); return len(sub),(sub[col]>0).mean(),m,m-1.96*se,m+1.96*se
def rep(titre,mask,cols=("sp_f","cp_fs","cp_ft")):
    print(f"\n== {titre}")
    for per in ("Tout","A (anc.)","B (recent)"):
        s=df[mask & ((df.per==per) | (per=="Tout"))]
        out=[]
        for c in cols:
            n,h,m,lo,hi=roi(s,c); out.append(f"{c}: hit {h:.0%} ROI {m:+.0%} [{lo:+.0%};{hi:+.0%}]" if n else "-")
        print(f"  {per:11s} n={len(s):4d} | "+" | ".join(out))
# base
rep("TOUS",df.n>0)
for d in df.disc.unique(): rep(d,df.disc==d)
