"""Pages course letrot.com (usage prive, 1 page / 3 s) pour 1 course attele sur 3 de l'historique : signaux avant course (ferrure, changement entraineur/driver, commentaire, avis, rentree, crack series...).
Sortie : data/letrot_pages.jsonl (1 ligne par course). Reprise possible."""
import json, sys, os, re, html, time, subprocess, unicodedata
N=sys.argv[1]; out=f"{N}/data/letrot_pages.jsonl"
rows=[json.loads(l) for l in open(f"{N}/data/historique_courses.jsonl")]
att=[r for r in rows if r["disc"]=="ATTELE" and r.get("cotes") and r.get("arr") and r.get("rap")]
att=sorted(att,key=lambda r:(r["d"][4:]+r["d"][2:4]+r["d"][:2],r["R"],r["C"]))[::3]
norm=lambda s:re.sub(r"[^A-Z0-9]","",unicodedata.normalize("NFKD",s or "").encode("ascii","ignore").decode().upper())
def fetch(u):
    t=subprocess.run(["curl","-sS","-m","50","-A","Mozilla/5.0 (analyse privee)",u],capture_output=True,text=True).stdout; time.sleep(3); return t
done=set()
if os.path.exists(out):
    for l in open(out):
        try: x=json.loads(l); done.add((x["d"],x["R"],x["C"]))
        except Exception: pass
codes={}
def day_codes(d):
    if d in codes: return codes[d]
    iso=f"{d[4:]}-{d[2:4]}-{d[:2]}"; raw=html.unescape(fetch(f"https://www.letrot.com/courses/{iso}"))
    codes[d]={norm(a):b for a,b in re.findall(r'"nomHippodrome":"([^"]+)","numHippodrome":"(\d+)"',raw)}; return codes[d]
print(len(att),"courses a traiter,",len(done),"deja faites",flush=True); n=0
with open(out,"a") as fo:
    for r in att:
        k=(r["d"],r["R"],r["C"])
        if k in done: continue
        try:
            cm=day_codes(r["d"]); hn=norm(r["hip"]); code=cm.get(hn) or next((v for a,v in cm.items() if hn in a or a in hn),None)
            if not code: continue
            iso=f"{r['d'][4:]}-{r['d'][2:4]}-{r['d'][:2]}"
            raw=fetch(f"https://www.letrot.com/courses/{iso}/{code}/{r['C']}")
            i=raw.find("<race-detail"); j=raw.find(':payload="',i); kk=raw.find('"',j+10); d=json.loads(html.unescape(raw[j+10:kk])); rc=d["race"]
            keep=["id","leavingNumber","name","age","sexe","avisEntraineur","changementEntraineur","firstFerrure","ferrure","firstJockey","firstGP","firstCorde","firstAutostart","courseRapprochee","isOldestLastRace","isClosestLastRace","crackSeries","commentairePartant","driverId","coachId","earningsAverage","record","recordAbsolu","newRecord","nonPartant","inedit","firstHerbGround","lastRaceDate","musics","song","earnings"]
            P=[{a:p.get(a) for a in keep} for p in rc["partants"]]
            fo.write(json.dumps(dict(d=r["d"],R=r["R"],C=r["C"],hip=r["hip"],code=code,categorie=rc.get("categorie"),autostart=rc.get("autostart"),allocation=rc.get("allocation"),partants=P),ensure_ascii=False)+"\n"); fo.flush(); n+=1
            if n%25==0: print(n,flush=True)
        except Exception as e: print("ERR",k,str(e)[:80],flush=True)
print("FINI",n,flush=True)
