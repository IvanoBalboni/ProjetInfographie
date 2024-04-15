import numpy as np
from PIL import Image
import vector as vect
import camera as cam
import plan
import color
import sphere

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
        for k in range(1, len(self.objects)):
            '''
            calcule l'intersection avec chaque objet et compare sur l'axe
            z quel est l'intersection la plus proche de la camera.
            '''
            (Tx, Ty, Tz) = self.objects[k].calcIntersection(self.cam, (x, y, 0))
            if( Tz <  0) and (Tz < Mz):
                (Mx, My, Mz) = (Tx, Ty, Tz)
                min = k
        if( Mz > 0):
            return COUL_FOND
        temp = self.objects[min]
        L = self.cam.ray( (Mx, My, Mz) )
        N = temp.calcNorm( (Mx, My, Mz) )
        #rint((Mx, My, Mz))
        LN = 0 #vector.VectscalarProduct(N)
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
        topleft_x = round(self.cam.pos[0]) - width//2
        topleft_y = round(self.cam.pos[1]) - height//2
        for i in range(topleft_x, topleft_x +width):
            for j in range(topleft_y, topleft_y +height):
                print(i,j)
                img.putpixel((topleft_x+i, topleft_y+j), (self.traceRay(i, j)))

        img.save(IMAGE)
        test = Image.open(IMAGE)





M = (0.0, 0.0, -50)
N = (-100.0, -100.0, -30)
K = (100.0, 100.0, -30)
CAM = cam.Camera(400,400,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 50)
P = sphere.Sphere(50, M, color.Color(255, 255, 0), None, None, None, False)
L = sphere.Sphere(50, N, color.Color(255, 0, 0), None, None, None, False)
S = sphere.Sphere(50, K, color.Color(0, 0, 255), None, None, None, False)

scene = Scene(CAM, [P,L,S], [], [1,1,1], IMAGE)

scene.draw(400, 400)
