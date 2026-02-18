import Donnees
import pygame as pg
import sys
import BaseDonnees


class Menu:
    """Classe regroupant tous les menus du jeu."""
    
    @staticmethod
    def fenetre_parametres(screen, vitesse_actuelle, reset_on_error_actuel=True, delai_niveau4_actuel=1500, joueur=None):
        """
        Affiche une fenêtre modale pour configurer les paramètres du jeu.
        Retourne un tuple (vitesse_pourcentage, reset_on_error, delai_niveau4) ou None si annulé.
        """
        vitesse_str = ""
        vitesse_affichee = str(vitesse_actuelle)
        reset_on_error = reset_on_error_actuel
        delai_str = ""
        delai_affiche = str(delai_niveau4_actuel)
        clock = pg.time.Clock()
        input_active = False
        input_delai_active = False
        
        # Division de l'écran en 3 zones
        zone_titre_height = Donnees.HEIGHT // Donnees.PARAMS_ZONE_TITRE_RATIO
        zone_params_height = Donnees.HEIGHT // Donnees.PARAMS_ZONE_PARAMS_RATIO
        zone_boutons_y = zone_titre_height + zone_params_height
        
        # Zone du milieu : calcul de l'espacement vertical
        # X pixels vides, Y pixels texte, X pixels vides, Y pixels texte, X pixels vides, Y pixels texte, X pixels vides
        param_height = Donnees.PARAMS_PARAM_HEIGHT
        spacing = (zone_params_height - 3 * param_height) // 4  # Espacement X pour 3 paramètres
        
        # Position verticale des paramètres dans la zone milieu
        param1_y = zone_titre_height + spacing
        param2_y = param1_y + param_height + spacing
        param3_y = param2_y + param_height + spacing
        
        # Alignement horizontal : labels à gauche, inputs à droite alignés
        label_x = Donnees.WIDTH // Donnees.PARAMS_LABEL_X_RATIO
        input_x = Donnees.WIDTH // 2 + Donnees.PARAMS_INPUT_X_OFFSET
        
        # Zones interactives
        input_box = pg.Rect(input_x, param1_y, Donnees.PARAMS_INPUT_BOX_WIDTH, Donnees.PARAMS_INPUT_BOX_HEIGHT)
        checkbox_rect = pg.Rect(input_x + Donnees.PARAMS_CHECKBOX_OFFSET_X, param2_y + Donnees.PARAMS_CHECKBOX_OFFSET_Y, 
                               Donnees.PARAMS_CHECKBOX_SIZE, Donnees.PARAMS_CHECKBOX_SIZE)
        input_delai_box = pg.Rect(input_x, param3_y, Donnees.PARAMS_INPUT_BOX_WIDTH, Donnees.PARAMS_INPUT_BOX_HEIGHT)
        
        # Boutons en bas
        bouton_w = Donnees.PARAMS_BOUTON_WIDTH
        bouton_h = Donnees.PARAMS_BOUTON_HEIGHT
        bouton_spacing = Donnees.PARAMS_BOUTON_SPACING
        total_boutons_width = 2 * bouton_w + bouton_spacing
        bouton_y = zone_boutons_y + (Donnees.HEIGHT - zone_boutons_y) // 2 - bouton_h // 2
        
        bouton_valider = pg.Rect(Donnees.WIDTH // 2 - total_boutons_width // 2, bouton_y, bouton_w, bouton_h)
        bouton_retour = pg.Rect(Donnees.WIDTH // 2 - total_boutons_width // 2 + bouton_w + bouton_spacing, bouton_y, bouton_w, bouton_h)
        
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    sys.exit()
                
                # Clic sur la zone de saisie
                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_active = True
                        input_delai_active = False
                        vitesse_str = ""
                    elif input_delai_box.collidepoint(event.pos):
                        input_delai_active = True
                        input_active = False
                        delai_str = ""
                    elif checkbox_rect.collidepoint(event.pos):
                        reset_on_error = not reset_on_error
                    elif bouton_retour.collidepoint(event.pos):
                        return None
                    elif bouton_valider.collidepoint(event.pos):
                        try:
                            val = int(vitesse_str) if vitesse_str else vitesse_actuelle
                        except Exception:
                            val = vitesse_actuelle
                        val = max(Donnees.VITESSE_POURCENTAGE_MIN, min(Donnees.VITESSE_POURCENTAGE_MAX, val))
                        vitesse_affichee = str(val)
                        
                        try:
                            delai_val = int(delai_str) if delai_str else delai_niveau4_actuel
                        except Exception:
                            delai_val = delai_niveau4_actuel
                        delai_val = max(Donnees.DELAI_NIVEAU4_MIN, min(Donnees.DELAI_NIVEAU4_MAX, delai_val))
                        delai_affiche = str(delai_val)
                        
                        # Sauvegarder la dernière valeur pour le joueur
                        if joueur is not None:
                            try:
                                nom_j, prenom_j = joueur
                                val_wpm = (val / 100.0) * Donnees.WPM_BASE_CONVERSION
                                BaseDonnees.set_derniere_vitesse(nom_j, prenom_j, val_wpm)
                            except Exception:
                                pass
                        
                        return (int(val), reset_on_error, int(delai_val))
                
                if event.type == pg.KEYDOWN:
                    if input_active:
                        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER or event.key == pg.K_TAB:
                            input_active = False
                            input_delai_active = True
                        elif event.key == pg.K_ESCAPE:
                            return None
                        elif event.key == pg.K_BACKSPACE:
                            vitesse_str = vitesse_str[:-1]
                        elif event.unicode.isdigit() and len(vitesse_str) < 3:
                            vitesse_str += event.unicode
                    elif input_delai_active:
                        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                            try:
                                val = int(vitesse_str) if vitesse_str else vitesse_actuelle
                            except Exception:
                                val = vitesse_actuelle
                            val = max(Donnees.VITESSE_POURCENTAGE_MIN, min(Donnees.VITESSE_POURCENTAGE_MAX, val))
                            vitesse_affichee = str(val)
                            
                            try:
                                delai_val = int(delai_str) if delai_str else delai_niveau4_actuel
                            except Exception:
                                delai_val = delai_niveau4_actuel
                            delai_val = max(Donnees.DELAI_NIVEAU4_MIN, min(Donnees.DELAI_NIVEAU4_MAX, delai_val))
                            delai_affiche = str(delai_val)
                            
                            if joueur is not None:
                                try:
                                    nom_j, prenom_j = joueur
                                    val_wpm = (val / 100.0) * Donnees.WPM_BASE_CONVERSION
                                    BaseDonnees.set_derniere_vitesse(nom_j, prenom_j, val_wpm)
                                except Exception:
                                    pass
                            
                            return (int(val), reset_on_error, int(delai_val))
                        elif event.key == pg.K_ESCAPE:
                            return None
                        elif event.key == pg.K_BACKSPACE:
                            delai_str = delai_str[:-1]
                        elif event.unicode.isdigit() and len(delai_str) < 5:
                            delai_str += event.unicode
                    else:
                        if event.key == pg.K_ESCAPE:
                            return None
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            font_titre = pg.font.Font(None, Donnees.PARAMS_FENETRE_POLICE_TITRE)
            font_label = pg.font.Font(None, Donnees.PARAMS_FENETRE_POLICE_LABEL)
            font_input = pg.font.Font(None, Donnees.PARAMS_FENETRE_POLICE_INPUT)
            font_bouton = pg.font.Font(None, Donnees.PARAMS_FENETRE_POLICE_BOUTON)
            
            # === ZONE TITRE ===
            titre = font_titre.render("Paramètres", True, Donnees.COULEUR_NOIR)
            screen.blit(titre, (Donnees.WIDTH // 2 - titre.get_width() // 2, zone_titre_height // 2 - titre.get_height() // 2))
            
            # Ligne de séparation après le titre
            pg.draw.line(screen, Donnees.PARAMS_LIGNE_SEPARATION_COULEUR, 
                        (Donnees.WIDTH // Donnees.PARAMS_LIGNE_SEPARATION_RATIO, zone_titre_height - Donnees.PARAMS_LIGNE_SEPARATION_OFFSET), 
                        (5 * Donnees.WIDTH // Donnees.PARAMS_LIGNE_SEPARATION_RATIO, zone_titre_height - Donnees.PARAMS_LIGNE_SEPARATION_OFFSET), 
                        Donnees.PARAMS_LIGNE_SEPARATION_EPAISSEUR)
            
            # === ZONE PARAMÈTRES ===
            
            # Paramètre 1 : Vitesse de défilement
            label_vitesse = font_label.render("Vitesse de défilement", True, Donnees.COULEUR_NOIR)
            screen.blit(label_vitesse, (label_x, param1_y + 10))
            
            # Input box vitesse
            pg.draw.rect(screen, Donnees.COULEUR_BLANC, input_box)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR if not input_active else Donnees.PARAMS_INPUT_BOX_COULEUR_ACTIVE, 
                        input_box, Donnees.PARAMS_INPUT_BOX_BORDURE)
            
            if input_active:
                texte_vitesse = font_input.render(vitesse_str + "|", True, Donnees.COULEUR_NOIR)
            else:
                texte_vitesse = font_input.render(vitesse_affichee + " %", True, (100, 100, 100))
            
            screen.blit(texte_vitesse, (input_box.centerx - texte_vitesse.get_width() // 2, 
                                        input_box.centery - texte_vitesse.get_height() // 2))
            
            # Paramètre 2 : Reset du mot après erreur
            label_reset = font_label.render("Reset du mot après erreur", True, Donnees.COULEUR_NOIR)
            screen.blit(label_reset, (label_x, param2_y + 10))
            
            # Checkbox
            pg.draw.rect(screen, Donnees.COULEUR_BLANC, checkbox_rect)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, checkbox_rect, Donnees.PARAMS_INPUT_BOX_BORDURE)
            
            if reset_on_error:
                # Checkmark
                pg.draw.line(screen, Donnees.COULEUR_VERT_FONCE, 
                            (checkbox_rect.left + Donnees.PARAMS_CHECKMARK_MARGIN_LEFT, checkbox_rect.centery),
                            (checkbox_rect.centerx - Donnees.PARAMS_CHECKMARK_MARGIN_RIGHT, checkbox_rect.bottom - Donnees.PARAMS_CHECKMARK_MARGIN_BOTTOM), 
                            Donnees.PARAMS_CHECKMARK_EPAISSEUR)
                pg.draw.line(screen, Donnees.COULEUR_VERT_FONCE,
                            (checkbox_rect.centerx - Donnees.PARAMS_CHECKMARK_MARGIN_RIGHT, checkbox_rect.bottom - Donnees.PARAMS_CHECKMARK_MARGIN_BOTTOM),
                            (checkbox_rect.right - Donnees.PARAMS_CHECKMARK_MARGIN_LEFT, checkbox_rect.top + Donnees.PARAMS_CHECKMARK_MARGIN_TOP), 
                            Donnees.PARAMS_CHECKMARK_EPAISSEUR)
            
            # Paramètre 3 : Délai d'affichage niveau 4
            label_delai = font_label.render("Délai affichage Niveau 4", True, Donnees.COULEUR_NOIR)
            screen.blit(label_delai, (label_x, param3_y + 10))
            
            # Input box délai
            pg.draw.rect(screen, Donnees.COULEUR_BLANC, input_delai_box)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR if not input_delai_active else Donnees.PARAMS_INPUT_BOX_COULEUR_ACTIVE, 
                        input_delai_box, Donnees.PARAMS_INPUT_BOX_BORDURE)
            
            if input_delai_active:
                texte_delai = font_input.render(delai_str + "|", True, Donnees.COULEUR_NOIR)
            else:
                texte_delai = font_input.render(delai_affiche + " ms", True, (100, 100, 100))
            
            screen.blit(texte_delai, (input_delai_box.centerx - texte_delai.get_width() // 2, 
                                      input_delai_box.centery - texte_delai.get_height() // 2))
            
            # Ligne de séparation avant les boutons
            pg.draw.line(screen, Donnees.PARAMS_LIGNE_SEPARATION_COULEUR, 
                        (Donnees.WIDTH // Donnees.PARAMS_LIGNE_SEPARATION_RATIO, zone_boutons_y + Donnees.PARAMS_LIGNE_SEPARATION_OFFSET), 
                        (5 * Donnees.WIDTH // Donnees.PARAMS_LIGNE_SEPARATION_RATIO, zone_boutons_y + Donnees.PARAMS_LIGNE_SEPARATION_OFFSET), 
                        Donnees.PARAMS_LIGNE_SEPARATION_EPAISSEUR)
            
            # === ZONE BOUTONS ===
            
            # Bouton Valider
            pg.draw.rect(screen, Donnees.PARAMS_BOUTON_COULEUR_VALIDER, bouton_valider)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, bouton_valider, Donnees.PARAMS_LIGNE_SEPARATION_EPAISSEUR)
            texte_valider = font_bouton.render("Valider", True, Donnees.COULEUR_BLANC)
            screen.blit(texte_valider, (bouton_valider.centerx - texte_valider.get_width() // 2,
                                       bouton_valider.centery - texte_valider.get_height() // 2))
            
            # Bouton Retour
            pg.draw.rect(screen, Donnees.PARAMS_BOUTON_COULEUR_RETOUR, bouton_retour)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, bouton_retour, Donnees.PARAMS_LIGNE_SEPARATION_EPAISSEUR)
            texte_retour = font_bouton.render("Retour", True, Donnees.COULEUR_BLANC)
            screen.blit(texte_retour, (bouton_retour.centerx - texte_retour.get_width() // 2,
                                      bouton_retour.centery - texte_retour.get_height() // 2))
            
            pg.display.flip()
            clock.tick(Donnees.FPS)

    @staticmethod
    def _calculer_rect_niveau(index):
        """
        Calcule le rectangle d'un bouton de niveau. 
        NB : on a ajouté un _ pour indiquer que c'est une fonction interne à ce module.
        """
        largeur_totale = (Donnees.NB_NIVEAUX * Donnees.NIVEAU_BOUTON_TAILLE + 
                         (Donnees.NB_NIVEAUX - 1) * Donnees.NIVEAU_BOUTON_ESPACEMENT)
        start_x = (Donnees.WIDTH - largeur_totale) // 2
        y = Donnees.HEIGHT // 2 - Donnees.NIVEAU_BOUTON_TAILLE // 2
        
        return pg.Rect(
            start_x + index * (Donnees.NIVEAU_BOUTON_TAILLE + Donnees.NIVEAU_BOUTON_ESPACEMENT),
            y,
            Donnees.NIVEAU_BOUTON_TAILLE,
            Donnees.NIVEAU_BOUTON_TAILLE
        )

    @staticmethod
    def fenetre_niveau(screen, joueur=None, vitesse_par_defaut=None, reset_on_error_defaut=None, delai_niveau4_defaut=None):
        """
        Affiche la fenêtre de sélection des niveaux avec un bouton paramètres.
        Retourne un tuple (niveau_selectionne, vitesse_pourcentage, reset_on_error, delai_niveau4).
        Retourne None si l'utilisateur appuie sur Échap (retour en arrière).
        Gère sa propre boucle jusqu'à ce qu'un niveau soit sélectionné.
        """
        clock = pg.time.Clock()
        niveau_selectionne = None
        niveau_survole = 0  # Index du niveau actuellement sélectionné au clavier (0-4)
        vitesse_pourcentage = vitesse_par_defaut if vitesse_par_defaut is not None else Donnees.VITESSE_POURCENTAGE_PAR_DEFAUT
        reset_on_error = reset_on_error_defaut if reset_on_error_defaut is not None else Donnees.RESET_ON_ERROR_PAR_DEFAUT
        delai_niveau4 = delai_niveau4_defaut if delai_niveau4_defaut is not None else Donnees.DELAI_NIVEAU4_PAR_DEFAUT
        
        # Définir le bouton paramètres (en bas à droite)
        btn_params = pg.Rect(
            Donnees.WIDTH - Donnees.NIVEAU_BOUTON_PARAMS_WIDTH - Donnees.NIVEAU_BOUTON_PARAMS_MARGIN,
            Donnees.HEIGHT - Donnees.NIVEAU_BOUTON_PARAMS_HEIGHT - Donnees.NIVEAU_BOUTON_PARAMS_MARGIN,
            Donnees.NIVEAU_BOUTON_PARAMS_WIDTH,
            Donnees.NIVEAU_BOUTON_PARAMS_HEIGHT
        )
        
        while niveau_selectionne is None:
            events = pg.event.get()
            
            # Survol avec la souris
            mouse_pos = pg.mouse.get_pos()
            for i in range(Donnees.NB_NIVEAUX):
                rect = Menu._calculer_rect_niveau(i)
                if rect.collidepoint(mouse_pos):
                    niveau_survole = i
                    break
            
            ## Gestion des événements ##
            for event in events:
                # Event 1 : Quitter le jeu
                if event.type == pg.QUIT:
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return None  # Retour en arrière
                    
                    # Navigation au clavier
                    if event.key == pg.K_LEFT:
                        niveau_survole = (niveau_survole - 1) % Donnees.NB_NIVEAUX
                    elif event.key == pg.K_RIGHT:
                        niveau_survole = (niveau_survole + 1) % Donnees.NB_NIVEAUX
                    elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        niveau_selectionne = niveau_survole + 1
                        break
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    position = event.pos
                    
                    # Vérifier le clic sur le bouton paramètres
                    if btn_params.collidepoint(position):
                        resultat = Menu.fenetre_parametres(screen, vitesse_pourcentage, reset_on_error, delai_niveau4, joueur)
                        if resultat is not None:
                            vitesse_pourcentage, reset_on_error, delai_niveau4 = resultat
                    
                    # Event 2 : Clic sur un niveau
                    for i in range(Donnees.NB_NIVEAUX):
                        rect = Menu._calculer_rect_niveau(i)
                        if rect.collidepoint(position): # Test si le clic est dans le rectangle du niveau
                            niveau_selectionne = i + 1 # Le niveau a été sélectionné > on sort de la boucle
                            break
            
            ## Affichage ##
            # Affichage 1 : Fond
            screen.fill(Donnees.COULEUR_FOND)
            font = pg.font.Font(None, Donnees.NIVEAU_TITRE_POLICE)
            font_small = pg.font.Font(None, Donnees.NIVEAU_POLICE_INFO)
            
            # Titre
            titre = font.render("Sélectionnez un niveau", True, Donnees.COULEUR_NOIR)
            screen.blit(titre, (Donnees.WIDTH//2 - titre.get_width()//2, Donnees.NIVEAU_TITRE_Y))
            
            # Affichage 2 : Boutons de niveaux
            for i in range(Donnees.NB_NIVEAUX):
                rect = Menu._calculer_rect_niveau(i)
                
                # Couleur de fond (surbrillance si sélectionné au clavier)
                couleur_fond = Donnees.NIVEAU_BOUTON_COULEUR_FOND
                if i == niveau_survole:
                    couleur_fond = (220, 220, 220)  # Couleur plus claire pour la sélection
                
                # Dessin du carré
                pg.draw.rect(screen, couleur_fond, rect)
                
                # Bordure plus épaisse si sélectionné
                epaisseur = Donnees.NIVEAU_BOUTON_EPAISSEUR_BORDURE
                if i == niveau_survole:
                    epaisseur = 5
                pg.draw.rect(screen, Donnees.NIVEAU_BOUTON_COULEUR_BORDURE, rect, epaisseur)
                
                # Numéro du niveau
                texte = font.render(str(i + 1), True, Donnees.NIVEAU_BOUTON_COULEUR_BORDURE)
                texte_rect = texte.get_rect(center=rect.center)
                screen.blit(texte, texte_rect)
            
            # Affichage 3 : Bouton paramètres
            pg.draw.rect(screen, Donnees.COULEUR_BLEU_BOUTON, btn_params)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, btn_params, Donnees.NIVEAU_BOUTON_PARAMS_BORDURE)
            texte_params = font_small.render("Paramètres", True, Donnees.COULEUR_BLANC)
            texte_params_rect = texte_params.get_rect(center=btn_params.center)
            screen.blit(texte_params, texte_params_rect)
            
            # Affichage 4 : Vitesse actuelle
            info_vitesse = font_small.render(f"Vitesse: {vitesse_pourcentage}%", True, Donnees.COULEUR_GRIS_FONCE)
            screen.blit(info_vitesse, (Donnees.NIVEAU_INFO_MARGIN, Donnees.HEIGHT - Donnees.NIVEAU_INFO_VITESSE_Y))
            
            # Affichage 5 : Mode reset
            reset_mode = "Reset: OUI" if reset_on_error else "Reset: NON"
            reset_color = Donnees.COULEUR_VERT_FONCE if reset_on_error else Donnees.COULEUR_ROUGE_FONCE
            info_reset = font_small.render(reset_mode, True, reset_color)
            screen.blit(info_reset, (Donnees.NIVEAU_INFO_MARGIN, Donnees.HEIGHT - Donnees.NIVEAU_INFO_RESET_Y))
            
            # Affichage 6 : Message Échap pour retour
            info_echap = font_small.render("Échap: retour | Flèches: navigation | Entrée: valider", True, Donnees.COULEUR_GRIS_FONCE)
            screen.blit(info_echap, (Donnees.WIDTH // 2 - info_echap.get_width() // 2, Donnees.HEIGHT - 30))
            
            pg.display.flip()
            clock.tick(Donnees.FPS)
        
        return niveau_selectionne, vitesse_pourcentage, reset_on_error, delai_niveau4

    @staticmethod
    def selection_monde(screen):
        """
        Affiche une fenêtre de sélection des mondes avec 4 carrés représentant :
        - Foret bleue
        - Foret violette
        - Vallée verte
        - Foret aux champignons
        
        Retourne la clé univers du monde sélectionné (str) ex: 'foret_bleue'.
        Retourne None si l'utilisateur appuie sur Échap (retour en arrière).
        """
        clock = pg.time.Clock()
        monde_selectionne = None
        monde_survole = 0  # Index du monde actuellement sélectionné au clavier (0-3)
        
        # Configuration des mondes avec leurs noms d'affichage et clés univers
        mondes = [
            {"nom": ["Forêt Bleue"], "cle": "foret_bleue", "couleur": (100, 150, 200)},
            {"nom": ["Forêt Violette"], "cle": "foret_violette", "couleur": (150, 100, 180)},
            {"nom": ["Vallée Verte"], "cle": "vallee_verte", "couleur": (100, 180, 100)},
            {"nom": ["Forêt", "Champignons"], "cle": "foret_au_champignon", "couleur": (200, 150, 100)}
        ]
        
        # Calcul de la position des carrés (2x2 grid)
        taille_carre = 150
        espacement = 50
        
        # Position de départ pour centrer la grille
        largeur_grille = 2 * taille_carre + espacement
        hauteur_grille = 2 * taille_carre + espacement
        start_x = (Donnees.WIDTH - largeur_grille) // 2
        start_y = (Donnees.HEIGHT - hauteur_grille) // 2 + 30  # Décalé vers le bas pour le titre
        
        # Créer les rectangles pour chaque monde
        rectangles_mondes = []
        for i in range(4):
            row = i // 2
            col = i % 2
            x = start_x + col * (taille_carre + espacement)
            y = start_y + row * (taille_carre + espacement)
            rectangles_mondes.append(pg.Rect(x, y, taille_carre, taille_carre))
        
        while monde_selectionne is None:
            events = pg.event.get()
            
            # Survol avec la souris
            mouse_pos = pg.mouse.get_pos()
            for i, rect in enumerate(rectangles_mondes):
                if rect.collidepoint(mouse_pos):
                    monde_survole = i
                    break
            
            # Gestion des événements
            for event in events:
                if event.type == pg.QUIT:
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return None  # Retour en arrière
                    
                    # Navigation au clavier (grille 2x2)
                    row = monde_survole // 2
                    col = monde_survole % 2
                    
                    if event.key == pg.K_LEFT:
                        col = (col - 1) % 2
                    elif event.key == pg.K_RIGHT:
                        col = (col + 1) % 2
                    elif event.key == pg.K_UP:
                        row = (row - 1) % 2
                    elif event.key == pg.K_DOWN:
                        row = (row + 1) % 2
                    elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        monde_selectionne = mondes[monde_survole]["cle"]
                        break
                    
                    monde_survole = row * 2 + col
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    position = event.pos
                    
                    # Vérifier le clic sur un des carrés de monde
                    for i, rect in enumerate(rectangles_mondes):
                        if rect.collidepoint(position):
                            monde_selectionne = mondes[i]["cle"]
                            break
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Polices
            font_titre = pg.font.Font(None, 48)
            font_monde = pg.font.Font(None, 28)
            font_info = pg.font.Font(None, 24)
            
            # Titre
            titre = font_titre.render("Sélectionnez un monde", True, Donnees.COULEUR_NOIR)
            screen.blit(titre, (Donnees.WIDTH // 2 - titre.get_width() // 2, 50))
            
            # Dessiner les carrés des mondes
            for i, (rect, monde) in enumerate(zip(rectangles_mondes, mondes)):
                # Fond du carré avec la couleur du monde
                pg.draw.rect(screen, monde["couleur"], rect)
                
                # Bordure plus épaisse si sélectionné au clavier
                epaisseur = 3
                couleur_bordure = Donnees.COULEUR_NOIR
                if i == monde_survole:
                    epaisseur = 6
                    couleur_bordure = Donnees.COULEUR_BLANC  # Bordure blanche pour mettre en valeur
                
                pg.draw.rect(screen, couleur_bordure, rect, epaisseur)
                
                # Nom du monde (centré, sur plusieurs lignes si nécessaire)
                lignes_nom = monde["nom"]
                hauteur_ligne = 30
                nb_lignes = len(lignes_nom)
                offset_y = -(nb_lignes - 1) * hauteur_ligne // 2
                
                for j, ligne in enumerate(lignes_nom):
                    texte = font_monde.render(ligne, True, Donnees.COULEUR_BLANC)
                    y_pos = rect.centery + offset_y + j * hauteur_ligne
                    texte_rect = texte.get_rect(center=(rect.centerx, y_pos))
                    screen.blit(texte, texte_rect)
            
            # Message d'information Échap
            info_text = font_info.render("Échap: retour | Flèches: navigation | Entrée: valider", True, Donnees.COULEUR_GRIS_FONCE)
            screen.blit(info_text, (Donnees.WIDTH // 2 - info_text.get_width() // 2, Donnees.HEIGHT - 40))
            
            pg.display.flip()
            clock.tick(Donnees.FPS)
        
        return monde_selectionne

    @staticmethod
    def get_chemins_monde(cle_monde):
        """
        Retourne les chemins des images de fond et de sol pour un monde donné.
        
        Args:
            cle_monde: La clé univers du monde (ex: "foret_bleue", "foret_violette", etc.)
        
        Returns:
            Un dictionnaire contenant 'fond_skin' (liste) et 'sol_skin' (str)
        """
        from BaseDonnees import Univers
        
        # Utiliser directement la clé univers
        chemin_background = Univers[cle_monde]["background"]["chemin"]
        
        # Construire les chemins complets
        sol_skin = Donnees.resource_path(chemin_background + "1.png")
        fond_skin = [Donnees.resource_path(chemin_background + f"{i}.png") for i in range(2, 8)]
        
        return {
            "sol_skin": sol_skin,
            "fond_skin": fond_skin
        }

    @staticmethod
    def fenetre_vitesse(screen, default_wpm=40, joueur=None):
        """Affiche une petite fenêtre pour saisir la vitesse (mots par minute).
        Retourne un int (10-200) ou None si annulé.
        """
        import pygame as pg
        import BaseDonnees

        min_wpm = 10
        max_wpm = 200
        # Commencer avec une zone vide (l'utilisateur tapera la valeur)
        wpm_str = ''

        # Tenter de récupérer stats joueur si fourni
        moyenne = None
        derniere = None
        try:
            if joueur is not None:
                nom_j, prenom_j = joueur
                j = BaseDonnees.get_joueur(nom_j, prenom_j)
                if j is not None:
                    try:
                        moyenne = float(j.get('Vitesse_Moyenne_WPM', 0.0))
                    except Exception:
                        moyenne = None
                    try:
                        derniere = float(j.get('Derniere_Vitesse_WPM', 0.0))
                    except Exception:
                        derniere = None
        except Exception:
            moyenne = None
            derniere = None

        clock = pg.time.Clock()
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        try:
                            val = int(wpm_str) if wpm_str != '' else int(default_wpm)
                        except Exception:
                            val = int(default_wpm)
                        val = max(min_wpm, min(max_wpm, val))
                        # Sauvegarder la dernière valeur entrée pour le joueur si fourni
                        if joueur is not None:
                            try:
                                import BaseDonnees
                                nom_j, prenom_j = joueur
                                BaseDonnees.set_derniere_vitesse(nom_j, prenom_j, val)
                                derniere = float(val)
                                print(f"Enregistré dernière vitesse {val} WPM pour {prenom_j} {nom_j}")
                            except Exception:
                                pass
                        return int(val)
                    if event.key == pg.K_ESCAPE:
                        return None
                    if event.key == pg.K_BACKSPACE:
                        wpm_str = wpm_str[:-1]
                    else:
                        ch = event.unicode
                        if ch.isdigit() and len(wpm_str) < 3:
                            if wpm_str == '0':
                                wpm_str = ch
                            else:
                                wpm_str += ch

            # Affichage simple
            screen.fill(Donnees.COULEUR_FOND)
            font_titre = pg.font.Font(None, 48)
            font_val = pg.font.Font(None, 44)
            font_info = pg.font.Font(None, 24)

            titre = font_titre.render("Réglage de la vitesse des mots", True, (0, 0, 0))
            screen.blit(titre, (Donnees.WIDTH//2 - titre.get_width()//2, 80))

            # Zone de saisie
            box_w, box_h = 240, 64
            box_rect = pg.Rect(Donnees.WIDTH//2 - box_w//2, Donnees.HEIGHT//2 - box_h//2, box_w, box_h)
            pg.draw.rect(screen, (255,255,255), box_rect)
            pg.draw.rect(screen, (0,0,0), box_rect, 2)

            # N'afficher rien si l'utilisateur n'a encore rien saisi
            display_val = wpm_str
            val_text = font_val.render(display_val, True, (0,0,0))
            screen.blit(val_text, (box_rect.x + 10, box_rect.y + box_h//2 - val_text.get_height()//2))

            label = font_info.render("mots par minutes", True, (0,0,0))
            screen.blit(label, (box_rect.right + 10, box_rect.y + box_h//2 - label.get_height()//2))

            info = font_info.render("Entrez un nombre puis Entrée (Échap pour annuler)", True, (50,50,50))
            screen.blit(info, (Donnees.WIDTH//2 - info.get_width()//2, Donnees.HEIGHT - 80))

            range_text = font_info.render(f"Plage: {min_wpm} - {max_wpm}", True, (80,80,80))
            rx = Donnees.WIDTH//2 - range_text.get_width()//2 - 120
            ry = Donnees.HEIGHT - 40
            screen.blit(range_text, (rx, ry))

            # Afficher uniquement la dernière valeur entrée (si disponible) à côté de la plage
            if derniere is not None:
                d = font_info.render(f"Dernière valeur entrée: {derniere:.0f}", True, (60,60,60))
                dx = rx + range_text.get_width() + 20
                dy = ry
                screen.blit(d, (dx, dy))

            pg.display.flip()
            clock.tick(30)

    @staticmethod
    def fenetre_menu_joueur(screen):
        """
        Affiche un menu pour choisir entre créer un nouveau joueur ou en charger un existant.
        Retourne "nouveau" ou "existant"
        """
        choix = None
        
        # Boutons
        bouton_nouveau = pg.Rect(Donnees.WIDTH // 4 - 100, Donnees.HEIGHT // 2 - 40, 200, 80)
        bouton_existant = pg.Rect(3 * Donnees.WIDTH // 4 - 100, Donnees.HEIGHT // 2 - 40, 200, 80)
        
        while choix is None:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_nouveau.collidepoint(event.pos):
                        choix = "nouveau"
                    elif bouton_existant.collidepoint(event.pos):
                        choix = "existant"
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 60)
            titre = font_titre.render("Chasse aux Mots", True, (0, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 80))
            screen.blit(titre, titre_rect)
            
            # Sous-titre
            font_sous_titre = pg.font.Font(None, 40)
            sous_titre = font_sous_titre.render("Êtes-vous un nouveau joueur?", True, (0, 0, 0))
            sous_titre_rect = sous_titre.get_rect(center=(Donnees.WIDTH // 2, 180))
            screen.blit(sous_titre, sous_titre_rect)
            
            # Bouton Nouveau joueur
            pg.draw.rect(screen, (100, 200, 100), bouton_nouveau)
            pg.draw.rect(screen, (0, 0, 0), bouton_nouveau, 3)
            texte_nouveau = font_sous_titre.render("Nouveau", True, (255, 255, 255))
            texte_nouveau_rect = texte_nouveau.get_rect(center=bouton_nouveau.center)
            screen.blit(texte_nouveau, texte_nouveau_rect)
            
            # Bouton Joueur existant
            pg.draw.rect(screen, (100, 150, 200), bouton_existant)
            pg.draw.rect(screen, (0, 0, 0), bouton_existant, 3)
            texte_existant = font_sous_titre.render("Existant", True, (255, 255, 255))
            texte_existant_rect = texte_existant.get_rect(center=bouton_existant.center)
            screen.blit(texte_existant, texte_existant_rect)
            
            pg.display.flip()
        
        return choix

    @staticmethod
    def fenetre_joueur(screen):
        """
        Affiche le menu d'entrée du nom et prénom du joueur.
        Retourne un tuple (nom, prenom) lorsque l'utilisateur valide.
        """
        
        class InputBox:
            def __init__(self, x, y, w, h, text=''):
                self.rect = pg.Rect(x, y, w, h)
                self.color = (200, 200, 200)
                self.color_active = (255, 255, 255)
                self.color_inactive = (200, 200, 200)
                self.active = False
                self.text = text
                self.txt_surface = None
                self.update_text()
            
            def handle_event(self, event):
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                
                if event.type == pg.KEYDOWN:
                    if self.active:
                        if event.key == pg.K_BACKSPACE:
                            self.text = self.text[:-1]
                        elif event.key == pg.K_SPACE:
                            self.text += ' '
                        elif len(self.text) < 20:  # Limite à 20 caractères
                            self.text += event.unicode
                        self.update_text()
            
            def update_text(self):
                font = pg.font.Font(None, 32)
                self.txt_surface = font.render(self.text if self.text else 'Entrez le texte...', True, (0, 0, 0))
            
            def draw(self, screen):
                screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 7))
                pg.draw.rect(screen, self.color, self.rect, 2)
            
            def get_text(self):
                return self.text.strip()
        
        
        # Initialisation des boîtes de saisie
        input_nom = InputBox(Donnees.WIDTH // 4, Donnees.HEIGHT // 2 - 50, 300, 40)
        input_prenom = InputBox(Donnees.WIDTH // 4, Donnees.HEIGHT // 2 + 50, 300, 40)
        
        # Bouton Valider
        bouton_valider = pg.Rect(Donnees.WIDTH // 2 - 75, Donnees.HEIGHT // 2 + 130, 150, 40)
        
        entree_complete = False
        
        while not entree_complete:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                
                input_nom.handle_event(event)
                input_prenom.handle_event(event)
                
                # Vérifier si le bouton Valider est cliqué
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_valider.collidepoint(event.pos):
                        if input_nom.get_text() and input_prenom.get_text():
                            entree_complete = True
                
                # Valider aussi avec la touche Entrée
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if input_nom.get_text() and input_prenom.get_text():
                            entree_complete = True
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 60)
            titre = font_titre.render("Bienvenue dans Chasse aux Mots!", True, (0, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 80))
            screen.blit(titre, titre_rect)
            
            # Labels
            font_label = pg.font.Font(None, 36)
            label_nom = font_label.render("Nom:", True, (0, 0, 0))
            label_prenom = font_label.render("Prénom:", True, (0, 0, 0))
            screen.blit(label_nom, (Donnees.WIDTH // 4 - 80, Donnees.HEIGHT // 2 - 50))
            screen.blit(label_prenom, (Donnees.WIDTH // 4 - 100, Donnees.HEIGHT // 2 + 50))
            
            # Boîtes de saisie
            input_nom.draw(screen)
            input_prenom.draw(screen)
            
            # Bouton Valider
            pg.draw.rect(screen, (100, 200, 100), bouton_valider)
            bouton_texte = font_label.render("Valider", True, (255, 255, 255))
            bouton_texte_rect = bouton_texte.get_rect(center=bouton_valider.center)
            screen.blit(bouton_texte, bouton_texte_rect)
            
            # Message d'erreur si champs vides
            if any(event.type == pg.MOUSEBUTTONDOWN and bouton_valider.collidepoint(event.pos) 
                   for event in events) and not (input_nom.get_text() and input_prenom.get_text()):
                message_erreur = font_label.render("Veuillez remplir tous les champs!", True, (255, 0, 0))
                screen.blit(message_erreur, (Donnees.WIDTH // 2 - 150, Donnees.HEIGHT - 70))
            
            pg.display.flip()
        
        # Retourner les données du joueur
        return input_nom.get_text(), input_prenom.get_text()

    @staticmethod
    def fenetre_charger_joueur(screen):
        """
        Affiche une liste de joueurs existants pour en sélectionner un.
        Retourne un tuple (nom, prenom) du joueur sélectionné.
        """
        import BaseDonnees
        
        joueurs_list = []
        if BaseDonnees.dict_joueurs:
            joueurs_list = [[j['nom'], j['prenom']] for j in BaseDonnees.dict_joueurs.values()]
        
        if not joueurs_list:
            # Aucun joueur enregistré, revenir au menu
            screen.fill(Donnees.COULEUR_FOND)
            font = pg.font.Font(None, 48)
            texte = font.render("Aucun joueur enregistré!", True, (0, 0, 0))
            texte_rect = texte.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
            screen.blit(texte, texte_rect)
            pg.display.flip()
            pg.time.wait(2000)
            return None
        
        selected_index = 0
        selection_complete = False
        joueur_rects = []
        escape_pressed = False
        
        while not selection_complete and not escape_pressed:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected_index = (selected_index - 1) % len(joueurs_list)
                    elif event.key == pg.K_DOWN:
                        selected_index = (selected_index + 1) % len(joueurs_list)
                    elif event.key == pg.K_RETURN:
                        selection_complete = True
                    elif event.key == pg.K_ESCAPE:
                        escape_pressed = True
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Gestion des clics sur les joueurs
                    for i, rect in enumerate(joueur_rects):
                        if rect.collidepoint(event.pos):
                            selected_index = i
                            selection_complete = True
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 60)
            titre = font_titre.render("Sélectionner un joueur", True, (0, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 50))
            screen.blit(titre, titre_rect)
            
            # Liste des joueurs
            font_joueur = pg.font.Font(None, 40)
            joueur_rects = []
            y_offset = 150
            
            for i, (nom, prenom) in enumerate(joueurs_list):
                couleur = (100, 200, 100) if i == selected_index else (200, 200, 200)
                joueur_rect = pg.Rect(Donnees.WIDTH // 4, y_offset + i * 60, Donnees.WIDTH // 2, 50)
                joueur_rects.append(joueur_rect)
                
                pg.draw.rect(screen, couleur, joueur_rect)
                pg.draw.rect(screen, (0, 0, 0), joueur_rect, 2)
                
                texte_joueur = font_joueur.render(f"{prenom} {nom}", True, (0, 0, 0))
                texte_rect = texte_joueur.get_rect(center=joueur_rect.center)
                screen.blit(texte_joueur, texte_rect)
            
            # Instructions
            font_info = pg.font.Font(None, 30)
            info = font_info.render("Haut/Bas: naviguer | Entrée: valider | Esc: retour", True, (100, 100, 100))
            screen.blit(info, (20, Donnees.HEIGHT - 50))
            
            pg.display.flip()
        
        if escape_pressed:
            return None
        
        # Retourner le joueur sélectionné
        nom, prenom = joueurs_list[selected_index]
        return nom, prenom

    @staticmethod
    def menu_selection_joueur(screen):
        """
        Gère le menu complet de sélection/création d'un joueur.
        Retourne un tuple (nom, prenom) une fois qu'un joueur valide est sélectionné.
        """
        import BaseDonnees
        import sys
        
        joueur_valide = False
        nom_joueur = None
        prenom_joueur = None
        
        while not joueur_valide:
            # Afficher le menu de choix
            choix = Menu.fenetre_menu_joueur(screen)
            
            if choix == "nouveau":
                # Créer un nouveau joueur
                while True:
                    nom, prenom = Menu.fenetre_joueur(screen)
                    succes, message = BaseDonnees.ajouter_joueur(nom, prenom)
                    
                    if succes:
                        nom_joueur = nom
                        prenom_joueur = prenom
                        joueur_valide = True
                        print(f"Bienvenue {prenom} {nom}! (Nouveau joueur créé)")
                        break
                    else:
                        # Le joueur existe déjà - afficher message et revenir au choix
                        screen.fill(Donnees.COULEUR_FOND)
                        font = pg.font.Font(None, Donnees.MENU_JOUEUR_POLICE_ERREUR)
                        font_small = pg.font.Font(None, Donnees.MENU_JOUEUR_POLICE_INFO)
                        
                        texte_erreur = font.render(message, True, Donnees.MENU_JOUEUR_COULEUR_ERREUR)
                        texte_retry = font_small.render("Appuyez sur une touche pour continuer...", True, Donnees.COULEUR_NOIR)
                        
                        screen.blit(texte_erreur, (Donnees.WIDTH // 2 - Donnees.MENU_JOUEUR_ERREUR_OFFSET_X, Donnees.HEIGHT // 2 - Donnees.MENU_JOUEUR_ERREUR_OFFSET_Y))
                        screen.blit(texte_retry, (Donnees.WIDTH // 2 - Donnees.MENU_JOUEUR_INFO_OFFSET_X, Donnees.HEIGHT // 2 + Donnees.MENU_JOUEUR_INFO_OFFSET_Y))
                        pg.display.flip()
                        
                        # Attendre une touche
                        en_attente = True
                        while en_attente:
                            for event in pg.event.get():
                                if event.type == pg.QUIT:
                                    sys.exit()
                                if event.type == pg.KEYDOWN:
                                    en_attente = False
                        break
            
            elif choix == "existant":
                # Charger un joueur existant
                result = Menu.fenetre_charger_joueur(screen)
                
                if result is not None:
                    nom_joueur, prenom_joueur = result
                    joueur_valide = True
                    print(f"Bienvenue {prenom_joueur} {nom_joueur}! (Joueur existant)")
                # else: retourner au menu de choix
        
        return nom_joueur, prenom_joueur

    @staticmethod
    def fenetre_afficher_stats_joueur(screen, nom, prenom):
        """
        Affiche les statistiques du joueur courant.
        """
        import BaseDonnees
        
        joueur = BaseDonnees.get_joueur(nom, prenom)
        
        if joueur is None:
            return
        
        # Récupérer les statistiques calculées depuis l'historique
        stats = BaseDonnees.get_statistiques_joueur(nom, prenom)
        
        if stats is None:
            return
        
        attente_stats = True
        while attente_stats:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    attente_stats = False
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, Donnees.STATS_JOUEUR_POLICE_TITRE)
            titre = font_titre.render("Profil du Joueur", True, Donnees.COULEUR_NOIR)
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, Donnees.STATS_JOUEUR_TITRE_Y))
            screen.blit(titre, titre_rect)
            
            # Infos du joueur
            font_info = pg.font.Font(None, Donnees.STATS_JOUEUR_POLICE_INFO)
            font_label = pg.font.Font(None, Donnees.STATS_JOUEUR_POLICE_LABEL)
            
            y_offset = Donnees.STATS_JOUEUR_STATS_Y
            
            # Nom et prénom
            joueur_nom = font_info.render(f"{joueur['prenom']} {joueur['nom']}", True, Donnees.STATS_JOUEUR_COULEUR_TITRE)
            screen.blit(joueur_nom, (Donnees.WIDTH // 2 - Donnees.STATS_FIN_STATS_OFFSET_X, y_offset))
            
            y_offset += Donnees.STATS_JOUEUR_LINE_HEIGHT + Donnees.STATS_JOUEUR_SECTION_SPACING
            
            # Statistiques calculées depuis l'historique
            nb_parties = stats['nb_parties']
            mots_reussis = stats['mots_reussis_total']
            vitesse_moyenne = stats['vitesse_moyenne_wpm']
            erreurs_total = stats['erreurs_total']
            
            stat_text = [
                f"Parties jouées: {nb_parties}",
                f"Mots réussis (total): {mots_reussis}",
                f"Vitesse moyenne: {vitesse_moyenne:.2f} caractères/s",
                f"Erreurs (total): {erreurs_total}"
            ]
            
            for stat in stat_text:
                texte = font_label.render(stat, True, Donnees.COULEUR_NOIR)
                screen.blit(texte, (Donnees.WIDTH // 4, y_offset))
                y_offset += Donnees.STATS_JOUEUR_LINE_HEIGHT
            
            # Message pour revenir
            info_text = font_label.render("Appuyez sur une touche pour continuer", True, Donnees.COULEUR_GRIS_MOYEN)
            info_rect = info_text.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT - Donnees.STATS_JOUEUR_INFO_MARGIN_BOTTOM))
            screen.blit(info_text, info_rect)
            
            pg.display.flip()
