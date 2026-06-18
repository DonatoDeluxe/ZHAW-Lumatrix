"""
Farben:
YELLOW,ORANGE,RED,PURPLE,PINK,BLUE,TEAL,AQUA,LIME,GREEN,LGREY,GREY,BROWN,LBROWN,WHITE,BLACK
"""

from zhaw_led_matrix import Lumatrix, ColorTable

mein_text = "+100 Aura"

lumatrix = Lumatrix()

while True:
    lumatrix.writeText(mein_text, ColorTable.ORANGE, 50)
