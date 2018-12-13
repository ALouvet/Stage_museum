# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 10:55:21 2018

@author: apolline l
"""

import matplotlib.pyplot as plt
import numpy as np

epsilon = 0.01

#Etape 1 : trace des probas de mort des graines maximales possibles
plt.figure()

plt.xlabel('Probabilite de germination')
plt.ylabel('Probabilite de mort des graines maximale')

def fonction(c, g):
    vald = (1-c)*(1-g)*(g+epsilon)
    val = 1 - ((epsilon)*1.0/vald)
    return max(val, 0)

x = [0.005*i for i in range(200)]

y1 = [fonction(0.1, x[i]) for i in range(200)]
y2 = [fonction(0.3, x[i]) for i in range(200)]
y3 = [fonction(0.5, x[i]) for i in range(200)]
y4 = [fonction(0.7, x[i]) for i in range(200)]
y5 = [fonction(0.9, x[i]) for i in range(200)]

plt.plot(x, y1, color = 'black', linestyle = '-', label = 'colonisation = 0.1')
plt.plot(x, y2, color = 'blue', linestyle = '-', label = 'colonisation = 0.3')
plt.plot(x, y3, color = 'red', linestyle = '-', label = 'colonisation = 0.5')
plt.plot(x, y4, color = 'yellow', linestyle = '-', label = 'colonisation = 0.7')
plt.plot(x, y5, color = 'green', linestyle = '-', label = 'colonisation = 0.9')
plt.legend(loc = 'upper right')
plt.xlim(0,1.0)
plt.ylim(0,1.0)

plt.savefig('test_bg_obs_'+str(epsilon)+'.png')
plt.close()

#Etape 2 : trace des probabilites de colonisation maximales
plt.figure()
val = np.zeros((80, 80))

for i in range(80):
    for j in range(80):
        germ = 0.1+0.01*i
        mort = 0.1+0.01*j
        val[i][j] = 1-fonction(mort, germ)

x = [0.1+ 0.01*i for i in range(0, 80, 10)]
y = [0.1+ 0.01*j for j in range(0,80, 10)]

plt.imshow(val, vmin = 0, vmax =1, origin = 'lower')
cbar = plt.colorbar(ticks = [0.1*i for i in range(11)])
cbar.ax.set_yticklabels([1 - 0.1*i for i in range(11)])

plt.xticks([i for i in range(0, 80, 10)], x)
plt.yticks([i for i in range(0,80, 10)], y)

plt.xlabel('probabilite de germination')
plt.ylabel('probabilite de mort des graines')

plt.savefig('repres_eps'+str(epsilon)+'.png')
