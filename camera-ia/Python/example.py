# Elio suit l'objet n° 1 appris dans l'atelier caméra d'Elioblocs.
from elio import Motors
from elio_camera import CameraIA
import analogio
import board
import pwmio
import time

vBatt_pin = analogio.AnalogIn(board.BATTERY)
motors = Motors(pwmio.PWMOut(board.IO36), pwmio.PWMOut(board.IO38),
                pwmio.PWMOut(board.IO35), pwmio.PWMOut(board.IO37), vBatt_pin)
camera = CameraIA()

try:
    while True:
        if camera.sees(0):
            x = camera.x(0)
            if x < 35:
                motors.turn_left(20)
            elif x > 65:
                motors.turn_right(20)
            else:
                motors.motor_stop()
        else:
            motors.motor_stop()
        time.sleep(0.1)
finally:
    # Les moteurs s'arrêtent même si le programme plante.
    motors.motor_stop()
