import time
import board
import adafruit_dht

# Initialize the DHT11 sensor
dht11 = adafruit_dht.DHT11(board.D2)

while True:
    try:
        temperature = dht11.temperature
        humidity = dht11.humidity

        print(f"Temp: {temperature} °C    Humidity: {humidity} %")

    except RuntimeError as error:
        # Errors happen fairly often with DHT sensors, keep trying
        print(f"Error: {error.args[0]}")

    time.sleep(2.0)