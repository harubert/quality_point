# Stile und Schriftsets

Zwanzig Stile für Quality-Point-Folien (1920×1080) und zwanzig frei kombinierbare Schriftsets. Alles liegt lokal –
zur Laufzeit werden keine Schriften oder Bilder aus dem Netz geladen.

**Auswahl ansehen:** `styles/index.html` im Browser öffnen. Die Seite ist zugleich das Onboarding: Ablauf in vier Schritten, die drei Bilder-Wege mit Kosten und Grenzen, dann alle Stile (Mini-Folien, Klick = alle acht Musterfolien groß). Neu bauen: `python styles/_werkzeuge/vorschau_bauen.py`.

**Ohne Schlüssel oder mit Bildgenerator?** `stil.json` → `bilder.vektor`: `voll` = Vektor gleichwertig (bauhaus, comic, fibel, journal, riso, tafelkreide) · `gut` = Vektor gut, Bildgenerator stimmungsvoller (gouache, nachtprogramm, papiertheater) · `schwach` = Bildgenerator empfohlen (knetwerk). Jede Stilkarte zeigt beide Beispielbilder nebeneinander.

## Stile

| Vorschau | Stil | Stimmung | Schriftset | passt zu |
|---|---|---|---|---|
| ![](papiertheater/vorschau.webp) | `papiertheater` | warm, handgemacht, erzählend | theater | Primarstufe, Fallbeispiele, Elternabende |
| ![](fibel/vorschau.webp) | `fibel` | klar, fröhlich, lehrreich | fibel | Grundschule, Lesen/Schreiben, Merksätze |
| ![](gouache/vorschau.webp) | `gouache` | ruhig, poetisch, geborgen | gouache | Bilderbuch, Elementarpädagogik, Werte |
| ![](knetwerk/vorschau.webp) | `knetwerk` | verspielt, weich, freundlich | knete | Kinder 4–10, Trickfilm, Projektarbeit |
| ![](nachtprogramm/vorschau.webp) | `nachtprogramm` | atmosphärisch, nachdenklich (dunkel) | nacht | Jugendliche, Social Media, Abendvorträge |
| ![](riso/vorschau.webp) | `riso` | frisch, grafisch, zeitgenössisch | riso | Erwachsenenbildung, Design, Pitches |
| ![](tafelkreide/vorschau.webp) | `tafelkreide` | schulisch, handgezeichnet (dunkel) | kreide | Unterrichtsplanung, Mathe/Sachunterricht |
| ![](bauhaus/vorschau.webp) | `bauhaus` | sachlich, mutig, strukturiert | grotesk | Gestaltung, Modelle, Daten |
| ![](journal/vorschau.webp) | `journal` | seriös, ruhig, präzise | journal | Forschung, Tagungen, Statistik |
| ![](comic/vorschau.webp) | `comic` | laut, witzig, dynamisch | comic | Einstiege, Jugendliche, Medienkritik |
| ![](herbarium/vorschau.webp) | `herbarium` | ruhig, gesammelt, naturkundlich | herbarium | Sachunterricht und Natur, Bibliotheks- und Lesethemen, Sammlungen, Material- und Methodenkoffer |
| ![](nordisch/vorschau.webp) | `nordisch` | ruhig, aufgeräumt, freundlich | nordisch | Elementar- und Primarpädagogik, Schulentwicklung und Konzepte, Elternabende und Beratung |
| ![](magazin/vorschau.webp) | `magazin` | ruhig, kultiviert, warm | magazin | Elternabende und Vorträge, Kultur-, Lese- und Buchthemen, Porträts und Fallgeschichten |
| ![](galerie/vorschau.webp) | `galerie` | still, konzentriert, kuratiert | galerie | Kunst, Fotografie, Bildkompetenz, Museums- und Kulturvermittlung, Portfolio- und Projektpräsentationen |
| ![](schweizer/vorschau.webp) | `schweizer` | klar, streng, selbstbewusst | schweiz | Hochschullehre und Vorlesungen, Gestaltung und Typografie, Thesen und Argumentationen |
| ![](zeitung/vorschau.webp) | `zeitung` | sachlich, dringlich, dokumentarisch | zeitung | Nachrichten, Fake News, Quellenkritik, Journalismus und Schülerzeitung, Politische Bildung |
| ![](linol/vorschau.webp) | `linol` | kraftvoll, handgemacht, grafisch | linol | Kunst- und Werkunterricht, Plakate, Kampagnen, Thesen, Medienkritik und Haltung |
| ![](beton/vorschau.webp) | `beton` | roh, direkt, laut | beton | Jugendliche und junge Erwachsene, Medienkritik und Provokation, Workshops, Hackathons, Projekttage |
| ![](konsole/vorschau.webp) | `konsole` | technisch, konzentriert, nerdig (dunkel) | konsole | Informatik und Coding-Unterricht, Algorithmen, KI und Datenschutz, Making, Robotik, Tüfteln |
| ![](blaupause/vorschau.webp) | `blaupause` | präzise, konstruktiv, ingenieurhaft (dunkel) | blaupause | Technik, Making und Werken, Planung und Unterrichtsentwürfe, Modelle, Abläufe, Architektur von Systemen |

