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
COUL_FOND = (130, 130, 130)

class Scene:
    """Classe qui va nous cree l'image finale. """
    def __init__(self, cam, objects, lights, ambLights, img):
        self.cam = cam
        self.objects = objects
        self.lights = lights
        self.ambLights = ambLights
        self.img = img

    def closest_inter(self, origin_coor, chosen_ray, skip):
        """Va trouver le point d'intersection chaque objet et trouver
        celle ce trouvant la plus proche. A partir de ca, la fonction
        va retourner la bonne couleur du pixel de l'image"""
        '''min = 0 # position de l'objet dans la liste d'objets
        M = self.objects[0].calcIntersection(origin_coor, chosen_ray)
        if M is not None:
            min = 0
        else:
            min = None'''
        #(x,y,0) le point P
        #print("Premier z = ", Mz)
        
        min = None
        M = None
        k = 0
        while k < len(self.objects):
        #for k in range(1, len(self.objects)):
            '''
            Calcul l'intersection avec chaque objet et compare sur l'axe
            z quel est l'intersection la plus proche de la camera.
            '''
            if k != skip:
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
            k += 1
        if min is None:
            return None
        #print("Chosen is ", M)
        return (M, min)

    def traceRay(self, origin_coor, chosen_ray, skip):
        # 1er phase: Trouver un point d'intersection ################
        test_inter = self.closest_inter(origin_coor, chosen_ray, skip)

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
        Ri = ( N.scalarMult( L.scalarMult(-1).scalarProduct(N) *2 ) ).addition(L)
        #print("NB RECURSION", obj_min)
        Cr = np.multiply(self.traceRay(coor_inter, Ri, obj_min), (Ks))
        #print(Cr)

        # Fin 2eme phase #################

        # 3eme phase: coefficient de transmission de l'objets #####

        # Refraction pour les objets transparents -> Ct

        # Fin 3eme phase ###########

        # 4eme phase: Calcul composante diffus et speculaire ############

        Id = 0  #Couleur noire
        spec = 0
        for i in range(len(self.lights)):
            
            # Calcul composante speculaire ###############
            # Ks * (R . V)**n avec R rayon reflechie vers la lumiere
            # V rayon de vue et n le coefficient de surbrillance
            n = 10
            L = (vect.Vector(origin = coor_inter, extremity = self.lights[i].pos)).normalize() # Rayon vers lum
            Rl = ( N.scalarMult( L.scalarMult(-1).scalarProduct(N) *2 ) ).addition(L) # Rayon reflechie vers la lum
            #print("Rl is and then N and hteir product", Rl, IV.normalize(), Rl.scalarProduct(IV.normalize()))
            spec = spec + np.power((Rl.normalize()).scalarProduct(IV.normalize()), n)
            
            
            
            # Partie diffusion
            closest_obj = self.closest_inter(coor_inter, L, obj_min) # Trouve l'element le plus proche
            LN = L.scalarProduct(N)
            # Calcul des distances pour savoir si l'intersection la plus proche est avant ou apres
            # la lumiere:
            if closest_obj != None:  
                dist_light = np.sqrt(np.sum(np.square(np.subtract(self.lights[i].pos, coor_inter))))
                dist_obj = np.sqrt(np.sum(np.square(np.subtract(closest_obj[0], coor_inter))))
                '''print("Obj is", obj_min)
                print("Coor init", coor_inter)
                print("Coor lum", self.lights[i].pos)
                print("Coor obj", closest_obj[0]) 
                print("Rl est", Rl)'''
            #couleur de lumiere pas sur de laisser
            #if obj_min == self.closest_inter(self.lights[i].pos, L)[1]:
            if ((closest_obj == None) or (dist_light < dist_obj)) and LN>0:  # Si aucune intersection ou lumiere + proche
                # Si LN est < 0 alors on va avoir du noir car on aura multiplier par exemple un 255* - quelque chose
                # Ce qui rend impossible l'addition par la suite
                '''print("Obj is", obj_min)
                print("Coor init", coor_inter)
                print("Coor lum", self.lights[i].pos)
                print("Coor obj", 0 if (closest_obj == None) else closest_obj[0]) '''
                '''if coor_inter[0] < -100 and coor_inter[1] < -100:
                    print("Coor ", coor_inter)
                    print("Welp LN ", LN)'''
                '''col = self.lights[i].color
                col_r, col_g, col_b = col.r, col.g, col.b
                
                new_r, new_g, new_b = col_r*LN, col_g*LN, col_b*LN
                Ir,Ig,Ib = Id
                Id = (Ir+new_r, Ig+new_g, Ib+new_b)'''
                Id = Id + LN


        #print(Id)
        #Cr = np.multiply(self.traceRay(coor_inter_ray, Ri), (Ks))

        # Fin 4eme phase ########################
        
        Io = self.objects[obj_min].color  # Couleur de l'objet
        Ii = (0.9, 0.9, 0.9)  # Intensite à la lumiere
        
        spec_rgb = Ks*spec  # Lumiere speculaire
        
        #print(Cr)
        #print("Testis ", test, "then specular is ", spec_rgb)
        #print("Then global ", Ka*self.ambLights[0] + Id[0] + spec_rgb)
        

        #print("intersection", coor_inter, "objet:", obj_min)
        #print("LN",LN)
        #print("Kd",Kd)
        
        #print("Io",Io)
        #print("Id",Id[0],Id[1],Id[2])
        #print("Ka puis ambLights puis produit", Ka, self.ambLights[2], Ka*self.ambLights[2])
        #print("Id pour etre sure et LN...", Id, LN)
        
        
        # 5eme phase: Addition de toutes les couleurs ############
        # Nous utilisons le modele de Phong:
        # Io Ia ka + Ii( Io kd( L.N) + ks( R.V)**n)
        
        r = round(Io.r*Ka*self.ambLights[0] + Ii[0]*(Io.r*Kd*Id + Ii[0]*spec_rgb) + Cr[0])
        g = round(Io.g*Ka*self.ambLights[1] + Ii[1]*(Io.g*Kd*Id + Ii[1]*spec_rgb) + Cr[1])
        b = round(Io.b*Ka*self.ambLights[2] + Ii[2]*(Io.b*Kd*Id + Ii[2]*spec_rgb) + Cr[2])
        pix_rgb = color.Color(r, g, b)
        pix_rgb.norm_color()
        """vec_color = vect.Vector(vec = (r, g, b))
        vec_color = vec_color.normalize()
        vec_color = vec_color.scalarMult(255)"""
        # Fin 5eme phase ##############################
        #print("Before", Io.r, Io.g, Io.b)
        #print("Middle", r, g, b)
        #print("After", vec_color.vec[0])
        
        return r, g, b


    def draw(self, width, height):
        """Va faire l'appel recursif pour chaque pixel de notre image """
        img = Image.new('RGB', (width, height), color = (100,60,100))
        
        print("Debut boucle draw")
        drawStart = time.time()
        for i in range(width):
            for j in range(height):
                #print("POUR I J ", i, j)
                origin_coor = self.cam.F  # Utilisation de la focale pour nos calcul
                #print("F in draw", origin_coor)
                true_ray = self.cam.ray((i, j), (width, height))
                #print("In draw type is", type(true_ray))
                #print("from draw", true_ray)
                img.putpixel((i, j), (self.traceRay(origin_coor, true_ray, len(self.objects))))
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
SP1 = (0.0, 0.0, -50)
SP2 = (-100.0, 0.0, -50)
SP3 = (100.0, 0.0, -50)

