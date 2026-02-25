import Obstacles
import Donnees
import Sol
import Personnage
import Mot
import BaseDonnees
import random

class Monde(object):
    "Classe liant les différents éléments du décor au monde."

    def __init__(self, personnage_id="fallen_angels_1"):
        """Constructeur de la classe Monde.
        
        Args:
            personnage_id: ID du personnage jouable à utiliser (ex: 'fallen_angels_1')
        """
        self.sol_gauche = None
        self.sol_droite = None
        self.personnage = None
        self.obstacle_actuel_config = None
        self.personnage_type = personnage_id
        self.univers = "foret_bleue"
        
        self.mot = None
        self.total_mots = None
        self.liste_mots = None
        
        # Variables de jeu
        self.compteur_mot = 0
        self.mot_state_precedent = True
        self.mot_visible = True
        self.animation_in_progress = False
        
        # Variables pour l'animation du personnage jouable
        self.player_walking = False  # Le personnage fait l'animation walk
        self.player_running = False  # Le personnage fait l'animation run
        self.player_move_to_enemy = False  # Le personnage se déplace vers le méchant
        self.background_paused = False  # Le fond/sol est en pause
        self.player_backing_away = False  # Le personnage recule après le slashing
        self.player_depart_x = None  # Position de départ du personnage (pour le recul)
        
        self.nb_erreurs = 0
        self.erreurs_detaillees = []  # Liste des erreurs avec détails: {'mot': str, 'lettre_attendue': str, 'lettre_tapee': str}
        self.temps_debut = None
        self.total_caracteres = 0
        self.vitesse_finale = None
        
        # Tracking pour le calcul de la vitesse de frappe précise (caractères/min)
        self.temps_apparition_mot = None  # Temps d'apparition du mot actuel
        self.caracteres_tapes_mot_actuel = 0  # Nombre de caractères tapés pour le mot actuel
        self.donnees_frappe = []  # Liste des données de frappe: {'temps_frappe': ms, 'caracteres_tapes': int}
        
        # Variables pour le niveau 4
        self.print_disparition_affiche = False  # Pour éviter d'afficher le print plusieurs fois
        self.temps_entree_complete = None  # Temps où le mot est devenu entièrement visible
        self.afficher_seulement_lettres_tapees = False  # Pour n'afficher que les lettres tapées
    
    def initialiser_niveau(self, niveau, univers="foret_bleue", total_mots=None, personnage_id=None):
        """Initialise tous les éléments du monde pour le niveau sélectionné.
        
        Args:
            niveau: Numéro du niveau (1-5)
            univers: ID de l'univers (ex: 'foret_bleue')
            total_mots: Nombre total de mots pour ce niveau
            personnage_id: ID du personnage jouable à utiliser
        """
        self.univers = univers  # Stocker l'univers choisi
        
        # Mettre à jour le personnage si fourni
        if personnage_id:
            self.personnage_type = personnage_id
        
        # Utiliser le total_mots passé en paramètre ou la valeur par défaut
        if total_mots is None:
            total_mots = Donnees.TOTAL_MOTS
        
        # Initialisation des sols
        self.sol_gauche = Sol.Sol(Donnees.SOL_SKIN,
                                  Donnees.SOL_DEPART_X,
                                  Donnees.SOL_DEPART_Y)
        
        self.sol_droite = Sol.Sol(Donnees.SOL_SKIN,
                                  Donnees.SOL_DEPART_X + Donnees.WIDTH,
                                  Donnees.SOL_DEPART_Y)
        
        # Initialisation du personnage avec le sprite du personnage sélectionné
        sprite_defaut = BaseDonnees.get_personnage_sprite_defaut_jouable(self.personnage_type)
        if not sprite_defaut:
            sprite_defaut = Donnees.PERSONNAGE_SKIN  # Fallback
        
        self.personnage = Personnage.Personnage(
            Donnees.PERSONNAGE_DEPART_X,
            Donnees.PERSONNAGE_DEPART_Y,
            sprite_defaut)
        
        # Initialisation de la liste des mots (AVANT initialiser_liste_obstacles)
        all_words = BaseDonnees.mots["niveau" + str(niveau)]
        nb_mots_disponibles = len(all_words)
        
        # Vérifier qu'il y a au moins 1 mot disponible
        if nb_mots_disponibles < 1:
            raise ValueError(f"La bibliothèque sélectionnée ne contient aucun mot pour le niveau {niveau}. Veuillez sélectionner une autre bibliothèque ou ajouter des mots.")
        
        # Ajuster le nombre de mots demandés si nécessaire
        self.total_mots = min(total_mots, nb_mots_disponibles)
        if self.total_mots < total_mots:
            print(f"[WARNING] Bibliothèque insuffisante : {nb_mots_disponibles} mots disponibles, {total_mots} demandés. Ajusté à {self.total_mots} mots.")
        
        self.liste_mots = random.sample(all_words, self.total_mots)
        
        # Initialiser la liste d'obstacles aléatoires
        self.liste_obstacles = self._initialiser_liste_obstacles()

        # Créer le premier obstacle
        self.mechant = self.creer_obstacle(0)  # Index 0 pour le premier
        
        # Initialisation du premier mot à afficher (positionné au-dessus du méchant)
        self.mot = Mot.Mot.from_string(
            Donnees.MOT_DEPART_X_PREMIER,  # Le premier mot spawn dans la fenêtre
            Donnees.MOT_DEPART_Y,
            self.liste_mots[0],
            Donnees.MOT_COULEUR)
        
    def _initialiser_liste_obstacles(self):
        """Génère une liste aléatoire de méchants de l'univers pour le niveau."""
        # Récupérer la liste des méchants disponibles dans l'univers
        mechants_disponibles = BaseDonnees.get_mechants_univers(self.univers)
        
        if not mechants_disponibles:
            # Fallback vers ancienne config si univers invalide
            obstacles_types = list(BaseDonnees.OBSTACLES_CONFIG.keys())
            self.liste_obstacles = [random.choice(obstacles_types) 
                                for _ in range(self.total_mots)]
        else:
            # Utiliser les méchants de l'univers
            self.liste_obstacles = [random.choice(mechants_disponibles) 
                                for _ in range(self.total_mots)]
        
        return self.liste_obstacles
    
    def creer_obstacle(self, index):
        """Crée un obstacle (méchant) basé sur l'index dans la liste."""
        if index >= len(self.liste_obstacles):
            return None
        
        obstacle_type = self.liste_obstacles[index]
        
        # Utiliser la position_y du personnage pour aligner les pieds
        position_y = self.personnage.position_y if self.personnage else Donnees.OBSTACLE_DEPART_Y
        
        # Essayer de charger avec la configuration d'univers
        mechants_disponibles = BaseDonnees.get_mechants_univers(self.univers)
        
        if mechants_disponibles and obstacle_type in mechants_disponibles:
            # Charger depuis l'univers
            config = BaseDonnees.get_mechant_config(self.univers, obstacle_type)
            
            if config and 'frames' in config:
                # Stocker la configuration de l'obstacle actuel
                self.obstacle_actuel_config = config
                
                # Le premier obstacle spawn dans la fenêtre, les autres hors écran
                position_x = Donnees.OBSTACLE_DEPART_X_PREMIER if index == 0 else Donnees.OBSTACLE_DEPART_X
                
                # Créer l'obstacle avec les frames d'animation et l'offset global
                return Obstacles.Obstacles(
                    config['frames'][0],  # Utiliser la première frame
                    position_x,
                    position_y,  # Utiliser la position_y du personnage
                    config['type'],
                    config['animation_delay'],
                    config['nb_images'],
                    animation_frames=config['frames'],  # Passer les frames d'animation
                    foot_offset=Donnees.MECHANT_FOOT_OFFSET  # Utiliser l'offset global
                )
        
        # Fallback vers ancienne config
        if obstacle_type in BaseDonnees.OBSTACLES_CONFIG:
            config = BaseDonnees.OBSTACLES_CONFIG[obstacle_type]
            
            # Stocker la configuration de l'obstacle actuel
            self.obstacle_actuel_config = config
            
            # Le premier obstacle spawn dans la fenêtre, les autres hors écran
            position_x = Donnees.OBSTACLE_DEPART_X_PREMIER if index == 0 else Donnees.OBSTACLE_DEPART_X
            
            return Obstacles.Obstacles(
                f"{config['chemin_base']}1.png",
                position_x,
                position_y,  # Utiliser la position_y du personnage
                config['type'],
                config['animation_delay'],
                config['nb_images'],
                foot_offset=Donnees.MECHANT_FOOT_OFFSET  # Utiliser l'offset global
            )
        
        return None
    
    # ========== Properties (accès pythonic aux attributs) ==========
    # Note: Les anciennes méthodes get_xxx/set_xxx sont conservées ci-dessous
    # pour compatibilité, mais les properties sont l'approche recommandée
    
    # Getters/setters classiques (conservés pour compatibilité)
    def get_sol_gauche(self):
        """Renvoie le sol gauche du monde."""
        return self.sol_gauche
    
    def get_sol_droite(self):
        """Renvoie le sol droite du monde."""
        return self.sol_droite
    
    def get_personnage(self):
        """Renvoie le personnage du monde."""
        return self.personnage
    
    def get_mechant(self):
        """Renvoie le méchant du monde."""
        return self.mechant
    
    def get_mot(self):
        """Renvoie le mot du monde."""
        return self.mot
    
    def get_liste_mots(self):
        """Renvoie la liste des mots du niveau."""
        return self.liste_mots
    
    def get_personnage_type(self):
        """Renvoie le type de personnage actuel."""
        return self.personnage_type
    
    def get_compteur_mot(self):
        return self.compteur_mot
    
    def set_compteur_mot(self, value):
        self.compteur_mot = value
    
    def get_total_mots(self):
        return self.total_mots
    
    def get_mot_state_precedent(self):
        return self.mot_state_precedent
    
    def set_mot_state_precedent(self, value):
        self.mot_state_precedent = value
    
    def get_mot_visible(self):
        return self.mot_visible
    
    def set_mot_visible(self, value):
        self.mot_visible = value
    
    def get_animation_in_progress(self):
        return self.animation_in_progress
    
    def set_animation_in_progress(self, value):
        self.animation_in_progress = value
    
    def get_nb_erreurs(self):
        return self.nb_erreurs
    
    def set_nb_erreurs(self, value):
        self.nb_erreurs = value
    
    def get_erreurs_detaillees(self):
        return self.erreurs_detaillees
    
    def ajouter_erreur_detaillee(self, mot, lettre_attendue, lettre_tapee):
        """Ajoute une erreur détaillée à la liste."""
        self.erreurs_detaillees.append({
            'mot': mot,
            'lettre_attendue': lettre_attendue,
            'lettre_tapee': lettre_tapee
        })
    
    def get_temps_debut(self):
        return self.temps_debut
    
    def set_temps_debut(self, value):
        self.temps_debut = value
    
    def get_total_caracteres(self):
        return self.total_caracteres
    
    def increment_total_caracteres(self, amount):
        self.total_caracteres += amount
    
    def get_vitesse_finale(self):
        return self.vitesse_finale
    
    def set_vitesse_finale(self, value):
        self.vitesse_finale = value
    
    # Méthodes pour le tracking de frappe précis
    def demarrer_nouveau_mot(self, temps_actuel):
        """Démarre le tracking pour un nouveau mot."""
        import pygame
        self.temps_apparition_mot = temps_actuel if temps_actuel else pygame.time.get_ticks()
        self.caracteres_tapes_mot_actuel = 0
        self.print_disparition_affiche = False
        self.temps_entree_complete = None
        self.afficher_seulement_lettres_tapees = False
    
    def ajouter_caractere_tape(self):
        """Incrémente le compteur de caractères tapés pour le mot actuel."""
        self.caracteres_tapes_mot_actuel += 1
    
    def finaliser_mot_actuel(self, temps_actuel):
        """Enregistre les données de frappe du mot actuel et réinitialise."""
        import pygame
        if self.temps_apparition_mot is not None:
            temps_fin = temps_actuel if temps_actuel else pygame.time.get_ticks()
            temps_frappe = temps_fin - self.temps_apparition_mot
            self.donnees_frappe.append({
                'temps_frappe': temps_frappe,
                'caracteres_tapes': self.caracteres_tapes_mot_actuel
            })
            self.temps_apparition_mot = None
            self.caracteres_tapes_mot_actuel = 0
    
    def calculer_vitesse_frappe(self):
        """Calcule la vitesse de frappe en caractères par seconde."""
        if not self.donnees_frappe:
            return 0.0
        
        temps_total_ms = sum(d['temps_frappe'] for d in self.donnees_frappe)
        caracteres_total = sum(d['caracteres_tapes'] for d in self.donnees_frappe)
        
        if temps_total_ms == 0:
            return 0.0
        
        # Convertir en caractères par seconde
        temps_total_s = temps_total_ms / 1000.0
        vitesse = caracteres_total / temps_total_s if temps_total_s > 0 else 0.0
        
        return vitesse
    
    def get_total_caracteres_tapes(self):
        """Retourne le nombre total de caractères tapés (corrects + erreurs)."""
        return sum(d['caracteres_tapes'] for d in self.donnees_frappe)
    
    # Getters et Setters pour l'animation du personnage jouable
    
    def set_player_walking(self, value):
        self.player_walking = value
    
    def set_player_running(self, value):
        self.player_running = value
    
    def get_player_move_to_enemy(self):
        return self.player_move_to_enemy
    
    def set_player_move_to_enemy(self, value):
        self.player_move_to_enemy = value
    
    def get_background_paused(self):
        return self.background_paused
    
    def set_background_paused(self, value):
        self.background_paused = value
    
    def get_player_backing_away(self):
        return self.player_backing_away
    
    def set_player_backing_away(self, value):
        self.player_backing_away = value
    
    def get_player_depart_x(self):
        return self.player_depart_x
    
    def set_player_depart_x(self, value):
        self.player_depart_x = value
    
    def faire_disparaitre_mot(self):
        """Fait disparaître le mot de l'écran (pour le niveau 4)."""
        # Ne pas cacher complètement, mais activer le mode "seulement lettres tapées"
        self.afficher_seulement_lettres_tapees = True