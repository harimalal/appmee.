"""Parcours animé : texte à gauche, illustration à droite, gain client en visuel."""

V, V2, LAV, LAV2, YEL, INK, GRN = "#4B39DD", "#7656F5", "#E8E2FF", "#F4F1FF", "#FFD84D", "#14102F", "#1F9D6B"

def _tick(x, y, d, color="#fff", w=3):
    return f'<path class="dr" style="--l:30;--d:{d}" d="m{x} {y} 5 5 9-10" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def il1():
    chips = ""
    for i, (t, y) in enumerate([("Secteur · Industrie", 142), ("Taille · ETI", 184), ("Fonction · DG", 226)]):
        d = 500 + i * 300
        chips += (f'<g class="a" style="--d:{d}"><rect x="44" y="{y}" width="160" height="30" rx="15" fill="{LAV2}" stroke="#D9D0FF"/>'
                  f'<text x="58" y="{y+19}" font-size="12" font-weight="700" fill="{V}">{t}</text>'
                  f'<circle cx="190" cy="{y+15}" r="9" fill="{GRN}"/>{_tick(185, y+14, d+250, w=2.4).replace("m185", "m185")}</g>')
    return f'''<svg class="il" viewBox="0 0 500 400" aria-hidden="true">
<g class="a" style="--d:0"><rect x="28" y="52" width="190" height="236" rx="22" fill="#fff" stroke="#DCD4FF" stroke-width="2"/>
<circle cx="74" cy="96" r="24" fill="{LAV}"/><circle cx="74" cy="90" r="9" fill="{V2}"/><path d="M57 113c5-14 29-14 34 0" fill="{V2}"/>
<rect x="108" y="84" width="88" height="10" rx="5" fill="#CFC6FF"/><rect x="108" y="102" width="56" height="10" rx="5" fill="{LAV}"/>
<text x="44" y="136" font-size="10" font-weight="700" letter-spacing="1.4" fill="#8A83B8">CLIENT IDÉAL</text></g>{chips}
<g transform="translate(362 196)"><circle class="a" style="--d:100" r="122" fill="#fff" stroke="#E4DCFF" stroke-width="2"/>
<circle class="a" style="--d:250" r="92" fill="{LAV2}" stroke="#D9D0FF" stroke-width="2"/><circle class="a" style="--d:400" r="62" fill="#fff" stroke="{V2}" stroke-width="3"/>
<circle class="a" style="--d:550" r="34" fill="{V2}"/><circle class="a" style="--d:700" r="12" fill="{YEL}"/>
<circle class="pl" r="34" fill="none" stroke="{V2}" stroke-width="3"/></g>
<g class="dart"><path d="M492 30 365 190" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><path d="M492 30l-6 24M492 30l-24 6" stroke="{V}" stroke-width="7" stroke-linecap="round"/></g>
<g class="burst"><path d="M362 196 L362 120M362 196 L430 196M362 196 L300 150M362 196 L440 130M362 196 L320 270" stroke="{YEL}" stroke-width="5" stroke-linecap="round"/></g></svg>'''

