"""Lädt die Schriften aller Schriftsets einmalig als WOFF2 (Teilmengen latin + latin-ext)
und schreibt lokale @font-face-Regeln. Danach lädt keine Seite mehr Schriften von fremden Servern.

  styles/_schriftsets/<set>.json   Quelle (Feld google_fonts_api)
  styles/_schriftsets/fonts/       alle WOFF2 + <set>.css je Set
  styles/<stil>/fonts/             Kopie des Standard-Sets eines Stils + fonts.css

Aufruf:  python styles/_werkzeuge/schriften_holen.py [set-id ...]
Alle Familien stehen unter der SIL Open Font License 1.1 (geprüft mit --lizenz).
"""
import json, re, shutil, sys, urllib.request
from pathlib import Path

STYLES = Path(__file__).resolve().parent.parent
SETS = STYLES / "_schriftsets"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def hole(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def set_laden(sid):
    cfg = json.loads((SETS / f"{sid}.json").read_text(encoding="utf-8"))
    css = hole(cfg["google_fonts_api"]).decode()
    ziel = SETS / "fonts"
    ziel.mkdir(exist_ok=True)
    regeln, dateien = [f"/* Schriftset „{cfg['name']}“ – lokal, SIL Open Font License 1.1 – "
                       f"erzeugt von _werkzeuge/schriften_holen.py */"], []
    for m in re.finditer(r"/\* ([\w-]+) \*/\s*@font-face\s*\{(.*?)\}", css, flags=re.S):
        subset, body = m.group(1), m.group(2)
        if subset not in ("latin", "latin-ext"):
            continue
        fam = re.search(r"font-family: '([^']+)'", body).group(1)
        style = re.search(r"font-style: (\w+)", body).group(1)
        wght = re.search(r"font-weight: ([\d ]+);", body).group(1).strip().replace(" ", "-")
        url = re.search(r"url\((https://[^)]+\.woff2)\)", body).group(1)
        name = f"{fam.replace(' ', '')}-{style}-{wght}-{subset}.woff2"
        if not (ziel / name).exists():
            (ziel / name).write_bytes(hole(url))
        dateien.append(name)
        regeln.append("@font-face {" + body.replace(url, name).rstrip() + "\n}")
    (ziel / f"{sid}.css").write_text("\n".join(regeln) + "\n", encoding="utf-8")
    # Standard-Set des Stils in dessen fonts/-Ordner spiegeln
    stil = STYLES / cfg["standard_fuer_stil"] / "fonts"
    stil.mkdir(parents=True, exist_ok=True)
    for d in dateien:
        shutil.copyfile(ziel / d, stil / d)
    (stil / "fonts.css").write_text("\n".join(regeln) + "\n", encoding="utf-8")
    print(f"{sid}: {len(dateien)} Dateien -> {cfg['standard_fuer_stil']}/fonts/")


def lizenz_pruefen():
    """Jede Familie muss im Ordner ofl/ des Repos google/fonts liegen."""
    ok = True
    for p in sorted(SETS.glob("*.json")):
        for fam in json.loads(p.read_text(encoding="utf-8"))["familien"]:
            ordner = re.sub(r"[^a-z0-9]", "", fam.lower())
            try:
                meta = hole(f"https://raw.githubusercontent.com/google/fonts/main/ofl/{ordner}/METADATA.pb").decode()
                lic = re.search(r'license: "(\w+)"', meta).group(1)
            except Exception:
                lic = "NICHT IN ofl/"
            ok &= lic == "OFL"
            print(f"{p.stem:9} {fam:24} {lic}")
    return ok


if __name__ == "__main__":
    if "--lizenz" in sys.argv:
        sys.exit(0 if lizenz_pruefen() else 1)
    ids = sys.argv[1:] or [p.stem for p in sorted(SETS.glob("*.json"))]
    for sid in ids:
        set_laden(sid)
