import numpy as np
from PIL import Image
import vector as vect
import camera as cam
import plan
import color

IMAGE = "rendu.png"
COUL_FOND = (30, 30, 30)

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
        comp = 0
        for k in range(1, len(self.objects)):
            '''
            calcule l'intersection avec chaque objet et compare sur l'axe
            z quel est l'intersection la plus proche de la camera.
            '''
            (Tx, Ty, Tz) = self.objects[k].calcIntersection(self.cam, (x, y, 0))
            if( Tz < Mz):
                (Mx, My, Mz) = (Tx, Ty, Tz)
                min = k
            comp += min
        temp = self.objects[min]
        print(comp)
        L = self.cam.ray( (Mx, My, Mz) )
        N = temp.calcNorm()
        LN = L.scalarProduct(N)
        Ks = temp.specular
        Kd = temp.diffus
        Ia = temp.ambiant
        C = self.objects[min].color
        r,g,b = round(C.r +LN), round(C.g +LN), round(C.b +LN)



        return (r, g, b)


    def draw(self, width, height):
        img = Image.new('RGB', (width, height), color = (100,60,100))

        '''
        dessin
        '''

        for i in range(width):
            for j in range(height):
                img.putpixel((i, j), (self.traceRay(i, j)))

        img.save(IMAGE)
        test = Image.open(IMAGE)





M = (50.0, 50.0, -50.0)
N = (0.0, 1.0, 2.00)
N2 = (1.0, 1.0, 1.5)

C = cam.Camera(400,400,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5.0)
P = plan.Plan(N, M, color.Color(0, 255, 255), None, None, None, False)
P2 = plan.Plan(N2, M, color.Color(255, 255, 0), None, None, None, False)
P0 = (0.0, 5.0, 0.0)

scene = Scene(C, [P,P2], [], [1,1,1], IMAGE)

scene.draw(400, 400)
