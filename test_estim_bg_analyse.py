# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:05:04 2018

@author: apolline l
"""

import csv
import matplotlib.pyplot as plt
import numpy as np

liste_estc = np.zeros((4, 5, 5))
liste_estg = np.zeros((4, 5, 5))
liste_estd = np.zeros((4, 5, 5))

val_g = [0.2, 0.4, 0.6, 0.8]
val_c = [0.1, 0.3, 0.5, 0.7, 0.9]
val_d = [0.1, 0.3, 0.5, 0.7, 0.9]

N_param = int(raw_input('Nombre de tests pour chaque jeu de parametres :'))

def test_egal(a, b):
    return (abs(a-b) < 10**-15)

fichier_a_tester = raw_input('Entrer le nom du fichier a tester :')

file_data = open(fichier_a_tester+'.csv', 'rb')
reader = csv.reader(file_data, delimiter = ';')

for row in reader :
    ind_col = val_c.index(float(row[0]))
    ind_germ = val_g.index(float(row[1]))
    ind_m = val_d.index(float(row[2]))
    c_est = float(row[3])*1.0/N_param
    g_est = float(row[4])*1.0/N_param
    d_est = float(row[5])*1.0/N_param
    
    liste_estc[ind_germ][ind_col][ind_m] += c_est
    liste_estg[ind_germ][ind_col][ind_m] += g_est
    liste_estd[ind_germ][ind_col][ind_m] += d_est

file_data.close()
    
#Figure : estimation des probabilites de germination
fig_g = plt.figure()
plt.xlabel('Probabilite de germination theorique')
plt.ylabel('Probabilite de germination moyenne estimee')

x = [0.005*i for i in range(200)]
y = [0.005*i for i in range(200)]

plt.plot(x, y, 'k-')

for i in range(4):
    germ = val_g[i]
    plt.plot(germ, liste_estg[i][0][0], 'bo')
    plt.plot(germ, liste_estg[i][0][1], 'b1')
    plt.plot(germ, liste_estg[i][0][2], 'bs')
    plt.plot(germ, liste_estg[i][0][3], 'b*')
    plt.plot(germ, liste_estg[i][0][4], 'bD')
    
    plt.plot(germ, liste_estg[i][1][0], 'ko')
    plt.plot(germ, liste_estg[i][1][1], 'k1')
    plt.plot(germ, liste_estg[i][1][2], 'ks')
    plt.plot(germ, liste_estg[i][1][3], 'k*')
    plt.plot(germ, liste_estg[i][1][4], 'kD')
    
    plt.plot(germ, liste_estg[i][2][0], 'go')
    plt.plot(germ, liste_estg[i][2][1], 'g1')
    plt.plot(germ, liste_estg[i][2][2], 'gs')
    plt.plot(germ, liste_estg[i][2][3], 'g*')
    plt.plot(germ, liste_estg[i][2][4], 'gD')
    
    plt.plot(germ, liste_estg[i][3][0], 'co')
    plt.plot(germ, liste_estg[i][3][1], 'c1')
    plt.plot(germ, liste_estg[i][3][2], 'cs')
    plt.plot(germ, liste_estg[i][3][3], 'c*')
    plt.plot(germ, liste_estg[i][3][4], 'cD')
    
    plt.plot(germ, liste_estg[i][4][0], 'yo')
    plt.plot(germ, liste_estg[i][4][1], 'y1')
    plt.plot(germ, liste_estg[i][4][2], 'ys')
    plt.plot(germ, liste_estg[i][4][3], 'y*')
    plt.plot(germ, liste_estg[i][4][4], 'yD')

plt.savefig('est_g.png')
plt.close()

#Figure : estimation des probabilites de colonisation
fig_c = plt.figure()
plt.xlabel('Probabilite de colonisation theorique')
plt.ylabel('Probabilite de colonisation moyenne estimee')

x = [0.005*i for i in range(200)]
y = [0.005*i for i in range(200)]

plt.plot(x, y, 'k-')

for i in range(5):
    col = val_c[i]
    plt.plot(col, liste_estc[0][i][0], 'bo')
    plt.plot(col, liste_estc[0][i][1], 'b1')
    plt.plot(col, liste_estc[0][i][2], 'bs')
    plt.plot(col, liste_estc[0][i][3], 'b*')
    plt.plot(col, liste_estc[0][i][4], 'bD')
    
    plt.plot(col, liste_estc[1][i][0], 'ko')
    plt.plot(col, liste_estc[1][i][1], 'k1')
    plt.plot(col, liste_estc[1][i][2], 'ks')
    plt.plot(col, liste_estc[1][i][3], 'k*')
    plt.plot(col, liste_estc[1][i][4], 'kD')
    
    plt.plot(col, liste_estc[2][i][0], 'go')
    plt.plot(col, liste_estc[2][i][1], 'g1')
    plt.plot(col, liste_estc[2][i][2], 'gs')
    plt.plot(col, liste_estc[2][i][3], 'g*')
    plt.plot(col, liste_estc[2][i][4], 'gD')
    
    plt.plot(col, liste_estc[3][i][0], 'co')
    plt.plot(col, liste_estc[3][i][1], 'c1')
    plt.plot(col, liste_estc[3][i][2], 'cs')
    plt.plot(col, liste_estc[3][i][3], 'c*')
    plt.plot(col, liste_estc[3][i][4], 'cD')

plt.savefig('est_c.png')
plt.close()

#Figure : estimation des probabilites de mort
fig_d = plt.figure()
plt.xlabel('Probabilite de mort theorique')
plt.ylabel('Probabilite de mort moyenne estimee')

x = [0.005*i for i in range(200)]
y = [0.005*i for i in range(200)]

plt.plot(x, y, 'k-')

for i in range(5):
    m = val_d[i]
    plt.plot(m, liste_estd[0][0][i], 'bo')
    plt.plot(m, liste_estd[0][1][i], 'b1')
    plt.plot(m, liste_estd[0][2][i], 'bs')
    plt.plot(m, liste_estd[0][3][i], 'b*')
    plt.plot(m, liste_estd[0][4][i], 'bD')
    
    plt.plot(m, liste_estd[1][0][i], 'ko')
    plt.plot(m, liste_estd[1][1][i], 'k1')
    plt.plot(m, liste_estd[1][2][i], 'ks')
    plt.plot(m, liste_estd[1][3][i], 'k*')
    plt.plot(m, liste_estd[1][4][i], 'kD')
    
    plt.plot(m, liste_estd[2][0][i], 'go')
    plt.plot(m, liste_estd[2][1][i], 'g1')
    plt.plot(m, liste_estd[2][2][i], 'gs')
    plt.plot(m, liste_estd[2][3][i], 'g*')
    plt.plot(m, liste_estd[2][4][i], 'gD')
    
    plt.plot(m, liste_estd[3][0][i], 'co')
    plt.plot(m, liste_estd[3][1][i], 'c1')
    plt.plot(m, liste_estd[3][2][i], 'cs')
    plt.plot(m, liste_estd[3][3][i], 'c*')
    plt.plot(m, liste_estd[3][4][i], 'cD')

plt.savefig('est_d.png')
plt.close()

#Figure : estimation des probabilites de mort (autre représentation)
fig_d = plt.figure()
plt.xlabel('Probabilite de mort theorique')
plt.ylabel('Probabilite de mort moyenne estimee')

x = [0.005*i for i in range(200)]
y = [0.005*i for i in range(200)]

plt.plot(x, y, 'k-')

for i in range(5):
    m = val_d[i]
    plt.plot(m, liste_estd[0][0][i], 'bo')
    plt.plot(m, liste_estd[1][0][i], 'b1')
    plt.plot(m, liste_estd[2][0][i], 'bs')
    plt.plot(m, liste_estd[3][0][i], 'b*')
    
    plt.plot(m, liste_estd[0][1][i], 'ko')
    plt.plot(m, liste_estd[1][1][i], 'k1')
    plt.plot(m, liste_estd[2][1][i], 'ks')
    plt.plot(m, liste_estd[3][1][i], 'k*')
    
    plt.plot(m, liste_estd[0][2][i], 'go')
    plt.plot(m, liste_estd[1][2][i], 'g1')
    plt.plot(m, liste_estd[2][2][i], 'gs')
    plt.plot(m, liste_estd[3][2][i], 'g*')
    
    plt.plot(m, liste_estd[0][3][i], 'yo')
    plt.plot(m, liste_estd[1][3][i], 'y1')
    plt.plot(m, liste_estd[2][3][i], 'ys')
    plt.plot(m, liste_estd[3][3][i], 'y*')
    
    plt.plot(m, liste_estd[0][4][i], 'co')
    plt.plot(m, liste_estd[1][4][i], 'c1')
    plt.plot(m, liste_estd[2][4][i], 'cs')
    plt.plot(m, liste_estd[3][4][i], 'c*')

plt.savefig('est_dc.png')
plt.close()