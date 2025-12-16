from pygame.sprite import Sprite
import pygame as pg

class Obstacles(object):
    "Classe correspondant aux obstacles du décor."

    def __init__(self, image, position_x, position_y, type):
        "Constructeur de la classe Obstacles."
        # Initialisation des attributs
        self.image = image
        self.position_x = position_x
        self.position_y = position_y
        self.type = type # 0: à sauter, 1: en hauteur, 2: méchant

        # Charger l'image une seule fois
        try:
            self.image = pg.image.load(self.image).convert_alpha()
        except Exception as e:
            self.image = None
            print(f"Erreur chargement image {self.image}: {e}")
    
    # Getter et Setter
    def get_image(self):
        "Renvoie l'image de l'obstacle."
        return self.image
    def set_image(self, image):
        "Modifie l'image de l'obstacle."
        if image is Sprite:
            self.image = image
    
    def get_position_x(self):
        "Renvoie la position en x de l'obstacle."
        return self.position_x
    def set_position_x(self, position_x):
        "Modifie la position en x de l'obstacle."
        if position_x is int:
            self.position_x = position_x

    def get_position_y(self):
        "Renvoie la position en y de l'obstacle."
        return self.position_y
    def set_position_y(self, position_y):
        "Modifie la position en y de l'obstacle."
        if position_y is int:
            self.position_y = position_y

    def get_type(self):
        "Renvoie le type de l'obstacle."
        return self.type
    def set_type(self, type):
        "Modifie le type de l'obstacle."
        if type is int:
            self.type = type
    
    def afficher(self, screen):
        "Affiche l'obstacle à l'écran."
        screen.blit(self.image, (self.position_x, self.position_y))