import sys, pygame
import Fenetre
import Donnees
import Personnage
import Obstacles
import Mot
import Symbole
pygame.init()

fenetre = Fenetre.Fenetre()
screen = pygame.display.set_mode(fenetre.size)


man = Personnage.Personnage(Donnees.PERSONNAGE_DEPART_X,
                            Donnees.PERSONNAGE_DEPART_Y,
                            Donnees.PERSONNAGE_SKIN)
mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_CENTIPEDE,
                              Donnees.OBSTACLE_DEPART_X,
                              Donnees.OBSTACLE_DEPART_Y,
                              Donnees.OBSTACLE_TYPE_CENTIPEDE)

# création du mot directement depuis la chaîne définie dans Donnees
mot = Mot.Mot.from_string(
    Donnees.MOT_DEPART_X,
    Donnees.MOT_DEPART_Y,
    Donnees.MOT_SYMBOLE,
    Donnees.MOT_COULEUR
)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Affichage des éléments
    screen.fill(fenetre.couleur_fond)
    man.afficher(screen)
    mechant.afficher(screen)
    mot.afficher(screen)

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(Donnees.FPS)