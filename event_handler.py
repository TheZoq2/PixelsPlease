from sfml import sf

def check_event(event, window):
    if type(event) is sf.MouseButtonEvent:
        if event.pressed and event.button == sf.Mouse.LEFT:
            print("LEFT")
        if event.pressed and event.button == sf.Mouse.RIGHT:
            print("RIGHT")

    if type(event) is sf.KeyEvent:
        if event.pressed and event.code == sf.Keyboard.X:
            window.close()
            exit()

    if type(event) is sf.CloseEvent:
        window.close()
        exit()
