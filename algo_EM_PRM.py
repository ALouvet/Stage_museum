# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 11:34:23 2018

@author: apolline l
"""

import generation_simulation as gs
import representation_simulation as rs
from numpy import *

def lecture_data(nom_du_csv):
    """Lit uniquement les données de présence absence, sans les coordonnées des patchs."""
    return rs.lire_csv(nom_du_csv)[0]

def liste_data_manquante(data):
    """Donne une liste contenant une sous-liste pour chaque patch, laquelle 
    comporte la liste des générations manquantes pour ce patch."""
    nbr_t = len(data) #Une ligne = une année d'observation
    nbr_pa = len(data[0]) #Une colonne = un patch
    liste = [[] for i in range(nbr_pa)]
    for i in range(nbr_pa):
        for t in range(nbr_t):
            if data[t][i] == 'na':
                liste[i].append(t)
    return liste
    
class ListePlante(object):
    """Contient la liste des observations pour un patch."""
    
    def __init__(self, liste):
        """prend en argument la liste d'observations pour un patch."""
        self.plante = liste
        self.tps = len(liste)
        try :
            for value in liste:
                assert value in [1, 0, 'na', '1', '0', '1.0', '0.0']
        except AssertionError:
            print('Attention : certaines données ne sont pas au format désiré. Celles-ci ont donc été considérées comme des données manquantes.')
        finally :
            for i in range(self.tps):
                value = liste[i]
                if value in ['1', '1.0']:
                    liste[i] = 1
                if value in ['0', '0.0']:
                    liste[i] = 0
                if value not in [1, 0, 'na', '1', '0', '1.0', '0.0']:
                    liste[i] = 'na'
    
    #méthodes conservant les données au bon format
    def __getitem__(self, index):
        return self.plante[index]
    
    def __setitem__(self, index, value):
        try:
            assert value in [1, 0, 'na']
        except AssertionError :
            print("Opération impossible : une donnée de présence absence ne peut être qu'au format 1, 0 ou na")
        else:
            self.plante[index] = value
    
    def __len__(self):
        return self.tps
    
    def complete(self, index, value):
        """Change la valeur de l'une des données de présence/absence."""
        self[index] = value
    
    def affiche(self):
        """Retourne la liste des données de présence/absence de plantes."""
        return self.plante
    
    def obs_manq(self):
        """Fait la liste des observations manquantes."""
        manq = []
        for i in range(self.tps):
            if self[i] == 'na':
                manq.append(i)
        return(manq)
    
    def completion(self):
        """Retourne la liste de toutes les completions de donnees manquantes possibles."""
        liste = [[]]
        for i in range(self.tps):
            nbr = len(liste)
            if self[i] == 0:
                for j in range(nbr):
                    liste[j].append(0)
            if self[i] == 1:
                for j in range(nbr):
                    liste[j].append(1)
            if self[i] == 'na':
                for j in range(nbr):
                    liste.append(liste[j][:])
                    liste[j].append(0)
                    liste[-1].append(1)
        liste2 = [ListePlante(a) for a in liste]
        return liste2
    
    def bg_compatible(self):
        """Retourne la liste des états pour la banque de graines compatibles avec les observations."""
        liste = [[]]
        for i in range(self.tps):
            nbr = len(liste)
            if self[i] == 0:
                for j in range(nbr):
                    liste.append(liste[j][:])
                    liste[j].append(0)
                    liste[-1].append(1)
            if self[i] == 1:
                for j in range(nbr):
                    liste[j].append(2)
            if self[i] == 'na':
                for j in range(nbr):
                    liste.append(liste[j][:])
                    liste.append(liste[j][:])
                    liste[j].append(0)
                    liste[-1].append(1)
                    liste[-2].append(2)
        return liste
    
    def proba_obs(self, modprm):
        """Calcule la probabilité d'observer la série d'observations donné en argument
        dans le cadre du modèle PRM donné en argument."""
        liste = self.bg_compatible()
        proba = 0
        mat = modprm.matrice_transition_prm()
        for i in range(len(liste)):
            proba_i = 0
            obs = liste[i]
            if obs[0] == 1 : 
                proba_i = modprm.pi*(1-modprm.g)
            if obs[0] == 2:
                proba_i = modprm.pi*modprm.g
            if obs[0] == 0 :
                proba_i = 1-modprm.pi
            for j in range(1, self.tps):
                if obs[j-1] == 0:
                    if obs[j] == 0:
                        proba_i *= mat[0][0]
                    elif obs[j] == 1:
                        proba_i *= mat[0][1]
                    else:
                        proba_i *= mat[0][2]
                elif obs[j-1] == 1:
                    if obs[j] == 0:
                        proba_i *= mat[1][0]
                    elif obs[j] == 1:
                        proba_i *= mat[1][1]
                    else:
                        proba_i *= mat[1][2]
                elif obs[j-1] == 2:
                    if obs[j] == 0:
                        proba_i *= mat[2][0]
                    elif obs[j] == 1:
                        proba_i *= mat[2][1]
                    else:
                        proba_i *= mat[2][2]
            proba += proba_i
        return(proba)
    
    def proba_obs_opt1(self, modprm):
        liste = [[]]
        mat = modprm.matrice_transition_prm()
        obs = self.plante
        #Etape 1 : initialisation
        if obs[0] == 1:
            liste[0] = [(2, modprm.pi*modprm.g)]
        elif obs[0] == 0 :
            liste[0] = [(0, 1-modprm.pi)]
            liste.append([(1, modprm.pi*(1-modprm.g))])      
        elif obs[0] == 'na' :
            liste[0] = [(0, 1-modprm.pi)]
            liste.append([(1, modprm.pi*(1-modprm.g))])
            liste.append([(2, modprm.pi*modprm.g)])
        
        #Etape 2 : completion
        for i in range(1, self.tps):
            nbr = len(liste)
            if self[i] == 0:
                for j in range(nbr):
                    liste.append(liste[j][:])
                    liste[j].append((0, mat[liste[j][-1][0]][0]*liste[j][-1][1]))
                    liste[-1].append((1, mat[liste[-1][-1][0]][1]*liste[-1][-1][1]))
            if self[i] == 1:
                for j in range(nbr):
                    liste[j].append((2, mat[liste[j][-1][0]][2]*liste[j][-1][1]))
            if self[i] == 'na':
                for j in range(nbr):
                    liste.append(liste[j][:])
                    liste.append(liste[j][:])
                    liste[j].append((0, mat[liste[j][-1][0]][0]*liste[j][-1][1]))
                    liste[-1].append((1, mat[liste[-1][-1][0]][1]*liste[-1][-1][1]))
                    liste[-2].append((2, mat[liste[-2][-1][0]][2]*liste[-2][-1][1]))
        proba = 0
        for elem in liste:
            proba += elem[-1][1]
        return proba
    
