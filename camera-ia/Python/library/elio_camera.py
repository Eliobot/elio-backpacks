# Caméra IA d'Eliobot : lit ce que voit la caméra (XIAO ESP32-S3 Sense,
# firmware elioblocs-camera-firmware) sur le bus I2C du robot.
#
# La caméra détecte elle-même les objets appris dans Elioblocs (atelier
# « Apprends à Elio à voir ») et publie, à l'adresse 0x32, un paquet de
# 32 octets :
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

camera_version = '1.0.0'

ADDRESS = 0x32
MAGIC = 0xE1
PACKET_SIZE = 32
MAX_DETECTIONS = 7
# En dessous de ce délai, on réutilise la dernière lecture : un programme qui
# demande « voit-il ? » puis « où ? » parle de la même image.
CACHE_SECONDS = 0.05


class CameraIA:
    def __init__(self, i2c=None, address=ADDRESS, min_score=50):
        # Bus I2C partagé de la carte (IO8/IO9), comme les autres backpacks.
        self.i2c = i2c if i2c is not None else board.I2C()
        self.address = address
        self.min_score = min_score
        self._buffer = bytearray(PACKET_SIZE)
        self._detections = []
        self._frame = None
        self._read_at = None

    def _read_packet(self):
        """Lit un paquet valide (3 essais) ; None si la caméra ne répond pas."""
        for _ in range(3):
            if not self.i2c.try_lock():
                time.sleep(0.002)
                continue
            try:
                self.i2c.readfrom_into(self.address, self._buffer)
            except OSError:
                continue
            finally:
                self.i2c.unlock()
            b = self._buffer
            if b[0] == MAGIC and b[1] <= MAX_DETECTIONS and sum(b[0:31]) & 0xFF == b[31]:
                return b
            time.sleep(0.002)
        return None

    def update(self):
        """Relit la caméra. Renvoie la liste des détections."""
        now = time.monotonic()
        if self._read_at is not None and now - self._read_at < CACHE_SECONDS:
            return self._detections
        packet = self._read_packet()
        self._read_at = now
        if packet is None:
            # Paquet abîmé ou caméra muette : on garde la dernière bonne image,
            # sauf si elle date (l'objet a pu disparaître).
            return self._detections
        detections = []
        for i in range(packet[1]):
            o = 2 + i * 4
            detections.append({
                'x': packet[o],
                'y': packet[o + 1],
                'score': packet[o + 2],
                'object': packet[o + 3],
            })
        self._detections = detections
        self._frame = packet[30]
        return detections

    def connected(self):
        """True si la caméra répond sur le bus."""
        return self._read_packet() is not None

    def _best(self, object_id):
        best = None
        for d in self.update():
            if d['object'] == object_id and d['score'] >= self.min_score:
                if best is None or d['score'] > best['score']:
                    best = d
        return best

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
        """Nombre d'objets vus (d'un seul type si object_id est donné)."""
        return len([
            d for d in self.update()
            if d['score'] >= self.min_score and (object_id is None or d['object'] == object_id)
        ])
