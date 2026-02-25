import pygame as pg
import Donnees
import unicodedata
from dataclasses import dataclass

@dataclass
class Symbole:
    """Structure simple pour représenter un caractère avec sa couleur."""
    couleur: tuple
    caractere: str

class Mot(object):
    """
    Mot composé d'objets Symbole.
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
            self._symboles = symboles
        elif isinstance(symboles, Symbole):
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
            self._symboles = value
        elif isinstance(value, Symbole):
            self._symboles = [value]
    
    @property
    def texte(self):
        """Retourne le texte complet du mot."""
        return ''.join([s.caractere for s in self._symboles])
    
    @property
    def largeur(self):
        """Retourne la largeur totale du mot en pixels."""
        font = pg.font.Font(None, Donnees.TAILLE_POLICE)
        total_width = 0
        for s in self._symboles:
            surf = font.render(s.caractere, True, (255, 255, 255))  # Couleur n'importe
            total_width += surf.get_width()
        return total_width

    def afficher(self, screen, afficher_seulement_tapees=False):
        """
        Rend chaque symbole en surface, centre horizontalement le bloc de texte
        sur self._position_x et aligne le bas du texte sur self._position_y.
        
        Args:
            screen: Surface pygame où afficher
            afficher_seulement_tapees: Si True, n'affiche que les lettres déjà tapées (grises)
        """
        font = pg.font.Font(None, Donnees.TAILLE_POLICE)
        # Pré-calculer surfaces et tailles
        surfaces = []
        symboles_a_afficher = []  # Pour tracker quels symboles afficher
        total_width = 0
        max_height = 0
        for s in self._symboles:
            ch = s.caractere
            couleur = s.couleur
            
            # Si mode "seulement tapées", ne prendre que les lettres grises
            if afficher_seulement_tapees:
                if couleur == (128, 128, 128):  # Lettre déjà tapée
                    surf = font.render(ch, True, couleur)
                    surfaces.append(surf)
                    symboles_a_afficher.append(True)
                    total_width += surf.get_width()
                    max_height = max(max_height, surf.get_height())
                else:
                    # Ne pas afficher cette lettre, mais garder l'espace
                    symboles_a_afficher.append(False)
            else:
                surf = font.render(ch, True, couleur)
                surfaces.append(surf)
                symboles_a_afficher.append(True)
                total_width += surf.get_width()
                max_height = max(max_height, surf.get_height())

        # point de départ pour centrer horizontalement (position_x = centre du mot)
        start_x = int(self._position_x) - total_width // 2
        x = start_x
        surf_idx = 0
        for idx, doit_afficher in enumerate(symboles_a_afficher):
            if doit_afficher:
                surf = surfaces[surf_idx]
                # aligner le bas de la surface sur position_y :
                y = int(self._position_y) - surf.get_height()
                screen.blit(surf, (int(x), int(y)))
                x += surf.get_width()
                surf_idx += 1

    @staticmethod
    def _conversion_symbole(chaine, couleur=None):
        """
        Convertit une chaîne en liste d'instances Symbole.
        - `chaine` : texte (str) à convertir ; les caractères seront pris tels quels.
        - `couleur` : tuple RGB ou None -> si None, on utilise Donnees.MOT_COULEUR.
        Retourne une liste d'objets Symbole.
        """
        if couleur is None:
            couleur = Donnees.MOT_COULEUR
        result = []
        for ch in str(chaine):
            result.append(Symbole(couleur, ch))
        return result

    @classmethod
    def from_string(cls, x, y, chaine, couleur=None):
        """
        Factory : crée directement une instance Mot à partir d'une chaîne.
        - x, y : positions (x = centre horizontal, y = bottom) (convention actuelle)
        - chaine : texte à transformer en symboles
        - couleur : optionnelle, couleur des symboles
        """
        symboles = cls._conversion_symbole(chaine, couleur)
        return cls(x, y, symboles)
    
    def process_input(self, events, reset_on_error=True):
        """Surveille le clavier et met a jour l'etat du mot.
        Lorsque la lettre du mot est tapee, elle devient grise.
        
        Args:
            events: Les evenements pygame
            reset_on_error: Si True, reinitialise le mot si une mauvaise lettre est tapee
        
        Returns:
            tuple: (erreur_commise, caracteres_corrects, info_erreur) 
                   - erreur_commise: 1/0 pour erreur
                   - caracteres_corrects: nombre de caractères tapés correctement
                   - info_erreur: dict avec {'lettre_attendue': str, 'lettre_tapee': str} ou None
        """
        erreur = 0
        caracteres_corrects = 0
        info_erreur = None
        
        for event in events:
            if event.type == pg.KEYDOWN:
                char = str(event.unicode).lower()
                
                # Ignorer les touches mortes (accents seuls) et les caracteres non imprimables
                if not char or char in '^`~"¨' or (ord(char) < 32 and ord(char) != 9):
                    continue
                
                if self._state and self._symboles:
                    # Trouver le premier symbole non gris
                    found = False
                    lettre_attendue = None
                    
                    for symbole in self._symboles:
                        if symbole.couleur != (128, 128, 128):
                            lettre_attendue = symbole.caractere
                            
                            # Verifier si le caractere correspond a ce symbole (avec normalisation Unicode)
                            symbole_normalized = unicodedata.normalize('NFD', symbole.caractere.lower())
                            char_normalized = unicodedata.normalize('NFD', char)
                            
                            if symbole_normalized == char_normalized:
                                symbole.couleur = (128, 128, 128)
                                found = True
                                caracteres_corrects += 1
                            break
                    
                    # Si la lettre est fausse : toujours compter l'erreur
                    if not found and lettre_attendue:
                        erreur = 1
                        info_erreur = {
                            'lettre_attendue': lettre_attendue,
                            'lettre_tapee': char
                        }
                        # Réinitialiser le mot uniquement si reset_on_error est True
                        if reset_on_error:
                            for symbole in self._symboles:
                                symbole.couleur = Donnees.MOT_COULEUR
                    
                    # Verifier si tous les symboles sont gris (mot complete)
                    if all(symbole.couleur == (128, 128, 128) for symbole in self._symboles):
                        self._state = False
        
        return erreur, caracteres_corrects, info_erreur

    def update_position(self, velocity):
        """Déplace le mot à une vitesse donnée et réinitialise s'il sort de l'écran."""
        self._position_x -= velocity
        
        # Réinitialiser la position si le mot sort de l'écran
        if self._position_x < -100:
            self._position_x = Donnees.WIDTH + 100
        
        return self._position_x