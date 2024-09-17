import board
import analogio
import time

rotary_sensor = analogio.AnalogIn(board.IO2)

while True :

    print(rotary_sensor.value)
    time.sleep(0.1)