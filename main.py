#!/usr/bin/python3
from sfml import sf
import event_handler
import image_handler
from models import ArticleTitle, Page
import generator

resolution = (1024, 768)

def main():
    window = sf.RenderWindow(sf.VideoMode(resolution[0], resolution[1]), "Pixels please")
    #window.clear(sf.Color.BLUE)

    censor_texture = sf.RenderTexture(resolution[0], resolution[1])
    censor_texture.clear(sf.Color.TRANSPARENT)
    censor_texture_sprite = sf.Sprite(censor_texture.texture)

    rekt = sf.RectangleShape();
    rekt.size = resolution
    rekt.fill_color = sf.Color(255, 255, 255)

    shader = sf.Shader.from_file("media/shaders/censor.vert", "media/shaders/censor.frag")

    #paper = sf.Texture.from_file('media/images/pixels_please_paper_1.png')
    map  = sf.Texture.from_file('media/images/pixels_please_paper_1_censor_map.png')
    page = get_page()
    paper = sf.Texture.from_image(page.get_image())


    while True:
        #time.sleep(0.001) # If you remove this your computer might freze


        censor_texture.display()
        window.draw(rekt)
        window.draw(sf.Sprite(paper))
        window.draw(censor_texture_sprite, sf.RenderStates(shader=shader))

        for a in page.articles:
            window.draw(a.get_text())

        window.display()

        for event in window.events:
            rt = event_handler.check_event(window, event, censor_texture)
            if rt == "END":
                end_censor(censor_texture.texture, map)


def end_censor(censor, map):
    per_people, per_goverment = image_handler.compare_images(map.to_image(), censor.to_image())
    # save the score
    # next page
    print("PEOPLE SCORE: "+str(per_people)) # debug
    print("GOV SCORE: "+str(per_goverment)) # debug


def get_page():
    articles = []

    articles.append(ArticleTitle(260, 140, "bg", generator.generate_headline()[0]))
    articles.append(ArticleTitle(260, 330, "tl", generator.generate_headline()[0]))
    articles.append(ArticleTitle(550, 330, "sm", generator.generate_headline()[0]))
    articles.append(ArticleTitle(550, 450, "sm", generator.generate_headline()[0]))

    return Page(articles)


main()
