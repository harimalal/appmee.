"""Historique complet des chevaux (letrot.com /v1/api/horses/<id>/perfs), usage prive, 1 requete / 3 s. Usage : python3 -I fetch_perfs.py <dossier_data> [nombre_max]"""
import sys, os, json, time, subprocess
D = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
ids = json.load(open(f"{D}/chevaux_ordre.json"))[:mx]; os.makedirs(f"{D}/perfs", exist_ok=True)
for n, h in enumerate(ids):
    f = f"{D}/perfs/{h}.json"
    if os.path.exists(f) and os.path.getsize(f) > 2: continue
    allp = []
    for page in (1, 2, 3, 4):
        r = subprocess.run(["curl", "-sS", "-m", "60", "-A", "Mozilla/5.0 (analyse privee)", "-H", "Accept: application/json",
                            f"https://www.letrot.com/v1/api/horses/{h}/perfs?limit=50&page={page}&excludeNP=true"], capture_output=True, text=True).stdout
        try: d = json.loads(r)
        except Exception: d = []
        allp += d if isinstance(d, list) else []
        time.sleep(3)
        if not isinstance(d, list) or len(d) < 50: break
    json.dump(allp, open(f, "w"))
    if n % 25 == 0: print(n, len(ids), h, len(allp), flush=True)
print("FINI")
