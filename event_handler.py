from sfml import sf
import draw

def set_showing_notes(state, is_viewing):
    state.is_viewing_notes = is_viewing

    if is_viewing:
        pass

def check_event(window, event, state, current_page):
    mouse_position = sf.Mouse.get_position(window)

    if type(event) is sf.MouseMoveEvent:
        if not state.is_viewing_notes:
            if sf.Mouse.is_button_pressed(sf.Mouse.LEFT):
                mouse_position = sf.Mouse.get_position(window)
                draw.censor(state.censor_textures[current_page], mouse_position)

            elif sf.Mouse.is_button_pressed(sf.Mouse.RIGHT):
                mouse_position = sf.Mouse.get_position(window)
                draw.uncensor(state.censor_textures[current_page], mouse_position)


    if type(event) is sf.MouseButtonEvent:
        if not state.is_viewing_notes:
            if event.pressed and event.button == sf.Mouse.LEFT:
                draw.censor(state.censor_textures[current_page], mouse_position)

            if event.pressed and event.button == sf.Mouse.RIGHT:
                draw.uncensor(state.censor_textures[current_page], mouse_position)

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

        if event.pressed and event.code == sf.Keyboard.P:
            if state.music_silenced:
                state.work_music.volume = 100
                state.score_music.volume = 100
                state.music_silenced = False

            elif not state.music_silenced:
                state.work_music.volume = 0
                state.score_music.volume = 0
                state.music_silenced = True

        if event.pressed and event.code == sf.Keyboard.C:
            state.censor_textures[current_page].clear(sf.Color.WHITE)
            print("clear the censored areas")

        if event.pressed and event.code == sf.Keyboard.N:
            state.is_viewing_notes = not state.is_viewing_notes

        if event.pressed and event.code == sf.Keyboard.ESCAPE:
            state.is_viewing_notes = False

    if type(event) is sf.CloseEvent:
        window.close()
        exit()
