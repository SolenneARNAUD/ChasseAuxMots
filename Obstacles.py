import pygame as pg

class Obstacles(object):
    "Classe correspondant aux obstacles du décor."

    def __init__(self, image, position_x, position_y, type):
        "Constructeur de la classe Obstacles."
        self._position_x = int(position_x)   # centre X
        self._position_y = int(position_y)   # bottom Y
        self.type = type  # 0: à sauter, 1: en hauteur, 2: méchant

        self.image = None
        self.rect = None
        self.set_image(image)

    def set_image(self, image):
        if isinstance(image, str):
            try:
                self.image = pg.image.load(image).convert_alpha()
                # midbottom => center X, bottom Y
                self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y))
            except Exception as e:
                print(f"Erreur chargement image {image}: {e}")
                self.image = None
                self.rect = None
        elif isinstance(image, pg.Surface):
            self.image = image
            self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y))
        else:
            self.image = None
            self.rect = None

    @property
    def position_x(self):
        return self._position_x

    @position_x.setter
    def position_x(self, value):
        if isinstance(value, (int, float)):
            self._position_x = int(value)
            if self.rect:
                self.rect.centerx = self._position_x

    @property
    def position_y(self):
        "Retourne la coordonnée bottom (bas) de l'obstacle."
        return self._position_y

    @position_y.setter
    def position_y(self, value):
        if isinstance(value, (int, float)):
            self._position_y = int(value)
            if self.rect:
                self.rect.bottom = self._position_y

    def afficher(self, screen):
        if self.image and self.rect:
            screen.blit(self.image, self.rect)
        else:
            # debug : petit rectangle positionné avec bottom = position_y
            w, h = 32, 32
            debug_rect = pg.Rect(self._position_x - w//2, self._position_y - h, w, h)
            pg.draw.rect(screen, (255, 0, 0), debug_rect)