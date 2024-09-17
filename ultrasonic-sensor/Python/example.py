import board
from digitalio import DigitalInOut, Direction
import pulseio
import time

# Initialize the trigger and echo pins
trigger = DigitalInOut(board.IO15)
trigger.direction = Direction.OUTPUT
trigger.value = False

echo = pulseio.PulseIn(board.IO16, maxlen=1)
echo.pause()
echo.clear()

# Function to measure the distance
def measure_distance():
    # Send a 10 microsecond pulse
    trigger.value = True
    time.sleep(0.00001)
    trigger.value = False

    echo.clear()
    echo.resume()

    start = time.monotonic()
    while len(echo) == 0:
        if time.monotonic() - start > 0.2:
            echo.pause()
            return None

    echo.pause()
    duration = echo[0] / 1000000  # Convertir à des secondes
    distance = (duration * 34300) / 2
    return distance


while True:
    print(measure_distance())

    time.sleep(1)
