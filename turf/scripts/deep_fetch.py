"""Collecte pour l'analyse approfondie : pages course letrot (partants, ids, driver, entraineur, flags) + carriere complete de chaque cheval (letrot, 1 req / 3 s)."""
import sys, os, json, re, html, time, subprocess
N=sys.argv[1]; DATE=sys.argv[2]; HIP=sys.argv[3]; COURSES=[int(x) for x in sys.argv[4].split(",")]
D=f"{N}/data"; os.makedirs(f"{D}/perfs",exist_ok=True); os.makedirs(f"{D}/deep",exist_ok=True)
def get(u,h=None):
    cmd=["curl","-sS","-m","60","-A","Mozilla/5.0 (analyse privee)"]+(["-H",h] if h else [])+[u]
    t=subprocess.run(cmd,capture_output=True,text=True).stdout; time.sleep(3); return t
ids={}
for c in COURSES:
    f=f"{D}/deep/{DATE}_{HIP}_C{c}.json"
    if os.path.exists(f): d=json.load(open(f))
    else:
        raw=get(f"https://www.letrot.com/courses/{DATE}/{HIP}/{c}"); i=raw.find("<race-detail"); j=raw.find(':payload="',i); k=raw.find('"',j+10)
        d=json.loads(html.unescape(raw[j+10:k])); json.dump(d["race"],open(f,"w"),ensure_ascii=False); d=d["race"]; 
    d=d if "partants" in d else d
    for p in d["partants"]: ids[p["id"]]=p["name"]
print(len(ids),"chevaux a historiser",flush=True)
n=0
for h,nm in ids.items():
    f=f"{D}/perfs/{h}.json"
    if os.path.exists(f) and os.path.getsize(f)>2: continue
    allp=[]
    for page in (1,2,3,4,5,6):
        try: d=json.loads(get(f"https://www.letrot.com/v1/api/horses/{h}/perfs?limit=50&page={page}&excludeNP=true","Accept: application/json"))
        except Exception: d=[]
        allp+=d if isinstance(d,list) else []
        if not isinstance(d,list) or len(d)<50: break
    json.dump(allp,open(f,"w")); n+=1
    if n%10==0: print(n,flush=True)
print("FINI",n,flush=True)
