"""Schémas du carrousel « maladies invisibles au travail » (charte EndoReconversion).
Sortie : assets/svg/mi-*.svg  (936 de large, polices héritées du moteur)."""
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg') + '/'
INK, INK2, INK3 = '#12301F', '#2E4A3A', '#5C7566'
ACC, SUN, EDGE = '#1F7A4F', '#FFD84A', '#D1A91A'
BAND, STEP, CARD = '#E7EFDC', '#CFE8D6', '#FFFDF8'


def svg(w, h, body, name):
    open(OUT + name, 'w', encoding='utf8').write(
        f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">{body}</svg>\n')


def card(x, y, w, h, title, subs, icon=None, fill=CARD, tsize=31, ssize=25):
    """Carte arrondie : pictogramme dans un rond à gauche, titre (str ou liste de lignes) et lignes à droite."""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
    tx = x + 24
    if icon:
        cx, cy = x + 58, y + h / 2
        s += f'<circle cx="{cx}" cy="{cy}" r="38" fill="{BAND}" stroke="{INK}" stroke-width="4"/>'
        s += f'<g transform="translate({cx} {cy})">{icon}</g>'
        tx = x + 112
    lines = [title] if isinstance(title, str) else title
    n = len(lines) + len(subs)
    top = y + (h - (len(lines) * (tsize + 4) + len(subs) * (ssize + 6))) / 2
    yy = top + tsize
    for t in lines:
        s += f'<text x="{tx}" y="{yy:.0f}" font-size="{tsize}" font-weight="800" fill="{INK}">{t}</text>'
        yy += tsize + 4
    yy += 2
    for t in subs:
        s += f'<text x="{tx}" y="{yy:.0f}" font-size="{ssize}" font-weight="600" fill="{INK2}">{t}</text>'
        yy += ssize + 6
    return s


def link(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK3}" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 10"/><circle cx="{x1}" cy="{y1}" r="8" fill="{SUN}" stroke="{INK}" stroke-width="3"/>'


def bolt(x, y, k=1.0, fill=SUN):
    return f'<path transform="translate({x} {y}) scale({k})" d="M10 -34 L-14 4 H2 L-8 34 L18 -8 H2 Z" fill="{fill}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'


# ---------- pictogrammes (centrés sur 0,0, rayon utile 28) ----------
IC_RINGS = f'<circle r="7" fill="{INK}"/><circle r="17" fill="none" stroke="{INK}" stroke-width="4"/><circle r="27" fill="none" stroke="{INK}" stroke-width="4" opacity=".5"/>'
IC_WAVE = f'<path d="M-28 6 L-18 6 L-12 -18 L-4 20 L4 -22 L12 14 L18 6 L28 6" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
IC_NERVE = f'<path d="M-28 0 H-8 M8 0 H28" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M-8 0 L-3 -9 L3 9 L8 0" fill="none" stroke="{ACC}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
IC_DOTS = f'<path d="M0 -26 C16 -26 26 -12 22 4 C18 18 8 26 0 26 C-8 26 -18 18 -22 4 C-26 -12 -16 -26 0 -26Z" fill="{STEP}" stroke="{INK}" stroke-width="4"/><circle cx="-7" cy="-4" r="5" fill="{SUN}" stroke="{INK}" stroke-width="2.5"/><circle cx="8" cy="8" r="5" fill="{SUN}" stroke="{INK}" stroke-width="2.5"/>'
IC_GUT = f'<path d="M-26 -16 H18 Q26 -16 26 -8 Q26 0 18 0 H-18 Q-26 0 -26 8 Q-26 16 -18 16 H26" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M-26 -16 H18 Q26 -16 26 -8 Q26 0 18 0 H-18 Q-26 0 -26 8 Q-26 16 -18 16 H26" fill="none" stroke="{SUN}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
IC_OVARY = f'<ellipse rx="24" ry="18" fill="{CARD}" stroke="{INK}" stroke-width="4"/><circle cx="-8" cy="-3" r="5" fill="none" stroke="{INK3}" stroke-width="3"/><circle cx="9" cy="5" r="4" fill="none" stroke="{INK3}" stroke-width="3"/><path d="M-26 -24 q18 -10 34 -4" fill="none" stroke="{ACC}" stroke-width="5" stroke-linecap="round"/>'
IC_MUSCLE = f'<path d="M-26 -14 q13 -12 26 0 t26 0 M-26 0 q13 -12 26 0 t26 0 M-26 14 q13 -12 26 0 t26 0" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
IC_JOINT = f'<circle r="13" fill="{SUN}" stroke="{INK}" stroke-width="4"/><g stroke="{INK}" stroke-width="4" stroke-linecap="round"><path d="M0 -20 V-28M0 20 V28M-20 0 H-28M20 0 H28M14 -14 L20 -20M-14 14 L-20 20M14 14 L20 20M-14 -14 L-20 -20"/></g>'
IC_BUTTERFLY = f'<path d="M0 0 C-10 -26 -30 -24 -28 -8 C-27 4 -12 8 0 0Z M0 0 C10 -26 30 -24 28 -8 C27 4 12 8 0 0Z M0 2 C-8 24 -22 24 -20 12 C-19 6 -8 2 0 2Z M0 2 C8 24 22 24 20 12 C19 6 8 2 0 2Z" fill="{STEP}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
IC_BATTERY = f'<rect x="-24" y="-14" width="44" height="28" rx="6" fill="none" stroke="{INK}" stroke-width="5"/><rect x="21" y="-6" width="6" height="12" rx="2" fill="{INK}"/><rect x="-18" y="-8" width="10" height="16" rx="2" fill="{SUN}"/>'
IC_DROP = f'<path d="M0 -26 C0 -26 -20 -2 -20 8 a20 20 0 0 0 40 0 C20 -2 0 -26 0 -26Z" fill="{SUN}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
IC_CLOUD = f'<path d="M-18 14 a12 12 0 0 1 2 -23 a16 16 0 0 1 30 4 a10 10 0 0 1 0 19Z" fill="{STEP}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><path d="M-8 20 l-4 8 M4 20 l-4 8 M16 20 l-4 8" stroke="{ACC}" stroke-width="4" stroke-linecap="round"/>'
IC_CAL = f'<rect x="-22" y="-20" width="44" height="42" rx="7" fill="{CARD}" stroke="{INK}" stroke-width="4"/><path d="M-22 -8 H22" stroke="{INK}" stroke-width="4"/><path d="M-10 -26 V-16 M10 -26 V-16" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><path d="M-9 6 l7 7 l13 -15" fill="none" stroke="{ACC}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
IC_EYE = f'<path d="M-28 0 Q0 -26 28 0 Q0 26 -28 0Z" fill="{CARD}" stroke="{INK}" stroke-width="4"/><circle r="9" fill="{INK}"/>'
IC_MOON = f'<path d="M10 -24 a24 24 0 1 0 14 34 a20 20 0 0 1 -14 -34Z" fill="{SUN}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
IC_BUBBLE = f'<path d="M-26 -20 H26 V10 H4 L-10 24 V10 H-26Z" fill="{CARD}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><path d="M-14 -9 H14 M-14 1 H4" stroke="{INK3}" stroke-width="4" stroke-linecap="round"/>'
IC_BOLT = bolt(0, 0, .8)
IC_SLIDERS = f'<path d="M-26 -14 H26 M-26 0 H26 M-26 14 H26" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="-10" cy="-14" r="8" fill="{SUN}" stroke="{INK}" stroke-width="4"/><circle cx="12" cy="0" r="8" fill="{SUN}" stroke="{INK}" stroke-width="4"/><circle cx="-4" cy="14" r="8" fill="{SUN}" stroke="{INK}" stroke-width="4"/>'
IC_KEY = f'<circle cx="-10" cy="-4" r="13" fill="{SUN}" stroke="{INK}" stroke-width="4"/><path d="M0 4 L24 22 M14 14 L22 6 M20 19 L28 11" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'


# ============ 1. Open space : ce qu'on ne voit pas ============
def person(x, hair, torso, hi=False):
    s = f'<rect x="{x - 62}" y="318" width="124" height="22" rx="6" fill="{CARD}" stroke="{INK}" stroke-width="5"/>'
    s += f'<path d="M{x - 50} 320 V304 Q{x - 50} 270 {x} 270 Q{x + 50} 270 {x + 50} 304 V320Z" fill="{torso}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    s += f'<circle cx="{x}" cy="236" r="29" fill="{CARD}" stroke="{INK}" stroke-width="5"/>'
    s += f'<path d="M{x - 30} 234 a30 30 0 0 1 60 0 q-30 -16 -60 0Z" fill="{hair}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<path d="M{x - 11} 248 q11 8 22 0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    return s


b = f'<rect x="0" y="340" width="936" height="10" rx="5" fill="{STEP}"/>'
xs = [96, 240, 384, 552, 696, 840]
cols = [BAND, STEP, BAND, ACC, STEP, BAND]
hairs = [INK, '#7A4A2B', INK2, INK, '#C9A25A', '#7A4A2B']
for x, c, h in zip(xs, cols, hairs):
    b += person(x, h, c)
# bulle "ce qu'on ne voit pas" au-dessus de la 4e personne
b += f'<circle cx="552" cy="188" r="8" fill="none" stroke="{INK}" stroke-width="4"/><circle cx="552" cy="164" r="12" fill="none" stroke="{INK}" stroke-width="4"/>'
b += f'<rect x="372" y="14" width="360" height="132" rx="40" fill="{CARD}" stroke="{INK}" stroke-width="5" stroke-dasharray="14 10"/>'
b += f'<g transform="translate(430 66)">{IC_BATTERY}</g><g transform="translate(552 66)">{IC_CLOUD}</g><g transform="translate(672 66)">{IC_BOLT}</g>'
b += f'<text x="552" y="130" font-size="28" font-weight="700" fill="{INK2}" text-anchor="middle">Ce qu\'on ne voit pas</text>'
svg(936, 360, b, 'mi-openspace.svg')


# ============ 2. La carte du corps ============
def sil(elems):
    """Silhouette en un seul contour : on dessine tout en encre, puis tout en vert clair par-dessus."""
    a = ''.join(e('ink') for e in elems)
    c = ''.join(e('fill') for e in elems)
    return a + c


def circ(cx, cy, r):
    return lambda m: f'<circle cx="{cx}" cy="{cy}" r="{r + (7 if m == "ink" else 0)}" fill="{INK if m == "ink" else STEP}"/>'


def seg(x1, y1, x2, y2, w):
    return lambda m: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK if m == "ink" else STEP}" stroke-width="{w + (14 if m == "ink" else 0)}" stroke-linecap="round"/>'


