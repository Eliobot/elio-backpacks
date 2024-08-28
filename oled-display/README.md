### SSD1306 OLED Display Documentation

---

#### 1. **Introduction**

The SSD1306 is a popular OLED (Organic Light Emitting Diode) display controller used in small monochrome displays, typically with a resolution of 128x64 or 128x32 pixels. These displays are commonly used in various projects due to their low power consumption, high contrast, and ease of integration with microcontrollers.

---

#### 2. **Technical Specifications**

- **Display Technology**: OLED (Organic Light Emitting Diode)
- **Resolution**: 128x64 or 128x32 pixels
- **Color**: Monochrome (usually white, blue, or yellow)
- **Interface**: I2C or SPI (configurable)
- **Operating Voltage**: 3.3V to 5V (varies by module)
- **Controller**: SSD1306
- **Dimensions**: Varies by model (commonly around 27mm x 27mm for 0.96" displays)

---

#### 3. **Pin Configuration**

The SSD1306 OLED display typically has four or more pins depending on the communication protocol used (I2C or SPI):

- **I2C Interface**:
    - **VCC**: Power supply (3.3V or 5V depending on the module)
    - **GND**: Ground
    - **SCL**: Serial Clock Line (connect to I2C clock on microcontroller)
    - **SDA**: Serial Data Line (connect to I2C data on microcontroller)

- **SPI Interface**:
    - **VCC**: Power supply (3.3V or 5V depending on the module)
    - **GND**: Ground
    - **SCK**: Serial Clock (SPI)
    - **MOSI**: Master Out Slave In (SPI data line)
    - **CS**: Chip Select (SPI, selects the display)
    - **DC**: Data/Command (indicates whether data or command is being sent)
    - **RES**: Reset (resets the display)

**Wiring Diagram** (for I2C):

1. **VCC** to 3.3V or 5V on your microcontroller.
2. **GND** to ground on your microcontroller.
3. **SCL** to the I2C clock pin (e.g., A5 on Arduino or SCL on CircuitPython boards).
4. **SDA** to the I2C data pin (e.g., A4 on Arduino or SDA on CircuitPython boards).

---

#### 4. **Using the SSD1306 with Arduino**

**Installing the Library**:

1. Open the Arduino IDE.
2. Go to **Sketch** > **Include Library** > **Manage Libraries**.
3. Search for "Adafruit SSD1306" and install it.
4. Also, install the "Adafruit GFX Library" which provides graphics functions.

**Example Code**:

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for SSD1306 display connected using I2C
#define OLED_RESET    -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  // Initialize the display
  if(!display.begin(SSD1306_I2C_ADDRESS, OLED_RESET)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  display.display();
  delay(2000); // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();

  // Display text
  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(0,0);     // Start at top-left corner
  display.println(F("Hello, world!"));
  
  display.display();
}

void loop() {
  // Main loop code goes here
}
```

**Notes**:

- Adjust the `SSD1306_I2C_ADDRESS` depending on your specific display (usually `0x3C` or `0x3D`).
- The `Adafruit_GFX` library provides functions for drawing shapes, text, and images on the display.

---

#### 5. **Using the SSD1306 with CircuitPython**

**Installing the Library**:

1. Ensure you have CircuitPython installed on your board.
2. Install the `Adafruit CircuitPython SSD1306` and `Adafruit CircuitPython GFX` libraries using the Adafruit CircuitPython Library Bundle.

**Example Code**:

```python
import board
import busio
import adafruit_ssd1306

# Create I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create the display object using I2C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear the display
display.fill(0)
display.show()

# Display text
display.text("Hello, world!", 0, 0, 1)
display.show()
```

**Notes**:

- `display.fill(0)` clears the display.
- The `display.text()` function allows you to print text at specific coordinates on the screen.
- The `show()` function updates the display with the current content of the buffer.

---

#### 6. **Troubleshooting**

- **Display Not Turning On**: Check the wiring, especially the power and ground connections. Ensure that the I2C address in your code matches the one used by your display.
- **Flickering or Noisy Display**: Ensure that your power supply is stable and that the connections are secure. Sometimes adding pull-up resistors to the I2C lines can help stabilize communication.
- **Incorrect Text or Graphics**: Ensure that the correct dimensions (128x64 or 128x32) are set in the code for your specific display.

---

#### 7. **Common Applications**

- Small graphical user interfaces
- Debugging screens for electronics projects
- IoT dashboards
- Clocks and timers
- Sensor data display