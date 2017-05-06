from sfml import sf

def get_pixel_color(image, x, y):
    pix = image.pixels
    pixNumber = x*pix.height + y
    return pix.data[pixNumber]

def show_image(path): # for reference
    texture = sf.Texture.from_file(path)
    sprite = sf.Sprite(texture)
    return sprite # window.draw(sprite)
