from fltk import *
from random import *
from time import *
from classe_cercle import Cercle
from classe_coeur import Coeur
from classe_fleur import Fleur
from classe_diamant import Diamant
import json

#--Constantes------------------
clavier = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
LARG = 800 #Largeur de la fenêtre
HAUT = 600 #Hauteur de la fenêtre
TAILLE = 8 #Nombre de lignes et de colonnes de la grille
TAILLE_CEL = 50 #Taille d'une cellule en pixels
X_OFFSET = 100 # décalage gauche - min 30 pour afficher les références
Y_OFFSET = 50 # décalage droite - min 30
lst_couleur = ['rouge', 'jaune', 'vert', 'bleu']
lst_color_light = ['red', 'yellow', 'light green', 'light blue']
lst_color = ['red', 'yellow', 'green', 'blue']
vide = False  # valeur pour représenter  une case vide dans la grille
bonus = "B"  
malus = "M"

# définition des codes de couleur ansi pour afficher les couleurs dans le terminal
codes_couleur = {
    "rouge": "\033[91m●\033[0m",    # rouge
    "jaune": "\033[93m●\033[0m",    # jaune
    "vert": "\033[92m●\033[0m",     # vert
    "bleu": "\033[94m●\033[0m"      # bleu 
}

# associer les codes couleur aux noms de couleurs
rouge = codes_couleur["rouge"]
jaune = codes_couleur["jaune"]
vert = codes_couleur["vert"]
bleu = codes_couleur["bleu"]

lst_couleur_dico = [rouge, jaune, vert, bleu]

# dictionnaire des couleurs pour les joueurs en fonction du nombre de joueurs
couleurs_joueurs = {
    2: {1: rouge, 2: jaune},
    3: {1: rouge, 2: jaune, 3: vert},
    4: {1: rouge, 2: jaune, 3: vert, 4: bleu}
}

#------------------------------

# fonction pour initialiser la grille avec bonus et malus
def etat_cases(taille_grille, bonus, malus, nb_bonus, nb_malus):
    grille = [[vide for _ in range(taille_grille)] for _ in range(taille_grille)]
    milieu = taille_grille // 2
    grille[milieu - 1][milieu - 1], grille[milieu - 1][milieu] = rouge, jaune
    grille[milieu][milieu - 1], grille[milieu][milieu] = vert, bleu
    
    if nb_bonus!=0:
        # placer des bonus
        for _ in range(nb_bonus):
            while True:
                x, y = randint(0, taille_grille - 1), randint(0, taille_grille - 1)
                if grille[x][y] == vide:
                    grille[x][y] = bonus
                    break
    if nb_malus!=0:
        # placer des malus
        for _ in range(nb_malus):
            while True:
                x, y = randint(0, taille_grille - 1), randint(0, taille_grille - 1)
                if grille[x][y] == vide:
                    grille[x][y] = malus
                    break

    return grille



# Affiche et retourne les scores des joueurs à côté de leur couleur 
def affiche_scores(nb_joueurs, lst_symbole, lst_pseudo, lst_color_light, lst_couleur):
    
    lst_taille = []
    
    x, y = taille_texte("SCORES", 'Times', 20)
    rectangle(largeur_fenetre() - 190, 30, largeur_fenetre() - 170+x, 30+y, remplissage = 'light blue')
    texte(largeur_fenetre() - 180, 30, "SCORES", taille = 20, police='Times')
    
    for i in range(nb_joueurs):
        if lst_symbole[i] == '●':
            x, y = taille_texte(f'{lst_pseudo[i]} :',  'Times', 15)
            rectangle(largeur_fenetre() - 205, 100+i*80, largeur_fenetre() - 175+x, 100+i*80+y, remplissage = lst_color_light[i])
            texte(largeur_fenetre() - 200, 100+i*80, f'{lst_pseudo[i]} :', taille = 15, police = 'Times')
            image(largeur_fenetre() - 250, 110+i*80, f'images/{lst_couleur[i]}_cercle.PNG', largeur = 40, hauteur = 40)
            lst_taille.append(x)

        elif lst_symbole[i] == '♥':
            x, y = taille_texte(f'{lst_pseudo[i]} :',  'Times', 15)
            rectangle(largeur_fenetre() - 205, 100+i*80, largeur_fenetre() - 175+x, 100+i*80+y, remplissage = lst_color_light[i])
            texte(largeur_fenetre() - 200, 100+i*80, f'{lst_pseudo[i]} :', taille = 15, police = 'Times')
            image(largeur_fenetre() - 250, 110+i*80, f'images/{lst_couleur[i]}_coeur.PNG', largeur = 75, hauteur = 75)
            lst_taille.append(x)
            
        elif lst_symbole[i] == '✿':
            x, y = taille_texte(f'{lst_pseudo[i]} :',  'Times', 15)
            rectangle(largeur_fenetre() - 205, 100+i*80, largeur_fenetre() - 175+x, 100+i*80+y, remplissage = lst_color_light[i])
            texte(largeur_fenetre() - 200, 100+i*80, f'{lst_pseudo[i]} :', taille = 15, police = 'Times')
            image(largeur_fenetre() - 250, 110+i*80, f'images/{lst_couleur[i]}_fleur.PNG', largeur = 50, hauteur = 50)
            lst_taille.append(x)

        elif lst_symbole[i] == '⬖':
            x, y = taille_texte(f'{lst_pseudo[i]} :',  'Times', 15)
            rectangle(largeur_fenetre() - 205, 100+i*80, largeur_fenetre() - 175+x, 100+i*80+y, remplissage = lst_color_light[i])
            texte(largeur_fenetre() - 200, 100+i*80, f'{lst_pseudo[i]} :', taille = 15, police = 'Times')
            image(largeur_fenetre() - 250, 110+i*80, f'images/{lst_couleur[i]}_diamant.PNG', largeur = 40, hauteur = 40)
            lst_taille.append(x)
          
    return lst_taille
            
   
# Calcul les scores de chaque joueurs
def calcul_score(lst_scores, taille, etat_case, couleur_joueur, joueur_actuel):
    score = 0
    
    for i in range(taille):
        for j in range(taille):
            if etat_case[i][j] == couleur_joueur:
                score +=1
    lst_scores[joueur_actuel-1] = score
 
 
