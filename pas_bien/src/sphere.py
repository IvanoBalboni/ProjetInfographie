import object as obj
import camera as cam
import vector as vect

class Sphere(obj.Object):
    """Classe qui va nous cree une sphere et nous permettre de trouver son intersection."""
    def __init__(self, rayon, pos, color, diffus, specular, ambiant, shadow):
        obj.Object.__init__(self, pos, color, diffus, specular, ambiant, shadow)
        self.rayon = rayon

    def calcIntersection(self, camera, p):
        (l,m,n) = self.pos # centre de la sphere
        #delta = (2 * ( fx - l) **2 +m +n))**2 - 4 * (self.rayon + l**2 + m**2 + n**2)

        (i, j, k) = camera.ray(p).vec # rayon de vue : FP
        (fx, fy, fz) = camera.F # focale : F
        cx, cy, cz = (l-fx), (m-fy), (n-fz)
        a = i**2 + j **2 + k **2
        b = -2 * (cx *i + cy*j + cz *k )
        c = cx**2 + cy**2 + cz**2 - self.rayon**2
        delta = b ** 2 - 4 * (a * c)
        '''
        print("Centre est: ", l, m, n)
        print("Rayon de vue est: ", i, j, k)
        print("Centre - Focale est: ",cx, cy, cz)
        print("a est: ", a)
        print("b est: ", b)
        print("c est: ", c)
        print("Delta est: ", delta, "\n")'''
        #x, y, z = (fx + i *t), (fy + j *t), (fz + k *t) #
        if( delta < 0):
	        return (0, 0, 50)
        t = - (b + delta**0.5) / (2 * a)

        return (fx+ i*t, fy+ j*t, fz+ k*t)

    def calcNorm(self, p):
        """Calcul de la normal d'un point d'intersection d'une sphere avec un rayon
        Calcul utilise lors des calcul de refractions."""
        return (vect.Vector(origin=self.pos, extremity=p)).normalize()
'''
M = (0.0, 9.0 - 1 / (2**0.5) , -4 - 1 /(2**0.5))

CAM = cam.Camera(11,11,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5.0)
P = Sphere(1, M, None, None, None, None, False)
P0 = (0.0, 5.0, 0.0)
I = P.calcIntersection(CAM, P0)
print(P.calcNorm(I))
'''
