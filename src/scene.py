import numpy as np
from PIL import Image
import time

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

    def closest_inter(self, origin_coor, chosen_ray):
        """Va trouver le point d'intersection chaque objet et trouver
        celle ce trouvant la plus proche. A partir de ca, la fonction
        va retourner la bonne couleur du pixel de l'image"""
        min = 0 # position de l'objet dans la liste d'objets
        M = self.objects[0].calcIntersection(origin_coor, chosen_ray)
        if M is not None:
            min = 0
        else:
            min = None
        #(x,y,0) le point P
        #print("Premier z = ", Mz)
        for k in range(1, len(self.objects)):
            '''
            calcule l'intersection avec chaque objet et compare sur l'axe
            z quel est l'intersection la plus proche de la camera.
            '''
            T = self.objects[k].calcIntersection(origin_coor, chosen_ray)
            if T is not None:
                #print("Potentiel prochain z est: ", Tz)
                if min is not None:
                    FT = vect.Vector(origin =chosen_ray.vec, extremity =T)
                    FM = vect.Vector(origin =chosen_ray.vec, extremity =M)
                    #print(M, TM)
                    #vu que les intersections sont sur la meme droite on peut tester
                    #la direction du vecteur TM pour determiner le plus proche
                    if FT.norm() > FM.norm():
                        min = k
                        M = T
                else:
                    min = k
                    M = T
        if min is None:
            return None
        return (M, min)

    def traceRay(self, origin_coor, chosen_ray):
        # 1er phase: Trouver un point d'intersection ################
        test_inter = self.closest_inter(origin_coor, chosen_ray)

        #print(coor_inter, obj_min)
        if test_inter is None:  # == Pas d'intersection trouve
            #print("pas d'intersection au pixel",i,j)
            return COUL_FOND
        # Fin 1er phase #####################
        coor_inter = test_inter[0]
        obj_min = test_inter[1]

        temp = self.objects[obj_min]
        # Parametre lumiere des obj_min: /!\ ce sont des constantes compris entre 0 et 1
        Ks = temp.specular
        Kd = temp.diffus
        Ka = temp.ambiant

        N = temp.calcNorm( coor_inter ) # Norme de l'obj_min
        #print("N: ", type(N))

        # Methode vu dans https://omaraflak.medium.com/ray-tracing-from-scratch-in-python-41670e6a96f9 :
        # Pour les prochains calculs traceRay de notre objet,
        # Afin d'éviter les risques que notre objet soit compter comme une intersection
        # Nous rajoutons deplacons légérement notre intersection suivant la normale de l'objet
        small_change = N.scalarMult(1e-5)
        coor_inter_ray = (small_change[0] + coor_inter[0], small_change[1] + coor_inter[1], small_change[2] + coor_inter[2])
        # /!\ Les coordonnees ne sont pas des vecteurs
        #print("Coor inter", coor_inter)
        #print("Coor inter ray", coor_inter_ray)

        # 2eme phase: Trouver le rayon reflechie  au point d'intersection Ri ####
        # R = 2(-I.N).N+I
        # Avec N norme du point d'intersection de l'objet
        # I rayon de Vue    IV

        #L = self.cam.ray( (Mx, My, Mz), resolution )

        IV = chosen_ray # Rayon vue depuis la camera
        L = IV.normalize()
        #print("type est", type(IV))
        '''test1 = IV.scalarMult(-1)  #.scalarProduct(N)
        print("test: ", test1)
        test2 = test1.scalarProduct(N)'''
        # Rayon reflechi en P :
        Ri = ( N.scalarMult( IV.scalarMult(-1).scalarProduct(N) *2 ) ).addition(IV)
        #print(Ri)
        #Cr = np.multiply(self.traceRay(coor_inter_ray, Ri), (Ks))
        #print(Cr)

        # Fin 2eme phase #################

        # 3eme phase: coefficient de transmission de l'objets #####

        # Refraction pour les objets transparents -> Ct

        # Fin 3eme phase ###########

        # 4eme phase: Calcul de l'ombre + composante diffus ############

        Id = (0, 0, 0)  #Couleur noire
        for i in range(len(self.lights)):
            L = (vect.Vector(origin = self.lights[i].pos, extremity = coor_inter)).normalize()
            LN = L.scalarProduct(N)
            #couleur de lumiere pas sur de laisser
            if obj_min == self.closest_inter(self.lights[i].pos, L)[1]:
                col = self.lights[i].color
                r,g,b = col.r, col.g, col.b
                r,g,b = r*LN, g*LN, b*LN
                Ir,Ig,Ib = Id
                Id = (Ir+r, Ig+g, Ib+b)

            #Il = vect.Vector(origin = coor_inter, extremity = self.lights[i].pos)
            #Rl = ( N.scalarMult( Il.scalarMult(-1).scalarProduct(N) *2 ) ).addition(Il)
            #closest_obj = self.closest_inter(coor_inter_ray, Rl) # Trouve l'element le plus proche
            # Find the distance between the two points
            #dist_light = np.sqrt(np.sum(np.square(np.subtract(self.lights[i].pos, coor_inter))))
            #print("DISTANCE OBJECT LIGHT", dist_light)
            #dist_obj = np.sqrt(np.sum(np.square(np.subtract(closest_obj[0], coor_inter))))
            #print("DISTANCE OBJECT OBJ", dist_obj, obj_min)
            """
            if dist_light < dist_obj:
                Id = (255,255,255)
            else:
                Id = (0,0,0)
            """
        print(Id)
        #Cr = np.multiply(self.traceRay(coor_inter_ray, Ri), (Ks))

        # Fin 4eme phase ########################


        #print("intersection", coor_inter, "objet:", obj_min)
        #print("LN",LN)
        #print("Kd",Kd)
        Io = self.objects[obj_min].color
        #print("Io",Io)
        #print("Id",Id[0],Id[1],Id[2])

        # 5eme phase: Addition de toutes les couleurs ############
        r,g,b = round(Io.r*(Ka + Kd*Id[0])), round(Io.g*(Ka + Kd*Id[1])),round(Io.b*(Ka + Kd*Id[2]))
        vec_color = vect.Vector(vec = (r, g, b))
        vec_color = vec_color.normalize()
        # Fin 5eme phase ##############################
        #print("Before", Io.r, Io.g, Io.b)
        #print("Middle", r, g, b)
        #print("After", vec_color)

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
        print("Debut boucle draw")
        drawStart = time.time()
        for i in range(width):
            for j in range(height):
                #print("POUR I J ", i, j, "X ET Y SONT ", x, y)
                origin_coor = self.cam.F
                #print("F in draw", origin_coor)
                true_ray = self.cam.ray((i, j), (width, height))
                #print("In draw type is", type(true_ray))
                #print("from draw", true_ray)
                img.putpixel((i, j), (self.traceRay(origin_coor, true_ray)))
        print("duree draw",time.time()-drawStart)

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
SP1 = (0.0, 0.0, -49)
SP2 = (-100.0, -100.0, -50)
SP3 = (100.0, 100.0, -50)