# Position des plans
PP1 = ((0.0, 1.0, 0.0), (0.0, -50.0, 0.0)) #Premier pour la norm, 2eme pour la pos du plan
PP2 = ((0.0, -0.25, 1.00), (0.0, 12.5, -50.0))
# Position des lumieres
LP1 = (0.0, 100.0, -50.0)
LP2 = (0.0, -100.0, -50.0)

#Calcul focale venant de https://stackoverflow.com/questions/18176215/how-to-select-focal-lengh-in-ray-tracing
F = round( (H/2) / np.tan(45/2) )

CAM = cam.Camera(W, H, (0.0, 0.0, 0.0), (0.0, 1.0, 0.0), F)

#Creation des objets (rayon, pos, color, diffus, specular, ambiant, shadow)
S1 = sphere.Sphere(50, SP1, color.Color(255, 255, 0), 0.5, 0.3, 0.2, False)
S2 = sphere.Sphere(50, SP2, color.Color(255, 0, 0), 0.8, 0.1, 0.1, False)
S3 = sphere.Sphere(50, SP3, color.Color(0, 0, 255), 0.5, 0.3, 0.2, False)

P1 = plan.Plan(PP1[0], PP1[1], color.Color(0,255,0), 0.5, 0.5, 0.5, False)
P2 = plan.Plan(PP2[0], PP2[1], color.Color(150,0,155), 0.5, 0.5, 0.5, False)

L1 = light.Light(LP1, color.Color(255, 255, 255))
L2 = light.Light(LP2, color.Color(255, 255, 255))

scene = Scene(CAM, [S1, S2, S3], [L1, L2], [1,1,1], IMAGE)  #, S2, S3, P1

scene.draw(300, 300)
