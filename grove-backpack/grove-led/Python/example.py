import board
import digitalio
import time

led = digitalio.DigitalInOut(board.IO15)
led.direction = digitalio.Direction.OUTPUT

print(led)

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)