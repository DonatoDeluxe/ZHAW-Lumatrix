import numpy as np
import pyaudiowpatch as pyaudio
import serial
import sys
import time

# --- Konfiguration ---
COM_PORT = "COM6"     # <-- anpassen!
BAUD = 115200
BANDS = 8
MAX_HEIGHT = 8
CHUNK = 1024
SMOOTH = 0.5
GAIN = 1.0
BAND_EDGES = [40, 120, 250, 500, 1000, 2200, 4500, 9000, 16000]

def open_serial():
    try:
        ser = serial.Serial(COM_PORT, BAUD, timeout=1)
        time.sleep(2)
        print(f"Serial offen auf {COM_PORT}")
        return ser
    except Exception as e:
        print(f"FEHLER Serial: {e}")
        print("Tipp: In Thonny auf STOP/Disconnect klicken (Port belegt?).")
        sys.exit(1)

def find_loopback(p):
    wasapi = p.get_host_api_info_by_type(pyaudio.paWASAPI)
    default_out = p.get_device_info_by_index(wasapi["defaultOutputDevice"])
    if not default_out.get("isLoopbackDevice", False):
        for lb in p.get_loopback_device_info_generator():
            if default_out["name"] in lb["name"]:
                return lb
    return default_out

def main():
    ser = open_serial()
    p = pyaudio.PyAudio()
    dev = find_loopback(p)
    rate = int(dev["defaultSampleRate"])
    channels = dev["maxInputChannels"]
    print(f"Audio-Quelle: {dev['name']} ({rate} Hz, {channels} ch)")

    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=rate,
        frames_per_buffer=CHUNK,
        input=True,
        input_device_index=dev["index"],
    )

    freqs = np.fft.rfftfreq(CHUNK, 1.0 / rate)
    band_bins = []
    for i in range(BANDS):
        lo, hi = BAND_EDGES[i], BAND_EDGES[i + 1]
        idx = np.where((freqs >= lo) & (freqs < hi))[0]
        band_bins.append(idx)

    smoothed = np.zeros(BANDS)
    print("Laeuft. Mit Strg+C beenden.")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            if channels > 1:
                samples = samples.reshape(-1, channels).mean(axis=1)

            windowed = samples * np.hanning(len(samples))
            spectrum = np.abs(np.fft.rfft(windowed))

            levels = np.zeros(BANDS)
            for i, idx in enumerate(band_bins):
                if len(idx) > 0:
                    levels[i] = spectrum[idx].mean()

            levels = np.log1p(levels) * GAIN
            norm = levels / 12.0
            heights = np.clip(norm * MAX_HEIGHT, 0, MAX_HEIGHT)

            smoothed = SMOOTH * heights + (1 - SMOOTH) * smoothed
            out = [int(round(v)) for v in smoothed]

            # print(out, "  raw max:", round(float(spectrum.max()), 1))  # DEBUG

            ser.write((",".join(map(str, out)) + "\n").encode())
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("\nBeende...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        ser.close()

if __name__ == "__main__":
    main()