Jeder Ordner `styles/<id>/` enthält:

| Datei | Inhalt |
|---|---|
| `stil.css` | Tokens in `:root` + Dekor-Regeln für die Folienklassen (wird nach `engine/src/basis.css` geladen) |
| `stil.json` | Name, Beschreibung, Stimmung, `passt_zu`, Farben, `schriften` (Rollen + Achsen), `google_fonts` (API-Familien), `bildprompt`, `vektor_hinweise` |
| `vorschau.webp` | Bildschirmfoto (Titel, Kapitel, Zitat, Kennzahl) |
| `beispiel/` | Beispielbilder: `titel`/`motiv` (KI-generiertes WebP oder SVG) und bei KI-Stilen zusätzlich `vektor.svg` – das, was Claude ohne Bildgenerator selbst zeichnet |

## Token-Vertrag

Ausführlich in [`engine/TOKENS.md`](../engine/TOKENS.md). Jeder Stil setzt in `:root`:

`--paper --paper2 --card --ink --ink2 --ink3 --red --teal --teal-d --yellow --coral`
(Farben) und `--serif` (Überschriften), `--accent` (Akzentwörter `h2 em`), `--lesen` (gut lesbare
Kursive für Zitate/Übersetzungen – keine schmale Condensed-Kursive), `--ui` (Text/Oberfläche), `--sans`.

Optional gesetzt: `--sand`, `--*-l`, `--night`, `--auf-dunkel`, `--auf-akzent`, `--buehne`, `--ui-dunkel`,
`--panel`, `--schatten`, `--radius`, `--radius-s`. Dunkle Stile (`nachtprogramm`, `tafelkreide`) **müssen**
`--auf-dunkel`, `--auf-akzent`, `--ui-dunkel`, `--panel` setzen, weil die Ableitungen aus `--ink` dort hell wären;
`--teal-d` ist dort eine *helle* Variante (Text auf `--teal-l`).

Dekor nur per CSS bzw. SVG-Data-URI (Papierkorn, Kreidestaub, Raster). Gestaltete Klassen: `slide`, `s-title`,
`s-chapter` (+ `.etikett`, `.toc`, `.bignum`), `s-dark`, `s-statement`, `s-auftrag` (+ `.panel`, `.wk`, `.meta`),
`kick`, `h1/h2 em`, `card` (`t/c/r/y`, `tape`), `tag`, `box` (`def/res/tip/daz`), `quote`, `ueb`, `tbl`,
`dots`, `steps`, `sb`, `wcard`, `bub`, `foto`, `zettel`, `zahl`, `zl`, `bars`, `lesehilfe`, `uf`, `pointe`.

## Schriftsets

`_schriftsets/<id>.json` beschreibt Rollen, Achsen und CSS-Variablen; `_schriftsets/fonts/<id>.css` lädt die
lokalen Dateien. Ein Set mit einem anderen Stil kombinieren: dessen `fonts/<id>.css` einbinden und die
`css_variablen` aus der JSON nach dem `stil.css` in `:root` setzen.

| Set | Titel | Akzent | Lesen (Kursive) | UI | Standard für |
|---|---|---|---|---|---|
| theater | Young Serif | Instrument Serif | Source Serif 4 | Instrument Sans | papiertheater |
| fibel | Archivo (breit) | Fraunces | Andika | Archivo | fibel |
| gouache | DM Serif Display | DM Serif Display Italic | Lora | Karla | gouache |
| knete | Fredoka | Grandstander | Nunito | Nunito | knetwerk |
| nacht | Syne | Bodoni Moda | Inter Tight | Inter Tight | nachtprogramm |
| riso | Bricolage Grotesque | IBM Plex Serif | IBM Plex Serif | IBM Plex Sans (+ Mono) | riso |
| kreide | Cabin Sketch | Caveat | Atkinson Hyperlegible | Atkinson Hyperlegible | tafelkreide |
| grotesk | Jost | Jost Italic | Libre Franklin | Libre Franklin | bauhaus |
| journal | Literata | Newsreader | Literata | Public Sans | journal |
| comic | Bangers | Titan One | Shantell Sans | Shantell Sans | comic |
| beton | Anton | Space Mono | Gelasio | Space Mono | beton |
| blaupause | Rajdhani | Saira | Saira | Saira | blaupause |
| galerie | Hanken Grotesk | Spectral | Spectral | Hanken Grotesk | galerie |
| herbarium | Cormorant Garamond | Cormorant Garamond | EB Garamond | Alegreya Sans | herbarium |
| konsole | Martian Mono | JetBrains Mono | Fira Sans | JetBrains Mono | konsole |
| linol | Alfa Slab One | Bitter | Bitter | Work Sans | linol |
| magazin | Libre Caslon Display | Libre Caslon Text | Libre Caslon Text | DM Sans | magazin |
| nordisch | Manrope | Crimson Pro | Crimson Pro | Manrope | nordisch |
| schweiz | Host Grotesk | Host Grotesk | Host Grotesk | Host Grotesk | schweizer |
| zeitung | Oswald | PT Serif | PT Serif | Barlow Semi Condensed | zeitung |