def blob(d):
    return lambda m: f'<path d="{d}" fill="{STEP}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>' if m == 'ink' else f'<path d="{d}" fill="{STEP}"/>'


body = sil([
    circ(468, 110, 62), seg(468, 160, 468, 205, 46),
    blob('M364 208 Q468 182 572 208 L588 480 Q468 512 348 480Z'),
    seg(350, 236, 304, 470, 52), seg(586, 236, 632, 470, 52),
    seg(418, 500, 408, 830, 76), seg(518, 500, 528, 830, 76),
])
# zones
head = bolt(468, 110, 1.5)
chest = f'<g transform="translate(468 316) scale(1.6)">{IC_BATTERY}</g>'
belly = f'<g transform="translate(468 432) scale(1.5)">{IC_DOTS}</g>'
joints = ''.join(f'<circle cx="{x}" cy="{y}" r="21" fill="{SUN}" stroke="{INK}" stroke-width="5"/>' for x, y in [(354, 234), (582, 234), (327, 356), (609, 356), (411, 650), (525, 650)])
g = f'<g transform="translate(93.6 0) scale(.8)">{body}{head}{chest}{belly}{joints}</g>'
g += link(520, 88, 610, 80) + link(530, 340, 610, 362) + link(416, 245, 306, 255) + link(426, 520, 306, 526)
g += card(610, 10, 320, 140, 'Tête &amp; nerfs', ['Migraine, épilepsie,', 'sclérose en plaques'], None, fill=CARD)
g += card(610, 292, 320, 140, 'Ventre &amp; bassin', ['Endométriose, Crohn,', 'RCH, SOPK'], None, fill=SUN)
g += card(6, 160, 300, 190, ['Énergie', '&amp; humeur'], ['Fatigue chronique,', 'diabète, anxiété,', 'dépression'], None, fill=CARD)
g += card(6, 430, 300, 190, ['Muscles &amp;', 'articulations'], ['Fibromyalgie, lupus,', 'polyarthrite'], None, fill=BAND)
svg(936, 730, g, 'mi-carte-corps.svg')


