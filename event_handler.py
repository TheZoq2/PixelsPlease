from sfml import sf
import draw

def check_event(window, event, censor_texture):
    mouse_position = sf.Mouse.get_position(window)

    if type(event) is sf.MouseMoveEvent:
        if sf.Mouse.is_button_pressed(sf.Mouse.LEFT):
            mouse_position = sf.Mouse.get_position(window)
            draw.censor(censor_texture, mouse_position)

        elif sf.Mouse.is_button_pressed(sf.Mouse.RIGHT):
            mouse_position = sf.Mouse.get_position(window)
            draw.uncensor(censor_texture, mouse_position)

    if type(event) is sf.MouseButtonEvent:
        if event.pressed and event.button == sf.Mouse.LEFT:
            draw.censor(censor_texture, mouse_position)

        if event.pressed and event.button == sf.Mouse.RIGHT:
            draw.uncensor(censor_texture, mouse_position)

        if event.released and event.button == sf.Mouse.LEFT:
            pass

        if event.released and event.button == sf.Mouse.RIGHT:
            pass

    if type(event) is sf.KeyEvent:
        if event.pressed and event.code == sf.Keyboard.X:
            window.close()
            exit()
        if event.pressed and event.code == sf.Keyboard.RETURN:
            return "END"


    if type(event) is sf.CloseEvent:
        window.close()
        exit()
