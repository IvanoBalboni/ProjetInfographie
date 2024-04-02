import numpy as np
import color as col

class Object():
	def __init__(self, pos=(0,0,0), color, diffus, speculos, ambiant, shadow=False):
		self.pos = pos
		self.color = color
		self.diffus = diffus
		self.speculos = speculos
		self.ambiant = ambiant
		self.shadow = shadow
	
	def Intersection(self, campos, rayon):
		return np.subtract(self.pos, campos)
	
	def Norm(self, )
		
