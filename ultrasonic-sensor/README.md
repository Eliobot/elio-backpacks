### Ultrasonic Sensor Documentation

---

#### 1. **Introduction**

An ultrasonic sensor is a device that uses sound waves to measure the distance to an object. It emits a sound wave at a specific frequency (typically 40 kHz), then listens for the sound wave to bounce back. By calculating the time it takes for the echo to return, the sensor can determine the distance to the object. Ultrasonic sensors are commonly used in robotics, automation, and obstacle detection.

---

#### 2. **Technical Specifications**

- **Operating Voltage**: 5V DC
- **Operating Current**: 15mA
- **Frequency**: 40 kHz
- **Max Range**: Typically 4 meters
- **Min Range**: Typically 2 cm
- **Measurement Angle**: 15 degrees
- **Dimensions**: Varies by model (e.g., HC-SR04: 45mm x 20mm x 15mm)

---

#### 3. **Pin Configuration**

A typical ultrasonic sensor, such as the HC-SR04, has four pins:

- **VCC**: Power supply (5V DC)
- **Trig**: Trigger pin (sends out the sound wave)
- **Echo**: Echo pin (receives the reflected sound wave)
- **GND**: Ground

**Wiring Diagram**:

1. **VCC** to 5V on your microcontroller.
2. **GND** to Ground on your microcontroller.
3. **Trig** to a digital output pin on your microcontroller (e.g., pin 9 on Arduino or any GPIO pin on CircuitPython boards).
4. **Echo** to a digital input pin on your microcontroller (e.g., pin 10 on Arduino or any GPIO pin on CircuitPython boards).

---

#### 4. **Using the Ultrasonic Sensor with Arduino**

**Example Code**:

```cpp
#define TRIG_PIN 9
#define ECHO_PIN 10

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // Clear the trigPin by setting it LOW:
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Trigger the sensor by setting it HIGH for 10 microseconds:
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read the echoPin. pulseIn() returns the duration (in microseconds) of the pulse:
  long duration = pulseIn(ECHO_PIN, HIGH);

  // Calculate the distance (speed of sound is ~343 meters per second):
  long distance = duration * 0.034 / 2;

  // Print the distance on the Serial Monitor:
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(500);
}
```

**Notes**:

- The `pulseIn()` function measures the time the Echo pin stays HIGH, which corresponds to the time taken by the sound wave to return.
- The distance calculation formula is based on the speed of sound in air (343 meters per second).

---

#### 5. **Using the Ultrasonic Sensor with CircuitPython**

**Example Code**:

```python
import time
import board
import digitalio

# Set up pins
trig = digitalio.DigitalInOut(board.D9)
trig.direction = digitalio.Direction.OUTPUT
echo = digitalio.DigitalInOut(board.D10)
echo.direction = digitalio.Direction.INPUT

def measure_distance():
    # Send a 10us pulse to trigger
    trig.value = True
    time.sleep(0.00001)
    trig.value = False

    # Measure how long the echo pin stays high
    while echo.value == False:
        start = time.time()

    while echo.value == True:
        end = time.time()

    duration = end - start
    distance = (duration * 34300) / 2  # Speed of sound is 34300 cm/s
    return distance

while True:
    distance = measure_distance()
    print(f"Distance: {distance:.2f} cm")
    time.sleep(0.5)
```

**Notes**:

- The `measure_distance()` function sends a pulse and measures the time taken for the echo to return.
- The speed of sound is used to calculate the distance in centimeters.

---

#### 6. **Troubleshooting**

- **No Distance Reading**: Ensure that the sensor is properly connected, with the correct pins used for Trig and Echo.
- **Inconsistent Readings**: Verify that the sensor is not too close to or too far from the object. Ensure there are no obstructions that could interfere with the sound wave.
- **Incorrect Distance**: Double-check the timing calculations in the code and ensure the sensor is calibrated correctly for the environment (temperature, humidity can affect sound speed).

---

#### 7. **Common Applications**

- Obstacle avoidance in robots
- Distance measurement for automation systems
- Parking assistance systems
- Liquid level measurement
- Proximity sensors in security systems
