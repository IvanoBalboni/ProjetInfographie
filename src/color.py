import numpy as np

class Color:
    """Defini la couleur d'un objet et contient de meme les calcul relatif
    a la courleur."""
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        string = "(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"
        return string

    def norm_color(self):
        max_rgb = max(self.r, self.g, self.b)
        if max_rgb > 255:
            # Division par le max pour se retrouver entre 0 et 1
            # Puis mulitplication par 255 pour le bon format PIP
            self.r = round((self.r/max_rgb)*255)
            self.g = round((self.g/max_rgb)*255)
            self.b = round((self.b/max_rgb)*255)
        