# Affiche l'écran d'accueil du jeu
def accueil(fenetre):
    
    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")

    rectangle(30, 100, 770, 250, remplissage="light blue")
    image(400, 180, "images/rolit.PNG", largeur = 252, hauteur = 110)
    
    x1, y1 = taille_texte("Jouer", "Blackadder ITC", 50)
    rectangle((750-x1)/2, 270, (830-x1)/2+x1, 270+y1, remplissage="light blue")
    texte((790-x1)/2, 270, "Jouer", taille=50, police="Blackadder ITC")
    
    x2, y2 = taille_texte("Reprendre", "Blackadder ITC", 50)
    rectangle((780-x2)/2, 400, (800-x2)/2+x2, 400+y2, remplissage="light blue")
    texte((790-x2)/2, 400, "Reprendre", taille=50, police="Blackadder ITC")

    with open("sauvegarde.json", "r", encoding="utf8") as fichier:
        contenu = fichier.read()
    
    while True:   
        ev = attend_ev()
        typeEv = type_ev(ev)
        
        if typeEv == "ClicGauche":
            x_clic, y_clic = abscisse(ev), ordonnee(ev)
            if (750-x1)/2 <= x_clic <= (830-x1)/2+x1 and 270 <= y_clic <= 270+y1 :
                rectangle((750-x1)/2, 270, (830-x1)/2+x1, 270+y1, remplissage="light green")
                texte((790-x1)/2, 270, "Jouer", taille=50, police="Blackadder ITC")
                accueil = 'jouer'
                break
            elif (780-x2)/2 <= x_clic <= (800-x2)/2+x2 and 400 <= y_clic <= 400+y2 and contenu!='' :
                rectangle((780-x2)/2, 400, (800-x2)/2+x2, 400+y2, remplissage="light green")
                texte((790-x2)/2, 400, "Reprendre", taille=50, police="Blackadder ITC")
                accueil = 'reprendre'
                break
            else:
                continue
            
    mise_a_jour()
    sleep(0.2)
    efface_tout()
   
    return accueil
    
 
 
 
 
 

# Demande le mode de jeu aux joueurs
def modes():
    
    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    x, y = taille_texte("Modes", "Blackadder ITC", 80)
    rectangle(30, 100, 770, 100+y, remplissage="light blue")
    texte((790-x)/2, 100, "Modes", taille=80, police="Blackadder ITC")
    
    x1, y1 = taille_texte("Classique", "Blackadder ITC", 50)
    rectangle((785-x1)/2, 270, (795-x1)/2+x1, 270+y1, remplissage="light blue")
    texte((790-x1)/2, 270, "Classique", taille=50, police="Blackadder ITC")
    
    x2, y2 = taille_texte("Capture obligatoire", "Blackadder ITC", 50)
    rectangle((785-x2)/2, 400, (795-x2)/2+x2, 400+y2, remplissage="light blue")
    texte((790-x2)/2, 400, "Capture obligatoire", taille=50, police="Blackadder ITC")
    
    while True:   
        ev = attend_ev()
        typeEv = type_ev(ev)
        
        if typeEv == "ClicGauche":
            x_clic, y_clic = abscisse(ev), ordonnee(ev)
            if (785-x1)/2 <= x_clic <= (795-x1)/2+x1 and 270 <= y_clic <= 270+y1 :
                rectangle((785-x1)/2, 270, (795-x1)/2+x1, 270+y1, remplissage="light green")
                texte((790-x1)/2, 270, "Classique", taille=50, police="Blackadder ITC")
                mode = 'classique'
                break
            elif (785-x2)/2 <= x_clic <= (795-x2)/2+x2 and 400 <= y_clic <= 400+y2 :
                rectangle((785-x2)/2, 400, (795-x2)/2+x2, 400+y2, remplissage="light green")
                texte((790-x2)/2, 400, "Capture obligatoire", taille=50, police="Blackadder ITC")
                mode = 'capture'
                break
            else:
                continue
            
    mise_a_jour()
    sleep(0.2)
    efface_tout()
   
    return mode
    
    
    




