import board
import pwmio

# Initialize the PWM output
pwm = pwmio.PWMOut(board.IO15, frequency=50)

# Set the servo to 0 degrees
# And back to 90 degrees
while True:
    pwm.duty_cycle =\
        int(((0 / 180.0) * (2750 - 750) + 750)
            * pwm.frequency * 65535 / 1000000)
    pwm.duty_cycle = (
        int(((90 / 180.0) * (2750 - 750) + 750)
            * pwm.frequency * 65535 / 1000000))