def lire_colonne_csv(lecture_csv):
    """Permet, une fois lu un fichier CSV, de découper son contenu en colonnes.
    Prend en argument ce qui est retourne par lire_csv."""
    data = lecture_csv[0]
    nbr_pa = len(data[0])
    liste_pa = []
    for i in range(nbr_pa):
        pa = []
        for j in range(len(data)):
            if data[j][i] == 'na':
                pa.append(data[j][i])
            else:
                pa.append(int(data[j][i]))
        liste_pa.append(ListePlante(pa[:]))
    return liste_pa

def algo_fb_prm(patch, modprm):
    """implementation de l'algorithme forwards-backwards.
    Attention : le patch doit contenir des donnees completes. """
    try :
        assert 'na' not in patch.plante
    except AssertionError:
        print("opération impossible : l'algorithme FB nécessite des données complètes.")
    #Etape 1 : creation des matrices contenant les valeurs pour alpha et beta
    alpha = [0 for i in range(patch.tps)]
    beta = [0 for i in range(patch.tps)]
    mat = modprm.matrice_transition_prm()    
    
    #Etape 2 : initialisations
    #Pour alpha
    if patch[0] == 0:
        alpha[0] = [1 - modprm.pi, modprm.pi*(1-modprm.g), 0]
    else :
        alpha[0] = [0, 0, modprm.pi*modprm.g]
    #Pour beta
    beta[-1] = [1, 1, 1]
    
    #Etape 3 : completion par recurrence
    #Pour alpha
    for i in range(1, patch.tps):
        alpha_0 = alpha[i-1][0]*mat[0][0] + alpha[i-1][1]*mat[1][0] + alpha[i-1][2]*mat[2][0]
        alpha_1 = alpha[i-1][0]*mat[0][1] + alpha[i-1][1]*mat[1][1] + alpha[i-1][2]*mat[2][1]
        alpha_2 = alpha[i-1][0]*mat[0][2] + alpha[i-1][1]*mat[1][2] + alpha[i-1][2]*mat[2][2]
        alpha[i] = [(1-patch[i])*alpha_0, (1-patch[i])*alpha_1, patch[i]*alpha_2]
    #Pour beta
    for i in range(patch.tps-2, -1, -1):
        beta_0 = mat[0][0]*beta[i+1][0]*(1-patch[i+1]) + mat[0][1]*beta[i+1][1]*(1-patch[i+1]) + mat[0][2]*beta[i+1][2]*patch[i+1]
        beta_1 = mat[1][0]*beta[i+1][0]*(1-patch[i+1]) + mat[1][1]*beta[i+1][1]*(1-patch[i+1]) + mat[1][2]*beta[i+1][2]*patch[i+1]
        beta_2 = mat[2][0]*beta[i+1][0]*(1-patch[i+1]) + mat[2][1]*beta[i+1][1]*(1-patch[i+1]) + mat[2][2]*beta[i+1][2]*patch[i+1]
        beta[i] = [beta_0, beta_1, beta_2]
    return alpha, beta

