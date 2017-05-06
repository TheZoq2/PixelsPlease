#!/usr/bin/python3
from sfml import sf
import event_handler
import image_handler
from models import Article, Page, Day
import generator

resolution = (1024, 768)

class GameState:
    def __init__(self):
        self.censor_texture = None
        self.censor_texture_sprite = None
        self.map = None
        self.page = None
        self.paper = None

def title_screen(window, music):
    title_texture = sf.Texture.from_file("media/images/Letter.png");
    title_sprite = sf.Sprite(title_texture);

    music.play()

    while True:
        window.draw(title_sprite);
        window.display()

        for event in window.events:
            if type(event) is sf.KeyEvent:
                if event.pressed and event.code == sf.Keyboard.X:
                    window.close()
                    exit()
                if event.pressed and event.code == sf.Keyboard.RETURN:
                    music.stop()
                    return

def main():
    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]), "Pixels please", sf.Style.CLOSE)
    state = GameState()

    world_state = generator.WorldState()

    #window.clear(sf.Color.BLUE)

    state.censor_texture = sf.RenderTexture(resolution[0], resolution[1])

    shader = sf.Shader.from_file("media/shaders/censor.vert", "media/shaders/censor.frag")
    clock_font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")

    work_music = sf.Music.from_file("media/music/PixelsPleaseCalm.ogg")
    score_music = sf.Music.from_file("media/music/PixelsPleaseTitle.ogg")

    work_music.loop = True
    score_music.loop = True

    title_screen(window, score_music)

    work_music.play()

    #paper = sf.Texture.from_file('media/images/pixels_please_paper_1.png')
    state.day = generate_day(world_state)

    for i in range(len(state.day.pages)):
        working_in_page = True
        state.map = state.day.pages[i].get_map_texture()
        state.paper = sf.Texture.from_image(state.day.pages[i].get_image())

        state.censor_texture.clear(sf.Color.TRANSPARENT)
        state.censor_texture_sprite = sf.Sprite(state.censor_texture.texture)

        time_limit = sf.seconds(30)
        current_time = sf.Clock()

        time_limit = sf.seconds(30)
        current_time = sf.Clock()

        while working_in_page:
            #time.sleep(0.001) # If you remove this your computer might freze

            state.censor_texture.display()
            window.draw(sf.Sprite(state.paper))
            window.draw(sf.Sprite(state.map.texture)) # debug
            window.draw(state.censor_texture_sprite, sf.RenderStates(shader=shader))

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
                rt = event_handler.check_event(window, event, state.censor_texture)
                if rt == "END":
                    end_censor(state, i)
                    working_in_page = False
    # end of day


def end_censor(state, i):
    per_people, per_goverment = image_handler.compare_images(state.map.texture.to_image(), state.censor_texture.texture.to_image())
    state.day.pages[i].people_score = per_people
    state.day.pages[i].goverment_score = per_goverment

    per_people, per_goverment = image_handler.compare_images(
            state.map.texture.to_image(),
            state.censor_texture.texture.to_image()
        )
    # save the score
    # next page
    print("PEOPLE SCORE: "+str(per_people)) # debug
    print("GOV SCORE: "+str(per_goverment)) # debug

    

def generate_day(world_state):
    pages = []
    for i in range(3): # 3 articles?
        pages.append(generate_page(world_state))

    return Day(pages)


def generate_page(world_state):
    articles = []

    articles.append(Article(260, 140, "bg", generator.generate_headline(world_state)))
    articles.append(Article(260, 330, "tl", generator.generate_headline(world_state)))
    articles.append(Article(550, 330, "sm", generator.generate_headline(world_state)))
    articles.append(Article(550, 450, "sm", generator.generate_headline(world_state)))

    return Page(articles)


main()
