# BME280 Sensor

The BME280 backpack is a temperature, humidity, and pressure sensor.

## Python

It needs the adafruit_bme280 library to work.

This sensor is using the I2C protocol.

### Usage

Python example:

```python
import board # Import the board module
import busio # Import the busio module
from adafruit_bme280 import basic as adafruit_bme280 # Import the adafruit_bme280 module

i2c = busio.I2C(board.IO9, board.IO8) # Create the I2C object

bme_sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76) # Create the sensor object

temperature = bme_sensor.temperature # Get the temperature
humidity = bme_sensor.humidity # Get the humidity
pressure = bme_sensor.pressure # Get the pressure

print("Temperature: ", temperature, "°C")
print("Humidity: ", humidity, "%")
print("Pressure: ", pressure, "hPa")
```
