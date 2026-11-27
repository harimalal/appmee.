"""
Mixage du son du reel « histoire » : voix Google (une phrase = un segment, déjà générée et vérifiée par tts.py) posée à l'instant
de chaque phrase de la timeline (aucun changement de vitesse), plus bruitages et nappe (synth.cjs) ;
  - chaque segment est ramené à un niveau moyen commun ; la nappe et les bruitages baissent sous la voix (sidechain) ;
  - normalisation EBU R128 à -14 LUFS, crête vraie <= -1,5 dBTP (deux passes) ;
  - la vidéo n'est PAS ré-encodée (copie) : seul le son est ajouté.
Usage : python3 -I mix.py <dossier_de_travail> <video_muette.mp4> <sortie.mp4> [--sans-nappe | --nappe 0.5]
Le dossier de travail contient trim/<id>.wav (voix) et sfx.wav / bed.wav (synth.cjs).
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAPPE = 1.0   # niveau de la nappe : --sans-nappe (0) ou --nappe 0.5
if '--sans-nappe' in sys.argv: NAPPE = 0.0; sys.argv.remove('--sans-nappe')
if '--nappe' in sys.argv: i = sys.argv.index('--nappe'); NAPPE = float(sys.argv[i + 1]); del sys.argv[i:i + 2]
WORK, VIDEO, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
TL = json.load(open(os.path.join(HERE, 'timeline.json'), encoding='utf-8'))
SEGS = [s for sc in TL['scenes'] for s in sc['sent']]
TOTAL = float(TL['total'])
TARGET_MEAN_DB = -21.0
os.makedirs(os.path.join(WORK, 'seg'), exist_ok=True)


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def mean_volume(path):
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'volumedetect', '-f', 'null', '-'])
    return float(re.search(r'mean_volume:\s*(-?[\d.]+) dB', r.stderr).group(1))


inputs, filters, labels = [], [], []
for i, s in enumerate(SEGS):
    src, tmp = os.path.join(WORK, 'trim', s['id'] + '.wav'), os.path.join(WORK, 'seg', s['id'] + '.wav')
    r = run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-af', 'aresample=48000', '-ac', '1', tmp])
    if r.returncode: sys.exit(r.stderr)
    gain = TARGET_MEAN_DB - mean_volume(tmp)
    ms = int(round(s['start'] * 1000))
    inputs += ['-i', tmp]
    filters.append(f'[{i}:a]volume={gain:.2f}dB,adelay={ms}|{ms}[s{i}]')
    labels.append(f'[s{i}]')
n = len(SEGS)
filters.append(''.join(labels) + f'amix=inputs={n}:normalize=0:duration=longest,apad=whole_dur={TOTAL},atrim=0:{TOTAL},asetpts=N/SR/TB[voice]')
voice_wav = os.path.join(WORK, 'voice-histoire.wav')
r = run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(filters), '-map', '[voice]', '-ar', '48000', '-ac', '1', voice_wav])
if r.returncode: sys.exit(r.stderr)

sfx, bed = os.path.join(WORK, 'sfx.wav'), os.path.join(WORK, 'bed.wav')
mix = (
    '[0:a]pan=stereo|c0=c0|c1=c0,volume=1.0[v];'
    '[v]asplit=3[vm][vk1][vk2];'
    f'[2:a]volume={0.62 * NAPPE:.3f}[b];[b][vk1]sidechaincompress=threshold=0.015:ratio=9:attack=15:release=350:makeup=1[bd];'
    '[1:a]volume=0.5[x];[x][vk2]sidechaincompress=threshold=0.03:ratio=3:attack=10:release=200:makeup=1[xd];'
    '[vm][bd][xd]amix=inputs=3:normalize=0:duration=first[m]'
)
ln = 'loudnorm=I=-14:TP=-1.5:LRA=11'
common = ['-i', voice_wav, '-i', sfx, '-i', bed]
p1 = run(['ffmpeg', '-hide_banner', '-nostats', *common, '-filter_complex', mix + f';[m]{ln}:print_format=json[o]', '-map', '[o]', '-f', 'null', '-'])
js = json.loads(p1.stderr[p1.stderr.rindex('{'):p1.stderr.rindex('}') + 1])
ln2 = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
       f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
final_wav = os.path.join(WORK, 'mix-histoire.wav')
r = run(['ffmpeg', '-y', '-loglevel', 'error', *common, '-filter_complex', mix + f';[m]{ln2},aresample=48000[o]', '-map', '[o]', '-ac', '2', final_wav])
if r.returncode: sys.exit(r.stderr)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
r = run(['ffmpeg', '-y', '-loglevel', 'error', '-i', VIDEO, '-i', final_wav, '-map', '0:v:0', '-map', '1:a:0',
         '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(TOTAL), '-movflags', '+faststart', OUT])
if r.returncode: sys.exit(r.stderr)
print(f'{OUT} ({os.path.getsize(OUT) / 1048576:.1f} Mo) · voix : {n} segments · mesure avant normalisation : {js["input_i"]} LUFS')
