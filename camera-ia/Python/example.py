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
        # Pivote par petits pas jusqu'à avoir l'objet au centre de l'image.
        camera.turn_toward(0, motors)
        time.sleep(0.1)
finally:
    # Les moteurs s'arrêtent même si le programme plante.
    motors.motor_stop()
