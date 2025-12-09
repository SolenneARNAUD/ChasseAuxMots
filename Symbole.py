from ctypes.wintypes import COLORREF
import string


class Symbole(object):
    """
    Cette classe a pour objectif d'encoder les lettres/symboles
    présent dans les mots. Les lettres/symboles doivent être 
    indépendant car elles sont tapé une par une
    """
    
    def __init__(self, couleur, symbole):
        """
        Constructeur :
        Initialise les attributs de l'objet.
        """
        self.state = True
        self.couleur = couleur
        self.symbole = symbole
    

# ---------- GETTERS / SETTERS ----------
    @property
    def state(self):
        return self.state

    @state.setter
    def state(self, value):
        if (isinstance(value, bool)):
            self.state = value
            
    @property
    def couleur(self):
        return self.couleur

    @couleur.setter
    def couleur(self, value):
        if (isinstance(value, COLORREF)):
            self.couleur = value
    
    @property
    def symbole(self):
        return self.symbole

    @symbole.setter
    def symbole(self, value):
        if (isinstance(value, str)):
            self.symbole = value







