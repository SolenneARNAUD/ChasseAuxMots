import pygame as pg
import Donnees

class Personnage(object):
    " Classe correspondant au personnage du jeu vidéo."

    def __init__(self, X, Y, skin, align_bottom_with=None):
        "Constructeur de la classe Personnage."
        self._position_x = int(X)   # centre X
        self._position_y = int(Y)   # bottom Y (on stocke la valeur bottom)
        self._skin = skin
        self.image = None
        self.rect = None
        
        # Animation du personnage
        self._is_animating = False
        self._animation_frame = 0
        self._animation_delay = 5  # nb frames avant changement sprite
        self._frame_counter = 0
        self._animation_frames = []  # liste des chemins des sprites pour l'animation
        self._animation_loop = False  # Boucler l'animation indéfiniment
        self._skin_base = skin  # conserve le skin par défaut
        self._is_flipped = False  # Flip horizontal du sprite

        # Charger l'image
        try:
            self.image = pg.image.load(self._skin).convert_alpha()
            # Redimensionner à une hauteur fixe
            w, h = self.image.get_size()
            if h > 0:
                scale = Donnees.PERSONNAGE_HEIGHT / h
                new_size = (int(w * scale), int(h * scale))
                self.image = pg.transform.smoothscale(self.image, new_size)
            # midbottom => center X, bottom Y
            self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y))
            # Si on demande un alignement sur le bas d'un autre sprite, l'appliquer tout de suite
            if align_bottom_with is not None and getattr(align_bottom_with, "rect", None):
                self.rect.bottom = align_bottom_with.rect.bottom
                # synchroniser la position interne (position_y représente bottom)
                self._position_y = self.rect.bottom
        except Exception as e:
            self.image = None
            self.rect = None
            print(f"Erreur chargement image {self._skin}: {e}")

    # position getters/setters (mettent à jour le rect)
    @property
    def position_x(self):
        return self._position_x

    @position_x.setter
    def position_x(self, X):
        if isinstance(X, (int, float)):
            self._position_x = int(X)
            if self.rect:
                self.rect.centerx = self._position_x

    @property
    def position_y(self):
        "Retourne la coordonnée bottom (bas) du sprite."
        return self._position_y

    @position_y.setter
    def position_y(self, Y):
        if isinstance(Y, (int, float)):
            self._position_y = int(Y)
            if self.rect:
                self.rect.bottom = self._position_y

    def get_skin(self):
        return self._skin

    def set_skin(self, skin):
        # accepter chemin ou Surface
        if isinstance(skin, str):
            self._skin = skin
            try:
                self.image = pg.image.load(self._skin).convert_alpha()
                self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y))
            except Exception as e:
                self.image = None
                self.rect = None
                print(f"Erreur chargement image {self._skin}: {e}")
        elif isinstance(skin, pg.Surface):
            self.image = skin
            self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y))

    def _set_skin_preserve_size(self, skin):
        """Charge un nouveau sprite en conservant la taille actuelle du personnage."""
        if isinstance(skin, str):
            # Conserver la taille actuelle
            current_size = None
            if self.rect:
                current_size = self.rect.size
            
            self._skin = skin
            try:
                self.image = pg.image.load(self._skin).convert_alpha()
                
                # Si on a une taille précédente, appliquer la même taille
                if current_size:
                    self.image = pg.transform.smoothscale(self.image, current_size)
                
                # Appliquer le flip si nécessaire
                if self._is_flipped:
                    self.image = pg.transform.flip(self.image, True, False)  # Flip horizontal
                
                self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y))
            except Exception as e:
                self.image = None
                self.rect = None
                print(f"Erreur chargement image {self._skin}: {e}")
        elif isinstance(skin, pg.Surface):
            self.image = skin
            # Appliquer le flip si nécessaire
            if self._is_flipped:
                self.image = pg.transform.flip(self.image, True, False)  # Flip horizontal
            self.rect = self.image.get_rect(midbottom=(self._position_x, self._position_y))

    def afficher(self, screen):
        "Affiche le personnage (center X, bottom Y) à l'écran."
        if self.image and self.rect:
            screen.blit(self.image, self.rect)

    def check_collision(self, obstacle):
        """Vérifie s'il y a collision entre le personnage et un obstacle.
        
        Args:
            obstacle: L'objet obstacle à vérifier
        
        Returns:
            True si collision détectée, False sinon
        """
        # Vérifier que les rect existent et sont valides
        if self.rect is None or not hasattr(obstacle, 'rect') or obstacle.rect is None:
            return False
        
        # Créer une copie du rect du personnage réduite pour diminuer la tolérance
        # On diminue la taille de 10 pixels de chaque côté (20 pixels au total par dimension)
        rect_tolerance = self.rect.inflate(-20, -20)
        # Vérifier la collision avec la zone élargie
        return rect_tolerance.colliderect(obstacle.rect)

    def start_animation(self, animation_frames, animation_delay=5, loop=False, flip=False):
        """Démarre une animation du personnage.
        
        Args:
            animation_frames: Liste des chemins des sprites (ex: ["images/Man/Viking/viking_1.png", ...])
            animation_delay: Nombre de frames avant de changer de sprite
            loop: Si True, l'animation boucle indéfiniment; sinon elle s'arrête une fois
            flip: Si True, le sprite est mirrorisé horizontalement
        """
        self._animation_frames = animation_frames
        self._animation_delay = animation_delay
        self._animation_frame = 0
        self._frame_counter = 0
        self._animation_loop = loop
        self._is_flipped = flip
        self._is_animating = True
        
        # Charger le premier sprite immédiatement
        if animation_frames and len(animation_frames) > 0:
            self._set_skin_preserve_size(animation_frames[0])

    def update_animation(self):
        """Met à jour l'animation en cours. À appeler à chaque frame."""
        if not self._is_animating or not self._animation_frames:
            return
        
        self._frame_counter += 1
        if self._frame_counter >= self._animation_delay:
            self._frame_counter = 0
            self._animation_frame += 1
            
            # Si on a terminé l'animation
            if self._animation_frame >= len(self._animation_frames):
                if self._animation_loop:
                    # Recommencer l'animation depuis le début et charger le premier sprite
                    self._animation_frame = 0
                    if len(self._animation_frames) > 0:
                        self._set_skin_preserve_size(self._animation_frames[0])
                else:
                    # Arrêter l'animation et revenir au sprite par défaut (avec flip si nécessaire)
                    self._is_animating = False
                    self._animation_frame = 0
                    # Ne pas changer _is_flipped ici si on veut garder le flip après animation
                    self._set_skin_preserve_size(self._skin_base)
                    return
            
            # Charger le prochain sprite en conservant la taille et le flip
            sprite_path = self._animation_frames[self._animation_frame]
            self._set_skin_preserve_size(sprite_path)

    def is_animating(self):
        """Retourne True si une animation est en cours."""
        return self._is_animating
    
    def set_flip(self, flip=False):
        """Change l'état du flip horizontal du sprite."""
        self._is_flipped = flip
        # Rafraîchir l'image avec le nouveau flip
        if self.image:
            self.image = pg.transform.flip(self.image, True, False) if flip else self.image
            # Recharger depuis la peau actuelle avec le nouveau flip
            if len(self._animation_frames) > 0:
                self._set_skin_preserve_size(self._animation_frames[self._animation_frame])
            else:
                self._set_skin_preserve_size(self._skin_base)