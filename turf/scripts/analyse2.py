import pandas as pd, numpy as np, itertools
D="/tmp/claude-0/-home-user-appmee-/be1f39c7-7663-5c9c-93f0-01020c239924/scratchpad/courses"
df=pd.read_pickle(f"{D}/data/df_profils.pkl")
df["cat"]=df.disc.map(lambda x:"trot" if x in("ATTELE","MONTE") else ("galop" if x=="PLAT" else "obstacle"))
df["cfb"]=pd.cut(df.cf,[0,1.8,2.5,3.5,5,100],labels=["<1.8","1.8-2.5","2.5-3.5","3.5-5",">5"])
df["nb"]=pd.cut(df.n,[0,8,11,14,30],labels=["<=8","9-11","12-14","15+"])
df["gapb"]=pd.cut(df.gap,[0,1.3,1.8,2.5,100],labels=["<1.3","1.3-1.8","1.8-2.5",">2.5"])
print("terrain ex:",df.terrain.dropna().iloc[:3].tolist())
def line(s,cols=("sp_f","cp_fs","cp_ft")):
    o=[]
    for c in cols:
        g=s[c]-1; m=g.mean(); se=g.std()/np.sqrt(max(len(g),1)); o.append(f"{c} hit {(s[c]>0).mean():.0%} ROI {m:+.0%}±{1.96*se:.0%}")
    return " | ".join(o)
print("\n--- cote favori x categorie (hit top3 favori, rapport moyen couple fav+2e quand gagné)")
for (cat,cfb),s in df.groupby(["cat","cfb"],observed=True):
    if len(s)<40: continue
    w=s[s.cp_fs>0].cp_fs
    print(f"{cat:8s} fav {cfb:8s} n={len(s):4d} fav top3 {s.fav_top.mean():.0%} | couple fav+2e gagne {len(w)/len(s):.0%} rapport median {w.median():.1f} | {line(s)}")
print("\n--- TROT seul, favori <2.5: nb partants x ecart fav/2e")
t=df[(df.cat=="trot")&(df.cf<2.5)]
for (nb,gb),s in t.groupby(["nb","gapb"],observed=True):
    if len(s)<30: continue
    print(f"n {nb:6s} ecart {gb:8s} n={len(s):3d} fav top3 {s.fav_top.mean():.0%} | {line(s)}")
print("\n--- Dq par course trot selon nb partants")
print(df[df.cat=="trot"].groupby("nb",observed=True).dq.mean().round(2).to_dict())
