### Servo Motor Documentation

---

#### 1. **Introduction**

A servo motor is a type of motor that can rotate to a specific angle with precision, typically controlled by a PWM (Pulse Width Modulation) signal. Servo motors are widely used in robotics, RC vehicles, and automated systems where precise movement is required. Unlike regular DC motors, servo motors are designed to move to and hold a particular position.

---

#### 2. **Technical Specifications**

- **Operating Voltage**: Typically 4.8V to 5V
- **Control Signal**: PWM (Pulse Width Modulation)
- **Rotation Range**: Usually 0° to 180°
- **Speed**: Time taken to rotate 60° (e.g., 0.1 sec/60° at 5V)
- **Connector**: Typically three wires (Power, Ground, Signal)

---

#### 3. **Pin Configuration**

Servo motors generally have three wires:

- **Red**: Power supply (usually 5V)
- **Brown/Black**: Ground (0V)
- **Orange/White/Yellow**: Control signal (PWM input)

**Wiring Diagram**:

1. **Red wire** to 5V on your microcontroller or an external power source.
2. **Black/Brown wire** to Ground (GND) on your microcontroller.
3. **Orange/White/Yellow wire** to a PWM-capable digital pin on your microcontroller (e.g., pin 9 on Arduino or any PWM pin on CircuitPython boards).

---

#### 4. **Using the Servo Motor with Arduino**

**Installing the Library**:

1. Open the Arduino IDE.
2. Go to **Sketch** > **Include Library** > **Manage Libraries**.
3. Search for "Servo" and install it (usually pre-installed with the Arduino IDE).

**Example Code**:

```cpp
#include <Servo.h>

Servo myservo;  // Create servo object to control a servo

int pos = 0;    // Variable to store the servo position

void setup() {
  myservo.attach(9);  // Attaches the servo on pin 9 to the servo object
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1) { // Goes from 0 degrees to 180 degrees
    myservo.write(pos);              // Tell servo to go to position in variable 'pos'
    delay(15);                       // Waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // Goes from 180 degrees to 0 degrees
    myservo.write(pos);              // Tell servo to go to position in variable 'pos'
    delay(15);                       // Waits 15ms for the servo to reach the position
  }
}
```

**Notes**:

- The `myservo.attach(9)` function attaches the servo to pin 9.
- The `myservo.write(pos)` function sets the position of the servo from 0° to 180°.

---

#### 5. **Using the Servo Motor with CircuitPython**

**Example Code**:

```python
import time
import board
import pulseio
from adafruit_motor import servo

# Create a PWMOut object on the control pin.
pwm = pulseio.PWMOut(board.D9, frequency=50)

# Create a servo object
my_servo = servo.Servo(pwm)

while True:
    # Sweep the servo from 0° to 180°
    for angle in range(0, 180):
        my_servo.angle = angle
        time.sleep(0.01)

    # Sweep the servo from 180° to 0°
    for angle in range(180, 0, -1):
        my_servo.angle = angle
        time.sleep(0.01)
```

**Notes**:

- Replace `board.D9` with the correct PWM pin on your CircuitPython board.
- The `my_servo.angle` controls the position of the servo, where `0` represents 0° and `180` represents 180°.

---

#### 6. **Troubleshooting**

- **Servo Not Moving**: Ensure that the power supply is adequate. Check that the PWM signal is being sent to the correct pin.
- **Jittery or Unstable Movement**: Verify that the power supply is stable and that the servo is not overloaded.
- **Limited Movement Range**: Ensure that the PWM signal is correctly configured, and verify that the servo motor is not physically obstructed.

---

#### 7. **Common Applications**

- Robotics (e.g., robotic arms, legs)
- Remote-controlled vehicles (e.g., steering, throttle control)
- Automated systems (e.g., door openers, control surfaces)
- Pan-and-tilt camera systems
- Animatronics
