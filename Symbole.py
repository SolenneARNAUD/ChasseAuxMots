class Symbole(object):
    """
    Cette classe a pour objectif d'encoder les lettres/symboles
    présent dans les mots. Les lettres/symboles doivent être 
    indépendant car elles sont tapé une par une
    """
    
    def __init__(self, couleur, symbole):
        """
        Constructeur :
        Initialise les attributs de l'objet.
        """
        self._state = True
        self._couleur = couleur
        self._symbole = symbole
    

# ---------- GETTERS / SETTERS ----------
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if (isinstance(value, bool)):
            self._state = value
            
    @property
    def couleur(self):
        return self._couleur
    @couleur.setter
    def couleur(self, value):
        if isinstance(value, tuple) and len(value) == 3:
            self._couleur = value
    
    @property
    def symbole(self):
        return self._symbole
    
    @symbole.setter
    def symbole(self, value):
        if isinstance(value, str):
            self._symbole = value





