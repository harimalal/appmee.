"""Commentaires de fin de course des courses PRECEDENTES des chevaux (letrot.com, usage prive, 1 page / 3,5 s). La page est lue puis effacee ; seuls les commentaires sont gardes.
Usage : python3 -I fetch_comments.py <dossier_data> <dossier_tmp>"""
import sys, os, json, html, time, subprocess
import pandas as pd
D, T = sys.argv[1], sys.argv[2]; os.makedirs(T, exist_ok=True)
L = pd.read_csv(f"{D}/comments_links.csv"); links = sorted(L[L.rang_prev == 1].link.unique(), key=lambda s: s.split("/")[2], reverse=True)
out = f"{D}/comments_prev.jsonl"; done = set()
if os.path.exists(out): done = {json.loads(l)["link"] for l in open(out)}
with open(out, "a") as fo:
    for n, lk in enumerate(links):
        if lk in done: continue
        f = f"{T}/p.html"
        subprocess.run(["curl", "-sS", "-m", "60", "-A", "Mozilla/5.0 (analyse privee)", "-o", f, f"https://www.letrot.com{lk}"])
        rec = dict(link=lk, runners={})
        try:
            raw = open(f, encoding="utf-8", errors="ignore").read(); i = raw.find("<race-detail"); j = raw.find(':payload="', i); k = raw.find('"', j + 10)
            r = json.loads(html.unescape(raw[j + 10:k]))["race"]; rec["n"] = len(r["partants"])
            for p in r["partants"]:
                rec["runners"][p["id"]] = dict(c=(p.get("commentairePartant") or {}).get("commentairePostCourses"), rk=p.get("formattedRank"), n=p.get("leavingNumber"))
        except Exception as e: rec["err"] = str(e)[:80]
        fo.write(json.dumps(rec) + "\n"); fo.flush()
        if os.path.exists(f): os.remove(f)
        if n % 40 == 0: print(n, len(links), lk, len(rec["runners"]), flush=True)
        time.sleep(3.5)
print("FINI")
