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
    
    def initialiser_niveau(self, niveau):
        """Initialise tous les éléments du monde pour le niveau sélectionné."""
        
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
        self.total_mots = Donnees.TOTAL_MOTS
        all_words = BaseDonnees.mots["niveau" + str(niveau)]
        self.liste_mots = random.sample(all_words, min(Donnees.TOTAL_MOTS, len(all_words)))
        
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
        """Génère une liste aléatoire d'obstacles pour le niveau."""
        obstacles_types = list(BaseDonnees.OBSTACLES_CONFIG.keys())
        self.liste_obstacles = [random.choice(obstacles_types) 
                            for _ in range(self.total_mots)]
        return self.liste_obstacles
    
    def creer_obstacle(self, index):
        """Crée un obstacle basé sur l'index dans la liste."""
        if index >= len(self.liste_obstacles):
            return None
        
        obstacle_type = self.liste_obstacles[index]
        config = BaseDonnees.OBSTACLES_CONFIG[obstacle_type]
        
        # Stocker la configuration de l'obstacle actuel
        self.obstacle_actuel_type = obstacle_type
        self.obstacle_actuel_config = config
        
        # Le premier obstacle spawn dans la fenêtre, les autres hors écran
        position_x = Donnees.OBSTACLE_DEPART_X_PREMIER if index == 0 else Donnees.OBSTACLE_DEPART_X
        
        return Obstacles.Obstacles(
            f"{config['chemin_base']}1.png",
            position_x,
            Donnees.OBSTACLE_DEPART_Y,
            config['type'],
            config['animation_delay'],
            config['nb_images']
        )
    
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
    
    def get_obstacle_actuel_config(self):
        return self.obstacle_actuel_config
    
    def get_obstacle_actuel_type(self):
        return self.obstacle_actuel_type