# Position des plans
PP1 = ((0.0, 0.25, 1.00), (0.0, -12.5, -50.0)) #Premier pour la norm, 2eme pour la pos du plan
PP2 = ((0.0, -0.25, 1.00), (0.0, 12.5, -50.0))
# Position des lumieres
LP1 = (0.0, 100.0, -50.0)

#Calcul focale venant de https://stackoverflow.com/questions/18176215/how-to-select-focal-lengh-in-ray-tracing
F = round( (H/2) / np.tan(45/2) )

CAM = cam.Camera(W, H, (0.0, 0.0, 0.0), (0.0, 1.0, 0.0), F)

#Creation des objets (rayon, pos, color, diffus, specular, ambiant, shadow)
S1 = sphere.Sphere(50, SP1, color.Color(255, 255, 0), 0.3, 0.5, 0.3, False)
S2 = sphere.Sphere(50, SP2, color.Color(255, 0, 0), 0.3, 0.5, 0.5, False)
S3 = sphere.Sphere(50, SP3, color.Color(0, 0, 255), 0.3, 0.5, 0.5, False)

P1 = plan.Plan(PP1[0], PP1[1], color.Color(0,255,0), 0.5, 0.5, 0.5, False)
P2 = plan.Plan(PP2[0], PP2[1], color.Color(150,0,155), 0.5, 0.5, 0.5, False)

L1 = light.Light(LP1, color.Color(255, 255, 255))

scene = Scene(CAM, [S1, S2, S3], [L1], [1,1,1], IMAGE)  #, S2, S3, P1

scene.draw(300, 300)
