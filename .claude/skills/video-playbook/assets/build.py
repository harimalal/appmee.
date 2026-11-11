"""Assemble un playbook vidéo.

Usage : python3 build.py <dossier_de_travail>

Le dossier de travail contient :
  body.html   le contenu des pages (copié depuis template.body.html puis rempli)
  content.py  META, FIGURES (fonction), G (glossaire), CH (chapitres), VERIFY, SRC
  extra.js    (optionnel) le script d'un outil interactif propre à ce playbook

Produit dans le dossier de travail :
  playbook.artifact.html  fragment à publier avec l'outil Artifact (sans doctype)
  playbook.full.html      page complète, pour les contrôles Playwright
et, si META["out"] est défini, une copie de la page complète dans ce dossier.

Syntaxe dans body.html :
  {{FIG:nom}}   remplacé par la figure F["nom"] construite dans content.FIGURES
  {{LEXIQUE}}   remplacé par les tableaux du lexique
  {{SOURCES}}   remplacé par chapitrage + noms à vérifier + sources
  [[1:23:45]]   horodatage cliquable vers la vidéo
  {V} {A} {O} {Q}  étiquettes VIDÉO, APPROFONDI, AVIS, À VÉRIFIER
"""
import html, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")


# ---------- aides SVG (importées par content.py : from build import *) ----------
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
def T(x, y, s, c="sv-t", a="start"):
    """Texte. Classes : sv-t normal, sv-tb gras, sv-tm petit mono gris, sv-oklbl vert, sv-nolbl rouge."""
    return f'<text class="{c}" x="{x}" y="{y}" text-anchor="{a}">{esc(s)}</text>'
def box(x, y, w, h, lines, cls="", center=True, title=True, top=False, pad=14):
    """Boîte avec lignes de texte ; la 1re ligne est en gras s'il y en a plusieurs.
    cls : "" neutre, "c" bleu (préparer), "n" vert (faire), "h" jaune (accélérer), "d" pointillé (option), "u" humain."""
    n = len(lines); lh = 17
    y0 = y + 24 if top else y + (h - (n - 1) * lh) / 2 + 4.5
    o = f'<rect class="sv-bx {cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
    for i, s in enumerate(lines):
        c = "sv-tb" if (title and i == 0 and n > 1) else "sv-t"
        o += T(x + w / 2, y0 + i * lh, s, c, "middle") if center else T(x + pad, y0 + i * lh, s, c)
    return o
def dia(cx, cy, hw, hh, lines):
    """Losange de décision (logigramme)."""
    o = f'<polygon class="sv-dec" points="{cx-hw},{cy} {cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh}"/>'
    y0 = cy - (len(lines) - 1) * 8 + 4.5
    for i, s in enumerate(lines): o += T(cx, y0 + i * 16, s, "sv-t", "middle")
    return o
def ar(x1, y1, x2, y2, m, c=""):
    """Flèche droite. c : "" encre, "ok" vert, "no" rouge, "d" pointillé."""
    return f'<line class="sv-ln {c}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#{m})"/>'
def pa(d, m, c=""): return f'<path class="sv-ln {c}" d="{d}" marker-end="url(#{m})"/>'
def band(x, y, w, h, s): return f'<rect class="sv-band" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>' + T(x + w / 2, y + h / 2 + 4.5, s, "sv-t", "middle")
def defs(m): return (f'<defs><marker id="{m}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker>'
    f'<linearGradient id="{m}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#17B26A"/><stop offset="1" stop-color="#8CF5BE"/></linearGradient></defs>')
def pill(x, y, w, h, s, m): return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="url(#{m}g)"/>'
    f'<text class="sv-tb" style="fill:#04140D" x="{x+w/2}" y="{y+h/2+4.5}" text-anchor="middle">{esc(s)}</text>')
def fig(inner, w, h, label, cap, m, minw=720):
    """Figure numérotée automatiquement. m : identifiant unique par figure (marqueurs, dégradé).
    label : description complète pour les lecteurs d'écran. cap : légende (HTML, étiquettes et [[horodatages]] permis)."""
    return (f'<figure><div class="fw"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}" style="min-width:{minw}px">{defs(m)}{inner}</svg></div>'
            f'<figcaption>{cap}</figcaption></figure>')
def chain(labels, m, y=30, w=920, bw=156, h=60, classes=None, ops=None):
    """Raccourci : une rangée de boîtes reliées par des flèches (labels = liste de listes de lignes)."""
    n = len(labels); gap = (w - 10 - n * bw) / max(n - 1, 1); o = ""
    for k, L in enumerate(labels):
        x = 5 + k * (bw + gap)
        o += box(x, y, bw, h, L, (classes or [""] * n)[k])
        if k < n - 1:
            o += ar(x + bw, y + h / 2, x + bw + gap - 2, y + h / 2, m)
            if ops: o += T(x + bw + gap / 2, y + h / 2 - 10, ops[k], "sv-tm", "middle")
    return o


