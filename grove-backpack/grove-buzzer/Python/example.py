import board
import pwmio
import time

# Init the buzzer
buzzer = pwmio.PWMOut(board.IO15, frequency=340, duty_cycle=0)


def buzz(on_time, off_time):
    """Makes the buzzer sound for a certain amount of time."""
    buzzer.duty_cycle = 65535 // 2  # PWM to 50%
    time.sleep(on_time)
    buzzer.duty_cycle = 0  # Stop PWM
    time.sleep(off_time)


while True:
    buzz(0.2, 0.5)  # Buzz for 0.2s, then wait for 0.5s
