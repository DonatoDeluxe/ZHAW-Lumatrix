# Importierte Bibliotheken
from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms

# Variablen / Objekte initialisieren
led_pin = Pin(19, Pin.OUT)
matrix = NeoPixel(led_pin, 64)

# Im Programmcode wird immer bei 0 gestartet
matrix[10] = [50, 0, 0]
matrix[11] = [0, 0, 50]
matrix[3] = [50, 0, 50]
matrix[4] = [50, 50, 0]
matrix[5] = [255, 255, 255]
matrix.write() # Informationen zur Matrix / den LEDs schicken