# Demande le nombre de joueurs
def demande_nb_joueurs():
    
    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    x, y = taille_texte("Combien de joueurs", "Blackadder ITC", 80)
    rectangle(30, 100, 770, 100+y, remplissage='light blue')
    
    longueur, hauteur = taille_texte('2', "Copperplate Gothic Bold", 50)
    
    cercle(175+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(375+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(575+longueur/2+5, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    
    mot = texte(50, 100, "Combien de joueurs", taille=80, police="Blackadder ITC")
    texte(175, 300, "2", taille=50, police="Copperplate Gothic Bold")
    texte(375, 300, "3", taille=50, police="Copperplate Gothic Bold")
    texte(575, 300, "4", taille=50, police="Copperplate Gothic Bold")
    
    while True:   
        ev = attend_ev()
        typeEv = type_ev(ev)
        
        if typeEv == "ClicGauche":
            x_clic, y_clic = abscisse(ev), ordonnee(ev)
            if 175-longueur <= x_clic <= 175+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(175+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(175, 300, "2", taille=50, police="Copperplate Gothic Bold")
                nb = 2
                break
            elif 375-longueur <= x_clic <= 375+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(375+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(375, 300, "3", taille=50, police="Copperplate Gothic Bold")
                nb = 3
                break
            elif 575-longueur <= x_clic <= 575+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(575+longueur/2+5, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(575, 300, "4", taille=50, police="Copperplate Gothic Bold")
                nb = 4
                break
            else:
                continue
            
    mise_a_jour()        
    sleep(0.2)   
    efface_tout()
        
    return nb


# Demande les pseudos
def pseudo(nb_joueurs):
    lst_pseudo=[]
    
    for i in range(nb_joueurs):
        lst_lettre=[]
        j = 200
        l=0
        pseudo = ''
        rectangle(10, 10, 790, 590, remplissage="light blue")
        rectangle(20, 20, 780, 580, remplissage="light cyan")
        
        
        x, y = taille_texte(f"Pseudo joueur {lst_couleur[i]}", "Blackadder ITC", 70)
        rectangle(30, 100, 770, 100+y, remplissage="light blue")
        
        texte(80, 100, f"Pseudo joueur {lst_couleur[i]}", taille=70, police="Blackadder ITC")
        rectangle(180, 280, 620, 340, remplissage="light blue")
        barre = ligne(j, 290, j, 330)
        
        while True:
            ev = attend_ev()
            tev = type_ev(ev)
            if tev == 'Touche':
                lettre = touche(ev)
                if lettre!='BackSpace' and j<590 and lettre in clavier:
                    efface(barre)
                    x, y = taille_texte(lettre, "Times", 35)
                    lst_lettre.append(x)
                    barre = ligne(j+x, 290, j+x, 330)
                    texte(j,285, lettre, taille=30, police="Times", tag = f"lettre{l}")
                    pseudo+=lettre
                    j+=lst_lettre[l]
                    l+=1
                    continue
                elif lettre == 'BackSpace':
                    if pseudo == '' and j<=200:
                        efface(barre)
                        j=200
                        l=0
                        barre = ligne(j, 290, j, 330)
                    elif pseudo != '' and j>210:
                        pseudo = pseudo[:-1]
                        efface(barre)
                        l-=1
                        j-=lst_lettre[l]
                        lst_lettre.pop(l)
                        barre = ligne(j, 290, j, 330)
                        efface(f"lettre{l}")
                    continue
                elif lettre == 'Return' and pseudo!='':
                    efface_tout()
                    j=200
                    l=0
                    lst_pseudo.append(pseudo)
                    efface_tout()
                    break
                else:
                    continue
            else:
                continue
    
    return lst_pseudo
        
    
# Demande aux joueurs de choisir leur symbole        
def demande_symbole(nb, lst_pseudo, lst_color):
    
    lst_symbole =[]
        
    for i in range(nb):
        rectangle(10, 10, 790, 590, remplissage="light blue")
        rectangle(20, 20, 780, 580, remplissage="light cyan")
        
        x, y = taille_texte(f"{lst_pseudo[i]} choisis ton symbole ", "Blackadder ITC", 50)
        rectangle(30, 100, 770, 110+y, remplissage='light blue')
        
        mot = texte((800-x)/2, 100, f"{lst_pseudo[i]} choisis ton symbole ", taille=50, police="Blackadder ITC")
        texte((800-x)/2, 100, f"{lst_pseudo[i]}", taille=50, police="Blackadder ITC", couleur = lst_color[i] )
        cercle = image(150, 320, 'images/cercle.PNG', largeur = 100, hauteur = 100)
        coeur = image(300, 320, 'images/coeur.PNG', largeur = 170, hauteur = 170)
        fleur = image(450, 320, 'images/fleur.PNG', largeur = 120, hauteur = 120)
        diamant = image(600, 320, 'images/diamant.PNG', largeur = 95, hauteur = 95)
        
        while True:
            ev = attend_ev()
            typeEv = type_ev(ev)
        
            if typeEv == "ClicGauche":
                x_clic, y_clic = abscisse(ev), ordonnee(ev)
                if 150-100/2 <= x_clic <= 150+100/2 and 320-100/2 <= y_clic <= 320+100/2 :
                    lst_symbole.append('●')
                    efface(cercle)
                    image(150, 310, 'images/cercle.PNG', largeur = 100, hauteur = 100)
                    break
                    
                elif 300-175/2 <= x_clic <= 300+175/2 and 320-175/2 <= y_clic <= 320+175/2 :
                    lst_symbole.append('♥')
                    efface(coeur)
                    image(300, 310, 'images/coeur.PNG', largeur = 170, hauteur = 170)
                    break
                    
                elif 450-125/2 <= x_clic <= 450+125/2 and 320-125/2 <= y_clic <= 320+125/2 :
                    lst_symbole.append('✿')
                    efface(fleur)
                    image(450, 310, 'images/fleur.PNG', largeur = 120, hauteur = 120)
                    break
                    
                elif 600-100/2 <= x_clic <= 600+100/2 and 320-100/2 <= y_clic <= 320+100/2 :
                    lst_symbole.append('⬖')
                    efface(diamant)
                    image(600, 310, 'images/diamant.PNG', largeur = 95, hauteur = 95)
                    break
                
                else:
                    continue
        
        mise_a_jour()
        sleep(0.2)
        efface_tout()
                
    if len(lst_symbole)<3:
        lst_symbole.extend([0,0])
    elif len(lst_symbole)<4:
        lst_symbole.append(0)
                
    return lst_symbole

# Demande le nombre de bonus aux joueurs
def n_bonus():
    
    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    x, y = taille_texte("Combien de bonus", "Blackadder ITC", 80)
    rectangle(30, 100, 770, 110+y, remplissage='light blue')
    
    longueur, hauteur = taille_texte('2', "Copperplate Gothic Bold", 50)
    
    cercle(125+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(275+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(425+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(580+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    
    mot = texte(80, 100, "Combien de bonus", taille=80, police="Blackadder ITC")
    chiffre_0 = texte(125, 300, "0", taille=50, police="Copperplate Gothic Bold")
    chiffre_1 = texte(275, 300, "1", taille=50, police="Copperplate Gothic Bold")
    chiffre_2 = texte(425, 300, "2", taille=50, police="Copperplate Gothic Bold")
    chiffre_3 = texte(580, 300, "3", taille=50, police="Copperplate Gothic Bold")
    
    while True:
        ev = attend_ev()
        typeEv = type_ev(ev)
        
        if typeEv == "ClicGauche":
            x_clic, y_clic = abscisse(ev), ordonnee(ev)
            if 125-longueur <= x_clic <= 125+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(125+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(125, 300, "0", taille=50, police="Copperplate Gothic Bold")
                bonus = 0
                break
            elif 275-longueur <= x_clic <= 275+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(275+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(275, 300, "1", taille=50, police="Copperplate Gothic Bold")
                bonus = 1
                break
            elif 425-longueur <= x_clic <= 425+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(425+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(425, 300, "2", taille=50, police="Copperplate Gothic Bold")
                bonus = 2
                break
            elif 580-longueur <= x_clic <= 580+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(580+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(580, 300, "3", taille=50, police="Copperplate Gothic Bold")
                bonus = 3
                break
        else:
            continue
    
    mise_a_jour()
    sleep(0.2)
    efface_tout()

    return bonus


# Demande le nombre de malus à mettre sur le plateau aux joueurs
def n_malus():
    
    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    x, y = taille_texte("Combien de malus", "Blackadder ITC", 80)
    rectangle(30, 100, 770, 110+y, remplissage='light blue')
    
    longueur, hauteur = taille_texte('2', "Copperplate Gothic Bold", 50)
    
    cercle(125+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(275+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(425+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(580+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    

    
    mot = texte(80, 100, "Combien de malus", taille=80, police="Blackadder ITC")
    chiffre_0 = texte(125, 300, "0", taille=50, police="Copperplate Gothic Bold")
    chiffre_1 = texte(275, 300, "1", taille=50, police="Copperplate Gothic Bold")
    chiffre_2 = texte(425, 300, "2", taille=50, police="Copperplate Gothic Bold")
    chiffre_3 = texte(580, 300, "3", taille=50, police="Copperplate Gothic Bold")
    
    while True:
        ev = attend_ev()
        typeEv = type_ev(ev)
        
        if typeEv == "ClicGauche":
            x_clic, y_clic = abscisse(ev), ordonnee(ev)
            if 125-longueur <= x_clic <= 125+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(125+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(125, 300, "0", taille=50, police="Copperplate Gothic Bold")
                malus = 0
                break
            elif 275-longueur <= x_clic <= 275+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(275+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(275, 300, "1", taille=50, police="Copperplate Gothic Bold")
                malus = 1
                break
            elif 425-longueur <= x_clic <= 425+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(425+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(425, 300, "2", taille=50, police="Copperplate Gothic Bold")
                malus = 2
                break
            elif 580-longueur <= x_clic <= 580+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(580+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(580, 300, "3", taille=50, police="Copperplate Gothic Bold")
                malus = 3
                break
        else:
            continue
    
    mise_a_jour()
    sleep(0.2)
    efface_tout()

    return malus

def demande_nb_manches():
    
    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    x, y = taille_texte("Combien de manches", "Blackadder ITC", 80)
    rectangle(30, 100, 770, 100+y, remplissage='light blue')
    
    longueur, hauteur = taille_texte('2', "Copperplate Gothic Bold", 50)
    
    cercle(175+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(375+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    cercle(580+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light blue')
    
    mot = texte(50, 100, "Combien de manches", taille=80, police="Blackadder ITC")
    texte(175, 300, "1", taille=50, police="Copperplate Gothic Bold")
    texte(375, 300, "2", taille=50, police="Copperplate Gothic Bold")
    texte(580, 300, "3", taille=50, police="Copperplate Gothic Bold")
    
    while True:   
        ev = attend_ev()
        typeEv = type_ev(ev)
        
        if typeEv == "ClicGauche":
            x_clic, y_clic = abscisse(ev), ordonnee(ev)
            if 175-longueur <= x_clic <= 175+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(175+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(175, 300, "1", taille=50, police="Copperplate Gothic Bold")
                nb = 1
                break
            elif 375-longueur <= x_clic <= 375+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(375+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(375, 300, "2", taille=50, police="Copperplate Gothic Bold")
                nb = 2
                break
            elif 580-longueur <= x_clic <= 580+longueur and 300-hauteur <= y_clic <= 300+hauteur :
                cercle(580+longueur/2, 300+hauteur/2, hauteur/1.5, remplissage = 'light green')
                texte(580, 300, "3", taille=50, police="Copperplate Gothic Bold")
                nb = 3
                break
            else:
                continue
            
    mise_a_jour()        
    sleep(0.2)   
    efface_tout()
        
    return nb


def lire_sauvegarde(fichier = 'sauvegarde.json'):
    lines = []
    with open(fichier, "r", encoding="utf8") as fichier:
        for line in fichier:
            lines.append(line)
        contenu = lines[0]
        sauvegarde = json.loads(contenu)
    return sauvegarde["mode"], sauvegarde["nb_joueurs"], sauvegarde["lst_pseudo"], sauvegarde["lst_symbole"], sauvegarde["joueur_actuel"], sauvegarde["coups"], sauvegarde["scores"], sauvegarde["aucun_mouvement_possible"], sauvegarde["sauter_tour"], sauvegarde["debut_partie"], sauvegarde["ETAT_CASE"], sauvegarde["score_joueur_max"], sauvegarde["scores_partie"], sauvegarde["nb_bonus"], sauvegarde["nb_malus"]



def menu_itel(fenetre, nb_joueurs, lst_pseudo, lst_symbole, scores, mode, coups, joueur_actuel, aucun_mouvement_possible, debut_partie, ETAT_CASE, sauter_tour, score_joueur_max, scores_partie, nb_bonus, nb_malus):
    
    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    l1, h1 = taille_texte('Quitter', "Blackadder ITC", 30)
    l2, h2 = taille_texte('Sauvegarder', "Blackadder ITC", 30)
    l3, h3 = taille_texte('Aide', "Blackadder ITC", 30)
    l4, h4 = taille_texte('Retour', "Blackadder ITC", 30)
    
    rectangle(l2, 140, (800-l2), 420, remplissage="light blue")
    
    texte((790-l1)/2,170, "Quitter", couleur="black", taille=30, police="Blackadder ITC")
    texte((790-l2)/2,250, "Sauvegarder", couleur="black", taille=30, police="Blackadder ITC")
    texte((790-l4)/2,320, "Retour", couleur="black", taille=30, police="Blackadder ITC")
    
    while True:
        ev = attend_ev()
        typeEv = type_ev(ev)
        x, y = abscisse(ev), ordonnee(ev)
        
        
        if (790-l1)/2-l1 <= x <= (790-l1)/2+l1 and 170-h1 <= y <= 170+h1:
            return 'quitter'
        
        elif (790-l2)/2-l2 <= x <= (790-l2)/2+l2 and 250-h2 <= y <= 250+h2:
            sauvegarde = {"mode": mode,
                        "nb_joueurs": nb_joueurs,
                        "lst_pseudo": lst_pseudo,
                        "lst_symbole": lst_symbole,
                        "joueur_actuel": joueur_actuel,
                        "coups": coups,
                        "scores": scores,
                        "aucun_mouvement_possible": aucun_mouvement_possible,
                        "sauter_tour": sauter_tour,
                        "debut_partie": debut_partie,
                        "ETAT_CASE": ETAT_CASE,
                        "score_joueur_max": score_joueur_max,
                        "scores_partie": scores_partie,
                        "nb_bonus": nb_bonus,
                        "nb_malus": nb_malus}
            
            sauv = json.dumps(sauvegarde)
            with open('sauvegarde.json', "w", encoding="utf8") as f:
                f.writelines(sauv)
            return 'sauvegarde'
        
        elif (790-l4)/2-l4 <= x <= (790-l4)/2+l4 and 320-h4 <= y <= 320+h4:
            return 'retour'
        
        else:
            continue


# Affiche le plateau à chaque tour
def affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, taille, taille_cel, x_offset, y_offset, grille, lst_coord, rouge, jaune, vert, bleu, bonus, malus):

    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    rectangle(x_offset-10, y_offset-10, x_offset+8*taille_cel+10, y_offset+8*taille_cel+10, remplissage="light blue")
    rectangle(x_offset, y_offset, x_offset+8*taille_cel, y_offset+8*taille_cel, couleur = 'light cyan', remplissage="light cyan")
    
    cercle(50, 50, 20, couleur = 'light blue', remplissage = 'light blue')
    image(50, 50, 'images/menu.PNG', largeur = 40, hauteur = 40)


    
    for i in range(taille + 1) :
        # Trace le plateau
        ligne(x_offset + i*taille_cel, y_offset, x_offset + i*taille_cel, y_offset + taille*taille_cel)
        ligne(x_offset, y_offset + i*taille_cel, x_offset + taille*taille_cel, y_offset + i*taille_cel)
    
    for k in range(nb_joueurs):
        for i in range(taille):
            for j in range(taille):
                if grille[i][j] == rouge:
                    joueur = pose_boule(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, lst_symbole, 'rouge', 0)
                    image(joueur.x, joueur.y, joueur.name, joueur.largeur, joueur.hauteur)
                elif grille[i][j] == jaune:
                    joueur = pose_boule(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, lst_symbole, 'jaune', 1)
                    image(joueur.x, joueur.y, joueur.name, joueur.largeur, joueur.hauteur)
                elif grille[i][j] == vert:
                    joueur = pose_boule(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, lst_symbole, 'vert', 2)
                    image(joueur.x, joueur.y, joueur.name, joueur.largeur, joueur.hauteur)
                elif grille[i][j] == bleu:
                    joueur = pose_boule(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, lst_symbole, 'bleu', 3)
                    image(joueur.x, joueur.y, joueur.name, joueur.largeur, joueur.hauteur)
                elif grille[i][j] == bonus:
                    image(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, 'images/etoile.PNG', largeur = 45, hauteur = 45)
                elif grille[i][j] == malus:
                    image(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, 'images/tete_de_mort.PNG', largeur = 65, hauteur = 65)
                
                    
                

#crée une liste contenant les coordonnées de cases du plateau sur la fenêtre
def coordonnees_case(taille, taille_cel, x_offset, y_offset):
    lst_coord=[]
    
    for i in range(taille):
        lst_coord.append([])  
        for j in range(taille):
            lst_coord[i].append([x_offset + j*taille_cel, y_offset + i*taille_cel])
            
    return lst_coord
            



# Affiche le plateau de jeu sur la fenêtre
def affiche_plateau(nb_cel, taille_cel, x_offset, y_offset, lst_coord, grille, lst_symbole, bonus, malus):

    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    rectangle(x_offset-10, y_offset-10, x_offset+8*taille_cel+10, y_offset+8*taille_cel+10, remplissage="light blue")
    rectangle(x_offset, y_offset, x_offset+8*taille_cel, y_offset+8*taille_cel, couleur = 'light cyan', remplissage="light cyan")
    
    cercle(50, 50, 20, couleur = 'light blue', remplissage = 'light blue')
    image(50, 50, 'images/menu.PNG', largeur = 40, hauteur = 40)

    
    for i in range(nb_cel + 1) :
        # Trace le plateau
        ligne(x_offset + i*taille_cel, y_offset, x_offset + i*taille_cel, y_offset + nb_cel*taille_cel)
        ligne(x_offset, y_offset + i*taille_cel, x_offset + nb_cel*taille_cel, y_offset + i*taille_cel)
        
        # Positionne les quatre boules de départ au milieu du plateau
        for i in range(len(grille)):
            for j in range(len(grille)):
                if grille[i][j] == rouge :
                    joueur = pose_boule(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, lst_symbole, 'rouge', 0)
                    image(joueur.x, joueur.y, joueur.name, joueur.largeur, joueur.hauteur)
                elif grille[i][j] == jaune :
                    joueur = pose_boule(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, lst_symbole, 'jaune', 1)
                    image(joueur.x, joueur.y, joueur.name, joueur.largeur, joueur.hauteur)
                elif grille[i][j] == vert :
                    joueur = pose_boule(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, lst_symbole, 'vert', 2)
                    image(joueur.x, joueur.y, joueur.name, joueur.largeur, joueur.hauteur)
                elif grille[i][j] == bleu :
                    joueur = pose_boule(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, lst_symbole, 'bleu', 3)
                    image(joueur.x, joueur.y, joueur.name, joueur.largeur, joueur.hauteur)
                elif grille[i][j] == bonus:
                    image(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, 'images/etoile.PNG', largeur = 45, hauteur = 45)
                elif grille[i][j] == malus:
                    image(lst_coord[i][j][0]+ taille_cel/2, lst_coord[i][j][1] + taille_cel/2, 'images/tete_de_mort.PNG', largeur = 65, hauteur = 65)


# Pose une boule dans le plateau
def pose_boule(x, y, lst_symbole, couleur, i):
    
    if lst_symbole[i] == '●':
        joueur_i = Cercle(x, y, f'images/{couleur}_cercle.PNG', largeur = 40, hauteur = 40)
    elif lst_symbole[i] == '♥':
        joueur_i = Coeur(x, y, f'images/{couleur}_coeur.PNG', largeur = 70, hauteur = 70)
    elif lst_symbole[i] == '✿':
        joueur_i = Fleur(x, y, f'images/{couleur}_fleur.PNG', largeur = 45, hauteur = 45)
    elif lst_symbole[i] == '⬖':
        joueur_i = Diamant(x, y, f'images/{couleur}_diamant.PNG', largeur = 40, hauteur = 40)
    else:
        joueur_i = Cercle(x, y, f'images/{couleur}_cercle.PNG', largeur = 40, hauteur = 40)
        
    return joueur_i



# Afiiche le pseudo du grand gagnant
def gagnant(index_gagnant, lst_color, lst_pseudo):
    
    rectangle(10, 10, 790, 590, remplissage="light blue")
    rectangle(20, 20, 780, 580, remplissage="light cyan")
    
    x, y = taille_texte(" Le grand gagnant est", "Blackadder ITC", 80)
    rectangle(30, 100, 770, 100+y, remplissage="light blue")
    texte((790-x)/2, 100, "Grand Gagnant", taille=80, police="Blackadder ITC")
    
    x1, y1 = taille_texte(f"{lst_pseudo[index_gagnant]}", "Blackadder ITC", 50)
    rectangle(50, 270, 750, 270+y1, remplissage="light blue")
    texte((790-x1)/2, 270, f"{lst_pseudo[index_gagnant]}", taille=50, police="Blackadder ITC", couleur = lst_color[index_gagnant])
    
    

# Vérifie si le joueur clique dans une case du plateau
def verif_clic_in_cel(x_clic, y_clic, x_offset, y_offset, taille, taille_cel, lst_coord):
    
    for i in range(taille):
        for coord in lst_coord[i]:
            if (coord[0]<= x_clic <= coord[0]+taille_cel) and (coord[1] <= y_clic <= coord[1]+taille_cel):
                x, y = coord[0], coord[1]
                return x, y
    return False

    
    

# fonction qui vérifie si une capture est possible dans une direction donnée
def peut_capturer(grille, ligne, colonne, dx, dy, joueur, taille_grille):
    adversaire_trouve = False  # indique si on a trouvé une pièce adverse
    x, y = ligne + dx, colonne + dy  # avance dans la direction donnée
    while 0 <= x < taille_grille and 0 <= y < taille_grille:
        if grille[x][y] in [vide, bonus, malus]:
            return False  # arrêt si on atteint une case vide
        if grille[x][y] == joueur:
            return adversaire_trouve  # capture valide seulement si un adversaire a été trouvé
        adversaire_trouve = True  # marque qu'un adversaire a été trouvé dans la direction
        x += dx
        y += dy
    return False  # aucune capture possible

# fonction pour retourner les pions capturés dans une direction donnée
def retourner_dans_direction(grille, ligne, colonne, dx, dy, joueur):
    x, y = ligne + dx, colonne + dy  # commence à avancer dans la direction donnée
    while grille[x][y] != joueur:
        grille[x][y] = joueur  # change la couleur de la pièce en couleur du joueur
        x += dx
        y += dy

# fonction pour capturer les pièces adverses autour d'une position donnée
def capturer_pieces(grille, ligne, colonne, joueur, taille_grille):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        if peut_capturer(grille, ligne, colonne, dx, dy, joueur, taille_grille):
            retourner_dans_direction(grille, ligne, colonne, dx, dy, joueur)
            




# fonction pour vérifier si un mouvement est valide (permettant une capture)
def mouvement_valide(grille, ligne, colonne, joueur, taille_grille):
    if grille[ligne][colonne] != vide and grille[ligne][colonne] != bonus and grille[ligne][colonne] != malus:
        return False  # la case est occupée
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        if peut_capturer(grille, ligne, colonne, dx, dy, joueur, taille_grille):
            return True  # si une capture est possible dans une direction
    return False  # aucun mouvement valide trouvé


# fonction pour vérifier si une case est adjacente à une autre bille
def case_adjacente(grille, ligne, colonne):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    taille_grille = len(grille)
    for dx, dy in directions:
        x, y = ligne + dx, colonne + dy
        if 0 <= x < taille_grille and 0 <= y < taille_grille and grille[x][y] not in [vide, bonus, malus]:
            return True
    return False


# fonction pour appliquer un malus
def appliquer_malus(grille, joueur, couleur_joueur):
    effet = choice(["perdre_pion", "sauter_tour"])
    if effet == "perdre_pion":
        positions = [(x, y) for x, ligne in enumerate(grille) for y, val in enumerate(ligne) if val == couleur_joueur]        
        if positions:
            x, y = choice(positions)
            grille[x][y] = vide
        
    return effet


# fonction pour passer au joueur suivant
def changer_joueur(joueur, nb_joueurs):
    return (joueur % nb_joueurs) + 1


# permet de faire la sérialisation pour pouvoir utiliser json
def fonction_m_b(obj): 
    if callable(obj):
        return {"type": "fonction", "nom": obj.__name__}  # Sérialisation de la fonction par son nom 
                   
def afficher_scores_cote(nb_joueurs, lst_taille, scores):
    score_rouge = 0
    score_jaune = 0
    score_vert = 0
    score_bleu = 0
    liste_score_couleur = [score_rouge, score_jaune, score_vert, score_bleu]
    for i in range(nb_joueurs):
        liste_score_couleur[i] = texte((largeur_fenetre() - 200)+lst_taille[i]+5, 102 + 80 * i, scores[i], taille = 12, police="Times")

# Lance le mode de jeu classique
def jeu(fenetre, sauvegarde, capture_obligatoire):   
    
    partie_deja_fini = False
    partie_quitte = False

    if capture_obligatoire:
        mode = "capture"
    if capture_obligatoire == False:
        mode = "classique"

    if sauvegarde == True:
        mode, nb_joueurs, lst_pseudo, lst_symbole, joueur_actuel, coups, scores, aucun_mouvement_possible, sauter_tour, debut_partie, ETAT_CASE, score_joueur_max, scores_partie, nb_bonus, nb_malus = lire_sauvegarde('sauvegarde.json')
        if max(scores_partie) < score_joueur_max:
            partie_quitte = manche(nb_joueurs, lst_pseudo, lst_symbole, 0, 0, score_joueur_max, scores_partie, joueur_actuel, coups, False, scores, sauter_tour, aucun_mouvement_possible, ETAT_CASE, capture_obligatoire)
        else:
            partie_deja_fini = True
    
    if sauvegarde == False:
        nb_joueurs = demande_nb_joueurs() # Demande le nombre de joueurs (2, 3, 4)
        
        lst_pseudo = pseudo(nb_joueurs) # Demande les pseudos
        
        lst_symbole = demande_symbole(nb_joueurs, lst_pseudo, lst_color) # Demande à chaque joueur de choisir un symbole (cercle, coeur, fleur, diamant)
        
        nb_bonus = n_bonus() # nombre de bonus (0, 2, 3, 4)
        nb_malus = n_malus() # nommbre de malus (0, 2, 3, 4)
    
        score_joueur_max = demande_nb_manches()

        scores_partie = [0, 0, 0, 0]

    if partie_deja_fini == False:
        while partie_quitte == False and max(scores_partie) < score_joueur_max:
            partie_quitte = manche(nb_joueurs, lst_pseudo, lst_symbole, nb_bonus, nb_malus, score_joueur_max, scores_partie, debut_partie=True, scores = [0, 0, 0, 0], capture_obligatoire= capture_obligatoire)
        
        if partie_quitte == False:
            index_gagnant = scores_partie.index(max(scores_partie))

            gagnant(index_gagnant, lst_color, lst_pseudo)
            
            
            
            


def manche(nb_joueurs, lst_pseudo, lst_symbole, nb_bonus = 0, nb_malus = 0, score_joueur_max = 3, scores_partie = [0, 0, 0, 0], joueur_actuel = 1, coups = 0, debut_partie = True, scores = [0, 0, 0, 0], sauter_tour = 0, aucun_mouvement_possible = False, ETAT_CASE = None, capture_obligatoire = False):

    if debut_partie:
        ETAT_CASE = etat_cases(TAILLE, bonus, malus, nb_bonus, nb_malus) #initialise l'état de chaque case du plateau (vide ou non vide)
    COORD = coordonnees_case(TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET) # initialise les coordonnées des bords ouest et nord de chaque case
    max_coups = TAILLE**2  # nombre maximum de coups possibles (nombre de cases)
    tours_joueurs = [0] + [1] * nb_joueurs  # liste pour suivre les tours de chaque joueur
    
    
    
    
    affiche_plateau(TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, COORD, ETAT_CASE, lst_symbole, bonus, malus) # affiche le plateau à chaque tour


    while sum(scores) < max_coups:
        
        # Vérifie si le tour du joueur est à sauter ou non
        if sauter_tour == joueur_actuel:
            joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
            sauter_tour = 0
        
        
        # Affiche les symboles et pseudos à côté des scores
        lst_taille = affiche_scores(nb_joueurs, lst_symbole, lst_pseudo, lst_color_light, lst_couleur)

        # Affiche les scores en temps réels
        afficher_scores_cote(nb_joueurs, lst_taille, scores)

        
        couleur_joueur = couleurs_joueurs[nb_joueurs][joueur_actuel]
        
        # Indique le tour de chaque joueur
        x, y = taille_texte("C'est le tour de", 'Times', 20)
        rectangle(X_OFFSET-10, Y_OFFSET+TAILLE_CEL*8+20, X_OFFSET+TAILLE_CEL*8+10, Y_OFFSET+TAILLE_CEL*8+y+25, remplissage = 'light blue')
        tour_de_joueur = texte(100, 475, "C'est le tour de", taille=20, police='Times')
        pseudos = texte(110+x, 475, f"{lst_pseudo[joueur_actuel-1]}", taille=20, police='Times', couleur = lst_color[joueur_actuel-1])
        
        # Vérifie s'il y a un mouvement de capture disponible pour le joueur actuel
        capture_disponible = any(
            mouvement_valide(ETAT_CASE, ligne, colonne, couleur_joueur, TAILLE)
            for ligne in range(TAILLE)
            for colonne in range(TAILLE)
            if ETAT_CASE[ligne][colonne] == vide or ETAT_CASE[ligne][colonne] == bonus or ETAT_CASE[ligne][colonne] == malus
        )

        # Attend que le joueur clique sur une case
        ev = attend_ev()
        typeEv = type_ev(ev)
        
        if typeEv == "ClicGauche":
            x_clic, y_clic = abscisse(ev), ordonnee(ev)
            if verif_clic_in_cel(x_clic, y_clic, X_OFFSET, Y_OFFSET, TAILLE, TAILLE_CEL, COORD) == False and x_clic>100 and y_clic>100 :
                # Affiche un message d'erreur si le joueur ne clique pas dans une case
                texte(X_OFFSET*2, Y_OFFSET/2, "Cliquez dans une case", taille=10, couleur='red', police='Courier')
                mise_a_jour()
                sleep(0.5)
                    
                # Réinitialise l'état du jeu
                efface_tout()
                    
                # Réaffiche le plateau
                affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                    
                continue
            
            elif 0 <= x_clic <= 100 and 0 <= y_clic <= 100:
                efface_tout()
                if menu_itel(fenetre, nb_joueurs, lst_pseudo, lst_symbole, scores, mode, coups, joueur_actuel, aucun_mouvement_possible, debut_partie, ETAT_CASE, sauter_tour, score_joueur_max, scores_partie, nb_bonus, nb_malus) in ['retour', 'sauvegarde']:
                    # Réinitialise l'état du jeu
                    efface_tout()
                    
                    # Réaffiche le plateau
                    affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                    
                    continue
                elif menu_itel(fenetre, nb_joueurs, lst_pseudo, lst_symbole, scores, mode, coups, joueur_actuel, aucun_mouvement_possible, debut_partie, ETAT_CASE, sauter_tour, score_joueur_max, scores_partie, nb_bonus, nb_malus) == 'quitter':
                    ferme_fenetre()
                    return True

            
        
            else:
                x, y = verif_clic_in_cel(x_clic, y_clic, X_OFFSET, Y_OFFSET, TAILLE, TAILLE_CEL, COORD)
                for i in range(TAILLE):
                    for coord in COORD[i]:
                        if [x, y] == coord :
                            ligne = i
                            colonne = COORD[i].index([x, y])
                            
        else:
            # Réinitialise l'état du jeu
            efface_tout()
            
            # Réaffiche le plateau
            affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
            
            continue
                

        # Vérifier si le joueur a cliqué dans une case du plateau ou sur le bouton menu
        if 0 <= ligne < TAILLE and 0 <= colonne < TAILLE:
            # Vérifie si la case est déjà occupée
            if ETAT_CASE[ligne][colonne] not in [vide, bonus, malus]  :
                # Affiche un message d'erreur si le joueur ne clique pas dans une case vide
                texte(X_OFFSET*2, Y_OFFSET/2, "Cliquez dans une case vide !", taille=10, couleur='red', police='Courier')
                mise_a_jour()
                sleep(1)
                    
                # Réinitialise l'état du jeu
                efface_tout()
                    
                # Réaffiche le plateau
                affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                    
                continue                
            
            else:
                if capture_obligatoire == True:
                    # Si une capture est possible, forcer le joueur à capturer
                    if capture_disponible:
                        if mouvement_valide(ETAT_CASE, ligne, colonne, couleur_joueur, TAILLE) and case_adjacente(ETAT_CASE, ligne, colonne) == True:
                            
                            # appliquer les effets de bonus/malus
                            effet = None
                            if ETAT_CASE[ligne][colonne] == bonus:
                                texte(X_OFFSET+TAILLE_CEL, Y_OFFSET/2, "Bonus activé ! Vous pouvez rejouer !", taille=10, couleur='green', police='Courier')
                                mise_a_jour()
                                sleep(0.7)
                                
                                ETAT_CASE[ligne][colonne] = couleur_joueur
                                capturer_pieces(ETAT_CASE, ligne, colonne, couleur_joueur, TAILLE)  # effectuer la capture
                                
                                # Réinitialise l'état du jeu
                                efface_tout() 
                                # Réaffiche le plateau
                                affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)                                                             
                                                
                                coups += 1
                                
                                
                                
                            elif ETAT_CASE[ligne][colonne] == malus:
                                effet = appliquer_malus(ETAT_CASE, joueur_actuel, couleurs_joueurs[nb_joueurs][joueur_actuel])
                                
                                if effet == 'perdre_pion':
                                    ETAT_CASE[ligne][colonne] = couleur_joueur

                                    texte(X_OFFSET+TAILLE_CEL, Y_OFFSET/2, "Malus activé ! Vous perdez un pion !", taille=10, couleur='red', police='Courier')
                                    mise_a_jour()
                                    sleep(0.7)
                                    
                                    # Réinitialise l'état du jeu
                                    efface_tout() 
                                    # Réaffiche le plateau
                                    affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)                                                             
                                                                    
                                    coups += 1
                                    joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                                    
                                elif effet == 'sauter_tour':
                                    sauter_tour = joueur_actuel
                                    ETAT_CASE[ligne][colonne] = couleur_joueur
        
                                    texte(X_OFFSET, Y_OFFSET/2, "Malus activé ! Vous sautez votre prochain tour!", taille=10, couleur='red', police='Courier')
                                    mise_a_jour()
                                    sleep(0.7)
                                    
                                    # Réinitialise l'état du jeu
                                    efface_tout() 
                                    # Réaffiche le plateau
                                    affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)                                                             
                                    
                                    
                                    coups += 1
                                    joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                                    
                            
                            else: 
                                ETAT_CASE[ligne][colonne] = couleur_joueur
                                capturer_pieces(ETAT_CASE, ligne, colonne, couleur_joueur, TAILLE)  # effectuer la capture
                                
                                # Réinitialise l'état du jeu
                                efface_tout()
                                    
                                # Réaffiche le plateau
                                affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                                    

                                coups += 1
                                joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                            
                            for i in range(nb_joueurs):
                                calcul_score(scores, TAILLE, ETAT_CASE, lst_couleur_dico[i], i+1)
                
                            
                        else:
                            # Affiche un message d'erreur si le joueur ne clique pas dans une case
                            texte(X_OFFSET*2, Y_OFFSET/2, "Vous devez capturez !", taille=10, couleur='red', police='Courier')
                            mise_a_jour()
                            sleep(0.5)
                                
                            # Réinitialise l'état du jeu
                            efface_tout()
                                
                            # Réaffiche le plateau
                            affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                                
                            continue  # demander à rejouer
                    else:
                        # Si aucune capture n'est possible, vérifier si le placement est adjacent à une autre bille
                        voisin_present = any(
                            0 <= ligne + dx < TAILLE and 0 <= colonne + dy < TAILLE and ETAT_CASE[ligne + dx][colonne + dy] not in [vide, bonus, malus]
                            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                        )
                        
                        if voisin_present and ETAT_CASE[ligne][colonne] not in [bonus, malus]:
                            ETAT_CASE[ligne][colonne] = couleur_joueur  # placer la bille
                            coups += 1
                            
                            # Réinitialise l'état du jeu
                            efface_tout()
                                
                            # Réaffiche le plateau
                            affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                            
                            for i in range(nb_joueurs):
                                calcul_score(scores, TAILLE, ETAT_CASE, lst_couleur_dico[i], i+1)
                            
                            
                            joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                            
                        elif ETAT_CASE[ligne][colonne] == bonus:
                            texte(X_OFFSET*2, Y_OFFSET/2, "Vous ne pouvez pas avoir de bonus !", taille=10, couleur='red', police='Courier')
                            mise_a_jour()
                            sleep(0.5)
                            
                            # Réinitialise l'état du jeu
                            efface_tout()
                                
                            # Réaffiche le plateau
                            affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                        
                            continue 
                            
                        else:
                            texte(X_OFFSET*2, Y_OFFSET/2, "Cliquez à côté d'une autre boule !", taille=10, couleur='red', police='Courier')
                            mise_a_jour()
                            sleep(0.5)
                                
                            # Réinitialise l'état du jeu
                            efface_tout()
                                
                            # Réaffiche le plateau
                            affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                        
                            continue 

                elif capture_obligatoire == False:   
                    if case_adjacente(ETAT_CASE, ligne, colonne) == True:
                        if mouvement_valide(ETAT_CASE, ligne, colonne, couleur_joueur, TAILLE):
                            
                            # appliquer les effets de bonus/malus
                            effet = None
                            if ETAT_CASE[ligne][colonne] == bonus:
                                texte(X_OFFSET+TAILLE_CEL, Y_OFFSET/2, "Bonus activé ! Vous pouvez rejouer !", taille=10, couleur='green', police='Courier')
                                mise_a_jour()
                                sleep(0.7)
                                
                                ETAT_CASE[ligne][colonne] = couleur_joueur
                                capturer_pieces(ETAT_CASE, ligne, colonne, couleur_joueur, TAILLE)  # effectuer la capture
                                
                                # Réinitialise l'état du jeu
                                efface_tout() 
                                # Réaffiche le plateau
                                affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)                                                             
                                                
                                coups += 1
                                
                                
                                
                            elif ETAT_CASE[ligne][colonne] == malus:
                                effet = appliquer_malus(ETAT_CASE, joueur_actuel, couleurs_joueurs[nb_joueurs][joueur_actuel])
                                
                                if effet == 'perdre_pion':
                                    ETAT_CASE[ligne][colonne] = couleur_joueur                               
            
                                    texte(X_OFFSET+TAILLE_CEL, Y_OFFSET/2, "Malus activé ! Vous perdez un pion !", taille=10, couleur='red', police='Courier')
                                    mise_a_jour()
                                    sleep(0.7)
                                    
                                    # Réinitialise l'état du jeu
                                    efface_tout() 
                                    # Réaffiche le plateau
                                    affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)                                                             
                                                                    
                                    coups += 1
                                    joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                                    
                                elif effet == 'sauter_tour':
                                    sauter_tour = joueur_actuel
                                    ETAT_CASE[ligne][colonne] = couleur_joueur

                                    texte(X_OFFSET, Y_OFFSET/2, "Malus activé ! Vous sautez votre prochain tour!", taille=10, couleur='red', police='Courier')
                                    mise_a_jour()
                                    sleep(0.7)
                                    
                                    # Réinitialise l'état du jeu
                                    efface_tout() 
                                    # Réaffiche le plateau
                                    affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                                    
                                    coups += 1
                                    joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)                        
                            
                            
                            elif ETAT_CASE[ligne][colonne] == vide :
                                ETAT_CASE[ligne][colonne] = couleur_joueur  # placer la bille
                                capturer_pieces(ETAT_CASE, ligne, colonne, couleur_joueur, TAILLE)  # effectuer la capture
                                
                                # Réinitialise l'état du jeu
                                efface_tout()
                                    
                                # Réaffiche le plateau
                                affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)

                                
                                coups += 1
                                joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                                
                        else:
                            # appliquer les effets de bonus/malus
                            effet = None
                            if ETAT_CASE[ligne][colonne] == bonus:
                                texte(X_OFFSET+TAILLE_CEL, Y_OFFSET/2, "Bonus activé ! Vous pouvez rejouer !", taille=10, couleur='green', police='Courier')
                                mise_a_jour()
                                sleep(0.7)
                                
                                ETAT_CASE[ligne][colonne] = couleur_joueur
                                capturer_pieces(ETAT_CASE, ligne, colonne, couleur_joueur, TAILLE)  # effectuer la capture
                                
                                # Réinitialise l'état du jeu
                                efface_tout() 
                                # Réaffiche le plateau
                                affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)                                                             
                                                
                                coups += 1
                                
                                
                                
                            elif ETAT_CASE[ligne][colonne] == malus:
                                effet = appliquer_malus(ETAT_CASE, joueur_actuel, couleurs_joueurs[nb_joueurs][joueur_actuel])
                                
                                if effet == 'perdre_pion':
                                    ETAT_CASE[ligne][colonne] = couleur_joueur                               
            
                                    texte(X_OFFSET+TAILLE_CEL, Y_OFFSET/2, "Malus activé ! Vous perdez un pion !", taille=10, couleur='red', police='Courier')
                                    mise_a_jour()
                                    sleep(0.7)
                                    
                                    # Réinitialise l'état du jeu
                                    efface_tout() 
                                    # Réaffiche le plateau
                                    affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)                                                             
                                                                    
                                    coups += 1
                                    joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                                    
                                elif effet == 'sauter_tour':
                                    sauter_tour = joueur_actuel
                                    ETAT_CASE[ligne][colonne] = couleur_joueur

                                    texte(X_OFFSET, Y_OFFSET/2, "Malus activé ! Vous sautez votre prochain tour!", taille=10, couleur='red', police='Courier')
                                    mise_a_jour()
                                    sleep(0.7)
                                    
                                    # Réinitialise l'état du jeu
                                    efface_tout() 
                                    # Réaffiche le plateau
                                    affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                                    
                                    coups += 1
                                    joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                                    
                            else:       
                                ETAT_CASE[ligne][colonne] = couleur_joueur  # placer la bille

                                # Réinitialise l'état du jeu
                                efface_tout()
                                    
                                # Réaffiche le plateau
                                affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)


                                coups += 1
                                joueur_actuel = changer_joueur(joueur_actuel, nb_joueurs)
                        
                        
                        for i in range(nb_joueurs):
                                calcul_score(scores, TAILLE, ETAT_CASE, lst_couleur_dico[i], i+1)
                                
                        continue
    
                    else:
                        texte(X_OFFSET*2, Y_OFFSET/2, "Cliquez à côté d'une autre boule !", taille=10, couleur='red', police='Courier')
                        mise_a_jour()
                        sleep(0.5)
                            
                        # Réinitialise l'état du jeu
                        efface_tout()
                            
                        # Réaffiche le plateau
                        affiche_plateau_tour(nb_joueurs, lst_couleur, lst_symbole, TAILLE, TAILLE_CEL, X_OFFSET, Y_OFFSET, ETAT_CASE, COORD, rouge, jaune, vert, bleu, bonus, malus)
                    
                        continue 

        else: # Affiche un message d'erreur si le mouvement est invalide
            texte(X_OFFSET*2, Y_OFFSET/2, "Mouvement invalide !", taille=10, couleur='red', police='Courier')
            sleep(0.5)
            
    # Affiche les symboles et pseudos à côté des scores
    lst_taille = affiche_scores(nb_joueurs, lst_symbole, lst_pseudo, lst_color_light, lst_couleur)

    # Affiche les scores en temps réels
    afficher_scores_cote(nb_joueurs, lst_taille, scores)

    if sum(scores) >= max_coups:

        score_gagnant = max(scores)
        index_gagnant = scores.index(score_gagnant)
        
        # Affiche le gagnant
        x, y = taille_texte("Le gagnant de la manche est ", 'Times', 20)
        rectangle(X_OFFSET-10, Y_OFFSET+TAILLE_CEL*8+20, X_OFFSET+TAILLE_CEL*8+10, Y_OFFSET+TAILLE_CEL*8+y+25, remplissage = 'light blue')
        texte(100, 475, "Le gagnant de la manche est ", taille=20, police='Times')
        pseudos = texte(110+x, 475, f"{lst_pseudo[index_gagnant]}", taille=20, police='Times', couleur = lst_color[index_gagnant])
        
        mise_a_jour()
        sleep(2)
        
        efface_tout()
        
        scores_partie[index_gagnant] += 1

        return False



# Programme principal
fenetre = cree_fenetre(LARG, HAUT) # crée une fenêtre de largeur 800 et de longueur 600

choix_accueil = accueil(fenetre)

if choix_accueil == 'jouer':
 
    mode = modes()
    if mode == 'classique':
        jeu(fenetre, False, False)
    
    elif mode == 'capture':
        jeu(fenetre, False, True)
        
elif choix_accueil == 'reprendre' :

    mode, nb_joueurs, lst_pseudo, lst_symbole, joueur_actuel, coups, scores, aucun_mouvement_possible, sauter_tour, debut_partie, ETAT_CASE, score_joueur_max, scores_partie, nb_bonus, nb_malus = lire_sauvegarde('sauvegarde.json')
    if mode == "classique":
        jeu(fenetre, True, False)
    
    elif mode == "capture":
        jeu(fenetre, True, True)
        
    




