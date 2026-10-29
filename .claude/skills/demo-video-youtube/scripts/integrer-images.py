#!/usr/bin/env python3
"""Remplit le bloc <script id="assets"> d'un diaporama : images en data URI + données.

Usage :
  python3 -I integrer-images.py demo.html \
     --img t_n1=miniatures/abc.jpg --img page=capture.jpg \
     --mur dossier_miniatures/ --json donnees.json

--img cle=fichier   une image (miniature 640×360, ou capture de page gardée en 1720 px de large
                    pour les clés page / apercu / toute clé qui commence par « page »)
--libre cle=fichier une image gardée dans ses proportions (story, visuel carré, galerie
                    affichée en grand), plus grand côté ramené à 1400 px
--mur dossier/      toutes les images du dossier, réduites à 240×135, dans A.wall (mur de miniatures)
--json f.json       fusionne des données (sheet, geo, listes…) dans A
--geo f.geo.json    raccourci : A.geo = contenu du fichier (sortie de capturer-page.cjs)

Le fichier reste un seul HTML autonome. Taille visée : moins de 15 Mo (limite d'un artefact : 16 Mo).
"""
import argparse, base64, glob, io, json, os, re, sys


def libre(path, cote=1400):
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        im.thumbnail((cote, cote))
        b = io.BytesIO()
        im.save(b, "JPEG", quality=80, optimize=True, progressive=True)
        return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    except ImportError:
        return uri(path, 0, 0, page=True)


def uri(path, w, h, page=False):
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        if page:
            if im.width > w:
                im = im.resize((w, round(im.height * w / im.width)))
            q = 78
        else:
            sw, sh = im.size  # recadre au ratio voulu (supprime les bandes des miniatures YouTube)
            t = sw * h / w
            if sh > t:
                im = im.crop((0, (sh - t) / 2, sw, (sh + t) / 2))
            im = im.resize((w, h))
            q = 72
        b = io.BytesIO()
        im.save(b, "JPEG", quality=q, optimize=True, progressive=True)
        return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    except ImportError:
        ext = os.path.splitext(path)[1].lstrip(".").replace("jpg", "jpeg") or "jpeg"
        return f"data:image/{ext};base64," + base64.b64encode(open(path, "rb").read()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--img", action="append", default=[])
    ap.add_argument("--libre", action="append", default=[])
    ap.add_argument("--mur")
    ap.add_argument("--json", action="append", default=[])
    ap.add_argument("--geo")
    a = ap.parse_args()
    s = open(a.html, encoding="utf-8").read()
    m = re.search(r'(<script id="assets" type="application/json">)(.*?)(</script>)', s, re.S)
    if not m:
        sys.exit('bloc <script id="assets"> introuvable')
    A = json.loads(m.group(2))
    # données d'abord : une clé vide dans le JSON ne doit pas écraser une image passée en --img
    for f in a.json:
        A.update(json.load(open(f, encoding="utf-8")))
    for kv in a.img:
        k, f = kv.split("=", 1)
        page = k.startswith("page") or k == "apercu"
        A[k] = uri(f, 1720, 0, page=True) if page else uri(f, 640, 360)
    for kv in a.libre:
        k, f = kv.split("=", 1)
        A[k] = libre(f)
    if a.mur:
        fs = sorted(f for f in glob.glob(os.path.join(a.mur, "*")) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
        A["wall"] = [uri(f, 240, 135) for f in fs]
    if a.geo:
        A["geo"] = json.load(open(a.geo, encoding="utf-8"))
    blob = json.dumps(A, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    open(a.html, "w", encoding="utf-8").write(s[:m.start(2)] + blob + s[m.end(2):])
    mo = os.path.getsize(a.html) / 1e6
    print(f"{a.html} : {len(A)} clés, {mo:.1f} Mo" + ("  ATTENTION : au-delà de 15 Mo, réduire le mur ou les captures" if mo > 15 else ""))


if __name__ == "__main__":
    main()
