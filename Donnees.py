import os
import sys

def resource_path(relative_path):
    """ Calcule le chemin absolu pour les ressources (indispensable pour le .exe) """
    if hasattr(sys, '_MEIPASS'):
        # Chemin vers le dossier temporaire du .exe
        return os.path.join(sys._MEIPASS, relative_path)
    # Chemin vers le dossier habituel en développement
    return os.path.join(os.path.abspath("."), relative_path)

# Fenêtre de jeu
WIDTH, HEIGHT = 1000, 500
COULEUR_FOND = (173,216,230)  # Bleu clair
FPS = 60

# Personnage
PERSONNAGE_DEPART_X = WIDTH/6
PERSONNAGE_DEPART_Y = HEIGHT * 2/3
PERSONNAGE_SKIN = resource_path("images/Man/Viking/viking_attaque_1.png")
PERSONNAGE_HEIGHT = 120

# Obstacles
OBSTACLE_DEPART_X = WIDTH + 50  # Spawn juste à la sortie de l'écran
OBSTACLE_DEPART_X_PREMIER = WIDTH * 2/3  # Position du premier obstacle (dans la fenêtre)
OBSTACLE_DEPART_Y = HEIGHT * 2/3
OBSTACLE_SKIN_DINO = resource_path("images/Mechant/dino")
OBSTACLE_NIMAGES_DINO = 4
OBSTACLE_NIMAGES_DINO_VOLANT = 7
OBSTACLE_VIMAGES_DINO_VOLANT = 7
OBSTACLE_SKIN_DINO_VOLANT = resource_path("images/Mechant/dino_volant")
OBSTACLE_TYPE = 2  # Méchant
OBSTACLE_HEIGHT = 120

# Mots
TAILLE_POLICE = 36
MOT_DEPART_X = WIDTH + 50  # Spawn juste à la sortie de l'écran
MOT_DEPART_X_PREMIER = WIDTH * 2/3  # Position du premier mot (dans la fenêtre)
MOT_DEPART_Y = HEIGHT * 2/3 - 50
MOT_COULEUR = (255, 255, 255)
MOT_SYMBOLE = 'début'  # Exemple de mot avec des caractères spéciaux
TOTAL_MOTS = 10

# Sol
SOL_DEPART_X = WIDTH / 2
SOL_DEPART_Y = HEIGHT
SOL_SKIN = resource_path("images/Sol/Terre.png")
SOL_VITESSE = 0.5
# Fond
FOND_SKIN = resource_path("images/Fond/volcan.jpg")
FOND_GAME_OVER = resource_path("images/Fond/volcan_erruption.jpg")

# Bandeau
BANDEAU_TEXTE = "Niveau "

# Niveaux
NB_NIVEAUX = 5
NIVEAU_BOUTON_TAILLE = 100
NIVEAU_BOUTON_ESPACEMENT = 30
NIVEAU_BOUTON_COULEUR_FOND = (200, 200, 200)
NIVEAU_BOUTON_COULEUR_BORDURE = (0, 0, 0)
NIVEAU_BOUTON_EPAISSEUR_BORDURE = 3
NIVEAU_TITRE_POLICE = 48

# Paramètres de jeu
VITESSE_WPM_PAR_DEFAUT = 40  # Vitesse par défaut en mots par minute
VITESSE_WPM_MIN = 10
VITESSE_WPM_MAX = 200
VITESSE_WPM_BASE = 40.0  # Vitesse de référence pour le calcul du multiplicateur

# Couleurs interface
COULEUR_NOIR = (0, 0, 0)
COULEUR_BLANC = (255, 255, 255)
COULEUR_GRIS_FONCE = (50, 50, 50)
COULEUR_GRIS_MOYEN = (80, 80, 80)
COULEUR_GRIS_CLAIR = (100, 100, 100)
COULEUR_VERT_FONCE = (0, 100, 0)
COULEUR_ROUGE_FONCE = (100, 0, 0)
COULEUR_BLEU_BOUTON = (100, 150, 200)
