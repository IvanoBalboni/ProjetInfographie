import numpy as np
import color as col

class Light:
    """Cree la position de la lumiere."""
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