def algo_fb_prm_rescale(patch, modprm):
    """implementation de l'algorithme forwards-backwards.
    Attention : le patch doit contenir des donnees completes. """
    try :
        assert 'na' not in patch.plante
    except AssertionError:
        print("opération impossible : l'algorithme FB nécessite des données complètes.")
    #Etape 1 : creation des matrices contenant les valeurs pour alpha et beta
    alpha = [0 for i in range(patch.tps)]
    beta = [0 for i in range(patch.tps)]
    coef = [1 for i in range(patch.tps)]
    mat = modprm.matrice_transition_prm()    
    
    #Etape 2 : initialisations
    #Pour alpha
    if patch[0] == 0:
        alpha[0] = [1 - modprm.pi, modprm.pi*(1-modprm.g), 0]
    else :
        alpha[0] = [0, 0, modprm.pi*modprm.g]
    
    #Etape 3 : completion par recurrence
    #Pour alpha
    for i in range(1, patch.tps):
        alpha_0 = alpha[i-1][0]*mat[0][0] + alpha[i-1][1]*mat[1][0] + alpha[i-1][2]*mat[2][0]
        alpha_1 = alpha[i-1][0]*mat[0][1] + alpha[i-1][1]*mat[1][1] + alpha[i-1][2]*mat[2][1]
        alpha_2 = alpha[i-1][0]*mat[0][2] + alpha[i-1][1]*mat[1][2] + alpha[i-1][2]*mat[2][2]
        alpha_0 *= (1-patch[i])
        alpha_1 *= (1-patch[i])
        alpha_2 *= patch[i]
        somme = alpha_0 + alpha_1 + alpha_2
        alpha_0 *= 1.0/somme
        alpha_1 *= 1.0/somme
        alpha_2 *= 1.0/somme
        alpha[i] = [alpha_0, alpha_1, alpha_2]
        coef[i] = somme
    #Pour beta
    #Etape 2
    beta[-1] = [1.0/coef[-1], 1.0/coef[-1], 1.0/coef[-1]]
    for i in range(patch.tps-2, -1, -1):
        beta_0 = mat[0][0]*beta[i+1][0]*(1-patch[i+1]) + mat[0][1]*beta[i+1][1]*(1-patch[i+1]) + mat[0][2]*beta[i+1][2]*patch[i+1]
        beta_1 = mat[1][0]*beta[i+1][0]*(1-patch[i+1]) + mat[1][1]*beta[i+1][1]*(1-patch[i+1]) + mat[1][2]*beta[i+1][2]*patch[i+1]
        beta_2 = mat[2][0]*beta[i+1][0]*(1-patch[i+1]) + mat[2][1]*beta[i+1][1]*(1-patch[i+1]) + mat[2][2]*beta[i+1][2]*patch[i+1]
        beta_0 *= 1.0/coef[i]
        beta_1 *= 1.0/coef[i]
        beta_2 *= 1.0/coef[i]
        beta[i] = [beta_0, beta_1, beta_2]
    return alpha, beta, coef

