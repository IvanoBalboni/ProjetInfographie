import numpy as np

class Vector():

	def __init__(self, **kwargs):
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
		return Vector(vec = np.add(self.vec,v2))

	def subtract(self, v2):
		return Vector(vec = np.subtract(self.vec,v2))

	def scalarMult(self, s):
		return Vector(vec = np.multiply(self.vec,s))

	def scalarProduct(self, v2):
		print(self.vec,"   ",v2)
		return np.dot(self.vec,v2)

	def vectorProduct(self, v2):
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
