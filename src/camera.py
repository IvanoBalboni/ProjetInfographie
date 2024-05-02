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
        self.orientation = vect.Vector(vec=orientation)
        self.df = df
        (x, y, z) = pos
        self.F = (x, y, z + self.df) #Focale

    def ray(self, ij, resolution):
        '''
        On donne (i,j) de P(i, j) pour placer le point P sur son
        plan de projection et determiner ensuite FP
        '''
        (i, j) = ij
        #print(i,j)
        dy = self.height / resolution[1]
        dx = self.width  / resolution[0]
        H = self.orientation.normalize()
        #print("H is: ", H)
        D = H.crossProduct(vect.Vector(origin=self.F, extremity = self.pos) ).normalize()
        #print("D is: ", D)
        P0 = vect.Vector(vec=self.pos).addition(
            H.scalarMult(self.height/2 - dy/2) ).subtract(
            D.scalarMult(self.width/2 - dx/2) )
        P = P0.subtract( H.scalarMult(j * dy) ).addition(
            D.scalarMult( i * dx) )
        P[0] = -P[0]
        FP = vect.Vector(origin = self.F, extremity = P.vec)
        #print(dx,dy)
        #print(P0)
        #print("FP",FP)
        return FP

'''
P = (0.0, 5.0, 0.0)
cam = Camera(11,11,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5.0)

print(cam.ray(P))
'''