# ============ 3. Zone : tête & nerfs ============
b = f'<circle cx="468" cy="340" r="260" fill="{BAND}"/>'
b += f'<circle cx="468" cy="340" r="150" fill="{STEP}" stroke="{INK}" stroke-width="6"/>'
b += f'<path d="M280 640 Q280 520 468 500 Q656 520 656 640Z" fill="{STEP}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
b += f'<rect x="438" y="470" width="60" height="44" rx="14" fill="{STEP}" stroke="{INK}" stroke-width="6"/>'
# cerveau
for cx, cy, r in [(412, 262, 52), (472, 238, 58), (530, 268, 50), (470, 296, 48)]:
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CARD}" stroke="{INK}" stroke-width="5"/>'
b += ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r - 3}" fill="{CARD}"/>' for cx, cy, r in [(412, 262, 52), (472, 238, 58), (530, 268, 50), (470, 296, 48)])
b += f'<path d="M388 262 q20 -22 40 0 t40 0 t40 4 M418 304 q26 16 52 0 t52 -6" fill="none" stroke="{INK3}" stroke-width="5" stroke-linecap="round"/>'
b += bolt(486, 264, 1.5)
# visage neutre
b += f'<path d="M426 372 q14 10 28 0 M482 372 q14 10 28 0 M444 424 H494" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
# ondes de douleur
b += ''.join(f'<circle cx="610" cy="250" r="{r}" fill="none" stroke="{ACC}" stroke-width="6" opacity="{o}"/>' for r, o in [(30, 1), (60, .65), (90, .35)])
b += link(600, 290, 700, 300).replace('M600 290', 'M600 290')
b += card(6, 0, 440, 140, 'Migraine chronique', ['Une douleur, la lumière', 'et le bruit en trop'], IC_RINGS)
b += card(490, 0, 440, 140, 'Épilepsie', ['Une crise peut survenir', 'sans prévenir'], IC_WAVE)
b += card(468 - 230, 556, 460, 140, 'Sclérose en plaques', ['Fatigue, vue, équilibre :', 'des symptômes qui varient'], IC_NERVE)
b += link(390, 330, 300, 132) + link(570, 300, 700, 132)
svg(936, 700, b, 'mi-zone-tete.svg')


