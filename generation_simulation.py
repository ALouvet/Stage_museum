# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 17:16:41 2018

@author: apolline l
"""

import matplotlib.pyplot as plt
import numpy as np
import numpy.core._methods
import matplotlib.backends.backend_tkagg
import matplotlib.backends.backend_qt4agg
import FileDialog
import numpy.lib.format
import random as rd

class PiedArbre(object):
    """Permet de créer un patch caractérisé par la position géographique de son centre, par la présence de plantes et celles de graines."""
    
    def __init__(self, abs, ord, plante, graine):
        """Crée un patch. Prend en arguments l'abscisse et l'ordonnée du patch,
        la présence/absence de plantes (format 1/0) et la présence/absence de graines.
        ! Attention : Les coordonnées géographiques ne sont plus modifiables après création. ! 
        Exemple : pour un patch situé en (1,2), dans lequel des graines sont présentes,
        mais pas des plantes.
        => PiedArbre(1, 2, 0, 1)"""   
        try:
            if plante != 0 and plante != 1:
                raise Warning("Attention : la donnée de présence/absence de plantes n'est pas au format désiré. Le pied d'arbre ne sera pas créé")
            elif graine != 0 and graine != 1:
                raise Warning("Attention : la donnée de présence/absence de graines n'est pas au format désiré. Le pied d'arbre ne sera pas créé")
        except Warning as e:
            print(e)
        else:
            self._x = abs
            self._y = ord
            self.plante = plante
            self.graine = graine
    
    #Méthodes permettant de bloquer la modification des coordonnées du patch.
    def get_x(self):
        return self._x
    
    def set_x(self, new):
        print("Opération impossible : les coordonnées du patch ne sont pas modifiables")
            
    def get_y(self):
        return self._y
    
    def set_y(self, new):
        print("Opération impossible : les coordonnées du patch ne sont pas modifiables")    
    
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    
    def affiche(self):
        """Affiche les coordonnées du pied d'arbre, ainsi que les données de présence/absence
        de plantes et de graines, le tout sous forme d'une liste.
        Exemple : PiedArbre(1, 2, 0, 1).affiche retournera
        => [1, 2, 0, 1] """
        return([self.x, self.y, self.plante, self.graine])
    
    #Méthodes peremttant de changer les données de présence/absence de façon
    #plus lisible pour l'utilisateur
    def nais_plante(self):
        self.plante = 1
    
    def mort_plante(self):
        self.plante = 0
    
    def nais_graine(self):
        self.graine = 1
    
    def mort_graine(self):
        self.graine = 0

class Milieu(PiedArbre):
    """Ensemble des patchs étudiés. """
    
    def __init__(self, liste):
        """Prend en argument une liste d'éléments de la classe PiedArbre. La liste des coordonnées
        des différents patchs, non modifiables, est créée automatiquement."""
        self.liste = liste
        coords = []
        for elem in liste:
            coords.append([elem.x, elem.y])
        self._coord = coords
    
    #Méthodes permettant de bloquer les modifications des coordonnées des patchs.
    def get_coord(self):
        return self._coord
    
    def set_coord(self, new):
        print("Opération impossible : les coordonnées des patchs ne sont pas modifiables") 
    
    coord = property(get_coord, set_coord)
    
    def patch(self,indice):
        """Extrait le patch d'indice i de la liste."""
        return self.liste[indice]
    
    def repres_patch(self, indice):
        """Extrait le patch d'indice i de la liste et l'affiche sous la forme d'une liste."""
        return self.liste[indice].affiche()
    
    def __len__(self):
        return len(self.liste)
    
    def spat_plot(self):
        """Rreprésente les données de présence/absence de façon spatiale.
        Chaque point correspond à un patch. Il est de couleur verte si il contient 
        des plantes, rouge si il ne contient que des graines et noir si il est vide."""
        plt.figure()
        for pied in self.liste:
            if pied.plante == 1:
                plt.plot(pied.x, pied.y, 'go')
            elif pied.graine == 1:
                plt.plot(pied.x, pied.y, 'ro')
            else :
                plt.plot(pied.x, pied.y, 'bo')
        plt.title('Etat de chaque patch')
     
    def spat_plot_save(self,nom):
        """Représente les données de présence/absence de façon spatiale et 
        sauvegarde la figure obtenue au format png sous le nom entré par l'utilisateur.
        Chaque point correspond à un patch. Il est de couleur verte si il contient 
        des plantes, rouge si il ne contient que des graines et noir si il est vide."""
        try :
            assert type(nom) == type('hello world')
        except AssertionError:
            print('Attention : le nom du fichier doit être une chaîne de caractères. Le fichier ne sera pas créé.')
        else: 
            fig_spat = plt.figure()
            for pied in self.liste:
                if pied.plante == 1:
                    plt.plot(pied.x, pied.y, 'go')
                elif pied.graine == 1:
                    plt.plot(pied.x, pied.y, 'ro')
                else :
                    plt.plot(pied.x, pied.y, 'bo')
            plt.title('Etat de chaque patch')
            fig_spat.savefig(nom+'.png')
            plt.close(fig_spat)
    
    def spat_plot_obs_save(self, nom):
        """Représente les données de présence/absence de plantes de façon spatiale et 
        sauvegarde la figure obtenue au format png sous le nom entré par l'utilisateur.
        Chaque point correspond à un pied d'arbre. Il est de couleur verte si il contient 
        des plantes, noir sinon."""
        try :
            assert type(nom) == type('hello world')
        except AssertionError:
            print('Attention : le nom du fichier doit être une chaîne de caractères. Le fichier ne sera pas créé.')
        else: 
            fig_spat = plt.figure()
            for pied in self.liste:
                if pied.plante == 1:
                    plt.plot(pied.x, pied.y, 'go')
                else :
                    plt.plot(pied.x, pied.y, 'bo')
            plt.title('Etat de chaque patch')
            fig_spat.savefig(nom+'.png')
            plt.close(fig_spat)
    
    def esp(self):
        """Retourne la liste des données de présence/absence de plantes."""
        espece = []
        for pied in self.liste:
            espece.append(pied.plante)
        return espece
    
    def bg(self):
        """Retourne la liste de données de présence/absence de graines."""
        bgraine = []
        for pied in self.liste:
            bgraine.append(pied.graine)
        return bgraine
    
    def line_plot(self):
        """Représente les données de présence/absence de plantes et de graines en supposant que les patchs sont ordonnés
        en ligne dans l'ordre utilisé pour la liste définissant le milieu."""
        plt.figure()
        ax = plt.axes()        
        N = len(self.liste)
        abs = np.array([i for i in range(N)])
        plt.axis([0,N-1, 0, 5])
        plt.plot(abs, self.esp(), color = 'blue', linestyle = 'solid', label = 'Presence - Plante')
        plt.plot(abs, self.bg(), color = 'green', linestyle = 'dashed', label = 'Presence - Graine')
        ax = ax.set(xlabel = "Position des patchs", ylabel = "Presence de l'espece")
        plt.legend(loc = 'upper right')
        plt.title('Etat de la rue')
    
    def line_plot_save(self,nom, form = '.png'):
        """Représente les données de présence/absence de plantes et de graines en supposant que les patchs sont ordonnés
        en ligne dans l'ordre utilisé pour la liste définissant le milieu. 
        Sauvegarde le fichier obtenu au format png par défaut."""
        try :
            assert type(nom) == type('hello world')
        except AssertionError:
            print('Attention : le nom du fichier doit être une chaîne de caractères. Le fichier ne sera pas créé.')
        else: 
            fig_line = plt.figure()
            ax = plt.axes()        
            N = len(self.liste)
            abs = np.array([i for i in range(N)])
            plt.axis([0,N-1, 0, 5])
            plt.plot(abs, self.esp(), color = 'blue', linestyle = 'solid', label = 'Presence - Plante')
            plt.plot(abs, self.bg(), color = 'green', linestyle = 'dashed', label = 'Presence - Graine')
            ax = ax.set(xlabel = "Position des patchs", ylabel = "Presence de l'espece")
            plt.legend(loc = 'upper right')
            plt.title('Etat de la rue')
            fig_line.savefig(nom+form)
            plt.close(fig_line)
    
    def line_plot_obs_save(self,nom):
        """Représente les données de présence/absence de plantesen supposant que les patchs sont ordonnés
        en ligne dans l'ordre utilisé pour la liste définissant le milieu. 
        Sauvegarde le fichier obtenu au format png."""
        try :
            assert type(nom) == type('hello world')
        except AssertionError:
            print('Attention : le nom du fichier doit être une chaîne de caractères. Le fichier ne sera pas créé.')
        else: 
            fig_line = plt.figure()
            ax = plt.axes()        
            N = len(self.liste)
            abs = np.array([i for i in range(N)])
            plt.axis([0,N-1, 0, 5])
            plt.plot(abs, self.esp(), color = 'blue', linestyle = 'solid', label = 'Presence - Plante')
            ax = ax.set(xlabel = "Position des pieds d'arbre", ylabel = "Presence de l'espece")
            plt.legend(loc = 'upper right')
            plt.title('Etat de la rue')
            fig_line.savefig(nom+'.png')
            plt.close(fig_line)
    
    def nbr(self):
        """Retourne le nombre de pieds d'arbres dans le milieu."""
        return len(self.liste)

