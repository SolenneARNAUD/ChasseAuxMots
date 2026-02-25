import pygame as pg
import Donnees

class Obstacles(object):
    "Classe correspondant aux obstacles du décor."

    def __init__(self, image, position_x, position_y, type, animation_delay = 5, nb_images=4, animation_frames=None, foot_offset=0):
        "Constructeur de la classe Obstacles."
        self._position_x = int(position_x)   # centre X
        self._position_y = int(position_y)   # bottom Y
        self._foot_offset = int(foot_offset)  # Ajustement vertical pour aligner les pieds
        self.type = type  # 0: à sauter, 1: en hauteur, 2: méchant
        self.animation_delay = animation_delay
        self.nb_images = nb_images
        
        # Animation support
        self.animation_frames = animation_frames  # Liste de chemins de frames d'animation
        self._current_frame_index = 0  # Index de frame actuel
        self._frame_counter = 0  # Compteur pour délai d'animation
        self._animation_active = animation_frames is not None and len(animation_frames) > 0

        self.image = None
        self.rect = None
        self.image_cache = {}  # Cache pour les images chargées
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
                # Flipper l'image horizontalement (miroir)
                self.image = pg.transform.flip(self.image, True, False)
                # midbottom => center X, bottom Y (avec offset)
                self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y + self._foot_offset))
            except Exception as e:
                print(f"Erreur chargement image {image}: {e}")
                self.image = None
                self.rect = None
        elif isinstance(image, pg.Surface):
            self.image = image
            # Flipper l'image horizontalement (miroir)
            self.image = pg.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y + self._foot_offset))
        else:
            self.image = None
            self.rect = None

    def _load_animation_frame(self, frame_index):
        """Charge et cache une frame d'animation."""
        if not self.animation_frames or frame_index >= len(self.animation_frames):
            return False
        
        frame_path = self.animation_frames[frame_index]
        
        # Vérifier le cache
        if frame_path in self.image_cache:
            self.image = self.image_cache[frame_path]
            if self.rect:
                self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y + self._foot_offset))
            return True
        
        # Charger la frame
        try:
            img = pg.image.load(frame_path).convert_alpha()
            # Redimensionner à une hauteur fixe
            w, h = img.get_size()
            if h > 0:
                scale = Donnees.OBSTACLE_HEIGHT / h
                new_size = (int(w * scale), int(h * scale))
                img = pg.transform.smoothscale(img, new_size)
            # Flipper l'image horizontalement (miroir)
            img = pg.transform.flip(img, True, False)
            
            # Mettre en cache
            self.image_cache[frame_path] = img
            self.image = img
            
            # Mettre à jour le rect (avec offset)
            if self.rect:
                self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y + self._foot_offset))
            else:
                self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y + self._foot_offset))
            
            return True
        except Exception as e:
            print(f"Erreur chargement frame {frame_path}: {e}")
            return False

    def _update_animation(self):
        """Gère l'avancement de l'animation."""
        if not self._animation_active or not self.animation_frames:
            return
        
        self._frame_counter += 1
        
        if self._frame_counter >= self.animation_delay:
            self._frame_counter = 0
            self._current_frame_index = (self._current_frame_index + 1) % len(self.animation_frames)
            self._load_animation_frame(self._current_frame_index)

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
                # Appliquer l'offset pour aligner les pieds visuels
                self.rect.bottom = self._position_y + self._foot_offset

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
        
        # Gère l'animation
        self._update_animation()
        
        # Réinitialiser la position si l'obstacle sort de l'écran
        if self._position_x < -100:
            self._position_x = Donnees.WIDTH + 100
            if self.rect:
                self.rect.centerx = self._position_x
        
        return self._position_x