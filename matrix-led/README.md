### NeoPixel 5x5 LED Matrix Documentation

---

#### 1. **Introduction**

The NeoPixel 5x5 LED matrix is a versatile and colorful display that can be controlled with a single data pin from a microcontroller. Each LED in the matrix is an RGB LED, allowing for millions of color combinations. This matrix is commonly used in creative lighting projects, displays, and interactive installations.

---

#### 2. **Technical Specifications**

- **Number of LEDs**: 25 (5x5 matrix)
- **Operating Voltage**: 3.3V DC
- **Data Protocol**: One-wire communication (WS2812 or WS2812B)
- **Current Draw**: Up to 60mA per LED at full brightness (all LEDs white)
- **Dimensions**: Typically around 50mm x 50mm (varies by manufacturer)
- **Pixel Color Order**: GRB (Green-Red-Blue) or RGB depending on the model

---

#### 3. **Pin Configuration**

The NeoPixel matrix typically has three pins:

- **3.3V**: Power supply (3.3V DC)
- **GND**: Ground
- **DIN**: Data input (connect to the microcontroller)

**Wiring Diagram**:

1. **3.3V** to a 3.3V power supply.
2. **GND** to the ground on your microcontroller.
3. **DIN** to a digital output pin on your microcontroller (e.g., pin 6 on Arduino or any GPIO pin on CircuitPython boards).

---

#### 4. **Using the NeoPixel Matrix with Arduino**

**Installing the Library**:

1. Open the Arduino IDE.
2. Go to **Sketch** > **Include Library** > **Manage Libraries**.
3. Search for "Adafruit NeoPixel" and install it.

**Example Code**:

```cpp
#include <Adafruit_NeoPixel.h>

#define PIN 2        // Pin connected to the DIN of the NeoPixel matrix
#define NUMPIXELS 25 // Number of LEDs in the matrix (5x5)

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin(); // Initialize the NeoPixel library
  pixels.show();  // Initialize all pixels to 'off'
}

void loop() {
  for(int i=0; i<NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(0, 150, 0)); // Set color to green
    pixels.show(); // Update the matrix
    delay(100);
  }

  delay(1000);

  for(int i=0; i<NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(0, 0, 0)); // Turn off all LEDs
  }
  pixels.show();
  delay(1000);
}
```

**Notes**:

- You can change the color by adjusting the `pixels.Color()` function, where the parameters represent the RGB values.
- The `NUMPIXELS` should always match the total number of LEDs in your matrix (25 for a 5x5 matrix).

---

#### 5. **Using the NeoPixel Matrix with CircuitPython**

**Installing the Library**:

1. Ensure you have CircuitPython installed on your board.
2. Install the `Adafruit CircuitPython NeoPixel` library using the Adafruit CircuitPython Library Bundle.

**Example Code**:

```python
import time
import board
import neopixel

# Configure the NeoPixel matrix
pixel_pin = board.IO2
num_pixels = 25
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

def color_wipe(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)

while True:
    color_wipe((255, 0, 0), 0.1)  # Red
    time.sleep(1)
    color_wipe((0, 255, 0), 0.1)  # Green
    time.sleep(1)
    color_wipe((0, 0, 255), 0.1)  # Blue
    time.sleep(1)
```

**Notes**:

- Adjust the `brightness` parameter to control the overall brightness of the matrix.
- The `color_wipe` function sets each pixel to the specified color with a slight delay to create a wiping effect.

---
