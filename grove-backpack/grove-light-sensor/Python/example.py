import time
import board
from analogio import AnalogIn

light_sensor = AnalogIn(board.IO15)

while True:
    light_level = light_sensor.value
    print("Light Level:", light_level)

    time.sleep(1)