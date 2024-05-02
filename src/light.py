import numpy as np
import color as col

class Light:
    """Cree la position de la lumiere."""
    def __init__(self, pos, color):
        self.color = color
        self.pos = pos
