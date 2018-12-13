# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:32:53 2018

@author: apolline l
"""

import numpy as np
from representation_simulation import *
from algo_EM_PRM import *
from random import uniform
import os

val_g = [0.2, 0.4, 0.6, 0.8]
val_c = [0.1, 0.3, 0.5, 0.7, 0.9]
val_d = [0.1, 0.3, 0.5, 0.7, 0.9]

N = 100
t = 10

N_param = 30 #Nombre de simulations réalisées pour chaque jeu de parametres
N_BGS = 5 #Nombre de tests realises pour le modele avec banque de graines simple
N_it = 10 #Nombre d'itérations dans l'algorithme EM

file_data = open('est_bg_Np'+str(N_param)+'Nbgs'+str(N_BGS)+'.csv', 'wb')
writer = csv.writer(file_data, delimiter = ';')

def fonction_test(c, g, d):
    AIC = 10000
    pi = uniform(0,1)
    modele = ModPRM(c, 1, g, d, pi)
    pop = generation_CI_complet_prm(N, pi, 0.1, 0.1, modele)
    simulation_prm_csv(pop, t, 'tempest')
    liste_data = lire_colonne_csv(lire_csv('tempest'))
    for m in range(N_BGS):
        mod_avec_BGS = ModPRM(uniform(0,1), 1, uniform(0,1), uniform(0,1), uniform(0,1))
        for i in range(N_it):
            resultat = etape_EM_PRM_BGS(liste_data,mod_avec_BGS)
            mod_avec_BGS = resultat[0]
            if resultat[2] < AIC :
                AIC = resultat[2]
                c_est = mod_avec_BGS.c
                g_est = mod_avec_BGS.g
                d_est = mod_avec_BGS.d
    return(c_est, g_est, d_est)

for germ in val_g:
    for col in val_c:
        for m in val_d:
            for i in range(N_param):
                val_est = fonction_test(col, germ, m)
                liste = [col, germ, m]
                liste.append(val_est[0])
                liste.append(val_est[1])
                liste.append(val_est[2])
                writer.writerow(liste)
            print('Etape g '+str(germ)+'c '+str(col)+'d '+str(m)+' terminee !')

file_data.close()
            
            