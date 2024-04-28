import numpy as np
import vector as vect

class Camera:
    """Classe qui cree une camera et peut retourner le rayon de vue demande."""

    def __init__(self, height, width, pos, orientation, df ):
        '''
        df = distance focale :)
        '''
        self.height = height
        self.width = width
        self.pos = pos
        self.orientation = orientation
        self.df = df
        (x, y, z) = pos
        self.F = (x, y, z + self.df) #Focale

    def ray(self, P):
        '''
        On donne 2 points F et P pour creer le vecteur FP
        qui est le rayon de vue non normalise.
        '''

        return vect.Vector(origin = self.F, extremity = P)

'''
P = (0.0, 5.0, 0.0)
cam = Camera(11,11,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5.0)

print(cam.ray(P))
'''