# ============ 4. Zone : ventre & bassin ============
BODY = 'M468 70 C590 70 646 140 626 240 C612 310 566 352 524 392 L518 440 C518 452 508 458 496 458 L440 458 C428 458 418 452 418 440 L412 392 C370 352 324 310 310 240 C290 140 346 70 468 70 Z'
CAVITY = 'M468 130 C536 130 556 178 544 232 C534 280 504 320 494 392 L442 392 C432 320 402 280 392 232 C380 178 400 130 468 130 Z'


def tube():
    s = f'<path d="M332 118 C270 86 208 98 174 150" fill="none" stroke="{INK}" stroke-width="24" stroke-linecap="round"/><path d="M332 118 C270 86 208 98 174 150" fill="none" stroke="{STEP}" stroke-width="13" stroke-linecap="round"/>'
    s += f'<ellipse cx="146" cy="226" rx="54" ry="40" transform="rotate(-18 146 226)" fill="{CARD}" stroke="{INK}" stroke-width="5"/>'
    return s


def dot(x, y, r=15):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SUN}" stroke="{INK}" stroke-width="4"/>'


b = f'<circle cx="468" cy="300" r="270" fill="{BAND}"/>'
b += f'<g transform="translate(0 170)"><path d="{BODY}" fill="{STEP}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><path d="{CAVITY}" fill="{SUN}" stroke="{EDGE}" stroke-width="4"/>{tube()}<g transform="translate(936 0) scale(-1 1)">{tube()}</g>'
b += dot(146, 226, 20) + dot(790, 232, 18) + dot(214, 118, 13) + dot(372, 410, 14) + dot(566, 410, 14) + '</g>'
b += card(6, 0, 440, 140, 'Endométriose', ['Du tissu s\'installe', 'hors de l\'utérus'], IC_DOTS)
b += card(490, 0, 440, 140, 'SOPK', ['Des cycles déréglés,', 'un équilibre hormonal'], IC_OVARY)
b += card(468 - 230, 570, 460, 140, 'Crohn et RCH', ['L\'intestin s\'enflamme', 'par poussées'], IC_GUT)
b += link(214, 288, 230, 140) + link(790, 402, 790, 140)
svg(936, 720, b, 'mi-zone-ventre.svg')


