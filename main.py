from zhaw_led_matrix import LedMatrix, ColorTable
import sys
import select

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

def draw(heights):
    WCL.clear()
    for x in range(8):
        for level in range(heights[x]):
            WCL.draw_list([[x, level]], bar_color(level))
    WCL.apply()

# Lebenszeichen
WCL.clear()
WCL.draw_list([[0,0],[7,7]], CL.GREEN)
WCL.apply()

# Roh über sys.stdin.buffer lesen
buf = b""
while True:
    # auf ein Byte warten (blockierend, roh)
    ch = sys.stdin.buffer.read(1)
    if ch:
        if ch == b"\n":
            try:
                parts = buf.decode().strip().split(",")
                if len(parts) == 8:
                    heights = [max(0, min(8, int(p))) for p in parts]
                    draw(heights)
            except (ValueError, UnicodeError):
                pass
            buf = b""
        else:
            buf += ch