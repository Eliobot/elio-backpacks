# InfraRed Sensor

The InfraRed sensor backpack is already implemented in Eliobot. It is used to detect obstacles in front 
of the robot but it can be used for other purposes like infrared remote control.

## Python

adafruit_irremote library is needed to work with this backpack but it is already installed in Eliobot.

This sensor is using the GPIO protocol.

### Usage

```python
from elio import IRRemote
import board
import pulseio

ir_receiver = pulseio.PulseIn(board.IO4, maxlen=200, idle_state=True)

decoder = IRRemote(ir_receiver)

code = decoder.decode_signal()
```