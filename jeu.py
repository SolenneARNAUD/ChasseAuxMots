import sys
import pygame
import Fenetre
import Donnees
import Mot
import BaseDonnees
import Monde


class Jeu:
    """Classe principale du jeu qui encapsule toute la logique."""
    
    def __init__(self):
        """Initialise le jeu et sélectionne le joueur."""
        pygame.init()
        
        # Créer le screen et la fenêtre
        self.screen = pygame.display.set_mode((Donnees.WIDTH, Donnees.HEIGHT))
        self.fenetre = Fenetre.Fenetre(Donnees.FOND_SKIN)
        
        # Menu d'entrée du joueur
        self.nom_joueur, self.prenom_joueur = Fenetre.menu_selection_joueur(self.screen)
    
    def initialiser_variables(self):
        """Initialise/réinitialise les variables de jeu."""
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.jeu_demarre = False    # Indique si le jeu a commencé (pour démarrer le défilement)
        self.niveau = None          # Niveau sélectionné par le joueur
        self.monde = None           # Monde actuel du jeu
        # Ne pas réinitialiser vitesse_pourcentage et reset_on_error ici pour conserver les valeurs entre les niveaux
        if not hasattr(self, 'vitesse_pourcentage'):
            self.vitesse_pourcentage = None     # Vitesse (en %) choisie par le joueur
        if not hasattr(self, 'reset_on_error'):
            self.reset_on_error = True          # Réinitialiser le mot en cas d'erreur
        self.multiplier = 1.0       # Multiplicateur de vitesse basé sur le choix du joueur
        self.mechant_step = 3       # Vitesse de base du méchant, ajustée par le multiplicateur
    
    def traiter_events_globaux(self, events):
        """Traite les événements globaux (fermeture, etc.). Retourne False si l'application doit se fermer."""
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
    
    def appliquer_vitesse(self, vitesse_pourcentage):
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
    
    def initialiser_monde(self):
        """Initialise le monde et tous ses éléments pour le niveau sélectionné."""
        self.monde = Monde.Monde()
        self.monde.initialiser_niveau(self.niveau)
        
        self.sol_gauche = self.monde.get_sol_gauche()
        self.sol_droite = self.monde.get_sol_droite()
        self.man = self.monde.get_personnage()
        self.mechant = self.monde.get_mechant()
        self.mot = self.monde.get_mot()
        self.liste_mots = self.monde.get_liste_mots()
        self.jeu_demarre = False # Le jeu commence après la première touche du joueur
    
    def gerer_game_over(self):
        """Gère l'affichage et la logique du game over."""
        self.fenetre.afficher_game_over(self.screen)
        pygame.display.flip()
        
        # Enregistrer les stats même en cas de défaite
        temps_fin = pygame.time.get_ticks()
        temps_total_ms = temps_fin - self.monde.get_temps_debut()
        temps_total_min = temps_total_ms / 60000.0
        vitesse_défaite = self.monde.get_compteur_mot() / temps_total_min if temps_total_min > 0 else 0
        
        BaseDonnees.update_stats_joueur(
            self.nom_joueur,
            self.prenom_joueur,
            mots_reussis=self.monde.get_compteur_mot(),
            vitesse_wpm=vitesse_défaite,
            nb_erreurs=self.monde.get_nb_erreurs()
        )
        
        # Attendre une touche pour retourner au menu
        retour_menu = False
        while not retour_menu:
            events = pygame.event.get()
            self.traiter_events_globaux(events)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    retour_menu = True
        
        # Réinitialiser le fond normal après le game over
        self.fenetre.set_image(Donnees.FOND_SKIN)
        
        return True  # Retourner au menu
    
    def gerer_niveau_reussi(self):
        """Gère l'affichage et la logique de fin de niveau réussi."""
        # Calculer les statistiques une seule fois
        if self.monde.get_vitesse_finale() is None:
            temps_fin = pygame.time.get_ticks()
            temps_total_ms = temps_fin - self.monde.get_temps_debut()
            temps_total_min = temps_total_ms / 60000.0
            vitesse_calc = self.monde.get_compteur_mot() / temps_total_min if temps_total_min > 0 else 0
            self.monde.set_vitesse_finale(vitesse_calc)
        
        self.fenetre.afficher_fond(self.screen)
        self.sol_gauche.afficher(self.screen)
        self.sol_droite.afficher(self.screen)
        self.man.afficher(self.screen)
        self.fenetre.afficher_stats_fin_niveau(
            self.screen, 
            self.monde.get_compteur_mot(), 
            self.monde.get_vitesse_finale(), 
            self.monde.get_nb_erreurs()
        )
        pygame.display.flip()
        
        # Attendre une touche pour continuer
        attente = True
        while attente:
            events = pygame.event.get()
            self.traiter_events_globaux(events)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Enregistrer les stats du joueur avant de retourner au menu
                        BaseDonnees.update_stats_joueur(
                            self.nom_joueur,
                            self.prenom_joueur,
                            mots_reussis=self.monde.get_compteur_mot(),
                            vitesse_wpm=self.monde.get_vitesse_finale(),
                            nb_erreurs=self.monde.get_nb_erreurs()
                        )
                        attente = False
        
        return True  # Retourner au menu

    def boucle_jeu(self):
        """Boucle principale du gameplay."""
        while True:
            events = pygame.event.get()
            self.traiter_events_globaux(events) # Ex : fermeture de la fenêtre
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    # Démarrage du jeu
                    self.jeu_demarre = True
                    if self.monde.get_temps_debut() is None:
                        self.monde.set_temps_debut(pygame.time.get_ticks())
            
            # GAME OVER : Si collision détectée
            if self.man.check_collision(self.mechant):
                self.game_over = True
            
            if self.game_over:
                return self.gerer_game_over()
            
            # Niveau réussi : Si tous les mots ont été complétés
            if self.monde.get_compteur_mot() >= self.monde.get_total_mots():
                return self.gerer_niveau_reussi()
            
            # Traitement des entrées clavier pour le mot
            erreur, caracteres_corrects = self.mot.process_input(events, reset_on_error=self.reset_on_error)
            if erreur:
                self.monde.set_nb_erreurs(self.monde.get_nb_erreurs() + erreur)
            self.monde.increment_total_caracteres(caracteres_corrects)
            
            # Vérifier si le mot vient d'être complété
            if self.monde.get_mot_state_precedent() and not self.mot._state:
                self.monde.set_compteur_mot(self.monde.get_compteur_mot() + 1)
                self.monde.set_mechant_move_to_man(True)
                self.monde.set_animation_in_progress(False)
                self.monde.set_delai_nouveau_mot(0)
                self.monde.set_mot_visible(False)
            
            # Mettre à jour l'état précédent
            self.monde.set_mot_state_precedent(self.mot._state)
            
            # Gestion du déplacement du méchant vers le personnage
            if self.monde.get_mechant_move_to_man():
                distance_x = -self.man.position_x + self.mechant.position_x
                
                if abs(distance_x) <= self.monde.get_distance_mechant_man():
                    self.mechant.position_x = self.man.position_x + self.monde.get_distance_mechant_man()
                    self.monde.set_mechant_move_to_man(False)
                    self.monde.set_animation_in_progress(True)
                    
                    # Lancer l'animation du personnage
                    animation_frames = BaseDonnees.get_animation_frames(
                        self.monde.get_personnage_type(), 
                        self.monde.get_personnage_animation()
                    )
                    animation_delay = BaseDonnees.get_animation_delay(
                        self.monde.get_personnage_type(), 
                        self.monde.get_personnage_animation()
                    )
                    
                    if animation_frames:
                        self.man.start_animation(animation_frames, animation_delay=animation_delay)
                else:
                    self.mechant.position_x -= self.mechant_step
            
            # Bloquer le méchant à la bonne position pendant l'animation
            if self.monde.get_animation_in_progress() and not self.monde.get_mechant_move_to_man():
                self.mechant.position_x = self.man.position_x + self.monde.get_distance_mechant_man()
            
            # Gestion du délai et du respawn après animation
            if self.monde.get_animation_in_progress():
                if not self.man.is_animating():
                    self.monde.set_delai_nouveau_mot(self.monde.get_delai_nouveau_mot() + 1)
                    
                    if self.monde.get_delai_nouveau_mot() >= 30:
                        if self.monde.get_compteur_mot() < self.monde.get_total_mots():
                            self.monde.set_num_img(1)
                            self.monde.set_frame_counter(0)
                            self.mechant = self.monde.creer_obstacle(self.monde.get_compteur_mot())
                            
                            # Créer le nouveau mot
                            self.mot = Mot.Mot.from_string(
                                Donnees.MOT_DEPART_X,
                                self.sol_gauche.get_rect().y - 100,
                                self.liste_mots[self.monde.get_compteur_mot()],
                                Donnees.MOT_COULEUR
                            )
                        
                        self.monde.set_animation_in_progress(False)
                        self.monde.set_delai_nouveau_mot(0)
                        self.monde.set_mot_visible(True)
            
            # Mise à jour des positions (déplacement avec le sol)
            if self.jeu_demarre:
                self.sol_gauche.defiler(Donnees.SOL_VITESSE)
                self.sol_droite.defiler(Donnees.SOL_VITESSE)
                self.mot.update_position(Donnees.SOL_VITESSE)
                self.mechant.update_position(Donnees.SOL_VITESSE)
                
                # Gestion de l'animation du méchant
                frame_counter = self.monde.get_frame_counter() + 1
                self.monde.set_frame_counter(frame_counter)
                
                if frame_counter >= self.mechant.animation_delay:
                    self.monde.set_frame_counter(0)
                    num_img = self.monde.get_num_img()
                    if num_img == self.mechant.nb_images:
                        self.monde.set_num_img(1)
                    else:
                        self.monde.set_num_img(num_img + 1)
                    
                    sprite_obstacle = f"{self.monde.get_obstacle_actuel_config()['chemin_base']}{self.monde.get_num_img()}.png"
                    self.mechant.set_image(sprite_obstacle)
                
                # Mise à jour de l'animation du personnage
                self.man.update_animation()
            
            # Affichage des éléments
            self.fenetre.afficher_fond(self.screen)
            self.sol_gauche.afficher(self.screen)
            self.sol_droite.afficher(self.screen)
            self.man.afficher(self.screen)
            self.mechant.afficher(self.screen)
            if self.monde.get_mot_visible():
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
        while True:
            # Réinitialiser les variables
            self.initialiser_variables()
            
            # Fenêtre des niveaux (et paramètres)
            self.niveau, self.vitesse_pourcentage, self.reset_on_error = Fenetre.fenetre_niveau(
                self.screen, 
                joueur=(self.nom_joueur, self.prenom_joueur),
                vitesse_par_defaut=self.vitesse_pourcentage,
                reset_on_error_defaut=self.reset_on_error
            )
            
            # Appliquer la vitesse configurée
            self.appliquer_vitesse(self.vitesse_pourcentage)
            
            # Initialisation du monde
            self.initialiser_monde()
            
            # Lancer la boucle de jeu
            self.boucle_jeu()



################
##### MAIN #####
################
if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()