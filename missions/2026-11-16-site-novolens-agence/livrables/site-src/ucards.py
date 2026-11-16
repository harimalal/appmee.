"""Section « Comprendre NOVOLENS en un coup d'œil » : 4 encarts successifs, photo en fond transparente + animation de l'action et du moyen."""
V, V2, LAV, LAV2, YEL, INK, GRN = "#4B39DD", "#7656F5", "#E8E2FF", "#F4F1FF", "#FFD84D", "#14102F", "#1F9D6B"
F = ''

def tick(x, y, d, color="#fff", w=2.6):
    return f'<path class="dr" style="--l:30;--d:{d}" d="m{x} {y} 4 4 8-9" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def u1():
    chips = ""
    for i, t in enumerate(["Secteur", "Taille", "Fonction"]):
        y = 34 + i * 40; d = 100 + i * 350
        chips += (f'<g class="a" style="--d:{d}"><rect x="8" y="{y}" width="112" height="30" rx="15" fill="#fff" stroke="#D9D0FF" stroke-width="1.5"/>'
                  f'<text x="22" y="{y+19}" font-size="12" font-weight="800" fill="{V}">{t}</text><circle cx="104" cy="{y+15}" r="9" fill="{GRN}"/>{tick(99, y+15, d+250)}</g>')
    return f'''<svg viewBox="0 0 300 190" aria-hidden="true">{chips}
<g transform="translate(214 98)"><circle class="a" style="--d:0" r="64" fill="#fff" stroke="#E0D8FF" stroke-width="2"/><circle class="a" style="--d:150" r="46" fill="{LAV2}" stroke="#D3C9FF" stroke-width="2"/>
<circle class="a" style="--d:300" r="28" fill="#fff" stroke="{V2}" stroke-width="3"/><circle class="a" style="--d:450" r="14" fill="{V2}"/><circle class="a" style="--d:600" r="5" fill="{YEL}"/><circle class="pl" r="14" fill="none" stroke="{V2}" stroke-width="2.5"/></g>
<g class="dart"><path d="M296 8 217 94" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><path d="M296 8l-4 16M296 8l-16 4" stroke="{V}" stroke-width="6" stroke-linecap="round"/></g></svg>'''

def u2(P):
    def ico(path, x, y):
        return f'<g transform="translate({x-10} {y-10}) scale(.83)" fill="none" stroke="{V}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</g>'
    nodes = [(238, 30, ico(P["phone"], 238, 30)), (264, 95, ico(P["mail"], 264, 95)), (238, 160, f'<text x="238" y="165" text-anchor="middle" font-size="14" font-weight="800" fill="{V}">in</text>')]
    lines = "".join(f'<path class="dash-flow" d="M64 95 L{x} {y}" stroke="#B9AEFF" stroke-width="2.2" fill="none"/>' for x, y, _ in nodes)
    pk = "".join(f'<circle class="pk" style="offset-path:path(\'M64 95 L{x} {y}\');--pd:{i*420}ms" cx="0" cy="0" r="5.5" fill="{YEL}" stroke="{INK}" stroke-width="1.4"/>' for i, (x, y, _) in enumerate(nodes))
    nn = "".join(f'<g class="a" style="--d:{300+i*220}"><circle cx="{x}" cy="{y}" r="23" fill="#fff" stroke="#D9D0FF" stroke-width="2"/>{g}</g>' for i, (x, y, g) in enumerate(nodes))
    return f'''<svg viewBox="0 0 300 190" aria-hidden="true">{lines}{nn}
<g class="a" style="--d:0"><circle cx="58" cy="95" r="32" fill="{V}"/><circle class="pl" cx="58" cy="95" r="32" fill="none" stroke="{V2}" stroke-width="2.5"/><circle cx="58" cy="95" r="12" fill="none" stroke="#fff" stroke-width="5"/><circle cx="58" cy="95" r="3.5" fill="#fff"/></g>{pk}
<g class="a" style="--d:900"><rect x="6" y="8" width="104" height="26" rx="13" fill="#fff" stroke="#D9D0FF" stroke-width="1.5"/><text x="18" y="25" font-size="11" font-weight="800" fill="{V}">128 comptes ciblés</text></g>
<g class="a" style="--d:1300"><rect x="6" y="152" width="120" height="30" rx="12" fill="#fff" stroke="#D9D0FF" stroke-width="1.5"/><text x="16" y="166" font-size="10.5" font-weight="700" fill="#8A83B8">86 décideurs contactés</text><rect x="16" y="172" width="100" height="5" rx="2.5" fill="{LAV}"/><rect class="grow-x" x="16" y="172" width="100" height="5" rx="2.5" fill="{V2}"/></g></svg>'''

