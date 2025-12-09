import Symbole


class Mot(object):
    """
    Cette classe a pour objectif d'encoder les mots qui sont composer 
    d'objets de la classe Symbole
    """
    
    def __init__(self, x, y, symboles):
        """
        Constructeur :
        Initialise les attributs de l'objet.
        """
        self.state = True
        self.position_x = x
        self.position_y = y
        self.symboles = symboles
    

# ---------- GETTERS / SETTERS ----------
    @property
    def state(self):
        return self.state

    @state.setter
    def state(self, value):
        if (isinstance(value, bool)):
            self.state = value
            
    @property
    def position_x(self):
        return self.position_x

    @position_x.setter
    def position_x(self, value):
        if (isinstance(value, int)):
            self.position_x = value

    @property
    def position_y(self):
        return self.position_y

    @position_y.setter
    def positiposition_yon_x(self, value):
        if (isinstance(value, int)):
            self.position_y = value
    
    @property
    def symbole(self):
        return self.symbole

    @symboles.setter
    def symboles(self, value):
        if (isinstance(value, list)):
            if(isinstance(elem, Symbole) for elem in value):
                self.symbole = value




