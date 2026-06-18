import sys
import select
from zhaw_led_matrix import LedMatrix, PixelColor, ColorTable

# --- Konfiguration ---
WCL = LedMatrix(8, 8)
CL = ColorTable()
WCL.set_brightness(15)

def bar_color(level):
    if level < 3:
        return CL.GREEN
    elif level < 6:
        return CL.YELLOW
    else:
        return CL.RED

# heights[x] = Höhe 0..8 für Spalte x. 0,0 ist unten links.
def draw(heights):
    WCL.clear()
    for x in range(8):
        h = heights[x]
        for level in range(h):
            y = level          # unten=0, wächst nach oben
            WCL.draw_list([[x, y]], bar_color(level))
    WCL.apply()

# --- Serial einlesen (nicht-blockierend) ---
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

buf = ""
while True:
    if poll.poll(0):
        ch = sys.stdin.read(1)
        if ch == "\n":
            parts = buf.split(",")
            if len(parts) == 8:
                try:
                    heights = [max(0, min(8, int(p))) for p in parts]
                    draw(heights)
                except ValueError:
                    pass
            buf = ""
        else:
            buf += ch