class ModPRM(object):
    """Permet de créer un objet correspondant au jeu de paramètres d'un modèle PRM.
    Les paramètres à indiquer sont dans l'ordre, la probabilité de colonisation, 
    la probabilité de persistance, la probabilité de germination et la probabilité de 
    mortalité des graines n'ayant pas germé. La proportion initiale de patchs 
    occupés par des graines peut être indiquée en argument supplémentaire."""
    def __init__(self, col, per, germ, mor, pro = 'na'):
        try:
            assert 0 <= col <= 1
            assert 0 <= per <= 1
            assert 0 <= germ <= 1
            assert 0 <= mor <= 1
            if type(pro) != str:
                assert 0 <= pro <= 1
        except AssertionError :
            print('Erreur : les probabilités et/ou les proportions initiales ne sont pas comprises entre 0 et 1 !')
        else :
            self._c = col
            self._p = per
            self._g = germ
            self._d = mor
            self._pi = pro
    
    #Méthodes permettant de bloquer la modification des paramètres du modèle PRM
    def get_c(self):
        return self._c
    
    def set_c(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    c = property(get_c, set_c)
    
    def get_p(self):
        return self._p
    
    def set_p(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    p = property(get_p, set_p)
    
    def get_g(self):
        return self._g
        
    def set_g(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    g = property(get_g, set_g)
    
    def get_d(self):
        return self._d
    
    def set_d(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    d = property(get_d, set_d)
    
    def get_pi(self):
        return self._pi
    
    def set_pi(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    pi = property(get_pi, set_pi)
    
    def affiche(self):
        """Affiche les paramètres du modèle PRM sous forme d'une liste comprenant dans l'ordre
        la probabilité de colonisation, la probabilité de persistance, la probabilité de germination, 
        la probabilité de mort des graines conditionnellement à la non germination et la proportion initiale de 
        patchs comprenant des graines (si applicable)."""
        return([self.c, self.p, self.g, self.d, self.pi])
    
    def matrice_transition_prm(self):
        mat = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        mat[0][0] = 1 - self.c
        mat[0][1] = self.c*(1-self.g)
        mat[0][2] = self.g*self.c
        mat[1][0] = self.d*(1-self.c)
        mat[1][1] = ((1 - self.d + self.d*self.c)*(1-self.g))
        mat[1][2] = self.g*(self.d*self.c + 1 - self.d)
        mat[2][0] = self.d*(1-self.c)*(1-self.p)
        mat[2][1] = (1 - self.d + self.d*self.p + self.d*self.c*(1-self.p))*(1-self.g)
        mat[2][2] = self.g*(1 - self.d + self.d*self.p + (1-self.p)*self.d*self.c)
        return mat
    
class ModLevins(object):
    """Permet de créer un objet correspondant au jeu de paramètres d'un modèle de Levins.
    Les paramètres à indiquer sont dans l'ordre, la constante de diffusion, le paramètre y, 
    la probabilité de persistance, la probabilité de germination et la probabilité de 
    mortalité des graines n'ayant pas germé. La proportion initiale de patchs 
    occupés par des graines peut être indiquée en argument supplémentaire."""
    
    def __init__(self, alph, ygrec, per, germ, mor, pro = 'na'):
        try:
            assert 0 <= alph
            assert 0 <= ygrec
            assert 0 <= per <= 1
            assert 0 <= germ <= 1
            assert 0 <= mor <= 1
            if type(pro) != str:
                assert 0 <= pro <= 1
        except AssertionError :
            print('Erreur : les probabilités et/ou les proportions initiales ne sont pas comprises entre 0 et 1, et/ou les paramètres de diffusion sont négatifs !')
        else :
            self._a = alph
            self._y = ygrec
            self._p = per
            self._g = germ
            self._d = mor
            self._pi = pro
    
    #méthodes bloquant la modification des paramètres du modèle
    def get_a(self):
        return self._a
    
    def set_a(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    a = property(get_a, set_a)
    
    def get_y(self):
        return self._y
    
    def set_y(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    y = property(get_y, set_y)
    
    def get_p(self):
        return self._p
    
    def set_p(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    p = property(get_p, set_p)
    
    def get_g(self):
        return self._g
        
    def set_g(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    g = property(get_g, set_g)
    
    def get_d(self):
        return self._d
    
    def set_d(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    d = property(get_d, set_d)
    
    def get_pi(self):
        return self._pi
    
    def set_pi(self, new):
        print('Opération impossible : les paramètres du modèle ne sont pas modifiables')
    
    pi = property(get_pi, set_pi)
    
    def affiche(self):
        """Retourne la liste des paramètres du modèle de Levins indiqué en argument."""
        return([self.a, self.y, self.p, self.g, self.d, self.pi])
    
class ReproPRM(PiedArbre):
    """Contient les différentes fonctions nécessaires à la simulation de l'évolution
    d'une métapopulation qui évolue suivant le modèle PRM."""
    def __init__(self, param, conditions_initiales):
        self.mod = param
        self.ci = conditions_initiales
    
    def germ_exp(self):
        """Fait germer indépendamment chaque patch avec même probabilité, indépendamment de 
        l'âge de la banque de graines."""
        nbr_pieds = len(self.ci)
        for i in range(nbr_pieds):
            pied = self.ci.patch(i)
            if pied.graine == 1:
                if rd.uniform(0,1) <= self.mod.g:
                    pied.nais_plante() #Les graines mourront plus tard de facon a pouvoir avoir acces au besoin a quelque chose sous le même format que le modele HMM
    
    def reproprm(self):
        """Fait mourir certaines des banques de graines, crée de nouvelles banques de graines
        à partir des plantes présentes, et fait mourir les plantes."""
        nbr_pieds = len(self.ci)
        for i in range(nbr_pieds):
            pied = self.ci.patch(i)
            if pied.graine ==1:
                if rd.uniform(0,1) <= self.mod.d:
                    pied.mort_graine()
            if pied.plante == 1:
                pied.mort_plante()
                if rd.uniform(0,1) <= self.mod.p:
                    pied.nais_graine()
            if rd.uniform(0,1) <= self.mod.c:
                pied.nais_graine()
    
    def prm_generation(self):
        """Effectue un cycle complet de reproduction selon le modèle PRM."""
        self.reproprm()
        self.germ_exp()

class ReproLevins(PiedArbre):
    def __init__(self, param, conditions_initiales):
        self.mod = param
        self.ci = conditions_initiales
    
    def disp_kernel(self, i, j):
        """Dispersion depuis le patch j vers le patch i."""
        dist = np.sqrt((self.ci.patch(i).x - self.ci.patch(j).x)**2 + (self.ci.patch(i).y - self.ci.patch(j).y)**2)
        return np.exp(-self.mod.a * dist)
    
    def connect(self, i):
        """Connectivité du patch i."""
        val = 0
        for j in range(self.ci.nbr()):
            if j != i:
                if self.ci.patch(j).plante != 0:
                    val += self.disp_kernel(i,j)
        return val
    
    def reprolevins(self):
        """Fait mourir certaines des banques de graines, crée de nouvelles banques de graines
        à partir des plantes présentes, et fait mourir les plantes."""
        nbr_pieds = self.ci.nbr()
        for i in range(nbr_pieds):           
            pied = self.ci.patch(i)
            if pied.graine ==1:
                if rd.uniform(0,1) <= self.mod.d:
                    pied.mort_graine()
            if pied.plante == 1:
                pied.mort_plante()
                if rd.uniform(0,1) <= self.mod.p:
                    pied.nais_graine()
        for i in range(nbr_pieds):
            pied = self.ci.patch(i)
            col_i = 1 - np.exp(-self.mod.y * self.connect(i))
            if rd.uniform(0,1) <= col_i:
                pied.nais_graine()
    
    def germ_exp(self):
        """Fait germer indépendamment chaque patch avec même probabilité, indépendamment de 
        l'âge de la banque de graines."""
        nbr_pieds = self.ci.nbr()
        for i in range(nbr_pieds):
            pied = self.ci.patch(i)
            if pied.graine == 1:
                if rd.uniform(0,1) <= self.mod.g:
                    pied.nais_plante()
    
    def levins_generation(self):
        """Effectue un cycle complet de reproduction selon le modèle de Levins."""
        self.reprolevins()
        self.germ_exp()

class GenerateurCI():
    """Prend en argument le nombre de patchs, la proportion initiale de graines attendues, et les pas en x et en y.
    Retourne des conditions initiales avant germination."""
    def __init__(self, npatch, pgraines, pasx, pasy):
        self.N = npatch
        self.pg = pgraines
        self.dx = pasx
        self.dy = pasy
    
    def generation_unif(self):
        """Permet de générer une répartition dans laquelle l'espèce peut indifféremment être présente partout."""
        liste = []
        for i in range(self.N):
            etat_g = rd.uniform(0,1)
            if etat_g <= self.pg:
                liste.append(PiedArbre(self.dx*i, self.dy*i, 0, 1))
            else:
                liste.append(PiedArbre(self.dx*i, self.dy*i, 0, 0))
        return liste

def generation_CI_complet_prm(n_patch, prop_init, dx, dy, modele):
    """Génère des conditions initiales après germination, dans le cadre du modèle PRM."""
    try :
        if type(modele.pi) != type('hello world'):
            assert modele.pi == prop_init
    except AssertionError :
        print("Attention : la proportion initiale de graines dans le modèle est différente de celle indiquée en argument. Seule celle du modèle sera conservée.")
        prop_init = modele.pi
    finally: 
        gen_CI = GenerateurCI(n_patch, prop_init, dx, dy)
        milieu = Milieu(gen_CI.generation_unif())
        pop = ReproPRM(modele, milieu)
        pop.germ_exp()
        return(pop)

def generation_CI_complet_levins(n_patch, prop_init, dx, dy, modele):
    """Génère des conditions initiales après germination, dans le cadre du modèle de Levins."""
    try :
        if type(modele.pi) != type('hello world'):
            assert modele.pi == prop_init
    except AssertionError :
        print("Attention : la proportion initiale de graines dans le modèle est différente de celle indiquée en argument. Seule celle du modèle sera conservée.")
        prop_init = modele.pi
    finally: 
        gen_CI = GenerateurCI(n_patch, prop_init, dx, dy)
        milieu = Milieu(gen_CI.generation_unif())
        pop = ReproLevins(modele, milieu)
        pop.germ_exp()
        return(pop)

if __name__ == "__main__":
    modele = ModLevins(0.6, 0.4, 0.1, 0.8, 1, 0.7)
    pop = generation_CI_complet_levins(50, 0.5, 0.1, 0.5, modele)
    pop.ci.line_plot_save('1')
    pop.levins_generation()
    pop.ci.line_plot_save('2')
    
