# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 15:17:24 2018

@author: apolline l
"""

from generation_simulation import *
import os
import csv
from Tkinter import *

def simulation_prm_csv(population, T, nom_du_csv):
    """A partir de conditions initiales données, simule l'évolution de la population selon un modèle PRM
    pendant un nombre de générations indiqué par l'utilisateur. Les données de présence/absence de plantes
    sont enregistrées dans un fichier csv."""
    file_name = nom_du_csv+".csv"
    file = open(file_name, 'wb')
    N = len(population.ci)
    try:
        writer = csv.writer(file, delimiter = ';')
        liste_str1 = []
        for i in range(N):
            liste_str1.append(str(population.ci.patch(i).x)+' ')
        writer.writerow(liste_str1)
        liste_str2 = []
        for i in range(N):
            liste_str2.append(str(population.ci.patch(i).y)+' ')
        writer.writerow(liste_str2)
        liste_plante = []
        for i in range(N):
            liste_plante.append(population.ci.patch(i).plante)
        writer.writerow(liste_plante)
        for j in range(T):
            population.prm_generation() #C'est pour cela que l'on a besoin de spécifier 'PRM'
            liste_plante = []
            for i in range(N):
                liste_plante.append(population.ci.patch(i).plante)
            writer.writerow(liste_plante)
    finally:
        file.close()

def simulation_prm_csv_complete(population, T, nom_du_csv):
    """A partir de conditions initiales données, simule l'évolution de la population selon un modèle PRM
    pendant un nombre de générations indiqué par l'utilisateur. Les données de présence/absence de plantes
    et de graines sont enregistrées dans un fichier csv."""
    file_name = nom_du_csv+".csv"
    file = open(file_name, 'wb')
    N = population.ci.nbr()
    try:
        writer = csv.writer(file, delimiter = ';')
        liste_str1 = []
        for i in range(N):
            liste_str1.append(str(population.ci.patch(i).x)+' ')
        writer.writerow(liste_str1)
        liste_str2 = []
        for i in range(N):
            liste_str2.append(str(population.ci.patch(i).y)+' ')
        writer.writerow(liste_str2)
        liste_plante = []
        for i in range(N):
            liste_plante.append(population.ci.patch(i).plante)
        writer.writerow(liste_plante)
        liste_graine = []
        for i in range(N):
            liste_graine.append(population.ci.patch(i).graine)
        writer.writerow(liste_graine)
        for j in range(T):
            population.prm_generation()
            liste_plante = []
            for i in range(N):
                liste_plante.append(population.ci.patch(i).plante)
            writer.writerow(liste_plante)
            liste_graine = []
            for i in range(N):
                liste_graine.append(population.ci.patch(i).graine)
            writer.writerow(liste_graine)
    finally:
        file.close()

def simulation_levins_csv(population, T, nom_du_csv):
    """A partir de conditions initiales données, simule l'évolution de la population selon un modèle de Levins
    pendant un nombre de générations indiqué par l'utilisateur. Les données de présence/absence de plantes
    sont enregistrées dans un fichier csv."""
    file_name = nom_du_csv+".csv"
    file = open(file_name, 'wb')
    N = population.ci.nbr()
    try:
        writer = csv.writer(file, delimiter = ';')
        liste_str1 = []
        for i in range(N):
            liste_str1.append(str(population.ci.patch(i).x)+' ')
        writer.writerow(liste_str1)
        liste_str2 = []
        for i in range(N):
            liste_str2.append(str(population.ci.patch(i).y)+' ')
        writer.writerow(liste_str2)
        liste_plante = []
        for i in range(N):
            liste_plante.append(population.ci.patch(i).plante)
        writer.writerow(liste_plante)
        for j in range(T):
            population.levins_generation() #D'ou la specification : 'de Levins'
            liste_plante = []
            for i in range(N):
                liste_plante.append(population.ci.patch(i).plante)
            writer.writerow(liste_plante)
    finally:
        file.close()

def simulation_levins_csv_complete(population, T, nom_du_csv):
    """A partir de conditions initiales données, simule l'évolution de la population selon un modèle PRM
    pendant un nombre de générations indiqué par l'utilisateur. Les données de présence/absence de plantes
    et de graines sont enregistrées dans un fichier csv."""
    file_name = nom_du_csv+".csv"
    file = open(file_name, 'wb')
    N = population.ci.nbr()
    try:
        writer = csv.writer(file, delimiter = ';')
        liste_str1 = []
        for i in range(N):
            liste_str1.append(str(population.ci.patch(i).x)+' ')
        writer.writerow(liste_str1)
        liste_str2 = []
        for i in range(N):
            liste_str2.append(str(population.ci.patch(i).y)+' ')
        writer.writerow(liste_str2)
        liste_plante = []
        for i in range(N):
            liste_plante.append(population.ci.patch(i).plante)
        writer.writerow(liste_plante)
        liste_graine = []
        for i in range(N):
            liste_graine.append(population.ci.patch(i).graine)
        writer.writerow(liste_graine)
        for j in range(T):
            population.levins_generation()
            liste_plante = []
            for i in range(N):
                liste_plante.append(population.ci.patch(i).plante)
            writer.writerow(liste_plante)
            liste_graine = []
            for i in range(N):
                liste_graine.append(population.ci.patch(i).graine)
            writer.writerow(liste_graine)
    finally:
        file.close()

def lire_csv(nom_du_csv):
    """Permet de lire un fichier csv contenant les données de présence/absence de plantes  pour les différents patchs.
    Le format doit être le suivant : 
    - un patch = une colonne
    - les deux premières lignes correspondent aux abscisses et ordonnées des différents patchs
    - les données manquantes sont au format 'na' """
    lecture_csv = []
    compteur = 0
    
    if type(nom_du_csv) == type('Hello world'):
        file_name = nom_du_csv+'.csv'
        file = open(file_name, 'rb')
    else :
        file = nom_du_csv
    
    reader = csv.reader(file, delimiter = ';')
    for row in reader :
        if compteur == 0:
            abs = row
            compteur += 1
        elif compteur == 1:
            ord = row
            compteur += 1
        else :
            lecture_csv.append(row)
            
    file.close()
    return(lecture_csv, abs, ord)
                
def visualisation_csv(nom_du_csv, nom_du_gif):  
    try:
        lecture_csv_tot = lire_csv(nom_du_csv)
        lecture_csv = lecture_csv_tot[0]
        abs = lecture_csv_tot[1]
        ord = lecture_csv_tot[2]
    finally:
        tps = len(lecture_csv)
        longueur = len(abs)
        liste_milieux = []
        for i in range(tps):
            liste_pa = []
            for j in range(longueur):
                liste_pa.append(PiedArbre(float(abs[j]), float(ord[j]), int(float(lecture_csv[i][j])), 0))
            liste_milieux.append(Milieu(liste_pa[:]))
        compteur = 0
        for milieu in liste_milieux:
            if compteur < 10:
                milieu.line_plot_obs_save('00'+str(compteur))
            elif 10 <= compteur < 100:
                milieu.line_plot_obs_save('0'+str(compteur))
            else:
                milieu.line_plot_obs_save(str(compteur))
            compteur += 1
        os.system('convert -delay 100 *.png '+nom_du_gif+'.gif')

        compteur = 0
        for milieu in liste_milieux:
            if compteur < 10:
                os.remove('00'+str(compteur)+'.png')
            elif 10 <= compteur < 100:
                os.remove('0'+str(compteur)+'.png')
            else:
                os.remove(str(compteur)+'.png')
            compteur += 1
        
def lire_csv_complet(nom_du_csv):
    """Permet de lire un fichier csv contenant les données de présence/absence de plantes  
    et de graines pour les différents patchs.
    Le format doit être le suivant : 
    - un patch = une colonne
    - les deux premières lignes correspondent aux abscisses et ordonnées des différents patchs
    - les données manquantes sont au format 'na' """
    lecture_csv_p = []
    lecture_csv_g = []
    compteur = 0
    
    file_name = nom_du_csv+'.csv'
    file = open(file_name, 'rb')
    
    reader = csv.reader(file, delimiter = ';')
    for row in reader :
        if compteur == 0:
            abs = row
            compteur += 1
        elif compteur == 1:
            ord = row
            compteur += 1
        else :
            if compteur % 2 == 0:
                lecture_csv_p.append(row)
                compteur += 1
            else: 
                lecture_csv_g.append(row)
                compteur += 1
    
    file.close()
    return(lecture_csv_p, lecture_csv_g, abs, ord)

def visualisation_csv_complete(nom_du_csv, nom_du_gif):
    try:
        lecture_csv_tot = lire_csv_complet(nom_du_csv)
        lecture_csv_p = lecture_csv_tot[0]
        lecture_csv_g = lecture_csv_tot[1]
        abs = lecture_csv_tot[2]
        ord = lecture_csv_tot[3]
    finally:
        tps = len(lecture_csv_p)
        print(tps)
        longueur = len(abs)
        liste_milieux = []
        for i in range(tps):
            liste_pa = []
            for j in range(longueur):
                liste_pa.append(PiedArbre(float(abs[j]), float(ord[j]), int(float(lecture_csv_p[i][j])), int(float(lecture_csv_g[i][j]))))
            liste_milieux.append(Milieu(liste_pa[:]))
        compteur = 0
        for milieu in liste_milieux:
            if compteur < 10:
                milieu.line_plot_save('00'+str(compteur))
            elif 10 <= compteur < 100:
                milieu.line_plot_save('0'+str(compteur))
            else:
                milieu.line_plot_save(str(compteur))
            compteur += 1
        os.system('convert -delay 100 *.png '+nom_du_gif+'.gif')

        compteur = 0
        for milieu in liste_milieux:
            if compteur < 10:
                os.remove('00'+str(compteur)+'.png')
            elif 10 <= compteur < 100:
                os.remove('0'+str(compteur)+'.png')
            else:
                os.remove(str(compteur)+'.png')
            compteur += 1

def visul_GUI(nom_du_csv):
    try:
        lecture_csv_tot = lire_csv_complet(nom_du_csv)
        lecture_csv_p = lecture_csv_tot[0]
        lecture_csv_g = lecture_csv_tot[1]
        abs = lecture_csv_tot[2]
        ord = lecture_csv_tot[3]
    finally:
        tps = len(lecture_csv_p)
        longueur = len(abs)
        liste_milieux = []
        for i in range(tps):
            liste_pa = []
            for j in range(longueur):
                liste_pa.append(PiedArbre(float(abs[j]), float(ord[j]), int(float(lecture_csv_p[i][j])), int(float(lecture_csv_g[i][j]))))
            liste_milieux.append(Milieu(liste_pa[:]))
        compteur = 0
        for milieu in liste_milieux:
            if compteur < 10:
                milieu.line_plot_save('00'+str(compteur))
            elif 10 <= compteur < 100:
                milieu.line_plot_save('0'+str(compteur))
            else:
                milieu.line_plot_save(str(compteur))
            compteur += 1
            
if __name__ == "__main__":
    modele = ModPRM(0.1, 0.5, 0.8, 0.8, 1)
    pop = generation_CI_complet_prm(50, 0.5, 0.1, 0.5, modele)
    simulation_prm_csv(pop, 20, 'test1')
    visualisation_csv('test1', 'hello')
    modele2 = ModLevins(0.1, 1.1, 0.8, 0.8, 0)
    pop2 = generation_CI_complet_levins(50, 0.5, 0.1, 0.5, modele2)
    simulation_levins_csv_complete(pop2, 20, 'test2')
    visualisation_csv_complete('test2', 'hello2')
    