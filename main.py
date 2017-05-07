#!/usr/bin/python3
from sfml import sf
import event_handler
import image_handler
from models import Article, Page, Day
import generator
from state import State

resolution = (1024, 768)

def title_screen(window, music):
    title_texture = sf.Texture.from_file("media/images/Letter.png")
    title_sprite = sf.Sprite(title_texture)

    continue_button_texture = sf.Texture.from_file("media/images/continue_button.png")
    continue_button_sprite = sf.Sprite(continue_button_texture)
    continue_button_size = (100, 50)
    continue_button_position = (resolution[0] - continue_button_size[0] - 10, \
                                resolution[1] - continue_button_size[1] - 10)
    continue_button_sprite.position = (continue_button_position[0], continue_button_position[1])


    music.play()

    while True:
        window.draw(title_sprite)
        window.draw(continue_button_sprite)
        window.display()


        for event in window.events:
            if isinstance(event, sf.KeyEvent):
                if event.pressed and event.code == sf.Keyboard.X:
                    window.close()
                    exit()
                if event.pressed and event.code == sf.Keyboard.RETURN:
                    music.stop()
                    return

            if isinstance(event, sf.MouseButtonEvent):
                if event.pressed and event.button == sf.Mouse.LEFT:
                    mouse_position = sf.Mouse.get_position(window)

                    if continue_button_sprite.global_bounds.contains(mouse_position):
                        music.stop()
                        return


def main():
    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]),
                             "Pixels please", sf.Style.CLOSE)
    state = State()

    state.init_world_state()
    state.init_day()
    state.init_censor()

    clock_font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")

    work_music = sf.Music.from_file("media/music/PixelsPleaseCalm.ogg")
    score_music = sf.Music.from_file("media/music/PixelsPleaseTitle.ogg")

    work_music.loop = True
    score_music.loop = True

    title_screen(window, score_music)

    work_music.play()

    current_page = 0

    button_size = (100, 50)
    next_button_texture = sf.Texture.from_file("media/images/next_button.png")
    next_button_sprite = sf.Sprite(next_button_texture)
    next_button_position = (resolution[0] - button_size[0] - 10, \
                                resolution[1] - button_size[1] - 10)
    next_button_sprite.position = (next_button_position[0], next_button_position[1])

    prev_button_texture = sf.Texture.from_file("media/images/back_button.png")
    prev_button_sprite = sf.Sprite(prev_button_texture)
    prev_button_position = (10, resolution[1] - button_size[1] - 10)
    prev_button_sprite.position = (prev_button_position[0], prev_button_position[1])

    working = True

    while not state.game_over:
        while working:
            working_in_page = True

            time_limit = sf.seconds(30)
            current_time = sf.Clock()

            while working_in_page:
                #time.sleep(0.001) # If you remove this your computer might freze

                state.censor_textures[current_page].display()
                window.draw(sf.Sprite(state.papers[current_page]))
                #window.draw(sf.Sprite(state.map.texture)) # debug
                window.draw(state.censor_sprites[current_page],
                            sf.RenderStates(shader=state.censor_shader))

                clock_text = sf.Text("Time left: " +
                                     str(int(time_limit.seconds - current_time.elapsed_time.seconds)))
                clock_text.position = (10, 10)
                clock_text.font = clock_font
                clock_text.character_size = 12
                clock_text.style = sf.Text.REGULAR
                clock_text.color = sf.Color.BLUE

                window.draw(clock_text)

                if current_time.elapsed_time >= time_limit:
                    #TODO: Do something when the time is over
                    current_time.restart()

                for a in state.day.pages[current_page].articles:
                    window.draw(a.get_text())

                if current_page + 1 < len(state.day.pages):
                    window.draw(next_button_sprite)

                if current_page > 0:
                    window.draw(prev_button_sprite)

                window.display()

                for event in window.events:
                    rt = event_handler.check_event(window, event, state.censor_textures[current_page])

                    if isinstance(event, sf.MouseButtonEvent):
                        if event.pressed and event.button == sf.Mouse.LEFT:
                            mouse_position = sf.Mouse.get_position(window)

                            back_clicked = prev_button_sprite.global_bounds.contains(
                                mouse_position
                            ) and current_page > 0

                            if back_clicked:
                                current_page -= 1

                            if next_button_sprite.global_bounds.contains(mouse_position):
                                working_in_page = False

                                # TODO: not needed when we have buttons
                                if current_page + 1 >= len(state.day.pages):
                                    working = False
                                else:
                                    current_page += 1
        # end of day
        for i in range(len(state.day.pages)):
            end_censor(state, i)

        end_of_day(state)
        working = True
        current_page = 0

def end_censor(state, i):
    per_people, per_goverment = image_handler.compare_images(
        state.maps[i].texture.to_image(),
        state.censor_textures[i].texture.to_image()
    )
    state.day.pages[i].people_score = per_people
    state.day.pages[i].goverment_score = per_goverment

    print("PEOPLE SCORE: "+str(per_people)) # debug
    print("GOV SCORE: "+str(per_goverment)) # debug

def end_of_day(state):
    people, gov = state.day.get_score()
    state.new_score(people, gov)
    state.new_state()
    print("End of day!") # debug
    print("PEOPLE: "+str(state.people_score)+" GOV: "+str(state.goverment_score)) # debug
    print("STATES: People: "+state.people_state+" Gov: "+state.goverment_state) # debug

    #TODO Show consequences and kill player if needed


main()
