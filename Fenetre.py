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
        texte_surface = font.render("GAME OVER", True, (255, 255, 255))
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

    def afficher_stats_fin_niveau(self, screen, mots_reussis, vitesse_wpm, erreurs):
        """Affiche les statistiques de fin de niveau."""
        # Fond semi-transparent
        overlay = pg.Surface((Donnees.WIDTH, Donnees.HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        font_titre = pg.font.Font(None, 60)
        font_stats = pg.font.Font(None, 40)
        
        # Titre
        titre = font_titre.render("Statistiques du niveau", True, (255, 255, 255))
        titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 150))
        screen.blit(titre, titre_rect)
        
        # Stats
        y_offset = 250
        line_height = 50
        
        stat1 = font_stats.render(f"Mots réussis: {mots_reussis}", True, (255, 255, 255))
        screen.blit(stat1, (Donnees.WIDTH // 2 - 150, y_offset))
        
        stat2 = font_stats.render(f"Vitesse: {vitesse_wpm:.1f} mots/min", True, (255, 255, 255))
        screen.blit(stat2, (Donnees.WIDTH // 2 - 150, y_offset + line_height))
        
        stat3 = font_stats.render(f"Erreurs: {erreurs}", True, (255, 255, 255))
        screen.blit(stat3, (Donnees.WIDTH // 2 - 150, y_offset + 2 * line_height))
        
        # Message pour retourner au menu
        menu = font_stats.render("Appuyez sur Échap pour retourner au menu", True, (200, 200, 200))
        menu_rect = menu.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT - 60))
        screen.blit(menu, menu_rect)


def fenetre_niveau(screen, events):
    """
    Affiche la fenêtre de sélection des niveaux.
    Retourne le numéro du niveau cliqué (1 à 5) ou None.
    """

    screen.fill(Donnees.COULEUR_FOND)

    font = pg.font.Font(None, 48)

    # Paramètres des carrés
    taille = 100    # Taille des carrés
    espacement = 30 # Espacement entre les carrés

    largeur_totale = Donnees.NB_NIVEAUX * taille + (Donnees.NB_NIVEAUX - 1) * espacement # Calcul de la largeur totale
    start_x = (Donnees.WIDTH - largeur_totale) // 2 # Position de départ en X
    y = Donnees.HEIGHT // 2 - taille // 2           # Position en Y

    rectangles = [] # Liste des rectangles des niveaux

    for i in range(Donnees.NB_NIVEAUX):
        rect = pg.Rect(
            start_x + i * (taille + espacement),
            y,
            taille,
            taille
        )
        rectangles.append(rect) # Stockage du rectangle

        # Dessin du carré
        pg.draw.rect(screen, (200, 200, 200), rect) # Fond blanc gris
        pg.draw.rect(screen, (0, 0, 0), rect, 3) # Bordure noire

        # Numéro du niveau
        texte = font.render(str(i + 1), True, (0, 0, 0))
        texte_rect = texte.get_rect(center=rect.center)
        screen.blit(texte, texte_rect)

    pg.display.flip()

    # Gestion des clics
    for event in events: 
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            position = event.pos
            for i, rect in enumerate(rectangles):
                if rect.collidepoint(position):
                    return i + 1
    return None

