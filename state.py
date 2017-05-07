from sfml import sf
import generator
from models import Article, Page, Day

resolution = (1024, 768)

class State():
    def __init__(self):
        self.goverment_state = "normal"
        self.people_state = "normal"
        self.goverment_score = 50
        self.people_score = 50
        self.salary = 50 # ??
        self.day = None

        self.map = None #TODO
        self.censor = None
        self.censor_sprite = None
        self.censor_shader = None

        self.world_state = None
        self.game_over = False


    def init_page(self):
        articles = []
        headline = generator.generate_headline(self.world_state)
        articles.append(Article(260, 140, "bg", headline))
        headline = generator.generate_headline(self.world_state)
        articles.append(Article(260, 330, "tl", headline))
        headline = generator.generate_headline(self.world_state)
        articles.append(Article(550, 330, "sm", headline))
        headline = generator.generate_headline(self.world_state)
        articles.append(Article(550, 450, "sm", headline))

        return Page(articles)

    def init_day(self, n=3):
        pages = []
        for i in range(n):
            pages.append(self.init_page())

        self.day = Day(pages)

    def init_censor(self):
        self.censor = sf.RenderTexture(resolution[0], resolution[1])
        self.censor_shader = sf.Shader.from_file("media/shaders/censor.vert", "media/shaders/censor.frag")

    def init_world_state(self):
        self.world_state = generator.WorldState()

    def new_score(self, people_score, goverment_score):
        self.people_score = (self.people_score * 0.3) + (people_score * 0.7)
        self.goverment_score = (self.goverment_score * 0.3) + (goverment_score * 0.7)

    def new_state(self):
        self.new_people_state()
        self.new_goverment_state()

    def new_goverment_state(self):
        if self.goverment_state == "+20":
            if self.goverment_score < 50:
                self.goverment_state = "normal"
            elif self.goverment_score < 80:
                self.goverment_state = "+10"
        elif self.goverment_state == "+10":
            if self.goverment_score > 80:
                self.goverment_state = "+20"
            elif self.goverment_score < 40:
                self.goverment_state = "-10"
            elif self.goverment_score < 50:
                self.goverment_state = "normal"
        elif self.goverment_state == "normal":
            if self.goverment_score > 60:
                self.goverment_state = "+10"
            elif self.goverment_score < 20:
                self.goverment_state = "-20"
            elif self.goverment_score < 50:
                self.goverment_state = "-10"
        elif self.goverment_state == "-10":
            if self.goverment_score > 50:
                self.goverment_state = "normal"
            elif self.goverment_score < 10:
                self.goverment_state = "jail"
            elif self.goverment_score < 30:
                self.goverment_state = "-20"
        elif self.goverment_state == "-20":
            if self.goverment_score > 50:
                self.goverment_state = "normal"
            elif self.goverment_score > 30:
                self.goverment_state = "-10"
            elif self.goverment_score < 15:
                self.goverment_state = "jail"
        else: # jail -> game over
            pass

    def new_people_state(self):
        if self.people_state == "empowered":
            if self.people_score > 80:
                self.people_state = "revolution"
            elif self.people_score < 30:
                self.people_state = "demostrations"
            elif self.people_score < 60:
                self.people_state = "normal"

        elif self.people_state == "normal":
            if self.people_score > 60:
                self.people_state = "empowered"
            elif self.people_score < 20:
                self.people_state = "riots"
            elif self.people_score < 40:
                self.people_state = "demostrations"

        elif self.people_state == "demostrations":
            if self.people_score > 50:
                self.people_state = "normal"
            elif self.people_score < 10:
                self.people_state = "revolution"
            elif self.people_score < 30:
                self.people_state = "riots"

        elif self.people_state == "riots":
            if self.people_state > 50:
                self.people_state = "normal"
            elif self.people_score > 40:
                self.people_state = "demostrations"
            elif self.people_score < 20:
                self.people_state = "revolution"

        else:
            pass # revolution, game over
