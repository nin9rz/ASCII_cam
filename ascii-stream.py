import cv2
import curses
from curses import wrapper


def main(screen):
    # Variables
    scale = 0.2
    contrast = 2
    # Préparer l'écran
    screen.clear()
    # Utiliser la webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open Webcam stream !")
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Sortir de la boucle si la capture échoue

        # Changer la taille de l'image
        frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        width = len(frame[0]) * 2
        # Convertir l'image en nuances de gris
        gscale = []
        for row in frame:
            for pixel in row:
                avg = sum(pixel) // 3
                gscale.extend([avg, avg])
        # Convertir les nuances de gris en ASCII
        chars = ["@", "%", "&", "$", "#", "+", "=", "-", ":", ".", " "]
        chars.reverse()
        ascii_px = [chars[pixel // 25] for pixel in gscale]
        ascii_px = ''.join(ascii_px)
        ascii_frame = [ascii_px[index:index + width] for index in range(0, len(ascii_px), width)]
        # Afficher l'image dans le terminal
        for i, line in enumerate(ascii_frame):
            try:
                screen.addstr(i, 0, line)
            except curses.error:
                pass
        screen.refresh()
    cap.release()

wrapper(main)
