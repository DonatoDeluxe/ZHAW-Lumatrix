from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

pin = Pin(19, Pin.OUT)
np = NeoPixel(pin, 64)

sleepTime = 35
brightness = 35

while True:
    for i in range(len(np)):
        np[i] = (brightness, 0, 0)
        np.write()
        sleep_ms(sleepTime)
    
    for i in range(len(np)):
        np[i] = (0, brightness, 0)
        np.write()
        sleep_ms(sleepTime)
    
    for i in range(len(np)):
        np[i] = (0, 0, brightness)
        np.write()
        sleep_ms(sleepTime)
    
    for i in range(len(np)):
        np[i] = (brightness, brightness, brightness)
        np.write()
        sleep_ms(sleepTime)
    
    for i in range(len(np)):
        np[i] = (0, 0, 0)
        np.write()
        sleep_ms(sleepTime)
