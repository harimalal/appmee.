"""
Construit cards.html : rendus fidèles des VRAIS fichiers de la Content Factory pour l'article OpenClaw
(atomes.md, positions.md, linkedin.md, x.md, sortie réelle de scripts/content-qa.mjs). Aucun texte n'est réécrit :
tout est lu dans les fichiers. Usage : python3 -I cards.py <sortie content-qa.txt>  puis  node cards.cjs
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '2026-10-23_combien-coute-openclaw-prix-reel-alternatives-2026')
rd = lambda f: open(os.path.join(SRC, f), encoding='utf-8').read()
E = html.escape

# --- atomes.md : lignes « - Ax · fait · statut · source »
atomes = []
for line in rd('atomes.md').splitlines():
    m = re.match(r'- (A\d+) · (.+)$', line)
    if m:
        parts = [p.strip() for p in m.group(2).split(' · ')]
        atomes.append({'id': m.group(1), 'fait': parts[0], 'statut': parts[1] if len(parts) > 1 else '', 'source': ' · '.join(parts[2:])})
KEEP = ['A1', 'A2', 'A6', 'A8', 'A12', 'A14']
fiche = [a for a in atomes if a['id'] in KEEP]

# --- positions.md : statut, thèse, verdicts
pos = rd('positions.md')
statut = re.search(r'Statut : (.+)', pos).group(1)
statut = re.sub(r'\*\*', '', statut).split('. Règle')[0]
these = re.search(r'## Thèse\n(.+)', pos).group(1).strip()
verd = re.findall(r'^\| (OpenClaw|Manus|Hermes Agent) \| \*\*(.+?)\*\*', pos, re.M)

# --- linkedin.md : LI-1
li = rd('linkedin.md')
li_post = re.search(r'### LI-1[^\n]*\n```post\n(.+?)\n```', li, re.S).group(1)
# --- x.md : X-FIL-1
xs = rd('x.md')
fil = re.search(r'### X-FIL-1[^\n]*\n(.+?)\n### ', xs, re.S).group(1)
x_posts = re.findall(r'```post\n(.+?)\n```', fil, re.S)

qa_out = open(sys.argv[1], encoding='utf-8').read().rstrip('\n').splitlines()

def para(txt):
    out = []
    for blk in txt.split('\n'):
        if not blk.strip():
            out.append('<div class="sp"></div>')
        else:
            cls = 'pr' + (' pp' if re.match(r'^(Pour qui|Les vrais red flags|La règle|La pépite|Le coupable)', blk) else '')
            out.append(f'<p class="{cls}">{E(blk)}</p>')
    return '\n'.join(out)

css = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#ECEAF6;font-family:'Inter','Helvetica Neue',Arial,sans-serif;color:#0F1020;padding:40px;display:flex;flex-direction:column;gap:60px;width:1100px}
.card{width:1000px;background:#fff;border-radius:28px;box-shadow:0 20px 50px rgba(20,20,60,.18);overflow:hidden}
.fh{display:flex;align-items:center;gap:14px;padding:26px 34px;background:#F4F2FC;border-bottom:2px solid #E4E1F3;font:700 26px/1 'JetBrains Mono',ui-monospace,monospace;color:#5A5B75}
.fh b{color:#0F1020}
.fb{padding:20px 34px 30px}
h3{font:900 44px/1.08 'Inter',sans-serif;letter-spacing:-.03em;margin:6px 0 18px}
.at{display:grid;grid-template-columns:96px 1fr;gap:18px;padding:18px 0;border-top:2px dashed #E4E1F3;align-items:start}
.at .id{height:56px;border-radius:14px;background:#0F1020;color:#FFD93B;font:900 28px/56px 'JetBrains Mono',monospace;text-align:center}
.at .f{font:700 31px/1.3 'Inter',sans-serif}
.at .m{margin-top:10px;display:flex;gap:10px;flex-wrap:wrap}
.chip{font:700 22px/1 'Inter',sans-serif;padding:9px 14px;border-radius:999px;background:#EAF8F1;color:#0E7A4F}
.chip.s{background:#EEF0FF;color:#4B45B8}
.stat{margin:6px 0 20px;padding:18px 22px;border-radius:18px;background:#FFF6DA;font:700 27px/1.35 'Inter',sans-serif;color:#6B4E00}
.th{font:800 36px/1.32 'Inter',sans-serif;letter-spacing:-.01em}
.vr{display:grid;grid-template-columns:230px 1fr;gap:16px;padding:16px 0;border-top:2px dashed #E4E1F3;font:700 29px/1.3 'Inter',sans-serif}
.vr b{font-weight:900}
.lk .hd{display:flex;align-items:center;gap:20px;padding:30px 34px 10px}
.av{width:84px;height:84px;border-radius:50%;background:linear-gradient(135deg,#6C5CE7,#E84393);color:#fff;font:900 34px/84px 'Inter';text-align:center}
.nm{font:900 32px/1.1 'Inter'} .nm small{display:block;font:600 24px/1.3 'Inter';color:#6A6B80;margin-top:4px}
.lk .bd{padding:14px 34px 34px}
.pr{font:500 29px/1.42 'Inter';color:#1B1C2E}
.pr.pp{font-weight:800;color:#0F1020}
.sp{height:22px}
.tag{display:inline-block;margin-top:18px;font:800 22px/1 'Inter';letter-spacing:.06em;text-transform:uppercase;color:#6A6B80;background:#F1EFFD;padding:10px 14px;border-radius:10px}
.xp{display:grid;grid-template-columns:84px 1fr;gap:20px;padding:28px 34px;border-top:2px solid #EEEDF5}
.xp:first-of-type{border-top:0}
.xp .t{font:500 30px/1.42 'Inter';color:#111}
.xp .who{font:900 28px/1 'Inter';margin-bottom:10px} .xp .who span{font-weight:600;color:#6A6B80}
.term{background:#12132A;color:#E9E8FF;font:600 27px/1.55 'JetBrains Mono',ui-monospace,monospace}
.term .fh{background:#1C1E3D;border-bottom:0;color:rgba(255,255,255,.75)}
.term .fb{padding:26px 34px 34px}
.ln{white-space:pre-wrap;word-break:break-word}
.ln.cmd{color:#FFD93B}
.ln.ok{color:#3DDC97;font-weight:800;font-size:31px;margin-top:8px}
.ln.f{color:#9FA3FF;font-weight:800}
"""

