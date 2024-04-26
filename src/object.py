import numpy as np
import color as col
import vector as vec

class Object():
    """Classe mere des objets que nous allons pouvoir cree dans notre scene."""
    def __init__(self, pos, color, diffus, specular, ambiant, shadow):
        self.pos = pos
        self.color = color
        self.diffus = diffus
        self.specular = specular
        self.ambiant = ambiant
        self.shadow = shadow

    def calcIntersection(self, camera, p):
        raise NotImplementedError("Object: Object type undefinned")


    def intersection(self, camera, p):
        return self.calcIntersection(camera, p)

    def calcNorm(self, p):
        raise NotImplementedError("Object: Object type undefinned")

    def norm(self, p):
        '''
        ORB!!
        '''
        return self.calcNorm()
