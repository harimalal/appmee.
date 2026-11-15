"""Commentaires de fin de course des 5 dernieres courses de chaque partant (pages letrot, 1 req / 3,5 s, page lue puis effacee). Usage : python3 -I deep_comments.py <dossier> <date AAAA-MM-JJ> <hip> <courses>"""
import sys, os, json, html, time, subprocess, glob
N=sys.argv[1]; DATE=sys.argv[2]; HIP=sys.argv[3]; D=f"{N}/data"; out=f"{D}/comments_prev.jsonl"
courses=[int(x) for x in sys.argv[4].split(",")]; links=set()
for c in courses:
    race=json.load(open(f"{D}/deep/{DATE}_{HIP}_C{c}.json"))
    for p in race["partants"]:
        f=f"{D}/perfs/{p['id']}.json"
        if not os.path.exists(f): continue
        for x in [x for x in json.load(open(f)) if x["datePerf"][:10]<DATE][:5]:
            ip=x.get("idPerf","").split("-")  # 2026-09-27-7500-1-11
            if len(ip)>=5: links.add(f"/courses/{'-'.join(ip[:3])}/{ip[3]}/{ip[4]}")
done=set()
if os.path.exists(out): done={json.loads(l)["link"] for l in open(out)}
todo=sorted(links-done); print(len(links),"pages precedentes,",len(todo),"a lire",flush=True)
with open(out,"a") as fo:
    for n,lk in enumerate(todo):
        f=f"{N}/data/deep/tmp.html"; subprocess.run(["curl","-sS","-m","60","-A","Mozilla/5.0 (analyse privee)","-o",f,f"https://www.letrot.com{lk}"]); rec=dict(link=lk,runners={})
        try:
            raw=open(f,encoding="utf-8",errors="ignore").read(); i=raw.find("<race-detail"); j=raw.find(':payload="',i); k=raw.find('"',j+10); r=json.loads(html.unescape(raw[j+10:k]))["race"]
            for p in r["partants"]: rec["runners"][p["id"]]=dict(c=(p.get("commentairePartant") or {}).get("commentairePostCourses"),rk=p.get("formattedRank"),n=p.get("leavingNumber"))
        except Exception as e: rec["err"]=str(e)[:80]
        fo.write(json.dumps(rec)+"\n"); fo.flush(); os.path.exists(f) and os.remove(f)
        if n%25==0: print(n,len(todo),flush=True)
        time.sleep(3.5)
print("FINI",flush=True)
