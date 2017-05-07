#!/usr/bin/python3
from sfml import sf
import event_handler
import image_handler
from models import Article, Page, Day
import generator
from state import State

resolution = (1024, 768)

def title_screen(window, music):
    title_texture = sf.Texture.from_file("media/images/Letter.png");
    title_sprite = sf.Sprite(title_texture);

    continue_button_texture = sf.Texture.from_file("media/images/continue_button.png")
    continue_button_sprite = sf.Sprite(continue_button_texture)
    continue_button_size = (100, 50)
    continue_button_position = (resolution[0] - continue_button_size[0] - 10, \
                                resolution[1] - continue_button_size[1] - 10)
    continue_button_sprite.position = (continue_button_position[0], continue_button_position[1])


    music.play()

    while True:
        window.draw(title_sprite);
        window.draw(continue_button_sprite)
        window.display()


        for event in window.events:
            if type(event) is sf.KeyEvent:
                if event.pressed and event.code == sf.Keyboard.X:
                    window.close()
                    exit()
                if event.pressed and event.code == sf.Keyboard.RETURN:
                    music.stop()
                    return

            if type(event) is sf.MouseButtonEvent:
                if event.pressed and event.button == sf.Mouse.LEFT:
                    mouse_position = sf.Mouse.get_position(window)

                    if mouse_position.x >= continue_button_position[0] and \
                       mouse_position.x <= continue_button_position[0] + continue_button_size[0] and \
                       mouse_position.y >= continue_button_position[1] and \
                       mouse_position.y <= continue_button_position[1] + continue_button_size[1]:
                        music.stop()
                        return


def main():
    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]), "Pixels please")
    state = State()

    state.init_world_state()
    state.init_censor()
    state.init_day()


    #window.clear(sf.Color.BLUE)

    state.censor_texture = sf.RenderTexture(resolution[0], resolution[1])

    clock_font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")


    title_screen(window, state.score_music)

    state.work_music.play()

    while not state.game_over:

        for i in range(len(state.day.pages)):
            working_in_page = True
            state.map = state.day.pages[i].get_map_texture()
            state.paper = sf.Texture.from_image(state.day.pages[i].get_image())

            state.censor.clear(sf.Color.TRANSPARENT)
            state.censor_sprite = sf.Sprite(state.censor.texture)

            time_limit = sf.seconds(30)
            current_time = sf.Clock()

            time_limit = sf.seconds(30)
            current_time = sf.Clock()

            while working_in_page:
                #time.sleep(0.001) # If you remove this your computer might freze

                state.censor.display()
                window.draw(sf.Sprite(state.paper))
                #window.draw(sf.Sprite(state.map.texture)) # debug
                window.draw(state.censor_sprite, sf.RenderStates(shader=state.censor_shader))

                clock_text = sf.Text("Time left: " + str(int(time_limit.seconds - current_time.elapsed_time.seconds)))
                clock_text.position = (10, 10)
                clock_text.font = clock_font
                clock_text.character_size = 12
                clock_text.style = sf.Text.REGULAR
                clock_text.color = sf.Color.BLUE

                window.draw(clock_text)

                if current_time.elapsed_time >= time_limit:
                    #TODO: Do something when the time is over
                    current_time.restart()

                for a in state.day.pages[i].articles:
                    window.draw(a.get_text())

                window.display()

                for event in window.events:
                    rt = event_handler.check_event(window, event, state)
                    if rt == "END":
                        end_censor(state, i)
                        working_in_page = False

        end_of_day(state)

def end_censor(state, i):
    per_people, per_goverment = image_handler.compare_images(state.map.texture.to_image(), state.censor.texture.to_image())
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