**Lizenzen:** alle Familien stehen unter der **SIL Open Font License 1.1** (geprüft gegen den Ordner
`ofl/` von [google/fonts](https://github.com/google/fonts) mit `python styles/_werkzeuge/schriften_holen.py --lizenz`).
Die OFL erlaubt Weitergabe und Einbetten, auch kommerziell; die Schriften dürfen nicht einzeln verkauft werden,
und abgeleitete Schriften dürfen die reservierten Namen nicht tragen. Lizenztexte: <https://openfontlicense.org>.

Neu laden: `python styles/_werkzeuge/schriften_holen.py [set …]` (Google-Fonts-CSS-API mit Chrome-Kennung,
nur `latin` + `latin-ext`, Ablage in `styles/_schriftsets/fonts/`).

## Bilder

**Mit Bildgenerator:** `python styles/bilder_generieren.py <stil> "<Motiv, englisch>" [--name k3] [--anbieter …]`.
Prompt = `bildprompt` aus `stil.json` + Motiv. Der Schlüssel wird nur aus der Umgebungsvariable gelesen –
nie in Dateien schreiben. `--nur-prompt` gibt nur den Prompt aus (zum Einfügen in ein Web-Tool).

| Anbieter | Variable | Vorteile | Nachteile |
|---|---|---|---|
| OpenAI gpt-image | `OPENAI_API_KEY` | folgt langen Stil-Prompts sehr genau, gute Komposition (Freifläche links) | eher teuer, langsam (20–60 s) |
| Google Imagen (Gemini API) | `GEMINI_API_KEY` | hohe Bildqualität, 16:9 nativ, günstig | strenge Inhaltsfilter (Kinder!), Modellnamen ändern sich |
| fal.ai Flux | `FAL_KEY` | sehr schnell und günstig (schnell-Modell), viele Modelle | Stiltreue bei „schnell“ geringer; Bild per URL |
| Stability AI | `STABILITY_API_KEY` | einfache API, WebP direkt, gute Malstile | Kreditsystem, Komposition weniger zuverlässig |
| Replicate | `REPLICATE_API_TOKEN` | jedes offene Modell (Flux, SDXL …) wählbar | Kaltstarts, Abrechnung pro Sekunde |

Modelle umstellbar über `QP_OPENAI_MODEL`, `QP_GEMINI_MODEL`, `QP_FAL_MODEL`, `QP_REPLICATE_MODEL`.
Nutzungsbedingungen des jeweiligen Anbieters beachten; keine realen Personen oder Marken erzeugen.

**Ohne Schlüssel – Vektor-Modus:** Das Skript gibt die `vektor_hinweise` des Stils aus. Claude zeichnet danach
eine SVG-Illustration (Beispiele: `tafelkreide/`, `bauhaus/`, `journal/`, `comic/` → `beispiel/*.svg`).

## Werkzeuge

| Befehl | Zweck |
|---|---|
| `python styles/_werkzeuge/vorschau_bauen.py [--bilder]` | `_vorschau/<stil>.html`, `index.html`; mit `--bilder` `vorschau.webp` per headless Edge/Chrome |
| `python styles/_werkzeuge/pruefen.py` | Token-Vertrag, CSS-Klammern/Deklarationen, Kontraste (Text ≥ 4.5:1, Akzente ≥ 3:1), externe URLs |
| `python styles/_werkzeuge/schriften_holen.py [--lizenz]` | Schriften laden bzw. Lizenzen prüfen |

Neuen Stil anlegen: Ordner kopieren, Tokens in `stil.css` anpassen, `stil.json` ausfüllen, Schriftset wählen,
dann `vorschau_bauen.py --bilder` und `pruefen.py` ausführen.
