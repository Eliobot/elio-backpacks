### BME280 Sensor Documentation

---

#### 1. **Introduction**

The BME280 is a high-precision sensor that measures temperature, humidity, and atmospheric pressure. It is commonly used in environmental monitoring, weather stations, and IoT projects due to its accuracy and reliability. The sensor communicates using either I2C or SPI interface, making it versatile for integration with various microcontrollers.

---

#### 2. **Technical Specifications**

- **Temperature Range**: -40 to 85 °C (±1.0°C accuracy)
- **Humidity Range**: 0% to 100% RH (±3% RH accuracy)
- **Pressure Range**: 300 to 1100 hPa (±1 hPa accuracy)
- **Operating Voltage**: 1.8V to 3.6V
- **Interface**: I2C (default) or SPI
- **Dimensions**: 2.5 mm x 2.5 mm x 0.93 mm
- **Power Consumption**: 0.1 µA in sleep mode, 1.8 µA at 1 Hz sampling

---

#### 3. **Pin Configuration**

The BME280 sensor typically has four or six pins, depending on the breakout board:

- **VIN**: Power supply (3.3V)
- **GND**: Ground (0V)
- **SCL (or SCK)**: Clock line for I2C (or SPI)
- **SDA (or SDI)**: Data line for I2C (or SPI data input)
- **CS**: Chip select (for SPI, usually tied to GND for I2C)
- **SDO**: SPI data output (can be used to set I2C address)

**Wiring Diagram**:

1. **VIN** to 3.3V power on your microcontroller.
2. **GND** to ground on your microcontroller.
3. **SCL** to the I2C clock pin on your microcontroller (e.g., A5 on Arduino or SCL on CircuitPython boards).
4. **SDA** to the I2C data pin on your microcontroller (e.g., A4 on Arduino or SDA on CircuitPython boards).

---

#### 4. **Using the BME280 with Arduino**

**Installing the Library**:

1. Open the Arduino IDE.
2. Go to **Sketch** > **Include Library** > **Manage Libraries**.
3. Search for "Adafruit BME280" and install it.

**Example Code**:

```cpp
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme;  // Use I2C interface

void setup() {
  Serial.begin(9600);
  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
}

void loop() {
  Serial.print("Temperature = ");
  Serial.print(bme.readTemperature());
  Serial.println(" °C");

  Serial.print("Pressure = ");
  Serial.print(bme.readPressure() / 100.0F);
  Serial.println(" hPa");

  Serial.print("Humidity = ");
  Serial.print(bme.readHumidity());
  Serial.println(" %");

  Serial.println();
  delay(2000);
}
```

---

#### 5. **Using the BME280 with CircuitPython**

**Installing the Library**:

1. Ensure you have CircuitPython installed on your board.
2. Install the `Adafruit CircuitPython BME280` library using the Adafruit CircuitPython Library Bundle.

**Example Code**:

```python
import time
import board
import adafruit_bme280

# Initialize the BME280 sensor
i2c = board.I2C()  # Uses board's default I2C pins
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Optionally, set the sea level pressure at your location
bme280.sea_level_pressure = 1013.25

while True:
    print(f"Temperature: {bme280.temperature:.1f} °C")
    print(f"Humidity: {bme280.humidity:.1f} %")
    print(f"Pressure: {bme280.pressure:.1f} hPa")
    print(f"Altitude: {bme280.altitude:.2f} meters")

    time.sleep(2.0)
```

**Notes**:

- Replace `board.I2C()` with the appropriate I2C setup if necessary.
- The `sea_level_pressure` variable can be adjusted based on your location for more accurate altitude readings.

---

#### 6. **Troubleshooting**

- **Sensor Not Detected**: Ensure the sensor is properly connected, and check that the I2C address (usually `0x76` or `0x77`) matches the one defined in your code.
- **Inaccurate Readings**: Verify the sensor is in a stable environment, and consider calibrating the sea level pressure if using altitude measurements.

---

#### 7. **Common Applications**

- Weather stations
- Environmental monitoring
- Altimeters
- IoT devices for climate and air quality monitoring