# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:16:40 2018

@author: apolline l
"""

from representation_simulation import *
from algo_EM_PRM import *
from Tkinter import *
import PIL.ImageTk
import PIL.Image
import tkFileDialog 
import FileDialog
import random 
import shutil

#Colonisation, persistance, germination, mort, y, dispersion, proportion initiale
valparam = [0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5]  

root = Tk()
frame_v = Frame(root)
frame_e = Frame(root)

#########################################
#Structure commune aux différents frames#
#########################################

def frame_v_visul():
    try:
        frame_e.grid_forget()
    except :
        pass
    frame_v.grid(row = 1, column = 1, rowspan = 15, columnspan = 11)

def frame_e_visul():
    try :
        frame_v.grid_forget()
    except:
        pass
    frame_e.grid(row = 1, column = 1, rowspan = 15, columnspan = 11)

Button(root, text = "Génération d'une simulation", command = frame_v_visul).grid(row = 0, column = 1, sticky = W)
Button(root, text = "Estimation de paramètres", command = frame_e_visul).grid(row = 0, column = 2, sticky = W)
Button(root, text = 'Quitter', command = root.destroy).grid(row = 0, column = 9, sticky = E)

##########################################
#Frame 1 : visualisation des simulations #
##########################################

#Probabilite de colonisation
c = StringVar()
c.set(str(valparam[0]))
labc = Label(frame_v, text = "Probabilité de colonisation")
entc = Entry(frame_v, textvariable = c)

#Probabilite de persistance
p = StringVar()
p.set(str(valparam[1]))
labp = Label(frame_v, text = "Probabilité de persistance")
entp = Entry(frame_v, textvariable = p)

#Probabilite de germination
g = StringVar()
g.set(str(valparam[2]))
labg = Label(frame_v, text = "Probabilité de germination")
entg = Entry(frame_v, textvariable = g)

#Probabilité de mort des graines
d = StringVar()
d.set(str(valparam[3]))
labd = Label(frame_v, text = "Probabilité de mort des graines")
entd = Entry(frame_v, textvariable = d)

#Parametre y
y = StringVar()
y.set(str(valparam[4]))
laby = Label(frame_v, text = 'Paramètre y')
enty = Entry(frame_v, textvariable = y)

#Constante de dispersion
aa = StringVar()
aa.set(str(valparam[5]))
laba = Label(frame_v, text = 'Constante de dispersion')
enta = Entry(frame_v, textvariable = aa)

#Proportion initiale
pinit =StringVar()
pinit.set(str(valparam[6]))
labinit = Label(frame_v, text = "Proportion initiale de graines")
entinit = Entry(frame_v, textvariable = pinit)

#Liste des parametres pour la génération des simulations
#Nombre de pieds d'arbre
npa = IntVar()    
npa.set(30)
Label(frame_v, text = 'Nombre de patchs :').grid(row = 10, column = 1, sticky = W)
n_patchs = Entry(frame_v, textvariable = npa)
n_patchs.grid(row = 10, column = 2, sticky = W)

#Duree d'observation
nt = IntVar()
nt.set(5)
Label(frame_v, text = "Temps d'observation :").grid(row = 11, column = 1, sticky = W)
n_t = Entry(frame_v, textvariable = nt)
n_t.grid(row = 11, column = 2, sticky = W)

#Pas en abscisse
dpx = StringVar()
dpx.set('0.1')
Label(frame_v, text = "Pas dans la direction x :").grid(row = 12, column = 1, sticky = W)
dx = Entry(frame_v, textvariable = dpx)
dx.grid(row = 12, column = 2, sticky = W)

#Pas en ordonnee
dpy = StringVar()
dpy.set('0.5')
Label(frame_v, text = "Pas dans la direction y :").grid(row = 13, column = 1, sticky = W)
dy = Entry(frame_v, textvariable = dpy)
dy.grid(row = 13, column = 2, sticky = W)

#Fonction de mise a jour des parametres
def maj_param():
    """Mise a jour des parametres du modele."""
    global c, p, g, d, y, aa, pinit, valparam, varMod, varBg 
    a = varMod.get()
    b = varBg.get()
    bouton.grid_forget()
    bouton2.grid(row = 11, column = 7, sticky = W)
    bouton3.grid(row = 8, column = 1)
    valparam[6] = pinit.get()
    labinit.grid_forget()
    entinit.grid_forget()
    if a == 0:
        valparam[0] = c.get()
        labc.grid_forget()
        entc.grid_forget()
        if b == 0:
            valparam[1] = p.get()
            labp.grid_forget()
            entp.grid_forget()
            valparam[2] = 1
            valparam[3] = 1
        elif b == 1:
            valparam[1] = 1
            valparam[2] = g.get()
            labg.grid_forget()
            entg.grid_forget()
            valparam[3] = d.get()
            labd.grid_forget()
            entd.grid_forget()
        else:
            valparam[1] = p.get()
            labp.grid_forget()
            entp.grid_forget()
            valparam[2] = g.get()
            labg.grid_forget()
            entg.grid_forget()
            valparam[3] = d.get()
            labd.grid_forget()
            entd.grid_forget()
    else:
        valparam[0] = 0
        valparam[4] = y.get()
        laby.grid_forget()
        enty.grid_forget()
        valparam[5] = aa.get()
        laba.grid_forget()
        enta.grid_forget()
        if b == 0:
            valparam[1] = p.get()
            labp.grid_forget()
            entp.grid_forget()
            valparam[2] = 1
            valparam[2] = 1
        elif b == 1:
            valparam[1] = 1
            valparam[2] = g.get()
            labg.grid_forget()
            entg.grid_forget()
            valparam[3] = d.get()
            labd.grid_forget()
            entd.grid_forget()
        else:
            valparam[1] = p.get()
            labp.grid_forget()
            entp.grid_forget()
            valparam[2] = g.get()
            labg.grid_forget()
            entg.grid_forget()
            valparam[3] = d.get()
            labd.grid_forget()
            entd.grid_forget()
bouton = Button(frame_v, text = 'Mettre à jour les paramètres', command = maj_param)
            
def entrer_param():
    """Saisie des paramètres du modèle sélectionné."""
    global varMod, varBg, valparam
    a = varMod.get()
    b = varBg.get()
    bouton3.grid_forget()
    if a == 0:
        labc.grid(row = 10, column = 3, sticky = W)    
        entc.grid(row = 10, column = 4, sticky = W)
        if b == 0:
            labp.grid(row = 11, column = 3, sticky = W)
            entp.grid(row = 11, column = 4, sticky = W)
            labinit.grid(row = 12, column = 3, sticky = W)
            entinit.grid(row = 12, column = 4, sticky = W)
        elif b == 1:
            labg.grid(row = 11, column = 3, sticky = W) 
            entg.grid(row = 11, column = 4, sticky = W)
            labd.grid(row = 12, column = 3, sticky = W)
            entd.grid(row = 12, column = 4, sticky = W)
            labinit.grid(row = 13, column = 3, sticky = W)
            entinit.grid(row = 13, column = 4, sticky = W)
        else :
            labp.grid(row = 11, column = 3, sticky = W)
            entp.grid(row = 11, column = 4, sticky = W)
            labg.grid(row = 12, column = 3, sticky = W)
            entg.grid(row = 12, column = 4, sticky = W)
            labd.grid(row = 13, column = 3, sticky = W)
            entd.grid(row = 13, column = 4, sticky = W)
            labinit.grid(row = 10, column = 5, sticky = W)
            entinit.grid(row = 10, column = 6, sticky = W)
    else:
        laby.grid(row = 10, column = 3, sticky = W)
        enty.grid(row = 10, column = 4, sticky = W)
        laba.grid(row = 11, column = 3, sticky = W)
        enta.grid(row = 11, column = 4, sticky = W)
        labinit.grid(row = 12, column = 3, sticky = W)
        entinit.grid(row = 12, column = 4, sticky = W)
        if b == 0:
            labp.grid(row = 10, column = 5, sticky = W)
            entp.grid(row = 10, column = 6, sticky = W)
        elif b == 1:
            labg.grid(row = 10, column = 5, sticky = W)
            entg.grid(row = 10, column = 6, sticky = W)
            labd.grid(row = 11, column = 5, sticky = W)
            entd.grid(row = 11, column = 6, sticky = W)
        else :
            labp.grid(row = 10, column = 5, sticky = W)
            entp.grid(row = 10, column = 6, sticky = W)
            labg.grid(row = 11, column = 5, sticky = W)
            entg.grid(row = 11, column = 6, sticky = W)
            labd.grid(row = 12, column = 5, sticky = W)
            entd.grid(row = 12, column = 6, sticky = W)
    bouton.grid(row = 10, column = 7, sticky = W)
    
bouton3 = Button(frame_v, text = "Entrer les paramètres du modèle", command = entrer_param)
bouton3.grid(row = 8, column = 1)

#Generation des simulations
animation = 0

def simulate():
    """Simulation du modèle choisi à partir des paramètres entrés."""
    if float(valparam[0]) != 0:
        modele = ModPRM(float(valparam[0]), float(valparam[1]), float(valparam[2]), float(valparam[3]), float(valparam[6]))
        pop = generation_CI_complet_prm(int(npa.get()), float(valparam[6]), float(dpx.get()), float(dpy.get()), modele)
        simulation_prm_csv_complete(pop, int(nt.get()), 'temp')
        visul_GUI('temp')
    else :
        modele = ModLevins(float(valparam[5]), float(valparam[4]), float(valparam[1]), float(valparam[2]), float(valparam[3]), float(pinit.get()))
        pop2 = generation_CI_complet_levins(int(npa.get()), float(pinit.get()), float(dpx.get()), float(dpy.get()), modele)
        simulation_levins_csv_complete(pop2, int(nt.get()), 'temp')
        visul_GUI('temp')
    b_l.grid(row = 10, column = 8, sticky = W)
    b_s.grid(row = 11, column = 8, sticky = W)
    b_r.grid(row = 12, column = 8, sticky = W)
    b_e.grid(row = 13, column = 8, sticky = W)
    bouton3.grid_forget()
    bouton2.grid_forget()
    exp.grid(row = 9, column = 3, sticky = W)
    export_champ.grid(row = 10, column = 3, sticky = W)
    export_bout.grid(row = 11, column = 3, sticky = W)

bouton2 = Button(frame_v, text = 'Lancer la simulation', command = simulate)


#Sauvegarde de la simulation
exp = Label(frame_v, text = "Exportation")
nom_f = StringVar()
nom_f.set('simul')
export_champ = Entry(frame_v, textvariable = nom_f)

def export():
    global nom_f
    directory = tkFileDialog.askdirectory()
    
    #Recuperation des donnees d'interet
    lecture_csv_tot = lire_csv_complet('temp')
    lecture_csv_p = lecture_csv_tot[0]
    abs = lecture_csv_tot[2]
    ord = lecture_csv_tot[3]
    
    #Creation du fichier
    file = open(nom_f.get()+'.csv', 'wb')
    writer = csv.writer(file, delimiter = ';')
    writer.writerow(abs)
    writer.writerow(ord)
    for row in lecture_csv_p:
        writer.writerow(row)
    file.close()
    
    #Deplacement du fichier
    shutil.move(nom_f.get()+'.csv', directory+os.sep+nom_f.get()+'.csv')  
    
    #Mise en forme de la fenetre
    exp.grid_forget()
    export_champ.grid_forget()
    export_bout.grid_forget()
    
export_bout = Button(frame_v, text = 'Exporter la simulation', command = export)

#Gestion de l'animation
animation = 0
iteration = 0

init_image1 = PIL.Image.open('blank.gif')
init_image2 = PIL.ImageTk.PhotoImage(init_image1)
label = Label(frame_v, image = init_image2)
label.image = init_image2
label.grid(row = 2, column = 3, rowspan = 6, columnspan = 6, sticky = W)

def animate():
    global animation, iteration
    if iteration < 10:
        image_new1 = PIL.Image.open('00'+str(iteration)+'.png')
        image_new2 = PIL.ImageTk.PhotoImage(image_new1)
        label.configure(image = image_new2)
        label.image = image_new2       
    elif 10 <= iteration < 100:
        image_new1 = PIL.Image.open('0'+str(iteration)+'.png')
        image_new2 = PIL.ImageTk.PhotoImage(image_new1)
        label.configure(image = image_new2)
        label.image = image_new2 
    else:
        image_new1 = PIL.Image.open(str(iteration)+'.png')
        image_new2 = PIL.ImageTk.PhotoImage(image_new1)
        label.configure(image = image_new2)
        label.image = image_new2 
    if animation > 0:
        iteration += 1
        if iteration < int(nt.get()):
            frame_v.after(1000, animate)
        else:
            animation = 0

def start_animate():
    global animation
    if animation == 0 or animation == 1:
        animation = 1
        animate()

def stop_animate():
    global animation
    animation = 0

def reinit():
    global iteration
    iteration = 0

def efface_animate():
    global animation, iteration
    animation = 0
    iteration = 0
    try :
        for compteur in range(int(nt.get())+1):
            if compteur < 10:
                os.remove('00'+str(compteur)+'.png')
            elif 10 <= compteur < 100:
                os.remove('0'+str(compteur)+'.png')
            else:
                os.remove(str(compteur)+'.png')
    except :
        pass
    b_l.grid_forget()
    b_s.grid_forget()
    b_r.grid_forget()
    b_e.grid_forget()
    label.configure(image = init_image2)
    label.image = init_image2
    bouton2.grid_forget()
    bouton3.grid(row = 8, column = 1)
    exp.grid_forget()
    export_champ.grid_forget()
    export_bout.grid_forget()

b_l = Button(frame_v, text = "Lancer l'animation", command = start_animate)
b_s = Button(frame_v, text = "Stopper l'animation", command = stop_animate)
b_r = Button(frame_v, text = "Reinitialiser l'animation", command = reinit)
b_e = Button(frame_v, text = "Effacer la simulation", command = efface_animate)

#Structure de base de la fenêtre de visualisation
Label(frame_v, text = "Type de modèle").grid(row = 1, column = 1, sticky = W)
Label(frame_v, text =  "Présence d'une banque de graines").grid(row = 4, column = 1, sticky = W)
Label(frame_v, text = "Simulation").grid(row = 9, column = 1, sticky = W)    

#Choix du type de modèle
val = [0, 1]
etiq = ['PRM', 'Levins']
varMod = IntVar()
varMod.set(0)
Radiobutton(frame_v, variable = varMod, text = etiq[0], value = val[0]).grid(row = 2, column = 1, sticky = W)
Radiobutton(frame_v, variable = varMod, text = etiq[1], value = val[1]).grid(row = 2, column = 2, sticky = W)

#Choix de la banque de graines
val2 = [0, 1, 2]
etiq2 = ['Non', 'A germination simple', 'A germination multiple']
varBg = IntVar()
varBg.set(0)
Radiobutton(frame_v, variable = varBg, text = etiq2[0], value = val2[0]).grid(row = 5, column = 1, columnspan = 2, sticky = W)
Radiobutton(frame_v, variable = varBg, text = etiq2[1], value = val2[1]).grid(row = 6, column = 1, columnspan = 2, sticky = W)
Radiobutton(frame_v, variable = varBg, text = etiq2[2], value = val2[2]).grid(row = 7, column = 1, columnspan = 2, sticky = W)

####################################
#Frame 2 : estimation de parametres#
####################################

filename = ''
vrais = StringVar()
vrais.set('0')
aic = StringVar()
aic.set('0')
liste_data = []

def ouvrir_fichier():
    global filename, liste_data
    filename = tkFileDialog.askopenfile(parent = root)
    liste_data = lire_colonne_csv(rs.lire_csv(filename))

def estimate():
    global liste_data
    a = varMod2.get()
    b = varBg2.get()
    est11.grid_forget()
    est12.grid_forget()
    est13.grid_forget()
    est21.grid_forget()
    est22.grid_forget()
    label_aic.configure(text = 'en cours de calcul')
    #Ouverture du fichier
    if a == 0:
        if b == 0:
            mod_sans_BG = ModPRM(random.uniform(0,1), random.uniform(0,1), 1, 1, random.uniform(0,1))
            resultat = etape_EM_PRM_SB(liste_data)
            AIC = resultat[2]
            p_col = resultat[0].c
            p_per = resultat[0].p
            p_init = resultat[0].pi
            label_aic.configure(text = str(AIC))
            est11.configure(text = 'Probabilité de colonisation :'+str(p_col))
            est12.configure(text = 'Probabilité de persistance :'+str(p_per))
            est21.configure(text = "Proportion initiale :"+str(p_init))
            est11.grid(row = 9, column = 5, sticky = W)
            est12.grid(row = 9, column = 6, sticky = W)
            est21.grid(row = 10, column = 5, sticky = W)
        elif b == 1:
            mod_avec_BGS = ModPRM(random.uniform(0,1), 1, random.uniform(0,1), random.uniform(0,1), random.uniform(0,1))
            for i in range(20):
                mod_avec_BGS = etape_EM_PRM_BGS(liste_data,mod_avec_BGS)[0]
            resultat = etape_EM_PRM_BGS(liste_data,mod_avec_BGS)
            AIC = resultat[2]
            p_col = resultat[0].c
            p_germ = resultat[0].g
            p_m = resultat[0].d
            p_init = resultat[0].pi
            label_aic.configure(text = str(AIC))
            est11.configure(text = 'Probabilité de colonisation :'+str(p_col))
            est12.configure(text = 'Probabilité de germination :'+str(p_germ))
            est21.configure(text = "Proportion initiale :"+str(p_init))
            est22.configure(text = 'Probabilité de mort des graines :'+str(p_m))
            est11.grid(row = 9, column = 5, sticky = W)
            est12.grid(row = 9, column = 6, sticky = W)
            est21.grid(row = 10, column = 5, sticky = W)
            est22.grid(row = 10, column = 6, sticky = W)
        else:
            mod_avec_BG = ModPRM(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), random.uniform(0,1))
            for i in range(20):
                mod_avec_BG = etape_EM_PRM(liste_data,mod_avec_BG)[0]
            resultat = etape_EM_PRM(liste_data,mod_avec_BG)
            AIC = resultat[2]
            p_col = resultat[0].c
            p_per = resultat[0].p
            p_germ = resultat[0].g
            p_m = resultat[0].d
            p_init = resultat[0].pi
            label_aic.configure(text = str(AIC))
            est11.configure(text = 'Probabilité de colonisation :'+str(p_col))
            est12.configure(text = 'Probabilité de germination :'+str(p_germ))
            est13.configure(text = "Proportion initiale :"+str(p_init))
            est21.configure(text = 'Probabilité de persistance :'+str(p_per))
            est22.configure(text = 'Probabilité de mort des graines :'+str(p_m))
            est11.grid(row = 9, column = 5, sticky = W)
            est12.grid(row = 9, column = 6, sticky = W)
            est13.grid(row = 9, column = 7, sticky = W)
            est21.grid(row = 10, column = 5, sticky = W)
            est22.grid(row = 10, column = 6, sticky = W)

def estimate_prm():
    #Etape 0 : mise en forme du cadre
    prm11.grid_forget()
    prm12.grid_forget()
    prm21.grid_forget()
    prm22.grid_forget()
    prm31.grid_forget()
    prm32.grid_forget()
    prm41.grid_forget()
    prm42.grid_forget()
    prm51.grid_forget()
    #Etape 1 : calcul des differents AIC
    #Ouverture du fichier
    global liste_data
    #A : modèle sans BG
    mod_sans_BG = ModPRM(random.uniform(0,1), random.uniform(0,1), 1, 1, random.uniform(0,1))
    resultat = etape_EM_PRM_SB(liste_data)
    AIC = resultat[2]
    p_col = resultat[0].c
    p_per = resultat[0].p
    p_germ = resultat[0].g
    p_m = resultat[0].d
    p_init = resultat[0].pi
    mod = 0
    #B : modèle avec BG simple
    for j in range(10):
        print(j)
        mod_avec_BGS = ModPRM(p_col, 1, 0.5, 0.5, p_init)
        for i in range(20):
            resultat = etape_EM_PRM_BGS(liste_data,mod_avec_BGS)
            mod_avec_BGS = resultat[0]
        if resultat[2] < AIC :
            AIC = resultat[2]
            p_col = resultat[0].c
            p_germ = resultat[0].g
            p_m = resultat[0].d
            p_init = resultat[0].pi
            mod = 1
    #C : modèle avec BG multiple
    for j in range(10):
        print(j)
        mod_avec_BG = ModPRM(p_col, p_per, 0.5, 0.5, p_init)
        for i in range(20):
            resultat = etape_EM_PRM(liste_data,mod_avec_BG)
            mod_avec_BG = resultat[0]
        if resultat[2] < AIC :
            AIC = resultat[2]
            p_col = resultat[0].c
            p_per = resultat[0].p
            p_germ = resultat[0].g
            p_m = resultat[0].d
            p_init = resultat[0].pi
            mod = 2
#Etape 2 : Affichage du resultat
    if mod == 0:
        prm12.configure(text = 'Modèle PRM sans banque de graines')
        prm11.grid(row = 13, column = 1)
        prm12.grid(row = 13, column = 2)
        prm22.configure(text = str(AIC))
        prm21.grid(row = 14, column = 1)
        prm22.grid(row = 14, column = 2)
        prm31.configure(text = 'Probabilité de colonisation :'+str(p_col))
        prm31.grid(row = 15, column = 1)
        prm32.configure(text = "Probabilité de persistance :"+str(p_per))
        prm32.grid(row = 15, column = 2)
        prm41.configure(text = 'Proportion initiale :'+str(p_init))
        prm41.grid(row = 16, column = 1)
    elif mod == 1:
        prm12.configure(text = 'Modèle PRM avec banque de graines à germination simple')
        prm11.grid(row = 13, column = 1)
        prm12.grid(row = 13, column = 2)
        prm22.configure(text = str(AIC))
        prm21.grid(row = 14, column = 1)
        prm22.grid(row = 14, column = 2)
        prm31.configure(text = 'Probabilité de colonisation :'+str(p_col))
        prm31.grid(row = 15, column = 1)
        prm32.configure(text = "Probabilité de germination :"+str(p_germ))
        prm32.grid(row = 15, column = 2)
        prm41.configure(text = 'Proportion initiale :'+str(p_init))
        prm41.grid(row = 16, column = 1)
        prm42.configure(text = "Probabilité de mort des graines :"+str(p_m))
        prm42.grid(row = 16, column = 2)
    else :
        prm12.configure(text = 'Modèle PRM avec banque de graines à germination multiple')
        prm11.grid(row = 13, column = 1)
        prm12.grid(row = 13, column = 2)
        prm22.configure(text = str(AIC))
        prm21.grid(row = 14, column = 1)
        prm22.grid(row = 14, column = 2)
        prm31.configure(text = 'Probabilité de colonisation :'+str(p_col))
        prm31.grid(row = 15, column = 1)
        prm32.configure(text = "Probabilité de germination :"+str(p_germ))
        prm32.grid(row = 15, column = 2)
        prm41.configure(text = "Probabilité de persistance :"+str(p_per))
        prm41.grid(row = 15, column = 2)
        prm42.configure(text = "Probabilité de mort des graines :"+str(p_m))
        prm42.grid(row = 16, column = 2)
        prm51.configure(text = 'Proportion initiale :'+str(p_init))
        prm51.grid(row = 16, column = 1)

def estimate_levins():
    ###TRUCS A FAIRE###
    print('En cours d ecriture !')

def estimate_total():
    ###TRUCS A FAIRE###
    print('En cours d ecriture !')

#Structure de base 
Button(frame_e, text = "Choisir un jeu de données", command = ouvrir_fichier).grid(row = 1, column = 1, sticky = W)
Label(frame_e, text = "Choix du modèle à tester").grid(row = 2, column = 1, sticky = W)
Label(frame_e, text = "Type de modèle").grid(row = 3, column = 1, sticky = W)
Label(frame_e, text =  "Présence d'une banque de graines").grid(row = 5, column = 1, sticky = W)

#Choix du type de modèle
val3 = [0, 1]
etiq3 = ['PRM', 'Levins (pas encore codé)']
varMod2 = IntVar()
varMod2.set(0)
Radiobutton(frame_e, variable = varMod2, text = etiq3[0], value = val3[0]).grid(row = 4, column = 1, sticky = W)
Radiobutton(frame_e, variable = varMod2, text = etiq3[1], value = val3[1]).grid(row = 4, column = 2, sticky = W)

#Choix de la banque de graines
val4 = [0, 1, 2]
etiq4 = ['Non', 'A germination simple', 'A germination multiple']
varBg2 = IntVar()
varBg2.set(0)
Radiobutton(frame_e, variable = varBg2, text = etiq4[0], value = val4[0]).grid(row = 6, column = 1, columnspan = 2, sticky = W)
Radiobutton(frame_e, variable = varBg2, text = etiq4[1], value = val4[1]).grid(row = 7, column = 1, columnspan = 2, sticky = W)
Radiobutton(frame_e, variable = varBg2, text = etiq4[2], value = val4[2]).grid(row = 8, column = 1, columnspan = 2, sticky = W)

#Estimation
Label(frame_e, text = 'AIC = ').grid(row = 9, column = 3)
label_aic = Label(frame_e, text = aic.get())
label_aic.grid(row = 9, column = 4)
est11 = Label(frame_e, text = '')
est12 = Label(frame_e, text = '')
est13 = Label(frame_e, text = '')
est21 = Label(frame_e, text = '')
est22 = Label(frame_e, text = '')

Button(frame_e, text = "Lancer l'estimation", command = estimate).grid(row = 9, column = 1, sticky = W)
Label(frame_e, text = 'Tests spécifiques').grid(row = 11, column = 1, sticky = W)
Button(frame_e, text = "Tester parmi tous les modèles PRM", command = estimate_prm).grid(row = 12, column = 1, columnspan = 2, sticky = W)
Button(frame_e, text = "Tester parmi tous les modèles de Levins (pas encore codé)", command = estimate_levins).grid(row = 18, column = 1, columnspan = 2, sticky = W)
Button(frame_e, text = "Tester parmi tous les modèles (pas encore codé)", command = estimate_total).grid(row = 24, column = 1, columnspan = 2, sticky = W)

frame_prm = Frame(frame_e)
frame_levins = Frame(frame_e)
frame_total = Frame(frame_e)
frame_prm.grid(row = 13, column = 1, rowspan = 5, columnspan = 2)
frame_levins.grid(row = 17, column = 1, rowspan = 5, columnspan = 2)
frame_total.grid(row = 21, column = 1, rowspan = 5, columnspan = 2)

prm11 = Label(frame_prm, text = 'Modèle retenu = ')
prm12 = Label(frame_prm, text = '(à calculer)')
prm21 = Label(frame_prm, text = 'AIC :')
prm22 = Label(frame_prm, text = '(à calculer)')
prm31 = Label(frame_prm, text = 'param1')
prm32 = Label(frame_prm, text = 'param2')
prm41 = Label(frame_prm, text = 'param3')
prm42 = Label(frame_prm, text = 'param4')
prm51 = Label(frame_prm, text = 'param5')

levins11 = Label(frame_levins, text = 'Modèle retenu = ')
levins12 = Label(frame_levins, text = '(à calculer)')
levins21 = Label(frame_levins, text = 'AIC :')
levins22 = Label(frame_levins, text = '(à calculer)')

total11 = Label(frame_total, text = 'Modèle retenu = ')
total12 = Label(frame_total, text = '(à calculer)')
total21 = Label(frame_total, text = 'AIC :')
total22 = Label(frame_total, text = '(à calculer)')

###################################
#Lancement de la fenêtre graphique#
###################################

root.mainloop()