# Baut alles neu, kopiert NUR freigegebene Dateien in den Veröffentlichungsordner (quality_point.json „ziel“)
# und prüft das Paket auf heikle Inhalte und tote Links. Treffer = Abbruch mit Fehlercode 1.
# Aufruf:  python engine/deploy.py <projektordner> [--ohne-bau]
import os, re, sys, glob, shutil, zipfile, subprocess, json, hashlib, secrets, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import konfig

K = konfig.lade()
ENG, PRJ = K['_engine'], K['_projekt']
os.chdir(PRJ)
ZIEL = K['_ziel']
SEITEN = konfig.seiten(K)                                       # Positivliste der Seiten
MAUS = K['materialien'].get('ausgabe', 'formulare')

# Sperrliste: Schlüssel, Zugangsdaten, absolute Pfade, private Mail-Domains, fremde Server (nur lokale Schriften/Skripte)
SPERRE = [r'(?<![A-Za-z])sk-[A-Za-z0-9_-]{20,}', r'sk-proj', r'sk-ant-', r'\bAPI[ _-]?Key\b', r'\bapi_key\b', r'FAL_KEY', r'\bsecret[_-]?key\b',
          r'Bearer [A-Za-z0-9._-]{20,}', r'AKIA[0-9A-Z]{16}', r'ghp_[A-Za-z0-9]{30,}',
          r'(?<![\w/])[A-Za-z]:[\\/](?:Users|Program|Windows|[^\\/\s"\'<>]{2,}[\\/])', r'file:///', r'/Users/[A-Za-z]', r'/home/[a-z]',
          r'@gmail\.com', r'@gmx\.', r'@web\.de', r'@yahoo\.', r'@hotmail\.', r'@outlook\.', r'@icloud\.com', r'@aon\.at',
          r'GoogleDrive', r'OneDrive', r'Dropbox', r'scratchpad',
          r'fonts\.googleapis', r'fonts\.gstatic', r'cdn\.jsdelivr', r'unpkg\.com', r'cdnjs\.', r'ajax\.googleapis'] + list(K['sperrliste_zusatz'])


def immer():
    """Schriften und Zusatzdateien – erst nach dem Bau ermitteln (der Bau legt fonts/ beim ersten Mal überhaupt erst an)."""
    liste = ['fonts/' + f for f in os.listdir('fonts')] if os.path.isdir('fonts') else []
    for z in K['seiten_zusatz']:                                # weitere Dateien/Ordner aus quality_point.json
        liste += [os.path.relpath(f, PRJ).replace('\\', '/') for f in glob.glob(z, recursive=True) if os.path.isfile(f)] or [z]
    return liste


def pbkdf2(pw):
    """Passwort-Hash im Format, das live/api.php prüft (pbkdf2$sha256$runden$salz$hash)."""
    salz, runden = secrets.token_hex(16), 200000
    return 'pbkdf2$sha256$%d$%s$%s' % (runden, salz, hashlib.pbkdf2_hmac('sha256', pw.encode('utf-8'), bytes.fromhex(salz), runden, 32).hex())


