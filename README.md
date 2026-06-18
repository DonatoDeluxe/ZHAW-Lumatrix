# USB Audio Equalizer — Raspberry Pi Pico + 8×8 LED Matrix

Eine Echtzeit-Audiovisualisierung: Der PC analysiert das gerade abgespielte
System-Audio, zerlegt es per FFT in 8 Frequenzbänder und sendet die Pegel über
USB-Serial an einen Raspberry Pi Pico, der sie als animierte Balken auf einer
8×8-RGB-LED-Matrix darstellt.

---

## Funktionsweise

Die schwere Rechenarbeit liegt komplett auf dem PC. Der Pico ist ein reiner
Anzeige-Client und kennt nur 8 Zahlen pro Frame.

```
Windows-Audio
        │ 
        ▼
WASAPI Loopback  ──►  [PC]  Aufnahme → FFT → 8 Frequenzbänder → Höhe 0–8
        │
        │  USB-Serial:  "3,6,8,4,7,2,5,6\n"   (~25 Frames/s)
        ▼
   [Pico]  Zeile parsen → 8 Balken auf der Matrix zeichnen
```

Diese Aufteilung hat drei Vorteile: kein WLAN/OAuth auf dem Pico nötig, die
FFT läuft mühelos auf dem PC, und die Pico-Firmware bleibt minimal.

---

## Hardware

| Komponente            | Details                                                        |
|-----------------------|----------------------------------------------------------------|
| Mikrocontroller       | Raspberry Pi Pico (original, Standard-MicroPython)             |
| Anzeige               | ZHAW 8×8 RGB-LED-Matrix (WS2812B), Treiber `zhaw_led_matrix`   |
| Verbindung            | USB-Kabel Pico ↔ PC (zugleich Strom und Datenkanal)            |
| Host                  | Windows-PC mit Audioausgabe                                    |

---

## Software-Voraussetzungen

**Auf dem Pico:** MicroPython und die `zhaw_led_matrix`-Bibliothek müssen
installiert sein. Entwicklung und Upload erfolgen über Thonny.

**Auf dem PC:** Python 3.11+ und folgende Pakete:

```bash
pip install numpy pyserial pyaudiowpatch
```

- `numpy` — FFT und Bandberechnung
- `pyserial` — USB-Serial-Kommunikation mit dem Pico
- `pyaudiowpatch` — WASAPI-Loopback, greift das System-Audio digital ab

---

## Projektstruktur

```
.
├── main.py                          # läuft auf dem Pico (aktive Version)
├── Programme/                       # ZHAW
├── Tutorial/                        # ZHAW
├── bitmaps/                         # ZHAW
├── zhaw_led_matrix/                 # ZHAW (Matrix-Treiber)
└── PersönlicheProjekte/
    └── Equalizer/
        ├── equalizer_8x8_pc.py        # auf dem PC ausführen
        └── equalizer_8x8_raspberry.py # Inhalt in main.py kopieren
```

## Dateien

| Datei                          | Läuft auf | Zweck                                            |
|--------------------------------|-----------|--------------------------------------------------|
| `main.py`                      | Pico      | Aktive Pico-Version (Quelle s. unten)            |
| `equalizer_8x8_raspberry.py`   | Pico      | Pico-Code; Inhalt bei Bedarf in `main.py` kopieren |
| `equalizer_8x8_pc.py`          | PC        | Audio-Aufnahme, FFT, Bänder, sendet an den Pico  |

> Der Pico führt beim Boot `main.py` aus. Der eigentliche Equalizer-Code liegt
> in `PersönlicheProjekte/Equalizer/equalizer_8x8_raspberry.py` — dessen Inhalt
> kopierst du in `main.py`, wenn der Equalizer laufen soll.

---

## Einrichtung

### 1. Pico vorbereiten

1. `main.py` über Thonny auf den Pico speichern (Ziel: *MicroPython device*).
2. In Thonny über die Shell testen, dass die Matrix grundsätzlich zeichnet:
   ```python
   draw([3,6,8,4,7,2,5,6])
   ```
   Es sollte eine Balken-Treppe erscheinen.

