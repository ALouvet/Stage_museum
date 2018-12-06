# -*- coding: utf-8 -*-
"""
Created on Thu Dec 06 09:14:54 2018

@author: apolline l
"""

from representation_simulation import *
from algo_EM_PRM import *
from random import uniform
import os

#Parametres du milieu
N = 100
t = 10

#Parametres du modele
c = 0.5
pi = 0.5
d = 0.2

#Parametres des tests
N_param = 50 #Nombre de simulations réalisées pour chaque jeu de parametres
N_BGS = 5 #Nombre de tests realises pour le modele avec banque de graines simple
N_it = 10 #Nombre d'itérations dans l'algorithme EM

liste = []

for i in range(17):
    g = 0.1 + i*0.05
    test = 0
    for k in range(N_param): #Nombre de simulations realisees pour chaque jeu de parametres
        #Generation des donnees
        pi = uniform(0,1)
        modele = ModPRM(c, 1, g, uniform(0,1), pi)
        pop = generation_CI_complet_prm(N, pi, 0.1, 0.1, modele)
        simulation_prm_csv(pop, t, 'temp')
        liste_data = lire_colonne_csv(lire_csv('temp'))
        
        #Test sans banque de graines
        mod_sans_BG = ModPRM(random.uniform(0,1), random.uniform(0,1), 1, 1, random.uniform(0,1))
        resultat = etape_EM_PRM_SB(liste_data)
        AIC = resultat[2]
        mod = 0
        
        #B : modèle avec BG simple
        for j in range(N_BGS):
            mod_avec_BGS = ModPRM(uniform(0,1), 1, uniform(0,1), uniform(0,1), uniform(0,1))
            for i in range(N_it):
                resultat = etape_EM_PRM_BGS(liste_data,mod_avec_BGS)
                mod_avec_BGS = resultat[0]
            if resultat[2] < AIC :
                mod = 1
                break
        if mod == 1:
            test += 1
        print('Etape '+str(g)+' '+str(k)+ ' terminee')
    liste.append([g, test*1.0/N_param])
    print(liste)

os.chdir('tests_detection_bg')
liste_germ = []
liste_tx = []
for elem in liste:
    liste_germ.append(elem[0])
    liste_tx.append(elem[0])

file_taux = open('test1_50.csv', 'wb')

try :
    writer = csv.writer(file_taux, delimiter = ";")
    writer.writerow(liste_germ)
    writer.writerow(liste_tx)

finally:
    file_taux.close()