def obs_bg_simple(alpha, beta, coef, tps, lo, modprm):
    """Permet de calculer la probabilité que la banque de graines d'un patch soit dans un 
    état donné sachant des observations complètes."""
    cst = 1.0/sum(alpha[-1])
    liste = [0 for i in range(tps)]
    
    for i in range(tps):
        liste[i] = [cst*alpha[i][0]*beta[i][0]*coef[i], cst*alpha[i][1]*beta[i][1]*coef[i], cst*alpha[i][2]*beta[i][2]*coef[i]]
    return liste

def obs_bg_trans(alpha, beta, tps, lo, modprm, obs_cond):
    """Idem mais pour la probabilité de deux etats consecutifs."""
    cst = 1.0/sum(alpha[-1])
    mat = modprm.matrice_transition_prm() 
    
    liste = [ [[0, 0, 0], [0, 0, 0], [0, 0, 0]] for i in range(lo-1)]
    
    for i in range(tps-1):
        liste[i][0] = [alpha[i][0]*mat[0][0]*beta[i+1][0]*(1-obs_cond[i+1])*cst, alpha[i][0]*mat[0][1]*beta[i+1][1]*(1-obs_cond[i+1])*cst, alpha[i][0]*mat[0][2]*beta[i+1][2]*(obs_cond[i+1])*cst]
        liste[i][1] = [alpha[i][1]*mat[1][0]*beta[i+1][0]*(1-obs_cond[i+1])*cst, alpha[i][1]*mat[1][1]*beta[i+1][1]*(1-obs_cond[i+1])*cst, alpha[i][1]*mat[1][2]*beta[i+1][2]*(obs_cond[i+1])*cst]
        liste[i][2] = [alpha[i][2]*mat[2][0]*beta[i+1][0]*(1-obs_cond[i+1])*cst, alpha[i][2]*mat[2][1]*beta[i+1][1]*(1-obs_cond[i+1])*cst, alpha[i][2]*mat[2][2]*beta[i+1][2]*(obs_cond[i+1])*cst]
        
    return liste

def etape_EM_PRM(liste_obs, modprm):
    api = 0
    bpi = 0
    ag = 0
    bg = 0
    ac = 0
    bc = 0
    ac2 = 0
    bc2 = 0
    ap2 = 0
    bp2 = 0
    vrais2 = 0
    #On separe la liste d'observations en les differents patchs
    for obs in liste_obs:

        algo_fb = algo_fb_prm_rescale(obs, modprm)   
     
        alpha = algo_fb[0]
        beta = algo_fb[1]
        coef = algo_fb[2]
        
        vrais2 += log(coef[-1])
        for value in coef:
            vrais2 += log(value)
        
        tps = obs.tps
        lo = len(obs)

        proba_s = obs_bg_simple(alpha, beta, coef, tps, lo, modprm)
        proba_t = obs_bg_trans(alpha, beta, tps, lo, modprm, obs)
        
        bpi += proba_s[0][0]
        api += (proba_s[0][1] + proba_s[0][2])
        
        ag += proba_s[0][2]
        bg += (proba_s[0][1])
        
        for j in range(len(obs)-1):
            ag += (proba_t[j][0][2] + proba_t[j][1][2] + proba_t[j][2][2])
            bg += (proba_t[j][0][1] + proba_t[j][1][1] + proba_t[j][2][1])
            
            ac += (proba_t[j][0][1] + proba_t[j][0][2])
            bc += proba_t[j][0][0]
            
            bc2 += (proba_t[j][1][0])
            ac2 += (proba_t[j][1][1] + proba_t[j][1][2])
            
            ap2 += (proba_t[j][2][1] + proba_t[j][2][2])
            bp2 += (proba_t[j][2][0])
    #On optimise
    npi = api/(api+bpi)
    ng = ag/(ag+bg)
    
    nc = ac/(ac+bc)
    nc2 = ac2/(ac2+bc2)
    np2 = ap2/(ap2+bp2)
    
    if np2 < nc2:
        nc2 = np2
        print('optimisation ratée')
    if nc2 < nc:
        nc = nc2
        print('optimisation ratée')

    nd = (1-nc2)/(1-nc)
    np = 1 - (1-np2)/(1-nc2)
    
