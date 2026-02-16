import Donnees
import pygame as pg


class Fenetre(object):
    "Classe correspondant à la fenêtre de jeu."

    def __init__(self, image):
        "Constructeur de la classe Fenetre."
        # Initialisation des attributs
        self.size = (Donnees.WIDTH, Donnees.HEIGHT)
        self.couleur_fond = Donnees.COULEUR_FOND
        self._images = []  # Liste d'images pour le fond multicouche
        self.set_image(image)
        self.bandeau = str(Donnees.BANDEAU_TEXTE)

    def set_image(self, image):
        """Définit l'image ou les images de fond (peut être une liste)."""
        self._images = []
        
        # Si c'est une liste d'images (fond multicouche)
        if isinstance(image, list):
            for img_path in image:
                try:
                    loaded_img = pg.image.load(img_path).convert_alpha()
                    loaded_img = pg.transform.smoothscale(loaded_img, self.size)
                    self._images.append(loaded_img)
                except Exception as e:
                    print(f"Erreur chargement image {img_path}: {e}")
        # Si c'est une seule image (string)
        elif isinstance(image, str):
            try:
                loaded_img = pg.image.load(image).convert()
                loaded_img = pg.transform.smoothscale(loaded_img, self.size)
                self._images.append(loaded_img)
            except Exception as e:
                print(f"Erreur chargement image {image}: {e}")
        # Si c'est déjà une Surface
        elif isinstance(image, pg.Surface):
            self._images.append(image)
            
    def afficher_fond(self, screen):
        """Affiche le fond (une ou plusieurs images superposées)."""
        if self._images:
            # Afficher les images en ordre inversé (indice le plus grand = arrière-plan)
            for img in reversed(self._images):
                screen.blit(img, (0, 0))
        else:
            # Fallback : afficher la couleur si aucune image n'est chargée
            screen.fill(self.couleur_fond)
    
    def afficher_bandeau(self, screen, niveau, n_mots, total_mots):
        fond = pg.Surface((Donnees.WIDTH, Donnees.BANDEAU_HAUTEUR))
        fond.fill(Donnees.COULEUR_NOIR)
        fond.set_alpha(Donnees.BANDEAU_ALPHA)
        font = pg.font.Font(None, Donnees.BANDEAU_POLICE_TAILLE)
        texte_surface = font.render(self.bandeau + str(niveau) + "          |         Mot n°" + str(n_mots) + "/" + str(total_mots), True, Donnees.COULEUR_BLANC)
        screen.blit(fond, (0, 0))
        screen.blit(texte_surface, (Donnees.BANDEAU_MARGIN, Donnees.BANDEAU_MARGIN))

    def afficher_game_over(self, screen):
        self.set_image(Donnees.FOND_GAME_OVER)
        self.afficher_fond(screen)
        font = pg.font.Font(None, Donnees.GAME_OVER_POLICE_TAILLE)
        bandeau = pg.Surface((Donnees.WIDTH, Donnees.GAME_OVER_BANDEAU_HAUTEUR))
        bandeau.fill(Donnees.COULEUR_NOIR)
        bandeau.set_alpha(Donnees.GAME_OVER_ALPHA)
        texte_surface = font.render("GAME OVER", True, Donnees.COULEUR_BLANC)
        rect = texte_surface.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
        screen.blit(bandeau, (0, Donnees.HEIGHT//2 - Donnees.GAME_OVER_BANDEAU_HAUTEUR//2))
        screen.blit(texte_surface, rect)
    
    def afficher_niveau_reussi(self, screen):
        font = pg.font.Font(None, Donnees.GAME_OVER_POLICE_TAILLE)
        bandeau = pg.Surface((Donnees.WIDTH, Donnees.GAME_OVER_BANDEAU_HAUTEUR))
        bandeau.fill(Donnees.COULEUR_NOIR)
        bandeau.set_alpha(Donnees.GAME_OVER_ALPHA)
        texte_surface = font.render("Niveau Réussi!", True, Donnees.COULEUR_BLANC)
        rect = texte_surface.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
        screen.blit(bandeau, (0, Donnees.HEIGHT//2 - Donnees.GAME_OVER_BANDEAU_HAUTEUR//2))
        screen.blit(texte_surface, rect)

    def afficher_stats_fin_niveau(self, screen, mots_reussis, vitesse_wpm, erreurs):
        """Affiche les statistiques de fin de niveau."""
        # Fond semi-transparent
        overlay = pg.Surface((Donnees.WIDTH, Donnees.HEIGHT))
        overlay.fill(Donnees.COULEUR_NOIR)
        overlay.set_alpha(Donnees.STATS_FIN_ALPHA)
        screen.blit(overlay, (0, 0))
        
        font_titre = pg.font.Font(None, Donnees.STATS_FIN_POLICE_TITRE)
        font_stats = pg.font.Font(None, Donnees.STATS_FIN_POLICE_TEXTE)
        
        # Titre
        titre = font_titre.render("Statistiques du niveau", True, Donnees.COULEUR_BLANC)
        titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, Donnees.STATS_FIN_TITRE_Y))
        screen.blit(titre, titre_rect)
        
        # Stats
        stat1 = font_stats.render(f"Mots réussis: {mots_reussis}", True, Donnees.COULEUR_BLANC)
        screen.blit(stat1, (Donnees.WIDTH // 2 - Donnees.STATS_FIN_STATS_OFFSET_X, Donnees.STATS_FIN_STATS_Y))
        
        stat2 = font_stats.render(f"Vitesse: {vitesse_wpm:.1f} mots/min", True, Donnees.COULEUR_BLANC)
        screen.blit(stat2, (Donnees.WIDTH // 2 - Donnees.STATS_FIN_STATS_OFFSET_X, Donnees.STATS_FIN_STATS_Y + Donnees.STATS_FIN_LINE_HEIGHT))
        
        stat3 = font_stats.render(f"Erreurs: {erreurs}", True, Donnees.COULEUR_BLANC)
        screen.blit(stat3, (Donnees.WIDTH // 2 - Donnees.STATS_FIN_STATS_OFFSET_X, Donnees.STATS_FIN_STATS_Y + 2 * Donnees.STATS_FIN_LINE_HEIGHT))
        
        # Message pour retourner au menu
        menu = font_stats.render("Appuyez sur Échap pour retourner au menu", True, Donnees.COULEUR_GRIS_TEXTE)
        menu_rect = menu.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT - Donnees.STATS_FIN_MARGIN_BOTTOM))
        screen.blit(menu, menu_rect)
