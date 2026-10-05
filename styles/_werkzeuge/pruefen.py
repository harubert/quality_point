"""Prüft alle Stile: Token-Vertrag, CSS-Syntax (grob), Kontraste, externe URLs, stil.json-Felder.

Aufruf:  python styles/_werkzeuge/pruefen.py        (Rückgabe 1 bei Fehlern)
"""
import json, re, sys
from pathlib import Path

STYLES = Path(__file__).resolve().parent.parent
TOKENS = ["paper", "paper2", "card", "ink", "ink2", "ink3", "red", "teal", "teal-d", "yellow", "coral",
          "serif", "accent", "lesen", "ui", "sans"]
JSON_FELDER = ["id", "name", "beschreibung", "stimmung", "passt_zu", "farben", "schriften", "bildprompt", "vektor_hinweise"]
ERLAUBT = ("http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink")   # Namensräume, kein Netzaufruf
fehler = []


def syntax(css, name):
    """Klammern/Anführungszeichen außerhalb von Kommentaren und Strings; Deklarationen der Form prop:wert."""
    s = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    tiefe, par, i, q = 0, 0, 0, None
    while i < len(s):
        c = s[i]
        if q:
            if c == "\\": i += 1
            elif c == q: q = None
        elif c in "\"'": q = c
        elif c == "{": tiefe += 1
        elif c == "}":
            tiefe -= 1
            if tiefe < 0: return f"{name}: '}}' ohne '{{' bei Zeichen {i}"
        elif c == "(": par += 1
        elif c == ")": par -= 1
        i += 1
    if q or tiefe or par:
        return f"{name}: unausgeglichen (Klammern {tiefe}, runde {par}, String {q})"
    ohne = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '""', s)
    for block in re.findall(r"\{([^{}]*)\}", ohne):
        for d in block.split(";"):
            d = d.strip()
            if d and not re.match(r"^-{0,2}[a-zA-Z][\w-]*\s*:", d) and not re.match(r"^(from|to|\d+%)", d):
                return f"{name}: verdächtige Deklaration „{d[:60]}“"
    return None


def rgb(v, grund=(255, 255, 255)):
    v = v.strip()
    m = re.match(r"#([0-9a-fA-F]{6})$", v)
    if m:
        h = m.group(1); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.match(r"rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)", v)
    if m:
        r, g, b = (float(m.group(i)) for i in (1, 2, 3)); a = float(m.group(4) or 1)
        return tuple(round(a * x + (1 - a) * y) for x, y in zip((r, g, b), grund))
    return None


def lum(c):
    f = lambda x: (x / 255) / 12.92 if x / 255 <= .03928 else ((x / 255 + .055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c); return .2126 * r + .7152 * g + .0722 * b


def kontrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)


def tokens(css):
    root = " ".join(re.findall(r":root\{(.*?)\}", css, re.S))
    return dict(re.findall(r"--([\w-]+):\s*([^;]+);", root))


ergebnis = []
for d in sorted(p for p in STYLES.iterdir() if (p / "stil.css").exists()):
    css = (d / "stil.css").read_text(encoding="utf-8")
    t = tokens(css)
    fehlend = [k for k in TOKENS if k not in t]
    if fehlend: fehler.append(f"{d.name}: Token fehlen {fehlend}")
    e = syntax(css, d.name + "/stil.css")
    if e: fehler.append(e)
    paper = rgb(t.get("paper", "#fff")); card = rgb(t.get("card", "#fff"), paper)
    werte, ok = {}, True
    for fg, mind in (("ink", 4.5), ("ink2", 4.5), ("ink3", 4.5), ("red", 3.0), ("teal", 3.0)):
        c = rgb(t.get(fg, "#000"), paper)
        k = min(kontrast(c, paper), kontrast(c, card))
        werte[fg] = round(k, 2)
        if k < mind:
            ok = False; fehler.append(f"{d.name}: Kontrast --{fg} {k:.2f} < {mind}")
    ergebnis.append((d.name, werte, ok))
    j = d / "stil.json"
    if not j.exists(): fehler.append(f"{d.name}: stil.json fehlt")
    else:
        cfg = json.loads(j.read_text(encoding="utf-8"))
        fehler += [f"{d.name}: stil.json ohne „{f}“" for f in JSON_FELDER if f not in cfg]
    if not (d / "fonts" / "fonts.css").exists(): fehler.append(f"{d.name}: fonts/fonts.css fehlt")

# externe URLs in CSS/HTML/SVG (Doku-Dateien ausgenommen)
for p in list(STYLES.rglob("*.css")) + list(STYLES.rglob("*.html")) + list(STYLES.rglob("*.svg")):
    txt = p.read_text(encoding="utf-8", errors="ignore")
    for u in re.findall(r"(?:https?:)?//[\w.-]+\.[a-z]{2,}[^\s\"')]*", txt):
        if not u.startswith(ERLAUBT) and not u.startswith("//www.w3.org"):
            fehler.append(f"externe URL in {p.relative_to(STYLES)}: {u[:80]}")
    for u in re.findall(r"url\(['\"]?([^'\")]+)", txt):
        if not u.startswith(("data:", "#", "%23")) and p.suffix == ".css":
            if not (p.parent / u).exists():
                fehler.append(f"fehlende Datei in {p.relative_to(STYLES)}: {u}")

print(f"{'Stil':15} {'ink':>6} {'ink2':>6} {'ink3':>6} {'red':>6} {'teal':>6}  ok")
for n, w, ok in ergebnis:
    print(f"{n:15} " + " ".join(f"{w[k]:6.2f}" for k in ("ink", "ink2", "ink3", "red", "teal")) + ("  ja" if ok else "  NEIN"))
print("\n".join(fehler) if fehler else "Keine Fehler.")
sys.exit(1 if fehler else 0)
