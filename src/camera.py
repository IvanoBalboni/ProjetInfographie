import numpy as np
import vector as vect

class Camera:
    '''Classe qui cree une camera et peut retourner le rayon de vue demande.'''

    def __init__(self, height, width, pos, orientation, df ):
        '''
        Liste des attributs: height et width la longueur et largueur de notre image
        pos la position et orientation l'orientation de la camera 
        df la distance focale
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
        
        dy = self.height / resolution[1]  # Delta x et y pour la taille
        dx = self.width  / resolution[0]  # d'un pixel
        
        H = self.orientation.normalize()
        D = H.crossProduct(vect.Vector(origin=self.F, extremity = self.pos) ).normalize()
        
        # Premier P(0,0), besoin pour les prochains calculs
        # P0 = C + H(h/2 - dy/2) - D(l/2 - dx/2)
        P0 = vect.Vector(vec=self.pos).addition(
            H.scalarMult(self.height/2 - dy/2) ).subtract(
            D.scalarMult(self.width/2 - dx/2) )
        # Pxy = P0 - H(y.dy) + D(x.dx)
        P = P0.subtract( H.scalarMult(j * dy) ).addition(
            D.scalarMult( i * dx) )
        # La methode subtract du P0 ne renvoit pas un résultat négatif alors que pour le 
        # resultat de P0[0] devrait l'etre, c'est pourquoi nous faison:
        P[0] = -P[0]  
        
        #Rayon vu FP
        FP = vect.Vector(origin = self.F, extremity = P.vec)
        print(FP)
        return FP

'''
P = (0.0, 5.0, 0.0)
cam = Camera(11,11,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5.0)

print(cam.ray(P))
'''
