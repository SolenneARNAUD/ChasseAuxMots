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
        font_titre = pg.font.Font(None, 60)
        titre = font_titre.render("Profil du Joueur", True, (0, 0, 0))
        titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 30))
        screen.blit(titre, titre_rect)
        
        # Infos du joueur
        font_info = pg.font.Font(None, 40)
        font_label = pg.font.Font(None, 32)
        
        y_offset = 120
        line_height = 50
        
        # Nom et prénom
        joueur_nom = font_info.render(f"{joueur['Prénom']} {joueur['Nom']}", True, (0, 100, 200))
        screen.blit(joueur_nom, (Donnees.WIDTH // 2 - 150, y_offset))
        
        y_offset += line_height + 20
        
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
            texte = font_label.render(stat, True, (0, 0, 0))
            screen.blit(texte, (Donnees.WIDTH // 4, y_offset))
            y_offset += line_height
        
        # Message pour revenir
        info_text = font_label.render("Appuyez sur une touche pour continuer", True, (100, 100, 100))
        info_rect = info_text.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT - 50))
        screen.blit(info_text, info_rect)
        
        pg.display.flip()