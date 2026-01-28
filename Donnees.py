
# Fenêtre de jeu
WIDTH, HEIGHT = 1000, 500
COULEUR_FOND = (173,216,230)  # Bleu clair
FPS = 60

# Personnage
PERSONNAGE_DEPART_X = WIDTH/6
PERSONNAGE_DEPART_Y = HEIGHT * 2/3
PERSONNAGE_SKIN = "images/Man/Viking/viking_attaque_1.png"
PERSONNAGE_HEIGHT = 120

# Obstacles
OBSTACLE_DEPART_X = WIDTH * 2/3
OBSTACLE_DEPART_Y = HEIGHT * 2/3
OBSTACLE_SKIN_DINO = "images/Mechant/dino"
OBSTACLE_NIMAGES_DINO = 4
OBSTACLE_NIMAGES_DINO_VOLANT = 7
OBSTACLE_VIMAGES_DINO_VOLANT = 7
OBSTACLE_SKIN_DINO_VOLANT = "images/Mechant/dino_volant"
OBSTACLE_TYPE = 2  # Méchant
OBSTACLE_HEIGHT = 120

# Mots
TAILLE_POLICE = 36
MOT_DEPART_X = WIDTH * 2/3
MOT_DEPART_Y = HEIGHT * 2/3 - 50
MOT_COULEUR = (255, 255, 255)
MOT_SYMBOLE = 'début'  # Exemple de mot avec des caractères spéciaux

# Sol
SOL_DEPART_X = WIDTH / 2
SOL_DEPART_Y = HEIGHT
SOL_SKIN = "images/Sol/Terre.png"
SOL_VITESSE = 0.5
# Fond
FOND_SKIN = "images/Fond/volcan.jpg"
FOND_GAME_OVER = "images/Fond/volcan_erruption.jpg"

# Bandeau
BANDEAU_TEXTE = "Niveau "

# Niveaux
NB_NIVEAUX = 5
