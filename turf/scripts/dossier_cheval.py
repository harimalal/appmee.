"""Affiche le dossier de chaque partant : carriere complete AVANT la date, une ligne par course (rang, cote, RK, driver, ferrure, commentaire de fin de course)."""
import sys, json, os
N=sys.argv[1]; DATE=sys.argv[2]; C=sys.argv[3]; NB=int(sys.argv[4]) if len(sys.argv)>4 else 8; D=f"{N}/data"
COM={}
for l in open(f"{D}/comments_prev.jsonl"):
    try: x=json.loads(l)
    except Exception: continue
    for hid,v in (x.get("runners") or {}).items(): COM[(x["link"],hid)]=v.get("c")
def red(v):
    try: x=int(v); return f"{x//1000}'{(x%1000)//10:02d}\"{x%10}" if x>0 else "-"
    except Exception: return "-"
HIPC=sys.argv[5] if len(sys.argv)>5 else "7500"; race=json.load(open(f"{D}/deep/{DATE}_{HIPC}_C{C}.json"))
for p in race["partants"]:
    hid=p["id"]; P=sorted([x for x in json.load(open(f"{D}/perfs/{hid}.json")) if x["datePerf"][:10]<DATE],key=lambda x:x["datePerf"],reverse=True)
    print(f"\n#### n{p['leavingNumber']} {p['name']} ({p['age']}{p['sexe']}) | driver {p['driver']} | ent {p['coach']} | ferrure {p['ferrure']} | crack {p['crackSeries']} | record {p.get('record')} | {len(P)} courses | gains/moy {p.get('earningsAverage')}")
    for x in P[:NB]:
        ip=x.get("idPerf","").split("-"); lk=f"/courses/{'-'.join(ip[:3])}/{ip[3]}/{ip[4]}" if len(ip)>=5 else None
        c=COM.get((lk,hid)); 
        print(f"  {x['datePerf'][:10]} {(x.get('nomHippodrome') or '')[:14]:14s} {x.get('speciality')} {x.get('distance')}m {x.get('allocation')}EUR cat{x.get('category')} | rang {x.get('rang')}/{x.get('nbPartant')} cote {x.get('rapportProbable')} RK {red(x.get('reduction'))} | {(x.get('driver') or '')[:16]} | {x.get('ferrure')} | {(c or '(commentaire non lu)')[:260]}")