### 2. PC-Skript einrichten

1. Pakete installieren (siehe oben).
2. Sicherstellen, dass die Musik über das **Standard-Ausgabegerät** läuft —
   genau dieses Gerät greift das Loopback ab.

### 3. Starten

1. In Thonny **Stop**, dann **Disconnect** (oder Thonny ganz schließen).
   Der COM-Port kann immer nur von *einem* Programm gleichzeitig belegt werden.
2. Pico einmal neu anstecken.
3. PC-Skript starten:
   ```bash
   python PersönlicheProjekte/Equalizer/equalizer_8x8_pc.py
   ```
4. Musik abspielen — die Matrix sollte reagieren.

---

## Konfiguration & Tuning

Die wichtigsten Stellschrauben in `equalizer_8x8_pc.py`:

| Parameter     | Wirkung                                                            |
|---------------|-------------------------------------------------------------------|
| `BAND_EDGES`  | Frequenzgrenzen der 8 Bänder (Hz)                                 |
| `BAND_GAIN`   | Pro-Band-Anhebung; hebt hohe Frequenzen an, damit sie nicht kleben|
| `GAIN`        | Globale Empfindlichkeit                                           |
| `SMOOTH`      | Glättung der Bewegung (0 = träge, 1 = sofort)                     |
| `CHUNK`       | FFT-Blockgröße; größer = feinere Frequenzauflösung, mehr Latenz   |

**Balken zu niedrig:** Teiler (`/ 12.0`) verkleinern oder `GAIN` erhöhen.
**Balken kleben oben:** Teiler vergrößern.
**Bewegung zu nervös:** `SMOOTH` senken (z. B. `0.3`).
**Höhen-Bänder zu schwach:** hintere Werte in `BAND_GAIN` erhöhen.

---

## Troubleshooting

**„Access is denied" / Port lässt sich nicht öffnen**
Thonny ist noch verbunden und hält den COM-Port. Thonny schließen, ggf. im
Task-Manager prüfen, ob `python.exe`/`thonny.exe` noch läuft.

**Erstes Band (Spalte 0) immer leer**
Bei 96 kHz Samplerate und `CHUNK = 1024` beträgt die FFT-Auflösung ~94 Hz/Bin —
in ein schmales 20–60-Hz-Band fällt kein Bin. Untere Bandgrenze anheben
(`BAND_EDGES` beginnt bei 40 Hz) oder `CHUNK` erhöhen (z. B. 4096).

**Nur Stille wird visualisiert**
Das abgegriffene Gerät und das Gerät, auf dem die Musik spielt, müssen identisch
sein. Beim Start gibt das Skript die gewählte Audioquelle aus — diese mit dem
tatsächlichen Wiedergabegerät abgleichen.

---

## Koordinatensystem

Auf dieser Matrix liegt `(0,0)` **unten links**, `(7,7)` oben rechts. Balken
wachsen von unten nach oben (`for level in range(heights[x])` zeichnet
aufsteigende y-Werte). Bei anderer Matrix-Orientierung lässt sich die Zuordnung
in der `draw()`-Funktion über eine Koordinatentransformation drehen oder
spiegeln.

---

## Mögliche Erweiterungen

- Spotify Web API (PC-seitig via `spotipy`): Titel/Interpret anzeigen, danach
  für einige Sekunden in den Equalizer-Modus wechseln.
- Peak-Hold-Punkte über den Balken (kurzes Halten des Maximums).
- Farbpalette und Helligkeit zur Laufzeit umschaltbar.

---

## ZHAW-Material & Lizenz

Privates Lernprojekt. Eigenentwicklung sind ausschließlich die Dateien unter
`PersönlicheProjekte/Equalizer/` sowie das daraus kopierte `main.py`.

Die folgenden Verzeichnisse stammen aus dem ZHAW-Lehrmaterial, unterliegen den
Bedingungen der ZHAW und sind **nicht** Teil der Eigenentwicklung:

- `Programme/` — ZHAW
- `Tutorial/` — ZHAW
- `bitmaps/` — ZHAW
- `zhaw_led_matrix/` — ZHAW (Matrix-Treiber)
