# Enrichit chaque cheval d une course analysee : classe (surclassement), vitesse relative (RK), finitions, hippodrome, alertes.
# Entrees (dossier de travail local, non versionne) : deep/, perfs/, dossier_*.txt, part/ (participants PMU), courses.json, chevaux3.json.
import json,re,glob,os,statistics as st,datetime,unicodedata,collections
D='../courses/data/'
RACES=[('2026-11-14',f'R1C{c}','7500',f'deep/2026-11-14_7500_C{c}.json',f'dossier_14112026_R1C{c}.txt',f'part/14112026_R1C{c}.json') for c in (2,3,4,5,6,7,9)]
RACES+=[('2026-11-14',f'R8C{c}','1400',f'deep/2026-11-14_1400_C{c}.json',f'dossier_caen_C{c}.txt',f'part/14112026_R8C{c}.json') for c in (1,2,3)]
RACES+=[('2026-11-16','R1C1','7500','deep/2026-11-16_7500_C1.json','dossier_R1C1.txt','part/16112026_R1C1.json')]
courses={c['id']:c for c in json.load(open('courses.json'))}
chev=json.load(open('chevaux3.json'))
def norm(s): return unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()
LAD=[0,12000,20000,30000,45000,65000,100000]
def lvl(a):
    n=0
    for i,t in enumerate(LAD):
        if a>=t: n=i
    return n
LVLNAME=['< 12 k€','12–20 k€','20–30 k€','30–45 k€','45–65 k€','65–100 k€','≥ 100 k€']
def rk_s(v):
    try:
        v=str(v).strip()
        if not v or v in('0',): return None
        n=int(v)
        m,rest=divmod(n,1000) if n>=1000 else (0,n)
        # formats like 1135 -> 1'13"5 ; 1075 -> 1'07"5
        s=str(n).zfill(4); mi=int(s[0]); ss=int(s[1:3]); t=int(s[3])
        return mi*60+ss+t/10
    except: return None
def fm(n): return f'{int(n):,}'.replace(',',' ')
def fc(x,d=1): return f'{x:.{d}f}'.replace('.',',')
def rk_txt(x): return f"{int(x//60)}'{x%60:04.1f}\"".replace('.','"',1)[:-0] if False else f"{int(x//60)}'{int(x%60):02d}\"{int(round((x%1)*10))%10}"
FIN_POS=['bien termine','a bien fini','bien fini','bien sprinte','a sprinte','termine fort','termine le plus vite','termine vite','belle fin','bonne fin','fini fort','finissant tres fort','a fini tres vite','a bien progresse','domine surement','dominant surement','a domine','avec autorite','a rattrape','bien repondu','tres correctement soutenu','courageusement','bien soutenu','en pleine finale','vif sprint','a bien sprinte','sprint','remonte','a bien termine','dominant']
FIN_NEG=['a faibli','a cede','essouffle','en perdition','sans pouvoir','n\'a pas pu','sans reaction','sans inquieter','a plafonne','en retrait','a manque d\'allant','a manque de pointe','manque de reaction','a concede','a fini honorablement','sans pouvoir endiguer','n\'a pas insiste','sans insister','a fini sans','sans appui']
CLS_NEG=['depasse','manque de classe','pas a la hauteur','manque de vitesse','manque de pointe','a plafonne','loin des premiers','sans inquieter','en retrait des premieres','n\'a pas ete a la hauteur']
CLS_POS=['domine','avec autorite','facilement','surement','largement','nettement','survole','en patron']
EXCUSE=['gene','barre','enferme','a perdu du temps','contraint','coince','manque de place','perdu sa place','mal place','handicape','incident','a galope','faute']
def kw(txt,L): return [k for k in L if k in txt]
def parse_dossier(path):
    out={}
    cur=None
    for line in open(path):
        m=re.match(r'#### n(\d+) (.+?) \((\d+)([HFM])\) \| driver (.*?) \| ent (.*?) \| ferrure (\S+) \| crack (\S+) \| record (.*?) \| (\d+) courses \| gains/moy (\S+)',line)
        if m:
            cur=dict(num=int(m[1]),nom=m[2],age=int(m[3]),sexe=m[4],driver=m[5],ent=m[6],ferrure=m[7],crack=m[8],record=m[9],nb=int(m[10]),runs=[]); out[cur['num']]=cur; continue
        m=re.match(r'\s+(\d{4}-\d\d-\d\d) (.{14}) ([AM]) (\d+)m (\d+)EUR cat(\S*) \| rang (\S+)/(\d+) cote (\S+) RK (.*?) \| (.*?) \| (\S*) \| (.*)',line)
        if m and cur:
            cur['runs'].append(dict(date=m[1],hip=m[2].strip(),sp=m[3],dist=int(m[4]),alloc=int(m[5]),cat=m[6],rang=m[7],n=int(m[8]),cote=m[9],rk=m[10],driver=m[11],ferr=m[12],com=m[13]))
    return out
