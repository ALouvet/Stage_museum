# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 11:35:52 2018

@author: apolline l
"""

import numpy as np
from representation_simulation import *
from algo_EM_PRM import *
from random import uniform
import os

def generation_image(matrice, nom):
    """Permet de générer une image corresponant aux proportions de tests ayant donné le bon résultat.
    La matrice mise en argument doit être un array numpy."""
    plt.imshow(matrice, vmin = 0, vmax = 1, origin = 'lower')
    plt.xlabel('probabilite de colonisation')
    plt.ylabel('probabilte de persistance')
    plt.savefig(nom+'.png')
    file_sauv = open(nom+'.csv', 'wb')
    writer = csv.writer(file_sauv, delimiter = ';')
    for i in range(len(matrice)):
        writer.writerow(matrice[i])
    file_sauv.close()
    return None

def fonction_test(c, p):
    test = 0
    for l in range(N_param): #Nombre de simulations realisees pour chaque jeu de parametres
        #Generation des donnees
        pi = uniform(0,1)
        modele = ModPRM(c, p, 1, 1, pi)
        pop = generation_CI_complet_prm(N, pi, 0.1, 0.1, modele)
        simulation_prm_csv(pop, t, 'tempsbg')
        liste_data = lire_colonne_csv(lire_csv('tempsbg'))
        
        #Test sans banque de graines
        resultat = etape_EM_PRM_SB(liste_data)
        AIC = resultat[2]
        mod = 0
        
        #B : modèle avec BG simple
        for m in range(N_BGS):
            mod_avec_BGS = ModPRM(uniform(0,1), 1, uniform(0,1), uniform(0,1), uniform(0,1))
            for i in range(N_it):
                resultat = etape_EM_PRM_BGS(liste_data,mod_avec_BGS)
                mod_avec_BGS = resultat[0]
                if resultat[2] < AIC :
                    if mod_avec_BGS.g < 0.9 and mod_avec_BGS.d < 0.8 :#Critère de prise en compte de la banque de graines...
                        mod = 1
                        break
        if mod == 0:
            test += 1
    return(test*1.0/N_param)

if __name__ == '__main__':
    
    N = int(raw_input('Entrer le nombre de patchs :'))
    t = int(raw_input("Entrer la duree d'observation :"))
    N_BGS = 1
    
    N_param = int(raw_input('Entrer le nombre de tests pour chaque jeu de parametres :'))
    N_it = 10 #Nombre d'itérations dans l'algorithme EM
    
    nom = raw_input("Entrer le nom de l'image obtenue :")

    
    resultat = np.zeros((17, 17))
    
    for j in range(17):
        for k in range(17):
            print('test '+str(j)+' '+str(k))
            col = 0.1 + 0.05*j
            per = 0.1 + 0.05*k
            val_test = fonction_test(col, per)
            resultat[j][k] = 1 - val_test #Pour afficher le pourcentage d'erreurs
    
    generation_image(resultat, nom)