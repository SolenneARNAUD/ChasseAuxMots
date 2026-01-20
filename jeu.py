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

sol_droite = Sol.Sol(Donnees.SOL_SKIN,
                     Donnees.SOL_DEPART_X + Donnees.WIDTH,
                     Donnees.SOL_DEPART_Y)

man = Personnage.Personnage(Donnees.PERSONNAGE_DEPART_X,
                            sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                            Donnees.PERSONNAGE_SKIN) # Changer position Y par WHEIGHT - 2/3 * hauteursprite
mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_CENTIPEDE,
                              Donnees.OBSTACLE_DEPART_X,
                              sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                              Donnees.OBSTACLE_TYPE_CENTIPEDE)

# création du mot directement depuis la base de donnée
compteur = 0
niveau="niveau2"
num_dino=1
liste_mots=BaseDonnees.df["niveau2"].dropna().tolist()
mot = Mot.Mot.from_string(
    Donnees.MOT_DEPART_X,
    sol_gauche.get_rect().y - 100,
    Donnees.MOT_SYMBOLE,
    Donnees.MOT_COULEUR
)


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Implémentation des mots
    if mot._state==False:
        compteur=compteur+1 
        liste_mots=BaseDonnees.df[niveau].dropna().tolist()
        mot = Mot.Mot.from_string(
                Donnees.MOT_DEPART_X,
                sol_gauche.get_rect().y - 100,
                liste_mots[compteur],
                Donnees.MOT_COULEUR)
        


    # Faire défiler le sol
    sol_gauche.defiler(Donnees.SOL_VITESSE)
    sol_droite.defiler(Donnees.SOL_VITESSE)
 
    # Affichage des éléments
    if num_dino==4:
        num_dino=1
    else:
        num_dino=num_dino+1
    
    sprite_obstacle="images/Mechant/dino"+str(num_dino)+".png"
    print(num_dino)
    mechant = Obstacles.Obstacles(sprite_obstacle,
                              Donnees.OBSTACLE_DEPART_X,
                              sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                              Donnees.OBSTACLE_TYPE_CENTIPEDE)
    
    #screen.fill(fenetre.couleur_fond)
    fenetre.afficher_fond(screen)
    sol_gauche.afficher(screen)
    sol_droite.afficher(screen)
    man.afficher(screen)
    mechant.afficher(screen)
    mot.afficher(screen)

    

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(Donnees.FPS)