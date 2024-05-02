import numpy as np
from PIL import Image
import vector as vect
import camera as cam
import plan
import color
import sphere
import light

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


    def traceRay(self, i, j, resolution):
        """Va trouver le point d'intersection chaque objet et trouver
        celle ce trouvant la plus proche. A partir de ca, la fonction
        va retourner la bonne couleur du pixel de l'image"""
        # 1er phase: Trouver un point d'intersection
        min = 0 # position de l'objet dans la liste d'objets
        (Mx, My, Mz) = self.objects[0].calcIntersection(self.cam, (i, j), resolution)
        #(x,y,0) le point P
        #print("Premier z = ", Mz)
        for k in range(1, len(self.objects)):
            '''
            calcule l'intersection avec chaque objet et compare sur l'axe
            z quel est l'intersection la plus proche de la camera.
            '''
            (Tx, Ty, Tz) = self.objects[k].calcIntersection(self.cam, (i, j), resolution)
            #print("Potentiel prochain z est: ", Tz)
            if( Tz <  0) and (Tz < Mz):
                (Mx, My, Mz) = (Tx, Ty, Tz)
                min = k
        if( Mz > 0):  # == Pas d'intersection trouve
            #print("pas d'intersection au pixel",i,j)
            return COUL_FOND
        # Fin 1er phase
        temp = self.objects[min]
        #2eme phase: Trouver le rayon reflechie  au point d'intersection Ri
        # R = 2(-I.N).N+I
        # Avec N norme du point d'intersection de l'objet
        # I rayon de Vue    IV
            
        #L = self.cam.ray( (Mx, My, Mz), resolution )
        
        N = temp.calcNorm( (Mx, My, Mz) )
        '''print("N: ", type(N))
        IV = self.cam.ray((i,j), resolution)
        test = (IV.scalarMult(-1)).scalarProduct(N)
        print("test: ", test)
        Ri = ( N.scalarMult( IV.scalarMult(-1).scalarProduct(N) *2 ) ).addition(IV)'''
        #print(N)
        print("intersection",(Mx, My, Mz),"objet:",min)
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
        #topleft_x = round(self.cam.pos[0]) - width//2
        #y = round(self.cam.pos[1]) + height//2
        '''
        dessin
        '''
        for i in range(width):
            for j in range(height):
                #print("POUR I J ", i, j, "X ET Y SONT ", x, y)
                img.putpixel((i, j), (self.traceRay(i, j, (width, height))))

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
# Pour plus de facilite, la taille de l'image = taille du dessin
W = 401  # Width
H = 401  # Height

# POsition des spheres
SP1 = (0.0, 0.0, -50)
SP2 = (-100.0, -100.0, -50)
SP3 = (100.0, 100.0, -50)

# Position des plans
PP1 = ((0.0, 0.25, -1.00), (0.0, 0.0, -50.0)) #Premier pour la norm, 2eme pour la pos du plan
 
# Position des lumieres
LP1 = (0.0, 100.0, -25)

#Calcul focale venant de https://stackoverflow.com/questions/18176215/how-to-select-focal-lengh-in-ray-tracing
F = round( (H/2) / np.tan(45/2) )

CAM = cam.Camera(W, H, (0.0, 0.0, 0.0), (0.0, 1.0, 0.0), F)

#Creation des objets
S1 = sphere.Sphere(50, SP1, color.Color(255, 255, 0), None, None, None, False)
S2 = sphere.Sphere(50, SP2, color.Color(255, 0, 0), None, None, None, False)
S3 = sphere.Sphere(50, SP3, color.Color(0, 0, 255), None, None, None, False)

P1 = plan.Plan(PP1[0], PP1[1], color.Color(0,250,0), None, None, None, False)

L1 = light.Light(LP1, color.Color(1, 1, 1))

scene = Scene(CAM, [S1, S2, S3, P1], [L1], [1,1,1], IMAGE)

scene.draw(100, 100)
