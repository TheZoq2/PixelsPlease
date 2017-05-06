from sfml import sf

def get_pixel_color(image, x, y):
    pix = image.pixels
    startPixel = (x + (y * pix.width)) * 4
    return sf.Color(pix.data[startPixel], pix.data[startPixel+1], pix.data[startPixel+2], pix.data[startPixel+3])

def show_image(path): # for reference
    texture = sf.Texture.from_file(path)
    sprite = sf.Sprite(texture)
    return sprite # window.draw(sprite)
