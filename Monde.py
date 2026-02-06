from pygame.sprite import Sprite
import Obstacles
import Donnees
import Sol
import Personnage
import Mot
import BaseDonnees

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
        
        # Initialisation du mot
        liste_mots = BaseDonnees.df["niveau" + str(niveau)].dropna().tolist()
        self.mot = Mot.Mot.from_string(
            self.mechant.position_x + Donnees.OBSTACLE_HEIGHT / 2,
            self.sol_gauche.get_rect().y - 100,
            liste_mots[0],
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
    