def il2():
    pts = [(390, 200), (320, 321), (180, 321), (110, 200), (180, 79), (320, 79)]
    lines = "".join(f'<path class="dash-flow" d="M250 200 L{x} {y}" stroke="#B9AEFF" stroke-width="2.4" fill="none"/>' for x, y in pts)
    nodes = ""
    for i, (x, y) in enumerate(pts):
        nodes += (f'<g class="a" style="--d:{300+i*140}"><circle cx="{x}" cy="{y}" r="27" fill="#fff" stroke="#D9D0FF" stroke-width="2.5"/>'
                  f'<circle cx="{x}" cy="{y-5}" r="8" fill="{V2}"/><path d="M{x-13} {y+14}c3-12 23-12 26 0" fill="{V2}"/></g>')
    pk = "".join(f'<circle class="pk" style="offset-path:path(\'M250 200 L{x} {y}\');animation-delay:{i*380}ms" cx="0" cy="0" r="6" fill="{YEL}" stroke="{INK}" stroke-width="1.5"/>' for i, (x, y) in enumerate(pts))
    return f'''<svg class="il" viewBox="0 0 500 400" aria-hidden="true">{lines}{nodes}
<g class="a" style="--d:0"><circle cx="250" cy="200" r="46" fill="{V}"/><circle cx="250" cy="200" r="46" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="3" class="pl"/><circle cx="250" cy="200" r="17" fill="none" stroke="#fff" stroke-width="6"/><circle cx="250" cy="200" r="5" fill="#fff"/></g>{pk}
<g class="a" style="--d:900"><rect x="14" y="14" width="156" height="46" rx="14" fill="#fff" stroke="#DCD4FF" stroke-width="2"/><text x="28" y="34" font-size="11" fill="#8A83B8" font-weight="600">Comptes ciblés</text><text x="28" y="53" font-size="17" font-weight="800" fill="{V}">128</text></g>
<g class="a" style="--d:1400"><rect x="316" y="342" width="172" height="48" rx="14" fill="#fff" stroke="#DCD4FF" stroke-width="2"/><text x="330" y="361" font-size="11" fill="#8A83B8" font-weight="600">Décideurs contactés · 86</text><rect x="330" y="372" width="144" height="8" rx="4" fill="{LAV}"/><rect class="grow-x" x="330" y="372" width="144" height="8" rx="4" fill="{V2}"/></g></svg>'''

def il3():
    falls = ""
    xs = [150, 190, 230, 270, 310, 350]
    for i, x in enumerate(xs):
        rej = i % 3 == 1
        cls = "rej" if rej else "fall"
        col = "#FF8CA3" if rej else "#CFC6FF"
        falls += f'<circle class="{cls}" style="--d:{i*420};--x:{(-1 if i < 3 else 1)*60}px" cx="{x}" cy="26" r="11" fill="{col}"/>'
    rows = ""
    for i, t in enumerate(["Décideur", "Besoin", "Intérêt"]):
        y = 236 + i * 38
        rows += (f'<g class="a" style="--d:{1100+i*450}"><rect x="344" y="{y}" width="140" height="30" rx="15" fill="#fff" stroke="#DCD4FF"/><circle cx="361" cy="{y+15}" r="9" fill="{GRN}"/>'
                 f'{_tick(356, y+14, 1300+i*450, w=2.4)}<text x="378" y="{y+19.5}" font-size="12.5" font-weight="700" fill="{INK}">{t}</text></g>')
    return f'''<svg class="il" viewBox="0 0 500 400" aria-hidden="true">
<g class="a" style="--d:0"><path d="M60 56 H320 L226 176 V258 L154 288 V176 Z" fill="url(#fg)"/></g>
<defs><linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{V2}"/><stop offset="1" stop-color="{V}"/></linearGradient></defs>
<g class="a" style="--d:300"><text x="190" y="98" text-anchor="middle" font-size="13" font-weight="800" letter-spacing="2" fill="#fff">QUALIFICATION</text></g>
<g transform="translate(-4 20)">{falls}</g>
<g class="a" style="--d:2200"><circle cx="190" cy="282" r="0" fill="{YEL}"/><circle cx="190" cy="304" r="18" fill="{YEL}" stroke="{INK}" stroke-width="2.5"/>{_tick(182, 303, 2300, INK, 3.2)}</g>
{rows}<g class="a" style="--d:600"><text x="352" y="222" font-size="10" font-weight="800" letter-spacing="1.4" fill="#8A83B8">CRITÈRES VÉRIFIÉS</text></g></svg>'''

