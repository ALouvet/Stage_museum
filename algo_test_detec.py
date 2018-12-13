# -*- coding: utf-8 -*-
"""
Created on Thu Dec 06 10:09:07 2018

@author: apolline l
"""

from representation_simulation import *
from algo_EM_PRM import *
from random import uniform
import os

#Permet de faire des tests a la chaine
#Contient une fonction permettant de realiser un test donne
#et d'automatiser les tests

N = int(raw_input('Entrer le nombre de patchs :'))
t = int(raw_input("Entrer la duree d'observation :"))

N_param = 50 #Nombre de simulations réalisées pour chaque jeu de parametres
N_BGS = 5 #Nombre de tests realises pour le modele avec banque de graines simple
N_it = 10 #Nombre d'itérations dans l'algorithme EM

pi = float(raw_input("Entrer la proportion initiale de graines :"))

def fonction_test(c, g, d):
    test = 0
    for l in range(N_param): #Nombre de simulations realisees pour chaque jeu de parametres
        #Generation des donnees
        pi = uniform(0,1)
        modele = ModPRM(c, 1, g, uniform(0,1), pi)
        pop = generation_CI_complet_prm(N, pi, 0.1, 0.1, modele)
        simulation_prm_csv(pop, t, 'temp')
        liste_data = lire_colonne_csv(lire_csv('temp'))
        
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
                mod = 1
                break
        if mod == 1:
            test += 1
    return(test*1.0/N_param)
    
nom = raw_input('Entrer le nom du fichier contenant les resultats :')

file_res = open(nom+'.csv', 'wb')
writer = csv.writer(file_res, delimiter = ';')

for i in range(17):
    for j in range(17):
        for k in range(17):
            col = 0.1 + 0.05*i
            germ = 0.1 + 0.05*j
            m = 0.1 + 0.05*k
            val_test = fonction_test(col, germ, m)
            print("Resultat de l'etape "+str(i)+'_'+str(j)+'_'+str(k))
            print(col, germ, m)
            print(val_test)
            liste = [N, t, N_param, N_BGS, N_it, pi, col, germ, m, val_test]
            writer.writerow(liste)
file_res.close()       
            
