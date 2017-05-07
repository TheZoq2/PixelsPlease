from sfml import sf
import copy

resolution = (1024, 768)

class Article():
    def __init__(self, x, y, size, headline):
        self.x = x
        self.y = y
        self.size = size # tl, bg or sm
        self.text = headline[0]
        self.type = headline[1]

    def get_lined_text(self):
        if self.size == "tl":
            count = 12
        elif self.size == "bg":
            count = 20
        else: # sm
            count = 20

        rt = ""

        chars = copy.deepcopy(self.text)
        last_space = None

        words = chars.split(" ")

        current_len = 0
        for word in words:
            current_len += len(word)

            if current_len > count:
                rt += "\n"
                current_len = 0
            else:
                rt += " "


            rt += word

        return rt


    def get_text_size(self):
        if self.size == "tl":
            return 20
        elif self.size == "bg":
            return 30
        else: # sm
            return 10

    def get_text(self):
        font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")
        title = sf.Text(self.get_lined_text())
        title.position = (self.x, self.y)
        title.font = font
        title.character_size = self.get_text_size()
        title.style = sf.Text.REGULAR
        title.color = sf.Color.BLACK
        return title


class Page():
    def __init__(self, articles):
        self.articles = articles
        self.people_score = None
        self.goverment_score = None

    def get_map_texture(self):
        base = sf.RenderTexture(resolution[0], resolution[1])
        base.clear(sf.Color.TRANSPARENT)
        for a in self.articles:
            #bounds = a.get_text().global_bounds
            #rect = sf.RectangleShape((bounds.size[0]-5, bounds.size[1]-5))
            #rect.position = bounds.position[0], (bounds.position[1] - (bounds.position[1] - resolution[1]/2)*2)-bounds.size[1]+5 # it works, don't ask how
            #if a.type == -1:
            #    rect.fill_color = sf.Color.BLACK
            #else: #0
            #    rect.fill_color = sf.Color.RED

            #base.draw(rect)
            text_object = a.get_text()
            if a.type == -1:
                text_object.color = sf.Color.BLACK
            else: #0
                text_object.color = sf.Color.RED

            base.draw(text_object)

        base.display()
        return base


    def get_image(self):

        base = sf.Image.from_file("media/images/empty_page.png")
        bg = sf.Image.from_file("media/images/bg_article.png")
        sm = sf.Image.from_file("media/images/sm_article.png")
        tl = sf.Image.from_file("media/images/tl_article.png")

        for a in self.articles:
            if a.size == "tl":
                base.blit(tl, (a.x, a.y))
            elif a.size == "sm":
                base.blit(sm, (a.x, a.y))
            else: #bg
                base.blit(bg, (a.x, a.y))

        return base

class Day():
    def __init__(self, pages):
        self.pages = pages

    def get_score(self):
        people = 0
        gov = 0
        for page in self.pages:
            people += page.people_score
            gov += page.goverment_score

        people /= len(self.pages)
        gov /= len(self.pages)

        return people, gov
