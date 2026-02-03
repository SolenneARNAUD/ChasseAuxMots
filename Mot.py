import Symbole
import pygame as pg
import Donnees
import unicodedata
import string

class Mot(object):
    """
    Mot composé d'objets Symbole.Symbole.
    Conventions :
      - position_x : centre horizontal (centre X) du mot
      - position_y : bottom (bas) du mot (coordonnée Y du bas)
    """

    def __init__(self, x, y, symboles):
        self._state = True
        self._position_x = int(x)
        self._position_y = int(y)   # bottom Y
        # normaliser symboles en liste
        if isinstance(symboles, list):
            self._symboles = [s for s in symboles if isinstance(s, Symbole.Symbole)]
        elif isinstance(symboles, Symbole.Symbole):
            self._symboles = [symboles]
        else:
            self._symboles = []

    @property
    def position_x(self):
        return self._position_x

    @position_x.setter
    def position_x(self, value):
        if isinstance(value, (int, float)):
            self._position_x = int(value)

    @property
    def position_y(self):
        "Retourne la coordonnée bottom (bas) du mot."
        return self._position_y

    @position_y.setter
    def position_y(self, value):
        if isinstance(value, (int, float)):
            self._position_y = int(value)

    @property
    def symboles(self):
        return self._symboles

    @symboles.setter
    def symboles(self, value):
        if isinstance(value, list):
            self._symboles = [s for s in value if isinstance(s, Symbole.Symbole)]
        elif isinstance(value, Symbole.Symbole):
            self._symboles = [value]

    def afficher(self, screen):
        """
        Rend chaque symbole en surface, centre horizontalement le bloc de texte
        sur self._position_x et aligne le bas du texte sur self._position_y.
        """
        font = pg.font.Font(None, Donnees.TAILLE_POLICE)
        # Pré-calculer surfaces et tailles
        surfaces = []
        total_width = 0
        max_height = 0
        for s in self._symboles:
            ch = getattr(s, "symbole", None) or getattr(s, "_symbole", "?")
            couleur = getattr(s, "couleur", None) or getattr(s, "_couleur", Donnees.MOT_COULEUR)
            surf = font.render(ch, True, couleur)
            surfaces.append(surf)
            total_width += surf.get_width()
            max_height = max(max_height, surf.get_height())

        # point de départ pour centrer horizontalement (position_x = centre du mot)
        start_x = int(self._position_x) - total_width // 2
        x = start_x
        for surf in surfaces:
            # aligner le bas de la surface sur position_y :
            y = int(self._position_y) - surf.get_height()
            screen.blit(surf, (int(x), int(y)))
            x += surf.get_width()

 
    def conversion_symbole(chaine, couleur=None):
        """
        Convertit une chaîne en liste d'instances Symbole.Symbole.
        - `chaine` : texte (str) à convertir ; les caractères seront pris tels quels.
        - `couleur` : tuple RGB ou None -> si None, on utilise Donnees.MOT_COULEUR.
        Retourne une liste d'objets Symbole.Symbole.
        """
        if couleur is None:
            couleur = Donnees.MOT_COULEUR
        result = []
        for ch in str(chaine):
            # Symbole.Symbole attend (couleur, symbole) d'après votre Symbole.py
            result.append(Symbole.Symbole(couleur, ch))
        return result

    @classmethod
    def from_string(cls, x, y, chaine, couleur=None):
        """
        Factory : crée directement une instance Mot à partir d'une chaîne.
        - x, y : positions (x = centre horizontal, y = bottom) (convention actuelle)
        - chaine : texte à transformer en symboles
        - couleur : optionnelle, couleur des symboles
        """
        symboles = cls.conversion_symbole(chaine, couleur)
        return cls(x, y, symboles)

    def process_input(self, events, reset_on_error=True):
        """Surveille le clavier et met a jour l'etat du mot.
        Lorsque la lettre du mot est tapee, elle devient grise.
        
        Args:
            events: Les evenements pygame
            reset_on_error: Si True, reinitialise le mot si une mauvaise lettre est tapee
        
        Returns:
            tuple: (erreur_commise, caracteres_corrects) - 1/0 pour erreur, nombre de caractères tapés correctement
        """
        erreur = 0
        caracteres_corrects = 0
        for event in events:
            if event.type == pg.KEYDOWN:
                char = str(event.unicode).lower()
                
                # Ignorer les touches mortes (accents seuls) et les caracteres non imprimables
                if not char or char in '^`~"¨' or (ord(char) < 32 and ord(char) != 9):
                    continue
                
                if self._state and self._symboles:
                    # Trouver le premier symbole non gris
                    found = False
                    for symbole in self._symboles:
                        if symbole._couleur != (128, 128, 128):
                            # Verifier si le caractere correspond a ce symbole (avec normalisation Unicode)
                            symbole_normalized = unicodedata.normalize('NFD', symbole._symbole.lower())
                            char_normalized = unicodedata.normalize('NFD', char)
                            
                            if symbole_normalized == char_normalized:
                                symbole._couleur = (128, 128, 128)
                                found = True
                                caracteres_corrects += 1
                            break
                    
                    # Si la lettre est fausse et reset_on_error est True
                    if not found and reset_on_error:
                        for symbole in self._symboles:
                            symbole._couleur = Donnees.MOT_COULEUR
                        erreur = 1
                    
                    # Verifier si tous les symboles sont gris (mot complete)
                    if all(symbole._couleur == (128, 128, 128) for symbole in self._symboles):
                        self._state = False
        
        return erreur, caracteres_corrects

    def update_position(self, velocity):
        """Déplace le mot à une vitesse donnée et réinitialise s'il sort de l'écran."""
        self._position_x -= velocity
        
        # Réinitialiser la position si le mot sort de l'écran
        if self._position_x < -100:
            self._position_x = Donnees.WIDTH + 100
        
        return self._position_x