import json, subprocess, sys, time, os
from concurrent.futures import ThreadPoolExecutor
N=sys.argv[1]; out=f"{N}/data/perfs_hist.jsonl"
rows=[json.loads(l) for l in open(f"{N}/data/historique_courses.jsonl")]
att=[r for r in rows if r["disc"]=="ATTELE" and r.get("cotes") and r.get("arr") and r.get("rap")]
done=set()
if os.path.exists(out):
    for l in open(out):
        try: x=json.loads(l); done.add((x["d"],x["R"],x["C"]))
        except Exception: pass
todo=[r for r in att if (r["d"],r["R"],r["C"]) not in done]; print(len(att),"courses attele,",len(todo),"a collecter",flush=True)
def f(r):
    u=f"https://online.turfinfo.api.pmu.fr/rest/client/7/programme/{r['d']}/R{r['R']}/C{r['C']}/performances-detaillees/pretty"
    for _ in range(3):
        try:
            t=subprocess.run(["curl","-sS","-m","40","-A","Mozilla/5.0 (analyse privee)",u],capture_output=True,text=True).stdout; j=json.loads(t); return dict(d=r["d"],R=r["R"],C=r["C"],p=j.get("participants",[]))
        except Exception: time.sleep(2)
    return None
n=0
with ThreadPoolExecutor(5) as ex, open(out,"a") as fo:
    for x in ex.map(f,todo):
        if x: fo.write(json.dumps(x)+"\n"); fo.flush(); n+=1
        if n%100==0: print(n,flush=True)
print("FINI",n,flush=True)