# ============ 5. Zone : muscles & articulations ============
def limb():
    s = f'<line x1="260" y1="330" x2="470" y2="470" stroke="{INK}" stroke-width="96" stroke-linecap="round"/><line x1="470" y1="470" x2="720" y2="320" stroke="{INK}" stroke-width="96" stroke-linecap="round"/>'
    s += f'<line x1="260" y1="330" x2="470" y2="470" stroke="{STEP}" stroke-width="84" stroke-linecap="round"/><line x1="470" y1="470" x2="720" y2="320" stroke="{BAND}" stroke-width="84" stroke-linecap="round"/>'
    # fibres musculaires
    s += f'<path d="M300 350 q40 -40 80 -4 t80 20 M310 392 q40 -40 80 -4 t60 30" fill="none" stroke="{INK3}" stroke-width="5" stroke-linecap="round"/>'
    return s


b = f'<circle cx="468" cy="380" r="280" fill="{BAND}" opacity=".6"/>' + limb()
b += ''.join(f'<path d="M470 470 l{dx} {dy}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' for dx, dy in [(0, 80), (-70, 60), (70, 60), (-92, 14), (92, 14)])
b += f'<circle cx="470" cy="470" r="52" fill="{SUN}" stroke="{INK}" stroke-width="6"/><circle cx="470" cy="470" r="22" fill="{CARD}" stroke="{INK}" stroke-width="4"/>'
b += dot(260, 330, 26) + dot(720, 320, 26)
b += card(6, 0, 440, 140, 'Fibromyalgie', ['Des douleurs diffuses,', 'un sommeil non réparateur'], IC_MUSCLE, ssize=25)
b += card(490, 0, 440, 140, 'Polyarthrite', ['Des articulations gonflées,', 'raides au réveil'], IC_JOINT, ssize=25)
b += card(468 - 230, 590, 460, 140, 'Lupus', ['Maladie auto-immune :', 'fatigue et poussées'], IC_BUTTERFLY, ssize=25)
b += link(300, 316, 220, 140) + link(690, 296, 720, 140)
svg(936, 730, b, 'mi-zone-muscles.svg')


# ============ 6. Zone : énergie & humeur ============
b = f'<circle cx="468" cy="360" r="270" fill="{BAND}"/>'
b += '<g transform="translate(70 70) scale(.85)">'
b += f'<rect x="338" y="140" width="260" height="420" rx="54" fill="{CARD}" stroke="{INK}" stroke-width="9"/><rect x="408" y="106" width="120" height="40" rx="12" fill="{INK}"/>'
for y in (176, 262, 348):
    b += f'<rect x="368" y="{y}" width="200" height="64" rx="22" fill="none" stroke="{INK3}" stroke-width="4" stroke-dasharray="10 10"/>'
b += f'<rect x="368" y="446" width="200" height="82" rx="26" fill="{SUN}" stroke="{INK}" stroke-width="5"/>'
b += bolt(468, 487, 1.0)
b += '</g>'
b += f'<g transform="translate(220 230) scale(2.6)">{IC_CLOUD}</g><g transform="translate(720 200) scale(2.4)">{IC_DROP}</g>'
b += card(6, 0, 440, 140, 'Fatigue chronique', ['Le repos ne répare pas', 'toujours l\'épuisement'], IC_BATTERY)
b += card(490, 0, 440, 140, 'Diabète', ['Une glycémie à surveiller', 'toute la journée'], IC_DROP)
b += card(468 - 230, 580, 460, 140, 'Anxiété, dépression', ['Un épuisement mental,', 'une concentration difficile'], IC_CLOUD, ssize=25)
svg(936, 730, b, 'mi-zone-energie.svg')


