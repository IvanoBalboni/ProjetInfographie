import numpy as np
import object as obj
import camera as cam
import vector as vect

class Plan(obj.Object):
	def __init__( self, norm, pos, color, diffus, speculos, ambiant, shadow):
		obj.Object.__init__(self, pos, color, diffus, speculos, ambiant, shadow)
		self.norm = norm


	def calcNorm(self):
		return self.norm

	def calcIntersection(self, camera, p):
		(A, B, C) = self.norm # vecteur traversant le plan
		(x, y, z) = self.pos # point definissant le plan : M
		(i, j, k) = camera.ray(p).vec # rayon de vue : FP
		(fx, fy, fz) = camera.F # focale : F

		D = (A*x) +(B*z) +(C*y)
		div = (A*i + B*j + C*k)
		if div == 0:
			return (0, 0, 0)

		t =  - (A*fx + B*fy + C*fz +D) / div

		(r1, r2, r3) = (fx + t*i,fy + t*j, fz + t*k)

		return (r1, r2, r3)


'''
M = (0.0, 0.0, -10.0)
N = (0.0, -1.0, 1.00)

CAM = cam.Camera(11,11,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5.0)
P = Plan(N, M, None, None, None, None, False)
P0 = (0.0, 5.0, 0.0)
'''
