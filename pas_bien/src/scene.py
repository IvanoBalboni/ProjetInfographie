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
    """Classe qui va nous cree l'image finale. """
    def __init__(self, cam, objects, lights, ambLights, img):
        self.cam = cam
        self.objects = objects
        self.lights = lights
        self.ambLights = ambLights
        self.img = img


    def traceRay(self, x, y):
        """Va trouver le point d'intersection chaque objet et trouver
        celle ce trouvant la plus proche. A partir de ca, la fonction
        va retourner la bonne couleur du pixel de l'image"""
        min = 0 # position de l'objet dans la liste d'objets
        (Mx, My, Mz) = self.objects[0].calcIntersection(self.cam, (x, y, 0))
        #(x,y,0) le point P
        #print("Premier z = ", Mz)
        for k in range(1, len(self.objects)):
            '''
            calcule l'intersection avec chaque objet et compare sur l'axe
            z quel est l'intersection la plus proche de la camera.
            '''
            (Tx, Ty, Tz) = self.objects[k].calcIntersection(self.cam, (x, y, 0))
            #print("Potentiel prochain z est: ", Tz)
            if( Tz <  0) and (Tz < Mz):
                (Mx, My, Mz) = (Tx, Ty, Tz)
                min = k
        if( Mz > 0):
            return COUL_FOND
        temp = self.objects[min]
        L = self.cam.ray( (Mx, My, Mz) )
        N = temp.calcNorm( (Mx, My, Mz) )
        print(N)
        #rint((Mx, My, Mz))
        LN = 0 #L.scalarProduct(N)
        Ks = temp.specular
        Kd = temp.diffus
        Ia = temp.ambiant
        C = self.objects[min].color
        r,g,b = round(C.r +LN), round(C.g +LN), round(C.b +LN)



        return (r, g, b)


    def draw(self, width, height):
        """Va faire l'appel recursif pour chaque pixel de notre image """
        img = Image.new('RGB', (width, height), color = (100,60,100))
        #P0 = [-(width/2-0.5), height/2-0.5]  # Base utilisee pour tout les suivant
        '''
        dessin
        '''
        topleft_x = round(self.cam.pos[0]) - width//2
        y = round(self.cam.pos[1]) + height//2
        for i in range(width):
            x = topleft_x
            for j in range(height):
                #print("POUR I J ", i, j, "X ET Y SONT ", x, y)
                img.putpixel((i, j), (self.traceRay(x, y)))
                x +=1
            y-=1

        img.save(IMAGE)
        test = Image.open(IMAGE)




'''
M = (0.0, 0.0, -3)
N = (-2.0, -2.0, -5)
K = (2.0, 2.0, -5)
CAM = cam.Camera(7,7,(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 5)
P = sphere.Sphere(1, M, color.Color(255, 255, 0), None, None, None, False)
L = sphere.Sphere(1, N, color.Color(255, 0, 0), None, None, None, False)
S = sphere.Sphere(1, K, color.Color(0, 0, 255), None, None, None, False)
'''

M = (0.0, 0.0, -50)
N = (-100.0, -100.0, -50)
K = (100.0, 100.0, -50)
W = 401
H = 401
F = round( (H/2) / np.tan(45/2) )
CAM = cam.Camera(W, H, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), F)
P = sphere.Sphere(50, M, color.Color(255, 255, 0), None, None, None, False)
L = sphere.Sphere(50, N, color.Color(255, 0, 0), None, None, None, False)
S = sphere.Sphere(50, K, color.Color(0, 0, 255), None, None, None, False)

scene = Scene(CAM, [P,L,S], [], [1,1,1], IMAGE)

scene.draw(W, H)
