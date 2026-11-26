"""
Plan de montage piloté par la voix : à partir de story.json et des durées mesurées (audio/voice-report.json),
calcule l'instant de début/fin de chaque scène, de chaque phrase et (approximativement) de chaque mot de la légende.
Sorties : timeline.json (outils) et timeline.js (chargé par story.html).
Usage : python3 -I plan.py
Les instants de mots sont PROPORTIONNELS à la longueur des mots (aucun horodatage de mot n'est fourni par la synthèse) : approximation.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'story.json'), encoding='utf-8'))
dur = {r['id']: r['parole_s'] for r in json.load(open(os.path.join(HERE, 'audio', 'voice-report.json'), encoding='utf-8'))}

cursor, scenes = 0.0, []
for sc in S['scenes']:
    start = cursor
    t = start + S['lead']
    sents = []
    for k, s in enumerate(sc['sentences']):
        d = dur[s['id']]
        words = s['cap'].split()
        wts = [len(w) + (3 if re.search(r'[,;:.!?]$', w) else 0) for w in words]
        tot = float(sum(wts)); a, b = t + .05, t + d - .02
        acc, ws = 0.0, []
        for w, wt in zip(words, wts):
            ws.append({'w': w, 't0': round(a + (b - a) * acc / tot, 3), 't1': round(a + (b - a) * (acc + wt) / tot, 3)})
            acc += wt
        sents.append({'id': s['id'], 'voice': s['voice'], 'cap': s['cap'], 'start': round(t, 3), 'end': round(t + d, 3), 'words': ws})
        t = t + d + (S['gap_sentence'] if k < len(sc['sentences']) - 1 else 0)
    end = max(t + S['tail'], start + sc.get('min', 0))   # min = durée mini d'une scène dont l'animation est plus longue que la phrase
    scenes.append({'id': sc['id'], 'bg': sc['bg'], 'caption': sc['caption'], 'start': round(start, 3), 'end': round(end, 3), 'sent': sents})
    cursor = end

TL = {'total': round(cursor + 0.0, 2), 'scenes': scenes}
json.dump(TL, open(os.path.join(HERE, 'timeline.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(HERE, 'timeline.js'), 'w', encoding='utf-8').write('window.TIMELINE=' + json.dumps(TL, ensure_ascii=False) + ';\n')
print('durée totale : %.1f s (%d scènes, %d phrases)' % (TL['total'], len(scenes), sum(len(s['sent']) for s in scenes)))
for s in scenes:
    print('  %-12s %5.1f → %5.1f  (%4.1f s)  phrases : %s' % (s['id'], s['start'], s['end'], s['end'] - s['start'], ' '.join('%s@%.1f' % (x['id'], x['start']) for x in s['sent'])))
