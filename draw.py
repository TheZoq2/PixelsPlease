from sfml import sf

# length of a side in pixels
censor_size = 30

def censor(censor_texture, position):
    rectangle = sf.RectangleShape((censor_size, censor_size))
    rectangle.fill_color = sf.Color.RED
    rectangle.position = position - (censor_size/2, censor_size/2)
    censor_texture.draw(rectangle)
