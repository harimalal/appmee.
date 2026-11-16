import pandas as pd, numpy as np
D="/tmp/claude-0/-home-user-appmee-/be1f39c7-7663-5c9c-93f0-01020c239924/scratchpad/courses"
df=pd.read_pickle(f"{D}/data/df_profils.pkl")
t=df[(df.disc=="ATTELE")&(df.cf<3.5)].copy(); t["sem"]=t.date.dt.to_period("W")
print("ATTELE fav<3.5 simple place : n",len(t),"ROI",f"{(t.sp_f-1).mean():+.1%}")
for per,s in t.groupby(pd.cut(t.date,3)): print(" tiers",str(per)[:30],len(s),f"hit {s.fav_top.mean():.0%} ROI {(s.sp_f-1).mean():+.1%}")
rng=np.random.default_rng(1); wk=t.groupby("sem").apply(lambda s:(s.sp_f-1).sum()); nn=t.groupby("sem").size()
b=[]
for _ in range(3000):
    i=rng.integers(0,len(wk),len(wk)); b.append(wk.values[i].sum()/nn.values[i].sum())
print("bootstrap par semaine ROI 95%:",np.percentile(b,[2.5,50,97.5]).round(3),"semaines",len(wk))
# meme chose, rapport moyen du place favori quand gagne
w=t[t.sp_f>0].sp_f; print("rapport place favori quand gagne: moyen",round(w.mean(),2),"median",w.median())
# terrain galop
g=df[df.disc=="PLAT"]; 
print("galop ROI fav place par terrain:",g.groupby("terrain",dropna=False).apply(lambda s:f"n{len(s)} {(s.sp_f-1).mean():+.0%}").to_dict() if g.terrain.map(type).eq(str).any() else "terrain=dict ou nul")
# pari 'sans risque': favori <1.8 top3 : combien de pertes sur 100
for cat,m in [("trot fav<2.5",(df.disc=="ATTELE")&(df.cf<2.5)),("galop fav<2.5",(df.disc=="PLAT")&(df.cf<2.5))]:
    s=df[m]; print(cat,"n",len(s),"favori hors des places :",f"{1-s.fav_top.mean():.0%}")
