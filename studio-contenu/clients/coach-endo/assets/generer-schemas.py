import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg') + '/'
INK, INK2, INK3 = '#12301F', '#2E4A3A', '#5C7566'
ACC, SUN, EDGE = '#1F7A4F', '#FFD84A', '#D1A91A'
BAND, STEP, CARD = '#E7EFDC', '#CFE8D6', '#FFFDF8'

BODY = 'M468 70 C590 70 646 140 626 240 C612 310 566 352 524 392 L518 440 C518 452 508 458 496 458 L440 458 C428 458 418 452 418 440 L412 392 C370 352 324 310 310 240 C290 140 346 70 468 70 Z'
CAVITY = 'M468 130 C536 130 556 178 544 232 C534 280 504 320 494 392 L442 392 C432 320 402 280 392 232 C380 178 400 130 468 130 Z'


def side(cyst=False):
    """Trompe + ovaire du côté gauche (à mettre en miroir pour le droit)."""
    s = f'<path d="M332 118 C270 86 208 98 174 150" fill="none" stroke="{INK}" stroke-width="24" stroke-linecap="round"/>'
    s += f'<path d="M332 118 C270 86 208 98 174 150" fill="none" stroke="{STEP}" stroke-width="13" stroke-linecap="round"/>'
    s += f'<g stroke="{INK}" stroke-width="5" stroke-linecap="round"><path d="M164 156 l-16 10"/><path d="M170 166 l-10 16"/><path d="M180 168 l-2 18"/></g>'
    s += f'<ellipse cx="146" cy="226" rx="54" ry="40" transform="rotate(-18 146 226)" fill="{CARD}" stroke="{INK}" stroke-width="5"/>'
    s += f'<circle cx="128" cy="222" r="9" fill="none" stroke="{INK3}" stroke-width="4"/><circle cx="162" cy="236" r="7" fill="none" stroke="{INK3}" stroke-width="4"/>'
    return s


def uterus(lining=True):
    s = f'<path d="{BODY}" fill="{STEP}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    if lining:
        s += f'<path d="{CAVITY}" fill="{SUN}" stroke="{EDGE}" stroke-width="4" stroke-linejoin="round"/>'
    s += f'<path d="M468 392 V458" stroke="{INK}" stroke-width="4"/>'
    s += side() + f'<g transform="translate(936 0) scale(-1 1)">{side()}</g>'
    return s


def dot(x, y, r=15):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SUN}" stroke="{INK}" stroke-width="4"/>'


def label(x, y, txt, anchor='start', size=32):
    w = len(txt) * size * 0.56 + 28
    x0 = x - 14 if anchor == 'start' else x - w + 14
    return f'<rect x="{x0:.0f}" y="{y - size + 2}" width="{w:.0f}" height="{size + 12}" rx="10" fill="{CARD}" opacity=".92"/><text x="{x}" y="{y}" font-size="{size}" font-weight="700" fill="{INK}" text-anchor="{anchor}">{txt}</text>'


def line(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK3}" stroke-width="3" stroke-linecap="round"/>'


def svg(w, h, body):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">{body}</svg>\n'


# 1. Anatomie normale annotée
b = uterus()
b += line(112, 64, 216, 100) + label(30, 62, 'Trompe')
b += line(96, 330, 124, 262) + label(30, 366, 'Ovaire')
b += line(690, 292, 536, 262) + label(700, 300, 'Endomètre')
b += line(690, 386, 596, 330) + label(700, 396, 'Utérus')
open(OUT + 'uterus.svg', 'w', encoding='utf8').write(svg(936, 500, b))


# 2. Comparaison : normal / endométriose
def panel(lesions):
    g = uterus()
    if lesions:
        g += dot(150, 226, 20) + dot(206, 120, 14) + dot(730, 150, 14) + dot(790, 236, 22)
        g += dot(372, 478, 15) + dot(468, 500, 15) + dot(566, 478, 15) + dot(630, 380, 13)
    return g


