# Screenshots einzelner Folien/Schritte (1920×1080) plus Kontaktbogen zum schnellen Ansehen.
# Aufruf: python engine/werkzeuge/screenshot.py <projekt> 3 3.2 5.4   -> <projekt>/screens/s_3.png, … und screens/bogen.png
# Adresse „5.4“ = Folie 5, Schritt 4 (die Engine liest #folie.schritt aus der URL). Ohne Angabe: Folie 1.
import os, sys, subprocess, pathlib, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import konfig
from pruefen import browser, datei

args = sys.argv[1:]
projekt = args.pop(0) if args and not args[0].replace('.', '').isdigit() else None
K = konfig.lade(projekt and os.path.abspath(projekt))
DATEI = datei(K)
OUT = pathlib.Path(K['_projekt']) / 'screens'; OUT.mkdir(exist_ok=True)
ziele = args or ['1']
B = browser()


def shot(z):
    png = OUT / f's_{z}.png'
    if png.exists(): png.unlink()
    prof = tempfile.mkdtemp(prefix='qp_')   # eigenes Profil je Aufnahme, damit parallele Browser sich nicht stören
    try:
        subprocess.run([B, '--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars', f'--user-data-dir={prof}', '--window-size=1920,1080',
                        '--virtual-time-budget=7000', f'--screenshot={png}', DATEI.as_uri() + '#' + z], capture_output=True, timeout=120)
    finally:
        shutil.rmtree(prof, ignore_errors=True)
    if not png.exists(): print('keine Aufnahme:', z)
    return png


with ThreadPoolExecutor(4) as ex: pngs = list(ex.map(shot, ziele))
try:
    from PIL import Image
    ims = [Image.open(p).convert('RGB').resize((960, 540)) for p in pngs if p.exists()]
    cols = 2; rows = max(1, (len(ims) + 1) // 2)
    bogen = Image.new('RGB', (960 * cols, 540 * rows), 'white')
    for i, im in enumerate(ims): bogen.paste(im, ((i % cols) * 960, (i // cols) * 540))
    bogen.save(OUT / 'bogen.png'); print('->', OUT / 'bogen.png')
except ImportError:
    print('PIL fehlt – Einzelbilder liegen in', OUT)
