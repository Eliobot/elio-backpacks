### DHT11 Sensor Documentation

---

#### 1. **Introduction**

The DHT11 is a digital temperature and humidity sensor widely used in environmental monitoring projects, IoT devices, and simple electronics projects. It provides readings of temperature and humidity with moderate accuracy and is easy to interface with microcontrollers.

---

#### 2. **Technical Specifications**

- **Temperature Range**: 0 to 50 °C (±2°C accuracy)
- **Humidity Range**: 20% to 90% RH (±5% RH accuracy)
- **Operating Voltage**: 3V to 5.5V
- **Interface**: Digital (single-wire)
- **Response Time**: 1 second
- **Dimensions**: 15.5 mm x 12 mm x 5.5 mm
- **Lifespan**: Over 20,000 measurement cycles

---

#### 3. **Pin Configuration**

The DHT11 sensor typically has four pins:

- **VCC**: Power supply (3V to 5.5V)
- **DATA**: Data output pin
- **NC**: Not connected (ignore this pin)
- **GND**: Ground (0V)

**Wiring Diagram**:

1. **VCC** to 3.3V or 5V power on your microcontroller.
2. **DATA** to a digital input pin on your microcontroller (e.g., pin 2 on Arduino or GPIO on a CircuitPython board).
3. **GND** to ground on your microcontroller.

---

#### 4. **Using the DHT11 with Arduino**

**Installing the Library**:

1. Open the Arduino IDE.
2. Go to **Sketch** > **Include Library** > **Manage Libraries**.
3. Search for "DHT sensor library" and install it.

**Example Code**:

```cpp
#include "DHT.h"

#define DHTPIN 2     // Pin where the DHT11 is connected
#define DHTTYPE DHT11   // Define DHT type as DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);  // Wait 2 seconds between readings

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println(" °C");
}
```

---

#### 5. **Using the DHT11 with CircuitPython**

**Installing the Library**:

1. Ensure you have CircuitPython installed on your board.
2. Install the `Adafruit CircuitPython DHT` library using the Adafruit CircuitPython Library Bundle.

**Example Code**:

```python
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
        # Errors happen fairly often with DHT sensors, just keep trying
        print(f"Error: {error.args[0]}")

    time.sleep(2.0)
```

**Notes**:

- Replace `board.D2` with the appropriate pin used on your CircuitPython board.
- The `time.sleep(2.0)` ensures that the sensor is read only every 2 seconds, which is recommended for reliable readings.

---

#### 6. **Troubleshooting**

- **Incorrect or No Readings**: Double-check the wiring. Ensure the sensor is connected correctly to the power and data pins.
- **Slow Response Time**: Make sure the sensor is placed in a stable environment. Large fluctuations or rapid changes in conditions might affect accuracy.

---

#### 7. **Common Applications**

- Home weather stations
- Humidity control systems
- Home automation projects
- IoT devices for environmental monitoring