b = f'<g transform="translate(0 46) scale(.5)">{panel(False)}</g>'
b += f'<g transform="translate(468 46) scale(.5)">{panel(True)}</g>'
b += f'<path d="M468 20 V400" stroke="{STEP}" stroke-width="4" stroke-dasharray="2 12" stroke-linecap="round"/>'
b += f'<text x="234" y="34" font-size="34" font-weight="800" fill="{ACC}" text-anchor="middle">Normal</text>'
b += f'<text x="702" y="34" font-size="34" font-weight="800" fill="{INK}" text-anchor="middle">Endométriose</text>'
b += f'<text font-size="28" font-weight="600" fill="{INK2}" text-anchor="middle"><tspan x="234" y="352">L\'endomètre reste</tspan><tspan x="234" y="386">dans l\'utérus</tspan></text>'
b += f'<text font-size="28" font-weight="600" fill="{INK2}" text-anchor="middle"><tspan x="702" y="352">Un tissu semblable</tspan><tspan x="702" y="386">s\'installe ailleurs</tspan></text>'
open(OUT + 'comparaison.svg', 'w', encoding='utf8').write(svg(936, 410, b))

# 3. Localisations
b = uterus()
b += f'<ellipse cx="468" cy="552" rx="112" ry="52" fill="{BAND}" stroke="{INK}" stroke-width="5"/>'
b += f'<path d="M40 560 C110 520 150 600 220 560 S330 520 372 590" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round"/>'
b += f'<path d="M40 560 C110 520 150 600 220 560 S330 520 372 590" fill="none" stroke="{STEP}" stroke-width="28" stroke-linecap="round"/>'
b += dot(146, 226, 22) + dot(214, 118, 15) + dot(790, 226, 22)
b += dot(372, 410, 15) + dot(566, 410, 15) + dot(468, 498, 15) + dot(468, 548, 15) + dot(262, 586, 15)
b += line(96, 318, 128, 252) + label(30, 356, 'Ovaires')
b += line(120, 70, 206, 106) + label(40, 66, 'Trompes')
b += line(700, 380, 580, 408) + label(700, 392, 'Péritoine', size=32)
b += line(700, 452, 574, 410) + label(700, 464, 'Ligaments', size=32)
b += label(612, 560, 'Vessie')
b += label(40, 640, 'Intestin') + line(124, 626, 156, 590)
open(OUT + 'localisations.svg', 'w', encoding='utf8').write(svg(936, 660, b))


