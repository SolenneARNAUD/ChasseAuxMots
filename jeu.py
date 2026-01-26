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

# Initialisation des sols
sol_gauche = Sol.Sol(Donnees.SOL_SKIN,
                    Donnees.SOL_DEPART_X,
                    Donnees.SOL_DEPART_Y)

sol_droite = Sol.Sol(Donnees.SOL_SKIN,
                     Donnees.SOL_DEPART_X + Donnees.WIDTH,
                     Donnees.SOL_DEPART_Y)

# Initialisation du personnage
man = Personnage.Personnage(Donnees.PERSONNAGE_DEPART_X,
                            sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                            Donnees.PERSONNAGE_SKIN)

# Initialisation du méchant
mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_DINO_VOLANT,
                              Donnees.OBSTACLE_DEPART_X,
                              sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                              Donnees.OBSTACLE_TYPE,
                              Donnees.OBSTACLE_VIMAGES_DINO_VOLANT,
                              Donnees.OBSTACLE_NIMAGES_DINO_VOLANT)

# Initialisation des mots
compteur_mot = 0
niveau = "niveau2"
num_img = 1
frame_counter = 0
liste_mots = BaseDonnees.df["niveau2"].dropna().tolist()
mot = Mot.Mot.from_string(
    Donnees.MOT_DEPART_X,
    sol_gauche.get_rect().y - 100,
    Donnees.MOT_SYMBOLE,
    Donnees.MOT_COULEUR
)

#################### Boucle principale ########################

clock = pygame.time.Clock()
game_over = False

while True:
    events = pygame.event.get()          
    for event in events:
        if event.type == pygame.QUIT: 
            sys.exit()

    # Si collision détectée, afficher écran noir et arrêter le jeu
    if man.check_collision(mechant):
        game_over = True

    if game_over:
        screen.fill((0, 0, 0))  # Remplir l'écran en noir
        pygame.display.flip()
        clock.tick(Donnees.FPS)
        continue

    # Traitement des entrées clavier pour le mot
    mot.process_input(events)

    # Génération d'un nouveau mot et respawn du méchant si le mot actuel est complété
    if not mot._state:
        compteur_mot += 1 
        liste_mots = BaseDonnees.df[niveau].dropna().tolist()
        mot = Mot.Mot.from_string(
            Donnees.MOT_DEPART_X,
            sol_gauche.get_rect().y - 100,
            liste_mots[compteur_mot],
            Donnees.MOT_COULEUR)
        
        # Respawn du méchant
        num_img = 1
        frame_counter = 0

        print('avant chargement')
        mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_DINO_VOLANT + str(num_img) + ".png",
                                      Donnees.OBSTACLE_DEPART_X,
                                      sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                                      Donnees.OBSTACLE_TYPE,
                                      Donnees.OBSTACLE_VIMAGES_DINO_VOLANT,
                                      Donnees.OBSTACLE_NIMAGES_DINO_VOLANT)
        print('apres chargement')

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Il faut ajouter des temps mort entre les frame de sol pour qu'il defile a une vitesse correcte
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # Mise à jour des positions (déplacement avec le sol)
    sol_gauche.defiler(Donnees.SOL_VITESSE)
    sol_droite.defiler(Donnees.SOL_VITESSE)
    
    mot.update_position(Donnees.SOL_VITESSE)
    mechant.update_position(Donnees.SOL_VITESSE)

    # Gestion de l'animation du méchant
    frame_counter += 1
    if frame_counter >= mechant.animation_delay:
        frame_counter = 0
        if num_img == mechant.nb_images:
            num_img = 1
        else:
            num_img = num_img + 1
        
        # Mise à jour de l'image du méchant
        sprite_obstacle = Donnees.OBSTACLE_SKIN_DINO_VOLANT + str(num_img) + ".png"
        mechant.set_image(sprite_obstacle)

    # Affichage des éléments
    fenetre.afficher_fond(screen)
    sol_gauche.afficher(screen)
    sol_droite.afficher(screen)
    man.afficher(screen)
    mechant.afficher(screen)
    mot.afficher(screen)

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(Donnees.FPS)