import Donnees
import pygame as pg


class Sol(object):
    "Classe correspondant aux sols."

    def __init__(self, image, position_x, position_y):
        """Constructeur de la classe Sol.

        image: chemin vers l'image ou Surface pygame
        position_x: centre X
        position_y: bottom Y
        """
        self._position_x = int(position_x) # centre X
        self._position_y = int(position_y)
        self._image = None
        self._rect = None
        self.set_image(image)

        # Redimensionner l'image en conservant le ratio (utiliser la Surface chargée)
        if self._image:
            w, h = self._image.get_size()
            if w > 0:
                scale = Donnees.WIDTH / w
                new_size = (int(w * scale), int(h * scale))
                self._image = pg.transform.smoothscale(self._image, new_size)
            # Mettre à jour le rect après le redimensionnement
            self._rect = self._image.get_rect(midbottom=(self._position_x, self._position_y))

    def set_image(self, image):
        if isinstance(image, str):
            try:
                self._image = pg.image.load(image).convert_alpha()
                # midbottom => center X, bottom Y
                self._rect = self._image.get_rect(midbottom=(self._position_x, self._position_y))
            except Exception as e:
                print(f"Erreur chargement image {image}: {e}")
                self._image = None
                self._rect = None
        elif isinstance(image, pg.Surface):
            self._image = image
            self._rect = self._image.get_rect(midbottom=(self._position_x, self._position_y))
        else:
            self._image = None
            self._rect = None

    @property
    def position_x(self):
        return self._position_x

    @position_x.setter
    def position_x(self, value):
        if isinstance(value, (int, float)):
            self._position_x = int(value)
            if self._rect:
                self._rect.centerx = self._position_x

    @property
    def position_y(self):
        """Retourne la coordonnée bottom (bas) du sol."""
        return self._position_y

    @position_y.setter
    def position_y(self, value):
        if isinstance(value, (int, float)):
            self._position_y = int(value)
            if self._rect:
                self._rect.bottom = self._position_y

    def afficher(self, screen):
        if self._image and self._rect:
            screen.blit(self._image, self._rect)
        else:
            # debug : petit rectangle positionné avec bottom = position_y
            debug_rect = pg.Rect(0, 0, 50, 20)
            debug_rect.midbottom = (self._position_x, self._position_y)
            pg.draw.rect(screen, (255, 0, 0), debug_rect)
    def get_rect(self):
        return self._rect
    
    def defiler(self, vitesse):
        """Fait défiler le sol vers la gauche à la vitesse donnée."""
        self.position_x -= vitesse
        # Si le sol est complètement hors de l'écran à gauche, le repositionner à droite
        if self._rect and self._rect.right < 0:
            self.position_x += 2 * Donnees.WIDTH  # Repositionner à droite de l'écran