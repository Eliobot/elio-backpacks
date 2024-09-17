import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
from docutils.nodes import address

# Create library object using our Bus I2C port
I2C = busio.I2C(board.IO9, board.IO8)

bme280_sensor = adafruit_bme280.Adafruit_BME280_I2C(I2C, address=0x76)

# You can define the sea level pressure to get better results
# bme280_sensor.sea_level_pressure = 1013.25

while True:

    print("\nTemperature: %0.1f C" % bme280_sensor.temperature)
    print("Humidity: %0.1f %%" % bme280_sensor.relative_humidity)
    print("Pressure: %0.1f hPa" % bme280_sensor.pressure)
    print("Altitude = %0.2f meters" % bme280_sensor.altitude)

    time.sleep(1)
