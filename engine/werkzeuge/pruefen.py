# Layoutprüfung: öffnet <projekt>/praesentation.html?check in einem Headless-Browser (Edge, Chrome oder Chromium),
# blendet auf jeder Folie alle Schritte ein und meldet Elemente, die über den Fußbereich oder den rechten Rand ragen.
# Aufruf: python engine/werkzeuge/pruefen.py <projekt>        Browser erzwingen: Umgebungsvariable QP_BROWSER=<pfad>
import os, re, sys, html, shutil, subprocess, pathlib, collections
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import konfig


def browser():
    if os.environ.get('QP_BROWSER') and os.path.exists(os.environ['QP_BROWSER']): return os.environ['QP_BROWSER']
    kand = []
    if sys.platform.startswith('win'):
        for basis in filter(None, [os.environ.get('PROGRAMFILES(X86)'), os.environ.get('PROGRAMFILES'), os.environ.get('LOCALAPPDATA')]):
            kand += [os.path.join(basis, r'Microsoft\Edge\Application\msedge.exe'), os.path.join(basis, r'Google\Chrome\Application\chrome.exe'),
                     os.path.join(basis, r'Chromium\Application\chrome.exe'), os.path.join(basis, r'BraveSoftware\Brave-Browser\Application\brave.exe')]
    elif sys.platform == 'darwin':
        for basis in ['/Applications', os.path.expanduser('~/Applications')]:
            kand += [f'{basis}/Google Chrome.app/Contents/MacOS/Google Chrome', f'{basis}/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
                     f'{basis}/Chromium.app/Contents/MacOS/Chromium', f'{basis}/Brave Browser.app/Contents/MacOS/Brave Browser']
    for p in kand:
        if os.path.exists(p): return p
    for n in ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'microsoft-edge', 'microsoft-edge-stable', 'msedge', 'chrome', 'brave-browser']:
        if shutil.which(n): return shutil.which(n)
    sys.exit('Kein Chromium-Browser (Edge/Chrome/Chromium) gefunden – QP_BROWSER=<pfad> setzen.')


def datei(K):
    return pathlib.Path(K['_projekt']) / K['ausgabe']


def main():
    K = konfig.lade()
    url = datei(K).as_uri() + '?check'
    dom = subprocess.run([browser(), '--headless=new', '--disable-gpu', '--no-first-run', '--window-size=1920,1080', '--virtual-time-budget=9000', '--dump-dom', url],
                         capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=180).stdout
    m = re.search(r'<pre id="checkout">(.*?)</pre>', dom, re.S)
    if not m: sys.exit('Keine Ausgabe – lädt die Seite? (build.py gelaufen?)')
    t = html.unescape(m.group(1)).strip()
    if t == 'OK': print('OK – kein Element ragt über den Rand.'); sys.exit(0)
    by = collections.OrderedDict()
    for l in [x for x in t.split('\n') if x.strip()]: by.setdefault(l.split(' ')[0], []).append(l)
    print('Folie  Anzahl  schlimmster Fall')
    for k, v in by.items():
        worst = max(v, key=lambda x: int(mm.group(1)) if (mm := re.search(r'bottom=(-?\d+)', x)) else 0)
        print(f'{k:>5}  {len(v):>6}  {worst[len(k)+1:][:150]}')
    sys.exit(1)


if __name__ == '__main__':
    main()
