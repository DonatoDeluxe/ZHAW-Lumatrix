from zhaw_led_matrix import (
    ColorTable,
    LedMatrix,
    PixelColor,
    Button
)

from time import sleep_ms

#Colors
mycolor_list = [ColorTable.YELLOW,
                ColorTable.ORANGE,
                ColorTable.RED,
                ColorTable.PURPLE,
                ColorTable.PINK,
                ColorTable.BLUE,
                ColorTable.TEAL,
                ColorTable.AQUA,
                ColorTable.LIME,
                ColorTable.GREEN,
                ColorTable.LGREY,
                ColorTable.GREY,
                ColorTable.BROWN,
                ColorTable.LBROWN,
                ColorTable.WHITE,
                ColorTable.BLACK]

# Button initialisieren
btn = Button()

def button_left(_):
    if btn.switch.value() == 0:
        if cursor_position[0]>0:
            cursor_position[0] -= 1
            cursor_blink()
    else:
        global current_color_index
        if current_color_index>0:
            current_color_index -= 1
        else:
            current_color_index = len(mycolor_list)-1
        
            
def button_right(_):
    if btn.switch.value() == 0:
        if cursor_position[0]<num_cols-1:
            cursor_position[0] += 1
            cursor_blink()
    else:
        global current_color_index
        if current_color_index<len(mycolor_list)-1:
            current_color_index += 1
        else:
            current_color_index = 0
        
def button_down(_):
    if btn.switch.value() == 0:
        if cursor_position[1]>0:
            cursor_position[1] -= 1
            cursor_blink()
    else:
        global current_brightness
        if current_brightness > 10:
            current_brightness -= 10
            matrix.set_brightness(current_brightness)
        
def button_up(_):
    if btn.switch.value() == 0:
        if cursor_position[1]<num_rows-1:
            cursor_position[1] += 1
            cursor_blink()
    else:
        global current_brightness
        if current_brightness < 90:
            current_brightness += 10
            matrix.set_brightness(current_brightness)

def button_center(_):
    x,y = cursor_position
    
    i, inlist = is_in_list(image_list,cursor_position)
    if inlist == False:
        image_list.append([x,y])
        r,g,b = mycolor_list[current_color_index]
        color_list.append([r,g,b])
    else:
        r,g,b = mycolor_list[current_color_index]
        color_list[i]=[r,g,b]
    cursor_blink()

def is_in_list(thelist,coord):
    x,y = coord
    for i in range(len(thelist)):
        if thelist[i][0] == x and thelist[i][1]==y:
            return i,True
    return 0,False

btn.set_left_handler(button_left)
btn.set_right_handler(button_right)
btn.set_up_handler(button_up)
btn.set_down_handler(button_down)
btn.set_center_handler(button_center)



num_rows = 8
num_cols = 8
image_list = []
color_list = []
cursor_position=[0,0]
current_color_index = 0
current_brightness = 20


# LED Matrix Objekt
matrix = LedMatrix(num_rows, num_cols)

# Setze Helligkeit
matrix.set_brightness(current_brightness)


def cursor_blink():
    matrix.clear()
    for i in range(len(image_list)):    
        matrix.draw_list([image_list[i],], color_list[i])
    matrix.draw_list([cursor_position,],ColorTable.BLACK)
    matrix.apply()
    sleep_ms(10)
    matrix.clear()
    for i in range(len(image_list)):    
        matrix.draw_list([image_list[i],], color_list[i])
    matrix.draw_list([cursor_position,],mycolor_list[current_color_index])
    matrix.apply()
    sleep_ms(1)
    

while True:
    matrix.clear()
    for i in range(len(image_list)):    
        matrix.draw_list([image_list[i],], color_list[i])
    matrix.draw_list([cursor_position,],mycolor_list[current_color_index])
    matrix.apply()
    sleep_ms(100)
