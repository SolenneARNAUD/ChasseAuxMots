import sys, pygame
import Fenetre
import Donnees
import Personnage
import Obstacles
import Mot
import Symbole
import Sol  
import BaseDonnees
pygame.init()

# Créer le screen AVANT la fenêtre (nécessaire pour .convert())
screen = pygame.display.set_mode((Donnees.WIDTH, Donnees.HEIGHT))
fenetre = Fenetre.Fenetre(Donnees.FOND_SKIN)

sol_gauche = Sol.Sol(Donnees.SOL_SKIN,
                    Donnees.SOL_DEPART_X,
                    Donnees.SOL_DEPART_Y)

man = Personnage.Personnage(Donnees.PERSONNAGE_DEPART_X,
                            sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                            Donnees.PERSONNAGE_SKIN) # Changer position Y par WHEIGHT - 2/3 * hauteursprite
mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_CENTIPEDE,
                              Donnees.OBSTACLE_DEPART_X,
                              sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                              Donnees.OBSTACLE_TYPE_CENTIPEDE)

# création du mot directement depuis la chaîne définie dans Donnees
mot = Mot.Mot.from_string(
    Donnees.MOT_DEPART_X,
    sol_gauche.get_rect().y - 30,
    Donnees.MOT_SYMBOLE,
    Donnees.MOT_COULEUR
)


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Implémentation des mots
    if mot._state==False:
       compteur=1 #compteur ++
       #bd(niveau[compteur] devient le nouveau mot -> utiliser la méthode from_string



        

    # Affichage des éléments
    
    #screen.fill(fenetre.couleur_fond)
    fenetre.afficher_fond(screen)
    sol_gauche.afficher(screen)
    man.afficher(screen)
    mechant.afficher(screen)
    mot.afficher(screen)
    

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(Donnees.FPS)