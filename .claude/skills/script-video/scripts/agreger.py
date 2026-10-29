"""Agrège les spectateurs simulés : rétention, durée moyenne, engagement, profils, départs.

  python3 -I agreger.py simu/ 367      (dossier des segment-*.json, durée de la vidéo en s)
"""
import os, sys
DOSSIER=sys.argv[1]; DUREE=int(sys.argv[2])
import json, glob, statistics as st, collections
V=[]; 
for f in sorted(glob.glob(os.path.join(DOSSIER,'segment-*.json'))): V+= [dict(v, seg=os.path.basename(f)[8]) for v in json.load(open(f))]
D=DUREE; out={'n':len(V)}
marks=[m for m in [5,15,30,60,90,120,180,240,300,420,600] if m<DUREE]+[DUREE]
out['retention']={m: round(100*sum(v['watch_s']>=m for v in V)/len(V)) for m in marks}
out['avd_s']=round(st.mean(min(v['watch_s'],D) for v in V)); out['avd_pct']=round(100*out['avd_s']/D)
for k in ['like','subscribe','share','clic_description']: out[k]=sum(bool(v.get(k)) for v in V)
out['comments']=sum(bool(v.get('comment')) for v in V)
for k in ['valeur_percue','originalite','voix']: out[k]=round(st.mean(v[k] for v in V),2)
seg={}
for s in sorted({v['seg'] for v in V}):
    g=[v for v in V if v['seg']==s]
    seg[s]={'avd_s':round(st.mean(min(v['watch_s'],D) for v in g)),'fin':sum(v['watch_s']>=D-5 for v in g),'r30':sum(v['watch_s']>=30 for v in g),
            'like':sum(bool(v['like']) for v in g),'abo':sum(bool(v['subscribe']) for v in g),'valeur':round(st.mean(v['valeur_percue'] for v in g),1),'voix':round(st.mean(v['voix'] for v in g),1)}
out['segments']=seg
b=collections.Counter((min(v['watch_s'],D)//30)*30 for v in V if v['watch_s']<D-5); out['departs_par_30s']=dict(sorted(b.items()))
json.dump(out,open(os.path.join(DOSSIER,'agregat.json'),'w'),indent=1,ensure_ascii=False); print(json.dumps(out,indent=1,ensure_ascii=False))
