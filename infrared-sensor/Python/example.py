from elio import Motors, IRRemote
import board
import pulseio
import ir_signals
import pwmio

# Initialize the IR receiver
ir_receiver = pulseio.PulseIn(board.IO4, maxlen=200, idle_state=True)

# Initialize the IR decoder
decoder = IRRemote(ir_receiver)

vBatt_pin = analogio.AnalogIn(board.BATTERY)

AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)

# Initialize the motors
motors = Motors(AIN1, AIN2, BIN1, BIN2,vBatt_pin)

distance = 20


while True:
    # Decode the IR signal
    code = decoder.decode_signal()
    # Check if the code is the one we are looking for
    if code == ir_signals.signal_up:
        for i in range(1):
            motors.move_one_step("forward", distance)