def il4():
    cells = ""
    rdv = {(0, 0): 900, (2, 0): 1300, (1, 1): 1700, (3, 1): 2100, (4, 2): 2500, (0, 2): 2900}
    for j in range(3):
        for i in range(5):
            x, y = 52 + i * 84, 112 + j * 70
            if (i, j) in rdv:
                d = rdv[(i, j)]
                cells += (f'<g class="a" style="--d:{d}"><rect x="{x}" y="{y}" width="76" height="60" rx="14" fill="url(#rg)"/>'
                          f'{_tick(x+25, y+30, d+200, w=3.4)}<text x="{x+38}" y="{y+52}" text-anchor="middle" font-size="9" font-weight="800" fill="#fff" opacity=".9">RDV QUALIFIÉ</text></g>')
            else:
                cells += f'<rect x="{x}" y="{y}" width="76" height="60" rx="14" fill="{LAV2}" stroke="#E4DCFF" stroke-dasharray="4 5"/>'
    days = "".join(f'<text x="{90+i*84}" y="102" text-anchor="middle" font-size="10" font-weight="800" letter-spacing="1.4" fill="#8A83B8">{d}</text>' for i, d in enumerate(["LUN", "MAR", "MER", "JEU", "VEN"]))
    return f'''<svg class="il" viewBox="0 0 500 400" aria-hidden="true"><defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{V2}"/><stop offset="1" stop-color="{V}"/></linearGradient></defs>
<g class="a" style="--d:0"><rect x="30" y="40" width="440" height="318" rx="24" fill="#fff" stroke="#DCD4FF" stroke-width="2"/><rect x="30" y="40" width="440" height="40" rx="24" fill="{LAV}"/><rect x="30" y="62" width="440" height="18" fill="{LAV}"/>
<circle cx="56" cy="60" r="5" fill="{V2}"/><circle cx="74" cy="60" r="5" fill="#B9AEFF"/><circle cx="92" cy="60" r="5" fill="#D9D0FF"/><text x="108" y="65" font-size="11" font-weight="800" fill="{V}">Mon agenda · Novembre</text></g>{days}{cells}
<g class="toast"><rect x="236" y="10" width="258" height="52" rx="16" fill="#fff" stroke="{YEL}" stroke-width="2.5"/><circle cx="262" cy="36" r="13" fill="{YEL}"/><path d="M256 40h12l-2-3v-5a4 4 0 0 0-8 0v5z" fill="{INK}"/>
<text x="284" y="32" font-size="12.5" font-weight="800" fill="{INK}">Nouveau rendez-vous</text><text x="284" y="49" font-size="11" fill="{V}" font-weight="700">Directeur Général · Industrie</text></g>
<g class="badge8"><circle cx="446" cy="348" r="36" fill="{YEL}" stroke="{INK}" stroke-width="3"/><text x="446" y="358" text-anchor="middle" font-size="28" font-weight="800" fill="{INK}">+8</text></g></svg>'''

def il5():
    bars = ""
    vals = [1, 2, 4, 5, 7, 8]
    for i, v in enumerate(vals):
        h = v * 20
        col = YEL if i == 5 else f"url(#bg{i%2})"
        stroke = f' stroke="{INK}" stroke-width="2.5"' if i == 5 else ""
        bars += f'<rect class="rise" style="--d:{500+i*180}" x="{66+i*64}" y="{340-h}" width="42" height="{h}" rx="9" fill="{col}"{stroke}/>'
    kp = ""
    for i, (n, l) in enumerate([("128", "Ciblées"), ("24", "Qualifiées"), ("8", "RDV")]):
        kp += (f'<g class="a" style="--d:{200+i*150}"><rect x="{54+i*140}" y="58" width="128" height="54" rx="14" fill="{LAV2}" stroke="#E4DCFF"/>'
               f'<text x="{70+i*140}" y="88" font-size="24" font-weight="800" fill="{V}">{n}</text><text x="{70+i*140}" y="104" font-size="10.5" font-weight="600" fill="#8A83B8">{l}</text></g>')
    return f'''<svg class="il" viewBox="0 0 500 400" aria-hidden="true"><defs><linearGradient id="bg0" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{V2}"/><stop offset="1" stop-color="{V}"/></linearGradient><linearGradient id="bg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A998FF"/><stop offset="1" stop-color="{V2}"/></linearGradient></defs>
<g class="a" style="--d:0"><rect x="30" y="30" width="440" height="340" rx="24" fill="#fff" stroke="#DCD4FF" stroke-width="2"/></g>{kp}
<g stroke="#EEEAFB" stroke-width="2"><path d="M54 340H446M54 290H446M54 240H446M54 190H446"/></g>{bars}
<path class="dr" style="--l:420;--d:900" d="M87 322 C150 300 180 270 215 240 S300 200 340 170 S400 120 438 92" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
<g class="a" style="--d:2000"><circle cx="438" cy="92" r="9" fill="{GRN}" stroke="#fff" stroke-width="3"/><circle class="pl" cx="438" cy="92" r="9" fill="none" stroke="{GRN}" stroke-width="3"/></g></svg>'''

