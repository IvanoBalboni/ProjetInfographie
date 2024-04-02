import numpy as np

class Vector():
	
	def __init__( self, origin=(0.0,0.0,0.0), extremity=(0.0,0.0,0.0) ):
		self.vec = np.subtract(extremity,origin)
		
	def Addition(self, v2):
		return np.add(self.vec,v2)
	
	def Subtract(self, v2):
		return np.subtract(self.vec,v2)
		
	def ScalarMult(self, s):
		return np.multiply(self.vec,s)
	
	def ScalarProduct(self, v2):
		return np.dot(self.vec,v2)
		
	def VectorProduct(self, v2):
		return np.cross(self.vec,v2)
	
	def Norm(self):
		return np.linalg.norm(self.vec)
	
	def Normalize(self):
		n = self.Norm()
		return np.divide(self.vec,n)
		

v1 = (1.0,2.0,3.0)
v2 = (4.0,5.0,6.0)
va = Vector(v1,v2)
vb = Vector(v2, v1)

print(va.Addition(vb.vec))
print(va.Subtract(vb.vec))
print(va.ScalarMult(5))
print(va.ScalarProduct(vb.vec))
print(va.VectorProduct(vb.vec))
print(va.Norm())
print(va.Normalize())




