# ich bin ein Kommentar

# Print
print("Hello World")
print(5)

my_number = 5
print (my_number) # prints 5
my_number = my_number + 3
print (my_number) # prints 10

a = 5
c = " Hello World ! " # string
print(c)

# boolean
d = True
e = False
print(d)

g = (2 > a) # False
print(g)
h = (5== a) # True
print(h)

# lists
list1 = ["Hi" , "you"]
list2 = [1 , 5, 7, 3]
print (list1 [0]) # prints first element "Hi"
print (len (list1)) # prints length "2"

from time import sleep_ms
# Schlafen fuer 1 '000 Millisekunden = 1 Sek
print("Ich bin müde!")
sleep_ms(1000)
print("Ich bin immernoch müde!")


if my_number > 10:
    print("Groesser als 10")
elif my_number < 5:
    print("Kleiner als 5")
else :
    print("Zwischen 5 und 10")
    
# for Schleife
for i in range (1 , 5):
    # i Werte : 1 ,2 ,3 ,4
    print (i)
    
for i in range (5):
    # i Werte : 0 ,1 ,2 ,3 ,4
    print (i)
    
mylist = [2 ,4 ,6 ,7]
for i in range(len(mylist)):
    # i Werte : 0 ,1 ,2 ,3 ( len = Laenge =4)
    print(i)
    
for i in mylist :
    # i Werte : 2 ,4 ,6 ,7
    print(i)
    
# while Schleife , zaehlt bis 9
number = 0
while number < 10:
    number += 1
    print(number)
    
# Dauerschleife
#while True :
#    print("Dauerschleife")
#    sleep_ms(1000)


def addieren(number1, number2):
    return number1 + number2

print(addieren(7, 14))

from machine import Pin
joystick_left = Pin(7, Pin.IN)
if joystick_left.value() == 0:
    print("Links gedrueckt")
    
    
from neopixel import NeoPixel

# Initialisiere NeoPixel
np = NeoPixel(Pin(19, Pin.OUT), 64)

# Farbwerte von 0 bis 255
np[0] = [100, 0, 0] # Pixel 0 leuchtet rot
np[1] = [0, 186, 0] # Pixel 1 leuchtet gruen
np[2] = [0, 0, 255] # Pixel 2 leuchtet blau

# Farbwerte an LEDs senden
np.write()


# Initialisiere NeoPixel
np = NeoPixel(Pin(19, Pin.OUT), 64)

# Erstelle Liste fuer LEDs , welche rot leuchten sollen
red_leds = [42, 45, 50, 53]

# Erstelle Liste fuer LEDs , welche blau leuchten sollen
blue_leds = [10, 11, 12, 13, 17, 22]

# Setze die LEDs aus den Listen im Neopixel
for i in red_leds:
    np[i] = [50, 0, 0]
for i in blue_leds:
    np[i] = [0, 0, 50]

# Farbwerte an LEDs senden
np.write()