def isda(r): return r=='DA' or (r.startswith('D') and r!='D0') or r in('A','T')
def num(r):
    return int(r) if r.isdigit() else None
res={}
for jour,key,code,deepf,dosf,partf in RACES:
    cid=f'{jour}-{key}'; c=courses[cid]
    deep=json.load(open(D+deepf)); dos=parse_dossier(D+dosf); pm={x['numPmu']:x for x in json.load(open(partf))['participants']}
    dist=deep.get('distance') or c['distance']; alloc=deep.get('allocation') or c['alloc']
    cond=' '.join(deep.get('conditions') or []) if isinstance(deep.get('conditions'),list) else str(deep.get('conditions'))
    cond=cond or c.get('conditions','')
    rc=json.load(open(D+deepf)).get('race_conditions') if False else None
    sp='M' if c['disc']=='Monté' else 'A'
    d0=datetime.date.fromisoformat(jour)
    field={}
    for p in deep['partants']:
        n=p['leavingNumber']
        if p.get('nonPartant'): continue
        pf=D+f"perfs/{p['id']}.json"
        perfs=json.load(open(pf)) if os.path.exists(pf) else []
        perfs=[x for x in perfs if x['datePerf'][:10]<jour]
        perfs.sort(key=lambda x:x['datePerf'],reverse=True)
        field[n]=dict(p=p,perfs=perfs)
    # speed per horse
    for n,f in field.items():
        rks=[]
        for x in f['perfs'][:10]:
            r=str(x.get('rang') or '')
            if x.get('speciality')!=sp or isda(r): continue
            v=rk_s(x.get('reduction'))
            if v and 66<v<95 and (x.get('distanceCourse') or 0)>=2000: rks.append(v)
        rks=rks[:8]
        f['rk']=None
        if len(rks)>=2:
            top=sorted(rks)[:min(4,len(rks))]
            f['rk']=st.median(top); f['rk_best']=min(rks); f['rk_n']=len(rks)
    rkv=sorted(f['rk'] for f in field.values() if f['rk'])
    rkmed=st.median(rkv) if rkv else None
    crk=sorted(int(f['p']['crackSeries']) for f in field.values() if f['p'].get('crackSeries'))
    for n,f in field.items():
        p=f['p']; pr=pm.get(n,{}); L=f['perfs']; dd=dos.get(n,{'runs':[]})
        al=[]
        # ---- classe
        last6=[x for x in L[:6] if x.get('allocation')]
        a_med=st.median([x['allocation'] for x in last6]) if last6 else None
        a_last=last6[0]['allocation'] if last6 else None
        cats=collections.Counter(x.get('category') for x in L[:6] if x.get('category'))
        cat_hab=','.join(k for k,_ in cats.most_common(2))
        diff=None; verdict='inconnu'
        if a_med:
            diff=lvl(alloc)-lvl(a_med)
            verdict='dedans' if diff<=0 and diff>=0 else (f'sur{diff}' if diff>0 else f'sous{-diff}')
            if diff==0 and alloc>=1.35*a_med: verdict='sur0plus'
        # a déjà couru à ce niveau
        hi=[x for x in L[:20] if x.get('allocation',0)>=0.85*alloc and x.get('speciality')==sp]
        hi_pl=sum(1 for x in hi if num(str(x.get('rang') or '')) in (1,2,3)); hi_w=sum(1 for x in hi if str(x.get('rang'))=='1')
        # plafond
        plaf=None
        m=re.search(r"pas gagn[ée]+ ([\d.]+)",cond)
        if m: plaf=int(m[1].replace('.',''))
        gains=int(str(p.get('earnings') or 0).replace(' ','') or 0)
        cl=f"Course à {fm(alloc)} € ({'cat. '+c['categorie'] if c['categorie'] else 'cat. ?'}). "
        if a_med: cl+=f"Habituel : {fm(a_med)} € (médiane des {len(last6)} dernières, cat. {cat_hab or '?'}), dernière sortie {fm(a_last)} €. "
        if hi: cl+=f"A déjà couru à ce niveau (≥ 85 % de l'allocation) : {len(hi)} fois, {hi_pl} placé(s), {hi_w} victoire(s). "
        else: cl+="N'a pas couru à ce niveau sur ses 20 dernières sorties. "
        if plaf and gains: cl+=f"Gains {fm(gains)} € pour un plafond de {fm(plaf)} € ({round(100*gains/plaf)} %). "
        # ---- vitesse
        v_txt='—'; rk_rang=None; rk_ecart=None
        if f['rk']:
            rk_rang=1+sum(1 for x in rkv if x<f['rk']); rk_ecart=f['rk']-rkmed
            v_txt=f"RK {rk_txt(f['rk'])} (4 meilleures sur {f['rk_n']} courses propres), {rk_rang}e/{len(rkv)} du lot, {'−' if rk_ecart<0 else '+'}{fc(abs(rk_ecart))} s/km vs médiane du lot. Record {p.get('record') or '—'}."
        # ---- finition + commentaires
        pos=neg=exc=cpos=cneg=0; last_fin=None; last_cls=None
        coms=[r for r in dd['runs'] if r['com'] and 'non lu' not in r['com']][:5]
        for r in coms:
            t=norm(r['com']); kp=kw(t,FIN_POS); kn=kw(t,FIN_NEG)
            if kp and not kn: pos+=1; last_fin=last_fin or (r['date'],r['com'])
            elif kn and not kp: neg+=1; last_fin=last_fin or (r['date'],r['com'])
            elif kp and kn: last_fin=last_fin or (r['date'],r['com'])
            if kw(t,EXCUSE): exc+=1
            if kw(t,CLS_POS) and r['rang'] in('1','2'): cpos+=1; last_cls=last_cls or (r['date'],r['com'])
            if kw(t,CLS_NEG): cneg+=1; last_cls=last_cls or (r['date'],r['com'])
        fidx=pos-neg
        def cut(s,n=170): return s if len(s)<=n else s[:n-1]+'…'
        f_txt=(f"{pos} finition(s) positive(s), {neg} négative(s) sur {len(coms)} commentaires lus, {exc} excuse(s) (gêne, faute). " if coms else "Pas de commentaire de fin de course lu. ")
        if last_fin: f_txt+=f"Dernier indice ({last_fin[0]}) : « {cut(last_fin[1])} »"
        c_txt=''
        if last_cls: c_txt=f"Commentaire de classe ({last_cls[0]}) : « {cut(last_cls[1])} »"
        # ---- hippodrome
        H=[x for x in L if x.get('numHippodrome')==code]
        hs=len(H); hw=sum(1 for x in H if str(x.get('rang'))=='1'); hp=sum(1 for x in H if num(str(x.get('rang') or '')) in (1,2,3)); hd=sum(1 for x in H if isda(str(x.get('rang') or '')))
        if hs==0: h_txt='Jamais couru ici'
        else: h_txt=f"{hs} course(s) ici : {hw} victoire(s), {hp} placé(s), {hd} DA"
        # distance
        Dd=[x for x in L if abs((x.get('distanceCourse') or 0)-dist)<=150 and x.get('speciality')==sp]
        ds=len(Dd); dp=sum(1 for x in Dd if num(str(x.get('rang') or '')) in (1,2,3))
        # ---- fautes
        l8=L[:8]; da8=sum(1 for x in l8 if isda(str(x.get('rang') or '')))
        da_last=bool(L) and isda(str(L[0].get('rang') or ''))
        jours=(d0-datetime.date.fromisoformat(L[0]['datePerf'][:10])).days if L else None
        # ---- alertes
        A=[]
        def add(sev,t): A.append(f'{sev}|{t}')
        if da_last: add('bad','DA à la dernière sortie')
        if da8>=2: add('bad' if da8>=3 else 'warn',f'{da8} DA sur ses {len(l8)} dernières sorties')
        if verdict.startswith('sur'):
            k=int(verdict[3]) if verdict[3:4].isdigit() and verdict!='sur0plus' else 0
            if verdict=='sur0plus': add('warn',f'Allocation +35 % vs son habituel ({fm(a_med)} €)')
            elif k>=2: add('bad',f'Surclassé de {k} niveaux')
            elif k==1: add('warn','Surclassé d\'un niveau')
            if k>=1 and hi and hi_pl>=1: add('ok',f'Mais déjà placé à ce niveau ({hi_pl}/{len(hi)})')
        elif verdict.startswith('sous') : add('ok',f'Classe inférieure de {verdict[4]} niveau(x) vs son habituel')
        elif verdict=='dedans': add('info','Dans sa catégorie')
        if hs==0: add('info','Jamais couru ici')
        elif hp>=2 and hp/hs>=0.5: add('ok',f'Aime l\'hippodrome : {hp} placé(s) sur {hs}')
        elif hs>=3 and hp==0: add('warn',f'Ne réussit pas ici : 0 placé sur {hs}')
        if hd>=2: add('warn',f'{hd} DA déjà ici')
        if ds==0: add('info','Jamais couru à cette distance')
        elif ds>=3 and dp==0: add('warn',f'0 placé en {ds} courses à cette distance')
        elif dp>=2 and dp/ds>=0.5: add('ok',f'Aime la distance : {dp} placé(s) sur {ds}')
        if jours and jours>=60: add('warn',f'Rentrée après {jours} jours')
        if p.get('firstFerrure'): add('warn','Première fois avec cette ferrure')
        if p.get('changementEntraineur'): add('info','Nouvel entraîneur')
        if p.get('firstJockey'): add('info','Premier driver')
        elif pr.get('driverChange'): add('info','Changement de driver')
        if p.get('firstAutostart'): add('info','Premier autostart')
        if p.get('firstSpecialiteMonte'): add('warn','Première fois monté')
        hd_=pr.get('handicapDistance')
        if hd_ and dist and hd_!=dist and abs(hd_-dist)>=25: add('warn',f'Recul : court sur {hd_} m (course {dist} m)' if hd_>dist else f'Avance de {dist-hd_} m')
        if fidx>=2: add('ok','Finitions positives répétées')
        if fidx<=-2: add('warn','Finitions négatives répétées')
        if exc>=2: add('info',f'{exc} excuses dans les commentaires')
        avis=pr.get('avisEntraineur') or {1:'POSITIF',2:'NEUTRE',3:'NEGATIF'}.get(p.get('avisEntraineur'),'')
        if avis=='NEGATIF': add('bad','Avis entraîneur négatif')
        elif avis=='POSITIF': add('info','Avis entraîneur positif (n\'ajoute rien à la cote)')
        res[(cid,n)]=dict(classe_verdict=verdict,classe_txt=cl.strip(),cat_hab=cat_hab,alloc_hab=int(a_med) if a_med else None,
            crack=int(p['crackSeries']) if p.get('crackSeries') else None,crack_rang=(1+sum(1 for x in crk if x<int(p['crackSeries']))) if p.get('crackSeries') else None,crack_n=len(crk),
            rk=round(f['rk'],2) if f['rk'] else None,rk_rang=rk_rang,rk_n_lot=len(rkv),rk_ecart=round(rk_ecart,2) if rk_ecart is not None else None,vitesse_txt=v_txt,
            finition_idx=fidx,finition_txt=f_txt,classe_comm=c_txt,hippo_txt=h_txt,hippo_starts=hs,hippo_places=hp,dist_txt=f"{ds} course(s) à ±150 m, {dp} placé(s)" if ds else 'Jamais couru à cette distance',
            da8=da8,jours=jours,avis=avis,alertes=' ;; '.join(A),nb_bad=sum(1 for a in A if a.startswith('bad')),nb_warn=sum(1 for a in A if a.startswith('warn')))
for x in chev:
    r=res.get((x['course'],x['num']))
    if r:
        x.update(r)
        c0,c1=x.get('cote_matin'),x.get('cote')
        if c0 and c1 and c0>0:
            if c1<=0.8*c0: x['alertes']+=(' ;; ' if x['alertes'] else '')+f"info|Cote en baisse : {fc(c0)} le matin, {fc(c1)} au départ (piste, p = 0,07)"
            elif c1>=1.25*c0: x['alertes']+=(' ;; ' if x['alertes'] else '')+f"info|Cote en hausse : {fc(c0)} le matin, {fc(c1)} au départ"
        x['nb_alertes']=len([a for a in x['alertes'].split(' ;; ') if a])
json.dump(chev,open('chevaux4.json','w'),ensure_ascii=False)
print(len(res),sum(1 for x in chev if 'classe_verdict' in x),len(chev))
# print sample
for x in chev:
    if x['course']=='2026-11-14-R1C5' and x['num'] in (2,9,11):
        print(x['nom'],{k:x.get(k) for k in('classe_verdict','classe_txt','vitesse_txt','finition_txt','hippo_txt','alertes','avis')})
import collections
print(collections.Counter(x.get('classe_verdict') for x in chev if x['course'].startswith('2026-11-14')))