def u3():
    falls = ""
    for i, x in enumerate([50, 80, 110, 140, 70, 120]):
        rej = i % 3 == 1
        falls += f'<circle class="{"rej" if rej else "fall"}" style="--e:{i*380}ms;--x:{-46 if i<3 else 46}px" cx="{x}" cy="14" r="8" fill="{"#FF8CA3" if rej else "#CFC6FF"}"/>'
    rows = ""
    for i, t in enumerate(["Décideur", "Besoin", "Intérêt"]):
        y = 44 + i * 40; d = 1200 + i * 450
        rows += (f'<g class="a" style="--d:{d}"><rect x="188" y="{y}" width="104" height="30" rx="15" fill="#fff" stroke="#D9D0FF" stroke-width="1.5"/><circle cx="204" cy="{y+15}" r="9" fill="{GRN}"/>{tick(199, y+15, d+200)}'
                 f'<text x="220" y="{y+19.5}" font-size="12" font-weight="800" fill="{INK}">{t}</text></g>')
    return f'''<svg viewBox="0 0 300 190" aria-hidden="true"><defs><linearGradient id="ufg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{V2}"/><stop offset="1" stop-color="{V}"/></linearGradient></defs>
<g class="a" style="--d:0"><path d="M16 36 H176 L118 108 V150 L74 168 V108 Z" fill="url(#ufg)"/></g>
<g class="a" style="--d:300"><text x="96" y="62" text-anchor="middle" font-size="10" font-weight="800" letter-spacing="1.6" fill="#fff">FILTRE</text></g>{falls}
<g class="a" style="--d:2300"><circle cx="96" cy="176" r="0" fill="{YEL}"/></g>{rows}</svg>'''

def u4():
    cells = ""
    rdv = {(0, 0): 700, (2, 0): 1050, (1, 1): 1400, (3, 1): 1750, (4, 2): 2100, (0, 2): 2450}
    for j in range(3):
        for i in range(5):
            x, y = 14 + i * 56, 52 + j * 42
            if (i, j) in rdv:
                d = rdv[(i, j)]
                cells += f'<g class="a" style="--d:{d}"><rect x="{x}" y="{y}" width="48" height="36" rx="10" fill="url(#urg)"/>{tick(x+16, y+18, d+200, w=3)}</g>'
            else:
                cells += f'<rect x="{x}" y="{y}" width="48" height="36" rx="10" fill="#fff" stroke="#DDD5FF" stroke-dasharray="3 4"/>'
    return f'''<svg viewBox="0 0 300 190" aria-hidden="true"><defs><linearGradient id="urg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{V2}"/><stop offset="1" stop-color="{V}"/></linearGradient></defs>
{cells}<g class="toast"><rect x="52" y="2" width="236" height="38" rx="13" fill="#fff" stroke="{YEL}" stroke-width="2.2"/><circle cx="74" cy="21" r="10" fill="{YEL}"/><path d="M69 24h10l-1.5-2.5v-4a3.5 3.5 0 0 0-7 0v4z" fill="{INK}"/>
<text x="92" y="18" font-size="12" font-weight="800" fill="{INK}">Nouveau rendez-vous</text><text x="92" y="31" font-size="10.5" font-weight="700" fill="{V}">Directeur Général · Industrie</text></g>
<g class="badge8"><circle cx="262" cy="160" r="26" fill="{YEL}" stroke="{INK}" stroke-width="2.5"/><text x="262" y="169" text-anchor="middle" font-size="22" font-weight="800" fill="{INK}">+8</text></g></svg>'''

def section(ic, P, heading_html, lead_html, wrap_id="video"):
    cards = [
      ("Calibrage", "On définit la cible parfaite avec vous.", u1(), [("users", "Atelier de cadrage"), ("target", "Client idéal")]),
      ("Prospection", "On contacte les bons décideurs à votre place.", u2(P), [("phone", "Téléphone"), ("mail", "E-mail"), ("in", "LinkedIn")]),
      ("Qualification", "On filtre : seuls les vrais intéressés passent.", u3(), [("phone", "Appel de qualification"), ("file", "Critères écrits")]),
      ("Rendez-vous", "Les rendez-vous tombent dans votre agenda.", u4(), [("calendar", "Agenda partagé"), ("file", "Dossier de contexte")]),
    ]
    out = ""
    for i, (t, sub, svg, means) in enumerate(cards):
        ms = "".join(f'<span class="mean">{("<b>in</b>" if k == "in" else ic(k))}{l}</span>' for k, l in means)
        out += f'''<div class="uwrap" data-reveal="{i*140}"><article class="ucard" style="--k:{i}"><div class="bg" style="background-image:url(img/card-{i+1}.jpg)" aria-hidden="true"></div>
<div class="u-top"><span class="u-num">{i+1}</span><h3>{t}</h3></div><p class="u-sub">{sub}</p><div class="u-anim">{svg}</div>
<div class="u-means"><small>Le moyen</small><div>{ms}</div></div></article></div>'''
    return f'''<section class="section band-soft" id="{wrap_id}"><div class="wrap"><div class="sec-head" data-reveal><p class="eyebrow">En 4 étapes</p><h2>{heading_html}</h2><p class="lead">{lead_html}</p></div>
<div class="ugrid" data-in-loop>{out}</div></div></section>'''
