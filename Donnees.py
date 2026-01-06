
# Fenêtre de jeu
WIDTH, HEIGHT = 1000, 500
COULEUR_FOND = (0, 0, 0)
FPS = 60

# Personnage
PERSONNAGE_DEPART_X = WIDTH/3
PERSONNAGE_DEPART_Y = HEIGHT * 2/3
PERSONNAGE_SKIN = "images/Man/Man.png"

# Obstacles
OBSTACLE_DEPART_X = WIDTH * 2/3
OBSTACLE_DEPART_Y = HEIGHT * 2/3
OBSTACLE_SKIN_CENTIPEDE = "images/Centipede/Centipede.png"
OBSTACLE_TYPE_CENTIPEDE = 2  # Méchant

# Mots
TAILLE_POLICE = 36
MOT_DEPART_X = WIDTH * 2/3
MOT_DEPART_Y = HEIGHT * 2/3 - 50
MOT_COULEUR = (255, 255, 255)
MOT_SYMBOLE = 'OK'  # Exemple de mot avec des caractères spéciaux

# Sol
SOL_DEPART_X = WIDTH / 2
SOL_DEPART_Y = HEIGHT
SOL_SKIN = "images/Sol/Terre.png"