# ============ 7. Iceberg au bureau ============
b = f'<rect x="0" y="236" width="936" height="520" fill="{BAND}"/>'
b += f'<path d="M0 236 C120 222 200 250 320 236 S520 222 640 236 S840 250 936 232" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="16 12"/>'
b += f'<path d="M330 236 L396 120 L448 168 L520 70 L596 150 L650 118 L720 236Z" fill="{CARD}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
b += f'<path d="M210 236 H770 L840 330 L810 470 L860 590 L740 690 L600 736 L420 724 L270 670 L170 560 L204 440 L150 330Z" fill="{STEP}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
# personne au bureau sur la pointe
b += f'<rect x="456" y="140" width="120" height="14" rx="4" fill="{INK}"/><circle cx="516" cy="112" r="16" fill="{CARD}" stroke="{INK}" stroke-width="4"/><path d="M500 140 V126 Q516 116 532 126 V140Z" fill="{ACC}" stroke="{INK}" stroke-width="3"/>'
b += f'<path d="M508 114 q8 7 16 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
b += f'<text x="30" y="40" font-size="30" font-weight="800" fill="{INK}">On voit</text><text x="30" y="76" font-size="27" font-weight="600" fill="{INK2}">un sourire,</text><text x="30" y="108" font-size="27" font-weight="600" fill="{INK2}">un dossier rendu</text>'
b += f'<text x="24" y="288" font-size="28" font-weight="800" fill="{ACC}">Sous</text><text x="24" y="320" font-size="28" font-weight="800" fill="{ACC}">la ligne</text>'


def bub(x, y, ic, t1, t2):
    return f'<rect x="{x}" y="{y}" width="300" height="96" rx="48" fill="{CARD}" stroke="{INK}" stroke-width="4"/><g transform="translate({x + 50} {y + 48})">{ic}</g><text x="{x + 98}" y="{y + 44}" font-size="26" font-weight="800" fill="{INK}">{t1}</text><text x="{x + 98}" y="{y + 74}" font-size="22" font-weight="600" fill="{INK2}">{t2}</text>'


b += bub(200, 296, IC_BOLT, 'La douleur', 'en réunion')
b += bub(520, 330, IC_BATTERY, 'La fatigue', 'qui rattrape à 15 h')
b += bub(184, 424, IC_CAL, 'Les rendez-vous', 'médicaux à caser')
b += bub(520, 462, IC_EYE, 'La peur', 'd\'être jugée')
b += bub(214, 552, IC_MOON, 'Les heures', 'rattrapées le soir')
b += bub(520, 596, IC_BUBBLE, 'Les explications', 'à répéter à chacun')
svg(936, 740, b, 'mi-iceberg.svg')


# ============ 8. Quatre portes (ce qu'on peut demander) ============
def porte(x, y, ic, t1, subs):
    s = f'<path d="M{x} {y + 210} V{y + 74} a74 74 0 0 1 148 0 V{y + 210}Z" fill="{STEP}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    s += f'<path d="M{x + 22} {y + 210} V{y + 80} a52 52 0 0 1 104 0 V{y + 210}Z" fill="{SUN}" stroke="{EDGE}" stroke-width="4"/>'
    s += f'<circle cx="{x + 104}" cy="{y + 150}" r="9" fill="{INK}"/>'
    s += f'<g transform="translate({x + 74} {y + 90}) scale(1.25)">{ic}</g>'
    tx = x + 172
    s += f'<text x="{tx}" y="{y + 70}" font-size="33" font-weight="800" fill="{INK}">{t1}</text>'
    for i, t in enumerate(subs):
        s += f'<text x="{tx}" y="{y + 70 + 36 + i * 32}" font-size="26" font-weight="600" fill="{INK2}">{t}</text>'
    return s


b = f'<rect x="0" y="228" width="936" height="8" rx="4" fill="{STEP}"/><rect x="0" y="518" width="936" height="8" rx="4" fill="{STEP}"/>'
b += porte(6, 20, IC_BUBBLE, 'En parler', ['Pas obligée de', 'nommer la maladie :', 'le secret médical', 's\'applique'])
b += porte(480, 20, IC_CAL, 'Médecin du travail', ['Une visite peut être', 'demandée à tout', 'moment'])
b += porte(6, 310, IC_SLIDERS, 'Aménager', ['Horaires, pauses,', 'télétravail : selon', 'la situation'])
b += porte(480, 310, IC_KEY, 'La RQTH', ['Demandée à la MDPH,', 'jamais automatique :', 'vous choisissez de', 'la communiquer'])
svg(936, 540, b, 'mi-portes.svg')
print('ok')
