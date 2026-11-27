"""
Voix off du reel « histoire » : une phrase = un segment, généré avec la voix Google (Gemini TTS) puis VÉRIFIÉ sans écoute :
transcription inverse par Gemini + durée mesurée. La voix pilote ensuite le montage (plan.py).

Usage :  python3 -I tts.py <dossier_de_travail>
  - audios bruts mis en cache dans audio/voice-raw/ (un appel facturé par phrase, jamais refait si le texte n'a pas changé)
  - sortie : <dossier_de_travail>/trim/<id>.wav (silences de début/fin retirés) et audio/voice-report.json
Clé : variable d'environnement GOOGLE_API_KEY (jamais écrite ni affichée). Seul le texte des phrases est envoyé à l'API.
"""
import base64, difflib, hashlib, json, os, re, subprocess, sys, time, unicodedata, wave

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'story.json'), encoding='utf-8'))
RAW = os.path.join(HERE, 'audio', 'voice-raw')
WORK = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else '/tmp/reel-audio'
KEY = os.environ.get('GOOGLE_API_KEY')
if not KEY:
    sys.exit('GOOGLE_API_KEY absente')
for d in (RAW, os.path.join(WORK, 'trim'), os.path.join(WORK, 'tmp')):
    os.makedirs(d, exist_ok=True)
BASE = 'https://generativelanguage.googleapis.com/v1beta/models/'


LAST_TTS = [0.0]


def call(model, body, name):
    """Un appel ; limite du modèle vocal : 10 requêtes/minute (niveau 1) -> 7 s mini entre deux synthèses, reprise après un 429."""
    req = os.path.join(WORK, 'tmp', name + '.req.json'); out = os.path.join(WORK, 'tmp', name + '.resp.json')
    json.dump(body, open(req, 'w', encoding='utf-8'))
    for attempt in range(5):
        if model == CFG['model']:
            wait = 7.0 - (time.time() - LAST_TTS[0])
            if wait > 0: time.sleep(wait)
            LAST_TTS[0] = time.time()
        subprocess.run(['curl', '-sS', '--max-time', '120', '-X', 'POST', '-H', 'x-goog-api-key: ' + KEY, '-H', 'Content-Type: application/json',
                        '--data', '@' + req, BASE + model + ':generateContent', '-o', out], check=True, capture_output=True)
        d = json.load(open(out, encoding='utf-8'))
        if d.get('error', {}).get('code') == 429 and attempt < 4:
            time.sleep(20 * (attempt + 1)); continue   # un appel refusé n'est pas facturé
        break
    if 'error' in d:
        sys.exit('API : ' + json.dumps(d['error'], ensure_ascii=False)[:300])
    return d


def wav_dur(p):
    w = wave.open(p); return w.getnframes() / w.getframerate()


def norm(s):
    s = unicodedata.normalize('NFKC', s).lower(); s = re.sub(r"[^\w\s']", ' ', s); return re.sub(r'\s+', ' ', s).strip()


def digest(text):  # le cache est lié au texte ET à la voix
    return hashlib.sha1((CFG['model'] + '|' + CFG['voice'] + '|' + text).encode('utf-8')).hexdigest()[:10]


rows, spent = [], 0
for sc in CFG['scenes']:
    for s in sc['sentences']:
        raw = os.path.join(RAW, f"{s['id']}-{digest(s['voice'])}.wav")
        if not os.path.exists(raw):
            body = {'contents': [{'parts': [{'text': s['voice']}]}], 'generationConfig': {'responseModalities': ['AUDIO'],
                    'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': CFG['voice']}}}}}
            d = call(CFG['model'], body, 'tts-' + s['id'])
            open(raw, 'wb').write(base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])); spent += 1
        tr = os.path.join(WORK, 'trim', s['id'] + '.wav')
        af = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse'
        if s.get('tempo') or CFG.get('tempo'): af += ',atempo=%s' % (s.get('tempo') or CFG.get('tempo'))   # ralentissement ponctuel d'une phrase lue trop vite par la synthèse
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af', af, '-ar', '24000', '-ac', '1', tr], check=True)
        prompt = ("Transcris exactement, en français, ce qui est dit dans cet audio. Écris tous les nombres en toutes lettres "
                  "(par exemple « vingt-trois »). Les noms propres anglais (Claude in Chrome, YouTube, SaaS) s'écrivent tels quels. Réponds uniquement par la transcription.")
        body = {'contents': [{'parts': [{'text': prompt}, {'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(open(tr, 'rb').read()).decode()}}]}]}
        heard = call(CFG['asr_model'], body, 'asr-' + s['id'])['candidates'][0]['content']['parts'][0]['text'].strip()
        sim = difflib.SequenceMatcher(None, norm(s['voice']), norm(heard)).ratio()
        rows.append({'id': s['id'], 'scene': sc['id'], 'attendu': s['voice'], 'entendu': heard, 'similarite': round(sim, 2), 'parole_s': round(wav_dur(tr), 2), 'ok_texte': sim >= 0.85})

json.dump(rows, open(os.path.join(HERE, 'audio', 'voice-report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('phrases générées cette fois (appels facturés) :', spent, '/', len(rows), '· durée de parole cumulée : %.1f s' % sum(r['parole_s'] for r in rows))
for r in rows:
    print('%-3s %.2f %5.2f s  %s%s' % (r['id'], r['similarite'], r['parole_s'], r['entendu'], '' if r['ok_texte'] else '   [TEXTE DIFFÉRENT]'))
