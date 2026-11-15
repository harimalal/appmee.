"""Lecture cheval par cheval, protocole strict : carriere complete (letrot), commentaires de fin de course, driver/entraineur filtres, correspondance, face-a-face.
Toutes les donnees sont ANTERIEURES a la date de la course. Usage : python3 -I deep_analyse.py <dossier> <AAAA-MM-JJ> <hip> <courses> """
import sys, os, json, re, glob, unicodedata, itertools, subprocess, time
import numpy as np, pandas as pd
N=sys.argv[1]; DATE=sys.argv[2]; HIP=sys.argv[3]; COURSES=[int(x) for x in sys.argv[4].split(",")]; D=f"{N}/data"
def rk(v):
    v=str(v or "").strip()
    if v.isdigit(): return int(v) if int(v)>0 else 99
    return -1 if v[:1] in "DTAR" else 99
def red(v):
    try: x=int(v); return (x//1000*60+(x%1000)//10+(x%10)/10) if x>0 else np.nan
    except Exception: return np.nan
# pool de carrieres en cache (pour driver / entraineur filtres)
POOL=[]
for f in glob.glob(f"{D}/perfs/*.json"):
    for x in json.load(open(f)):
        if x.get("speciality")!="A": continue
        POOL.append(dict(date=x["datePerf"][:10],hip=str(x.get("numHippodrome")),driver=x.get("driverId"),coach=x.get("coachId"),rang=rk(x.get("rang")),dist=x.get("distance") or 0))
POOL=pd.DataFrame(POOL); POOL["top3"]=((POOL.rang>=1)&(POOL.rang<=3)).astype(int); POOL=POOL[POOL.date<DATE]
# commentaires de fin de course
COM={}
for l in open(f"{D}/comments_prev.jsonl"):
    try: x=json.loads(l)
    except Exception: continue
    for hid,v in (x.get("runners") or {}).items(): COM[(x["link"],hid)]=v.get("c")
POS=["a bien fini","bien fini","fini fort","finissant fort","s'imposant","s'est impos","a dominé","sans être inquiété","a belle allure","a pris la mesure","en progression","a bien terminé","remontant","a bien résisté","a bien répondu","avec brio","facilement","largement","bien lancé","très bien","a fait bonne figure","de bon augure"]
NEG=["a faibli","a craqué","en perdition","n'a pas pu","sans réaction","sans rien pouvoir","a manqué de pointe","a lâché","distancé","très lointain","a déçu","a dû céder","s'est éteint","a perdu pied","a baissé pavillon","a terminé en roue libre","décevant"]
EXC=["gêné","gené","enfermé","bouché","s'est vu fermer","barré","contraint de","a été bousculé","privé de","handicapé","pris dans","a dû se rabattre","dans le dos"]
ALR=["disqualifié","irrégulier","a rompu","faute","a galopé","s'est mis à la faute","a commis"]
def tag(c):
    if not c: return ""
    t=c.lower(); r=[]
    if any(k in t for k in ALR): r.append("FAUTE")
    if any(k in t for k in EXC): r.append("EXCUSE")
    if any(k in t for k in POS): r.append("+")
    if any(k in t for k in NEG): r.append("-")
    return "/".join(r)
H2H={}
def get(u):
    t=subprocess.run(["curl","-sS","-m","40","-A","Mozilla/5.0 (analyse privee)",u],capture_output=True,text=True).stdout
    try: return json.loads(t)
    except Exception: return {}
out=[]; summ=[]
for c in COURSES:
    race=json.load(open(f"{D}/deep/{DATE}_{HIP}_C{c}.json")); dist=race["distance"]; alloc=race["allocation"]; ps=[p for p in race["partants"] if not p.get("nonPartant")]
    dstr=DATE.replace("-","")[6:8]+DATE.replace("-","")[4:6]+DATE.replace("-","")[:4]
    pmu=get(f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{dstr}/R1/C{c}/participants").get("participants",[])
    cote={p["numPmu"]:(p.get("dernierRapportDirect") or {}).get("rapport") for p in pmu}
    names={p["leavingNumber"]:p["name"] for p in ps}
    # face-a-face (5 dernieres perfs PMU)
    pd_=get(f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{dstr}/R1/C{c}/performances-detaillees/pretty").get("participants",[]); ff={p["leavingNumber"]:0 for p in ps}
    nm2n={v:k for k,v in names.items()}
    for pp in pd_:
        n=pp["numPmu"]
        for cc in pp["coursesCourues"]:
            pres={q["nomCheval"]:q["place"] for q in cc["participants"]}; me=pres.get(pp["nomCheval"])
            if not me or me["statusArrivee"]!="PLACE": continue
            for nm,pl in pres.items():
                if nm in nm2n and nm2n[nm]!=n and pl["statusArrivee"]=="PLACE" and me["place"]<pl["place"]: ff[n]=ff.get(n,0)+1
    rows=[]
    for p in ps:
        hid=p["id"]; n=p["leavingNumber"]; f=f"{D}/perfs/{hid}.json"
        P=[x for x in json.load(open(f)) if x["datePerf"][:10]<DATE and x.get("speciality")=="A"] if os.path.exists(f) else []
        P=sorted(P,key=lambda x:x["datePerf"],reverse=True)
        R=[rk(x.get("rang")) for x in P]; top=[1 if 1<=r<=3 else 0 for r in R]; win=[1 if r==1 else 0 for r in R]
        l5=P[:5]; l10=P[:10]
        def rate(a,k): return (sum(a[:k])/len(a[:k])) if len(a[:k]) else np.nan
        dm=lambda x:abs((x.get("distance") or 0)-dist)<=150; vm=lambda x:str(x.get("numHippodrome"))==HIP
        am=lambda x:bool(x.get("allocation")) and 0.6*alloc<=x["allocation"]<=1.6*alloc
        m3=sum(1 for x,r in zip(P,R) if 1<=r<=3 and dm(x) and vm(x) and am(x)); m2=sum(1 for x,r in zip(P,R) if 1<=r<=3 and (dm(x)+vm(x)+am(x))==2)
        dd=[(1 if 1<=r<=3 else 0) for x,r in zip(P,R) if dm(x)]; vv=[(1 if 1<=r<=3 else 0) for x,r in zip(P,R) if vm(x)]
        rks=[red(x.get("reduction")) for x in P if dm(x) and not np.isnan(red(x.get("reduction")))]
        rks=[r for r in rks if 60<r<100][:10]
        dq_last=bool(R) and R[0]==-1; dq10=sum(1 for r in R[:10] if r==-1)
        jours=(pd.Timestamp(DATE)-pd.Timestamp(P[0]["datePerf"][:10])).days if P else 999
        # driver / entraineur / tandem (pool cache, Vincennes)
        did=p.get("driverId"); cid=p.get("coachId")
        pv=POOL[POOL.hip==HIP]; pdv=pv[pv.driver==did]; pcv=pv[pv.coach==cid]; ptd=pv[(pv.driver==did)&(pv.coach==cid)]
        aff=[(1 if 1<=r<=3 else 0) for x,r in zip(P,R) if x.get("driverId")==did]
        coms=[]
        for x in l5:
            ip=x.get("idPerf","").split("-"); lk=f"/courses/{'-'.join(ip[:3])}/{ip[3]}/{ip[4]}" if len(ip)>=5 else None
            coms.append(dict(date=x["datePerf"][:10],hip=x.get("nomHippodrome"),dist=x.get("distance"),rang=x.get("rang"),n=x.get("nbPartant"),cote=x.get("rapportProbable"),c=COM.get((lk,hid)) if lk else None))
        tg=[tag(k["c"]) for k in coms]
        rows.append(dict(n=n,nom=p["name"],age=p["age"],sexe=p["sexe"],driver=p["driver"],avis=p.get("avisEntraineur"),cote=cote.get(n),nrun=len(P),
            r5=rate(top,5),r10=rate(top,10),w10=rate(win,10),m3=m3,m2=m2,d_n=len(dd),d_r=np.mean(dd) if dd else np.nan,v_n=len(vv),v_r=np.mean(vv) if vv else np.nan,
            rk_best=min(rks) if rks else np.nan,rk_mean=np.mean(rks[:5]) if rks else np.nan,dq_last=dq_last,dq10=dq10,jours=jours,
            drv_n=len(pdv),drv_r=pdv.top3.mean() if len(pdv) else np.nan,coach_n=len(pcv),coach_r=pcv.top3.mean() if len(pcv) else np.nan,tand_n=len(ptd),tand_r=ptd.top3.mean() if len(ptd) else np.nan,
            aff_n=len(aff),aff_r=np.mean(aff) if aff else np.nan,ff=ff.get(n,0),ferr1=bool(p.get("firstFerrure")),chg_ent=bool(p.get("changementEntraineur")),first_drv=bool(p.get("firstJockey")),
            crack=p.get("crackSeries"),musique=[r if r>0 else ("D" if r==-1 else "0") for r in R[:6]],coms=coms,tags=tg,
            cplus=sum("+" in t for t in tg),cmoins=sum("-" in t for t in tg),cexc=sum("EXCUSE" in t for t in tg),cfaute=sum("FAUTE" in t for t in tg)))
    df=pd.DataFrame(rows)
    # ---- criteres : "ressort du lot" = dans les 3 meilleurs du lot sur le critere, avec volume suffisant
    def top(col,asc=False,k=3,minn=None,ncol=None):
        s=df[col].copy()
        if ncol: s=s.where(df[ncol]>=minn)
        r=s.rank(ascending=asc,method="min"); return (r<=k)&s.notna()
    C={}
    C["strike 10 dernieres"]=top("r10",ncol="nrun",minn=5)
    C["strike 5 dernieres"]=top("r5",ncol="nrun",minn=3)
    C["correspondance exacte"]=(df.m3>=1)|(df.m2>=2)
    C["distance"]=top("d_r",ncol="d_n",minn=3)
    C["hippodrome"]=top("v_r",ncol="v_n",minn=3)
    C["chrono (RK a distance)"]=top("rk_mean",asc=True)
    C["driver (Vincennes, n>=30)"]=top("drv_r",ncol="drv_n",minn=30)
    C["entraineur (n>=30)"]=top("coach_r",ncol="coach_n",minn=30)
    C["tandem driver-entraineur (n>=15)"]=top("tand_r",ncol="tand_n",minn=15)
    C["affinite cheval-driver"]=(df.aff_n>=2)&(df.aff_r>=0.5)
    C["face-a-face"]=df.ff>=df.ff.nlargest(3).min()
    C["commentaires positifs"]=(df.cplus>=2)&(df.cmoins==0)
    C["excuses a revoir"]=(df.cexc>=1)&(df.r5<0.4)
    C["sans faute"]=(df.dq10==0)&(df.nrun>=5)&(~df.dq_last)
    C["flag pre-course"]=df.ferr1|df.chg_ent|df.first_drv
    C["avis entraineur +"]=df.avis.astype(str).str.upper().str.startswith(("POSIT","1"))
    K=pd.DataFrame(C); df["nb"]=K.sum(axis=1); df["crit"]=K.apply(lambda r:", ".join(k for k,v in r.items() if v),axis=1)
    neg=[]
    for i,r in df.iterrows():
        m=[]
        if r.dq_last: m.append("DQ derniere sortie")
        if r.dq10>=3: m.append(f"{r.dq10} fautes/10")
        if r.cfaute>=2: m.append("fautes citees dans les commentaires")
        if r.cmoins>=2: m.append("commentaires negatifs")
        if r.jours>60: m.append(f"rentree ({r.jours} j)")
        if r.nrun<5: m.append("peu d'historique")
        neg.append(", ".join(m))
    df["alertes"]=neg
    df=df.sort_values(["nb","cote"],ascending=[False,True])
    df.to_pickle(f"{D}/deep_{DATE}_C{c}.pkl")
    out.append(f"\n## Vincennes R1C{c} - {race.get('nomCourse')} - {dist} m - {alloc} EUR - {len(ps)} partants")
    for r in df.itertuples():
        out.append(f"\n**n{r.n} {r.nom}** ({r.age}{r.sexe}) cote {r.cote} | driver {r.driver} | {r.nrun} courses | musique {' '.join(map(str,r.musique))} | **{r.nb} criteres** : {r.crit or '-'} | alertes : {r.alertes or '-'}")
        out.append(f"  strike 5/10 : {r.r5:.0%}/{r.r10:.0%} ; distance : {r.d_r:.0%} (n={r.d_n}) ; Vincennes : {r.v_r:.0%} (n={r.v_n}) ; RK moyen : {r.rk_mean:.1f} ; driver Vincennes : {r.drv_r:.0%} (n={r.drv_n}) ; entraineur : {r.coach_r:.0%} (n={r.coach_n}) ; tandem : {r.tand_r:.0%} (n={r.tand_n})")
        for k in r.coms[:3]:
            if k["c"]: out.append(f"  - {k['date']} {k['hip']} {k['dist']} m, {k['rang']} sur {k['n']} (cote {k['cote']}) : {k['c'][:210]}")
open(f"{D}/deep_{DATE}.md","w").write("\n".join(out)); print("ok",len(out),"lignes")
