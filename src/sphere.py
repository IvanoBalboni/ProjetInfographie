import object as obj
import camera as cam
import vector as vect

class Sphere(obj.Object):
    """Classe qui va nous cree une sphere et nous permettre de trouver son intersection."""
    def __init__(self, rayon, pos, color, diffus, specular, ambiant, shadow):
        obj.Object.__init__(self, pos, color, diffus, specular, ambiant, shadow)
        self.rayon = rayon

    def calcIntersection(self, origin_coor, chosen_ray):
        (l,m,n) = self.pos # centre de la sphere
        (i, j, k) = chosen_ray.vec # rayon de vue 
        (fx, fy, fz) = origin_coor # point faisant partie du rayon de vue
        cx, cy, cz = (fx-l), (fy-m), (fz-n) # (x-l) (y-m) (z-n)

        # On cherche tous les resultats pour faire a*t^2 + b*t + c
        # On utilise l'eq implicite des plans pour x, y et z sous la forme
        # M + tD avec M un point du rayon de vue D
        # On prend tous les D^2 pour a
        # tous les 2*D*(M+l/m/n) pour b
        # tous les (M+l/m/n)^2 - r^2 pour c
        a = i**2 + j **2 + k **2
        b = 2 * (cx *i + cy*j + cz *k )
        c = cx**2 + cy**2 + cz**2 - self.rayon**2
        
        # Calcul de delta pour savoir combien nous avons de solutions
        delta = b ** 2 - 4 * a * c
        if delta < 0:
            return None
        elif delta == 0:
            t = -b / (2*a)
            return (fx+ i*t, fy+ j*t, fz+ k*t)
        else:
            #Premiere solution
            t1 = (-b + delta**0.5) / (2 * a)
            s1 = (fx+ i*t1, fy+ j*t1, fz+ k*t1)
            vec1 = vect.Vector(origin = origin_coor, extremity = s1 )
            #Seconde solution
            t2 = (-b - delta**0.5) / (2 * a)
            s2 = (fx+ i*t2, fy+ j*t2, fz+ k*t2)
            vec2 = vect.Vector(origin = origin_coor, extremity = s2 )
            #print("Choix entre s1 et s2 ", s1, s2)
            #Comparaison pour renvoyer le plus petit == plus proche de la cam
            if vec2.norm() > vec1.norm():
                return s1
            else:
                return s2

    def calcNorm(self, intersection):
        '''Calcul de la normal d'un point d'intersection d'une sphere avec un rayon
        Calcul utilise lors des calculs de refractions.'''
        return (vect.Vector(origin=self.pos, extremity=intersection)).normalize()

'''
M = (0.0, 9.0 - 1 / (2**0.5) , -4 - 1 /(2**0.5))

CAM = cam.Camera(11,11,(0.0, 0.0, 0.0), (0.0, 1.0, 0.0), 5.0)
P = Sphere(1, M, None, None, None, None, False)
P0 = (5,0)
I = P.calcIntersection(CAM, P0, (11,11))
print(I)
print(P.calcNorm(I))'''
