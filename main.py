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

def main():
    state = GameState()

    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]), "Pixels please")
    #window.clear(sf.Color.BLUE)

    state.censor_texture = sf.RenderTexture(resolution[0], resolution[1])
    state.censor_texture.clear(sf.Color.TRANSPARENT)
    state.censor_texture_sprite = sf.Sprite(state.censor_texture.texture)

    shader = sf.Shader.from_file("media/shaders/censor.vert", "media/shaders/censor.frag")

    #paper = sf.Texture.from_file('media/images/pixels_please_paper_1.png')
    state.day = generate_day()
    for i in range(len(state.day.pages)):
        working_in_page = True
        state.map  = state.day.pages[i].get_map_texture()
        state.paper = sf.Texture.from_image(state.day.pages[i].get_image())


        while working_in_page:
            #time.sleep(0.001) # If you remove this your computer might freze

            state.censor_texture.display()
            window.draw(sf.Sprite(state.paper))
            #window.draw(sf.Sprite(state.map.texture)) # debug
            window.draw(state.censor_texture_sprite, sf.RenderStates(shader=shader))

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
    # save the score
    # next page
    print("PEOPLE SCORE: "+str(per_people)) # debug
    print("GOV SCORE: "+str(per_goverment)) # debug

    #generate a new game state

def generate_day():
    pages = []
    for i in range(3): # 3 articles?
        pages.append(generate_page())

    return Day(pages)


def generate_page():
    articles = []

    articles.append(Article(260, 140, "bg", generator.generate_headline()[0], generator.generate_headline()[1]))
    articles.append(Article(260, 330, "tl", generator.generate_headline()[0], generator.generate_headline()[1]))
    articles.append(Article(550, 330, "sm", generator.generate_headline()[0], generator.generate_headline()[1]))
    articles.append(Article(550, 450, "sm", generator.generate_headline()[0], generator.generate_headline()[1]))

    return Page(articles)


main()