STEPS = [
 dict(key="calibrage", tab="Calibrage", title="On définit <mark class='hl'>la cible parfaite</mark> avec vous.",
      text="Un atelier pour fixer vos objectifs, votre client idéal et les critères d'un rendez-vous qui vaut le coup.",
      bullets=["Profil de client idéal et comptes prioritaires", "Message et argumentaire validés avec vous", "Critères de qualification écrits noir sur blanc"],
      gain=("target", "Une cible nette", "Dès la première semaine"), il=il1),
 dict(key="prospection", tab="Prospection", title="On <mark class='hl'>contacte les bons décideurs</mark> à votre place.",
      text="Téléphone, e-mail, LinkedIn : une équipe dédiée prospecte et relance avec persévérance, sans que vos commerciaux s'en occupent.",
      bullets=["Contacts sélectionnés et vérifiés", "Séquences multicanales personnalisées", "Relances jusqu'à une réponse claire"],
      gain=("clock", "Des heures rendues", "Vos équipes restent sur la vente"), il=il2),
 dict(key="qualification", tab="Qualification", title="On <mark class='hl'>filtre</mark> : seuls les vrais intéressés passent.",
      text="Chaque contact est vérifié sur le décideur, le besoin et l'intérêt. Ce qui ne passe pas le filtre ne vous est jamais livré.",
      bullets=["Fonction et pouvoir de décision confirmés", "Besoin et contexte identifiés", "Niveau d'intérêt évalué"],
      gain=("shield", "Zéro rendez-vous pour rien", "Que du potentiel réel"), il=il3),
 dict(key="rdv", tab="Rendez-vous", title="Les <mark class='hl'>rendez-vous tombent</mark> dans votre agenda.",
      text="Vous recevez des rendez-vous confirmés, avec un dossier complet : profil, contexte, besoin, prochaine étape.",
      bullets=["Rendez-vous confirmés dans votre agenda", "Fiche de contexte et compte rendu", "Vos commerciaux arrivent préparés"],
      gain=("calcheck", "Un agenda qui se remplit", "Des rendez-vous prêts à signer"), il=il4),
 dict(key="pilotage", tab="Pilotage", title="Vous <mark class='hl'>pilotez avec des chiffres</mark>, pas des impressions.",
      text="Un reporting partagé suit chaque étape, du compte ciblé au rendez-vous. Un point régulier ajuste la cible et le message.",
      bullets=["Tableau de bord partagé en continu", "Point de pilotage régulier", "Ajustements rapides de cible et de message"],
      gain=("trend", "Un pipeline prévisible", "Qui progresse semaine après semaine"), il=il5),
]

def story(ic, n=4):
    steps = STEPS[:n]
    tabs = "".join(
        f'<button class="story-tab" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-i="{i}"><span class="n">{i+1}</span><span>{s["tab"]}</span><i></i></button>'
        for i, s in enumerate(steps))
    slides = ""
    for i, s in enumerate(steps):
        bl = "".join(f"<li>{ic('checkc')}{b}</li>" for b in s["bullets"])
        gi, gt, gs = s["gain"]
        slides += f'''<div class="slide{" on" if i == 0 else ""}" data-i="{i}" role="tabpanel">
<div class="s-text"><span class="s-label">Étape {i+1} sur {len(steps)}</span><h3>{s["title"]}</h3><p>{s["text"]}</p><ul class="s-list">{bl}</ul>
<div class="gain-line"><span>Ce que vous gagnez</span><b>{gt}</b></div></div>
<div class="stage">{s["il"]()}<img class="photo" data-src="img/etape-{i+1}.jpg" alt="" width="1000" height="800" hidden>
<span class="photo-tag">Photo remplaçable : img/etape-{i+1}.jpg</span>
<div class="gain"><span class="g-ic">{ic(gi)}</span><div><small>Vous gagnez</small><b>{gt}</b><em>{gs}</em></div></div></div></div>'''
    return f'''<div class="story" data-story data-dur="7000"><div class="story-tabs" role="tablist" aria-label="Les étapes">{tabs}</div><div class="story-slides">{slides}</div></div>'''
