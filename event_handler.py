from sfml import sf
import draw

def check_event(window, event, state, current_page):
    mouse_position = sf.Mouse.get_position(window)

    if type(event) is sf.MouseMoveEvent:
        if sf.Mouse.is_button_pressed(sf.Mouse.LEFT):
            mouse_position = sf.Mouse.get_position(window)
            draw.censor(state.censor_textures[current_page], mouse_position)

        elif sf.Mouse.is_button_pressed(sf.Mouse.RIGHT):
            mouse_position = sf.Mouse.get_position(window)
            draw.uncensor(state.censor_textures[current_page], mouse_position)


    if type(event) is sf.MouseButtonEvent:
        if event.pressed and event.button == sf.Mouse.LEFT:
            draw.censor(state.censor_textures[current_page], mouse_position)

        if event.pressed and event.button == sf.Mouse.RIGHT:
            draw.uncensor(state.censor_textures[current_page], mouse_position)

        if event.released and event.button == sf.Mouse.LEFT:
            pass

        if event.released and event.button == sf.Mouse.RIGHT:
            pass

    if type(event) is sf.ResizeEvent:
        print("Fuck")
        window.setView(sf.View(sf.FloatRect(0, 0, event.size.width, event.size.height)));

    if type(event) is sf.KeyEvent:
        if event.pressed and event.code == sf.Keyboard.X:
            window.close()
            exit()
        if event.pressed and event.code == sf.Keyboard.RETURN:
            return "END"

        if event.pressed and event.code == sf.Keyboard.P:
            if state.music_silenced:
                state.work_music.volume = 100
                state.score_music.volume = 100
                state.music_silenced = False

            elif not state.music_silenced:
                state.work_music.volume = 0
                state.score_music.volume = 0
                state.music_silenced = True

    if type(event) is sf.CloseEvent:
        window.close()
        exit()
