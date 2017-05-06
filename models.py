from sfml import sf

class Day():
    def __init__(self, pages):
        self.pages = pages

    def get_score(self):
        people = 0
        gov = 0
        for page in self.pages:
            people += page.pScore
            gov += page.gScore

        people /= len(self.pages)
        gov /= len(self.pages)

        return people, gov

class ArticleTitle():
    def __init__(self, x, y, size, text=""):
        self.x = x
        self.y = y
        self.size = size # tl, bg or sm
        self.text = text

    def get_text_size(self):
        if self.size == "tl":
            return 20
        elif self.size == "bg":
            return 30
        else: # sm
            return 10

    def get_text(self):
        font = sf.Font.from_file("media/fonts/Pixelated-Regular.ttf")
        title = sf.Text(self.text)
        title.position = (self.x, self.y)
        title.font = font
        title.character_size = self.get_text_size()
        title.style = sf.Text.REGULAR
        title.color = sf.Color.BLACK
        return title

class Page():
    def __init__(self, articles):
        self.articles = articles

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
