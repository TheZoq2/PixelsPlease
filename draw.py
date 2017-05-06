from sfml import sf

# length of a side in pixels
square_length = 30

def draw_square(window, position):
    rectangle = sf.RectangleShape((square_length, square_length))
    rectangle.fill_color = sf.Color.RED
    rectangle.position = position - (square_length/2, square_length/2)
    window.draw(rectangle)
