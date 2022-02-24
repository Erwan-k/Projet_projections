
"""
Ce code va permettre d'afficher les surfaces représentatives de fonctions données.
Plus précisément, il va permettre de générer un ensemble de segments que l'on souhaitera afficher

Ici, les fonctions f et g sont définies.
On va aussi définir la zone de points autour de laquelle on veut l'observer : points et 
etendu_x, etendu_y ainsi que le nombre de points de maille.

J'ajoute seg1 qui permettra d'afficher les axes x, y et z.
"""

from math import exp
from utils import creation_des_segments_a_afficher
from utils import afficher_vue_rotation_autour_z_depuis_distance_r_hauteur_h

from os import getcwd,chdir,mkdir,listdir
if not os.getcwd()[-6:] != "sortie":
    if not os.listdir().count("sortie"):
        os.mkdir("sortie")
    os.chdir("./sortie")

### Définition des fonctions que l'on veut afficher

def f(x,y):
    return (x**2-y**2)*exp(-(x**2+y**2))

def g(x,y):
    #return -exp(-1)+x**2+(y-1)**2 #approximation en (1;0)
    return -exp(-1)+x**2+(y+1)**2 #approximation en (0;1)
    #return x**2-y**2 #approximation en (0;0)
    #return exp(-1)-(x+1)**2-y**2 #approximation en (-1;0)
    #return exp(-1)-(x-1)**2-y**2 #approximation en (0;-1)


#Préparation des segments pour l'affichage des axes
seg1 = [[[-10**6,0,0],[10**6,0,0]],
        [[0,-10**6,0],[0,10**6,0]],
        [[0,0,-10**6],[0,0,10**6]]]

point = [0,0]
etendue_x,etendue_y = 2.5,2.5
nombre_de_mailles = 71
seg2 = creation_des_segments_a_afficher(f,etendue_x,etendue_y,point,nombre_de_mailles)

point = [0,-1]
etendue_x,etendue_y = 2.5,2.5
nombre_de_mailles = 81
seg3 = creation_des_segments_a_afficher(g,etendue_x,etendue_y,point,nombre_de_mailles)

segments =  [{"nom":"axes","seg":seg1,"couleur":"k","epaisseur":0.5},
             {"nom":"fonction","seg":seg2,"couleur":"b","epaisseur":1},
             {"nom":"approximation","seg":seg3,"couleur":"r","epaisseur":1}]
segments = [segments[0],segments[2],segments[1]]

nbr_prises = 201 #Nombre de prises de vues au cours de la rotation
axes = [-3,3,-0.7,0.7] #Ce sont les axes de l'image renvoyée par matplotlib qui n'a pas conscience du processus de projection/rotation que l'on a implémenté
r,h = 3,0.3
afficher_vue_rotation_autour_z_depuis_distance_r_hauteur_h(segments,nbr_prises,r,h,axes)

