#    if npi < 0.05:
#        npi = 0.05
#    if npi > 0.95:
#        npi = 0.95
#    if nc < 0.05 :
#        nc = 0.05
#    if nc > 0.95:
#        nc = 0.95
#    if ng < 0.05 :
#        ng = 0.05
#    if ng > 0.95 :
#        ng = 0.95
#    if nd < 0.05 :
#        nd = 0.05
#    if nd > 0.95 :
#        nd = 0.95
#    if np < 0.05:
#        np = 0.05
#    if np > 0.95 :
#        np = 0.95
    
    #On calcule la vraisemblance
    vrais = api*log(npi)+bpi*log(1-npi)+ag*log(ng)+bg*log(1-ng) + ac*log(nc)+bc*log(1-nc)
    vrais += ac2*log(nc2)+bc2*log(1-nc2)+ap2*log(np2)+bp2*log(1-np2)
#    AIC = 10 - 2*vrais
    AIC2 = 10 - 2*vrais2

    newmod = gs.ModPRM(nc, np, ng, nd, npi)
#    return (newmod , exp(vrais), AIC, AIC2)
    return (newmod , exp(vrais), AIC2)

def etape_EM_PRM_BGS(liste_obs, modprm):
    try:
        assert modprm.p == 1
    except AssertionError:
        print("Attention : le modèle PRM entré en argument n'est pas un modèle à banque graines à germination simple.")
        return(modprm)
        
    api = 0
    bpi = 0
    ag = 0
    bg = 0
    ac = 0
    bc = 0
    ac2 = 0
    bc2 = 0
    vrais2 = 0
    #On separe la liste d'observations en les differents patchs
    for obs in liste_obs:
        algo_fb = algo_fb_prm_rescale(obs, modprm)

        alpha = algo_fb[0]
        beta = algo_fb[1]
        coef = algo_fb[2]
        
        tps = obs.tps
        lo = len(obs)
        
        vrais2 += log(coef[-1])
        for value in coef:
            vrais2 += log(value)
        
        proba_s = obs_bg_simple(alpha, beta, coef, tps, lo, modprm)
        proba_t = obs_bg_trans(alpha, beta, tps, lo, modprm, obs)
        
        bpi += proba_s[0][0]
        api += (proba_s[0][1] + proba_s[0][2])
        
        ag += proba_s[0][2]
        bg += (proba_s[0][1])
        
        for j in range(len(obs)-1):
            ag += (proba_t[j][0][2] + proba_t[j][1][2] + proba_t[j][2][2])
            bg += (proba_t[j][0][1] + proba_t[j][1][1] + proba_t[j][2][1])
            
            ac += (proba_t[j][0][1] + proba_t[j][0][2])
            bc += proba_t[j][0][0]
            
            bc2 += (proba_t[j][1][0])
            ac2 += (proba_t[j][1][1] + proba_t[j][1][2])

    #On optimise
    npi = api/(api+bpi)
    ng = ag/(ag+bg)
    
    if ac + bc == 0:
        ac += 0.001
    nc = ac/(ac+bc)
    nc2 = ac2/(ac2+bc2)
    
    if nc == 1 :
        nc = 0.99

    if nc2 < nc:
        nc = nc2
        #print('optimisation ratée')
   
    nd = (1-nc2)/(1-nc)
    
    np = 1
    
    vrais = api*log(npi) + bpi*log(1-npi) + ag*log(ng) + bg*log(1-ng)
    vrais += ac*log(nc) + bc*log(1-nc) + ac2*log(nc2) + bc2*log(1-nc2)
    
    try :
        newmod = gs.ModPRM(nc, np, ng, nd, npi)
    except :
        return(modprm, 0, 10000)
    return (newmod, exp(vrais), 8 - 2*vrais2)

