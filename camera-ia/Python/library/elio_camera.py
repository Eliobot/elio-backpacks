# Caméra IA d'Eliobot : lit ce que voit la caméra (XIAO ESP32-S3 Sense,
# firmware elioblocs-camera-firmware 2.1 ou plus) sur la liaison série du port
# backpack (TX = IO43, RX = IO44, 921 600 bauds).
#
# La caméra détecte elle-même les objets appris dans Elioblocs (atelier
# « Apprends à Elio à voir ») et envoie après chaque image, précédé de A5 5A,
# un paquet de 32 octets :
#   [0]      0xE1 (signature)
#   [1]      nombre de détections (0 à 7)
#   [2..29]  7 x (x, y, confiance, objet), x et y de 0 à 100, confiance de 0 à 100
#   [30]     compteur d'images
#   [31]     somme des 31 octets précédents, modulo 256
#
# Exemple :
#   from elio_camera import CameraIA
#   camera = CameraIA()
#   if camera.sees(0):
#       print(camera.x(0))

import time
import board
import busio

camera_version = '2.1.0'

BAUDRATE = 921600
SYNC = b'\xa5\x5a\xe1'
PACKET_SIZE = 32
MAX_DETECTIONS = 7
# Sans paquet depuis ce délai, la caméra est considérée muette : plus rien n'est vu.
STALE_SECONDS = 0.6
# Un objet reste « vu » ce temps après sa dernière détection : la caméra en fait
# environ 4 par seconde, et une seule image ratée ne doit pas arrêter Elio net.
HOLD_SECONDS = 0.5
# Zones de l'image (position horizontale, 0 à 100), les mêmes que le livret IA.
LEFT_LIMIT = 35
RIGHT_LIMIT = 65


