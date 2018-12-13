# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 09:17:26 2018

@author: apolline l
"""

#Donne les probabilites de germination et de mort des graines obtenues lors des
#"faux positifs" pour une banque de graines

import numpy as np
from representation_simulation import *
from algo_EM_PRM import *
from random import uniform
import os
import csv

#Generation d'un fichier csv contenant les donnes
file_err = open('err_est_sbg.csv', 'wb')
writer = csv.writer(file_err, delimiter = ';')

N = 100
t = 10

N_param = 100 #Nombre de simulations réalisées pour chaque jeu de parametres
N_BGS = 1 #Nombre de tests realises pour le modele avec banque de graines simple
N_it = 10 #Nombre d'itérations dans l'algorithme EM

def fonction_test(c, p):
    global listeg
    global listed
    for l in range(N_param): #Nombre de simulations realisees pour chaque jeu de parametres
        #Generation des donnees
        pi = uniform(0,1)
        modele = ModPRM(c, p, 1, 1, pi)
        pop = generation_CI_complet_prm(N, pi, 0.1, 0.1, modele)
        simulation_prm_csv(pop, t, 'temperr')
        liste_data = lire_colonne_csv(lire_csv('temperr'))
        
        #Test sans banque de graines
        resultat = etape_EM_PRM_SB(liste_data)
        AIC = resultat[2]
        
        #B : modèle avec BG simple
        for m in range(N_BGS):
            mod_avec_BGS = ModPRM(uniform(0,1), 1, uniform(0,1), uniform(0,1), uniform(0,1))
            for i in range(N_it):
                resultat = etape_EM_PRM_BGS(liste_data,mod_avec_BGS)
                mod_avec_BGS = resultat[0]
            if resultat[2] < AIC :
                AIC = resultat[2]
                liste_res = [c, p, mod_avec_BGS.g, mod_avec_BGS.d]
                writer.writerow(liste_res)
    return None

for i in range(17):
    for j in range(17):
        col = 0.1 + 0.05*i
        per = 0.1 + 0.05*j
        fonction_test(col, per)
        print('test '+str(i)+str(j))

file_err.close()
file_err = open('err_est_sbg.csv', 'rb')
reader = csv.reader(file_err, delimiter = ';')

plt.figure()

for row in reader:
    plt.plot(row[2], row[3], 'bo')

plt.savefig('err_est_sbg.png')
plt.close()
        
