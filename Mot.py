import Symbole
import pygame as pg

class Mot(object):
    """
    Cette classe a pour objectif d'encoder les mots qui sont composer 
    d'objets de la classe Symbole
    """
    
    def __init__(self, x, y, symboles):
        """
        Constructeur :
        Initialise les attributs de l'objet.
        """
        self._state = True
        self._position_x = x
        self._position_y = y
        self._symboles = []
        self._symboles = symboles
    

# ---------- GETTERS / SETTERS ----------
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if (isinstance(value, bool)):
            self._state = value
            
    @property
    def position_x(self):
        return self._position_x
    @position_x.setter
    def position_x(self, value):
        if (isinstance(value, int)):
            self._position_x = value
    @property
    def position_y(self):
        return self._position_y

    @position_y.setter
    def position_y(self, value):
        if (isinstance(value, int)):
            self.position_y = value
    
    @property
    def symbole(self):
        return self._symbole

    # @symboles.setter
    # def symboles(self, value):
    #     if (isinstance(value, list)):
    #         if(isinstance(elem, Symbole) for elem in value):
    #             self.symbole = value
    
    def afficher(self, screen):
        """
        Affiche le mot dans la fenêtre pygame en affichant chaque symbole
        """
        decalage = 0
        font = pg.font.Font(None, 36)
        for symbole in self._symboles:
            # Afficher chaque symbole à la position correcte
            symbole_surface = font.render(symbole._symbole, True, symbole._couleur)
            screen.blit(symbole_surface, (self._position_x + decalage, self._position_y))
            decalage += symbole_surface.get_width()  # Mettre à jour le décalage pour le prochain symbole




