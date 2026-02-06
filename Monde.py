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
        self.mechant = None
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
        self.personnage = Personnage.Personnage(
            Donnees.PERSONNAGE_DEPART_X,
            self.sol_gauche.get_rect().y + self.sol_gauche.get_rect().height / 4,
            Donnees.PERSONNAGE_SKIN)
        
        # Initialisation du méchant
        self.mechant = Obstacles.Obstacles(
            Donnees.OBSTACLE_SKIN_DINO_VOLANT + "1.png",
            Donnees.OBSTACLE_DEPART_X,
            self.sol_gauche.get_rect().y + self.sol_gauche.get_rect().height / 4,
            Donnees.OBSTACLE_TYPE,
            Donnees.OBSTACLE_VIMAGES_DINO_VOLANT,
            Donnees.OBSTACLE_NIMAGES_DINO_VOLANT)
        
        # Initialisation de la liste des mots
        self.total_mots = Donnees.TOTAL_MOTS
        all_words = BaseDonnees.df["niveau" + str(niveau)].dropna().tolist()
        self.liste_mots = random.sample(all_words, min(Donnees.TOTAL_MOTS, len(all_words)))
        
        # Initialisation du premier mot à afficher (positionné au-dessus du méchant)
        self.mot = Mot.Mot.from_string(
            Donnees.MOT_DEPART_X,
            self.sol_gauche.get_rect().y - 100,
            self.liste_mots[0],
            Donnees.MOT_COULEUR)
    
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
        "Renvoie la liste des mots du monde."
        return self.liste_mots
    
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