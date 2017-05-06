#!/usr/bin/python3
from sfml import sf
import event_handler
import image_handler
from models import ArticleTitle, Page
import generator

resolution = (1024, 768)

class GameState:
    def __init__(self):
        self.censor_texture = None
        self.censor_texture_sprite = None
        self.map = None
        self.page = None
        self.paper = None

def main():
    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]), "Pixels please", sf.Style.CLOSE)
    state = GameState()
    #window.clear(sf.Color.BLUE)

    state.censor_texture = sf.RenderTexture(resolution[0], resolution[1])
    state.censor_texture.clear(sf.Color.TRANSPARENT)
    state.censor_texture_sprite = sf.Sprite(state.censor_texture.texture)

    shader = sf.Shader.from_file("media/shaders/censor.vert", "media/shaders/censor.frag")

    #paper = sf.Texture.from_file('media/images/pixels_please_paper_1.png')
    state.page = get_page()
    state.map  = state.page.get_map_texture()
    state.paper = sf.Texture.from_image(state.page.get_image())

    time_limit = sf.seconds(30)
    current_time = sf.Clock()

    clock_font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")

    while True:
        #time.sleep(0.001) # If you remove this your computer might freze
        state.censor_texture.display()
        window.draw(sf.Sprite(state.paper))
        #window.draw(sf.Sprite(state.map.texture)) # debug
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

        for a in state.page.articles:
            window.draw(a.get_text())

        window.display()

        for event in window.events:
            rt = event_handler.check_event(window, event, state.censor_texture)
            if rt == "END":
                end_censor(state)


def end_censor(state):
    per_people, per_goverment = image_handler.compare_images(state.map.texture.to_image(), state.censor_texture.texture.to_image())
    # save the score
    # next page
    print("PEOPLE SCORE: "+str(per_people)) # debug
    print("GOV SCORE: "+str(per_goverment)) # debug

    #generate a new game state


def get_page():
    articles = []

    articles.append(ArticleTitle(260, 140, "bg", generator.generate_headline()[0], generator.generate_headline()[1]))
    articles.append(ArticleTitle(260, 330, "tl", generator.generate_headline()[0], generator.generate_headline()[1]))
    articles.append(ArticleTitle(550, 330, "sm", generator.generate_headline()[0], generator.generate_headline()[1]))
    articles.append(ArticleTitle(550, 450, "sm", generator.generate_headline()[0], generator.generate_headline()[1]))

    return Page(articles)


main()
