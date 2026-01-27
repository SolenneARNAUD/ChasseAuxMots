import Donnees
import pygame as pg

class Fenetre(object):
    "Classe correspondant à la fenêtre de jeu."

    def __init__(self, image):
        "Constructeur de la classe Fenetre."
        # Initialisation des attributs
        self.size = (Donnees.WIDTH, Donnees.HEIGHT)
        self.couleur_fond = Donnees.COULEUR_FOND
        self._image = None
        self.set_image(image)
        self.bandeau = str(Donnees.BANDEAU_TEXTE)

    def set_image(self, image):
        if isinstance(image, str):
            try:
                self._image = pg.image.load(image).convert()
                # Redimensionner l'image au format de la fenêtre
                self._image = pg.transform.smoothscale(self._image, self.size)
            except Exception as e:
                print(f"Erreur chargement image {image}: {e}")
                self._image = None
        elif isinstance(image, pg.Surface):
            self._image = image
        else:
            self._image = None
    def afficher_fond(self, screen):
        if self._image:
            screen.blit(self._image, (0, 0))
        else:
            # Fallback : afficher la couleur si l'image ne charge pas
            screen.fill(self.couleur_fond)
    
    def afficher_bandeau(self, screen, niveau, n_mots, total_mots):
        fond = pg.Surface((Donnees.WIDTH, 40))
        fond.fill((0, 0, 0))  # Fond noir
        fond.set_alpha(150)   # Transparence
        font = pg.font.Font(None, 36)
        texte_surface = font.render(self.bandeau + str(niveau) + "          |         Mot n°" + str(n_mots) + "/" + str(total_mots), True, (255, 255, 255))
        screen.blit(fond, (0, 0))
        screen.blit(texte_surface, (10, 10))

    def afficher_game_over(self, screen):
        self.set_image(Donnees.FOND_GAME_OVER)
        self.afficher_fond(screen)
        font = pg.font.Font(None, 72)
        taille_bandeau = 100
        bandeau = pg.Surface((Donnees.WIDTH, taille_bandeau))
        bandeau.fill((0, 0, 0))  # Fond noir
        bandeau.set_alpha(150)   # Transparence
        texte_surface = font.render("GAME OVER", True, (255, 0, 0))
        rect = texte_surface.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
        screen.blit(bandeau, (0, Donnees.HEIGHT//2 - taille_bandeau//2))
        screen.blit(texte_surface, rect)
    
    def afficher_niveau_reussi(self, screen):
        font = pg.font.Font(None, 72)
        taille_bandeau = 100
        bandeau = pg.Surface((Donnees.WIDTH, taille_bandeau))
        bandeau.fill((0, 0, 0))  # Fond noir
        bandeau.set_alpha(150)   # Transparence
        texte_surface = font.render("Niveau Réussi!", True, (255, 255, 255))
        rect = texte_surface.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
        screen.blit(bandeau, (0, Donnees.HEIGHT//2 - taille_bandeau//2))
        screen.blit(texte_surface, rect)