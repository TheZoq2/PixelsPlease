from sfml import sf;
import sfml;

import time

def main():
    window = sf.RenderWindow(sf.VideoMode(640, 480), "Pixels please")
    window.clear(sf.Color.BLUE)

    while True:
        time.sleep(0.001) # If you remove this your computer might freze
        window.display()

        for event in window.events:
            pass
        window.close()
        exit()
            #if type(event) is sf.CloseEvent:
                #window.close()

main()
