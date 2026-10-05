"""Erzeugt Folienbilder im Stil eines Quality-Point-Stils mit einem Bildgenerator deiner Wahl.

Prompt = styles/<stil>/stil.json → „bildprompt“ + „Subject: <motiv>“.

Aufruf
  python styles/bilder_generieren.py <stil> "<Motiv auf Englisch>" [--name datei] [--ausgabe ordner]
                                     [--anbieter openai|gemini|fal|stability|replicate] [--nur-prompt]
Beispiel
  python styles/bilder_generieren.py tafelkreide "a child explaining a tablet to a grandparent" --name k3

Anbieter (Schlüssel NUR als Umgebungsvariable – wird nie gespeichert oder ausgegeben):
  OPENAI_API_KEY       → OpenAI gpt-image (Modell: QP_OPENAI_MODEL, Vorgabe gpt-image-1)
  GEMINI_API_KEY       → Google Imagen über die Gemini API (QP_GEMINI_MODEL, Vorgabe imagen-4.0-generate-001)
  FAL_KEY              → fal.ai Flux (QP_FAL_MODEL, Vorgabe fal-ai/flux/schnell)
  STABILITY_API_KEY    → Stability AI Stable Image Core
  REPLICATE_API_TOKEN  → Replicate Flux (QP_REPLICATE_MODEL, Vorgabe black-forest-labs/flux-schnell)
Ohne --anbieter wird der erste Anbieter genommen, dessen Variable gesetzt ist (Reihenfolge wie oben).
Ohne Schlüssel: Hinweis auf den Vektor-Modus (Claude zeichnet SVG nach „vektor_hinweise“ in stil.json).
Nur Python-Standardbibliothek; Pillow (optional) wandelt in WebP ≤ 1600 px um.
"""
import argparse, base64, json, os, re, sys, uuid, urllib.error, urllib.request
from pathlib import Path

STYLES = Path(__file__).resolve().parent
ANBIETER = [("openai", "OPENAI_API_KEY"), ("gemini", "GEMINI_API_KEY"), ("fal", "FAL_KEY"),
            ("stability", "STABILITY_API_KEY"), ("replicate", "REPLICATE_API_TOKEN")]


def http(url, daten=None, kopf=None, roh=False, timeout=300):
    kopf = dict(kopf or {})
    if daten is not None and not isinstance(daten, bytes):
        daten = json.dumps(daten).encode(); kopf.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=daten, headers=kopf, method="POST" if daten is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        meldung = e.read()[:400].decode(errors="ignore")
        sys.exit(f"HTTP {e.code} von {url.split('/')[2]}: {meldung}")
    return body if roh else json.loads(body)


def openai(prompt, key):
    model = os.environ.get("QP_OPENAI_MODEL", "gpt-image-1")
    d = http("https://api.openai.com/v1/images/generations",
             {"model": model, "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1},
             {"Authorization": f"Bearer {key}"})
    return base64.b64decode(d["data"][0]["b64_json"])


def gemini(prompt, key):
    model = os.environ.get("QP_GEMINI_MODEL", "imagen-4.0-generate-001")
    d = http(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict",
             {"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": "16:9"}},
             {"x-goog-api-key": key})
    return base64.b64decode(d["predictions"][0]["bytesBase64Encoded"])


def fal(prompt, key):
    model = os.environ.get("QP_FAL_MODEL", "fal-ai/flux/schnell")
    d = http(f"https://fal.run/{model}", {"prompt": prompt, "image_size": "landscape_16_9", "num_images": 1},
             {"Authorization": f"Key {key}"})
    return http(d["images"][0]["url"], roh=True)


def stability(prompt, key):
    grenze = uuid.uuid4().hex
    teile = [("prompt", prompt), ("aspect_ratio", "16:9"), ("output_format", "webp")]
    body = b"".join(f'--{grenze}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in teile)
    body += f"--{grenze}--\r\n".encode()
    return http("https://api.stability.ai/v2beta/stable-image/generate/core", body,
                {"Authorization": f"Bearer {key}", "Accept": "image/*",
                 "Content-Type": f"multipart/form-data; boundary={grenze}"}, roh=True)


def replicate(prompt, key):
    model = os.environ.get("QP_REPLICATE_MODEL", "black-forest-labs/flux-schnell")
    d = http(f"https://api.replicate.com/v1/models/{model}/predictions",
             {"input": {"prompt": prompt, "aspect_ratio": "16:9", "output_format": "webp"}},
             {"Authorization": f"Bearer {key}", "Prefer": "wait"})
    out = d.get("output")
    if not out:
        sys.exit(f"Replicate: kein Ergebnis (Status {d.get('status')}): {d.get('error')}")
    return http(out[0] if isinstance(out, list) else out, roh=True)


def speichern(daten, ziel):
    try:
        from io import BytesIO
        from PIL import Image
        im = Image.open(BytesIO(daten)).convert("RGB")
        im.thumbnail((1600, 1600))
        ziel = ziel.with_suffix(".webp"); im.save(ziel, "WEBP", quality=82, method=6)
    except ImportError:
        ext = ".png" if daten[:4] == b"\x89PNG" else ".webp" if daten[8:12] == b"WEBP" else ".jpg"
        ziel = ziel.with_suffix(ext); ziel.write_bytes(daten)
    return ziel


def main():
    for strom in (sys.stdout, sys.stderr):
        try: strom.reconfigure(encoding="utf-8", errors="replace")
        except Exception: pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stil"); ap.add_argument("motiv")
    ap.add_argument("--name"); ap.add_argument("--ausgabe", default="bilder")
    ap.add_argument("--anbieter", choices=[a for a, _ in ANBIETER]); ap.add_argument("--nur-prompt", action="store_true")
    a = ap.parse_args()
    pfad = STYLES / a.stil / "stil.json"
    if not pfad.exists():
        sys.exit(f"Unbekannter Stil „{a.stil}“. Vorhanden: " +
                 ", ".join(sorted(p.parent.name for p in STYLES.glob("*/stil.json"))))
    cfg = json.loads(pfad.read_text(encoding="utf-8"))
    prompt = f"{cfg['bildprompt']} Subject: {a.motiv.strip().rstrip('.')}."
    if a.nur_prompt:
        print(prompt); return
    wahl = [(n, v) for n, v in ANBIETER if os.environ.get(v) and (a.anbieter in (None, n))]
    if not wahl:
        print("Kein Bild-API-Schlüssel gefunden (" + ", ".join(v for _, v in ANBIETER) + ").\n"
              "→ Vektor-Modus: Claude zeichnet die Illustration als SVG nach diesen Regeln:\n\n  "
              + cfg["vektor_hinweise"] + "\n\nPrompt für einen externen Generator:\n  " + prompt)
        sys.exit(2)
    name, var = wahl[0]
    print(f"Anbieter: {name} – Stil: {cfg['name']}")
    daten = globals()[name](prompt, os.environ[var])
    ordner = Path(a.ausgabe); ordner.mkdir(parents=True, exist_ok=True)
    slug = a.name or re.sub(r"[^a-z0-9]+", "-", a.motiv.lower()).strip("-")[:40]
    print("gespeichert:", speichern(daten, ordner / f"{a.stil}-{slug}"))


if __name__ == "__main__":
    main()
