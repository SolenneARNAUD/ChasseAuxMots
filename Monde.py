from pygame.sprite import Sprite
import Obstacles
import Donnees
import Sol
import Personnage
import Mot
import BaseDonnees
import random

class Monde(object):
    "Classe liant les différents éléments du décor au monde."

    def __init__(self):
        "Constructeur de la classe Monde."
        self.fond = None
        self.sol_gauche = None
        self.sol_droite = None
        self.personnage = None
        self.obstacle_actuel_type = None
        self.obstacle_actuel_config = None
        self.personnage_type = "viking"  # Type de personnage par défaut
        self.personnage_animation = "attaque"  # Animation par défaut
        self.univers = "foret_bleue"  # Univers par défaut

    
        self.mot = None
        self.total_mots = None
        self.liste_mots = None
        
        # Variables de jeu
        self.compteur_mot = 0
        self.frame_counter = 0
        self.num_img = 1
        
        self.mot_state_precedent = True
        self.mot_visible = True
        
        self.mechant_move_to_man = False
        self.animation_in_progress = False
        self.delai_nouveau_mot = 0
        self.distance_mechant_man = 150
        
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
        self.niveau = None
        self.print_disparition_affiche = False  # Pour éviter d'afficher le print plusieurs fois
        self.mot_entierement_visible = False  # Pour tracker si le mot est entièrement entré dans la fenêtre
        self.temps_entree_complete = None  # Temps où le mot est devenu entièrement visible
        self.afficher_seulement_lettres_tapees = False  # Pour n'afficher que les lettres tapées
    
    def initialiser_niveau(self, niveau, univers="foret_bleue", total_mots=None):
        """Initialise tous les éléments du monde pour le niveau sélectionné."""
        self.niveau = niveau  # Stocker le niveau actuel
        self.univers = univers  # Stocker l'univers choisi
        
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
        
        # Initialisation du personnage
        sprite_defaut = BaseDonnees.get_personnage_sprite_defaut(self.personnage_type)
        if not sprite_defaut:
            sprite_defaut = Donnees.PERSONNAGE_SKIN  # Fallback
        
        self.personnage = Personnage.Personnage(
            Donnees.PERSONNAGE_DEPART_X,
            Donnees.PERSONNAGE_DEPART_Y,
            sprite_defaut)
        
        # Initialisation de la liste des mots (AVANT initialiser_liste_obstacles)
        self.total_mots = total_mots
        all_words = BaseDonnees.mots["niveau" + str(niveau)]
        self.liste_mots = random.sample(all_words, min(total_mots, len(all_words)))
        
        # Initialiser la liste d'obstacles aléatoires
        self.liste_obstacles = self.initialiser_liste_obstacles()

        # Créer le premier obstacle
        self.mechant = self.creer_obstacle(0)  # Index 0 pour le premier
        
        # Initialisation du premier mot à afficher (positionné au-dessus du méchant)
        self.mot = Mot.Mot.from_string(
            Donnees.MOT_DEPART_X_PREMIER,  # Le premier mot spawn dans la fenêtre
            Donnees.MOT_DEPART_Y,
            self.liste_mots[0],
            Donnees.MOT_COULEUR)
        
    def initialiser_liste_obstacles(self):
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
                self.obstacle_actuel_type = obstacle_type
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
            self.obstacle_actuel_type = obstacle_type
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
    
    # Getter et Setter
    def get_sol_gauche(self):
        "Renvoie le sol gauche du monde."
        return self.sol_gauche
    
    def get_sol_droite(self):
        "Renvoie le sol droite du monde."
        return self.sol_droite
    
    def get_personnage(self):
        "Renvoie le personnage du monde."
        return self.personnage
    
    def get_mechant(self):
        "Renvoie le méchant du monde."
        return self.mechant
    
    def get_mot(self):
        "Renvoie le mot du monde."
        return self.mot
    
    def get_liste_mots(self):
        "Renvoie la liste des mots du niveau."
        return self.liste_mots
    
    def get_liste_mots(self):
        "Renvoie la liste des mots du monde."
        return self.liste_mots
    
    def get_personnage_type(self):
        "Renvoie le type de personnage actuel."
        return self.personnage_type
    
    def set_personnage_type(self, type):
        "Définit le type de personnage."
        self.personnage_type = type
    
    def get_personnage_animation(self):
        "Renvoie le nom de l'animation du personnage."
        return self.personnage_animation
    
    def set_personnage_animation(self, animation):
        "Définit l'animation du personnage."
        self.personnage_animation = animation
    
    # Getters et setters pour les variables de jeu
    def get_compteur_mot(self):
        return self.compteur_mot
    
    def set_compteur_mot(self, value):
        self.compteur_mot = value
    
    def get_total_mots(self):
        return self.total_mots
    
    def get_frame_counter(self):
        return self.frame_counter
    
    def set_frame_counter(self, value):
        self.frame_counter = value
    
    def get_num_img(self):
        return self.num_img
    
    def set_num_img(self, value):
        self.num_img = value
    
    def get_mot_state_precedent(self):
        return self.mot_state_precedent
    
    def set_mot_state_precedent(self, value):
        self.mot_state_precedent = value
    
    def get_mot_visible(self):
        return self.mot_visible
    
    def set_mot_visible(self, value):
        self.mot_visible = value
    
    def get_mechant_move_to_man(self):
        return self.mechant_move_to_man
    
    def set_mechant_move_to_man(self, value):
        self.mechant_move_to_man = value
    
    def get_animation_in_progress(self):
        return self.animation_in_progress
    
    def set_animation_in_progress(self, value):
        self.animation_in_progress = value
    
    def get_delai_nouveau_mot(self):
        return self.delai_nouveau_mot
    
    def set_delai_nouveau_mot(self, value):
        self.delai_nouveau_mot = value
    
    def get_distance_mechant_man(self):
        return self.distance_mechant_man
    
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
    
    def set_total_caracteres(self, value):
        self.total_caracteres = value
    
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
        self.print_disparition_affiche = False  # Réinitialiser pour le nouveau mot
        self.mot_entierement_visible = False  # Réinitialiser le flag de visibilité
        self.temps_entree_complete = None  # Réinitialiser le temps d'entrée complète
        self.afficher_seulement_lettres_tapees = False  # Réinitialiser le mode d'affichage
    
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
    
    def get_obstacle_actuel_config(self):
        return self.obstacle_actuel_config
    
    def get_obstacle_actuel_type(self):
        return self.obstacle_actuel_type
    
    def faire_disparaitre_mot(self):
        """Fait disparaître le mot de l'écran (pour le niveau 4)."""
        # Ne pas cacher complètement, mais activer le mode "seulement lettres tapées"
        self.afficher_seulement_lettres_tapees = True