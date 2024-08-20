# DHT11 Sensor

The DHT11 backpack is a simple temperature and humidity sensor.

## Python

It needs the adafruit_dht library to work.

This sensor is using the GPIO protocol.

### Usage

Python example:

```python
import board # Import the board module
import adafruit_dht # Import the adafruit_dht module

sensor_dht = adafruit_dht.DHT11(board.IO15) # Create the sensor object

temperature = sensor_dht.temperature # Get the temperature
humidity = sensor_dht.humidity # Get the humidity

print("Temperature: ", temperature, "°C")
print("Humidity: ", humidity, "%")
```