import numpy as np
import * from PIL
from PIL import Image

IMAGE = "rendu.png"

class Scene:
    def __init__(self, cam, objects, lights, ambLights, img):
        self.cam = cam
        self.objects = objects
        self.lights = lights
        self.ambLights = ambLights
        self.img = img


    def traceRay(self, x, y): # stocke chaque point d'intersection du rayon
        min = 0 # position de l'objet dans la liste d'objets
        (Mx, My, Mz) = self.objects[0].calcIntersection(self.cam, (x, y, 0))
        #(x,y,0) le point P
        for k in range(1, len(self.objects)):
            '''
            calcule l'intersection avec chaque objet et compare sur l'axe
            z quel est l'intersection la plus proche de la camera.
            '''
            (Tx, Ty, Tz) = self.objects[k].calcIntersection(self.cam, (x, y, 0))
            if( Tz < Mz):
                (Mx, My, Mz) = (Tx, Ty, Tz)
                min = k
        N = self.objets[min].calcNorm()
        Ir



    def draw(self, width, height):
        img = Image.new('RGB', (width, height), color = (100,60,100))

        '''
        dessin
        '''

        for i in range(width):
            for j in range(height):


            pass
        img.save(IMAGE)





M = (0.0, 0.0, -10.0)
N = (0.0, -1.0, 1.00)

cam = cam.Camera(11,11,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5.0)
P = Plan(N, M, None, None, None, None, False)
P0 = (0.0, 5.0, 0.0)

scene = Scene(cam, [P], [], [1,1,1], IMAGE)
