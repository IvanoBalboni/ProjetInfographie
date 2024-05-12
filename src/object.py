import numpy as np
import color as col
import vector as vec

class Object():
    '''Classe mere des objets que nous allons pouvoir cree dans notre scene.'''
    
    def __init__(self, pos, color, diffus, specular, ambiant, shadow):
        '''
        Liste des attributs: pos la position et color la couleur de notre objet
        diffus la composante diffuse, specular la composante speculaire et ambiant
        la composante ambiante 
        /!\ ces composantes doivent etre compris entre 0 et 1 et leur somme doit etre egal a 1
        shadow un bool pour savoir si nous voulons des ombres
        '''
        self.pos = pos
        self.color = color
        self.diffus = diffus
        self.specular = specular
        self.ambiant = ambiant
        self.shadow = shadow

    def calcIntersection(self, camera, p, resolution):
        '''Va renvoyer a la fonction enfant si elle existe '''
        raise NotImplementedError("Object: Object type undefinned")


    def calcNorm(self, p):
        raise NotImplementedError("Object: Object type undefinned")

