import Donnees
import pygame as pg


class CoucheParallaxe(object):
    """Classe représentant une couche de parallaxe avec défilement continu."""

    def __init__(self, image_path, vitesse_facteur, position_y=0):
        """Constructeur de la classe CoucheParallaxe.
        
        Args:
            image_path: chemin vers l'image de la couche
            vitesse_facteur: facteur de vitesse par rapport au sol (0.0 à 1.0)
                            1.0 = vitesse du sol, 0.0 = pas de défilement
            position_y: position verticale de la couche (0 = haut de l'écran)
        """
        self._vitesse_facteur = vitesse_facteur
        self._position_y = position_y
        self._position_x1 = 0.0  # Position de la première image
        self._position_x2 = float(Donnees.WIDTH)  # Position de la deuxième image
        self._image = None
        self._rect1 = None
        self._rect2 = None
        self.set_image(image_path)

    def set_image(self, image_path):
        """Charge et redimensionne l'image pour la couche."""
        if isinstance(image_path, str):
            try:
                self._image = pg.image.load(image_path).convert_alpha()
                # Redimensionner l'image à la taille de l'écran
                self._image = pg.transform.smoothscale(self._image, (Donnees.WIDTH, Donnees.HEIGHT))
                # Créer les rectangles pour les deux images
                self._rect1 = self._image.get_rect(topleft=(self._position_x1, self._position_y))
                self._rect2 = self._image.get_rect(topleft=(self._position_x2, self._position_y))
            except Exception as e:
                print(f"Erreur chargement image {image_path}: {e}")
                self._image = None
                self._rect1 = None
                self._rect2 = None
        else:
            self._image = None
            self._rect1 = None
            self._rect2 = None

    def defiler(self, vitesse_sol):
        """Fait défiler la couche vers la gauche à une vitesse proportionnelle au sol.
        
        Args:
            vitesse_sol: vitesse de défilement du sol
        """
        vitesse = vitesse_sol * self._vitesse_facteur
        self._position_x1 -= vitesse
        self._position_x2 -= vitesse
        
        # Si la première image est complètement sortie à gauche, la repositionner à droite
        if self._position_x1 + Donnees.WIDTH <= 0:
            self._position_x1 = self._position_x2 + Donnees.WIDTH
        
        # Si la deuxième image est complètement sortie à gauche, la repositionner à droite
        if self._position_x2 + Donnees.WIDTH <= 0:
            self._position_x2 = self._position_x1 + Donnees.WIDTH
        
        # Mettre à jour les rectangles
        if self._rect1 and self._rect2:
            self._rect1.x = round(self._position_x1)
            self._rect2.x = round(self._position_x2)

    def afficher(self, screen):
        """Affiche la couche de parallaxe sur l'écran."""
        if self._image and self._rect1 and self._rect2:
            screen.blit(self._image, self._rect1)
            screen.blit(self._image, self._rect2)

    @property
    def vitesse_facteur(self):
        """Retourne le facteur de vitesse de la couche."""
        return self._vitesse_facteur

    @vitesse_facteur.setter
    def vitesse_facteur(self, value):
        """Définit le facteur de vitesse de la couche."""
        if 0.0 <= value <= 1.0:
            self._vitesse_facteur = value
