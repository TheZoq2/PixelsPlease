#!/usr/bin/python3
from sfml import sf
import sfml
import event_handler

import time

resolution = (1024, 768)

def main():
    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]), "Pixels please")
    window.clear(sf.Color.BLUE)

    tex = sf.RenderTexture(resolution)

    while True:
        time.sleep(0.001) # If you remove this your computer might freze
        window.display()

        for event in window.events:
            pass
            event_handler.check_event(window, event)

main()
