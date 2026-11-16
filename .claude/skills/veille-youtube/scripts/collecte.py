#!/usr/bin/env python3
"""Collecte YouTube pour la veille : pages de résultats (filtre Vidéos) puis une page par chaîne.

Usage :
  python3 -I collecte.py --sortie dossier/ "requête 1" "requête 2" ...
Options : --max 40 (vidéos par requête), --hl fr, --pause 3 (secondes entre deux pages),
          --miniatures (télécharge les miniatures dans dossier/miniatures/).

Sorties dans le dossier :
  brut.json   toutes les vidéos trouvées, avec vues, date approximative, durée, abonnés
  lignes.json les vidéos retenues (filtres de references/methode.md), calculées et triées
  top.md      le classement lisible, à relire avant l'analyse

Ce script ne lit que les pages qu'un navigateur ouvrirait (une par requête, une par chaîne),
à un rythme humain. Si YouTube répond autre chose qu'une page normale (vérification « robot »,
consentement, code d'erreur), il s'arrête, garde ce qu'il a, et le dit : on bascule alors sur
la collecte au navigateur (Claude in Chrome) décrite dans references/methode.md.
Ne jamais chercher à contourner une vérification.
"""
import argparse, datetime, json, os, random, re, sys, time, urllib.parse, urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
FILTRE_VIDEOS = "EgIQAQ%3D%3D"  # filtre « Vidéos » de la page de résultats (exclut les Shorts listés à part)


class Bloque(Exception):
    pass


def page(url, langue):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": langue})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode("utf-8", "ignore")
    except Exception as e:
        raise Bloque(f"{url} : {e}")
    if "ytInitialData" not in html:
        raise Bloque(f"{url} : page inattendue (consentement ou vérification)")
    return html


def initial_data(html):
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        raise Bloque("ytInitialData introuvable")
    return json.loads(m.group(1))


def texte(x):
    x = x or {}
    return x.get("simpleText") or "".join(r.get("text", "") for r in x.get("runs", []))


def renderers(o, cle, out):
    if isinstance(o, dict):
        if cle in o:
            out.append(o[cle])
        for v in o.values():
            renderers(v, cle, out)
    elif isinstance(o, list):
        for v in o:
            renderers(v, cle, out)
    return out


def entier(t):
    """'146 837 vues' -> 146837 ; '1,2 M de vues' -> 1200000 ; 'Aucune vue' -> 0."""
    t = (t or "").replace(" ", " ").replace("\xa0", " ").lower()
    m = re.search(r"([\d][\d .,]*)\s*(k|m|md|b|mille|million|milliard)?", t)
    if not m:
        return 0
    n, u = m.group(1).strip(), (m.group(2) or "")
    if u:
        n = float(n.replace(" ", "").replace(",", "."))
        return int(n * {"k": 1e3, "mille": 1e3, "m": 1e6, "million": 1e6, "md": 1e9, "b": 1e9, "milliard": 1e9}[u])
    return int(re.sub(r"[ .,]", "", n))


def duree(t):
    p = [int(x) for x in (t or "0").split(":") if x.isdigit()]
    s = 0
    for x in p:
        s = s * 60 + x
    return s


UNITES = [("sec", 1 / 86400), ("min", 1 / 1440), ("heure", 1 / 24), ("hour", 1 / 24), ("jour", 1), ("day", 1),
          ("sem", 7), ("week", 7), ("mois", 30.4), ("m.", 30.4), ("month", 30.4), ("an", 365), ("year", 365)]


def age_jours(t):
    """'il y a 3 sem.' / '3 weeks ago' -> 21. Approximation : YouTube n'affiche qu'une date relative."""
    t = (t or "").lower()
    m = re.search(r"(\d+)\s*([a-zé.]+)", t)
    if not m:
        return None
    n, u = int(m.group(1)), m.group(2)
    for k, j in UNITES:
        if u.startswith(k) or u == k:
            return max(1, round(n * j))
    return None


def recherche(q, n, hl, pause):
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": q, "hl": hl}) + "&sp=" + FILTRE_VIDEOS
    data = initial_data(page(url, f"{hl},{hl[:2]};q=0.9"))
    out = []
    for v in renderers(data, "videoRenderer", [])[:n]:
        try:
            ch = v["ownerText"]["runs"][0]
            out.append({
                "i": v["videoId"], "t": texte(v.get("title")), "c": ch["text"],
                "cid": ch["navigationEndpoint"]["browseEndpoint"]["browseId"],
                "v": entier(texte(v.get("viewCountText"))), "pub": texte(v.get("publishedTimeText")),
                "a": age_jours(texte(v.get("publishedTimeText"))), "u": duree(texte(v.get("lengthText"))),
                "src": q,
            })
        except (KeyError, IndexError):
            continue
    time.sleep(pause + random.random())
    return out