def live_einrichten():
    """Server-Modus: live/api.php + Datenordner ins Paket; Referenten-Passwort aus QP_LIVE_PASSWORT, sonst aus der Konfiguration,
    sonst einmal erzeugen (wird angezeigt). Ein vorhandener Datenordner bleibt erhalten (laufende Sitzung)."""
    L = K['live']; lz = os.path.join(ZIEL, 'live'); dz = os.path.join(lz, 'daten'); os.makedirs(dz, exist_ok=True)
    shutil.copy2(os.path.join(ENG, 'live', 'api.php'), os.path.join(lz, 'api.php'))
    open(os.path.join(dz, '.htaccess'), 'w', encoding='utf-8').write('Require all denied\n')
    open(os.path.join(dz, 'index.html'), 'w', encoding='utf-8').write('')
    zugang = os.path.join(dz, 'zugang.json')
    pw = os.environ.get('QP_LIVE_PASSWORT') or str(L.get('passwort') or '')
    if pw or not os.path.exists(zugang):
        neu = not pw
        if neu: pw = secrets.choice(['ampel', 'tafel', 'kreide', 'folie', 'pult', 'beamer', 'pause', 'wolke']) + '-' + str(secrets.randbelow(9000) + 1000)
        json.dump({'hash': pbkdf2(pw), 'erstellt': int(time.time())}, open(zugang, 'w', encoding='utf-8'))
        print('Live: Referenten-Passwort ' + ('(neu erzeugt, bitte notieren) ' if neu else '(aus Konfiguration/Umgebung) ') + pw + ' – ändern im Live-Panel (Taste A → Einstellungen)')
    else:
        print('Live: vorhandenes Passwort bleibt (live/daten/zugang.json); neues per QP_LIVE_PASSWORT')
    einst = os.path.join(dz, 'einstellungen.json')
    if not os.path.exists(einst):
        json.dump({'folgen': bool(L.get('folgen', True)), 'notizen': bool(L.get('notizen', True)), 'fertig': bool(L.get('fertig', True)),
                   'barometer': list(L.get('barometer', [])), 'ergebnisse': L.get('ergebnisse', 'freigabe'), 'freigaben': {}, 'version': 1, 'start': int(time.time())},
                  open(einst, 'w', encoding='utf-8'), ensure_ascii=False)
    print('Live: Server-Teil in', os.path.relpath(lz, ZIEL) + '/ (PHP 8, Schreibrecht auf live/daten/ – siehe docs/LIVE.md)')


def herkunft(pfad):
    """Quelldatei zu einem Verweis: im Projekt, sonst (Abbildungen figures/…) im claude-research-Ordner des Artikels."""
    if os.path.exists(pfad): return pfad
    if pfad.startswith('figures/') and K['_artikel']:
        alt = os.path.join(K['_artikel'], pfad)
        if os.path.exists(alt): return alt
    return ''


