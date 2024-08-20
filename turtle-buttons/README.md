# Turtle Buttons

This backpack has seven buttons that can be used to control eliobot or any othe function you want.

## Python

No special library is needed to work with this backpack.

This backpack is using the GPIO protocol.

### Usage

Python example:

```python
import board # Import the board module
import digitalio # Import the digitalio module

buttonForward = digitalio.DigitalInOut(board.IO15)
buttonBackward = digitalio.DigitalInOut(board.IO2)
buttonRight = digitalio.DigitalInOut(board.IO16)
buttonLeft = digitalio.DigitalInOut(board.IO42)
buttonStart = digitalio.DigitalInOut(board.IO39)
buttonStop = digitalio.DigitalInOut(board.IO41)
buttonRepeat = digitalio.DigitalInOut(board.IO40)

buttonForward.direction = digitalio.Direction.INPUT
buttonBackward.direction = digitalio.Direction.INPUT
buttonRight.direction = digitalio.Direction.INPUT
buttonLeft.direction = digitalio.Direction.INPUT
buttonStart.direction = digitalio.Direction.INPUT
buttonStop.direction = digitalio.Direction.INPUT
buttonRepeat.direction = digitalio.Direction.INPUT

buttonForward.pull = digitalio.Pull.UP
buttonBackward.pull = digitalio.Pull.UP
buttonRight.pull = digitalio.Pull.UP
buttonLeft.pull = digitalio.Pull.UP
buttonStart.pull = digitalio.Pull.UP
buttonStop.pull = digitalio.Pull.UP
buttonRepeat.pull = digitalio.Pull.UP

while True:
    if not buttonForward.value:
        print("Forward")
    if not buttonBackward.value:
        print("Backward")
    if not buttonRight.value:
        print("Right")
    if not buttonLeft.value:
        print("Left")
    if not buttonStart.value:
        print("Start")
    if not buttonStop.value:
        print("Stop")
    if not buttonRepeat.value:
        print("Repeat")
```

Simple program that reads the state of the buttons and prints the name of the button that is pressed.