import Donnees
import pygame as pg
import sys
import BaseDonnees


class Menu:
    """Classe regroupant tous les menus du jeu."""
    
    @staticmethod
    def fenetre_parametres(screen, vitesse_actuelle, reset_on_error_actuel=True, joueur=None):
        """
        Affiche une fenêtre modale pour configurer les paramètres du jeu.
        Retourne un tuple (vitesse_pourcentage, reset_on_error) ou None si annulé.
        """
        vitesse_str = ""
        vitesse_affichee = str(vitesse_actuelle)
        reset_on_error = reset_on_error_actuel
        clock = pg.time.Clock()
        input_active = False
        
        # Zones interactives
        input_box = pg.Rect(Donnees.WIDTH // 2 - 150, Donnees.HEIGHT // 2 - 80, 300, 60)
        checkbox_rect = pg.Rect(Donnees.WIDTH // 2 - 30, Donnees.HEIGHT // 2 + 80, 40, 40)
        bouton_valider = pg.Rect(Donnees.WIDTH // 2 - 100, Donnees.HEIGHT - 120, 200, 50)
        
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    sys.exit()
                
                # Clic sur la zone de saisie
                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_active = True
                        vitesse_str = ""
                    elif checkbox_rect.collidepoint(event.pos):
                        reset_on_error = not reset_on_error
                    elif bouton_valider.collidepoint(event.pos):
                        try:
                            val = int(vitesse_str) if vitesse_str else vitesse_actuelle
                        except Exception:
                            val = vitesse_actuelle
                        val = max(Donnees.VITESSE_POURCENTAGE_MIN, min(Donnees.VITESSE_POURCENTAGE_MAX, val))
                        vitesse_affichee = str(val)
                        
                        # Sauvegarder la dernière valeur pour le joueur
                        if joueur is not None:
                            try:
                                nom_j, prenom_j = joueur
                                val_wpm = (val / 100.0) * Donnees.WPM_BASE_CONVERSION
                                BaseDonnees.set_derniere_vitesse(nom_j, prenom_j, val_wpm)
                            except Exception:
                                pass
                        
                        return (int(val), reset_on_error)
                
                if event.type == pg.KEYDOWN:
                    if input_active:
                        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                            try:
                                val = int(vitesse_str) if vitesse_str else vitesse_actuelle
                            except Exception:
                                val = vitesse_actuelle
                            val = max(Donnees.VITESSE_POURCENTAGE_MIN, min(Donnees.VITESSE_POURCENTAGE_MAX, val))
                            vitesse_affichee = str(val)
                            
                            if joueur is not None:
                                try:
                                    nom_j, prenom_j = joueur
                                    val_wpm = (val / 100.0) * Donnees.WPM_BASE_CONVERSION
                                    BaseDonnees.set_derniere_vitesse(nom_j, prenom_j, val_wpm)
                                except Exception:
                                    pass
                            
                            return (int(val), reset_on_error)
                        
                        if event.key == pg.K_ESCAPE:
                            return None
                        
                        if event.key == pg.K_BACKSPACE:
                            vitesse_str = vitesse_str[:-1]
                        elif event.unicode.isdigit() and len(vitesse_str) < 3:
                            vitesse_str += event.unicode
                    else:
                        if event.key == pg.K_ESCAPE:
                            return None
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            font_titre = pg.font.Font(None, 60)
            font_label = pg.font.Font(None, 40)
            font_input = pg.font.Font(None, 48)
            font_info = pg.font.Font(None, 28)
            
            # Titre
            titre = font_titre.render("Paramètres", True, Donnees.COULEUR_NOIR)
            screen.blit(titre, (Donnees.WIDTH // 2 - titre.get_width() // 2, 40))
            
            # Paramètre 1 : Vitesse
            label_vitesse = font_label.render("Vitesse (%)", True, Donnees.COULEUR_NOIR)
            screen.blit(label_vitesse, (Donnees.WIDTH // 2 - 250, Donnees.HEIGHT // 2 - 80))
            
            pg.draw.rect(screen, (255, 255, 255), input_box)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, input_box, 3)
            
            if input_active:
                texte_vitesse = font_input.render(vitesse_str, True, Donnees.COULEUR_NOIR)
            else:
                texte_vitesse = font_input.render(vitesse_affichee, True, (150, 150, 150))
            
            screen.blit(texte_vitesse, (input_box.centerx - texte_vitesse.get_width() // 2, 
                                        input_box.centery - texte_vitesse.get_height() // 2))
            
            # Hint pour cliquer
            if not input_active:
                hint = font_info.render("(cliquez pour modifier)", True, (180, 180, 180))
                screen.blit(hint, (input_box.centerx - hint.get_width() // 2, input_box.bottom + 10))
            
            # Paramètre 2 : Reset on Error
            label_reset = font_label.render("Réinitialiser en cas d'erreur", True, Donnees.COULEUR_NOIR)
            screen.blit(label_reset, (Donnees.WIDTH // 2 - 250, Donnees.HEIGHT // 2 + 60))
            
            # Case à cocher
            pg.draw.rect(screen, (255, 255, 255), checkbox_rect)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, checkbox_rect, 3)
            
            if reset_on_error:
                # Dessiner une croix ou un checkmark
                pg.draw.line(screen, Donnees.COULEUR_VERT_FONCE, 
                            (checkbox_rect.left + 5, checkbox_rect.top + 5),
                            (checkbox_rect.right - 5, checkbox_rect.bottom - 5), 4)
                pg.draw.line(screen, Donnees.COULEUR_VERT_FONCE,
                            (checkbox_rect.right - 5, checkbox_rect.top + 5),
                            (checkbox_rect.left + 5, checkbox_rect.bottom - 5), 4)
            
            # Bouton Valider
            pg.draw.rect(screen, (100, 200, 100), bouton_valider)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, bouton_valider, 2)
            texte_valider = font_label.render("Valider", True, (255, 255, 255))
            screen.blit(texte_valider, (bouton_valider.centerx - texte_valider.get_width() // 2,
                                       bouton_valider.centery - texte_valider.get_height() // 2))
            
            # Instructions
            info = font_info.render("Esc: Annuler", True, Donnees.COULEUR_ROUGE_FONCE)
            screen.blit(info, (Donnees.WIDTH // 2 - info.get_width() // 2, Donnees.HEIGHT - 40))
            
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
    def fenetre_niveau(screen, joueur=None, vitesse_par_defaut=None, reset_on_error_defaut=None):
        """
        Affiche la fenêtre de sélection des niveaux avec un bouton paramètres.
        Retourne un tuple (niveau_selectionne, vitesse_pourcentage, reset_on_error).
        Gère sa propre boucle jusqu'à ce qu'un niveau soit sélectionné.
        """
        clock = pg.time.Clock()
        niveau_selectionne = None
        vitesse_pourcentage = vitesse_par_defaut if vitesse_par_defaut is not None else Donnees.VITESSE_POURCENTAGE_PAR_DEFAUT
        reset_on_error = reset_on_error_defaut if reset_on_error_defaut is not None else Donnees.RESET_ON_ERROR_PAR_DEFAUT
        
        # Définir le bouton paramètres (en bas à droite)
        btn_params = pg.Rect(
            Donnees.WIDTH - Donnees.NIVEAU_BOUTON_PARAMS_WIDTH - Donnees.NIVEAU_BOUTON_PARAMS_MARGIN,
            Donnees.HEIGHT - Donnees.NIVEAU_BOUTON_PARAMS_HEIGHT - Donnees.NIVEAU_BOUTON_PARAMS_MARGIN,
            Donnees.NIVEAU_BOUTON_PARAMS_WIDTH,
            Donnees.NIVEAU_BOUTON_PARAMS_HEIGHT
        )
        
        while niveau_selectionne is None:
            events = pg.event.get()
            
            ## Gestion des événements ##
            for event in events:
                # Event 1 : Quitter le jeu
                if event.type == pg.QUIT:
                    sys.exit()
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    position = event.pos
                    
                    # Vérifier le clic sur le bouton paramètres
                    if btn_params.collidepoint(position):
                        resultat = Menu.fenetre_parametres(screen, vitesse_pourcentage, reset_on_error, joueur)
                        if resultat is not None:
                            vitesse_pourcentage, reset_on_error = resultat
                    
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
                
                # Dessin du carré
                pg.draw.rect(screen, Donnees.NIVEAU_BOUTON_COULEUR_FOND, rect)
                pg.draw.rect(screen, Donnees.NIVEAU_BOUTON_COULEUR_BORDURE, rect, Donnees.NIVEAU_BOUTON_EPAISSEUR_BORDURE)
                
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
            
            pg.display.flip()
            clock.tick(Donnees.FPS)
        
        return niveau_selectionne, vitesse_pourcentage, reset_on_error

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
        if not BaseDonnees.df_joueurs.empty:
            joueurs_list = BaseDonnees.df_joueurs[['Nom', 'Prénom']].values.tolist()
        
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
            joueur_nom = font_info.render(f"{joueur['Prénom']} {joueur['Nom']}", True, Donnees.STATS_JOUEUR_COULEUR_TITRE)
            screen.blit(joueur_nom, (Donnees.WIDTH // 2 - Donnees.STATS_FIN_STATS_OFFSET_X, y_offset))
            
            y_offset += Donnees.STATS_JOUEUR_LINE_HEIGHT + Donnees.STATS_JOUEUR_SECTION_SPACING
            
            # Statistiques
            nb_parties = int(joueur['Nb_Parties'])
            mots_reussis = int(joueur['Mots_Réussis_Total'])
            vitesse_moyenne = float(joueur['Vitesse_Moyenne_WPM'])
            erreurs_total = int(joueur['Erreurs_Total'])
            
            stat_text = [
                f"Parties jouées: {nb_parties}",
                f"Mots réussis (total): {mots_reussis}",
                f"Vitesse moyenne: {vitesse_moyenne:.2f} mots/min",
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
