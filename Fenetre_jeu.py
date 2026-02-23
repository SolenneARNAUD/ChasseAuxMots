import Donnees
import pygame as pg
import CoucheParallaxe
import Menu
import os


class Fenetre(object):
    "Classe correspondant à la fenêtre de jeu."

    def __init__(self, image):
        "Constructeur de la classe Fenetre."
        # Initialisation des attributs
        self.size = (Donnees.WIDTH, Donnees.HEIGHT)
        self.couleur_fond = Donnees.COULEUR_FOND
        self._images = []  # Liste d'images pour le fond multicouche
        self._couches_parallaxe = []  # Liste des couches de parallaxe
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
    
    def initialiser_parallaxe(self, chemins_images):
        """Initialise les couches de parallaxe avec les chemins d'images fournis.
        
        Args:
            chemins_images: Liste de chemins d'images ordonnés du plus éloigné au plus proche
                          (index 0 = couche 7, la plus lente)
        """
        self._couches_parallaxe = []
        nb_couches = len(chemins_images)
        
        for i, chemin in enumerate(chemins_images):
            # Calculer le facteur de vitesse : 
            # - Couche 0 (image 7, la plus éloignée) : vitesse_facteur très faible
            # - Couche n-1 (image 1, la plus proche) : vitesse_facteur < 1 pour rester en dessous du sol
            # Formule : vitesse augmente progressivement de 0.1 à 0.8 (le sol est à 1.0)
            vitesse_facteur = 0.1 + (i / (nb_couches - 1)) * 0.7 if nb_couches > 1 else 0.5
            
            couche = CoucheParallaxe.CoucheParallaxe(chemin, vitesse_facteur, 0)
            self._couches_parallaxe.append(couche)
    
    def defiler_parallaxe(self, vitesse_sol):
        """Fait défiler toutes les couches de parallaxe.
        
        Args:
            vitesse_sol: vitesse de défilement du sol
        """
        for couche in self._couches_parallaxe:
            couche.defiler(vitesse_sol)
            
    def afficher_fond(self, screen):
        """Affiche le fond (une ou plusieurs images superposées ou couches de parallaxe)."""
        # Si on utilise la parallaxe, afficher les couches
        if self._couches_parallaxe:
            for couche in self._couches_parallaxe:
                couche.afficher(screen)
        # Sinon, afficher les images statiques
        elif self._images:
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
        """Affiche l'écran de game over avec un bouton pour accéder aux statistiques."""
        self.set_image(Donnees.FOND_GAME_OVER)
        self.afficher_fond(screen)
        
        # Bandeau semi-transparent
        bandeau = pg.Surface((Donnees.WIDTH, Donnees.GAME_OVER_BANDEAU_HAUTEUR))
        bandeau.fill(Donnees.COULEUR_NOIR)
        bandeau.set_alpha(Donnees.GAME_OVER_ALPHA)
        
        # Titre "GAME OVER" centré dans le bandeau
        font = pg.font.Font(None, Donnees.GAME_OVER_POLICE_TAILLE)
        texte_surface = font.render("GAME OVER", True, Donnees.COULEUR_BLANC)
        rect = texte_surface.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
        
        # Bouton "Statistiques"
        bouton_rect = pg.Rect(
            Donnees.WIDTH // 2 - Donnees.NIVEAU_REUSSI_BOUTON_WIDTH // 2,
            Donnees.NIVEAU_REUSSI_BOUTON_Y,
            Donnees.NIVEAU_REUSSI_BOUTON_WIDTH,
            Donnees.NIVEAU_REUSSI_BOUTON_HEIGHT
        )
        
        # Dessiner le bouton
        pg.draw.rect(screen, Donnees.NIVEAU_REUSSI_BOUTON_COULEUR, bouton_rect)
        pg.draw.rect(screen, Donnees.COULEUR_BLANC, bouton_rect, 3)
        
        # Texte du bouton
        font_bouton = pg.font.Font(None, Donnees.NIVEAU_REUSSI_BOUTON_POLICE)
        texte_bouton = font_bouton.render("Statistiques", True, Donnees.COULEUR_BLANC)
        rect_texte_bouton = texte_bouton.get_rect(center=bouton_rect.center)
        
        # Affichage
        screen.blit(bandeau, (0, Donnees.HEIGHT//2 - Donnees.GAME_OVER_BANDEAU_HAUTEUR//2))
        screen.blit(texte_surface, rect)
        screen.blit(texte_bouton, rect_texte_bouton)
        
        return bouton_rect
    
    def afficher_niveau_reussi(self, screen):
        """Affiche l'écran de niveau réussi avec un bouton pour accéder aux statistiques."""
        # Bandeau semi-transparent
        bandeau = pg.Surface((Donnees.WIDTH, Donnees.NIVEAU_REUSSI_BANDEAU_HAUTEUR))
        bandeau.fill(Donnees.COULEUR_NOIR)
        bandeau.set_alpha(Donnees.NIVEAU_REUSSI_BANDEAU_ALPHA)
        
        # Titre "Niveau réussi" en gros - centré dans le bandeau
        font_titre = pg.font.Font(None, Donnees.NIVEAU_REUSSI_POLICE_TITRE)
        texte_surface = font_titre.render("Niveau réussi", True, Donnees.COULEUR_BLANC)
        rect_titre = texte_surface.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
        
        # Bouton "Statistiques"
        bouton_rect = pg.Rect(
            Donnees.WIDTH // 2 - Donnees.NIVEAU_REUSSI_BOUTON_WIDTH // 2,
            Donnees.NIVEAU_REUSSI_BOUTON_Y,
            Donnees.NIVEAU_REUSSI_BOUTON_WIDTH,
            Donnees.NIVEAU_REUSSI_BOUTON_HEIGHT
        )
        
        # Dessiner le bouton
        pg.draw.rect(screen, Donnees.NIVEAU_REUSSI_BOUTON_COULEUR, bouton_rect)
        pg.draw.rect(screen, Donnees.COULEUR_BLANC, bouton_rect, 3)
        
        # Texte du bouton
        font_bouton = pg.font.Font(None, Donnees.NIVEAU_REUSSI_BOUTON_POLICE)
        texte_bouton = font_bouton.render("Statistiques", True, Donnees.COULEUR_BLANC)
        rect_texte_bouton = texte_bouton.get_rect(center=bouton_rect.center)
        
        # Affichage
        screen.blit(bandeau, (0, Donnees.HEIGHT//2 - Donnees.NIVEAU_REUSSI_BANDEAU_HAUTEUR//2))
        screen.blit(texte_surface, rect_titre)
        screen.blit(texte_bouton, rect_texte_bouton)
        
        return bouton_rect

    def afficher_stats_detaillees(self, screen, vitesse_wpm, erreurs_detaillees, caracteres_justes=0, caracteres_tapes=0, graphique_surface=None):
        """Affiche les statistiques détaillées : vitesse, mots avec erreurs, précision et historique graphique.
        
        Args:
            graphique_surface: Surface pygame pré-générée du graphique (pour éviter de le regénérer à chaque frame)
        """
        # Fond semi-transparent
        overlay = pg.Surface((Donnees.WIDTH, Donnees.HEIGHT))
        overlay.fill(Donnees.COULEUR_NOIR)
        overlay.set_alpha(Donnees.STATS_DETAILS_ALPHA)
        screen.blit(overlay, (0, 0))
        
        font_titre = pg.font.Font(None, Donnees.STATS_DETAILS_POLICE_TITRE)
        font_texte = pg.font.Font(None, Donnees.STATS_DETAILS_POLICE_TEXTE)
        font_erreur = pg.font.Font(None, Donnees.STATS_DETAILS_POLICE_ERREUR)
        
        # Zone pour l'historique (à gauche) - sans rectangle
        graph_x = 30
        graph_y = 80
        
        # Afficher le graphique d'historique s'il est fourni
        if graphique_surface:
            screen.blit(graphique_surface, (graph_x, graph_y))
        else:
            # Pas de graphique disponible
            texte_graph = font_texte.render("Historique (min. 2 parties)", True, Donnees.COULEUR_GRIS_TEXTE)
            screen.blit(texte_graph, (graph_x + 150, graph_y + 200))
        
        # Titre
        titre = font_titre.render("Statistiques détaillées", True, Donnees.COULEUR_BLANC)
        titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, Donnees.STATS_DETAILS_TITRE_Y))
        screen.blit(titre, titre_rect)
        
        # Vitesse de frappe (ajusté pour ne pas dépasser de la fenêtre)
        graph_max_width = 650
        x_stats = 620  # Position fixe pour éviter de dépasser WIDTH (1000px)
        y_current = Donnees.STATS_DETAILS_VITESSE_Y
        
        vitesse_texte = font_texte.render(f"Vitesse de frappe : {vitesse_wpm:.1f} caractères/s", True, Donnees.COULEUR_BLANC)
        screen.blit(vitesse_texte, (x_stats, y_current))
        y_current += 50  # Espacement après la vitesse
        
        # Précision
        if caracteres_tapes > 0:
            precision_pourcent = (caracteres_justes / caracteres_tapes) * 100
            precision_texte = font_texte.render(f"Précision : {caracteres_justes}/{caracteres_tapes} ({precision_pourcent:.1f}%)", True, Donnees.COULEUR_BLANC)
            screen.blit(precision_texte, (x_stats, y_current))
            y_current += 60  # Espacement après la précision
        else:
            y_current += 10  # Petit espacement si pas de précision
        
        # Affichage des erreurs
        if erreurs_detaillees:
            y_offset = y_current
            erreur_titre = font_texte.render("Mots avec erreurs :", True, Donnees.COULEUR_BLANC)
            screen.blit(erreur_titre, (x_stats, y_offset))
            y_offset += Donnees.STATS_DETAILS_LIGNE_HEIGHT + 5  # Espacement après le titre des erreurs
            
            # Dictionnaire pour regrouper les erreurs par mot puis par lettre
            erreurs_par_mot = {}
            for erreur in erreurs_detaillees:
                mot = erreur['mot']
                if mot not in erreurs_par_mot:
                    erreurs_par_mot[mot] = {}
                
                lettre_attendue = erreur['lettre_attendue']
                lettre_tapee = erreur['lettre_tapee']
                
                if lettre_attendue not in erreurs_par_mot[mot]:
                    erreurs_par_mot[mot][lettre_attendue] = []
                erreurs_par_mot[mot][lettre_attendue].append(lettre_tapee)
            
            # Afficher chaque mot avec ses erreurs
            for mot, erreurs_par_lettre in erreurs_par_mot.items():
                # Assigner une couleur à chaque lettre ayant des erreurs
                lettres_avec_erreurs = list(erreurs_par_lettre.keys())
                couleurs_par_lettre = {}
                for i, lettre in enumerate(lettres_avec_erreurs):
                    couleurs_par_lettre[lettre] = Donnees.PALETTE_ERREURS[i % len(Donnees.PALETTE_ERREURS)]
                
                # Afficher le mot avec les lettres colorées
                x_pos = x_stats
                for lettre in mot:
                    # Afficher l'espace comme "_"
                    lettre_affichee = "_" if lettre == " " else lettre
                    
                    if lettre in couleurs_par_lettre:
                        couleur = couleurs_par_lettre[lettre]
                    else:
                        couleur = Donnees.COULEUR_BLANC
                    
                    texte_lettre = font_erreur.render(lettre_affichee, True, couleur)
                    screen.blit(texte_lettre, (x_pos, y_offset))
                    x_pos += texte_lettre.get_width()
                
                # Afficher les lettres tapées incorrectement avec la même couleur
                x_pos += 15
                texte_separateur = font_erreur.render(" : ", True, Donnees.COULEUR_GRIS_TEXTE)
                screen.blit(texte_separateur, (x_pos, y_offset))
                x_pos += texte_separateur.get_width()
                
                # Afficher chaque groupe d'erreurs avec sa couleur
                first_group = True
                for lettre_attendue in lettres_avec_erreurs:
                    if not first_group:
                        texte_virgule = font_erreur.render(", ", True, Donnees.COULEUR_GRIS_TEXTE)
                        screen.blit(texte_virgule, (x_pos, y_offset))
                        x_pos += texte_virgule.get_width()
                    first_group = False
                    
                    couleur = couleurs_par_lettre[lettre_attendue]
                    
                    # Afficher les lettres tapées (pas la lettre attendue)
                    lettres_tapees = erreurs_par_lettre[lettre_attendue]
                    for lettre_tapee in lettres_tapees:
                        lettre_tapee_affichee = "_" if lettre_tapee == " " else lettre_tapee
                        texte_lettre_tapee = font_erreur.render(lettre_tapee_affichee, True, couleur)
                        screen.blit(texte_lettre_tapee, (x_pos, y_offset))
                        x_pos += texte_lettre_tapee.get_width()
                
                y_offset += Donnees.STATS_DETAILS_LIGNE_HEIGHT + 10  # Espacement entre chaque mot avec erreur
                
                # Limiter l'affichage pour ne pas déborder de l'écran
                if y_offset > Donnees.HEIGHT - 100:
                    texte_plus = font_erreur.render("...", True, Donnees.COULEUR_GRIS_TEXTE)
                    screen.blit(texte_plus, (x_stats, y_offset))
                    break
        else:
            texte_no_erreur = font_texte.render("Aucune erreur - Parfait !", True, Donnees.COULEUR_BLANC)
            screen.blit(texte_no_erreur, (x_stats, y_current))
        
        # Bouton Retour
        bouton_retour = pg.Rect(
            Donnees.WIDTH // 2 - 100,
            Donnees.HEIGHT - 80,
            200,
            50
        )
        
        # Dessiner le bouton
        pg.draw.rect(screen, (200, 100, 100), bouton_retour)
        pg.draw.rect(screen, Donnees.COULEUR_BLANC, bouton_retour, 3)
        
        # Texte du bouton
        font_bouton = pg.font.Font(None, 40)
        texte_bouton = font_bouton.render("Retour", True, Donnees.COULEUR_BLANC)
        rect_texte_bouton = texte_bouton.get_rect(center=bouton_retour.center)
        screen.blit(texte_bouton, rect_texte_bouton)
        
        return bouton_retour
    
    def afficher_menu_pause(self, screen, capture_ecran):
        """
        Affiche le menu pause avec l'écran de jeu en transparence.
        Retourne les rectangles des boutons (continuer, quitter).
        
        Args:
            screen: Surface pygame principale
            capture_ecran: Capture d'écran du jeu à afficher en fond
        
        Returns:
            tuple: (bouton_continuer, bouton_quitter)
        """
        # Afficher la capture d'écran du jeu
        screen.blit(capture_ecran, (0, 0))
        
        # Overlay semi-transparent
        overlay = pg.Surface((Donnees.WIDTH, Donnees.HEIGHT))
        overlay.fill(Donnees.COULEUR_NOIR)
        overlay.set_alpha(Donnees.PAUSE_OVERLAY_ALPHA)
        screen.blit(overlay, (0, 0))
        
        # Titre "PAUSE"
        font_titre = pg.font.Font(None, Donnees.PAUSE_TITRE_POLICE)
        texte_titre = font_titre.render("PAUSE", True, Donnees.COULEUR_BLANC)
        rect_titre = texte_titre.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 3))
        screen.blit(texte_titre, rect_titre)
        
        # Calcul des positions des boutons (centrés verticalement)
        bouton_w = Donnees.PAUSE_BOUTON_WIDTH
        bouton_h = Donnees.PAUSE_BOUTON_HEIGHT
        bouton_spacing = Donnees.PAUSE_BOUTON_SPACING
        total_boutons_height = 2 * bouton_h + bouton_spacing
        bouton_y_start = Donnees.HEIGHT // 2 - total_boutons_height // 2 + 50
        
        # Rectangle bouton Continuer
        bouton_continuer = pg.Rect(
            Donnees.WIDTH // 2 - bouton_w // 2,
            bouton_y_start,
            bouton_w,
            bouton_h
        )
        
        # Rectangle bouton Quitter
        bouton_quitter = pg.Rect(
            Donnees.WIDTH // 2 - bouton_w // 2,
            bouton_y_start + bouton_h + bouton_spacing,
            bouton_w,
            bouton_h
        )
        
        # Dessiner bouton Continuer
        pg.draw.rect(screen, Donnees.PAUSE_BOUTON_COULEUR_CONTINUER, bouton_continuer)
        pg.draw.rect(screen, Donnees.COULEUR_BLANC, bouton_continuer, 3)
        
        font_bouton = pg.font.Font(None, Donnees.PAUSE_BOUTON_POLICE)
        texte_continuer = font_bouton.render("Continuer", True, Donnees.COULEUR_BLANC)
        rect_texte_continuer = texte_continuer.get_rect(center=bouton_continuer.center)
        screen.blit(texte_continuer, rect_texte_continuer)
        
        # Dessiner bouton Quitter
        pg.draw.rect(screen, Donnees.PAUSE_BOUTON_COULEUR_QUITTER, bouton_quitter)
        pg.draw.rect(screen, Donnees.COULEUR_BLANC, bouton_quitter, 3)
        
        texte_quitter = font_bouton.render("Quitter sans sauvegarder", True, Donnees.COULEUR_BLANC)
        rect_texte_quitter = texte_quitter.get_rect(center=bouton_quitter.center)
        screen.blit(texte_quitter, rect_texte_quitter)
        
        return bouton_continuer, bouton_quitter

