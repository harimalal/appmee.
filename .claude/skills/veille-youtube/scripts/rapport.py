#!/usr/bin/env python3
"""Ajoute ou remplace un rapport dans la page « Veille YouTube ».

Usage :
  python3 -I rapport.py page.html rapport.json [--miniatures dossier/] [--retirer r1]

- page.html : la page existante (au départ, une copie de assets/veille-youtube-modele.html).
- rapport.json : un rapport au format de references/format-rapport.md. Ses lignes (rows)
  peuvent venir telles quelles de lignes.json (collecte.py) : les champs calculés manquants
  (q, m, o, g, n, kpi) sont complétés ici.
- --miniatures : dossier des miniatures <id>.jpg ; chaque miniature est réduite à 320×180
  et intégrée dans la page (champ h), pour que la page reste un seul fichier.
- --retirer : supprime un rapport par son id (ex. le rapport d'exemple r1 du modèle).

Un rapport de même id est remplacé ; sinon il est ajouté avec un nouvel id et un seq suivant.
"""
import argparse, base64, io, json, os, re, sys

PH = ("data:image/svg+xml;base64," + base64.b64encode(
    b'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180"><rect width="320" height="180" fill="#1b2335"/>'
    b'<text x="160" y="96" fill="#8A94A8" font-family="sans-serif" font-size="16" text-anchor="middle">miniature</text></svg>').decode())


def miniature(path):
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        w, h = im.size
        t = w * 9 / 16  # recadre en 16:9 (hqdefault a des bandes noires)
        if h > t:
            im = im.crop((0, (h - t) / 2, w, (h + t) / 2))
        im = im.resize((320, 180))
        b = io.BytesIO()
        im.save(b, "JPEG", quality=55, optimize=True, progressive=True)
        return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    except Exception:
        return "data:image/jpeg;base64," + base64.b64encode(open(path, "rb").read()).decode()


def completer(r, dmin):
    rows = r["rows"]
    for v in rows:
        v.setdefault("k", "ok")
        if v.get("q") is None and v.get("s"):
            v["q"] = v["v"] / v["s"]
        if v.get("m") is None and v.get("a"):
            v["m"] = round(v["v"] / (v["a"] / 30.4), 1)
        v.setdefault("n", (v.get("a") or 99) <= 7)
        if not v.get("h"):
            f = os.path.join(dmin, v["i"] + ".jpg") if dmin else ""
            v["h"] = miniature(f) if f and os.path.exists(f) else PH
        for k in ("cid", "pub", "src", "b"):
            v.pop(k, None)
    rows.sort(key=lambda x: (-(x.get("q") or 0), -(x.get("m") or 0)))
    for i, v in enumerate(rows, 1):
        v["o"] = i
        v["g"] = 1 if i <= 15 else 2
    if rows and "kpi" not in r:
        bv = max(rows, key=lambda x: x["v"])
        br = rows[0]
        r["kpi"] = {"n": len(rows), "nr": sum(1 for x in rows if (x.get("q") or 0) >= 3),
                    "bv": {"t": bv["t"], "c": bv["c"], "v": bv["v"]},
                    "br": {"c": br["c"], "q": br["q"], "s": br["s"]}}
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("rapport", nargs="?")
    ap.add_argument("--miniatures")
    ap.add_argument("--retirer", action="append", default=[])
    a = ap.parse_args()
    s = open(a.page, encoding="utf-8").read()
    m = re.search(r'(<script id="data" type="application/json">)(.*?)(</script>)', s, re.S)
    if not m:
        sys.exit("bloc <script id=\"data\"> introuvable : la page n'est pas une page Veille YouTube")
    d = json.loads(m.group(2))
    d["reports"] = [r for r in d["reports"] if r["id"] not in a.retirer]
    if a.rapport:
        r = completer(json.load(open(a.rapport, encoding="utf-8")), a.miniatures)
        ids = [x["id"] for x in d["reports"]]
        if r.get("id") in ids:
            d["reports"][ids.index(r["id"])] = r
        else:
            n = max([int(re.sub(r"\D", "", i) or 0) for i in ids] + [0]) + 1
            r["id"] = f"r{n}"
            r["seq"] = max([x.get("seq", 0) for x in d["reports"]] + [0]) + 1
            d["reports"].append(r)
        print(f"rapport {r['id']} « {r['name']} » : {len(r['rows'])} vidéos", file=sys.stderr)
    blob = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    open(a.page, "w", encoding="utf-8").write(s[:m.start(2)] + blob + s[m.end(2):])
    print(f"{a.page} : {len(d['reports'])} rapport(s), {os.path.getsize(a.page) // 1024} Ko", file=sys.stderr)


if __name__ == "__main__":
    main()
