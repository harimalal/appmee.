import sys, json, numpy as np, pandas as pd, statsmodels.api as sm
N=sys.argv[1]
exec(open(f"{N}/methode_3temps.py").read().split("df=pd.DataFrame(rows)")[0].replace("N=sys.argv[1]",f"N='{N}'"))
Hd=pd.DataFrame(HOR).fillna({"forme":False,"progression":False,"corresp":False,"sans_dq":False,"classe":False,"face_a_face":False}); Hd["lp"]=np.log(Hd.att/(1-Hd.att))
Hd["race"]=Hd.d
X=sm.add_constant(Hd[["lp","sig"]]); m=sm.GLM(Hd.top3,X,family=sm.families.Binomial()).fit(cov_type="cluster",cov_kwds={"groups":Hd.race})
print("ENSEMBLE : effet de chaque signal coche en plus, au-dela de la cote (logit, IC95 par course)"); print(m.summary().tables[1])
sigs=["forme","progression","corresp","sans_dq","classe","face_a_face"]
X=sm.add_constant(pd.concat([Hd[["lp"]],Hd[sigs].fillna(False).astype(int)],axis=1)); m2=sm.GLM(Hd.top3,X,family=sm.families.Binomial()).fit(cov_type="cluster",cov_kwds={"groups":Hd.race})
print("\nSIGNAL PAR SIGNAL (tous ensemble) :"); print(m2.summary().tables[1])
# cotes moyennes/hautes seulement (les chevaux 'evidents' ecartes)
for nom,msk in (("cote < 6",Hd.cote<6),("cote 6-15",(Hd.cote>=6)&(Hd.cote<15)),("cote >= 15",Hd.cote>=15)):
    s=Hd[msk]; X=sm.add_constant(s[["lp","sig"]]); mm=sm.GLM(s.top3,X,family=sm.families.Binomial()).fit(cov_type="cluster",cov_kwds={"groups":s.race})
    b=mm.params["sig"]; ci=mm.conf_int().loc["sig"]; print(f"{nom:10s} {len(s):5d} chevaux | par signal en plus : odds ratio {np.exp(b):.3f} [{np.exp(ci[0]):.3f} ; {np.exp(ci[1]):.3f}] p={mm.pvalues['sig']:.3f}")