class CameraIA:
    def __init__(self, uart=None, min_score=50):
        self.uart = uart if uart is not None else busio.UART(
            board.TX, board.RX, baudrate=BAUDRATE, timeout=0, receiver_buffer_size=1024)
        self.min_score = min_score
        self._buf = b''
        self._detections = []
        self._frame = None
        self._got_at = None
        self._last = {}  # objet -> (meilleure détection, heure), pour HOLD_SECONDS
        # La vidéo n'est utile qu'à l'atelier : on la coupe si elle était restée active.
        self.uart.write(b'v')

    def _parse(self):
        """Garde le dernier paquet complet et valide du tampon."""
        buf = self._buf
        found = None
        start = 0
        while True:
            i = buf.find(SYNC, start)
            if i < 0 or i + 2 + PACKET_SIZE > len(buf):
                break
            p = buf[i + 2:i + 2 + PACKET_SIZE]
            if p[1] <= MAX_DETECTIONS and sum(p[0:31]) & 0xFF == p[31]:
                found = p
                start = i + 2 + PACKET_SIZE
            else:
                start = i + 1
        # On ne garde que la fin, qui peut contenir un paquet incomplet.
        self._buf = buf[-(PACKET_SIZE + 2):] if found is None else buf[start:]
        return found

    def update(self):
        """Lit ce qui est arrivé et renvoie la liste des détections."""
        n = self.uart.in_waiting
        if n:
            self._buf += self.uart.read(n)
            if len(self._buf) > 4096:
                self._buf = self._buf[-512:]
            p = self._parse()
            if p is not None:
                self._detections = [{
                    'x': p[2 + i * 4],
                    'y': p[3 + i * 4],
                    'score': p[4 + i * 4],
                    'object': p[5 + i * 4],
                } for i in range(p[1])]
                self._frame = p[30]
                self._got_at = time.monotonic()
                best = {}
                for d in self._detections:
                    o = d['object']
                    # Sous le seuil, l'image ne compte pas : l'objet garde sa
                    # dernière vraie détection pendant HOLD_SECONDS.
                    if d['score'] < self.min_score:
                        continue
                    if o not in best or d['score'] > best[o]['score']:
                        best[o] = d
                for o, d in best.items():
                    self._last[o] = (d, self._got_at)
        if self._got_at is None or time.monotonic() - self._got_at > STALE_SECONDS:
            self._detections = []
        return self._detections

    def connected(self):
        """True si la caméra a envoyé un paquet récemment."""
        self.update()
        return self._got_at is not None and time.monotonic() - self._got_at <= STALE_SECONDS

    def _best(self, object_id):
        """Dernière détection de l'objet si elle date de moins de HOLD_SECONDS."""
        self.update()
        held = self._last.get(object_id)
        if held is None or self._got_at is None:
            return None
        d, at = held
        if time.monotonic() - at > HOLD_SECONDS or d['score'] < self.min_score:
            return None
        return d

    def sees(self, object_id):
        """Elio voit-il l'objet (0 = le premier appris) ?"""
        return self._best(object_id) is not None

    def x(self, object_id):
        """Position horizontale de l'objet : 0 à gauche, 100 à droite, -1 s'il n'est pas vu."""
        d = self._best(object_id)
        return d['x'] if d else -1

    def y(self, object_id):
        """Position verticale de l'objet : 0 en haut, 100 en bas, -1 s'il n'est pas vu."""
        d = self._best(object_id)
        return d['y'] if d else -1

    def score(self, object_id):
        """Confiance de la caméra pour cet objet, de 0 à 100 (0 s'il n'est pas vu)."""
        d = self._best(object_id)
        return d['score'] if d else 0

    def count(self, object_id=None):
        """Nombre d'objets vus sur la dernière image (d'un seul type si object_id est donné).
        Deux objets qui se touchent peuvent compter pour un."""
        return len([
            d for d in self.update()
            if d['score'] >= self.min_score and (object_id is None or d['object'] == object_id)
        ])

    def zone(self, object_id):
        """'left', 'center' ou 'right' selon la position horizontale ; None si l'objet n'est pas vu."""
        d = self._best(object_id)
        if d is None:
            return None
        if d['x'] < LEFT_LIMIT:
            return 'left'
        if d['x'] > RIGHT_LIMIT:
            return 'right'
        return 'center'

    def is_at(self, object_id, where):
        """L'objet est-il dans cette zone ('left', 'center' ou 'right') ?"""
        return self.zone(object_id) == where

    def wait_for(self, object_id):
        """Attend qu'Elio voie l'objet."""
        while not self.sees(object_id):
            time.sleep(0.02)

    def set_min_score(self, value):
        """Confiance minimale (0 à 100) pour qu'un objet compte comme vu. 50 au départ."""
        self.min_score = max(0, min(100, int(value)))

    def _wait_new_image(self, images=2, timeout=1.0):
        """Attend des détections faites après cet appel (la première peut dater d'avant)."""
        end = time.monotonic() + timeout
        seen = 0
        frame = self._frame
        while seen < images and time.monotonic() < end:
            self.update()
            if self._frame != frame:
                frame = self._frame
                seen += 1
            time.sleep(0.01)

    def turn_toward(self, object_id, motors, speed=40, timeout=5):
        """Pivote par petits pas jusqu'à avoir l'objet au centre de l'image.
        Après chaque pas, Elio attend une image prise à l'arrêt : en pivotant
        sans s'arrêter, il dépasserait l'objet. Renvoie True si l'objet est au
        centre, False s'il n'est plus vu ou au bout de timeout secondes."""
        end = time.monotonic() + timeout
        try:
            while time.monotonic() < end:
                d = self._best(object_id)
                if d is None:
                    return False
                if LEFT_LIMIT <= d['x'] <= RIGHT_LIMIT:
                    return True
                # Pas plus long quand l'objet est loin du centre.
                step = 0.04 + abs(d['x'] - 50) * 0.002
                if d['x'] < LEFT_LIMIT:
                    motors.turn_left(speed)
                else:
                    motors.turn_right(speed)
                time.sleep(step)
                motors.motor_stop()
                self._wait_new_image()
            return False
        finally:
            motors.motor_stop()
