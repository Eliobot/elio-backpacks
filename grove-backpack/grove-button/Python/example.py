import board
import digitalio
import time

# button definition
button = digitalio.DigitalInOut(board.IO2)
button.direction = digitalio.Direction.INPUT
# no pull up because the button has a pull up resistor

# main loop
while True:
    if button.value:  # button pressed when high
        print("Button pressed")
    else:
        print("Button released.")  # button released when low
    time.sleep(0.1) # debounce