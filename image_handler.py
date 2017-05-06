from sfml import sf

CENSOR_REWARD = 10
CENSOR_PENALTY = 2

def show_image(path): # for reference
    texture = sf.Texture.from_file(path)
    sprite = sf.Sprite(texture)
    return sprite # window.draw(sprite)

def compare_images(base, user):
    gov_score_max = 0
    people_score_max = 0
    gov_score = 0
    people_score = 0

    for i in range(base.width):
        for j in range(base.height):
            cb = base[i,j]
            cu = user[i,j]
            if cb == sf.Color.BLACK:
                gov_score_max += CENSOR_REWARD
                if cu == sf.Color.BLACK:
                    gov_score += CENSOR_REWARD
                    people_score -= CENSOR_PENALTY

            elif cb == sf.Color.RED:
                people_score_max += CENSOR_REWARD
                if cu != sf.Color.BLACK:
                    people_score += CENSOR_REWARD


    per_people = (people_score*100)/people_score_max
    per_goverment = (gov_score*100)/gov_score_max)

    #print("PEOPLE SCORE MAX: "+str(people_score_max)+" SCORE: "+str(people_score)+" PER: "+str(per_people))
    #print("GOV SCORE MAX: "+str(gov_score_max)+" SCORE: "+str(gov_score)+" PER: "+str(per_goverment)

    return per_people, per_goverment


base = sf.Image.from_file("../base.png")
user = sf.Image.from_file("../user.png")

sc = compare_images(base, user)
