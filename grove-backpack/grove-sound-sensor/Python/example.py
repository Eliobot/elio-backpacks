import time
import board
from analogio import AnalogIn

sound_sensor = AnalogIn(board.IO15)


def read_average_sound(levels=32):
    """
    Read the average sound level from the sound sensor
    """
    sum = 0
    for _ in range(levels):
        sum += sound_sensor.value
    return sum // levels


while True:
    average_sound = read_average_sound()
    print(average_sound)
    time.sleep(0.01)
