import numpy as np
import object as obj
import camera as cam
import vector as vect

class Plan(obj.Object):
	def __init__( self, norm, pos, color, diffus, speculos, ambiant, shadow):
		obj.Object.__init__(self, pos, color, diffus, speculos, ambiant, shadow)
		self.norm = vect.Vector(vec=norm)


	def calcNorm(self, p):
		return self.norm

	def calcIntersection(self, origin_coor, chosen_ray):
		(A, B, C) = self.norm # vecteur traversant le plan
		(x, y, z) = self.pos # point definissant le plan
		(i, j, k) = chosen_ray.vec # rayon de vue
		(fx, fy, fz) = origin_coor # origine du point de vue

        # Nous cherchons à trouver notre point d'intersection avec le plan
        # en utilisant V = M + t*D1 avec M un point du rayon de vue D1
        # Pour cela nous avons besoin de t = A.x1 + B.y1 + C.z1 + D2 / A.i + B.j + C.k
        # Premier calcul retrouver D2:
        # Ax + By + Cz + D = 0
		D = -(A*x) -(B*z) -(C*y)
		div = (A*i + B*j + C*k)

		#renvoie None si le rayon de vue est trop "parallele" au plan
		# ou n'atteind jamais le plan
		angle = self.norm.scalarProduct(chosen_ray.normalize())
		if angle > -0.08 or div ==0:
			return None

        # Deuxieme calcul: t
		t =  -(A*fx + B*fy + C*fz +D) / div
        # Dernier calcul: notre point d'intersection
		(r1, r2, r3) = (fx + t*i, fy + t*j, fz + t*k)

		return (r1, r2, r3)


'''
M = (0.0, 0.0, -10.0)
N = (0.0, -1.0, 1.00)

CAM = cam.Camera(11,11,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5.0)
P = Plan(N, M, None, None, None, None, False)
P0 = (0.0, 5.0, 0.0)
'''
