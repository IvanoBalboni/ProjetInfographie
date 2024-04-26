import numpy as np

class Vector():
    """Classe regroupant tout ce qui s'attache aux vecteurs et leurs calcul."""

    def __init__(self, **kwargs):
        """Soit cree un vecteur a partir de 2 coordonnees donnees (soustraction),
        soit cree un vecteur a partir de 3 valeurs donnees."""
        k =  kwargs.keys()
        (x,y,z) = (0,0,0)
        if len(k) == 1:
	        (x,y,z) = kwargs['vec']
        if len(k) == 2:
	        e = kwargs['extremity']
	        o = kwargs['origin']
	        (x,y,z) = np.subtract(e, o)

        self.vec = (x, y, z)

    '''
    def __init__( self, origin=(0.0, 0.0, 0.0), extremity=(0.0, 0.0, 0.0) kwwargs):
    self.vec = np.subtract(extremity,origin)
    '''

    def addition(self, v2):
        """Addition vecteur x vecteur, retourne un vecteur."""
        return Vector(vec = np.add(self.vec,v2))

    def subtract(self, v2):
        """Soustraction vecteur x vecteur, retourne un vecteur."""
        return Vector(vec = np.subtract(self.vec,v2))

    def scalarMult(self, s):
        """Multiplication vecteur x scalaire, retourne un vecteur."""
        return Vector(vec = np.multiply(self.vec,s))

    def scalarProduct(self, v2):
        """Multiplication vecteur x vecteur, retourne un scalaire."""
        print(self.vec,"   ",v2)
        return np.dot(self.vec,v2)

    def vectorProduct(self, v2):
        """Multiplication vecteur x vecteur, retourne un vecteur."""
        return Vector(vec = np.cross(self.vec,v2))

    def norm(self):
        return np.linalg.norm(self.vec)

    def normalize(self):
        n = self.norm()
        return Vector(vec = np.divide(self.vec,n))


    def __str__(self):
        string = "(" + str(self.vec[0]) + ", " + str(self.vec[1]) + ", " + str(self.vec[2]) + ")"
        return string

'''
v1 = (1.0,2.0,3.0)
v2 = (4.0,5.0,6.0)
va = Vector(origin=v1,extremity= v2)
vb = Vector(origin = v2,extremity = v1)

print(va.addition(vb.vec))
print(va.subtract(vb.vec))
print(va.scalarMult(5))
print("scalar prod   ",va.scalarProduct(vb.vec))
print(va.vectorProduct(vb.vec))
print(va.norm())
print(va.normalize())
'''
