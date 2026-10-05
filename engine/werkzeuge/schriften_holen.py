# Lädt die Schriften eines Stils einmalig als WOFF2 nach styles/<stil>/fonts/ und schreibt fonts/fonts.css
# mit lokalen @font-face-Regeln (url() relativ zu fonts.css). Danach lädt keine Seite Schriften von fremden Servern.
# Familienliste: styles/<stil>/stil.json -> {"schriften": ["Young Serif", "Instrument Sans:ital,wght@0,400..700;1,400..700", …]}
#   (Schreibweise wie im Google-Fonts-css2-Parameter „family=“; nur Schriften unter freier Lizenz, z. B. SIL OFL).
# Aufruf: python engine/werkzeuge/schriften_holen.py <stil> [<stile-ordner>]
import os, re, sys, json, urllib.request, urllib.parse

ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) < 2: sys.exit('Aufruf: python engine/werkzeuge/schriften_holen.py <stil> [<stile-ordner>]')
STILE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(ENGINE, '..', 'styles'))
STIL = os.path.join(STILE, sys.argv[1])
cfg = json.load(open(os.path.join(STIL, 'stil.json'), encoding='utf-8'))
fam = cfg.get('google_fonts') or (cfg.get('schriften') if isinstance(cfg.get('schriften'), list) else [])
if not fam: sys.exit('stil.json enthält keine „schriften“')
subsets = cfg.get('subsets', ['latin', 'latin-ext'])
FONTS = os.path.join(STIL, 'fonts'); os.makedirs(FONTS, exist_ok=True)
URL = 'https://fonts.googleapis.com/css2?' + '&'.join('family=' + urllib.parse.quote(f, safe=':,@;.') for f in fam) + '&display=swap'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
css = urllib.request.urlopen(urllib.request.Request(URL, headers=UA)).read().decode()
out = [f'/* Lokale Schriften des Stils „{sys.argv[1]}“ (freie Lizenzen, meist SIL OFL 1.1) – erzeugt von engine/werkzeuge/schriften_holen.py */']
for m in re.finditer(r'/\* ([\w-]+) \*/\s*@font-face\s*\{(.*?)\}', css, flags=re.S):
    subset, body = m.group(1), m.group(2)
    if subset not in subsets: continue
    name_f = re.search(r"font-family: '([^']+)'", body).group(1)
    style = re.search(r'font-style: (\w+)', body).group(1)
    url = re.search(r'url\((https://[^)]+\.woff2)\)', body).group(1)
    name = f"{name_f.replace(' ', '')}-{style}-{subset}.woff2"
    with open(os.path.join(FONTS, name), 'wb') as f:
        f.write(urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read())
    out.append('@font-face {' + body.replace(url, name).rstrip() + '\n}')
    print(name)
open(os.path.join(FONTS, 'fonts.css'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(out) - 1, '@font-face-Regeln ->', os.path.join(FONTS, 'fonts.css'))
