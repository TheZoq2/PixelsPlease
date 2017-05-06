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
    state.map  = sf.Texture.from_file('media/images/pixels_please_paper_1_censor_map.png')
    state.page = get_page()
    state.paper = sf.Texture.from_image(state.page.get_image())


    while True:
        #time.sleep(0.001) # If you remove this your computer might freze


        state.censor_texture.display()
        window.draw(sf.Sprite(state.paper))
        window.draw(state.censor_texture_sprite, sf.RenderStates(shader=shader))

        for a in state.page.articles:
            window.draw(a.get_text())

        window.display()

        for event in window.events:
            rt = event_handler.check_event(window, event, state.censor_texture)
            if rt == "END":
                end_censor(state)


def end_censor(state):
    per_people, per_goverment = image_handler.compare_images(state.map.to_image(), state.censor.to_image())
    # save the score
    # next page
    print("PEOPLE SCORE: "+str(per_people)) # debug
    print("GOV SCORE: "+str(per_goverment)) # debug

    #generate a new game state


def get_page():
    articles = []

    articles.append(ArticleTitle(260, 140, "bg", generator.generate_headline()[0]))
    articles.append(ArticleTitle(260, 330, "tl", generator.generate_headline()[0]))
    articles.append(ArticleTitle(550, 330, "sm", generator.generate_headline()[0]))
    articles.append(ArticleTitle(550, 450, "sm", generator.generate_headline()[0]))

    return Page(articles)


main()
