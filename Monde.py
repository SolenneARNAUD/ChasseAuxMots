from pygame.sprite import Sprite
import Obstacles

class Monde(object):
    "Classe liant les différents éléments du décor au monde."

    def __init__(self, fond, sol, obstacles):
        "Constructeur de la classe Monde."
        # Initialisation des attributs
        self.fond = fond
        self.sol = sol
        self.obstacles = obstacles
    
    # Getter et Setter
    def get_fond(self):
        "Renvoie le fond du monde."
        return self.fond
    def set_fond(self, fond):
        "Modifie le fond du monde."
        if fond is Sprite:
            self.fond = fond
    
    def get_sol(self):
        "Renvoie le sol du monde."
        return self.sol
    def set_sol(self, sol):
        "Modifie le sol du monde."
        if sol is Sprite:
            self.sol = sol
    
    def get_obstacles(self):
        "Renvoie les obstacles du monde."
        return self.obstacles
    def set_obstacles(self, obstacles):
        "Modifie les obstacles du monde."
        if (isinstance(elem, Obstacles) for elem in obstacles):
            self.obstacles = obstacles