import pygame as pg
from pygame.sprite import Sprite

class Personnage(object):
    " Classe correspondant au personnage du jeu vidéo."

    def __init__(self,X,Y,skin):
        "Constructeur de la classe Personnage."
        # Initialisation des attributs
        self.position_x = X
        self.position_y = Y
        self.skin = skin

        # Charger l'image une seule fois
        try:
            self.image = pg.image.load(self.skin).convert_alpha()
        except Exception as e:
            self.image = None
            print(f"Erreur chargement image {self.skin}: {e}")
    
    # Getter et Setter
    def get_position_x(self):
        "Renvoie la position en x du personnage."
        return self.position_x
    def set_position_x(self, X):
        "Modifie la position en x du personnage."
        if X is int:
            self.position_x = X

    def get_position_y(self):
        "Renvoie la position en y du personnage."
        return self.position_y
    def set_position_y(self, Y):
        "Modifie la position en y du personnage."
        if Y is int:
            self.position_y = Y
    
    def get_skin(self):
        "Renvoie le skin du personnage."
        return self.skin
    def set_skin(self, skin):
        "Modifie le skin du personnage."
        if skin is Sprite:
            self.skin = skin
    
    def afficher(self, screen):
        "Affiche le personnage à l'écran."
        screen.blit(self.image, (self.position_x, self.position_y))