import Donnees

class Fenetre(object):
    "Classe correspondant à la fenêtre de jeu."

    def __init__(self):
        "Constructeur de la classe Fenetre."
        # Initialisation des attributs
        self.size = (Donnees.WIDTH, Donnees.HEIGHT)
        self.couleur_fond = Donnees.COULEUR_FOND