def main():
    sys.path.insert(0, HERE)
    spec = importlib.util.spec_from_file_location("content", os.path.join(WD, "content.py"))
    C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
    META = C.META
    yt = "https://www.youtube.com/watch?v=" + META["video_id"]
    body = open(os.path.join(WD, "body.html"), encoding="utf-8").read()
    body = re.sub(r"<!--.*?-->\s*", "", body, flags=re.S)  # les commentaires du gabarit ne sont pas publiés

    F = C.FIGURES() if hasattr(C, "FIGURES") else {}
    missing = sorted(set(re.findall(r"\{\{FIG:(\w+)\}\}", body)) - set(F))
    assert not missing, f"figures manquantes : {missing}"
    body = re.sub(r"\{\{FIG:(\w+)\}\}", lambda mm: F[mm.group(1)], body)

    G = C.G
    gloss = [{"m": g[1], "cs": g[2], "t": g[0], "d": g[3]} for g in G]
    def rows(kind):
        return "".join(f"<tr><td>{html.escape(g[0])}</td><td>{html.escape(g[3])}</td></tr>"
                       for g in sorted([g for g in G if g[4] == kind], key=lambda x: x[0].lower()))
    lex = ('<h3>Acronymes</h3><div class="tw"><table><tr><th>Sigle</th><th>Signification</th></tr>' + rows("acr") + "</table></div>"
           "<h3>Jargon et termes de l'épisode</h3><div class=\"tw\"><table><tr><th>Terme</th><th>En clair</th></tr>" + rows("jar") + "</table></div>")
    body = body.replace("{{LEXIQUE}}", lex)

    names = dict(re.findall(r'<section class="page" id="([a-z0-9]+)" data-title="([^"]+)"', body))
    def link(p): return '<a href="#' + p + '">' + html.escape(names[p]) + '</a>' if p else "—"
    tr = "".join("<tr><td>[[" + t + "]]</td><td>" + html.escape(c) + "</td><td>" + link(p) + "</td></tr>" for t, c, p in C.CH)
    src = '<ul class="src">' + "".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for u, t in C.SRC) + "</ul>"
    sources = ("<h3>Chapitrage de l'épisode</h3><div class=\"tw\"><table><tr><th>Passage</th><th>Chapitre</th><th>Page du playbook</th></tr>" + tr + "</table></div>"
               "<h3>Noms et passages à vérifier</h3><ul>" + "".join(f"<li>{v}</li>" for v in C.VERIFY) + "</ul>"
               f"<h3>Sources de la recherche (relevé en {META['releve']})</h3>" + src +
               '<p class="muted">Beaucoup de ces pages sont des blogs d\'éditeurs ou des comparatifs ; les prix changent souvent. Confirmez sur la page officielle avant de décider.</p>')
    body = body.replace("{{SOURCES}}", sources)

    body = re.sub(r"\[\[([0-9:]+)\]\]", lambda mm: f'<a class="ts" href="{yt}" data-t="{mm.group(1)}">{mm.group(1)}</a>', body)
    for k, v in {"{V}": '<span class="tg v">VIDÉO</span>', "{A}": '<span class="tg a">APPROFONDI</span>',
                 "{O}": '<span class="tg o">AVIS</span>', "{Q}": '<span class="tg q">À VÉRIFIER</span>'}.items():
        body = body.replace(k, v)
    left = re.findall(r"\{\{\w+|\[\[[^\]]*|\{[VAOQ]\}", body)
    assert not left, f"marqueurs non remplacés : {left[:5]}"

    css = open(os.path.join(HERE, "engine.css"), encoding="utf-8").read()
    js = (open(os.path.join(HERE, "engine.js"), encoding="utf-8").read()
          .replace("__GLOSS__", json.dumps(gloss, ensure_ascii=False))
          .replace("__VIDEO_URL__", yt).replace("__STORE_KEY__", "playbook-" + META["slug"]))
    extra = os.path.join(WD, "extra.js")
    if os.path.exists(extra): js += "\n" + open(extra, encoding="utf-8").read()
    head = (f'<title>{html.escape(META["tab_title"])}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700&family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap">\n'
            "<style>\n" + css + "\n</style>\n")
    frag = head + body + "\n<script>\n" + js + "\n</script>\n"
    full = ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            + head + "</head><body>" + body + "\n<script>\n" + js + "\n</script>\n</body></html>")
    open(os.path.join(WD, "playbook.artifact.html"), "w", encoding="utf-8").write(frag)
    open(os.path.join(WD, "playbook.full.html"), "w", encoding="utf-8").write(full)
    if META.get("out"):
        os.makedirs(META["out"], exist_ok=True)
        open(os.path.join(META["out"], "index.html"), "w", encoding="utf-8").write(full)
    print("ok", len(frag), "octets · pages", body.count('class="page"'), "· figures", body.count("<figure>"), "· glossaire", len(G))


if __name__ == "__main__":
    main()
