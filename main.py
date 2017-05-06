#!/usr/bin/python3
from sfml import sf
import sfml
import event_handler

import time

resolution = (1024, 768)

def main():
    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]), "Pixels please")
    #window.clear(sf.Color.BLUE)

    censor_texture = sf.RenderTexture(resolution[0], resolution[1])
    censor_texture.clear(sf.Color.TRANSPARENT)
    censor_texture_sprite = sf.Sprite(censor_texture.texture)

    rekt = sf.RectangleShape();
    rekt.size = resolution
    rekt.fill_color = sf.Color(255, 0, 0)

    shader = sf.Shader.from_file("media/shaders/censor.vert", "media/shaders/censor.frag")

    while True:
        #time.sleep(0.001) # If you remove this your computer might freze


        censor_texture.display()
        window.draw(rekt)
        window.draw(censor_texture_sprite, sf.RenderStates(shader=shader))

        window.display()

        for event in window.events:
            event_handler.check_event(window, event, censor_texture)

main()