# 4. Cycle
def glyph(k):
    if k == 0:
        return ''.join(f'<rect x="{-34 + i * 6}" y="{20 - i * 22}" width="{68 - i * 12}" height="14" rx="7" fill="{ACC}"/>' for i in range(3))
    drop = 'M0 -36 C22 -8 30 4 30 18 A30 30 0 0 1 -30 18 C-30 4 -22 -8 0 -36 Z'
    if k == 1:
        return f'<path d="{drop}" fill="{ACC}"/>'
    if k == 2:
        return f'<circle r="54" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="3 12" stroke-linecap="round"/><path d="{drop}" transform="scale(.62) translate(0 6)" fill="{ACC}"/>'
    rays = ''.join(f'<path d="M0 -50 L0 -68" stroke="{INK}" stroke-width="7" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45))
    return f'{rays}<circle r="32" fill="{INK}"/><circle r="14" fill="{SUN}"/>'


names = [('Le tissu', 's\'épaissit'), ('Il', 'saigne'), ('Le sang reste', 'piégé'), ('Inflammation', 'et douleur')]
b = ''
for k in range(4):
    cx = 117 + k * 234
    b += f'<circle cx="{cx}" cy="100" r="82" fill="{SUN if k == 3 else STEP}" stroke="{INK}" stroke-width="5"/>'
    b += f'<g transform="translate({cx} 100)">{glyph(k)}</g>'
    b += f'<text x="{cx}" y="236" font-size="30" font-weight="800" fill="{INK}" text-anchor="middle">{names[k][0]}</text>'
    b += f'<text x="{cx}" y="274" font-size="30" font-weight="800" fill="{INK}" text-anchor="middle">{names[k][1]}</text>'
    if k < 3:
        b += f'<path d="M{cx + 92} 100 h46 m-14 -14 l14 14 -14 14" fill="none" stroke="{ACC}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
open(OUT + 'cycle.svg', 'w', encoding='utf8').write(svg(936, 296, b))
import math

# 5. Cercle vicieux (fonction réutilisable : 5 étapes + titre central)
def cercle(fichier, pills, centre):
    CX, CY, R = 468, 350, 270
    angles = [-90, -18, 54, 126, 198]
    b = f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{STEP}" stroke-width="18"/>'
    for a in [-54, 18, 90, 162, 234]:
        t = math.radians(a)
        px, py = CX + R * math.cos(t), CY + R * math.sin(t)
        dx, dy = -math.sin(t), math.cos(t)
        nx, ny = math.cos(t), math.sin(t)
        tip = (px + dx * 30, py + dy * 30)
        b1 = (px - dx * 16 + nx * 24, py - dy * 16 + ny * 24)
        b2 = (px - dx * 16 - nx * 24, py - dy * 16 - ny * 24)
        b += f'<path d="M{tip[0]:.1f} {tip[1]:.1f} L{b1[0]:.1f} {b1[1]:.1f} L{b2[0]:.1f} {b2[1]:.1f} Z" fill="{ACC}" stroke="{ACC}" stroke-width="4" stroke-linejoin="round"/>'
    for k, (l1, l2) in enumerate(pills):
        t = math.radians(angles[k])
        x, y = CX + R * math.cos(t), CY + R * math.sin(t)
        b += f'<rect x="{x - 135:.1f}" y="{y - 50:.1f}" width="270" height="100" rx="30" fill="{SUN if k == 0 else CARD}" stroke="{INK}" stroke-width="5"/>'
        b += f'<text x="{x:.1f}" y="{y - 6:.1f}" font-size="30" font-weight="800" fill="{INK}" text-anchor="middle">{l1}</text>'
        b += f'<text x="{x:.1f}" y="{y + 30:.1f}" font-size="30" font-weight="800" fill="{INK}" text-anchor="middle">{l2}</text>'
        b += f'<circle cx="{x - 135:.1f}" cy="{y - 50:.1f}" r="22" fill="{INK}"/><text x="{x - 135:.1f}" y="{y - 41:.1f}" font-size="26" font-weight="800" fill="#fff" text-anchor="middle">{k + 1}</text>'
    b += f'<text x="{CX}" y="{CY - 6}" font-size="58" font-weight="800" fill="{INK}" text-anchor="middle">{centre[0]}</text>'
    b += f'<text x="{CX}" y="{CY + 56}" font-size="58" font-weight="800" fill="{ACC}" text-anchor="middle">{centre[1]}</text>'
    b += f'<text x="{CX}" y="{CY + 104}" font-size="30" font-weight="600" fill="{INK3}" text-anchor="middle">{centre[2]}</text>'
    open(OUT + fichier, 'w', encoding='utf8').write(svg(936, 660, b))


cercle('cercle.svg', [('Cycle et', 'douleurs'), ('Fatigue,', 'sommeil haché'), ('Arrêts et', 'jours difficiles'), ('Baisse de', 'productivité'), ('Culpabilité,', 'stress, moral')], ('Le cercle', 'vicieux', "qui s'auto-alimente"))
cercle('cercle-intime.svg', [('Douleur pendant', 'ou après'), ('Appréhension,', "peur d'avoir mal"), ('Évitement,', 'distance'), ('Culpabilité,', 'incompréhension'), ('Tension', 'dans le couple')], ('Le cercle', 'du silence', 'qui éloigne'))

# 6. Leviers
def lev(k):
    if k == 0:
        s = f'<rect x="-38" y="-32" width="76" height="68" rx="12" fill="{CARD}" stroke="{INK}" stroke-width="6"/><rect x="-38" y="-32" width="76" height="20" rx="10" fill="{ACC}"/>'
        s += ''.join(f'<circle cx="{-20 + i * 20}" cy="{6 + j * 18}" r="5" fill="{INK}"/>' for i in range(3) for j in range(2))
        return s
    if k == 1:
        return f'<rect x="-46" y="-34" width="92" height="62" rx="18" fill="{CARD}" stroke="{INK}" stroke-width="6"/><path d="M-24 28 L-40 52 L-6 28 Z" fill="{CARD}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M-26 -14 h52 M-26 4 h34" stroke="{ACC}" stroke-width="7" stroke-linecap="round"/>'
    return f'<path d="M0 34 C-54 -2 -38 -46 -12 -36 C-4 -32 0 -24 0 -24 C0 -24 4 -32 12 -36 C38 -46 54 -2 0 34 Z" fill="{ACC}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'


labs = [('Comprendre', 'ses cycles'), ('Aménager', 'son poste'), ('Se faire', 'accompagner')]
b = ''
for k in range(3):
    cx = 156 + k * 312
    b += f'<circle cx="{cx}" cy="110" r="92" fill="{SUN if k == 1 else STEP}" stroke="{INK}" stroke-width="5"/><g transform="translate({cx} 112)">{lev(k)}</g>'
    b += f'<text x="{cx}" y="246" font-size="32" font-weight="800" fill="{INK}" text-anchor="middle">{labs[k][0]}</text><text x="{cx}" y="284" font-size="32" font-weight="800" fill="{INK}" text-anchor="middle">{labs[k][1]}</text>'
open(OUT + 'leviers.svg', 'w', encoding='utf8').write(svg(936, 310, b))
# 7. Dialogue : trois bulles
bulles = [
    (20, 20, SUN, 'left', ("Ce n'est pas vous,", "c'est la douleur.")),
    (256, 210, CARD, 'right', ('Dites-moi ce qui vous', 'fait du bien.')),
    (20, 400, STEP, 'left', ("On peut chercher d'autres", 'façons d\'être proches.')),
]
b = ''
for x, y, col, cote, (l1, l2) in bulles:
    w, h = 660, 150
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="36" fill="{col}" stroke="{INK}" stroke-width="5"/>'
    tx = x + 60 if cote == 'left' else x + w - 130
    ty = y + h
    b += f'<path d="M{tx} {ty} L{tx + (-10 if cote == "left" else 70)} {ty + 38} L{tx + 70} {ty} Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<rect x="{tx + 4}" y="{ty - 4}" width="62" height="9" fill="{col}"/>'
    b += f'<text x="{x + 40}" y="{y + 68}" font-size="38" font-weight="800" fill="{INK}">{l1}</text><text x="{x + 40}" y="{y + 114}" font-size="38" font-weight="800" fill="{INK}">{l2}</text>'
open(OUT + 'dialogue.svg', 'w', encoding='utf8').write(svg(936, 580, b))

# 8. Intimité : bien plus que les rapports
CX, CY, R = 468, 350, 250
labs = ['Tendresse', 'Complicité', 'Dialogue', 'Câlins', 'Rapports']
b = ''
pos = [(CX + R * math.cos(math.radians(a)), CY + R * math.sin(math.radians(a))) for a in [-90, -18, 54, 126, 198]]
for x, y in pos:
    b += f'<path d="M{CX} {CY} L{x:.1f} {y:.1f}" stroke="{STEP}" stroke-width="12" stroke-linecap="round"/>'
b += f'<circle cx="{CX}" cy="{CY}" r="104" fill="{SUN}" stroke="{INK}" stroke-width="5"/><text x="{CX}" y="{CY + 14}" font-size="42" font-weight="800" fill="{INK}" text-anchor="middle">Intimité</text>'
for k, (x, y) in enumerate(pos):
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="92" fill="{STEP if k % 2 == 0 else CARD}" stroke="{INK}" stroke-width="5"/><text x="{x:.1f}" y="{y + 10:.1f}" font-size="30" font-weight="800" fill="{INK}" text-anchor="middle">{labs[k]}</text>'
open(OUT + 'intimite.svg', 'w', encoding='utf8').write(svg(936, 660, b))
# 9. Parcours médical : frise verticale en 6 étapes
etapes = [
    ('Premiers symptômes', 'des règles très douloureuses'),
    ('« C\'est normal »', 'des douleurs minimisées'),
    ('Antalgiques', 'sans chercher la cause'),
    ('Autre avis, autre spécialiste', '3 à 4 professionnels en moyenne'),
    ('Examens ciblés', 'échographie, IRM pelvienne'),
    ('Le diagnostic', 'enfin un nom sur la douleur'),
]
b = ''
H0, DY = 62, 112
xs = [90, 150, 70, 150, 90, 120]
for k in range(len(etapes) - 1):
    y1, y2 = H0 + k * DY, H0 + (k + 1) * DY
    c = 150 if k % 2 == 0 else 30
    b += f'<path d="M{xs[k]} {y1 + 44} C{c} {y1 + 60} {c} {y2 - 60} {xs[k + 1]} {y2 - 44}" fill="none" stroke="{STEP}" stroke-width="12" stroke-linecap="round" stroke-dasharray="2 20"/>'
for k, (t, s) in enumerate(etapes):
    y = H0 + k * DY
    last = k == len(etapes) - 1
    b += f'<rect x="170" y="{y - 46}" width="750" height="92" rx="26" fill="{SUN if last else CARD}" stroke="{INK}" stroke-width="5"/>'
    b += f'<text x="204" y="{y - 6}" font-size="32" font-weight="800" fill="{INK}">{t}</text><text x="204" y="{y + 30}" font-size="27" font-weight="600" fill="{INK2}">{s}</text>'
    b += f'<circle cx="{xs[k]}" cy="{y}" r="44" fill="{ACC if last else STEP}" stroke="{INK}" stroke-width="5"/><text x="{xs[k]}" y="{y + 14}" font-size="40" font-weight="800" fill="{"#fff" if last else INK}" text-anchor="middle">{k + 1}</text>'
    b += f'<path d="M{xs[k] + 44} {y} H170" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
open(OUT + 'parcours.svg', 'w', encoding='utf8').write(svg(936, H0 + len(etapes) * DY - 40, b))


# 10. Questions à poser : trois bulles
def bulles(fichier, textes):
    cols = [SUN, CARD, STEP]
    cotes = ['left', 'right', 'left']
    ys = [20, 210, 400]
    b = ''
    for k, (l1, l2) in enumerate(textes):
        x, y, w, h, col, cote = (20 if cotes[k] == 'left' else 256), ys[k], 660, 150, cols[k], cotes[k]
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="36" fill="{col}" stroke="{INK}" stroke-width="5"/>'
        tx = x + 60 if cote == 'left' else x + w - 130
        ty = y + h
        b += f'<path d="M{tx} {ty} L{tx + (-10 if cote == "left" else 70)} {ty + 38} L{tx + 70} {ty} Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        b += f'<rect x="{tx + 4}" y="{ty - 4}" width="62" height="9" fill="{col}"/>'
        b += f'<text x="{x + 40}" y="{y + 68}" font-size="38" font-weight="800" fill="{INK}">{l1}</text><text x="{x + 40}" y="{y + 114}" font-size="38" font-weight="800" fill="{INK}">{l2}</text>'
    open(OUT + fichier, 'w', encoding='utf8').write(svg(936, 580, b))


bulles('questions.svg', [('Mes douleurs peuvent-elles', "venir d'une endométriose ?"), ('Quels examens me', 'conseillez-vous ?'), ('Vers quel spécialiste', "m'orienter ?")])

# 11. Causes de la fatigue : quatre flèches convergentes
b = ''
cx, cy = 468, 330
causes = [(190, 84, 'Douleur', 'chronique'), (746, 84, 'Inflammation', 'de fond'), (190, 576, 'Sommeil', 'perturbé'), (746, 576, 'Charge', 'mentale')]
for x, y, l1, l2 in causes:
    dx, dy = cx - x, cy - y
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    sx, sy = x + ux * 150, y + uy * 62
    ex, ey = cx - ux * 150, cy - uy * 130
    b += f'<path d="M{sx:.0f} {sy:.0f} L{ex:.0f} {ey:.0f}" stroke="{ACC}" stroke-width="10" stroke-linecap="round"/>'
    px, py = ex, ey
    nx, ny = -uy, ux
    b += f'<path d="M{px + ux * 30:.0f} {py + uy * 30:.0f} L{px - nx * 26:.0f} {py - ny * 26:.0f} L{px + nx * 26:.0f} {py + ny * 26:.0f} Z" fill="{ACC}"/>'
for x, y, l1, l2 in causes:
    b += f'<rect x="{x - 165}" y="{y - 52}" width="330" height="104" rx="30" fill="{CARD}" stroke="{INK}" stroke-width="5"/>'
    b += f'<text x="{x}" y="{y - 4}" font-size="34" font-weight="800" fill="{INK}" text-anchor="middle">{l1}</text><text x="{x}" y="{y + 36}" font-size="34" font-weight="800" fill="{INK}" text-anchor="middle">{l2}</text>'
b += f'<circle cx="{cx}" cy="{cy}" r="116" fill="{SUN}" stroke="{INK}" stroke-width="6"/><text x="{cx}" y="{cy + 18}" font-size="52" font-weight="800" fill="{INK}" text-anchor="middle">Fatigue</text>'
open(OUT + 'causes-fatigue.svg', 'w', encoding='utf8').write(svg(936, 660, b))

# 12. Nuit-type : courbe de sommeil avec réveils
b = ''
for y, t in [(90, 'Éveillée'), (190, 'Léger'), (290, 'Profond')]:
    b += f'<path d="M200 {y} H910" stroke="{STEP}" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round"/><text x="188" y="{y + 9}" font-size="26" font-weight="700" fill="{INK2}" text-anchor="end">{t}</text>'
pts = [(200, 90), (250, 90), (270, 190), (330, 190), (350, 290), (430, 290), (450, 190), (480, 190), (500, 90), (530, 90), (550, 190), (610, 190), (630, 290), (670, 290), (690, 190), (710, 90), (740, 90), (760, 190), (810, 190), (830, 90), (910, 90)]
b += f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{ACC}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>'
for x in (500, 710, 830):
    b += f'<circle cx="{x}" cy="90" r="20" fill="{SUN}" stroke="{INK}" stroke-width="5"/><text x="{x}" y="99" font-size="26" font-weight="800" fill="{INK}" text-anchor="middle">!</text>'
b += f'<path d="M200 350 H910" stroke="{INK3}" stroke-width="4"/>'
for x, t in [(200, '22 h'), (380, '0 h'), (560, '2 h'), (740, '4 h'), (910, '6 h')]:
    b += f'<path d="M{x} 350 v14" stroke="{INK3}" stroke-width="4"/><text x="{x}" y="398" font-size="28" font-weight="700" fill="{INK2}" text-anchor="middle">{t}</text>'
b += f'<circle cx="214" cy="446" r="16" fill="{SUN}" stroke="{INK}" stroke-width="4"/><text x="246" y="456" font-size="28" font-weight="700" fill="{INK}">Réveil causé par la douleur</text>'
open(OUT + 'nuit.svg', 'w', encoding='utf8').write(svg(936, 480, b))


# 13. Batteries : une nuit réparatrice / une nuit hachée
def batterie(x, y, n, col, titre, sous):
    s = f'<rect x="{x}" y="{y}" width="360" height="160" rx="30" fill="{CARD}" stroke="{INK}" stroke-width="6"/><rect x="{x + 360}" y="{y + 52}" width="26" height="56" rx="10" fill="{INK}"/>'
    for i in range(4):
        fill = col if i < n else STEP
        op = '1' if i < n else '.55'
        s += f'<rect x="{x + 20 + i * 83}" y="{y + 20}" width="70" height="120" rx="16" fill="{fill}" opacity="{op}"/>'
    s += f'<text x="{x + 180}" y="{y + 222}" font-size="36" font-weight="800" fill="{INK}" text-anchor="middle">{titre}</text><text x="{x + 180}" y="{y + 262}" font-size="28" font-weight="600" fill="{INK2}" text-anchor="middle">{sous}</text>'
    return s


b = batterie(30, 70, 4, ACC, 'Nuit réparatrice', 'on se réveille rechargée') + batterie(516, 70, 1, SUN, 'Nuit hachée', 'on démarre à plat')
b += f'<path d="M430 150 h46 m-14 -14 l14 14 -14 14" fill="none" stroke="{INK3}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
open(OUT + 'batterie.svg', 'w', encoding='utf8').write(svg(936, 400, b))


# 14. Soirée : arc de soirée en 4 repères
def pic(k):
    if k == 0:
        return f'<circle r="30" fill="{CARD}" stroke="{INK}" stroke-width="6"/><circle r="14" fill="none" stroke="{INK3}" stroke-width="5"/><path d="M-46 -22 v44 M46 -22 v44" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    if k == 1:
        return f'<rect x="-34" y="-26" width="68" height="46" rx="8" fill="{CARD}" stroke="{INK}" stroke-width="6"/><path d="M-12 26 h24" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M-44 -34 L44 34" stroke="{ACC}" stroke-width="8" stroke-linecap="round"/>'
    if k == 2:
        return f'<path d="M-30 -18 h56 v26 a28 28 0 0 1 -56 0 Z" fill="{CARD}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M26 -8 a16 16 0 0 1 0 28" fill="none" stroke="{INK}" stroke-width="6"/><path d="M-12 -34 q8 -10 0 -18 M6 -34 q8 -10 0 -18" fill="none" stroke="{ACC}" stroke-width="5" stroke-linecap="round"/>'
    return f'<path d="M14 -40 a40 40 0 1 0 28 56 a32 32 0 0 1 -28 -56 Z" fill="{SUN}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'


stops = [(130, 440, '19 h', 'Dîner léger'), (327, 230, '20 h', 'Écrans en pause'), (609, 230, '21 h', 'Tisane, lecture'), (806, 440, '22 h', 'Coucher régulier')]
b = f'<path d="M130 440 A359 359 0 0 1 806 440" fill="none" stroke="{STEP}" stroke-width="16" stroke-linecap="round" stroke-dasharray="2 26"/>'
for k, (x, y, h, t) in enumerate(stops):
    b += f'<circle cx="{x}" cy="{y}" r="78" fill="{SUN if k == 3 else STEP}" stroke="{INK}" stroke-width="5"/><g transform="translate({x} {y}) scale(.9)">{pic(k)}</g>'
    b += f'<text x="{x}" y="{y + 124}" font-size="40" font-weight="800" fill="{INK}" text-anchor="middle">{h}</text><text x="{x}" y="{y + 160}" font-size="28" font-weight="600" fill="{INK2}" text-anchor="middle">{t}</text>'
open(OUT + 'soiree.svg', 'w', encoding='utf8').write(svg(936, 640, b))
print('ok', os.listdir(OUT))