parts = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css}</style></head><body>']
# fiche
parts.append('<div class="card" id="fiche"><div class="fh">CONTENT/…/<b>atomes.md</b></div><div class="fb"><h3>Fiche d\'atomes</h3>')
for a in fiche:
    chips = f'<span class="chip">{E(a["statut"])}</span>' + (f'<span class="chip s">{E(a["source"])}</span>' if a['source'] else '')
    parts.append(f'<div class="at" id="at-{a["id"]}"><div class="id">{a["id"]}</div><div><div class="f">{E(a["fait"])}</div><div class="m">{chips}</div></div></div>')
parts.append('</div></div>')
# position
parts.append(f'<div class="card" id="position"><div class="fh">CONTENT/…/<b>positions.md</b></div><div class="fb"><h3>Fiche de position</h3><div class="stat" id="pos-statut">{E(statut)}</div><div class="th" id="pos-these">{E(these)}</div><div style="height:18px"></div>')
for o, v in verd:
    parts.append(f'<div class="vr"><b>{E(o)}</b><span>{E(v)}</span></div>')
parts.append('</div></div>')
# linkedin
parts.append(f'<div class="card lk" id="linkedin"><div class="fh">CONTENT/…/<b>linkedin.md</b> · LI-1</div><div class="hd"><div class="av">R</div><div class="nm">Reflex IA<small>Post LinkedIn · position</small></div></div><div class="bd">{para(li_post)}</div></div>')
# x
parts.append('<div class="card" id="x"><div class="fh">CONTENT/…/<b>x.md</b> · X-FIL-1 · fil de ' + str(len(x_posts)) + '</div>')
for i, p in enumerate(x_posts):
    parts.append(f'<div class="xp" id="xp-{i + 1}"><div class="av">R</div><div><div class="who">Reflex IA <span>· fil</span></div><div class="t">{E(p)}</div></div></div>')
parts.append('</div>')
# terminal
parts.append('<div class="card term" id="term"><div class="fh">Terminal</div><div class="fb">')
parts.append('<div class="ln cmd" id="tl-0">$ node scripts/content-qa.mjs CONTENT/2026-10-23_combien-coute-openclaw-prix-reel-alternatives-2026</div>')
k = 1
for line in qa_out:
    if not line.strip():
        continue
    cls = 'ok' if line.startswith('✓') else ('f' if not line.startswith(' ') else '')
    parts.append(f'<div class="ln {cls}" id="tl-{k}">{E(line)}</div>'); k += 1
parts.append('</div></div>')
parts.append('</body></html>')
open(os.path.join(HERE, 'cards.html'), 'w', encoding='utf-8').write('\n'.join(parts))
json.dump({'fiche': [a['id'] for a in fiche], 'x_posts': len(x_posts), 'term_lines': k, 'verdicts': verd, 'these': these}, open(os.path.join(HERE, 'cards-src.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('fiche', [a['id'] for a in fiche], '| x', len(x_posts), '| term', k, '| verdicts', len(verd))