def abonnes(cid, pause):
    html = page(f"https://www.youtube.com/channel/{cid}?hl=en", "en-US,en;q=0.9")
    time.sleep(pause + random.random())
    m = re.search(r'"accessibilityLabel":"([\d.,]+)\s*(thousand|million|billion)?\s*subscribers"', html)
    if m:
        n = float(m.group(1).replace(",", ""))
        return int(n * {"thousand": 1e3, "million": 1e6, "billion": 1e9}.get(m.group(2) or "", 1))
    m = re.search(r"([\d.,]+)([KMB]?) subscribers", html)
    if m:
        return int(float(m.group(1).replace(",", "")) * {"K": 1e3, "M": 1e6, "B": 1e9, "": 1}[m.group(2)])
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("requetes", nargs="+")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--max", type=int, default=40)
    ap.add_argument("--hl", default="fr")
    ap.add_argument("--pause", type=float, default=3)
    ap.add_argument("--miniatures", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.sortie, exist_ok=True)
    brut_f = os.path.join(a.sortie, "brut.json")
    vids = {}
    if os.path.exists(brut_f):  # reprise après un arrêt
        vids = {v["i"]: v for v in json.load(open(brut_f))}
    arret = None
    try:
        for q in a.requetes:
            for v in recherche(q, a.max, a.hl, a.pause):
                vids.setdefault(v["i"], v)
            print(f"« {q} » : {len(vids)} vidéos uniques", file=sys.stderr)
        cache = {}
        for v in vids.values():
            if v.get("s") is not None:
                cache[v["cid"]] = v["s"]
        for cid in sorted({v["cid"] for v in vids.values()} - set(cache)):
            cache[cid] = abonnes(cid, a.pause)
            for v in vids.values():
                if v["cid"] == cid:
                    v["s"] = cache[cid]
        print(f"{len(cache)} chaînes lues", file=sys.stderr)
    except Bloque as e:
        arret = str(e)
    json.dump(list(vids.values()), open(brut_f, "w"), ensure_ascii=False, indent=1)

    today = datetime.date.today()
    lignes = []
    for v in vids.values():
        s, age = v.get("s"), v.get("a")
        ok = bool(s) and age is not None and v["u"] >= 240 and v["v"] >= 500 and 2 <= age <= 365
        if not ok:
            continue
        q = v["v"] / s
        lignes.append(dict(v, d=(today - datetime.timedelta(days=age)).isoformat(), q=q,
                           m=round(v["v"] / (age / 30.4), 1), k="ok", n=age <= 7))
    lignes.sort(key=lambda x: (-x["q"], -x["m"]))
    for r, x in enumerate(lignes, 1):
        x["o"] = r
        x["g"] = 1 if r <= 15 else 2  # 1 = top 15 affiché en tête du rapport
    json.dump(lignes, open(os.path.join(a.sortie, "lignes.json"), "w"), ensure_ascii=False, indent=1)

    if a.miniatures:
        dmin = os.path.join(a.sortie, "miniatures")
        os.makedirs(dmin, exist_ok=True)
        for x in lignes[:30]:
            f = os.path.join(dmin, x["i"] + ".jpg")
            if not os.path.exists(f):
                try:
                    urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{x['i']}/hqdefault.jpg", f)
                except Exception as e:
                    print(f"miniature {x['i']} : {e}", file=sys.stderr)

    with open(os.path.join(a.sortie, "top.md"), "w") as f:
        f.write("| # | Ratio | Vues/mois | Vues | Abonnés | Âge (j) | Durée | Chaîne | Titre |\n|---|---|---|---|---|---|---|---|---|\n")
        for x in lignes:
            f.write(f"| {x['o']} | {x['q']:.1f} × | {x['m']:.0f} | {x['v']} | {x['s']} | {x['a']} | {x['u']//60} min | {x['c']} | [{x['t']}](https://www.youtube.com/watch?v={x['i']}) |\n")
    print(f"{len(vids)} vidéos trouvées, {len(lignes)} retenues -> {a.sortie}/top.md", file=sys.stderr)
    if arret:
        print(f"ARRÊT : YouTube a refusé une page ({arret}). Données partielles gardées ; relancer plus tard "
              "(la commande reprend où elle s'est arrêtée) ou finir au navigateur.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