def main():
    ns = K.get('notizschutz') or {}             # vor allem anderen prüfen: nie ein ungeschütztes Paket in den Zielordner legen
    if ns and not (os.environ.get('QP_NOTIZ_PIN') or ns.get('pin')):
        sys.exit('Notizschutz eingeschaltet, aber keine PIN (Umgebungsvariable QP_NOTIZ_PIN) – Abbruch, Zielordner unverändert')
    if ns:
        try: import cryptography  # noqa: F401
        except ImportError: sys.exit('Notizschutz braucht das Paket „cryptography“ (pip install cryptography) – Abbruch, Zielordner unverändert')
    if '--ohne-bau' not in sys.argv:
        py = sys.executable
        if K['materialien'].get('an'):
            subprocess.run([py, os.path.join(ENG, 'werkzeuge', 'materialien_bauen.py'), PRJ], check=True)
            subprocess.run([py, os.path.join(ENG, 'werkzeuge', 'unterricht_folien.py'), PRJ], check=True)
        subprocess.run([py, os.path.join(ENG, 'build.py'), PRJ], check=True)
        subprocess.run([py, os.path.join(ENG, 'werkzeuge', 'seiten_bauen.py'), PRJ], check=True)
    if os.path.abspath(ZIEL) in (os.path.abspath(PRJ), os.path.abspath(ENG)) or os.path.abspath(PRJ).startswith(os.path.abspath(ZIEL) + os.sep):
        sys.exit(f'Ziel {ZIEL} darf nicht Projekt- oder Engine-Ordner (oder deren Elternordner) sein')
    os.makedirs(ZIEL, exist_ok=True)
    daten_live = os.path.join(ZIEL, 'live', 'daten')     # gesammelte Live-Daten (Antworten, Hinweise, Passwort) überleben den Neubau
    for dp, ds, fs in os.walk(ZIEL, topdown=False):     # leeren (leere Ordner dürfen bleiben – Cloud-Sync sperrt sie manchmal)
        if os.path.abspath(dp).startswith(os.path.abspath(daten_live)): continue
        for f in fs: os.remove(os.path.join(dp, f))
        for d in ds:
            try: os.rmdir(os.path.join(dp, d))
            except OSError: pass
    dateien = set(immer())
    for s in SEITEN:
        if not os.path.exists(s): print('FEHLT (Seite):', s); continue
        shutil.copy2(s, os.path.join(ZIEL, s))
        txt = open(s, encoding='utf-8').read()
        dateien |= set(re.findall(r'(?:src|href|data-img|data-a|data-b)="((?:img|' + re.escape(MAUS) + r'|media|fonts|figures)/[^"#?]+)"', txt))
    for a in sorted(dateien):
        q = herkunft(a)
        if not q: print('FEHLT:', a); continue
        os.makedirs(os.path.dirname(os.path.join(ZIEL, a)) or ZIEL, exist_ok=True); shutil.copy2(q, os.path.join(ZIEL, a))
    if K['live'].get('an'): live_einrichten()
    ns = K.get('notizschutz') or {}
    if ns:                                                       # Sprechernotizen im Paket nur mit PIN
        sys.path.insert(0, os.path.join(ENG, 'werkzeuge')); import notizschutz
        if notizschutz.aktiv(ns): notizschutz.schuetzen(os.path.join(ZIEL, K['ausgabe']), notizschutz.pin_aus(ns))
        else: print(f'Notizschutz: Stichtag {ns.get("bis")} erreicht – Notizen bleiben offen')

    treffer = []
    for dp, _, fs in os.walk(ZIEL):
        for f in fs:
            p = os.path.join(dp, f); texte = []
            if f.endswith(('.html', '.css', '.js', '.json', '.txt', '.md', '.svg')): texte.append(open(p, encoding='utf-8', errors='ignore').read())
            elif f.endswith(('.docx', '.xlsx', '.pptx')):
                with zipfile.ZipFile(p) as z: texte += [z.read(n).decode('utf-8', 'ignore') for n in z.namelist() if n.endswith('.xml')]
            for t in texte:
                for b in SPERRE:
                    for m in re.finditer(b, t, flags=re.I if b.startswith('\\bapi') or 'secret' in b else 0):
                        treffer.append(f'{os.path.relpath(p, ZIEL)}: „{b}“ … {t[max(0, m.start()-40):m.end()+40]!r}')
    # Linkprüfung: jeder relative Verweis (href/src/data-img, auch in Skript-Vorlagen und CSS url()) muss im Paket existieren
    for f in SEITEN:
        q = os.path.join(ZIEL, f)
        if not os.path.exists(q): continue
        t = re.sub(r'/\*.*?\*/|<!--.*?-->', '', open(q, encoding='utf-8').read(), flags=re.S)   # Beispiele in Kommentaren ignorieren
        for m in re.finditer(r'(?:href|src|data-img|data-a|data-b)=["\']([^"\'#?]+?\.(?:html|webp|png|jpe?g|gif|svg|css|js|docx|pdf|mp4|woff2))(?:[#?][^"\']*)?["\']|url\(["\']?([^)"\'#?]+?\.(?:woff2?|webp|png|jpe?g|svg))', t):
            ziel = m.group(1) or m.group(2)
            if re.match(r'[a-z]+:|//|/', ziel) or '${' in ziel or ziel.startswith('video_lokal/'): continue
            if not os.path.exists(os.path.join(ZIEL, ziel)): treffer.append(f'{f}: toter Verweis auf {ziel}')
    if treffer:
        print('\n!!! SICHERHEITSPRÜFUNG FEHLGESCHLAGEN – NICHT VERÖFFENTLICHEN !!!')
        for h in treffer[:40]: print('  ', h)
        sys.exit(1)
    print(f'{ZIEL}: {sum(len(f) for _, _, f in os.walk(ZIEL))} Dateien, Sicherheitsprüfung bestanden.')


if __name__ == '__main__':
    main()
