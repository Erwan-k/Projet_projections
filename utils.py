
from math import sin,cos,atan2,pi
import matplotlib.pyplot as plt
from copy import deepcopy
from numpy import linspace

### Faire une rotation d'angle teta d'un vecteur Vect autour du vecteur U

def normer(U):
    s = sum([i**2 for i in U])**(1/2)
    return [U[0]/s,U[1]/s,U[2]/s]

def rechercher_V_orthogonal_à_(U):
    return [0 if i else 1 for i in U] if U.count(0) else [-U[2],0,U[0]]

def produit_vectoriel(U,V):
    return [U[1]*V[2]-V[1]*U[2],U[2]*V[0]-V[2]*U[0],U[0]*V[1]-V[0]*U[1]]

def produit_matriciel(A,B):
    return [[sum([A[i][k]*B[k][j] for k in range(len(A[0]))]) for j in range(len(B))] for i in range(len(A))]

def produit_matrice_vecteur(A,B):
    return [A[0][0]*B[0]+A[0][1]*B[1]+A[0][2]*B[2],A[1][0]*B[0]+A[1][1]*B[1]+A[1][2]*B[2],A[2][0]*B[0]+A[2][1]*B[1]+A[2][2]*B[2]]

def rotation_d_angle_teta_autour_de_U(Vect,U,teta):
    U = normer(U)
    V = rechercher_V_orthogonal_à_(U)
    V = normer(V)
    W = produit_vectoriel(U,V) #Le produit vectoriel de deux vecteurs normés est normé
    P = [[U[0],V[0],W[0]],[U[1],V[1],W[1]],[U[2],V[2],W[2]]]
    Pinv = [U,V,W] #P est la matrice de changement de la base canonique vers une BON
    M = [[1,0,0],[0,cos(teta),-sin(teta)],[0,sin(teta),cos(teta)]]
    R = produit_matriciel(P,produit_matriciel(M,Pinv)) #R = PMP**(-1)
    return produit_matrice_vecteur(R,Vect)

### Projections : sur P parallèlement à D ; sur P et orthogonale ; sur (Oyz) et orthogonale

def projection_sur_P_parallellement_a_D(n,u,pt):
    s = n[0]*u[0]+n[1]*u[1]+n[2]*u[2]
    return [pt[0]-(pt[0]*n[0]*u[0]/s+pt[1]*n[1]*u[0]/s+pt[2]*n[2]*u[0]/s),pt[1]-(pt[0]*n[0]*u[1]/s+pt[1]*n[1]*u[1]/s+pt[2]*n[2]*u[1]/s),pt[2]-(pt[0]*n[0]*u[2]/s+pt[1]*n[1]*u[2]/s+pt[2]*n[2]*u[2]/s)]

def projection_ortho_sur_P_dirige_par_u_(u,pt): #Superflu
    return projection_sur_P_parallellement_a_D(u,u,pt)

def projection_ortho_sur_oyz(pt): #Superflu
    return projection_ortho_sur_P_dirige_par_u_([1,0,0],pt)

### Processus d'affichage

def afficher_vue_depuis_le_point_u(segment,u,couleur,epaisseur):
    seg = deepcopy(segment) #Je suis pas sur que ce soit nécessaire
    
    ##Je cherche les coordonnées shpériques de u
    #Je cherche un vecteur orthogonal a u et son projeté sur Oxy
    ortho_n = produit_vectoriel(u,[u[0],u[1],0])
    
    #Je récupère les coordonnées sphériques de n
    theta,phi = atan2(u[1],u[0]),atan2(u[2],(u[0]**2+u[1]**2)**(1/2))

    for i in range(len(seg)):
        for j in range(len(seg[i])):
            
            #Je fais une rotation d'angle -phi autour de ortho_n 
            #Puis, je fais une rotation d'angle -theta autour de Uz
            if phi:
                seg[i][j] = rotation_d_angle_teta_autour_de_U(seg[i][j],ortho_n,-phi)
            if theta:
                seg[i][j] = rotation_d_angle_teta_autour_de_U(seg[i][j],[0,0,1],-theta)
            
            #Je projette orthogonalement le point sur Oyz
            seg[i][j] = projection_ortho_sur_oyz(seg[i][j])
        
            #Je ne conserve que les coordonnées y et z de la projection
            seg[i][j] = [seg[i][j][1],seg[i][j][2]]

    #J'affiche les segments
    for i in seg:
        plt.plot([i[0][0],i[1][0]],[i[0][1],i[1][1]],couleur,linewidth=epaisseur)

### Processus de maillage

def creation_des_segments_a_afficher(f,etendue_x,etendue_y,pt_depart,nombre_de_mailles):
    seg3 = []
    X,Y = linspace(-etendue_x,etendue_x,nombre_de_mailles), linspace(-etendue_y,etendue_y,nombre_de_mailles)
    for i in range(len(X)-1): #mailles horizontales
        for j in range(len(Y)):
            seg3 += [[  [X[i],Y[j],f(X[i],Y[j])] , [X[i+1],Y[j],f(X[i+1],Y[j])]  ]]
    for i in range(len(X)):
        for j in range(len(Y)-1): #mailles verticales
            seg3 += [[  [X[i],Y[j],f(X[i],Y[j])] , [X[i],Y[j+1],f(X[i],Y[j+1])]  ]]
    return seg3

### Processus de vue en rotation

def afficher_vue_rotation_autour_z_depuis_distance_r_hauteur_h(segments,nbr_prises,r,h,axes):
    compteur = 0
    for i in linspace(0,2*pi,nbr_prises):
        plt.axis(axes)
        for j in segments:
            afficher_vue_depuis_le_point_u(j["seg"],[r*cos(i),r*sin(i),h],j["couleur"],j["epaisseur"])
        
        num_image = str(compteur)
        num_image = "0"*(3-len(num_image))+num_image
        plt.savefig("image"+num_image+".png")
        print(num_image)
        compteur += 1

        plt.show()
