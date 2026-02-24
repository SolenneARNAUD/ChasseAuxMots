import sys
import os
import pygame
import Fenetre_jeu
import Menu
import Donnees
import Mot
import BaseDonnees
import Monde


class Jeu:
    """Classe principale du jeu qui encapsule toute la logique."""
    
    def __init__(self):
        """Initialise le jeu."""
        pygame.init()
        
        # Créer le screen et la fenêtre
        self.screen = pygame.display.set_mode((Donnees.WIDTH, Donnees.HEIGHT))
        self.fenetre = Fenetre_jeu.Fenetre(Donnees.FOND_SKIN)
        # Initialiser la parallaxe dès le démarrage
        self.fenetre.initialiser_parallaxe(Donnees.FOND_SKIN)
    
    def _initialiser_variables(self):
        """Initialise/réinitialise les variables de jeu."""
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.jeu_demarre = False    # Indique si le jeu a commencé (pour démarrer le défilement)
        self.niveau = None          # Niveau sélectionné par le joueur
        self.monde = None           # Monde actuel du jeu
        self.mechant_position_saved = None  # Position du méchant sauvegardée au début du combat
        self.monde = None           # Monde actuel du jeu
        # Ne pas réinitialiser vitesse_pourcentage et reset_on_error ici pour conserver les valeurs entre les niveaux
        if not hasattr(self, 'vitesse_pourcentage'):
            self.vitesse_pourcentage = 100     # Vitesse par défaut (en %) choisie par le joueur
        if not hasattr(self, 'reset_on_error'):
            self.reset_on_error = True          # Réinitialiser le mot en cas d'erreur
        if not hasattr(self, 'total_mots'):
            self.total_mots = Donnees.TOTAL_MOTS  # Nombre de mots par partie
        if not hasattr(self, 'bibliotheque'):
            biblio_active = BaseDonnees.BIBLIOTHEQUE_ACTIVE
            # Convertir en liste si nécessaire
            if isinstance(biblio_active, str):
                self.bibliotheque = [biblio_active]
            else:
                self.bibliotheque = list(biblio_active) if biblio_active else ["dinosaure"]
        if not hasattr(self, 'personnage_joueur'):
            self.personnage_joueur = "fallen_angels_1"  # Personnage par défaut
        self.multiplier = 1.0       # Multiplicateur de vitesse basé sur le choix du joueur
        self.mechant_step = 3       # Vitesse de base du méchant, ajustée par le multiplicateur
    
    def _traiter_events_globaux(self, events):
        """Traite les événements globaux (fermeture, etc.). Retourne False si l'application doit se fermer."""
        for event in events:
            if event.type == pygame.QUIT:
                # Afficher la fenêtre de confirmation avant de quitter
                # Passer les paramètres actuels si disponibles
                pseudo = getattr(self, 'pseudo_joueur', None)
                vitesse = getattr(self, 'vitesse_pourcentage', None)
                reset = getattr(self, 'reset_on_error', None)
                
                resultat = Menu.Menu.fenetre_confirmation_quitter(self.screen, pseudo, vitesse, reset)
                
                if resultat in ['quitter', 'sauvegarder']:
                    sys.exit()
                # Si resultat == 'annuler', on ne fait rien et on continue le jeu
    
    def _appliquer_vitesse(self, vitesse_pourcentage):
        """Applique la vitesse configurée au jeu."""
        # Calcul du multiplicateur de vitesse (100% = multiplicateur de 1.0)
        try:
            self.multiplier = float(vitesse_pourcentage) / 100.0
        except Exception:
            self.multiplier = 1.0
        
        # Appliquer la vitesse du sol/mots
        Donnees.SOL_VITESSE = 0.5 * self.multiplier
        
        # Vitesse du méchant adaptée
        self.mechant_step = max(1, int(3 * self.multiplier))
    
    def _initialiser_monde(self):
        """Initialise le monde et tous ses éléments pour le niveau sélectionné."""
        self.monde = Monde.Monde(personnage_id=self.personnage_joueur)
        self.monde.initialiser_niveau(self.niveau, self.monde_choisi, self.total_mots, personnage_id=self.personnage_joueur)
        
        self.sol_gauche = self.monde.get_sol_gauche()
        self.sol_droite = self.monde.get_sol_droite()
        self.man = self.monde.get_personnage()
        self.mechant = self.monde.get_mechant()
        self.mot = self.monde.get_mot()
        self.liste_mots = self.monde.get_liste_mots()
        self.jeu_demarre = False # Le jeu commence après la première touche du joueur
        
        # Sauvegarder la position de départ du personnage pour le recul après slashing
        self.monde.set_player_depart_x(Donnees.PERSONNAGE_DEPART_X)
    
    def _gerer_game_over(self):
        """Gère l'affichage et la logique du game over."""
        # Calculer la vitesse de frappe en caractères/min
        vitesse_défaite = self.monde.calculer_vitesse_frappe()
        
        # Enregistrer l'essai complet
        BaseDonnees.enregistrer_essai(
            pseudo=self.pseudo_joueur,
            monde=self.monde_choisi,
            niveau=self.niveau,
            erreurs_detaillees=self.monde.get_erreurs_detaillees(),
            vitesse_frappe=vitesse_défaite,
            vitesse_defilement=self.vitesse_pourcentage,
            reset_mots_actif=self.reset_on_error,
            score=self.monde.get_compteur_mot(),
            caracteres_justes=self.monde.get_total_caracteres(),
            caracteres_tapes=self.monde.get_total_caracteres_tapes()
        )
        
        # Sauvegarder les paramètres actuels (vitesse, reset, personnage)
        BaseDonnees.sauvegarder_parametres_joueur(
            pseudo=self.pseudo_joueur,
            vitesse_defilement=self.vitesse_pourcentage,
            reset_mots_actif=self.reset_on_error,
            delai_niveau4=Donnees.DELAI_NIVEAU4_PAR_DEFAUT,
            personnage_id=self.personnage_joueur
        )
        
        # État de l'écran : 'gameover' ou 'stats'
        ecran_actuel = 'gameover'
        
        # Pré-générer le graphique (une seule fois) pour éviter de le régénérer à chaque frame
        graphique_surface = None
        if self.pseudo_joueur:
            graphique_path = Menu.Menu.generer_graphique_stats(self.pseudo_joueur)
            if graphique_path and os.path.exists(graphique_path):
                try:
                    graphique_surface = pygame.image.load(graphique_path)
                    # Redimensionner pour s'adapter à la zone d'affichage
                    graph_max_width = 650
                    graph_max_height = Donnees.HEIGHT - 180
                    ratio = min(graph_max_width / graphique_surface.get_width(), 
                               graph_max_height / graphique_surface.get_height())
                    new_width = int(graphique_surface.get_width() * ratio)
                    new_height = int(graphique_surface.get_height() * ratio)
                    graphique_surface = pygame.transform.smoothscale(graphique_surface, (new_width, new_height))
                except Exception as e:
                    print(f"[ERROR] Impossible de charger le graphique: {e}")
                    graphique_surface = None
        
        # Boucle de gestion des écrans
        while True:
            # Afficher l'écran approprié
            if ecran_actuel == 'gameover':
                bouton_stats = self.fenetre.afficher_game_over(self.screen)
                # Afficher les sols même en game over
                self.sol_gauche.afficher(self.screen)
                self.sol_droite.afficher(self.screen)
            else:  # écran 'stats'
                # Afficher le fond normal pour les stats
                self.fenetre.set_image(Donnees.FOND_SKIN)
                self.fenetre.afficher_fond(self.screen)
                bouton_retour = self.fenetre.afficher_stats_detaillees(
                    self.screen,
                    vitesse_défaite,
                    self.monde.get_erreurs_detaillees(),
                    self.monde.get_total_caracteres(),
                    self.monde.get_total_caracteres_tapes(),
                    graphique_surface
                )
            
            pygame.display.flip()
            
            # Gérer les événements
            events = pygame.event.get()
            self._traiter_events_globaux(events)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Réinitialiser le fond normal après le game over
                        self.fenetre.set_image(Donnees.FOND_SKIN)
                        return True  # Retourner au menu
                
                # Gestion du clic sur le bouton Statistiques (depuis game over)
                if ecran_actuel == 'gameover' and event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_stats.collidepoint(event.pos):
                        ecran_actuel = 'stats'
                        break  # Sortir de la boucle d'événements pour afficher le nouvel écran
                
                # Gestion du clic sur le bouton Retour (depuis stats)
                elif ecran_actuel == 'stats' and event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_retour.collidepoint(event.pos):
                        # Réinitialiser le fond normal après le game over
                        self.fenetre.set_image(Donnees.FOND_SKIN)
                        return True  # Retourner au menu
    
    def _gerer_niveau_reussi(self):
        """Gère l'affichage et la logique de fin de niveau réussi."""
        # Calculer les statistiques une seule fois
        if self.monde.get_vitesse_finale() is None:
            vitesse_calc = self.monde.calculer_vitesse_frappe()
            self.monde.set_vitesse_finale(vitesse_calc)
        
        # Enregistrer l'essai complet
        BaseDonnees.enregistrer_essai(
            pseudo=self.pseudo_joueur,
            monde=self.monde_choisi,
            niveau=self.niveau,
            erreurs_detaillees=self.monde.get_erreurs_detaillees(),
            vitesse_frappe=self.monde.get_vitesse_finale(),
            vitesse_defilement=self.vitesse_pourcentage,
            reset_mots_actif=self.reset_on_error,
            score=self.monde.get_compteur_mot(),
            caracteres_justes=self.monde.get_total_caracteres(),
            caracteres_tapes=self.monde.get_total_caracteres_tapes()
        )
        
        # Sauvegarder les paramètres actuels (vitesse, reset, personnage)
        BaseDonnees.sauvegarder_parametres_joueur(
            pseudo=self.pseudo_joueur,
            vitesse_defilement=self.vitesse_pourcentage,
            reset_mots_actif=self.reset_on_error,
            delai_niveau4=Donnees.DELAI_NIVEAU4_PAR_DEFAUT,
            personnage_id=self.personnage_joueur
        )
        
        # État de l'écran : 'reussite' ou 'stats'
        ecran_actuel = 'reussite'
        
        # Pré-générer le graphique (une seule fois) pour éviter de le régénérer à chaque frame
        graphique_surface = None
        if self.pseudo_joueur:
            graphique_path = Menu.Menu.generer_graphique_stats(self.pseudo_joueur)
            if graphique_path and os.path.exists(graphique_path):
                try:
                    graphique_surface = pygame.image.load(graphique_path)
                    # Redimensionner pour s'adapter à la zone d'affichage
                    graph_max_width = 650
                    graph_max_height = Donnees.HEIGHT - 180
                    ratio = min(graph_max_width / graphique_surface.get_width(), 
                               graph_max_height / graphique_surface.get_height())
                    new_width = int(graphique_surface.get_width() * ratio)
                    new_height = int(graphique_surface.get_height() * ratio)
                    graphique_surface = pygame.transform.smoothscale(graphique_surface, (new_width, new_height))
                except Exception as e:
                    print(f"[ERROR] Impossible de charger le graphique: {e}")
                    graphique_surface = None
        
        # Boucle de gestion des écrans
        while True:
            # Afficher le fond
            self.fenetre.afficher_fond(self.screen)
            self.sol_gauche.afficher(self.screen)
            self.sol_droite.afficher(self.screen)
            self.man.afficher(self.screen)
            
            # Afficher l'écran approprié
            if ecran_actuel == 'reussite':
                bouton_stats = self.fenetre.afficher_niveau_reussi(self.screen)
            else:  # écran 'stats'
                bouton_retour = self.fenetre.afficher_stats_detaillees(
                    self.screen,
                    self.monde.get_vitesse_finale(),
                    self.monde.get_erreurs_detaillees(),
                    self.monde.get_total_caracteres(),
                    self.monde.get_total_caracteres_tapes(),
                    graphique_surface
                )
            
            pygame.display.flip()
            
            # Gérer les événements
            events = pygame.event.get()
            self._traiter_events_globaux(events)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True  # Retourner au menu
                
                # Gestion du clic sur le bouton Statistiques (depuis réussite)
                if ecran_actuel == 'reussite' and event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_stats.collidepoint(event.pos):
                        ecran_actuel = 'stats'
                
                # Gestion du clic sur le bouton Retour (depuis stats)
                elif ecran_actuel == 'stats' and event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_retour.collidepoint(event.pos):
                        return True  # Retourner au menu


    def _boucle_jeu(self):
        """Boucle principale du gameplay."""
        en_pause = False
        capture_ecran = None
        
        while True:
            events = pygame.event.get()
            self._traiter_events_globaux(events) # Ex : fermeture de la fenêtre
            
            # Gestion du menu pause
            if en_pause:
                # Afficher le menu pause
                bouton_continuer, bouton_quitter = self.fenetre.afficher_menu_pause(self.screen, capture_ecran)
                pygame.display.flip()
                
                # Gérer les événements pendant la pause
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Reprendre le jeu
                            en_pause = False
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if bouton_continuer.collidepoint(event.pos):
                            # Continuer le jeu
                            en_pause = False
                        elif bouton_quitter.collidepoint(event.pos):
                            # Quitter sans sauvegarder - retour au menu
                            return True
                
                self.clock.tick(Donnees.FPS)
                continue  # Sauter le reste de la boucle pendant la pause
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    # Niveau 4 : Tab pour réafficher le mot (sans réinitialiser les lettres tapées)
                    if event.key == pygame.K_TAB and self.niveau == 4:
                        # Réafficher tout le mot (lettres tapées + non tapées)
                        self.monde.afficher_seulement_lettres_tapees = False
                        # Réinitialiser le timer pour qu'il ne disparaisse pas immédiatement
                        self.monde.temps_entree_complete = None
                        self.monde.print_disparition_affiche = False
                    
                    # Gestion de la touche Échap pour mettre en pause
                    if event.key == pygame.K_ESCAPE:
                        # Capturer l'écran actuel avant d'afficher le menu pause
                        capture_ecran = self.screen.copy()
                        en_pause = True
                        continue
                    
                    # Démarrage du jeu
                    if not self.jeu_demarre:
                        self.jeu_demarre = True
                        if self.monde.get_temps_debut() is None:
                            temps_actuel = pygame.time.get_ticks()
                            self.monde.set_temps_debut(temps_actuel)
                            # Démarrer le tracking pour le premier mot
                            self.monde.demarrer_nouveau_mot(temps_actuel)
                        
                        # Démarrer l'animation walk du personnage
                        self.monde.set_player_walking(True)
                        personnage_type = self.monde.get_personnage_type()
                        personnages_jouables = BaseDonnees.lister_personnages_jouable()
                        
                        if personnage_type in personnages_jouables:
                            animation_frames = BaseDonnees.get_animation_frames_jouable(
                                personnage_type,
                                "walking"
                            )
                            animation_delay = BaseDonnees.get_animation_delay_jouable(
                                personnage_type,
                                "walking"
                            )
                        else:
                            animation_frames = None
                            animation_delay = 5
                        
                        if animation_frames:
                            self.man.start_animation(animation_frames, animation_delay=animation_delay, loop=True)
            
            # GAME OVER : Si collision détectée (mais pas pendant le combat du personnage)
            # Ignorer la collision si le personnage est en train de combattre le méchant
            if self.man.check_collision(self.mechant) and not self.monde.get_player_move_to_enemy() and not self.monde.get_animation_in_progress():
                self.game_over = True
                # Finaliser le tracking du mot actuel en cas de collision
                self.monde.finaliser_mot_actuel(pygame.time.get_ticks())
            
            if self.game_over:
                return self._gerer_game_over()
            
            # Niveau réussi : Si tous les mots ont été complétés
            if self.monde.get_compteur_mot() >= self.monde.get_total_mots():
                return self._gerer_niveau_reussi()
            
            # Filtrer les événements Tab pour qu'ils ne soient pas traités comme des entrées de texte
            events_filtres = [e for e in events if not (e.type == pygame.KEYDOWN and e.key == pygame.K_TAB)]
            
            # Traitement des entrées clavier pour le mot
            erreur, caracteres_corrects, info_erreur = self.mot.process_input(events_filtres, reset_on_error=self.reset_on_error)
            
            # Pour le niveau 4 : démarrer le timer de disparition lors de la première frappe correcte
            if self.niveau == 4 and caracteres_corrects > 0 and self.monde.temps_entree_complete is None:
                self.monde.temps_entree_complete = pygame.time.get_ticks()
            
            # Compter tous les caractères tapés (corrects + erreurs) pour le calcul de vitesse
            total_caracteres_tapes = caracteres_corrects + erreur
            for _ in range(total_caracteres_tapes):
                self.monde.ajouter_caractere_tape()
            
            if erreur:
                self.monde.set_nb_erreurs(self.monde.get_nb_erreurs() + erreur)
                # Enregistrer l'erreur détaillée si disponible
                if info_erreur:
                    self.monde.ajouter_erreur_detaillee(
                        mot=self.mot.get_texte(),
                        lettre_attendue=info_erreur['lettre_attendue'],
                        lettre_tapee=info_erreur['lettre_tapee']
                    )
            self.monde.increment_total_caracteres(caracteres_corrects)
            
            # Vérifier si le mot vient d'être complété (animation)
            if self.monde.get_mot_state_precedent() and not self.mot._state:
                # Finaliser le tracking de frappe pour ce mot
                self.monde.finaliser_mot_actuel(pygame.time.get_ticks())
                
                self.monde.set_compteur_mot(self.monde.get_compteur_mot() + 1)
                # Nouvelles interactions : le personnage court vers le méchant au lieu que le méchant vienne
                self.monde.set_player_move_to_enemy(True)
                self.monde.set_player_running(True)
                self.monde.set_background_paused(True)
                self.monde.set_animation_in_progress(False)
                self.monde.set_delai_nouveau_mot(0)
                self.monde.set_mot_visible(False)
                
                # Sauvegarder la position du méchant pour éviter qu'il ne bouge
                self.mechant_position_saved = (self.mechant.position_x, self.mechant.position_y)
                
                # Démarrer l'animation "running" du personnage
                personnage_type = self.monde.get_personnage_type()
                personnages_jouables = BaseDonnees.lister_personnages_jouable()
                
                if personnage_type in personnages_jouables:
                    animation_frames = BaseDonnees.get_animation_frames_jouable(
                        personnage_type,
                        "running"
                    )
                    animation_delay = BaseDonnees.get_animation_delay_jouable(
                        personnage_type,
                        "running"
                    )
                else:
                    animation_frames = None
                    animation_delay = 5
                
                if animation_frames:
                    self.man.start_animation(animation_frames, animation_delay=animation_delay)
            
            # Mettre à jour l'état précédent
            self.monde.set_mot_state_precedent(self.mot._state)
            
            # Gestion du mouvement du personnage vers le méchant
            if self.monde.get_player_move_to_enemy():
                # Geler la position du méchant pendant le running et le slashing
                if self.mechant_position_saved:
                    self.mechant.position_x = self.mechant_position_saved[0]
                    self.mechant.position_y = self.mechant_position_saved[1]
                
                distance_x = self.mechant.position_x - self.man.position_x
                distance = abs(distance_x)
                
                # Continuer le running jusqu'à atteindre 200px du méchant
                if distance > 200:
                    # Toujours en train de courir - s'il n'animation n'est pas active, la relancer
                    if not self.man.is_animating():
                        personnage_type = self.monde.get_personnage_type()
                        personnages_jouables = BaseDonnees.lister_personnages_jouable()
                        
                        if personnage_type in personnages_jouables:
                            animation_frames = BaseDonnees.get_animation_frames_jouable(
                                personnage_type,
                                "running"
                            )
                            animation_delay = BaseDonnees.get_animation_delay_jouable(
                                personnage_type,
                                "running"
                            )
                        else:
                            animation_frames = None
                            animation_delay = 5
                        
                        if animation_frames:
                            self.man.start_animation(animation_frames, animation_delay=animation_delay)
                    
                    # Avancer vers le méchant
                    if distance_x > 0:
                        # Méchant à droite, se déplacer à droite
                        self.man.position_x += 6 * self.multiplier
                    else:
                        # Méchant à gauche, se déplacer à gauche
                        self.man.position_x -= 6 * self.multiplier
                    
                    # Recalculer la distance après le mouvement
                    distance_x = self.mechant.position_x - self.man.position_x
                    distance = abs(distance_x)
                
                # Vérifier après le mouvement si on doit passer au slashing
                if distance <= 200 and self.monde.get_player_move_to_enemy():
                    # Distance <= 200px - le personnage doit attaquer
                    self.monde.set_player_move_to_enemy(False)
                    self.monde.set_player_running(False)
                    self.monde.set_animation_in_progress(True)
                    
                    # Le personnage reste à sa position (200px du méchant) - pas de repositionner
                    
                    # Lancer l'animation du personnage en slashing
                    personnage_type = self.monde.get_personnage_type()
                    personnages_jouables = BaseDonnees.lister_personnages_jouable()
                    
                    if personnage_type in personnages_jouables:
                        # Utiliser les fonctions pour personnages jouables
                        animation_frames = BaseDonnees.get_animation_frames_jouable(
                            personnage_type,
                            "slashing"
                        )
                        animation_delay = BaseDonnees.get_animation_delay_jouable(
                            personnage_type,
                            "slashing"
                        )
                    else:
                        # Fallback
                        animation_frames = None
                        animation_delay = 5
                    
                    if animation_frames:
                        self.man.start_animation(animation_frames, animation_delay=animation_delay)
            
            # Gestion du déplacement du méchant vers le personnage (ancien comportement - DESACTIVÉ)
            if self.monde.get_mechant_move_to_man():
                distance_x = -self.man.position_x + self.mechant.position_x
                
                if abs(distance_x) <= self.monde.get_distance_mechant_man():
                    self.mechant.position_x = self.man.position_x + self.monde.get_distance_mechant_man()
                    self.mechant.position_y = self.man.position_y  # Aligner les pieds
                    self.monde.set_mechant_move_to_man(False)
                    self.monde.set_animation_in_progress(True)
                    
                    # Lancer l'animation du personnage
                    personnage_type = self.monde.get_personnage_type()
                    animation_name = self.monde.get_personnage_animation()
                    
                    # Déterminer si c'est un personnage jouable
                    personnages_jouables = BaseDonnees.lister_personnages_jouable()
                    
                    if personnage_type in personnages_jouables:
                        # Utiliser les fonctions pour personnages jouables
                        animation_frames = BaseDonnees.get_animation_frames_jouable(
                            personnage_type,
                            animation_name
                        )
                        animation_delay = BaseDonnees.get_animation_delay_jouable(
                            personnage_type,
                            animation_name
                        )
                    else:
                        # Utiliser les anciennes fonctions pour personnages standards
                        animation_frames = BaseDonnees.get_animation_frames(
                            personnage_type, 
                            animation_name
                        )
                        animation_delay = BaseDonnees.get_animation_delay(
                            personnage_type,
                            animation_name
                        )
                    
                    if animation_frames:
                        self.man.start_animation(animation_frames, animation_delay=animation_delay)
                else:
                    # Le méchant accélère vers le personnage - on le déplace manuellement
                    # L'animation de scrolling sera gérée plus bas pour synchroniser avec le sol
                    self.mechant.position_x -= self.mechant_step
                    self.mechant.position_y = self.man.position_y  # Aligner les pieds pendant le déplacement
                    # Mettre à jour l'animation du méchant même pendant le déplacement manuel
                    self.mechant.update_animation()
            
            # Geler la position du méchant pendant le slashing (animation)
            if self.monde.get_animation_in_progress() and not self.monde.get_mechant_move_to_man() and not self.monde.get_player_backing_away():
                if self.mechant_position_saved:
                    self.mechant.position_x = self.mechant_position_saved[0]
                    self.mechant.position_y = self.mechant_position_saved[1]
            
            # Gestion du recul du personnage après le slashing
            if self.monde.get_player_backing_away():
                depart_x = self.monde.get_player_depart_x()
                if depart_x is not None:
                    # Reculer progressivement vers la position de départ
                    distance_to_travel = self.man.position_x - depart_x
                    if abs(distance_to_travel) > 2:  # 2px de tolérance
                        if self.man.position_x > depart_x:
                            # Reculer à gauche
                            self.man.position_x -= 3
                        else:
                            # Reculer à droite
                            self.man.position_x += 3
                    else:
                        # Position de départ atteinte - créer le nouvel obstacle et mot
                        self.man.position_x = depart_x
                        self.monde.set_player_backing_away(False)
                        self.monde.set_animation_in_progress(False)
                        
                        if self.monde.get_compteur_mot() < self.monde.get_total_mots():
                            self.monde.set_num_img(1)
                            self.monde.set_frame_counter(0)
                            self.mechant = self.monde.creer_obstacle(self.monde.get_compteur_mot())
                            
                            # Créer le nouveau mot
                            self.mot = Mot.Mot.from_string(
                                Donnees.MOT_DEPART_X,
                                Donnees.MOT_DEPART_Y,
                                self.liste_mots[self.monde.get_compteur_mot()],
                                Donnees.MOT_COULEUR
                            )
                            
                            # Démarrer le tracking de frappe pour le nouveau mot
                            self.monde.demarrer_nouveau_mot(pygame.time.get_ticks())
                        
                        self.monde.set_delai_nouveau_mot(0)
                        self.monde.set_mot_visible(True)
                        
                        # Reprendre le défilement du fond et recommencer l'animation walk
                        self.monde.set_background_paused(False)
                        self.monde.set_player_move_to_enemy(False)
                        self.monde.set_player_running(False)
                        self.monde.set_player_walking(True)
                        
                        # Redémarrer l'animation walking du personnage
                        personnage_type = self.monde.get_personnage_type()
                        personnages_jouables = BaseDonnees.lister_personnages_jouable()
                        
                        if personnage_type in personnages_jouables:
                            animation_frames = BaseDonnees.get_animation_frames_jouable(
                                personnage_type,
                                "walking"
                            )
                            animation_delay = BaseDonnees.get_animation_delay_jouable(
                                personnage_type,
                                "walking"
                            )
                        else:
                            animation_frames = None
                            animation_delay = 5
                        
                        if animation_frames:
                            self.man.start_animation(animation_frames, animation_delay=animation_delay, loop=True)
            if self.monde.get_animation_in_progress() and not self.monde.get_player_backing_away():
                if not self.man.is_animating():
                    # L'animation de slashing vient de finir - faire disparaître le méchant et déclencher le recul
                    self.mechant.position_x = -500  # Placer le méchant hors de l'écran
                    
                    # Lancer l'animation running inversée pour le backing away
                    personnage_type = self.monde.get_personnage_type()
                    personnages_jouables = BaseDonnees.lister_personnages_jouable()
                    
                    if personnage_type in personnages_jouables:
                        animation_frames = BaseDonnees.get_animation_frames_jouable(
                            personnage_type,
                            "running"
                        )
                        animation_delay = BaseDonnees.get_animation_delay_jouable(
                            personnage_type,
                            "running"
                        )
                    else:
                        animation_frames = None
                        animation_delay = 5
                    
                    if animation_frames:
                        # Lancer l'animation running inversée (flip=True)
                        self.man.start_animation(animation_frames, animation_delay=animation_delay, loop=True, flip=True)
                    
                    self.monde.set_player_backing_away(True)
            
            # Mise à jour des positions (déplacement avec le sol)
            if self.jeu_demarre and not self.monde.get_background_paused():
                # Calculer la vitesse de défilement en fonction de l'état du méchant
                # Si le méchant accélère vers le personnage, tout accélère avec lui
                if self.monde.get_mechant_move_to_man():
                    vitesse_defilement = self.mechant_step
                else:
                    vitesse_defilement = Donnees.SOL_VITESSE
                
                # Faire défiler la parallaxe
                self.fenetre.defiler_parallaxe(vitesse_defilement)
                # Faire défiler le sol
                self.sol_gauche.defiler(vitesse_defilement)
                self.sol_droite.defiler(vitesse_defilement)
                self.mot.update_position(vitesse_defilement)
                
                # La mise à jour du mechant gère aussi son animation interne
                # Pendant l'accélération vers le joueur, on ne fait PAS de update_position
                # car le déplacement manuel suffit (et le sol accélère pour correspondre)
                # Aussi, le méchant ne doit pas bouger pendant le combat du personnage (running + slashing + backing away)
                if not self.monde.get_mechant_move_to_man() and not self.monde.get_player_move_to_enemy() and not self.monde.get_animation_in_progress() and not self.monde.get_player_backing_away():
                    self.mechant.update_position(vitesse_defilement)
                
                # Faire disparaître le mot immédiatement après la première frappe (niveau 4)
                if self.niveau == 4 and self.monde.temps_entree_complete is not None and not self.monde.print_disparition_affiche:
                    self.monde.faire_disparaitre_mot()
                    self.monde.print_disparition_affiche = True
            
            # Mise à jour de l'animation du personnage (même pendant la pause du fond)
            if self.jeu_demarre:
                self.man.update_animation()
            
            # Affichage des éléments
            self.fenetre.afficher_fond(self.screen)
            self.sol_gauche.afficher(self.screen)
            self.sol_droite.afficher(self.screen)
            self.man.afficher(self.screen)
            # Ne pas afficher le méchant pendant le backing away (après le slashing)
            if not self.monde.get_player_backing_away():
                self.mechant.afficher(self.screen)
            if self.monde.get_mot_visible():
                # Au niveau 4, après disparition, afficher seulement les lettres tapées
                if self.niveau == 4 and self.monde.afficher_seulement_lettres_tapees:
                    self.mot.afficher(self.screen, afficher_seulement_tapees=True)
                else:
                    self.mot.afficher(self.screen)
            self.fenetre.afficher_bandeau(
                self.screen, 
                self.niveau, 
                self.monde.get_compteur_mot(), 
                self.monde.get_total_mots()
            )
            
            # Mise à jour de l'affichage
            pygame.display.flip()
            self.clock.tick(Donnees.FPS)
    
    def run(self):
        """Lance la boucle principale du jeu."""
        
        # Boucle principale permettant de revenir à la sélection du joueur
        while True:
            # Menu d'entrée du joueur
            self.pseudo_joueur = Menu.Menu.menu_selection_joueur(self.screen)
            
            # Récupérer les derniers paramètres utilisés par le joueur
            derniers_params = BaseDonnees.get_derniers_parametres_joueur(self.pseudo_joueur)
            if derniers_params:
                # Initialiser avec les derniers paramètres du joueur
                self.vitesse_pourcentage = derniers_params['vitesse_defilement']
                self.reset_on_error = derniers_params['reset_mots_actif']
                self.personnage_joueur = derniers_params.get('personnage_id', 'fallen_angels_1')
                print(f"[INFO] Paramètres du dernier essai chargés: vitesse={self.vitesse_pourcentage}%, reset={self.reset_on_error}, personnage={self.personnage_joueur}")
            else:
                # Valeurs par défaut pour un nouveau joueur
                self.vitesse_pourcentage = 100
                self.reset_on_error = True
                self.personnage_joueur = 'fallen_angels_1'
            
            # Boucle de sélection du monde
            while True:
                # Sélection du monde
                self.monde_choisi = Menu.Menu.selection_monde(self.screen)
                
                # Si l'utilisateur a appuyé sur Échap, retourner à la sélection du joueur
                if self.monde_choisi is None:
                    break  # Sortir de la boucle monde pour retourner à la sélection du joueur
                
                # Mettre à jour les chemins d'images pour le monde sélectionné
                chemins_monde = Menu.Menu.get_chemins_monde(self.monde_choisi)
                Donnees.SOL_SKIN = chemins_monde['sol_skin']
                Donnees.FOND_SKIN = chemins_monde['fond_skin']
                self.fenetre.set_image(Donnees.FOND_SKIN)
                # Initialiser la parallaxe avec les 7 couches du fond
                self.fenetre.initialiser_parallaxe(Donnees.FOND_SKIN)
                
                # Boucle de sélection de niveau et jeu
                while True:
                    # Réinitialiser les variables
                    self._initialiser_variables()
                    
                    # Fenêtre des niveaux (et paramètres)
                    resultat = Menu.Menu.fenetre_niveau(
                        self.screen, 
                        joueur=self.pseudo_joueur,
                        vitesse_par_defaut=self.vitesse_pourcentage,
                        reset_on_error_defaut=self.reset_on_error,
                        total_mots_defaut=self.total_mots,
                        monde_choisi=self.monde_choisi,
                        bibliotheque_defaut=self.bibliotheque,
                        personnage_par_defaut=self.personnage_joueur
                    )
                    
                    # Si l'utilisateur a appuyé sur Échap, retourner à la sélection du monde
                    if resultat is None:
                        break  # Sortir de la boucle de niveau pour retourner à la sélection du monde
                    
                    self.niveau, self.vitesse_pourcentage, self.reset_on_error, self.total_mots, self.bibliotheque, self.personnage_joueur = resultat
                    
                    # Appliquer la bibliothèque sélectionnée
                    BaseDonnees.set_bibliotheque_active(self.bibliotheque)
                    
                    # Appliquer la vitesse configurée
                    self._appliquer_vitesse(self.vitesse_pourcentage)
                    
                    # Initialisation du monde
                    self._initialiser_monde()
                    
                    # Lancer la boucle de jeu
                    self._boucle_jeu()



################
##### MAIN #####
################
if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()