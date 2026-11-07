from fltk import *

# Classe représentant les coeurs sans les afficher immédiatement
class Coeur:
    def __init__(self, x, y, name, largeur, hauteur):
        self.x = x
        self.y = y
        self.name = name
        self.largeur = largeur
        self.hauteur = hauteur
        
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_name(self):
        return self.name
    
    def get_largeur(self):
        return self.largeur
    
    def get_hauteur(self):
        return self.hauteur
