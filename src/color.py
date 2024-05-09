import numpy as np

class Color:
    """Defini la couleur d'un objet et contient de meme les calcul relatif
    a la courleur."""
    def __init__(self,r, g, b):
            self.r = r
            self.g = g
            self.b = b

    def __str__(self):
        string = "(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"
        return string
