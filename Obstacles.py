import pygame as pg
import Donnees

class Obstacles(object):
    "Classe correspondant aux obstacles du décor."

    def __init__(self, image, position_x, position_y, type, animation_delay = 5, nb_images=4):
        "Constructeur de la classe Obstacles."
        self._position_x = int(position_x)   # centre X
        self._position_y = int(position_y)   # bottom Y
        self.type = type  # 0: à sauter, 1: en hauteur, 2: méchant
        self.animation_delay = animation_delay
        self.nb_images = nb_images

        self.image = None
        self.rect = None
        self.set_image(image)

    def set_image(self, image):
        if isinstance(image, str):
            try:
                self.image = pg.image.load(image).convert_alpha()
                # Redimensionner à une hauteur fixe
                w, h = self.image.get_size()
                if h > 0:
                    scale = Donnees.OBSTACLE_HEIGHT / h
                    new_size = (int(w * scale), int(h * scale))
                    self.image = pg.transform.smoothscale(self.image, new_size)
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

    def update_position(self, vitesse):
        """Déplace l'obstacle à une vitesse donnée et réinitialise s'il sort de l'écran."""
        self._position_x -= vitesse
        if self.rect:
            self.rect.centerx = self._position_x
        
        # Réinitialiser la position si l'obstacle sort de l'écran
        if self._position_x < -100:
            self._position_x = Donnees.WIDTH + 100
            if self.rect:
                self.rect.centerx = self._position_x
        
        return self._position_x