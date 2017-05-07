#!/usr/bin/python3
from sfml import sf
import event_handler
import image_handler
from models import Article, Page, Day
import generator
from state import State
import random

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

def load_texture_and_sprite(filename, pos):
    texture = sf.Texture.from_file(filename)
    sprite = sf.Sprite(texture)
    sprite.position = pos
    return sprite

def main():
    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]),
                             "Pixels please", sf.Style.CLOSE)
    state = State()

    state.init_world_state()

    clock_font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")


    title_screen(window, state.score_music)

    state.work_music.play()

    current_page = 0
    button_size = (100, 50)

    next_button_sprite = load_texture_and_sprite(
        "media/images/next_button.png",
        (resolution[0] - button_size[0] - 10, resolution[1] - button_size[1] - 10)
    )
    prev_button_sprite = load_texture_and_sprite(
        "media/images/back_button.png", (10, resolution[1] - button_size[1] - 10)
    )
    publish_button_sprite = load_texture_and_sprite(
        "media/images/publish_button.png",
        (resolution[0] // 2 - button_size[0] // 2, resolution[1] - button_size[1] - 10)
    )
    clear_button_width = 50
    clear_button_sprite = load_texture_and_sprite(
        "media/images/clear_all_button.png",
        (resolution[0] - clear_button_width - 10, 10)
    )

    working = True

    while not state.game_over:
        state.init_day()
        state.init_censor()
        while working:
            working_in_page = True

            while working_in_page:
                #time.sleep(0.001) # If you remove this your computer might freze

                state.censor_textures[current_page].display()
                window.draw(sf.Sprite(state.papers[current_page]))
                #window.draw(sf.Sprite(state.map.texture)) # debug
                window.draw(state.censor_sprites[current_page],
                            sf.RenderStates(shader=state.censor_shader))

                for a in state.day.pages[current_page].articles:
                    window.draw(a.get_text())

                if current_page + 1 < len(state.day.pages):
                    window.draw(next_button_sprite)

                if current_page > 0:
                    window.draw(prev_button_sprite)

                window.draw(publish_button_sprite)
                window.draw(clear_button_sprite)

                window.display()

                for event in window.events:
                    rt = event_handler.check_event(window, event, state, current_page)

                    if isinstance(event, sf.MouseButtonEvent):
                        if event.pressed and event.button == sf.Mouse.LEFT:
                            mouse_position = sf.Mouse.get_position(window)

                            def button_clicked(sprite):
                                return sprite.global_bounds.contains(mouse_position)

                            if button_clicked(prev_button_sprite) and current_page > 0:
                                current_page -= 1

                            on_last_page = current_page + 1 >= len(state.day.pages)
                            if button_clicked(next_button_sprite) and not on_last_page:
                                current_page += 1

                            if button_clicked(clear_button_sprite):
                                state.censor_textures[current_page].clear(sf.Color.WHITE)

                            if button_clicked(publish_button_sprite):
                                working_in_page = False
                                working = False
        # end of day
        for i in range(len(state.day.pages)):
            end_censor(state, i)

        end_of_day(state, window)
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

def end_of_day(state, window):
    people, gov = state.day.get_score()
    state.new_score(people, gov)
    state.new_state()

    print("End of day!") # debug
    print("PEOPLE: "+str(state.people_score)+" GOV: "+str(state.goverment_score)) # debug
    print("STATES: People: "+state.people_state+" Gov: "+state.goverment_state) # debug

    # Select a random amount of events to trigger
    event_amount = random.randint(1, 5)

    noticeList = []
    noticeList.append(state.get_people_state())
    noticeList.append(state.get_government_state())

    for i in range(0, event_amount):
        result = generator.random_event(state.world_state)
        if result:
            noticeList.append(result)

    #TODO Show states

    end_day_texture = sf.Texture.from_file("media/images/table_texture.png")
    end_day_sprite = sf.Sprite(end_day_texture)


    sleep_button_texture = sf.Texture.from_file("media/images/go_to_sleep_button.png") # temporal
    sleep_button_sprite = sf.Sprite(sleep_button_texture)
    sleep_button_size = (100, 50)
    sleep_button_position = (resolution[0] - sleep_button_size[0] - 10, \
                                resolution[1] - sleep_button_size[1] - 10)
    sleep_button_sprite.position = (sleep_button_position[0], sleep_button_position[1])

    notices = notice_panel(noticeList)
    notices_sprite = sf.Sprite(notices.texture)
    people_bar = progress_bar("People", state.people_score, resolution[0]/2-180, 60)
    people_bar_sprite = sf.Sprite(people_bar.texture)
    goverment_bar = progress_bar("Government", state.goverment_score, resolution[0]/2+100, 60)
    goverment_bar_sprite = sf.Sprite(goverment_bar.texture)

    while True:
        window.draw(end_day_sprite)
        window.draw(notices_sprite)
        window.draw(sleep_button_sprite)
        window.draw(goverment_bar_sprite)
        window.draw(people_bar_sprite)

        window.display()

        for event in window.events:
            if type(event) is sf.KeyEvent:
                if event.pressed and event.code == sf.Keyboard.X:
                    window.close()
                    exit()
                if event.pressed and event.code == sf.Keyboard.RETURN:
                    state.score_music.stop()
                    return

            if type(event) is sf.MouseButtonEvent:
                if event.pressed and event.button == sf.Mouse.LEFT:
                    mouse_position = sf.Mouse.get_position(window)

                    if sleep_button_sprite.global_bounds.contains(mouse_position):
                        state.score_music.stop()
                        return

def notice_panel(notices):
    base = sf.RenderTexture(resolution[0], resolution[1])
    base.clear(sf.Color.TRANSPARENT)

    font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")
    title = sf.Text()
    title.font = font
    title.character_size = 20
    title.style = sf.Text.REGULAR
    title.color = sf.Color.WHITE

    for i, n in enumerate(notices):
        title.string = n
        title.position = (10, 25*i+(resolution[1]*0.7))

        base.draw(title)

    base.display()
    return base



def progress_bar(name, progress, posx, posy):
    base = sf.RenderTexture(resolution[0], resolution[1])
    base.clear(sf.Color.TRANSPARENT)

    font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")
    title = sf.Text(name)
    title.position = (posx-5, posy)
    title.font = font
    title.character_size = 20
    title.style = sf.Text.REGULAR
    title.color = sf.Color.WHITE

    red_size = (progress * 370) / 100
    black_size = 370 - red_size

    black = sf.RectangleShape((80, black_size))
    black.position = posx, posy+30
    black.fill_color = sf.Color.BLACK

    red = sf.RectangleShape((80, red_size))
    red.position = posx, black.position.y+black_size
    red.fill_color = sf.Color.RED

    base.draw(black)
    base.draw(red)
    base.draw(title)

    base.display()

    return base

main()
