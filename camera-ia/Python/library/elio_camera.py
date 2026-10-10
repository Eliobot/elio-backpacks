# Caméra IA d'Eliobot : lit ce que voit la caméra (XIAO ESP32-S3 Sense,
# firmware elioblocs-camera-firmware 2.1 ou plus) sur la liaison série du port
# backpack (TX = IO43, RX = IO44, 460 800 bauds).
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

camera_version = '2.0.0'

BAUDRATE = 460800
SYNC = b'\xa5\x5a\xe1'
PACKET_SIZE = 32
MAX_DETECTIONS = 7
# Sans paquet depuis ce délai, la caméra est considérée muette : plus rien n'est vu.
STALE_SECONDS = 0.6


class CameraIA:
    def __init__(self, uart=None, min_score=50):
        self.uart = uart if uart is not None else busio.UART(
            board.TX, board.RX, baudrate=BAUDRATE, timeout=0, receiver_buffer_size=1024)
        self.min_score = min_score
        self._buf = b''
        self._detections = []
        self._frame = None
        self._got_at = None
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
        if self._got_at is None or time.monotonic() - self._got_at > STALE_SECONDS:
            self._detections = []
        return self._detections

    def connected(self):
        """True si la caméra a envoyé un paquet récemment."""
        self.update()
        return self._got_at is not None and time.monotonic() - self._got_at <= STALE_SECONDS

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
