# Caméra IA

Backpack caméra d'Eliobot (XIAO ESP32-S3 Sense pour le prototype, puis carte maison sur la même architecture). La caméra reconnaît elle-même les objets appris dans Elioblocs, sans serveur ni connexion : les photos restent sur l'ordinateur et le modèle est écrit directement dans la caméra.

- Firmware de la caméra : [Eliobot/elioblocs-camera-firmware](https://github.com/Eliobot/elioblocs-camera-firmware)
- Apprentissage : Elioblocs, atelier « Apprends à Elio à voir »
- Côté robot : `Python/library/elio_camera.py` (bus I2C de la carte, adresse 0x32)

## Branchement

| XIAO | Eliobot |
| --- | --- |
| D4 (GPIO5, SDA) | SDA (IO8) |
| D5 (GPIO6, SCL) | SCL (IO9) |
| GND | GND |

Alimentation de la XIAO : à documenter d'après le montage de Baptiste (non vérifié).

## Utilisation en Python

```python
from elio_camera import CameraIA

camera = CameraIA()
if camera.sees(0):           # 0 = premier objet appris
    print(camera.x(0))       # 0 à gauche, 100 à droite
```

Voir `Python/example.py` (Elio suit un objet).
