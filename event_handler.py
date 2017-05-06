from sfml import sf
import draw


def check_event(window, event):
    mouse_position = sf.Mouse.get_position(window)

    if type(event) is sf.MouseMoveEvent:
        mouse_position = sf.Mouse.get_position(window)

    if type(event) is sf.MouseButtonEvent:
        if event.pressed and event.button == sf.Mouse.LEFT:
            #print("LEFT press", mouse_position)
            draw.draw_square(window, mouse_position)

        if event.pressed and event.button == sf.Mouse.RIGHT:
            print("RIGHT press", mouse_position)

        if event.released and event.button == sf.Mouse.LEFT:
            print("LEFT released", mouse_position)

        if event.released and event.button == sf.Mouse.RIGHT:
            print("RIGHT press", mouse_position)

    if type(event) is sf.KeyEvent:
        if event.pressed and event.code == sf.Keyboard.X:
            window.close()
            exit()

    if event.type == sf.Event.CLOSED:
        window.close()
        exit()
