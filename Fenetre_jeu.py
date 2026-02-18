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

    def afficher_stats_detaillees(self, screen, vitesse_wpm, erreurs_detaillees):
        """Affiche les statistiques détaillées : vitesse, mots avec erreurs, et zone pour historique."""
        # Fond semi-transparent
        overlay = pg.Surface((Donnees.WIDTH, Donnees.HEIGHT))
        overlay.fill(Donnees.COULEUR_NOIR)
        overlay.set_alpha(Donnees.STATS_DETAILS_ALPHA)
        screen.blit(overlay, (0, 0))
        
        font_titre = pg.font.Font(None, Donnees.STATS_DETAILS_POLICE_TITRE)
        font_texte = pg.font.Font(None, Donnees.STATS_DETAILS_POLICE_TEXTE)
        font_erreur = pg.font.Font(None, Donnees.STATS_DETAILS_POLICE_ERREUR)
        
        # Rectangle pour l'historique (à gauche) - zone réservée pour plus tard
        rect_graph = pg.Rect(
            Donnees.STATS_DETAILS_GRAPH_X,
            Donnees.STATS_DETAILS_GRAPH_Y,
            Donnees.STATS_DETAILS_GRAPH_WIDTH,
            Donnees.STATS_DETAILS_GRAPH_HEIGHT
        )
        pg.draw.rect(screen, Donnees.COULEUR_GRIS_FONCE, rect_graph)
        pg.draw.rect(screen, Donnees.COULEUR_BLANC, rect_graph, 2)
        
        # Texte "Historique" dans le rectangle
        texte_graph = font_texte.render("Historique", True, Donnees.COULEUR_GRIS_TEXTE)
        rect_texte_graph = texte_graph.get_rect(center=(rect_graph.centerx, rect_graph.centery))
        screen.blit(texte_graph, rect_texte_graph)
        
        # Titre
        titre = font_titre.render("Statistiques détaillées", True, Donnees.COULEUR_BLANC)
        titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, Donnees.STATS_DETAILS_TITRE_Y))
        screen.blit(titre, titre_rect)
        
        # Vitesse de frappe
        x_stats = Donnees.STATS_DETAILS_GRAPH_X + Donnees.STATS_DETAILS_GRAPH_WIDTH + 50
        vitesse_texte = font_texte.render(f"Vitesse de frappe : {vitesse_wpm:.1f} caractères/s", True, Donnees.COULEUR_BLANC)
        screen.blit(vitesse_texte, (x_stats, Donnees.STATS_DETAILS_VITESSE_Y))
        
        # Affichage des erreurs
        if erreurs_detaillees:
            y_offset = Donnees.STATS_DETAILS_ERREUR_Y
            erreur_titre = font_texte.render("Mots avec erreurs :", True, Donnees.COULEUR_BLANC)
            screen.blit(erreur_titre, (x_stats, y_offset))
            y_offset += Donnees.STATS_DETAILS_LIGNE_HEIGHT
            
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
                
                y_offset += Donnees.STATS_DETAILS_LIGNE_HEIGHT
                
                # Limiter l'affichage pour ne pas déborder de l'écran
                if y_offset > Donnees.HEIGHT - 100:
                    texte_plus = font_erreur.render("...", True, Donnees.COULEUR_GRIS_TEXTE)
                    screen.blit(texte_plus, (x_stats, y_offset))
                    break
        else:
            texte_no_erreur = font_texte.render("Aucune erreur - Parfait !", True, Donnees.COULEUR_BLANC)
            screen.blit(texte_no_erreur, (x_stats, Donnees.STATS_DETAILS_ERREUR_Y))
        
        # Message pour retourner
        info_retour = font_erreur.render("Appuyez sur Échap pour retourner au menu", True, Donnees.COULEUR_GRIS_TEXTE)
        info_rect = info_retour.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT - 30))
        screen.blit(info_retour, info_rect)

