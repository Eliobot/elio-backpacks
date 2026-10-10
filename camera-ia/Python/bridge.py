# Passerelle Eliobot : relaie la caméra IA (liaison série du port backpack)
# vers l'ordinateur (USB), pour l'atelier d'Elioblocs. Lancée en mémoire par
# l'app, rien n'est écrit sur le robot ; Ctrl+C l'arrête.
# Ordinateur -> robot, en lignes de texte (jamais d'octet 0x03, qui
# interromprait le programme) : « C<texte> » envoie le texte tel quel à la
# caméra, « B<base64> » envoie des octets bruts (le modèle).
import board, busio, usb_cdc, binascii
uart = busio.UART(board.TX, board.RX, baudrate=921600, timeout=0, receiver_buffer_size=32768)
host = usb_cdc.console
buf = bytearray(4096)
view = memoryview(buf)
line = b''
host.write(b'---BRIDGE_READY---')
while True:
    n = uart.readinto(buf)
    if n:
        host.write(view[:n])
    k = host.in_waiting
    if k:
        line += host.read(k)
        while b'\n' in line:
            cmd, line = line.split(b'\n', 1)
            cmd = cmd.strip()
            if cmd[:1] == b'C':
                uart.write(cmd[1:])
            elif cmd[:1] == b'B':
                uart.write(binascii.a2b_base64(cmd[1:]))
