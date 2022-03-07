import random

from enum import Enum

def random_colour():
    colour = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (colour(), colour(), colour())

class Colour(Enum):
    """
    Default colours to use in Embeds or as strings.
    
    Colours:
    - Blue : BLUE
    - Green : GREEN
    - Yellow : YELLOW
    - Pink : PINK
    - Red : RED
    - Black : BLACK
    - White : WHITE
    - Random : RANDOM
    """

    def __str__(self):
        return str(self.value)

    BLUE = "#5865F2"
    GREEN = "#57F287"
    YELLOW = "#FEE75C"
    PINK = "#EB459E"
    RED = "#ED4245"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    RANDOM = random_colour()
