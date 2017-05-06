from sfml import sf

# length of a side in pixels
censor_size = 30
rectangle = sf.RectangleShape((censor_size, censor_size))

def censor(censor_texture, position):
    rectangle.fill_color = sf.Color.BLACK
    rectangle.position = position - (censor_size/2, censor_size/2)
    censor_texture.draw(rectangle)

def uncensor(censor_texture, position):
    rectangle.fill_color = sf.Color.WHITE
    rectangle.position = position - (censor_size/2, censor_size/2)
    censor_texture.draw(rectangle)
