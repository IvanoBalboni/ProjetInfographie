import object as obj

class Sphere(obj.Object):
	def __init__(self, rayon, pos=(0,0,0), color, diffus, speculos, ambiant, shadow=False):
		Object.__init__(pos=(0,0,0), color, diffus, speculos, ambiant, shadow=False)
		self.rayon = rayon
		
	def Intersection(self, campos):
		