#def etape_EM_PRM_SB(liste_obs):
#    """Permet d'estimer les paramètres dans le cadre du modèle sans banque de graines.
#    Attention : ne permet pas de traiter le cas des données manquantes."""
#    nbr_obs = len(liste_obs)
#    nbr_1 = 0
#    nbr_t_0 = 0
#    nbr_t_1 = 0
#    nbr_t_10 = 0
#    nbr_t_01 = 0
#    for obs in liste_obs :
#        nbr_1 += obs[0]
#        for i in range(1, len(obs)):
#            nbr_t_1 += obs[i-1]
#            nbr_t_0 += 1 - obs[i-1]
#            nbr_t_01 += (1-obs[i-1])*obs[i]
#            nbr_t_10 += obs[i-1]*(1-obs[i])
#    pi = nbr_1*1.0/nbr_obs
#    c = nbr_t_01*1.0/nbr_t_0
#    A = nbr_t_10*1.0/nbr_t_1
#    if A > 1 - c:
#        print('Attention : le modèle PRM sans banque de graines ne permet pas de bien rendre compte de la dynamique.')
#        A = 1 - c
#    p = 1 - (A*1.0/(1-c))
#    vrais = 0
#    for obs in liste_obs :
#        vrais += (obs[0]*log(pi) + (1-obs[0])*log(1-pi))
#        for i in range(1, len(obs)):
#            vrais += (1-obs[i-1])*(1-obs[i])*log(1-c)
#            vrais += (1-obs[i-1])*obs[i]*log(c)
#            vrais += obs[i-1]*(1-obs[i])*log((1-p)*(1-c))
#            vrais += obs[i-1]*obs[i]*log(p + (1-p)*c)
#    print(c)
#    print(p)
#    print(pi)
#    return (gs.ModPRM(c, p, 1, 1, pi), exp(vrais), 6 - 2*vrais)

def etape_EM_PRM_SB(liste_obs):
    """Permet d'estimer les paramètres dans le cadre du modèle sans banque de graines.
    Attention : ne permet pas de traiter le cas des données manquantes."""
    nbr_obs = len(liste_obs)
    nbr_1 = 0
    nbr_t_0 = 0
    nbr_t_1 = 0
    nbr_t_10 = 0
    nbr_t_01 = 0
    for obs in liste_obs :
        nbr_1 += obs[0]
        for i in range(1, len(obs)):
            nbr_t_1 += obs[i-1]
            nbr_t_0 += 1 - obs[i-1]
            nbr_t_01 += (1-obs[i-1])*obs[i]
            nbr_t_10 += obs[i-1]*(1-obs[i])
    pi = nbr_1*1.0/nbr_obs
    try :
        c = nbr_t_01*1.0/nbr_t_0
    except :
        c = 0.99
    try :
        A = nbr_t_10*1.0/nbr_t_1
    except :
        A = 0.99
    if c == 1 :
        c = 0.99
    if A > 1 - c:
        print('Attention : le modèle PRM sans banque de graines ne permet pas de bien rendre compte de la dynamique.')
        A = 1 - c
    p = 1 - (A*1.0/(1-c))
    vrais = 0
    for obs in liste_obs :
        if obs[0] == 0:
            coef = pi
        else :
            coef = 1 - pi
        for i in range(1, len(obs)):
            if obs[i-1] == 0:
                if obs[i] == 0:
                    coef *= (1-c)
                else :
                    coef *= c
            else :
                if obs[i] == 0:
                    coef *= (1-p)*(1-c)
                else :
                    coef *= (p + (1-p)*c)
                    
        vrais += log(coef)
    return (gs.ModPRM(c, p, 1, 1, pi), exp(vrais), 6 - 2*vrais)
    
if __name__ == '__main__':
    patch_ex = ListePlante([0, 1, 1, 1, 0, 1, 0, 1, 0])
    prm_ex = ModPRM(0.8, 0.6, 0.3, 0.2, 0.5)
    for i in range(10):
        res = etape_EM_PRM([patch_ex, patch_ex], prm_ex)
        print(res[2])
#        print(res[3])
        prm_ex = res[0]
        print(prm_ex.c, prm_ex.p, prm_ex.g, prm_ex.d, prm_ex.pi)

      
    
